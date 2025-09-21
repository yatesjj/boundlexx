# Steam Authentication Migration Guide

**Document Version**: 1.0
**Last Updated**: September 21, 2025
**Migration Target**: 21-Day Encrypted App Tickets
**Legacy Source**: Sentry File Based Authentication

## Overview

This guide provides step-by-step instructions for migrating from the obsolete sentry file based Steam authentication to the new 21-day encrypted app ticket implementation.

## Why Migrate?

### Legacy Issues (Sentry Files)
- ❌ **Deprecated**: Steam deprecated machine authentication server-side in 2023
- ❌ **Unreliable**: `ClientUpdateMachineAuth` events no longer sent by Steam servers
- ❌ **Security Risk**: Persistent credential storage on disk
- ❌ **Daily 2FA**: Required 2FA prompts every 24 hours

### New Implementation Benefits
- ✅ **21-Day Duration**: Encrypted app tickets valid for 21 days
- ✅ **95% 2FA Reduction**: From daily to once every 3 weeks
- ✅ **Official API**: Uses current Steam.py v1.4.4 methods
- ✅ **Production Ready**: Clean output, error handling, session management

## Migration Checklist

### 1. Remove Obsolete Code Patterns

#### ❌ Remove Sentry File Usage
```python
# REMOVE: Obsolete sentry file setup
client.set_credential_location("/path/to/sentry")

# REMOVE: Machine auth event handlers
@client.on("auth_code_required")
def auth_code_handler(is_2fa, code_mismatch):
    pass

@client.on("ClientUpdateMachineAuth")
def machine_auth_handler(sentry):
    pass
```

#### ❌ Remove Incorrect Import Patterns
```python
# REMOVE: This doesn't exist in Steam.py v1.4.4
from steam import Client

# REMOVE: Async patterns that don't exist
async def get_app_and_encrypted_ticket():
    boundless_app = await client.fetch_app(324510)
    return await boundless_app.encrypted_ticket()
```

### 2. Implement Current API Patterns

#### ✅ Use Correct Steam.py v1.4.4 API
```python
# CURRENT: Correct import
from steam.client import SteamClient
from steam.enums import EResult

# CURRENT: Proper initialization
client = SteamClient()

# CURRENT: Interactive 2FA login
result = client.cli_login(username, password)

# CURRENT: 21-day encrypted app tickets
encrypted_ticket = client.get_encrypted_app_ticket(324510, b'')

# CURRENT: Convert to hex format
if hasattr(encrypted_ticket, 'SerializeToString'):
    ticket_hex = encrypted_ticket.SerializeToString().hex()
else:
    ticket_hex = encrypted_ticket.hex()
```

### 3. Update Environment Configuration

#### Remove Sentry Directory Configuration
```bash
# REMOVE from environment files
STEAM_SENTRY_DIR=/path/to/sentry

# REMOVE sentry file cleanup scripts
rm -rf /path/to/sentry/*
```

#### Use Session File Configuration
```bash
# Session files are automatically managed in /app/.steam/
# No environment configuration needed
```

### 4. Update Django Integration

#### Old Pattern (Remove)
```python
# REMOVE: Old authentication patterns
def authenticate_steam_old(username, password):
    client = SteamClient()
    client.set_credential_location("/app/.steam")

    # Event handler setup...
    result = client.login(username, password)
    # Immediate logout preventing sentry persistence
    client.logout()
```

#### New Pattern (Implement)
```python
# CURRENT: Use production-ready authentication
from boundlexx.boundless.game.steam_session_ticket_auth import get_steam_authentication_for_boundless

def authenticate_steam_current(username, password):
    return get_steam_authentication_for_boundless(username, password)
```

### 5. Update Management Commands

#### Replace Custom Commands
```bash
# REMOVE obsolete commands (already cleaned up)
# - setup_steam_auth.py
# - setup_steam_auth_enhanced.py
# - setup_steam_official.py
# - steam_persistent_login.py
# - steam_session_ticket_auth.py (command version)
# - test_steam_session_ticket.py

# USE the production command
python manage.py prompt_steam_guard
```

### 6. Clean Up Test Files

All test/experimental files have been removed in the cleanup:
```bash
# These files were removed (reference for migration)
rm -f test_*.py debug_*.py explore_*.py steam_rate_limit_test.py
rm -f boundlexx/boundless/game/steam_auth_*.py
```

## File-by-File Migration

### Core Authentication Module
**File**: `boundlexx/boundless/game/steam_session_ticket_auth.py`
**Status**: ✅ **Keep - Production Ready**
- Contains correct 21-day encrypted ticket implementation
- Handles session persistence automatically
- Provides fallback to 24-hour tickets

### Management Command
**File**: `boundlexx/boundless/management/commands/prompt_steam_guard.py`
**Status**: ✅ **Keep - Production Ready**
- User-facing authentication command
- Clean output without Web API validation warnings
- Dynamic session duration display

### BoundlessClient Integration
**File**: `boundlexx/boundless/game/client.py`
**Action**: Update `_get_steam_session_ticket` method to use new authentication:

```python
def _get_steam_session_ticket(self, username, password):
    from boundlexx.boundless.game.steam_session_ticket_auth import get_steam_authentication_for_boundless
    return get_steam_authentication_for_boundless(username, password)
```

## Testing Migration

### 1. Clear Old Sessions
```bash
# Clear any old sentry files or sessions
python manage.py prompt_steam_guard --clear-session
```

### 2. Test Fresh Authentication
```bash
# Test new 21-day authentication
python manage.py prompt_steam_guard --test-tickets
```

### 3. Verify Session Duration
Expected output should show:
```
Sessions expire in ~21 days (encrypted app tickets)
```

### 4. Test BoundlessClient Integration
```python
from boundlexx.boundless.game.client import BoundlessClient
client = BoundlessClient()
# This should use the new authentication automatically
query_token = client.query_token
```

## Rollback Plan

If issues arise, you can temporarily revert to 24-hour tickets by modifying the authentication module to skip encrypted tickets:

```python
# Temporary rollback: comment out encrypted ticket attempt
# try:
#     encrypted_ticket = client.get_encrypted_app_ticket(324510, b'')
#     # ... encrypted ticket handling
# except Exception as e:

# Use standard tickets directly
ticket_response = client.get_app_ticket(324510)
```

## Validation Checklist

After migration, verify:

- [ ] **Authentication Works**: `python manage.py prompt_steam_guard` succeeds
- [ ] **21-Day Duration**: Output shows "~21 days" expiry
- [ ] **No Sentry References**: No `set_credential_location` calls in code
- [ ] **Clean Output**: No Web API validation warnings
- [ ] **Session Persistence**: Second run uses cached session (no 2FA)
- [ ] **BoundlessClient Integration**: Discovery Server authentication works
- [ ] **Error Handling**: Graceful fallback to 24-hour tickets

## Troubleshooting

### Issue: Import Errors
**Symptom**: `ImportError: cannot import name 'Client' from 'steam'`
**Solution**: Use `from steam.client import SteamClient` instead

### Issue: Method Not Found
**Symptom**: `AttributeError: 'SteamClient' object has no attribute 'fetch_app'`
**Solution**: Use `client.get_encrypted_app_ticket(324510, b'')` directly

### Issue: Session Not Persisting
**Symptom**: 2FA required every time
**Solution**: Ensure no `client.logout()` calls preventing session files

### Issue: 21-Day Tickets Not Working
**Symptom**: Falls back to 24-hour tickets consistently
**Solution**: Check Steam server status, verify Steam.py v1.4.4 installation

## Post-Migration Cleanup

### Remove Obsolete Documentation
All obsolete Steam documentation has been removed:
- `STEAM_SENTRY_IMPLEMENTATION_COMPLETE.md`
- `STEAM_AUTH_ANALYSIS.md`
- `STEAM_AUTHENTICATION_PRODUCTION.md`
- Various other experimental documentation files

### Update Team Documentation
- Point team to `docs/modernization/STEAM_AUTHENTICATION.md` for technical details
- Update any internal documentation referencing sentry files
- Inform team of new 21-day session duration

## Support

### Primary Documentation
- **Technical Guide**: `docs/modernization/STEAM_AUTHENTICATION.md`
- **Implementation Files**:
  - `boundlexx/boundless/game/steam_session_ticket_auth.py`
  - `boundlexx/boundless/management/commands/prompt_steam_guard.py`

### Official References
- **Steam.py v1.4.4**: https://steam-py.github.io/docs/latest/api/
- **Steamworks Partner**: https://partner.steamgames.com/doc/features/auth

---

**Migration Complete**: Once validation checklist is passed, the migration to 21-day encrypted app tickets is complete and the system is production-ready.
