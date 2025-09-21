#!/usr/bin/env python3
"""
Advanced Steam authentication test with event listening for sentry file creation.

This test listens for Steam client events to understand the sentry file creation process.
"""

import os
import sys
import time
import threading
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, '/app')

# Set up Django environment
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from steam.client import SteamClient
from steam.enums import EResult
from django.conf import settings

class SteamAuthTester:
    def __init__(self):
        self.client = None
        self.events_received = []
        self.login_key_received = False
        self.sentry_dir = '/app/.steam'

    def setup_event_listeners(self):
        """Set up event listeners for Steam client events."""

        @self.client.on(self.client.EVENT_NEW_LOGIN_KEY)
        def on_new_login_key(login_key):
            print(f"🔑 NEW_LOGIN_KEY event received: {login_key}")
            self.events_received.append(('NEW_LOGIN_KEY', login_key))
            self.login_key_received = True

        @self.client.on(self.client.EVENT_LOGGED_ON)
        def on_logged_on():
            print(f"✅ LOGGED_ON event received")
            self.events_received.append(('LOGGED_ON', None))

        @self.client.on(self.client.EVENT_AUTH_CODE_REQUIRED)
        def on_auth_code_required(is_2fa, code_mismatch):
            print(f"🔐 AUTH_CODE_REQUIRED event: 2FA={is_2fa}, mismatch={code_mismatch}")
            self.events_received.append(('AUTH_CODE_REQUIRED', (is_2fa, code_mismatch)))

        print("📡 Event listeners configured")

    def test_authentication_with_events(self, username: str, password: str):
        """Test Steam authentication with comprehensive event monitoring."""
        print(f"🔐 Testing Steam authentication with events for: {username}")
        print("=" * 60)

        # Initialize client
        self.client = SteamClient()
        self.client.set_credential_location(self.sentry_dir)

        # Set up event listeners
        self.setup_event_listeners()

        # Check initial sentry status
        sentry_path = self.client._get_sentry_path(username)
        print(f"📁 Expected sentry path: {sentry_path}")
        print(f"📍 Sentry exists before auth: {os.path.exists(sentry_path)}")

        # Check relogin availability
        print(f"🔄 Relogin available: {self.client.relogin_available}")

        print()
        print("🚀 Starting authentication process...")

        try:
            # Try relogin first
            if self.client.relogin_available:
                print("📋 Attempting relogin...")
                result = self.client.relogin()
                print(f"🔄 Relogin result: {result}")
            else:
                print("📋 No relogin available, trying fresh login...")

                # Connect to Steam
                print("📡 Connecting to Steam...")
                connect_result = self.client.connect()
                print(f"🔗 Connect result: {connect_result}")

                # Attempt login
                print("🔑 Attempting login...")
                result = self.client.login(username, password)
                print(f"🔐 Login result: {result}")

                # If login fails with 2FA requirement, use cli_login
                if result in [EResult.AccountLoginDeniedNeedTwoFactor, EResult.AccountLogonDenied]:
                    print("🛡️ 2FA required, switching to cli_login...")
                    result = self.client.cli_login(username, password)
                    print(f"🔐 CLI login result: {result}")

            if result == EResult.OK:
                print("✅ Authentication successful!")
                print(f"🔗 Client logged on: {self.client.logged_on}")
                print(f"👤 Steam ID: {self.client.steam_id}")

                # Wait for events and sentry file creation
                print()
                print("⏳ Waiting for events and sentry file creation...")

                for i in range(20):  # Wait up to 20 seconds
                    time.sleep(1)

                    # Check for events
                    if self.events_received:
                        print(f"📨 Events received so far: {len(self.events_received)}")
                        for event_type, data in self.events_received:
                            print(f"   - {event_type}: {data}")

                    # Check sentry file
                    if os.path.exists(sentry_path):
                        print(f"✅ Sentry file created: {sentry_path}")
                        stat = os.stat(sentry_path)
                        print(f"📊 Sentry file size: {stat.st_size} bytes")
                        break

                    if i % 5 == 0:
                        print(f"⏰ Still waiting... ({i}/20 seconds)")

                # Final status check
                print()
                print("📊 Final Status:")
                print(f"   Sentry exists: {os.path.exists(sentry_path)}")
                print(f"   Relogin available: {self.client.relogin_available}")
                print(f"   Events received: {len(self.events_received)}")
                print(f"   Login key received: {self.login_key_received}")

                # Test session ticket generation
                print()
                print("🎫 Testing session ticket generation...")
                try:
                    app_ticket = self.client.get_app_ticket(324510)  # Boundless
                    if app_ticket and hasattr(app_ticket, 'ticket'):
                        print(f"✅ App ticket generated: {len(app_ticket.ticket)} bytes")
                        return True
                    else:
                        print("❌ Failed to generate app ticket")
                        return False
                except Exception as e:
                    print(f"❌ App ticket error: {e}")
                    return False

            else:
                print(f"❌ Authentication failed: {result}")
                return False

        except Exception as e:
            print(f"💥 Authentication error: {e}")
            import traceback
            traceback.print_exc()
            return False

        finally:
            # Don't logout - preserve session for sentry files
            print("🔄 Preserving session (not calling logout)")

def main():
    """Main test runner."""
    # Get credentials
    steam_users = getattr(settings, 'STEAM_USERNAMES', [])
    steam_passes = getattr(settings, 'STEAM_PASSWORDS', [])

    if not steam_users or not steam_passes:
        print("❌ No Steam credentials configured")
        return False

    username = steam_users[0]
    password = steam_passes[0]

    # Run the test
    tester = SteamAuthTester()
    success = tester.test_authentication_with_events(username, password)

    print()
    print("=" * 60)
    print("📋 Test Summary:")
    if success:
        print("   ✅ Authentication successful")
        print("   ✅ Session ticket generated")
        print("   ✅ Implementation working")
    else:
        print("   ⚠️  Authentication issues detected")
        print("   ✅ Debugging information collected")

    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
