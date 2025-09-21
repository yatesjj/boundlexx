"""
Pure Python Steam authentication implementation for Boundless.

This module provides Steam authentication functionality using the steam[client]
library, designed for Python 3.12 compatibility and robust 2FA handling.
"""

import logging
import os
import time
from typing import Optional

from django.conf import settings
from steam.client import SteamClient
from steam.enums import EResult

logger = logging.getLogger(__name__)


class SteamAuthenticationError(Exception):
    """Raised when Steam authentication fails."""
    pass


class PurePythonSteamAuth:
    """Steam authentication using steam[client] library."""

    def __init__(self):
        """Initialize Steam client with proper configuration."""
        self.client = None
        self.sentry_dir = getattr(settings, 'STEAM_SENTRY_DIR', '/tmp/steam_sentry')
        self.app_id = getattr(settings, 'STEAM_APP_ID', 324510)  # Boundless app ID

        # Ensure sentry directory exists for credential storage
        os.makedirs(self.sentry_dir, exist_ok=True)

    def authenticate_with_2fa(self, username: str, password: str) -> Optional[str]:
        """Authenticate with Steam and return session ticket."""
        logger.info(f"Authenticating with Steam as {username}...")

        try:
            # Initialize Steam client
            self.client = SteamClient()

            # Set credential location for persistent auth
            self.client.set_credential_location(self.sentry_dir)

            # Attempt login with 2FA support
            result = self._login_with_2fa_support(username, password)

            if result == EResult.OK and self.client.logged_on:
                logger.info("Steam authentication successful!")

                # Get session ticket for Boundless
                ticket = self._get_session_ticket()

                if ticket:
                    logger.info(f"Got session ticket: {len(ticket)} bytes")
                    return ticket.hex()
                else:
                    logger.error("Failed to get session ticket")
                    return None
            else:
                logger.error(f"Steam authentication failed: {result}")
                return None

        except Exception as e:
            logger.error(f"Steam authentication error: {e}")
            return None
        finally:
            if self.client and self.client.logged_on:
                self.client.logout()
                logger.info("Logged out from Steam")

    def _login_with_2fa_support(self, username: str, password: str) -> EResult:
        """Handle login with interactive 2FA support."""

        # Try relogin first if available
        try:
            if self.client.relogin_available:
                logger.info("Attempting relogin with stored credentials...")
                result = self.client.relogin()
                if result == EResult.OK:
                    logger.info("Relogin successful!")
                    return result
                else:
                    logger.info(f"Relogin failed ({result}), trying fresh login...")
        except Exception as e:
            logger.info(f"Relogin attempt failed: {e}")

        # Fresh login
        logger.info("Attempting fresh login...")
        result = self.client.login(username, password)

        if result == EResult.OK:
            logger.info("Login successful!")
            return result
        elif result == EResult.AccountLoginDeniedNeedTwoFactor:
            logger.info("Steam Guard 2FA required - switching to interactive login")
            return self.client.cli_login(username, password)
        elif result == EResult.AccountLogonDenied:
            logger.info("Steam Guard email code required - switching to interactive login")
            return self.client.cli_login(username, password)
        elif result == EResult.TwoFactorCodeMismatch:
            logger.warning("2FA code mismatch - retrying with interactive login")
            return self.client.cli_login(username, password)
        elif result == EResult.RateLimitExceeded:
            logger.warning("Rate limit exceeded - waiting and retrying...")
            time.sleep(30)
            return self.client.cli_login(username, password)
        elif result == EResult.InvalidPassword:
            logger.error(f"Invalid password for user {username}")
            logger.info("Trying cli_login as fallback...")
            return self.client.cli_login(username, password)
        else:
            logger.error(f"Login failed with result: {result}")
            return result

    def _get_session_ticket(self) -> Optional[bytes]:
        """Get auth session ticket for Boundless app."""
        try:
            # Use get_app_ticket() method which returns a protobuf response
            # The actual ticket data is in the 'ticket' field of the response
            response = self.client.get_app_ticket(self.app_id)

            if response and hasattr(response, 'ticket'):
                ticket_data = response.ticket
                logger.info(f"Got app ticket: {len(ticket_data)} bytes")
                return ticket_data
            else:
                logger.error("Failed to get app ticket or ticket data missing")
                return None
        except Exception as e:
            logger.error(f"Error getting session ticket: {e}")
            return None


def get_steam_session_ticket_pure_python(username: str, password: str) -> Optional[str]:
    """
    Main function to get Steam session ticket.

    This is the primary integration point for BoundlessClient.

    Args:
        username: Steam username
        password: Steam password

    Returns:
        Hex-encoded session ticket string or None if failed
    """
    auth = PurePythonSteamAuth()
    return auth.authenticate_with_2fa(username, password)


def main():
    """Command-line interface for testing Steam authentication."""
    import sys

    if len(sys.argv) != 3:
        print("Usage: python steam_auth_pure_python.py <username> <password>")
        sys.exit(1)

    username, password = sys.argv[1], sys.argv[2]

    ticket = get_steam_session_ticket_pure_python(username, password)

    if ticket:
        print(ticket)
        sys.exit(0)
    else:
        print("Authentication failed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
