import os
import time
from shutil import copy2

import djclick as click
from django.conf import settings
from steam.client import SteamClient


@click.command()
def command():
    client = SteamClient()
    client.set_credential_location(settings.STEAM_SENTRY_DIR)

    for index, username in enumerate(settings.STEAM_USERNAMES):
        click.echo(f"Logging into Steam as {username}...")
        client.cli_login(username=username, password=settings.STEAM_PASSWORDS[index])

        time.sleep(5)

        # Check what files were actually created
        steam_dir = settings.STEAM_SENTRY_DIR
        created_files = []
        if os.path.exists(steam_dir):
            for file in os.listdir(steam_dir):
                if file != ".gitkeep" and username.lower() in file.lower():
                    created_files.append(file)

        if created_files:
            click.echo(f"Found Steam auth files: {created_files}")

            # Try to find the sentry file with various naming patterns
            sentry_file = None
            for file in created_files:
                if "sentry" in file.lower():
                    sentry_file = file
                    break

            if sentry_file:
                # copy to correct location for `auth-ticket.js`
                src = os.path.join(steam_dir, sentry_file)
                dest = os.path.join(steam_dir, f"sentry.{username}.bin")
                try:
                    copy2(src, dest)
                    click.echo(f"Copied {sentry_file} to sentry.{username}.bin")
                except Exception as e:
                    click.echo(f"Warning: Could not copy sentry file: {e}")
            else:
                click.echo(
                    "Warning: No sentry file found, but authentication succeeded"
                )
        else:
            click.echo(
                "Warning: No auth files created, but authentication may have succeeded"
            )

        click.echo("Login successful. Steam Guard should not prompt anymore")
        client.logout()
