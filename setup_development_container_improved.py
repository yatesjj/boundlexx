#!/usr/bin/env python3
"""
Enhanced development container setup with folder-based naming.
Creates docker-compose.override.yml with proper container names and
original upstream ports.
"""

import argparse
import os
import sys
from pathlib import Path
import shutil


def get_folder_prefix():
    """Get container prefix from parent folder name."""
    current_dir = Path.cwd()
    parent_folder = current_dir.parent.name

    # Use parent folder name as prefix (e.g., boundlexx-yatesjj)
    if parent_folder and parent_folder != '/':
        return parent_folder
    else:
        # Fallback to current folder name
        return current_dir.name


def create_development_environment(prefix, force=False, dry_run=False):
    """Create development environment with unique container names and original ports."""

    print(f"🛠️ Setting up development environment with prefix: {prefix}")
    print(f"📁 Working directory: {Path.cwd()}")
    print("🔢 Using original upstream ports (28000, 5432, 6379, 8025)")

    # Create docker-compose.override.yml for development environment
    override_content = f"""# Auto-generated development environment override
# Prefix: {prefix}
# Uses original upstream ports

services:
  django: &django
    container_name: {prefix}-django-1
    env_file:
      - ./.env
      - ./.local.env
    ports:
      - "28000:8000"
    volumes:
      - .:/app
    networks:
      - {prefix}-network

  manage:
    <<: *django
    container_name: {prefix}-manage-1
    ports: []
    networks:
      - {prefix}-network

  test:
    <<: *django
    container_name: {prefix}-test-1
    ports: []
    networks:
      - {prefix}-network

  lint:
    <<: *django
    container_name: {prefix}-lint-1
    ports: []
    networks:
      - {prefix}-network

  format:
    <<: *django
    container_name: {prefix}-format-1
    ports: []
    networks:
      - {prefix}-network

  celery:
    <<: *django
    container_name: {prefix}-celery-1
    ports: []
    networks:
      - {prefix}-network

  celerybeat:
    <<: *django
    container_name: {prefix}-celerybeat-1
    ports: []
    networks:
      - {prefix}-network

  huey-consumer:
    <<: *django
    container_name: {prefix}-huey-consumer-1
    ports: []
    networks:
      - {prefix}-network

  huey-scheduler:
    <<: *django
    container_name: {prefix}-huey-scheduler-1
    ports: []
    networks:
      - {prefix}-network

  postgres:
    container_name: {prefix}-postgres-1
    env_file:
      - ./.env
      - ./.local.env
    networks:
      - {prefix}-network

  redis:
    container_name: {prefix}-redis-1
    networks:
      - {prefix}-network

networks:
  {prefix}-network:
    name: {prefix}-network
    driver: bridge
"""

    # Show what would be created
    print("\n📋 Development environment configuration:")
    print("   Django: http://localhost:28000")
    print("   PostgreSQL: internal only (port 5432)")
    print("   Redis: internal only (port 6379)")
    print("   MailHog: internal only (port 8025)")
    print(f"   Network: {prefix}-network")

    if dry_run:
        print("\n🔍 DRY RUN - Would create docker-compose.override.yml:")
        print("=" * 60)
        print(override_content)
        print("=" * 60)
        return True

    # Write the override file
    try:
        with open('docker-compose.override.yml', 'w') as f:
            f.write(override_content)
        print(f"✅ Created docker-compose.override.yml with {prefix} prefix")
    except Exception as e:
        print(f"❌ Error creating override file: {e}")
        return False

    # Auto-copy .env and .local.env if not present
    for env_file in ['.env', '.local.env']:
        if not Path(env_file).exists():
            try:
                shutil.copyfile(f"{env_file}.example", env_file)
                print(f"📄 Copied {env_file}.example to {env_file}")
            except Exception as e:
                print(f"❌ Error copying {env_file}: {e}")
                return False

    return True


def main():
    parser = argparse.ArgumentParser(
        description='Setup development environment with unique container names'
    )
    parser.add_argument(
        '--prefix',
        help='Container name prefix (auto-detected from folder if not specified)'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Show what would be created without making changes'
    )
    parser.add_argument(
        '--force', action='store_true',
        help='Force overwrite of existing docker-compose.override.yml'
    )

    args = parser.parse_args()

    # Get prefix from folder name if not specified
    if args.prefix:
        prefix = args.prefix
        print(f"📝 Using specified prefix: {prefix}")
    else:
        prefix = get_folder_prefix()
        print(f"📁 Auto-detected prefix from folder: {prefix}")

    # Validate we're in a boundlexx project
    if not os.path.exists('docker-compose.yml'):
        print("❌ Error: docker-compose.yml not found. "
              "Are you in the boundlexx project root?")
        sys.exit(1)

    # Check if override file exists and handle --force flag
    override_exists = os.path.exists('docker-compose.override.yml')
    if override_exists and not args.force:
        print("❌ Error: docker-compose.override.yml already exists. "
              "Use --force to overwrite.")
        sys.exit(1)

    success = create_development_environment(prefix, args.force, args.dry_run)

    if success:
        if not args.dry_run:
            print(f"\n🎉 Development environment '{prefix}' is ready!")
            print("   Django: http://localhost:28000")
            print("   Admin: http://localhost:28000/admin/")
            print("   Edit docker-compose.override.yml to customize paths")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
