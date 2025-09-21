#!/usr/bin/env python3
"""
Test persistent Steam client session without sentry files.

This tests whether we can keep a Steam client session alive across
multiple session ticket requests to reduce 2FA frequency.
"""

import os
import sys
import time

# Add the app directory to Python path
sys.path.insert(0, '/app')

# Set up Django environment
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from steam.client import SteamClient
from steam.enums import EResult
from django.conf import settings

class PersistentSteamClient:
    """Test persistent Steam client without logout."""

    def __init__(self):
        self.client = None
        self.authenticated = False
        self.username = None

    def authenticate_once(self, username: str, password: str) -> bool:
        """Authenticate once and keep session alive."""
        print(f"🔐 Authenticating Steam client for {username}...")

        self.client = SteamClient()
        self.client.set_credential_location('/app/.steam')

        try:
            print("📡 Connecting to Steam...")
            self.client.connect()

            print("🔑 Attempting login...")
            result = self.client.login(username, password)

            if result in [EResult.AccountLoginDeniedNeedTwoFactor, EResult.AccountLogonDenied]:
                print("🛡️ 2FA required, using cli_login...")
                result = self.client.cli_login(username, password)

            if result == EResult.OK and self.client.logged_on:
                print("✅ Authentication successful!")
                print(f"👤 Steam ID: {self.client.steam_id}")
                self.authenticated = True
                self.username = username
                return True
            else:
                print(f"❌ Authentication failed: {result}")
                return False

        except Exception as e:
            print(f"💥 Authentication error: {e}")
            return False

    def get_session_ticket(self, attempt_num: int) -> str:
        """Get session ticket using existing authentication."""
        print(f"🎫 Attempt #{attempt_num}: Getting session ticket...")

        if not self.authenticated or not self.client or not self.client.logged_on:
            print("❌ Client not authenticated")
            return None

        try:
            start_time = time.time()
            response = self.client.get_app_ticket(324510)  # Boundless
            ticket_time = time.time() - start_time

            if response and hasattr(response, 'ticket'):
                ticket_hex = response.ticket.hex()
                print(f"✅ Session ticket generated in {ticket_time:.2f}s")
                print(f"📊 Ticket length: {len(ticket_hex)} characters")
                print(f"📄 Ticket preview: {ticket_hex[:20]}...")
                return ticket_hex
            else:
                print("❌ Failed to get session ticket")
                return None

        except Exception as e:
            print(f"💥 Session ticket error: {e}")
            return None

    def cleanup(self):
        """Clean up client connection."""
        print("🧹 Cleaning up client connection...")
        if self.client and self.client.logged_on:
            # NOTE: We're testing WITHOUT logout to see if session persists
            print("🔄 Keeping session alive (not calling logout)")
            # self.client.logout()  # Commented out for testing
        else:
            print("ℹ️  Client was not logged on")

def test_persistent_session():
    """Test persistent Steam session approach."""
    print("🧪 Testing Persistent Steam Session Approach")
    print("=" * 60)

    # Get credentials
    steam_users = getattr(settings, 'STEAM_USERNAMES', [])
    steam_passes = getattr(settings, 'STEAM_PASSWORDS', [])

    if not steam_users or not steam_passes:
        print("❌ No Steam credentials configured")
        return False

    username = steam_users[0]
    password = steam_passes[0]

    # Create persistent client
    steam_client = PersistentSteamClient()

    try:
        # Step 1: Authenticate once (may require 2FA)
        print("📋 Step 1: Initial Authentication")
        auth_success = steam_client.authenticate_once(username, password)

        if not auth_success:
            print("❌ Initial authentication failed")
            return False

        print()

        # Step 2: Test multiple session ticket requests
        print("📋 Step 2: Multiple Session Ticket Requests")
        print("Testing if we can get multiple tickets without re-authentication...")

        tickets = []
        times = []

        for i in range(5):
            print(f"\n🎫 Request {i+1}/5:")

            start_time = time.time()
            ticket = steam_client.get_session_ticket(i+1)
            request_time = time.time() - start_time

            if ticket:
                tickets.append(ticket)
                times.append(request_time)
                print(f"⏱️  Total request time: {request_time:.2f}s")
            else:
                print("❌ Failed to get session ticket")
                break

            # Small delay between requests
            if i < 4:
                time.sleep(2)

        # Step 3: Analyze results
        print("\n📊 Results Analysis:")
        print("=" * 40)
        print(f"✅ Successful ticket requests: {len(tickets)}/5")
        print(f"⏱️  Average request time: {sum(times)/len(times):.2f}s")
        print(f"🎫 All tickets unique: {len(set(tickets)) == len(tickets)}")

        if len(tickets) >= 3:
            print("🎉 SUCCESS: Persistent session working!")
            print("   - Multiple tickets generated without re-authentication")
            print("   - No additional 2FA prompts required")
            print("   - Session remains active across requests")
            return True
        else:
            print("⚠️  Partial success: Some tickets generated")
            return False

    finally:
        steam_client.cleanup()

def main():
    """Main test runner."""
    try:
        success = test_persistent_session()

        print("\n🔮 Conclusions:")
        if success:
            print("✅ Persistent session approach is VIABLE!")
            print("   - Keep Steam client alive without logout()")
            print("   - Generate multiple session tickets from one authentication")
            print("   - Significantly reduces 2FA frequency")
            print()
            print("💡 Implementation Strategy:")
            print("   1. Authenticate Steam client once (with 2FA)")
            print("   2. Keep client instance alive (no logout)")
            print("   3. Generate session tickets on demand")
            print("   4. Re-authenticate only when session expires")
        else:
            print("⚠️  Persistent session has limitations")
            print("   - May need different approach for production")
            print("   - Consider connection pooling or other strategies")

        return success

    except KeyboardInterrupt:
        print("\n🛑 Test interrupted")
        return False
    except Exception as e:
        print(f"\n💥 Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
