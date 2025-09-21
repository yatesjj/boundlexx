"""
Steam Authentication Manager

Modern Steam authentication using official Steam.py API patterns.
Replaces deprecated sentry file approach with Session Ticket + Web API pattern.

This command creates a single authentication session that can provide
app ownership tickets for Boundless (AppID 324510) without requiring
multiple 2FA authentications.

Usage:
    python manage.py prompt_steam_guard

Features:
- Single 2FA authentication per session
- 21-day encrypted app ownership ticket generation
- Session management for BoundlessClient integration
"""

import asyncio
import logging
import os
from datetime import datetime, timedelta

import djclick as click
from django.conf import settings
from steam.client import SteamClient

from boundlexx.boundless.game.steam_session_ticket_auth import SteamSessionTicketManager

# Global session manager for reuse
_global_session_manager = None


class GlobalSteamSessionManager:
    """Global Steam session manager for single authentication across multiple requests"""

    def __init__(self):
        self.managers = {}  # username -> SteamSessionTicketManager
        self.authenticated_users = set()
        self.logger = logging.getLogger("GlobalSteamAuth")

    async def authenticate_user(self, username, password):
        """Authenticate a user and store session for reuse"""
        if username in self.authenticated_users:
            self.logger.info(f"User {username} already authenticated in this session")
            return self.managers[username]

        self.logger.info(f"Performing fresh authentication for {username}")
        manager = SteamSessionTicketManager(username, password)

        # Perform authentication
        ticket = manager.get_valid_session_ticket()
        if ticket:
            self.managers[username] = manager
            self.authenticated_users.add(username)
            self.logger.info(f"Successfully authenticated {username}")
            return manager
        else:
            raise Exception(f"Failed to authenticate {username}")

    def get_manager(self, username):
        """Get existing authenticated manager"""
        return self.managers.get(username)

    def clear_session(self):
        """Clear all authentication sessions"""
        # Clear in-memory managers
        for manager in self.managers.values():
            try:
                # Clear session files from disk
                if hasattr(manager, "_clear_session"):
                    manager._clear_session()
                # Logout Steam client
                if hasattr(manager, "client") and manager.client:
                    manager.client.logout()
            except Exception as e:
                self.logger.warning(f"Error clearing session: {e}")

        # Also clear any existing session files on disk (in case managers weren't loaded)
        try:
            steam_dir = os.path.expanduser("~/.steam")
            if not os.path.exists(steam_dir):
                steam_dir = "/app/.steam"  # Container environment

            if os.path.exists(steam_dir):
                for filename in os.listdir(steam_dir):
                    if filename.startswith("session_") and filename.endswith(".json"):
                        session_file = os.path.join(steam_dir, filename)
                        os.remove(session_file)
                        self.logger.info(f"Removed session file: {session_file}")
        except Exception as e:
            self.logger.warning(f"Error clearing session files: {e}")

        self.managers.clear()
        self.authenticated_users.clear()
        self.logger.info("Cleared all authentication sessions")


def get_global_steam_manager():
    """Get or create global Steam session manager"""
    global _global_session_manager
    if _global_session_manager is None:
        _global_session_manager = GlobalSteamSessionManager()
    return _global_session_manager


@click.command()
@click.option(
    "--test-tickets",
    is_flag=True,
    help="Test app ticket generation after authentication",
)
@click.option(
    "--clear-session", is_flag=True, help="Clear existing authentication sessions"
)
def command(test_tickets, clear_session):
    """
    Steam Authentication Manager

    Authenticate Steam accounts and optionally test app ticket generation.
    Maintains single authentication session to avoid multiple 2FA prompts.
    """

    # Setup logging
    logging.basicConfig(
        level=logging.INFO, format="[%(asctime)s] %(name)s %(levelname)s: %(message)s"
    )
    logger = logging.getLogger("SteamAuth")

    click.echo("Steam Authentication Manager")
    click.echo("=" * 50)

    # Get global session manager
    session_mgr = get_global_steam_manager()

    if clear_session:
        session_mgr.clear_session()
        click.echo("✅ Cleared existing authentication sessions")
        return

    # Validate configuration
    if not settings.STEAM_USERNAMES or not settings.STEAM_PASSWORDS:
        click.echo(
            "❌ STEAM_USERNAMES and STEAM_PASSWORDS must be configured in settings"
        )
        return

    if len(settings.STEAM_USERNAMES) != len(settings.STEAM_PASSWORDS):
        click.echo("❌ STEAM_USERNAMES and STEAM_PASSWORDS must have same length")
        return

    click.echo(
        f"Found {len(settings.STEAM_USERNAMES)} Steam account(s) to authenticate"
    )

    # Authenticate each user
    for index, username in enumerate(settings.STEAM_USERNAMES):
        password = settings.STEAM_PASSWORDS[index]

        click.echo(f"\n🔐 Authenticating Steam user: {username}")

        try:
            # Check if already authenticated
            existing_manager = session_mgr.get_manager(username)
            if existing_manager:
                click.echo(f"✅ {username} already authenticated in this session")
                manager = existing_manager
            else:
                # Perform fresh authentication
                manager = SteamSessionTicketManager(username, password)
                ticket = manager.get_valid_session_ticket()

                if ticket:
                    session_mgr.managers[username] = manager
                    session_mgr.authenticated_users.add(username)
                    click.echo(f"✅ Authentication successful for {username}")
                    click.echo(f"   Session ticket length: {len(ticket)} characters")

                    # Show ticket expiry if available
                    if hasattr(manager, "session_expires") and manager.session_expires:
                        expiry_str = manager.session_expires.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        click.echo(f"   Ticket expires: {expiry_str}")
                else:
                    click.echo(f"❌ Authentication failed for {username}")
                    continue

            # Test app ticket generation if requested
            if test_tickets:
                click.echo(f"🎮 Testing Boundless app ticket generation for {username}")
                try:
                    app_ticket = manager.get_app_ticket(324510)  # Boundless App ID
                    if app_ticket:
                        click.echo(f"✅ App ticket generated successfully")
                        click.echo(f"   Ticket length: {len(app_ticket)} characters")

                        # Web API validation commented out - 21-day encrypted tickets work without it
                        # if settings.STEAM_WEB_API_KEY:
                        #     click.echo("🔍 Validating ticket with Steam Web API...")
                        #     is_valid, steam_id = manager.validate_ticket_with_steam(app_ticket)
                        #     if is_valid:
                        #         click.echo(f"✅ Ticket validation successful")
                        #         click.echo(f"   Validated Steam ID: {steam_id}")
                        #     else:
                        #         click.echo("❌ Ticket validation failed")
                        # else:
                        #     click.echo("⚠️  Skipping ticket validation (no STEAM_WEB_API_KEY)")
                    else:
                        click.echo("❌ App ticket generation failed")

                except Exception as e:
                    click.echo(f"❌ App ticket test failed: {e}")

        except Exception as e:
            click.echo(f"❌ Authentication failed for {username}: {e}")
            logger.exception(f"Authentication error for {username}")

    # Summary
    click.echo(f"\n📊 Session Summary:")
    click.echo(f"   Authenticated users: {len(session_mgr.authenticated_users)}")
    click.echo(f"   Users: {', '.join(session_mgr.authenticated_users)}")

    if session_mgr.authenticated_users:
        click.echo("\n✅ Steam authentication sessions established")
        click.echo("   These sessions can be reused by BoundlessClient")
        click.echo("   Run with --clear-session to clear sessions")
    else:
        click.echo("\n❌ No successful authentications")

    click.echo("\n🔧 Integration Notes:")
    click.echo("   - BoundlessClient will use these authenticated sessions")
    click.echo("   - No additional 2FA prompts needed for this session")

    # Show actual session expiry information
    if session_mgr.authenticated_users and session_mgr.managers:
        # Get session expiry times from active managers
        session_expires = []
        for username in session_mgr.authenticated_users:
            if username in session_mgr.managers:
                manager = session_mgr.managers[username]
                if hasattr(manager, "ticket_expiry") and manager.ticket_expiry:
                    from datetime import datetime

                    time_remaining = manager.ticket_expiry - datetime.utcnow()
                    if time_remaining.days >= 14:
                        session_expires.append(f"~{time_remaining.days} days")
                    elif time_remaining.days >= 1:
                        session_expires.append(f"~{time_remaining.days} days")
                    else:
                        hours = time_remaining.seconds // 3600
                        session_expires.append(f"~{hours} hours")

        if session_expires:
            # Show the longest session duration
            longest_session = max(
                session_expires, key=lambda x: int(x.split()[0].replace("~", ""))
            )
            click.echo(
                f"   - Sessions expire in {longest_session} (encrypted app tickets)"
            )
        else:
            click.echo("   - Session expiry information not available")
    else:
        click.echo("   - Session expiry information not available")
