#!/usr/bin/env python3
"""
Enhanced test container setup with folder-based naming and dry-run capability.
Automatically detects folder name and applies it as container prefix.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
import shutil


def get_folder_prefix():
    """Get container prefix from parent folder name."""
    current_dir = Path.cwd()
    parent_folder = current_dir.parent.name

    # Use parent folder name as prefix (e.g., boundlexx-yatesjj-test-env)
    if parent_folder and parent_folder != '/':
        return parent_folder
    else:
        # Fallback to current folder name
        return current_dir.name


def create_test_environment(prefix, port_offset=1, dry_run=False, force=False):
    """Create test environment with unique container names and ports."""

    print(f"🧪 Setting up test environment with prefix: {prefix}")
    print(f"📁 Working directory: {Path.cwd()}")
    print(f"🔢 Port offset: {port_offset}")

    # Define port mappings with offset (only Django needs external port)
    django_port = 28000 + port_offset     # 28001 for first test env

    # Create docker-compose.override.yml for test environment
    override_content = f"""# Auto-generated test environment override
# Prefix: {prefix}
# Port offset: {port_offset}

version: '3.8'

services:
  django:
    container_name: {prefix}-django-1
    ports:
      - "{django_port}:8000"
    networks:
      - {prefix}-network

  postgres:
    container_name: {prefix}-postgres-1
    networks:
      - {prefix}-network

  redis:
    container_name: {prefix}-redis-1
    networks:
      - {prefix}-network

  celery:
    container_name: {prefix}-celery-1
    networks:
      - {prefix}-network

  celerybeat:
    container_name: {prefix}-celerybeat-1
    networks:
      - {prefix}-network

  huey-consumer:
    container_name: {prefix}-huey-consumer-1
    networks:
      - {prefix}-network

  huey-scheduler:
    container_name: {prefix}-huey-scheduler-1
    networks:
      - {prefix}-network

networks:
  {prefix}-network:
    name: {prefix}-network
    driver: bridge
"""

    # Show what would be created
    print("\n📋 Test environment configuration:")
    print(f"   Django: http://localhost:{django_port}")
    print("   PostgreSQL: internal only (port 5432)")
    print("   Redis: internal only (port 6379)")
    print(f"   Network: {prefix}-network")

    if dry_run:
        print("\n🔍 DRY RUN - Would create docker-compose.override.yml:")
        print("=" * 60)
        print(override_content)
        print("=" * 60)
        print("\n🔍 DRY RUN - Would run: docker-compose up -d")
        return True

    # Write the override file
    try:
        with open('docker-compose.override.yml', 'w') as f:
            f.write(override_content)
        print(f"✅ Created docker-compose.override.yml with {prefix} prefix")
    except Exception as e:
        print(f"❌ Error creating override file: {e}")
        return False

    # Copy .env file if not exists
    try:
        if not os.path.exists('.env'):
            shutil.copyfile('.env.example', '.env')
            print("✅ Copied .env.example to .env")
        else:
            print("⚠️  .env file already exists, not overwriting")
    except Exception as e:
        print(f"❌ Error copying .env file: {e}")
        return False

    # Start the containers
    try:
        print("\n🚀 Starting test containers...")
        subprocess.run(['docker-compose', 'up', '-d'],
                       check=True, capture_output=True, text=True)
        print("✅ Test environment started successfully!")
        django_url = f"http://localhost:{django_port}"
        print(f"🌐 Access your test environment at: {django_url}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting containers: {e}")
        print(f"   stdout: {e.stdout}")
        print(f"   stderr: {e.stderr}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Setup test environment with unique container names and ports'
    )
    parser.add_argument(
        '--prefix',
        help='Container name prefix (auto-detected from folder if not specified)'
    )
    parser.add_argument(
        '--port-offset', type=int, default=1,
        help='Port offset for test environment (default: 1)'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Show what would be created without making changes'
    )
    parser.add_argument(
        '--force', action='store_true',
        help='Force overwrite of existing files (docker-compose.override.yml, .env)'
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

    # Check if files already exist and handle --force option
    override_exists = os.path.exists('docker-compose.override.yml')
    env_exists = os.path.exists('.env')

    if override_exists or env_exists:
        if args.force:
            print("⚠️  Overwriting existing files:")
            if override_exists:
                print("   - docker-compose.override.yml")
            if env_exists:
                print("   - .env")
        else:
            print("❌ Error: The following files already exist:")
            if override_exists:
                print("   - docker-compose.override.yml")
            if env_exists:
                print("   - .env")
            print("Run with --force to overwrite these files.")
            sys.exit(1)

    success = create_test_environment(
        prefix,
        args.port_offset,
        args.dry_run,
        args.force
    )

    if success:
        if not args.dry_run:
            print(f"\n🎉 Test environment '{prefix}' is ready!")
            print(f"   Django: http://localhost:{28000 + args.port_offset}")
            print(f"   Admin: http://localhost:{28000 + args.port_offset}/admin/")
            print("   PostgreSQL: internal only (port 5432)")
            print("   Redis: internal only (port 6379)")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
