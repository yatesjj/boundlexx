#!/usr/bin/env python3

import os
import json
import requests
import django
from typing import Optional

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.conf import settings

def test_discovery_server_auth():
    """Test authentication with Boundless Discovery Server step by step"""

    print("=== Boundless Discovery Server Authentication Test ===")
    print(f"DS Base URL: {settings.BOUNDLESS_DS_URL}")
    print(f"Auth Required: {settings.BOUNDLESS_DS_REQUIRES_AUTH}")
    print()

    # Test 1: Check Discovery Server connectivity
    print("1. Testing Discovery Server connectivity...")
    try:
        response = requests.get(f"{settings.BOUNDLESS_DS_URL}/list-gameservers", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Game servers: {len(data.get('servers', []))} found")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Connection failed: {e}")
    print()

    if not settings.BOUNDLESS_DS_REQUIRES_AUTH:
        print("Authentication not required - skipping auth tests")
        return

    # Test 2: Get Boundless JWT
    print("2. Testing Boundless JWT authentication...")
    try:
        username = settings.BOUNDLESS_USERNAMES[0]
        password = settings.BOUNDLESS_PASSWORDS[0]

        jwt_response = requests.post(
            f"{settings.BOUNDLESS_ACCOUNTS_URL}/accounts/{username}/token/",
            data={"password": password},
            timeout=10
        )

        if jwt_response.status_code == 200:
            jwt_token = jwt_response.json()["token"]
            print(f"   ✅ JWT Success: {jwt_token[:20]}...{jwt_token[-10:]}")
        else:
            print(f"   ❌ JWT Failed: {jwt_response.status_code} - {jwt_response.text}")
            return
    except Exception as e:
        print(f"   ❌ JWT Error: {e}")
        return
    print()

    # Test 3: Get Steam session ticket
    print("3. Testing Steam session ticket...")
    try:
        from boundlexx.boundless.game.steam_auth_pure_python import get_steam_session_ticket_pure_python

        steam_username = settings.STEAM_USERNAMES[0]
        steam_password = settings.STEAM_PASSWORDS[0]

        print(f"   Authenticating Steam user: {steam_username}")
        steam_ticket = get_steam_session_ticket_pure_python(steam_username, steam_password)

        if steam_ticket:
            print(f"   ✅ Steam Success: {len(steam_ticket)} chars")
            print(f"   Ticket preview: {steam_ticket[:40]}...{steam_ticket[-20:]}")
        else:
            print("   ❌ Steam Failed: No ticket returned")
            return
    except Exception as e:
        print(f"   ❌ Steam Error: {e}")
        return
    print()

    # Test 4: Test Discovery Server login with both tokens
    print("4. Testing Discovery Server login...")
    try:
        login_data = {
            "authToken": jwt_token,
            "steamTicket": steam_ticket,
            "vcplatform": 1,
        }

        if settings.BOUNDLESS_TESTING_FEATURES:
            login_data["gameVersion"] = "testing"

        print(f"   Login payload keys: {list(login_data.keys())}")
        print(f"   authToken length: {len(login_data['authToken'])}")
        print(f"   steamTicket length: {len(login_data['steamTicket'])}")

        login_response = requests.post(
            f"{settings.BOUNDLESS_DS_URL}/login",
            data=json.dumps(login_data),
            headers={"content-type": "application/json"},
            timeout=30
        )

        print(f"   Status: {login_response.status_code}")

        if login_response.status_code == 200:
            query_token_data = login_response.json()
            print(f"   ✅ Login Success!")
            print(f"   Query token: {query_token_data}")
        else:
            print(f"   ❌ Login Failed: {login_response.text}")

            # Try to get more details
            print("   Response headers:", dict(login_response.headers))

    except Exception as e:
        print(f"   ❌ Login Error: {e}")
    print()

    # Test 5: Test without Steam ticket (Boundless-only auth)
    print("5. Testing Boundless-only authentication (without Steam)...")
    try:
        boundless_only_data = {
            "authToken": jwt_token,
            "vcplatform": 1,
        }

        if settings.BOUNDLESS_TESTING_FEATURES:
            boundless_only_data["gameVersion"] = "testing"

        boundless_response = requests.post(
            f"{settings.BOUNDLESS_DS_URL}/login",
            data=json.dumps(boundless_only_data),
            headers={"content-type": "application/json"},
            timeout=30
        )

        print(f"   Status: {boundless_response.status_code}")

        if boundless_response.status_code == 200:
            print(f"   ✅ Boundless-only auth works!")
        else:
            print(f"   ❌ Boundless-only failed: {boundless_response.text}")

    except Exception as e:
        print(f"   ❌ Boundless-only error: {e}")

if __name__ == "__main__":
    test_discovery_server_auth()
