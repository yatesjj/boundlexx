#!/usr/bin/env python3
"""
Combined Steam and Boundless Authentication Test

This script tests the complete authentication chain:
1. Steam authentication → session ticket
2. Boundless authentication → JWT token
3. Combined authentication → query token
4. Test API call with authenticated client

Usage:
    python test_combined_auth.py
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

import logging
from django.conf import settings
from boundlexx.boundless.game.client import BoundlessClient
from boundlexx.boundless.game.steam_auth_pure_python import get_steam_session_ticket_pure_python

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_steam_authentication():
    """Test Steam authentication directly."""
    print("\n🎮 TESTING STEAM AUTHENTICATION")
    print("=" * 50)

    if not hasattr(settings, 'STEAM_USERNAMES') or not settings.STEAM_USERNAMES:
        print("❌ STEAM_USERNAMES not configured in settings")
        return False

    steam_username = settings.STEAM_USERNAMES[0] if isinstance(settings.STEAM_USERNAMES, list) else settings.STEAM_USERNAMES.split(',')[0]
    steam_password = settings.STEAM_PASSWORDS[0] if isinstance(settings.STEAM_PASSWORDS, list) else settings.STEAM_PASSWORDS.split(',')[0]

    print(f"📧 Steam Username: {steam_username}")

    try:
        ticket = get_steam_session_ticket_pure_python(steam_username, steam_password)

        if ticket:
            print(f"✅ Steam authentication successful!")
            print(f"🎫 Session ticket length: {len(ticket)} characters")
            print(f"🎫 Ticket preview: {ticket[:50]}...")
            return True
        else:
            print("❌ Steam authentication failed - no ticket returned")
            return False

    except Exception as e:
        print(f"❌ Steam authentication error: {e}")
        return False

def test_boundless_authentication():
    """Test Boundless authentication directly."""
    print("\n🌍 TESTING BOUNDLESS AUTHENTICATION")
    print("=" * 50)

    if not hasattr(settings, 'BOUNDLESS_USERNAMES') or not settings.BOUNDLESS_USERNAMES:
        print("❌ BOUNDLESS_USERNAMES not configured in settings")
        return False

    boundless_username = settings.BOUNDLESS_USERNAMES[0] if isinstance(settings.BOUNDLESS_USERNAMES, list) else settings.BOUNDLESS_USERNAMES.split(',')[0]
    boundless_password = settings.BOUNDLESS_PASSWORDS[0] if isinstance(settings.BOUNDLESS_PASSWORDS, list) else settings.BOUNDLESS_PASSWORDS.split(',')[0]

    print(f"📧 Boundless Username: {boundless_username}")

    try:
        client = BoundlessClient()
        jwt_token = client._get_game_jwt(boundless_username, boundless_password)

        if jwt_token:
            print(f"✅ Boundless authentication successful!")
            print(f"🎟️ JWT token length: {len(jwt_token)} characters")
            print(f"🎟️ Token preview: {jwt_token[:50]}...")
            return True
        else:
            print("❌ Boundless authentication failed - no JWT returned")
            return False

    except Exception as e:
        print(f"❌ Boundless authentication error: {e}")
        return False

def test_combined_authentication():
    """Test combined authentication via BoundlessClient."""
    print("\n🔗 TESTING COMBINED AUTHENTICATION")
    print("=" * 50)

    try:
        client = BoundlessClient()

        print("🔄 Triggering query token generation (combines Steam + Boundless auth)...")
        query_token = client.query_token

        if query_token:
            print(f"✅ Combined authentication successful!")
            print(f"👤 Player: {query_token.player.get('name', 'Unknown')}")
            print(f"🆔 Player ID: {query_token.player.get('id', 'Unknown')}")
            print(f"🎫 Query token length: {len(query_token.token)} characters")
            print(f"🎫 Token preview: {query_token.token[:50]}...")
            print(f"👤 Username: {query_token.username}")
            return True, client
        else:
            print("❌ Combined authentication failed - no query token")
            return False, None

    except Exception as e:
        print(f"❌ Combined authentication error: {e}")
        return False, None

def test_api_call(client):
    """Test an actual API call with authenticated client."""
    print("\n🌐 TESTING API CALL WITH AUTHENTICATION")
    print("=" * 50)

    if not client:
        print("❌ No authenticated client available")
        return False

    try:
        # Try to get world data for a known world (world ID 1 is usually available)
        from boundlexx.boundless.game import World as SimpleWorld

        print("🔄 Attempting to fetch world data for world ID 1...")
        world_data = client.get_world_data(SimpleWorld(1, None))

        if world_data:
            print(f"✅ API call successful!")
            print(f"🌍 World data keys: {list(world_data.keys())}")

            if 'worldData' in world_data:
                world_info = world_data['worldData']
                print(f"🌍 World Name: {world_info.get('name', 'Unknown')}")
                print(f"🌍 World Type: {world_info.get('worldType', 'Unknown')}")
                print(f"🌍 World Status: {world_info.get('status', 'Unknown')}")

            return True
        else:
            print("❌ API call failed - no world data returned")
            return False

    except Exception as e:
        print(f"❌ API call error: {e}")
        return False

def main():
    """Run all authentication tests."""
    print("🚀 COMBINED STEAM + BOUNDLESS AUTHENTICATION TEST")
    print("=" * 60)

    # Check basic configuration
    print("\n⚙️ CONFIGURATION CHECK")
    print("=" * 30)
    print(f"🔧 BOUNDLESS_DS_REQUIRES_AUTH: {getattr(settings, 'BOUNDLESS_DS_REQUIRES_AUTH', False)}")
    print(f"🔧 BOUNDLESS_API_URL_BASE: {getattr(settings, 'BOUNDLESS_API_URL_BASE', 'Not set')}")
    print(f"🔧 Steam accounts configured: {len(getattr(settings, 'STEAM_USERNAMES', []))}")
    print(f"🔧 Boundless accounts configured: {len(getattr(settings, 'BOUNDLESS_USERNAMES', []))}")

    # Run individual tests
    steam_success = test_steam_authentication()
    boundless_success = test_boundless_authentication()

    # Run combined test
    combined_success, client = test_combined_authentication()

    # Test API call if combined auth worked
    api_success = False
    if combined_success:
        api_success = test_api_call(client)

    # Summary
    print("\n📊 TEST SUMMARY")
    print("=" * 30)
    print(f"🎮 Steam Authentication: {'✅ PASS' if steam_success else '❌ FAIL'}")
    print(f"🌍 Boundless Authentication: {'✅ PASS' if boundless_success else '❌ FAIL'}")
    print(f"🔗 Combined Authentication: {'✅ PASS' if combined_success else '❌ FAIL'}")
    print(f"🌐 API Call Test: {'✅ PASS' if api_success else '❌ FAIL'}")

    overall_success = all([steam_success, boundless_success, combined_success, api_success])
    print(f"\n🎯 OVERALL RESULT: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")

    if overall_success:
        print("\n🎉 Congratulations! Your Steam + Boundless authentication is fully functional!")
        print("🚀 Ready for production world discovery and data polling tasks.")
    else:
        print("\n🛠️ Please check the failed tests and verify your configuration:")
        print("   - .local.env file contains correct credentials")
        print("   - Steam Guard 2FA has been set up (run: python manage.py prompt_steam_guard)")
        print("   - Network connectivity to Steam and Boundless servers")

    return overall_success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        sys.exit(1)
