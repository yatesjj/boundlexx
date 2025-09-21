#!/usr/bin/env python3
"""
Test script for validating Steam sentry file implementation.

This script tests the new sentry file persistence approach by:
1. Attempting authentication (may require 2FA first time)
2. Checking for sentry file creation
3. Testing relogin functionality on subsequent calls
4. Verifying session ticket generation works consistently

Usage:
    python test_sentry_implementation.py <username> <password>
"""

import os
import sys
import time
from pathlib import Path

# Add the app directory to Python path so we can import boundlexx modules
sys.path.insert(0, '/app')

# Set up Django environment
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from boundlexx.boundless.game.steam_auth_pure_python import PurePythonSteamAuth
from django.conf import settings

def test_sentry_implementation(username: str, password: str):
    """Test the sentry file implementation."""
    print("🧪 Testing Steam Sentry File Implementation")
    print("=" * 50)

    # Initialize auth with test settings
    auth = PurePythonSteamAuth()
    sentry_dir = auth.sentry_dir

    print(f"📁 Sentry directory: {sentry_dir}")
    print(f"🎮 Steam App ID: {auth.app_id}")
    print()

    # Test 1: Check initial sentry status
    print("🔍 Test 1: Initial sentry file check")
    sentry_files_before = list(Path(sentry_dir).glob("*"))
    print(f"   Existing sentry files: {len(sentry_files_before)}")
    for f in sentry_files_before:
        print(f"   - {f.name}")
    print()

    # Test 2: First authentication (may require 2FA)
    print("🔐 Test 2: First authentication attempt")
    print("   This may require 2FA if no valid sentry file exists...")

    start_time = time.time()
    ticket1 = auth.authenticate_with_2fa(username, password)
    auth_time1 = time.time() - start_time

    if ticket1:
        print(f"   ✅ Authentication successful! ({auth_time1:.2f}s)")
        print(f"   🎫 Ticket length: {len(ticket1)} characters")
        print(f"   🎫 Ticket preview: {ticket1[:16]}...")
    else:
        print("   ❌ Authentication failed!")
        return False
    print()

    # Test 3: Check sentry file creation
    print("🔍 Test 3: Sentry file creation check")
    sentry_files_after = list(Path(sentry_dir).glob("*"))
    print(f"   Sentry files after auth: {len(sentry_files_after)}")

    new_files = set(sentry_files_after) - set(sentry_files_before)
    if new_files:
        print("   ✅ New sentry files created:")
        for f in new_files:
            print(f"   - {f.name} ({f.stat().st_size} bytes)")
    else:
        print("   ⚠️  No new sentry files detected")
    print()

    # Test 4: Second authentication (should use sentry/relogin)
    print("🔄 Test 4: Second authentication (should be faster with sentry)")
    print("   This should use relogin() and skip 2FA...")

    # Create new auth instance to simulate fresh process
    auth2 = PurePythonSteamAuth()

    start_time = time.time()
    ticket2 = auth2.authenticate_with_2fa(username, password)
    auth_time2 = time.time() - start_time

    if ticket2:
        print(f"   ✅ Second authentication successful! ({auth_time2:.2f}s)")
        print(f"   🎫 Ticket length: {len(ticket2)} characters")
        print(f"   🎫 Ticket preview: {ticket2[:16]}...")

        # Compare performance
        speed_improvement = (auth_time1 - auth_time2) / auth_time1 * 100
        if auth_time2 < auth_time1:
            print(f"   🚀 Speed improvement: {speed_improvement:.1f}% faster!")
        else:
            print(f"   ⚠️  Second auth took longer (+{-speed_improvement:.1f}%)")
    else:
        print("   ❌ Second authentication failed!")
        return False
    print()

    # Test 5: Validate tickets are different (single-use)
    print("🔍 Test 5: Session ticket uniqueness check")
    if ticket1 != ticket2:
        print("   ✅ Tickets are unique (single-use confirmed)")
    else:
        print("   ⚠️  Tickets are identical (unexpected)")
    print()

    # Test 6: Summary and recommendations
    print("📊 Test Summary")
    print("=" * 50)
    print(f"   First auth time:  {auth_time1:.2f}s")
    print(f"   Second auth time: {auth_time2:.2f}s")
    print(f"   Sentry files:     {len(sentry_files_after)}")
    print(f"   Both tickets:     {'✅ Valid' if ticket1 and ticket2 else '❌ Invalid'}")

    if auth_time2 < 5.0:
        print("   🎉 SENTRY OPTIMIZATION WORKING! Fast relogin achieved.")
    elif auth_time2 < auth_time1:
        print("   ✅ Sentry optimization partially working (some improvement)")
    else:
        print("   ⚠️  Sentry optimization may not be working (no speed improvement)")

    print()
    print("🔮 Next Steps:")
    print("   1. Test this authentication in BoundlessClient")
    print("   2. Verify query_token caching works with sentry auth")
    print("   3. Monitor 2FA requirements in production")
    print("   4. Set up persistent sentry volume for containers")

    return True

def main():
    """Main test runner."""
    if len(sys.argv) != 3:
        print("Usage: python test_sentry_implementation.py <username> <password>")
        print()
        print("This will test the Steam sentry file implementation by:")
        print("1. Performing initial authentication (may require 2FA)")
        print("2. Checking sentry file creation")
        print("3. Testing relogin on second authentication")
        print("4. Measuring performance improvements")
        sys.exit(1)

    username, password = sys.argv[1], sys.argv[2]

    try:
        success = test_sentry_implementation(username, password)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
