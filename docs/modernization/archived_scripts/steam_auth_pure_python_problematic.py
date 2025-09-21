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
        logger.info(f"Steam sentry directory: {self.sentry_dir}")

    def check_sentry_status(self, username: str) -> bool:
        """Check if sentry file exists for username."""
        if not self.client:
            return False

        sentry_data = self.client.get_sentry(username)
        has_sentry = sentry_data is not None
        logger.info(f"Sentry file status for {username}: {'Found' if has_sentry else 'Not found'}")

        # Also check filesystem directly
        sentry_file = os.path.join(self.sentry_dir, f"{username}.sentry")
        file_exists = os.path.exists(sentry_file)
        logger.info(f"Sentry file on disk: {'Found' if file_exists else 'Not found'} at {sentry_file}")

        return has_sentry

    def wait_for_sentry_creation(self, username: str, timeout: int = 10) -> bool:
        """Wait for sentry file to be created after successful authentication."""
        import time
        start_time = time.time()

        while time.time() - start_time < timeout:
            if self.check_sentry_status(username):
                logger.info(f"Sentry file created for {username} after {time.time() - start_time:.1f}s")
                return True
            time.sleep(0.5)

        logger.warning(f"Sentry file not created for {username} after {timeout}s timeout")
        return False

    def authenticate_with_2fa(self, username: str, password: str) -> Optional[str]:
        """Authenticate with Steam and return session ticket."""
        logger.info(f"Authenticating with Steam as {username}...")

        try:
            # Initialize Steam client
            self.client = SteamClient()

            # Set credential location for persistent auth (CRITICAL for sentry files)
            self.client.set_credential_location(self.sentry_dir)
            logger.info(f"Set credential location: {self.sentry_dir}")

            # Check existing sentry file status
            self.check_sentry_status(username)

            # Attempt login with 2FA support
            result = self._login_with_2fa_support(username, password)

            if result == EResult.OK and self.client.logged_on:
                logger.info("Steam authentication successful!")

                # Wait for sentry file creation (especially important after 2FA)
                logger.info("Waiting for sentry file creation...")
                self.wait_for_sentry_creation(username, timeout=10)

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
        # NOTE: No logout() call - preserve Steam session for sentry file persistence
        # This allows relogin() to work without 2FA on subsequent calls

    def _login_with_2fa_support(self, username: str, password: str) -> EResult:
        """Handle login with interactive 2FA support."""

        # PRIORITY 1: Try relogin first if sentry file available
        try:
            if self.client.relogin_available:
                logger.info("Sentry file found - attempting relogin without 2FA...")
                result = self.client.relogin()
                if result == EResult.OK:
                    logger.info("Relogin successful! No 2FA required.")
                    return result
                else:
                    logger.info(f"Relogin failed ({result}), falling back to fresh login...")
        except Exception as e:
            logger.info(f"Relogin attempt failed: {e}, trying fresh login...")

        # PRIORITY 2: Fresh login (may require 2FA)
        logger.info("Attempting fresh login (may require 2FA)...")
        result = self.client.login(username, password)

        if result == EResult.OK:
            logger.info("Fresh login successful!")
            return result
        elif result == EResult.AccountLoginDeniedNeedTwoFactor:
            logger.info("Steam Guard 2FA required - switching to interactive login")
            result = self.client.cli_login(username, password)
            if result == EResult.OK:
                logger.info("✅ 2FA authentication successful - sentry file should be created")
            return result
        elif result == EResult.AccountLogonDenied:
            logger.info("Steam Guard email code required - switching to interactive login")
            result = self.client.cli_login(username, password)
            if result == EResult.OK:
                logger.info("✅ Email authentication successful - sentry file should be created")
            return result
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
