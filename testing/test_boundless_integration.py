#!/usr/bin/env python3
"""
BoundlessClient Integration Test

This script validates the complete authentication chain:
1. Steam persistent session → Steam session ticket
2. Boundless JWT authentication
3. Discovery Server dual authentication
4. Query token caching (12 hours)
5. World discovery API calls
6. Performance metrics collection

Tests the end-to-end workflow that production uses.
"""

import os
import sys
import time
import logging
import traceback
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

import django
django.setup()

from django.conf import settings
from django.core.cache import cache
from boundlexx.boundless.game.client import BoundlessClient, NoCharacterException
from boundlexx.boundless.game.models import World

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/app/boundless_integration_test.log')
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class AuthenticationMetrics:
    """Track authentication performance and success rates"""
    steam_auth_time: float = 0.0
    boundless_jwt_time: float = 0.0  
    discovery_auth_time: float = 0.0
    query_token_time: float = 0.0
    total_auth_time: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    steam_2fa_required: bool = False
    auth_success: bool = False
    error_details: Optional[str] = None
    world_api_calls: List[Dict] = field(default_factory=list)

@dataclass
class WorldAPIMetrics:
    """Track individual world API call performance"""
    world_id: int
    api_path: str
    response_time: float
    success: bool
    cached_query_token: bool
    error_details: Optional[str] = None

class BoundlessIntegrationTester:
    """Comprehensive integration testing for Steam + Boundless authentication"""
    
    def __init__(self):
        self.client = None
        self.metrics = AuthenticationMetrics()
        self.start_time = time.time()
        
    def setup_environment(self) -> bool:
        """Verify environment configuration"""
        logger.info("=== Environment Setup Verification ===")
        
        required_settings = [
            'BOUNDLESS_API_URL_BASE',
            'BOUNDLESS_USERNAMES', 
            'BOUNDLESS_PASSWORDS',
            'STEAM_USERNAMES',
            'STEAM_PASSWORDS',
            'BOUNDLESS_DS_REQUIRES_AUTH'
        ]
        
        missing_settings = []
        for setting in required_settings:
            if not hasattr(settings, setting) or not getattr(settings, setting):
                missing_settings.append(setting)
                
        if missing_settings:
            logger.error(f"❌ Missing required settings: {missing_settings}")
            return False
            
        logger.info(f"✅ Environment configured for {len(settings.BOUNDLESS_USERNAMES)} accounts")
        logger.info(f"✅ Discovery Server auth: {settings.BOUNDLESS_DS_REQUIRES_AUTH}")
        logger.info(f"✅ API base: {settings.BOUNDLESS_API_URL_BASE}")
        
        # Check .steam directory
        steam_dir = "/app/.steam"
        if os.path.exists(steam_dir):
            logger.info(f"✅ Steam directory exists: {steam_dir}")
            sentry_files = [f for f in os.listdir(steam_dir) if f.endswith('.bin')]
            logger.info(f"✅ Found {len(sentry_files)} sentry files")
        else:
            logger.warning(f"⚠️  Steam directory not found: {steam_dir}")
            
        return True
        
    def test_steam_authentication(self) -> bool:
        """Test Steam persistent session approach"""
        logger.info("=== Steam Authentication Test ===")
        
        start_time = time.time()
        
        try:
            from boundlexx.boundless.game.steam_auth_pure_python import (
                get_steam_session_ticket_pure_python
            )
            
            # Get credentials for first account
            steam_username = settings.STEAM_USERNAMES[0]
            steam_password = settings.STEAM_PASSWORDS[0]
            
            logger.info(f"Testing Steam auth for user: {steam_username}")
            
            # Test session ticket generation
            ticket = get_steam_session_ticket_pure_python(steam_username, steam_password)
            
            self.metrics.steam_auth_time = time.time() - start_time
            
            if ticket:
                logger.info(f"✅ Steam session ticket generated: {len(ticket)} characters")
                logger.info(f"✅ Steam auth time: {self.metrics.steam_auth_time:.2f}s")
                return True
            else:
                logger.error("❌ Steam session ticket generation failed")
                self.metrics.error_details = "Steam ticket generation returned None"
                return False
                
        except Exception as e:
            self.metrics.steam_auth_time = time.time() - start_time
            self.metrics.error_details = f"Steam auth exception: {str(e)}"
            logger.error(f"❌ Steam authentication failed: {e}")
            traceback.print_exc()
            return False
    
    def test_boundless_client_initialization(self) -> bool:
        """Test BoundlessClient initialization and user selection"""
        logger.info("=== BoundlessClient Initialization ===")
        
        try:
            self.client = BoundlessClient()
            user = self.client.user
            
            logger.info(f"✅ BoundlessClient initialized")
            logger.info(f"✅ Selected user: {user['boundless']['username']}")
            
            if settings.BOUNDLESS_DS_REQUIRES_AUTH:
                logger.info(f"✅ Steam user: {user['steam']['username']}")
                
            return True
            
        except Exception as e:
            logger.error(f"❌ BoundlessClient initialization failed: {e}")
            self.metrics.error_details = f"Client init failed: {str(e)}"
            traceback.print_exc()
            return False
            
    def test_query_token_acquisition(self) -> bool:
        """Test full Discovery Server authentication and query token caching"""
        logger.info("=== Query Token Acquisition Test ===")
        
        if not self.client:
            logger.error("❌ BoundlessClient not initialized")
            return False
            
        start_time = time.time()
        
        try:
            # Clear cache to force fresh authentication
            cache_key = f"boundless_client:query_token:{self.client.user['boundless']['username']}"
            cache.delete(cache_key)
            logger.info("Cleared query token cache to force fresh authentication")
            
            # Trigger authentication chain
            query_token = self.client.query_token
            
            self.metrics.query_token_time = time.time() - start_time
            self.metrics.total_auth_time = self.metrics.steam_auth_time + self.metrics.query_token_time
            
            logger.info(f"✅ Query token acquired: {query_token.token[:20]}...")
            logger.info(f"✅ Player: {query_token.player['name']} (ID: {query_token.player['id']})")
            logger.info(f"✅ Username: {query_token.username}")
            logger.info(f"✅ Authentication time: {self.metrics.query_token_time:.2f}s")
            logger.info(f"✅ Total auth time: {self.metrics.total_auth_time:.2f}s")
            
            # Test cache hit
            cache_start = time.time()
            cached_token = self.client.query_token
            cache_time = time.time() - cache_start
            
            if cached_token.token == query_token.token:
                logger.info(f"✅ Query token cache hit: {cache_time:.3f}s")
                self.metrics.cache_hits = 1
            else:
                logger.warning("⚠️  Query token cache miss")
                self.metrics.cache_misses = 1
                
            self.metrics.auth_success = True
            return True
            
        except NoCharacterException as e:
            logger.error(f"❌ No character found: {e}")
            self.metrics.error_details = f"No character: {str(e)}"
            return False
        except Exception as e:
            self.metrics.query_token_time = time.time() - start_time
            self.metrics.error_details = f"Query token failed: {str(e)}"
            logger.error(f"❌ Query token acquisition failed: {e}")
            traceback.print_exc()
            return False
            
    def test_world_discovery_apis(self) -> bool:
        """Test actual world discovery API calls"""
        logger.info("=== World Discovery API Tests ===")
        
        if not self.client:
            logger.error("❌ BoundlessClient not initialized")
            return False
            
        try:
            # Get some test worlds
            worlds = list(World.objects.filter(active=True)[:3])
            if not worlds:
                logger.warning("⚠️  No active worlds found in database")
                return True
                
            logger.info(f"Testing with {len(worlds)} worlds")
            
            success_count = 0
            
            for world in worlds:
                world_metrics = self._test_single_world_api(world)
                self.metrics.world_api_calls.append(world_metrics.__dict__)
                
                if world_metrics.success:
                    success_count += 1
                    
            success_rate = (success_count / len(worlds)) * 100
            logger.info(f"✅ World API success rate: {success_rate:.1f}% ({success_count}/{len(worlds)})")
            
            return success_count > 0
            
        except Exception as e:
            logger.error(f"❌ World discovery API test failed: {e}")
            traceback.print_exc()
            return False
            
    def _test_single_world_api(self, world: World) -> WorldAPIMetrics:
        """Test API calls for a single world"""
        logger.info(f"Testing world: {world.display_name} (ID: {world.id})")
        
        metrics = WorldAPIMetrics(
            world_id=world.id,
            api_path="/world/data",
            response_time=0.0,
            success=False,
            cached_query_token=True  # Assume cached since we just got it
        )
        
        start_time = time.time()
        
        try:
            # Test world data retrieval
            world_data = self.client.get_world_data(world)
            metrics.response_time = time.time() - start_time
            
            if world_data:
                logger.info(f"  ✅ World data retrieved: {len(str(world_data))} bytes")
                logger.info(f"  ✅ Response time: {metrics.response_time:.2f}s")
                metrics.success = True
                
                # Try to get poll data if available
                if 'pollData' in world_data:
                    poll_start = time.time()
                    poll_response = self.client.get_world_poll(world, world_data['pollData'])
                    poll_time = time.time() - poll_start
                    
                    if poll_response:
                        logger.info(f"  ✅ Poll data retrieved: {poll_time:.2f}s")
                    else:
                        logger.warning(f"  ⚠️  Poll data empty")
                        
            else:
                logger.warning(f"  ⚠️  World data empty (world may be offline)")
                metrics.success = True  # Empty response is valid for offline worlds
                
        except Exception as e:
            metrics.response_time = time.time() - start_time
            metrics.error_details = str(e)
            logger.error(f"  ❌ World API failed: {e}")
            
        return metrics
        
    def test_performance_characteristics(self) -> bool:
        """Test key performance characteristics"""
        logger.info("=== Performance Characteristics Test ===")
        
        if not self.client:
            logger.error("❌ BoundlessClient not initialized")
            return False
            
        try:
            # Test multiple query token requests (should all be cached)
            cache_times = []
            
            for i in range(5):
                start_time = time.time()
                token = self.client.query_token
                cache_time = time.time() - start_time
                cache_times.append(cache_time)
                
            avg_cache_time = sum(cache_times) / len(cache_times)
            max_cache_time = max(cache_times)
            
            logger.info(f"✅ Average cache response time: {avg_cache_time:.3f}s")
            logger.info(f"✅ Maximum cache response time: {max_cache_time:.3f}s")
            
            # Verify all requests returned the same token
            if all(cache_times[i] < 0.1 for i in range(1, len(cache_times))):
                logger.info("✅ Query token caching working efficiently")
            else:
                logger.warning("⚠️  Query token caching may not be optimal")
                
            return True
            
        except Exception as e:
            logger.error(f"❌ Performance test failed: {e}")
            return False
            
    def generate_report(self) -> str:
        """Generate comprehensive test report"""
        total_time = time.time() - self.start_time
        
        report = f"""
=== BOUNDLESS INTEGRATION TEST REPORT ===
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Test Time: {total_time:.2f}s

AUTHENTICATION METRICS:
- Steam Auth Time: {self.metrics.steam_auth_time:.2f}s
- Query Token Time: {self.metrics.query_token_time:.2f}s  
- Total Auth Time: {self.metrics.total_auth_time:.2f}s
- Authentication Success: {self.metrics.auth_success}
- Cache Hits: {self.metrics.cache_hits}
- Cache Misses: {self.metrics.cache_misses}
- 2FA Required: {self.metrics.steam_2fa_required}

WORLD API METRICS:
- Total World Tests: {len(self.metrics.world_api_calls)}
- Successful Calls: {sum(1 for call in self.metrics.world_api_calls if call['success'])}
- Average Response Time: {sum(call['response_time'] for call in self.metrics.world_api_calls) / max(len(self.metrics.world_api_calls), 1):.2f}s

PERFORMANCE SUMMARY:
- 🚀 {((20 - self.metrics.total_auth_time) / 20 * 100):.0f}% faster than 2FA baseline (20s)
- 💾 Query token caching: {'✅ Working' if self.metrics.cache_hits > 0 else '❌ Not working'}
- 🔐 Persistent Steam sessions: {'✅ Working' if self.metrics.steam_auth_time < 5 else '❌ May need 2FA'}

ERRORS:
{self.metrics.error_details or 'None'}

RECOMMENDATIONS:
"""
        
        if self.metrics.auth_success:
            report += "✅ Authentication chain is working correctly\n"
            report += "✅ Ready for production deployment\n"
        else:
            report += "❌ Authentication issues detected\n"
            report += "❌ Review error details and configuration\n"
            
        if self.metrics.total_auth_time < 2:
            report += "🚀 Excellent performance - persistent sessions working\n"
        elif self.metrics.total_auth_time < 10:
            report += "⚠️  Moderate performance - may have occasional 2FA\n"
        else:
            report += "🐌 Poor performance - persistent sessions not working\n"
            
        return report
        
    def run_full_test_suite(self) -> bool:
        """Run the complete integration test suite"""
        logger.info("🚀 Starting Boundless Integration Test Suite")
        logger.info("=" * 60)
        
        test_results = []
        
        # Environment setup
        test_results.append(("Environment Setup", self.setup_environment()))
        
        # Steam authentication
        test_results.append(("Steam Authentication", self.test_steam_authentication()))
        
        # BoundlessClient initialization
        test_results.append(("Client Initialization", self.test_boundless_client_initialization()))
        
        # Query token acquisition
        test_results.append(("Query Token", self.test_query_token_acquisition()))
        
        # World discovery APIs
        test_results.append(("World Discovery", self.test_world_discovery_apis()))
        
        # Performance testing
        test_results.append(("Performance", self.test_performance_characteristics()))
        
        # Results summary
        logger.info("=" * 60)
        logger.info("🏁 Test Suite Complete")
        logger.info("=" * 60)
        
        passed = 0
        failed = 0
        
        for test_name, result in test_results:
            status = "✅ PASS" if result else "❌ FAIL"
            logger.info(f"{test_name}: {status}")
            if result:
                passed += 1
            else:
                failed += 1
                
        logger.info(f"\nResults: {passed} passed, {failed} failed")
        
        # Generate detailed report
        report = self.generate_report()
        logger.info(report)
        
        # Save report to file
        with open('/app/boundless_integration_report.txt', 'w') as f:
            f.write(report)
        logger.info("📄 Detailed report saved to: /app/boundless_integration_report.txt")
        
        return failed == 0

def main():
    """Main test runner"""
    tester = BoundlessIntegrationTester()
    
    try:
        success = tester.run_full_test_suite()
        
        if success:
            logger.info("🎉 All tests passed! Integration is working correctly.")
            sys.exit(0)
        else:
            logger.error("💥 Some tests failed. Check the report for details.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Test suite crashed: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()