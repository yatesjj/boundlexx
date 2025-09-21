#!/usr/bin/env python3
"""
Steam Authentication Monitoring Dashboard

Real-time monitoring and metrics collection for Steam + Boundless authentication:
- 2FA frequency tracking
- Authentication performance metrics  
- Session persistence monitoring
- Query token cache efficiency
- Health status alerts
- Historical trend analysis

Usage:
    python auth_monitoring.py --mode dashboard    # Interactive dashboard
    python auth_monitoring.py --mode collect      # Collect metrics only
    python auth_monitoring.py --mode report       # Generate report
    python auth_monitoring.py --mode alert        # Check alerts
"""

import os
import sys
import time
import json
import argparse
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import sqlite3
import statistics

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

import django
django.setup()

from django.conf import settings
from django.core.cache import cache
from boundlexx.boundless.game.client import BoundlessClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class AuthMetrics:
    """Authentication metrics snapshot"""
    timestamp: float
    steam_auth_time: float
    query_token_time: float
    total_auth_time: float
    cache_hit: bool
    steam_2fa_required: bool
    success: bool
    error_details: Optional[str] = None
    account_used: Optional[str] = None

@dataclass
class SessionMetrics:
    """Steam session persistence metrics"""
    timestamp: float
    session_active: bool
    sentry_files_count: int
    session_age_hours: float
    tickets_generated: int
    last_2fa_time: Optional[float] = None

@dataclass
class SystemHealth:
    """Overall system health status"""
    timestamp: float
    auth_success_rate: float
    avg_auth_time: float
    cache_hit_rate: float
    active_sessions: int
    alerts: List[str]

class AuthMetricsCollector:
    """Collect and store authentication metrics"""
    
    def __init__(self, db_path: str = "/app/auth_metrics.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database for metrics storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Auth metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS auth_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                steam_auth_time REAL,
                query_token_time REAL,
                total_auth_time REAL,
                cache_hit BOOLEAN,
                steam_2fa_required BOOLEAN,
                success BOOLEAN,
                error_details TEXT,
                account_used TEXT
            )
        """)
        
        # Session metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS session_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                session_active BOOLEAN,
                sentry_files_count INTEGER,
                session_age_hours REAL,
                tickets_generated INTEGER,
                last_2fa_time REAL
            )
        """)
        
        # System health table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_health (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                auth_success_rate REAL,
                avg_auth_time REAL,
                cache_hit_rate REAL,
                active_sessions INTEGER,
                alerts TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        
    def test_authentication(self) -> AuthMetrics:
        """Test authentication and collect metrics"""
        start_time = time.time()
        
        metrics = AuthMetrics(
            timestamp=start_time,
            steam_auth_time=0.0,
            query_token_time=0.0,
            total_auth_time=0.0,
            cache_hit=False,
            steam_2fa_required=False,
            success=False
        )
        
        try:
            # Initialize client
            client = BoundlessClient()
            user = client.user
            metrics.account_used = user['boundless']['username']
            
            # Clear cache to test fresh auth
            cache_key = f"boundless_client:query_token:{user['boundless']['username']}"
            cache.delete(cache_key)
            
            # Test authentication
            auth_start = time.time()
            query_token = client.query_token
            metrics.query_token_time = time.time() - auth_start
            
            # Test cache hit
            cache_start = time.time()
            cached_token = client.query_token
            cache_time = time.time() - cache_start
            
            metrics.cache_hit = cache_time < 0.1  # Sub-100ms indicates cache hit
            metrics.total_auth_time = time.time() - start_time
            metrics.success = True
            
            logger.info(f"✅ Auth test: {metrics.total_auth_time:.2f}s (cache: {metrics.cache_hit})")
            
        except Exception as e:
            metrics.error_details = str(e)
            metrics.total_auth_time = time.time() - start_time
            logger.error(f"❌ Auth test failed: {e}")
            
        return metrics
        
    def collect_session_metrics(self) -> SessionMetrics:
        """Collect Steam session persistence metrics"""
        timestamp = time.time()
        
        # Check .steam directory
        steam_dir = "/app/.steam"
        sentry_files = 0
        session_active = False
        session_age_hours = 0.0
        
        if os.path.exists(steam_dir):
            sentry_files = len([f for f in os.listdir(steam_dir) if f.endswith('.bin')])
            
            # Check for active session files
            session_files = ['cm_servers.json', 'loginusers.json']
            active_files = [f for f in session_files if os.path.exists(os.path.join(steam_dir, f))]
            session_active = len(active_files) > 0
            
            # Calculate session age from oldest file
            if active_files:
                oldest_time = min(
                    os.path.getmtime(os.path.join(steam_dir, f)) 
                    for f in active_files
                )
                session_age_hours = (timestamp - oldest_time) / 3600
                
        return SessionMetrics(
            timestamp=timestamp,
            session_active=session_active,
            sentry_files_count=sentry_files,
            session_age_hours=session_age_hours,
            tickets_generated=0  # Would need to track this separately
        )
        
    def store_metrics(self, auth_metrics: AuthMetrics, session_metrics: SessionMetrics):
        """Store metrics in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Store auth metrics
        cursor.execute("""
            INSERT INTO auth_metrics (
                timestamp, steam_auth_time, query_token_time, total_auth_time,
                cache_hit, steam_2fa_required, success, error_details, account_used
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            auth_metrics.timestamp,
            auth_metrics.steam_auth_time,
            auth_metrics.query_token_time,
            auth_metrics.total_auth_time,
            auth_metrics.cache_hit,
            auth_metrics.steam_2fa_required,
            auth_metrics.success,
            auth_metrics.error_details,
            auth_metrics.account_used
        ))
        
        # Store session metrics
        cursor.execute("""
            INSERT INTO session_metrics (
                timestamp, session_active, sentry_files_count,
                session_age_hours, tickets_generated, last_2fa_time
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            session_metrics.timestamp,
            session_metrics.session_active,
            session_metrics.sentry_files_count,
            session_metrics.session_age_hours,
            session_metrics.tickets_generated,
            session_metrics.last_2fa_time
        ))
        
        conn.commit()
        conn.close()
        
    def get_recent_metrics(self, hours: int = 24) -> Tuple[List[AuthMetrics], List[SessionMetrics]]:
        """Get metrics from the last N hours"""
        since = time.time() - (hours * 3600)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get auth metrics
        cursor.execute("""
            SELECT * FROM auth_metrics 
            WHERE timestamp > ? 
            ORDER BY timestamp DESC
        """, (since,))
        
        auth_data = cursor.fetchall()
        auth_metrics = [
            AuthMetrics(
                timestamp=row[1],
                steam_auth_time=row[2],
                query_token_time=row[3],
                total_auth_time=row[4],
                cache_hit=bool(row[5]),
                steam_2fa_required=bool(row[6]),
                success=bool(row[7]),
                error_details=row[8],
                account_used=row[9]
            )
            for row in auth_data
        ]
        
        # Get session metrics
        cursor.execute("""
            SELECT * FROM session_metrics 
            WHERE timestamp > ? 
            ORDER BY timestamp DESC
        """, (since,))
        
        session_data = cursor.fetchall()
        session_metrics = [
            SessionMetrics(
                timestamp=row[1],
                session_active=bool(row[2]),
                sentry_files_count=row[3],
                session_age_hours=row[4],
                tickets_generated=row[5],
                last_2fa_time=row[6]
            )
            for row in session_data
        ]
        
        conn.close()
        return auth_metrics, session_metrics

class AuthMonitoringDashboard:
    """Interactive monitoring dashboard"""
    
    def __init__(self, collector: AuthMetricsCollector):
        self.collector = collector
        
    def calculate_health_status(self, hours: int = 24) -> SystemHealth:
        """Calculate overall system health"""
        auth_metrics, session_metrics = self.collector.get_recent_metrics(hours)
        
        if not auth_metrics:
            return SystemHealth(
                timestamp=time.time(),
                auth_success_rate=0.0,
                avg_auth_time=0.0,
                cache_hit_rate=0.0,
                active_sessions=0,
                alerts=["No recent metrics available"]
            )
            
        # Calculate success rate
        successful = sum(1 for m in auth_metrics if m.success)
        auth_success_rate = (successful / len(auth_metrics)) * 100
        
        # Calculate average auth time
        auth_times = [m.total_auth_time for m in auth_metrics if m.success]
        avg_auth_time = statistics.mean(auth_times) if auth_times else 0.0
        
        # Calculate cache hit rate
        cache_hits = sum(1 for m in auth_metrics if m.cache_hit)
        cache_hit_rate = (cache_hits / len(auth_metrics)) * 100
        
        # Count active sessions
        recent_sessions = [s for s in session_metrics if s.session_active]
        active_sessions = len(set(s.timestamp for s in recent_sessions))
        
        # Generate alerts
        alerts = []
        if auth_success_rate < 95:
            alerts.append(f"Low success rate: {auth_success_rate:.1f}%")
        if avg_auth_time > 10:
            alerts.append(f"Slow authentication: {avg_auth_time:.1f}s")
        if cache_hit_rate < 80:
            alerts.append(f"Low cache hit rate: {cache_hit_rate:.1f}%")
        if not recent_sessions:
            alerts.append("No active Steam sessions detected")
            
        return SystemHealth(
            timestamp=time.time(),
            auth_success_rate=auth_success_rate,
            avg_auth_time=avg_auth_time,
            cache_hit_rate=cache_hit_rate,
            active_sessions=active_sessions,
            alerts=alerts
        )
        
    def display_dashboard(self):
        """Display real-time monitoring dashboard"""
        try:
            while True:
                # Clear screen
                os.system('clear' if os.name == 'posix' else 'cls')
                
                print("🔐 STEAM AUTHENTICATION MONITORING DASHBOARD")
                print("=" * 60)
                print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print()
                
                # Get recent metrics
                auth_metrics, session_metrics = self.collector.get_recent_metrics(24)
                health = self.calculate_health_status(24)
                
                # System Health Overview
                print("📊 SYSTEM HEALTH (24 Hours)")
                print("-" * 30)
                status_icon = "🟢" if not health.alerts else "🟡" if len(health.alerts) < 3 else "🔴"
                print(f"{status_icon} Overall Status: {'Healthy' if not health.alerts else 'Warning' if len(health.alerts) < 3 else 'Critical'}")
                print(f"✅ Success Rate: {health.auth_success_rate:.1f}%")
                print(f"⚡ Avg Auth Time: {health.avg_auth_time:.2f}s")
                print(f"💾 Cache Hit Rate: {health.cache_hit_rate:.1f}%")
                print(f"🔗 Active Sessions: {health.active_sessions}")
                print()
                
                # Recent Authentication Performance
                if auth_metrics:
                    recent_auth = auth_metrics[:5]
                    print("🚀 RECENT AUTHENTICATION TESTS")
                    print("-" * 40)
                    for auth in recent_auth:
                        timestamp = datetime.fromtimestamp(auth.timestamp).strftime('%H:%M:%S')
                        status = "✅" if auth.success else "❌"
                        cache_status = "💾" if auth.cache_hit else "🔄"
                        print(f"{timestamp} | {status} | {auth.total_auth_time:.2f}s | {cache_status} | {auth.account_used or 'Unknown'}")
                    print()
                
                # Steam Session Status
                if session_metrics:
                    latest_session = session_metrics[0]
                    print("🎮 STEAM SESSION STATUS")
                    print("-" * 25)
                    session_icon = "🟢" if latest_session.session_active else "🔴"
                    print(f"{session_icon} Session Active: {latest_session.session_active}")
                    print(f"📁 Sentry Files: {latest_session.sentry_files_count}")
                    print(f"⏰ Session Age: {latest_session.session_age_hours:.1f} hours")
                    print()
                
                # Performance Trends
                if len(auth_metrics) > 1:
                    recent_times = [m.total_auth_time for m in auth_metrics[:10] if m.success]
                    if recent_times:
                        avg_recent = statistics.mean(recent_times)
                        baseline_improvement = ((20 - avg_recent) / 20) * 100
                        print("📈 PERFORMANCE TRENDS")
                        print("-" * 22)
                        print(f"🚀 Speed vs Baseline: {baseline_improvement:.0f}% faster")
                        print(f"📊 Recent Avg: {avg_recent:.2f}s")
                        if len(recent_times) > 1:
                            trend = "📈" if recent_times[0] < recent_times[-1] else "📉"
                            print(f"{trend} Trend: {'Improving' if recent_times[0] < recent_times[-1] else 'Stable/Declining'}")
                        print()
                
                # Alerts
                if health.alerts:
                    print("🚨 ALERTS")
                    print("-" * 10)
                    for alert in health.alerts:
                        print(f"⚠️  {alert}")
                    print()
                
                # Quick Actions
                print("🔧 QUICK ACTIONS")
                print("-" * 15)
                print("Press Ctrl+C to exit")
                print("Check logs: tail -f /app/logs/steam_auth.log")
                print("Test auth: python test_boundless_integration.py")
                
                # Update every 30 seconds
                time.sleep(30)
                
        except KeyboardInterrupt:
            print("\n👋 Dashboard stopped by user")
            
    def generate_report(self, hours: int = 24) -> str:
        """Generate detailed performance report"""
        auth_metrics, session_metrics = self.collector.get_recent_metrics(hours)
        health = self.calculate_health_status(hours)
        
        report = f"""
🔐 STEAM AUTHENTICATION MONITORING REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Period: Last {hours} hours
{'=' * 50}

EXECUTIVE SUMMARY:
- System Status: {'🟢 Healthy' if not health.alerts else '🟡 Warning' if len(health.alerts) < 3 else '🔴 Critical'}
- Authentication Success Rate: {health.auth_success_rate:.1f}%
- Average Authentication Time: {health.avg_auth_time:.2f}s
- Cache Efficiency: {health.cache_hit_rate:.1f}%
- Active Steam Sessions: {health.active_sessions}

PERFORMANCE METRICS:
"""
        
        if auth_metrics:
            successful_auths = [m for m in auth_metrics if m.success]
            if successful_auths:
                auth_times = [m.total_auth_time for m in successful_auths]
                report += f"- Total Authentication Tests: {len(auth_metrics)}\n"
                report += f"- Successful Tests: {len(successful_auths)}\n"
                report += f"- Fastest Authentication: {min(auth_times):.2f}s\n"
                report += f"- Slowest Authentication: {max(auth_times):.2f}s\n"
                report += f"- Median Authentication Time: {statistics.median(auth_times):.2f}s\n"
                
                # Performance vs baseline
                baseline_improvement = ((20 - health.avg_auth_time) / 20) * 100
                report += f"- Performance vs 2FA Baseline: {baseline_improvement:.0f}% faster\n"
                
                # Cache performance
                cache_hits = sum(1 for m in auth_metrics if m.cache_hit)
                report += f"- Cache Hits: {cache_hits}/{len(auth_metrics)} ({health.cache_hit_rate:.1f}%)\n"
        
        report += "\nSTEAM SESSION ANALYSIS:\n"
        if session_metrics:
            active_sessions = [s for s in session_metrics if s.session_active]
            if active_sessions:
                latest = active_sessions[0]
                report += f"- Current Session Age: {latest.session_age_hours:.1f} hours\n"
                report += f"- Sentry Files Available: {latest.sentry_files_count}\n"
                report += f"- Session Persistence: {'✅ Working' if latest.session_active else '❌ Failed'}\n"
                
                # 2FA frequency analysis
                session_hours = [s.session_age_hours for s in active_sessions]
                avg_session_age = statistics.mean(session_hours)
                if avg_session_age > 12:  # Sessions lasting > 12 hours indicate good persistence
                    report += f"- 2FA Frequency: 🟢 Low (sessions lasting {avg_session_age:.1f}h avg)\n"
                elif avg_session_age > 4:
                    report += f"- 2FA Frequency: 🟡 Moderate (sessions lasting {avg_session_age:.1f}h avg)\n"
                else:
                    report += f"- 2FA Frequency: 🔴 High (sessions lasting {avg_session_age:.1f}h avg)\n"
        
        if health.alerts:
            report += f"\nALERTS AND ISSUES:\n"
            for i, alert in enumerate(health.alerts, 1):
                report += f"{i}. {alert}\n"
        else:
            report += "\n✅ NO ALERTS - SYSTEM OPERATING NORMALLY\n"
        
        report += f"\nRECOMMENDations:\n"
        if health.auth_success_rate < 95:
            report += "- Investigate authentication failures\n"
            report += "- Check Steam credentials and network connectivity\n"
        if health.avg_auth_time > 5:
            report += "- Steam sessions may be requiring 2FA\n"
            report += "- Verify .steam directory persistence\n"
        if health.cache_hit_rate < 80:
            report += "- Query token caching may not be working optimally\n"
            report += "- Check cache backend configuration\n"
        if not health.alerts:
            report += "- System is performing optimally\n"
            report += "- Continue monitoring for trending analysis\n"
            
        return report

def main():
    """Main monitoring application"""
    parser = argparse.ArgumentParser(description="Steam Authentication Monitoring")
    parser.add_argument(
        '--mode', 
        choices=['dashboard', 'collect', 'report', 'alert'],
        default='dashboard',
        help='Operation mode'
    )
    parser.add_argument(
        '--hours', 
        type=int, 
        default=24,
        help='Hours of history to analyze'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=300,  # 5 minutes
        help='Collection interval in seconds'
    )
    
    args = parser.parse_args()
    
    collector = AuthMetricsCollector()
    dashboard = AuthMonitoringDashboard(collector)
    
    try:
        if args.mode == 'dashboard':
            print("🚀 Starting Authentication Monitoring Dashboard...")
            dashboard.display_dashboard()
            
        elif args.mode == 'collect':
            print(f"📊 Collecting metrics every {args.interval} seconds...")
            while True:
                auth_metrics = collector.test_authentication()
                session_metrics = collector.collect_session_metrics()
                collector.store_metrics(auth_metrics, session_metrics)
                
                status = "✅" if auth_metrics.success else "❌"
                print(f"{datetime.now().strftime('%H:%M:%S')} | {status} | {auth_metrics.total_auth_time:.2f}s")
                
                time.sleep(args.interval)
                
        elif args.mode == 'report':
            print(f"📄 Generating {args.hours}-hour performance report...")
            report = dashboard.generate_report(args.hours)
            print(report)
            
            # Save to file
            filename = f"/app/auth_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(report)
            print(f"\n📁 Report saved to: {filename}")
            
        elif args.mode == 'alert':
            print("🚨 Checking system health for alerts...")
            health = dashboard.calculate_health_status(args.hours)
            
            if health.alerts:
                print(f"⚠️  {len(health.alerts)} alerts found:")
                for alert in health.alerts:
                    print(f"   - {alert}")
                sys.exit(1)
            else:
                print("✅ No alerts - system healthy")
                sys.exit(0)
                
    except KeyboardInterrupt:
        print("\n👋 Monitoring stopped by user")
    except Exception as e:
        logger.error(f"💥 Monitoring error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()