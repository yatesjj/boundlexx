#!/usr/bin/env python3
"""
Enhanced development container setup with folder-based naming.
Creates docker-compose.override.yml with proper container names and
original upstream ports.
"""

import argparse
import re
import shutil
from pathlib import Path


def get_folder_prefix():
    """Get container prefix from current folder name."""
    current_dir = Path.cwd()
    # Use current folder name as prefix (e.g., boundlexx-yatesjj)
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
        with open("docker-compose.override.yml", "w") as f:
            f.write(override_content)
        print(f"✅ Created docker-compose.override.yml with {prefix} prefix")
    except Exception as e:
        print(f"❌ Error creating override file: {e}")
        return False

    # Auto-copy .env and .local.env if not present
    for env_file in [".env", ".local.env"]:
        if not Path(env_file).exists():
            try:
                shutil.copyfile(f"{env_file}.example", env_file)
                print(f"📄 Copied {env_file}.example to {env_file}")
            except Exception as e:
                print(f"❌ Error copying {env_file}: {e}")
                return False

    return True


def setup_development_containers(dry_run=False, prefix=None, force=False):
    """Set up development container with folder name prefixes."""
    repo_dir = Path(__file__).resolve().parent

    if prefix:
        folder_name = prefix
    else:
        folder_name = repo_dir.name

    print(f"🛠️ Setting up development environment with prefix: {folder_name}")
    print(f"📁 Working directory: {repo_dir}")
    print(f"🔄 Dry run: {dry_run}")
    print(f"💥 Force overwrite: {force}")

    compose_files = [
        repo_dir / "docker-compose.yml",
        repo_dir / "docker-compose.override.yml",
    ]
    env_file = repo_dir / ".env"
    local_env_file = repo_dir / ".local.env"

    # Auto-copy .env to .local.env if missing
    if not local_env_file.exists() and env_file.exists():
        if dry_run:
            print(f"📋 Would copy {env_file} to {local_env_file}")
        else:
            try:
                shutil.copy(env_file, local_env_file)
                print(f"✅ Copied {env_file} to {local_env_file}")
            except Exception as e:
                print(f"❌ Error copying env file: {e}")
                return

    name_pattern = re.compile(r"(container_name|service|network|name):\s*([\w-]+)")

    def prefix_name(match):
        key, value = match.groups()
        if value.startswith(folder_name):
            return match.group(0)
        return f"{key}: {folder_name}-{value}"

    def update_yaml_file(path):
        if not path.exists():
            print(f"⚠️ Warning: {path} does not exist, skipping...")
            return

        text = path.read_text(encoding="utf-8")
        original_text = text

        text = name_pattern.sub(prefix_name, text)

        if text == original_text:
            print(f"✅ No changes needed for {path}")
            return

        if dry_run:
            print(f"📋 Would update {path}:")
            print("=" * 60)
            print(text)
            print("=" * 60)
        else:
            if path.exists() and not force:
                print(f"⚠️ {path} exists - use --force to overwrite")
                return
            path.write_text(text, encoding="utf-8")
            print(f"✅ Updated {path}")

    def update_env_file(path):
        if not path.exists():
            print(f"⚠️ Warning: {path} does not exist, skipping...")
            return

        lines = path.read_text(encoding="utf-8").splitlines()
        new_lines = []
        changes_made = False

        for line in lines:
            m2 = re.match(r"([A-Z_]+)=(.+)", line)
            if m2 and not m2.group(2).startswith(folder_name):
                key, value = m2.groups()
                if "NAME" in key or "SERVICE" in key or "NETWORK" in key:
                    new_lines.append(f"{key}={folder_name}-{value}")
                    changes_made = True
                    continue
            new_lines.append(line)

        if not changes_made:
            print(f"✅ No changes needed for {path}")
            return

        text = "\n".join(new_lines) + "\n"

        if dry_run:
            print(f"📋 Would update {path}:")
            print("=" * 60)
            print(text)
            print("=" * 60)
        else:
            if path.exists() and not force:
                print(f"⚠️ {path} exists - use --force to overwrite")
                return
            path.write_text(text, encoding="utf-8")
            print(f"✅ Updated {path}")

    for f in compose_files:
        update_yaml_file(f)
    update_env_file(env_file)

    if not dry_run:
        print(f"🎉 Development environment '{folder_name}' is ready!")
    else:
        print(f"🔍 Dry run complete for '{folder_name}'.")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Set up development container with folder-prefixed names "
            "and original ports"
        )
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making any modifications",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files without prompting",
    )
    parser.add_argument(
        "--prefix",
        type=str,
        help=(
            "Custom prefix for container names (default: auto-detect "
            "from git or folder)"
        ),
    )

    args = parser.parse_args()
    setup_development_containers(
        dry_run=args.dry_run, prefix=args.prefix, force=args.force
    )


if __name__ == "__main__":
    main()
