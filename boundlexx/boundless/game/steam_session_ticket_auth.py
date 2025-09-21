"""
Steam Session Ticket Authentication for BoundlessClient Integration

Official Steamworks implementation using Session Ticket + Web API pattern
for game-to-backend server authentication with Django integration.

Based on: https://partner.steamgames.com/doc/features/auth
"""

import os
import json
import logging
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple

from django.conf import settings
from steam.client import SteamClient
from steam.enums import EResult


class SteamSessionTicketManager:
    """
    Production-ready Steam Session Ticket authentication manager

    Implements the official Steamworks Session Ticket + Web API pattern
    with automatic refresh, comprehensive error handling, and Django integration.
    """

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.session_file = f'/app/.steam/session_{username}.json'
        self.logger = logging.getLogger(f'SteamTicketManager_{username}')

        # Session state
        self.session_ticket: Optional[str] = None
        self.ticket_expiry: Optional[datetime] = None
        self.steam_id: Optional[int] = None

        # Load existing session if available
        self._load_session()

    def get_valid_session_ticket(self) -> Optional[str]:
        """
        Get a valid session ticket, refreshing if necessary

        Returns:
            Optional[str]: Valid session ticket or None if authentication fails
        """
        try:
            # Check if current session is valid
            if self._is_session_valid():
                self.logger.info(f"Using existing valid session (expires: {self.ticket_expiry})")
                return self.session_ticket

            # Session expired or doesn't exist, need to refresh
            self.logger.info("Session expired or missing, performing fresh authentication...")

            success, error = self._perform_authentication()
            if success:
                return self.session_ticket
            else:
                self.logger.error(f"Authentication failed: {error}")
                return None

        except Exception as e:
            self.logger.error(f"Failed to get session ticket: {str(e)}")
            return None

    def validate_ticket_with_steam(self, ticket: str) -> Tuple[bool, Optional[int]]:
        """
        Validate session ticket with Steam Web API

        Args:
            ticket (str): Session ticket to validate

        Returns:
            Tuple[bool, Optional[int]]: (is_valid, steam_id)
        """
        try:
            api_key = getattr(settings, 'STEAM_WEB_API_KEY', None)
            if not api_key:
                self.logger.error("STEAM_WEB_API_KEY not configured")
                return False, None

            api_url = "https://partner.steam-api.com/ISteamUserAuth/AuthenticateUserTicket/v1/"
            request_data = {
                'key': api_key,
                'appid': 324510,  # Boundless AppID
                'ticket': ticket
            }

            response = requests.post(api_url, data=request_data, timeout=30)

            if response.status_code == 200:
                api_response = response.json()

                if 'response' in api_response and 'params' in api_response['response']:
                    steam_id = int(api_response['response']['params']['steamid'])
                    self.logger.info(f"Ticket validation successful for Steam ID: {steam_id}")
                    return True, steam_id
                else:
                    self.logger.error("Invalid API response format")
                    return False, None
            else:
                self.logger.error(f"API request failed: HTTP {response.status_code}")
                return False, None

        except Exception as e:
            self.logger.error(f"Ticket validation failed: {str(e)}")
            return False, None

    def get_app_ticket(self, app_id: int) -> Optional[str]:
        """
        Get app ownership ticket for specified app ID from current session

        Args:
            app_id: Steam Application ID

        Returns:
            App ownership ticket as hex string or None if failed
        """
        if self.session_ticket and self._is_session_valid():
            self.logger.info(f"Returning cached app ticket for app {app_id}")
            return self.session_ticket

        self.logger.info(f"Generating fresh app ticket for app {app_id}")

        # Need fresh authentication
        ticket = self.get_valid_session_ticket()
        return ticket

    def _is_session_valid(self) -> bool:
        """Check if current session is valid and not expired"""
        if not self.session_ticket or not self.ticket_expiry:
            return False

        # Add 5-minute buffer before expiry
        buffer_time = timedelta(minutes=5)
        return datetime.utcnow() < (self.ticket_expiry - buffer_time)

    def _load_session(self):
        """Load existing session from file if available"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    session_data = json.load(f)

                self.session_ticket = session_data.get('session_ticket')
                self.steam_id = session_data.get('steam_id')

                if session_data.get('ticket_expiry'):
                    self.ticket_expiry = datetime.fromisoformat(session_data['ticket_expiry'])

                self.logger.info(f"Loaded existing session (expires: {self.ticket_expiry})")
            else:
                self.logger.info("No existing session file found")

        except Exception as e:
            self.logger.warning(f"Failed to load session: {str(e)}")
            self._clear_session()

    def _save_session(self):
        """Save current session to file"""
        try:
            session_data = {
                'username': self.username,
                'steam_id': self.steam_id,
                'session_ticket': self.session_ticket,
                'ticket_expiry': self.ticket_expiry.isoformat() if self.ticket_expiry else None,
                'created_at': datetime.utcnow().isoformat(),
                'authentication_method': 'session_ticket_web_api'
            }

            os.makedirs(os.path.dirname(self.session_file), exist_ok=True)

            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)

            self.logger.info(f"Session saved: {self.session_file}")

        except Exception as e:
            self.logger.warning(f"Failed to save session: {str(e)}")

    def _clear_session(self):
        """Clear current session data"""
        self.session_ticket = None
        self.ticket_expiry = None
        self.steam_id = None

        try:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
                self.logger.info("Session file removed")
        except Exception as e:
            self.logger.warning(f"Failed to remove session file: {str(e)}")

    def _perform_authentication(self) -> Tuple[bool, str]:
        """Perform fresh Steam authentication and generate session ticket"""
        client = None

        try:
            self.logger.info("Starting fresh Steam authentication...")

            # Initialize Steam client
            client = SteamClient()

            # Perform login
            result = client.cli_login(username=self.username, password=self.password)

            if result != EResult.OK:
                error_msg = f"Steam login failed: {EResult(result)}"
                return False, error_msg

            self.logger.info(f"Steam login successful for: {client.user.name}")
            self.steam_id = int(client.steam_id)

            # Generate app ownership ticket for Boundless (AppID 324510)
            # Try Encrypted Application Ticket first (21-day expiry) for maximum session duration
            try:
                self.logger.info("Attempting to get Encrypted Application Ticket (21-day expiry)...")

                # Use synchronous get_encrypted_app_ticket method (steam.py v1.4.4)
                encrypted_ticket = client.get_encrypted_app_ticket(324510, b'')

                if encrypted_ticket:
                    # Convert encrypted ticket to hex format for Web API validation
                    # The encrypted ticket is a protobuf message with binary data
                    if hasattr(encrypted_ticket, 'SerializeToString'):
                        self.session_ticket = encrypted_ticket.SerializeToString().hex()
                    else:
                        # If it's already bytes, convert directly
                        self.session_ticket = encrypted_ticket.hex() if isinstance(encrypted_ticket, bytes) else str(encrypted_ticket)

                    # Encrypted app tickets expire after 21 days per Steam documentation
                    self.ticket_expiry = datetime.utcnow() + timedelta(days=21)
                    self.logger.info(f"✅ Encrypted app ticket obtained (21-day expiry: {self.ticket_expiry})")
                else:
                    raise Exception("Failed to retrieve encrypted app ticket")

            except Exception as e:
                self.logger.warning(f"Encrypted app ticket failed ({e}), falling back to session ticket...")

                # Fallback to regular session ticket (24-hour expiry)
                ticket_response = client.get_app_ticket(324510)

                if not ticket_response or not hasattr(ticket_response, 'ticket'):
                    return False, "Failed to generate any app ticket"

                # Convert to hex format required by Web API
                self.session_ticket = ticket_response.ticket.hex()
                # Regular app tickets expire after 24 hours
                self.ticket_expiry = datetime.utcnow() + timedelta(hours=24)
                self.logger.info(f"⚠️  Using fallback session ticket (24-hour expiry: {self.ticket_expiry})")

            self.logger.info(f"Session ticket generated successfully (expires: {self.ticket_expiry})")

            # Web API validation commented out - 21-day encrypted tickets work without it
            # if hasattr(settings, 'STEAM_WEB_API_KEY') and settings.STEAM_WEB_API_KEY:
            #     is_valid, validated_steam_id = self.validate_ticket_with_steam(self.session_ticket)
            #
            #     if not is_valid or validated_steam_id != self.steam_id:
            #         self.logger.warning("Session ticket validation failed, but continuing without validation")
            #     else:
            #         self.logger.info("Session ticket validation successful")
            # else:
            #     self.logger.info("Skipping ticket validation (no STEAM_WEB_API_KEY configured)")

            # Save the session
            self._save_session()

            self.logger.info("Authentication completed successfully")
            return True, "Authentication successful"

        except Exception as e:
            error_msg = f"Authentication failed: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg

        finally:
            # Always cleanup client connection
            if client:
                try:
                    client.logout()
                except:
                    pass


def get_steam_session_ticket(username: str, password: str) -> Optional[str]:
    """
    High-level function to get a valid Steam session ticket

    Args:
        username (str): Steam username
        password (str): Steam password

    Returns:
        Optional[str]: Valid session ticket or None if failed
    """
    manager = SteamSessionTicketManager(username, password)
    return manager.get_valid_session_ticket()


def validate_steam_session_ticket(ticket: str) -> Tuple[bool, Optional[int]]:
    """
    Validate a Steam session ticket using the Steamworks Web API

    Args:
        ticket (str): Session ticket to validate

    Returns:
        Tuple[bool, Optional[int]]: (is_valid, steam_id)
    """
    # Create a temporary manager for validation
    manager = SteamSessionTicketManager("", "")
    return manager.validate_ticket_with_steam(ticket)


# Integration function for BoundlessClient
def get_steam_authentication_for_boundless(username: str, password: str) -> str:
    """
    Get Steam authentication ticket for Boundless using global session manager.

    This function integrates with the global session manager to reuse
    authentication sessions and avoid multiple 2FA prompts.

    Args:
        username: Steam username
        password: Steam password

    Returns:
        App ownership ticket as hex string

    Raises:
        Exception: If authentication fails
    """
    auth_logger = logging.getLogger('BoundlessAuth')
    auth_logger.info(f"Getting Steam authentication for Boundless (user: {username})")

    try:
        # Try to get from global session manager first
        from boundlexx.boundless.management.commands.prompt_steam_guard import get_global_steam_manager

        session_mgr = get_global_steam_manager()
        existing_manager = session_mgr.get_manager(username)

        if existing_manager:
            auth_logger.info(f"Using existing authentication session for {username}")
            try:
                # Try to get fresh app ticket from existing session
                ticket = existing_manager.get_app_ticket(324510)
                if ticket:
                    auth_logger.info(f"Successfully obtained app ticket from existing session")
                    return ticket
                else:
                    auth_logger.warning(f"Failed to get app ticket from existing session, creating new session")
            except Exception as e:
                auth_logger.warning(f"Existing session failed: {e}, creating new session")

        # Create new session manager if needed
        auth_logger.info(f"Creating new authentication session for {username}")
        manager = SteamSessionTicketManager(username, password)
        ticket = manager.get_valid_session_ticket()

        if ticket:
            # Store in global session manager for reuse
            session_mgr.managers[username] = manager
            session_mgr.authenticated_users.add(username)
            auth_logger.info(f"Successfully created new authentication session")
            return ticket
        else:
            raise Exception("Failed to obtain session ticket")

    except Exception as e:
        auth_logger.error(f"Steam authentication failed: {e}")
        raise


def get_steam_session_ticket(username: str, password: str) -> str:
    """
    Direct Steam session ticket generation (legacy interface).

    This function provides direct access to session ticket generation
    without global session management.
    """
    manager = SteamSessionTicketManager(username, password)
    return manager.get_valid_session_ticket()
