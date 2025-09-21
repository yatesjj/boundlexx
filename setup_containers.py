#!/usr/bin/env python3
"""
Unified Boundlexx Container Setup Script

Creates Docker Compose override configurations for:
- Development environments (Django on port 28001)
- Test environments (test- prefix, Django on port 28002)
- Production environments (Django on port 28000)

All naming is handled by Docker Compose project naming (folder-based).

Usage:
    python setup_containers.py                    # Interactive mode
    python setup_containers.py --env dev          # Development setup
    python setup_containers.py --env test         # Test setup
    python setup_containers.py --env production   # Production setup
    python setup_containers.py --dry-run          # Preview without writing
"""

import argparse
import sys
from pathlib import Path


def get_environment_choice():
    """Interactive environment selection."""
    print("\n🐳 Boundlexx Container Setup")
    print("=" * 40)
    print("Choose your environment type:")
    print("  1. Development (Django on port 28001)")
    print("  2. Test (test- prefix, Django on port 28002)")
    print("  3. Production (Django on port 28000)")
    print()

    while True:
        choice = input("Enter choice (1, 2, or 3): ").strip()
        if choice == "1":
            return "dev"
        elif choice == "2":
            return "test"
        elif choice == "3":
            return "production"
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def create_development_override():
    """Create development environment configuration."""
    return """# Auto-generated development environment override
# Environment: Development
# Django port: 28001

services:
  boundlexx-django: &django
    container_name: boundlexx-django-dev
    env_file:
      - ./.env
      - ./.local.env
    ports:
      - "28001:8000"
    volumes:
      - .:/app
      ## Replace with path to your Boundless install
      - "/c/Program Files (x86)/Steam/steamapps/common/Boundless:/boundless"
      ## Replace with path to your out folder for `boundless_icon_render`
      - "/c/VSCode/boundless_headless_renderer/out:/boundless-icons"
    depends_on:
      - boundlexx-postgres
      - boundlexx-redis
    networks:
      - app-network
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: django
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-dev
      app.kubernetes.io/environment: development
      app.kubernetes.io/managed-by: docker-compose

  boundlexx-manage:
    <<: *django
    container_name: boundlexx-manage-dev
    ports: []
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: manage
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-dev
      app.kubernetes.io/environment: development
      app.kubernetes.io/managed-by: docker-compose

  boundlexx-test:
    <<: *django
    container_name: boundlexx-test-dev
    ports: []
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: test
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-dev
      app.kubernetes.io/environment: development
      app.kubernetes.io/managed-by: docker-compose

  boundlexx-lint:
    <<: *django
    container_name: boundlexx-lint-dev
    ports: []
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: lint
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-dev
      app.kubernetes.io/environment: development
      app.kubernetes.io/managed-by: docker-compose

  boundlexx-format:
    <<: *django
    container_name: boundlexx-format-dev
    ports: []
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: format
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-dev
      app.kubernetes.io/environment: development
      app.kubernetes.io/managed-by: docker-compose

  boundlexx-celery:
    <<: *django
    container_name: boundlexx-celery-dev
    ports: []
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: celery
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-dev
      app.kubernetes.io/environment: development
      app.kubernetes.io/managed-by: docker-compose

  boundlexx-celerybeat:
    <<: *django
    container_name: boundlexx-celerybeat-dev
    ports: []
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: celerybeat
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-dev
      app.kubernetes.io/environment: development
      app.kubernetes.io/managed-by: docker-compose

  boundlexx-huey-consumer:
    <<: *django
    container_name: boundlexx-huey-consumer-dev
    ports: []
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: huey-consumer
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-dev
      app.kubernetes.io/environment: development
      app.kubernetes.io/managed-by: docker-compose

  boundlexx-huey-scheduler:
    <<: *django
    container_name: boundlexx-huey-scheduler-dev
    ports: []
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: huey-scheduler
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-dev
      app.kubernetes.io/environment: development
      app.kubernetes.io/managed-by: docker-compose

  boundlexx-postgres:
    container_name: boundlexx-postgres-dev
    volumes:
      - postgres-data:/var/lib/postgresql/data
    env_file:
      - ./.env
      - ./.local.env
    networks:
      - app-network
    labels:
      app.kubernetes.io/name: boundlexx-postgres
      app.kubernetes.io/component: database
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-dev
      app.kubernetes.io/environment: development
      app.kubernetes.io/managed-by: docker-compose

  boundlexx-redis:
    container_name: boundlexx-redis-dev
    networks:
      - app-network
    labels:
      app.kubernetes.io/name: boundlexx-redis
      app.kubernetes.io/component: cache
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-dev
      app.kubernetes.io/environment: development
      app.kubernetes.io/managed-by: docker-compose

volumes:
  postgres-data:

networks:
  app-network:
    name: app-network
    driver: bridge
"""


def create_test_override():
    """Create test environment configuration."""
    return """# Auto-generated test environment override
# Environment: Test
# Django port: 28002

services:
  boundlexx-django:
    container_name: boundlexx-django-test
    env_file:
      - ./.env
      - ./.local.env
    ports:
      - "28002:8000"
    volumes:
      - .:/app
      ## Replace with path to your Boundless install
      - "/c/Program Files (x86)/Steam/steamapps/common/Boundless:/boundless"
      ## Replace with path to your out folder for `boundless_icon_render`
      - "/c/VSCode/boundless_headless_renderer/out:/boundless-icons"
    depends_on:
      - boundlexx-postgres
      - boundlexx-redis
    networks:
      - test-app-network
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: django
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-test
      app.kubernetes.io/environment: test
      app.kubernetes.io/managed-by: docker-compose

  boundlexx-manage:
    container_name: boundlexx-manage-test
    env_file:
      - ./.env
      - ./.local.env
    depends_on:
      - boundlexx-postgres
      - boundlexx-redis
    networks:
      - test-app-network
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: manage
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-test
      app.kubernetes.io/environment: test
      app.kubernetes.io/managed-by: docker-compose

  boundlexx-test:
    container_name: boundlexx-test-test
    env_file:
      - ./.env
      - ./.local.env
    depends_on:
      - boundlexx-postgres
      - boundlexx-redis
    networks:
      - test-app-network
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: test
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-test
      app.kubernetes.io/environment: test
      app.kubernetes.io/managed-by: docker-compose

  boundlexx-lint:
    container_name: boundlexx-lint-test
    env_file:
      - ./.env
      - ./.local.env
    depends_on: []
    networks:
      - test-app-network
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: lint
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-test
      app.kubernetes.io/environment: test
      app.kubernetes.io/managed-by: docker-compose

  boundlexx-format:
    container_name: boundlexx-format-test
    env_file:
      - ./.env
      - ./.local.env
    depends_on: []
    networks:
      - test-app-network
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: format
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-test
      app.kubernetes.io/environment: test
      app.kubernetes.io/managed-by: docker-compose

  boundlexx-celery:
    container_name: boundlexx-celery-test
    env_file:
      - ./.env
      - ./.local.env
    depends_on:
      - boundlexx-postgres
      - boundlexx-redis
    networks:
      - test-app-network
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: celery
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-test
      app.kubernetes.io/environment: test
      app.kubernetes.io/managed-by: docker-compose

  boundlexx-celerybeat:
    container_name: boundlexx-celerybeat-test
    env_file:
      - ./.env
      - ./.local.env
    depends_on:
      - boundlexx-postgres
      - boundlexx-redis
    networks:
      - test-app-network
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: celerybeat
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-test
      app.kubernetes.io/environment: test
      app.kubernetes.io/managed-by: docker-compose

  boundlexx-huey-consumer:
    container_name: boundlexx-huey-consumer-test
    env_file:
      - ./.env
      - ./.local.env
    depends_on:
      - boundlexx-postgres
      - boundlexx-redis
    networks:
      - test-app-network
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: huey-consumer
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-test
      app.kubernetes.io/environment: test
      app.kubernetes.io/managed-by: docker-compose

  boundlexx-huey-scheduler:
    container_name: boundlexx-huey-scheduler-test
    env_file:
      - ./.env
      - ./.local.env
    depends_on:
      - boundlexx-postgres
      - boundlexx-redis
    networks:
      - test-app-network
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: huey-scheduler
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-test
      app.kubernetes.io/environment: test
      app.kubernetes.io/managed-by: docker-compose

  boundlexx-postgres:
    container_name: boundlexx-postgres-test
    volumes:
      - test-postgres-data:/var/lib/postgresql/data
    env_file:
      - ./.env
      - ./.local.env
    networks:
      - test-app-network
    labels:
      app.kubernetes.io/name: boundlexx-postgres
      app.kubernetes.io/component: database
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-test
      app.kubernetes.io/environment: test
      app.kubernetes.io/managed-by: docker-compose

  boundlexx-redis:
    container_name: boundlexx-redis-test
    networks:
      - test-app-network
    labels:
      app.kubernetes.io/name: boundlexx-redis
      app.kubernetes.io/component: cache
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx-test
      app.kubernetes.io/environment: test
      app.kubernetes.io/managed-by: docker-compose

volumes:
  test-postgres-data:

networks:
  test-app-network:
    name: test-app-network
    driver: bridge
"""


def create_production_override():
    """Create production environment configuration."""
    return """# Auto-generated production environment override
# Environment: Production
# Django port: 28000

services:
  boundlexx-django: &django
    container_name: boundlexx-django
    env_file:
      - ./.env
      - ./.local.env
    ports:
      - "28000:8000"
    volumes:
      - .:/app
      ## Replace with path to your Boundless install
      - "/c/Program Files (x86)/Steam/steamapps/common/Boundless:/boundless"
      ## Replace with path to your out folder for `boundless_icon_render`
      - "/c/VSCode/boundless_headless_renderer/out:/boundless-icons"
    depends_on:
      - boundlexx-postgres
      - boundlexx-redis
    networks:
      - app-network
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: django
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx
      app.kubernetes.io/environment: production
      app.kubernetes.io/managed-by: kubernetes

  boundlexx-manage:
    <<: *django
    container_name: boundlexx-manage
    ports: []
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: manage
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx
      app.kubernetes.io/environment: production
      app.kubernetes.io/managed-by: kubernetes

  boundlexx-test:
    <<: *django
    container_name: boundlexx-test
    ports: []
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: test
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx
      app.kubernetes.io/environment: production
      app.kubernetes.io/managed-by: kubernetes

  boundlexx-lint:
    <<: *django
    container_name: boundlexx-lint
    ports: []
    depends_on: []
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: lint
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx
      app.kubernetes.io/environment: production
      app.kubernetes.io/managed-by: kubernetes

  boundlexx-format:
    <<: *django
    container_name: boundlexx-format
    ports: []
    depends_on: []
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: format
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx
      app.kubernetes.io/environment: production
      app.kubernetes.io/managed-by: kubernetes

  boundlexx-celery:
    <<: *django
    container_name: boundlexx-celery
    ports: []
    command: ["celery", "--app=config.celery_app", "worker", "--loglevel=info"]
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: celery
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx
      app.kubernetes.io/environment: production
      app.kubernetes.io/managed-by: kubernetes

  boundlexx-celerybeat:
    <<: *django
    container_name: boundlexx-celerybeat
    ports: []
    command: ["celery", "--app=config.celery_app", "beat", "--loglevel=info"]
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: celerybeat
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx
      app.kubernetes.io/environment: production
      app.kubernetes.io/managed-by: kubernetes

  boundlexx-huey-consumer:
    <<: *django
    container_name: boundlexx-huey-consumer
    ports: []
    command: ["python", "manage.py", "run_huey"]
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: huey-consumer
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx
      app.kubernetes.io/environment: production
      app.kubernetes.io/managed-by: kubernetes

  boundlexx-huey-scheduler:
    <<: *django
    container_name: boundlexx-huey-scheduler
    ports: []
    command: ["python", "manage.py", "run_huey", "--periodic"]
    labels:
      app.kubernetes.io/name: boundlexx-django
      app.kubernetes.io/component: huey-scheduler
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx
      app.kubernetes.io/environment: production
      app.kubernetes.io/managed-by: kubernetes

  boundlexx-postgres:
    container_name: boundlexx-postgres
    networks:
      - app-network
    labels:
      app.kubernetes.io/name: boundlexx-postgres
      app.kubernetes.io/component: database
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx
      app.kubernetes.io/environment: production
      app.kubernetes.io/managed-by: kubernetes

  boundlexx-redis:
    container_name: boundlexx-redis
    networks:
      - app-network
    labels:
      app.kubernetes.io/name: boundlexx-redis
      app.kubernetes.io/component: cache
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx
      app.kubernetes.io/environment: production
      app.kubernetes.io/managed-by: kubernetes

volumes:
  postgres-data:

networks:
  app-network:
    name: app-network
    driver: bridge
"""


def update_devcontainer_config(env_type, dry_run=False):
    """Update devcontainer.json for the selected environment."""
    devcontainer_path = Path(".devcontainer/devcontainer.json")

    if not devcontainer_path.exists():
        print(f"ℹ️  No devcontainer.json found at {devcontainer_path}, skipping...")
        return True

    try:
        # Read current devcontainer.json
        with open(devcontainer_path, encoding="utf-8") as f:
            content = f.read()

        # Determine new port based on environment
        if env_type == "dev":
            new_port = 28001
        elif env_type == "test":
            new_port = 28002
        else:  # production
            new_port = 28000

        # Use regex to find and update forwardPorts
        import re

        port_pattern = r'"forwardPorts"\s*:\s*\[\s*(\d+)\s*\]'
        match = re.search(port_pattern, content)

        if match:
            old_port = int(match.group(1))
            if old_port == new_port:
                if not dry_run:
                    print(
                        f"ℹ️  devcontainer.json already configured for "
                        f"port {new_port}"
                    )
                return True

            if dry_run:
                print("📋 Would update devcontainer.json:")
                print(f"   forwardPorts: [{old_port}] → [{new_port}]")
            else:
                # Replace the port in the content
                new_content = re.sub(
                    port_pattern,
                    f'"forwardPorts": [\n        {new_port}\n    ]',
                    content,
                )

                with open(devcontainer_path, "w", encoding="utf-8") as f:
                    f.write(new_content)

                print("✅ Updated devcontainer.json:")
                print(f"   forwardPorts: [{old_port}] → [{new_port}]")
        else:
            if dry_run:
                print("📋 No forwardPorts found in devcontainer.json to update")
            else:
                print("ℹ️  No forwardPorts found in devcontainer.json to update")

        return True

    except Exception as e:
        print(f"⚠️  Warning: Could not update devcontainer.json: {e}")
        return True  # Don't fail the whole setup for this


def setup_environment(env_type, dry_run=False, force=False):
    """Set up the specified environment."""

    # Auto-copy .env to .local.env with overwrite prompt
    env_file = Path(".env")
    local_env_file = Path(".local.env")
    if env_file.exists():
        should_create_local_env = False

        if not local_env_file.exists():
            should_create_local_env = True
        elif not force and not dry_run:
            prompt = f"\n⚠️  {local_env_file} already exists. Overwrite? (y/N): "
            overwrite = input(prompt).strip().lower()
            should_create_local_env = overwrite == "y"
        elif force:
            should_create_local_env = True
        elif dry_run:
            should_create_local_env = True

        if should_create_local_env:
            if not dry_run:
                # Use binary mode to preserve line endings (especially Linux LF)
                local_env_file.write_bytes(env_file.read_bytes())
                print(f"✅ Created {local_env_file} from {env_file}")
            else:
                if local_env_file.exists():
                    print(f"📋 Would overwrite {local_env_file} from {env_file}")
                else:
                    print(f"📋 Would create {local_env_file} from {env_file}")
        elif local_env_file.exists() and not dry_run:
            print(f"ℹ️  Keeping existing {local_env_file}")
    elif not dry_run:
        print(f"⚠️  Warning: {env_file} not found, cannot create {local_env_file}")

    # Determine configuration
    if env_type == "dev":
        env_name = "Development"
        port = 28001
        container_suffix = "-dev"
        network_name = "app-network"
        volume_name = "postgres-data"
        override_content = create_development_override()
    elif env_type == "test":
        env_name = "Test"
        port = 28002
        container_suffix = "-test"
        network_name = "test-app-network"
        volume_name = "test-postgres-data"
        override_content = create_test_override()
    else:  # production
        env_name = "Production"
        port = 28000
        container_suffix = ""
        network_name = "app-network"
        volume_name = "postgres-data"
        override_content = create_production_override()

    project_name = Path.cwd().name  # folder name becomes Docker Compose project

    print(f"\n🛠️ Setting up {env_name} environment")
    print(f"   Project: {project_name}")
    print(f"   Django port: {port}")
    print(f"   Network: {project_name}_{network_name}")
    print(f"   Volumes: {project_name}_{volume_name}")
    print(
        f"   Containers: boundlexx-django{container_suffix}, "
        f"boundlexx-postgres{container_suffix}, etc."
    )

    # Check for existing override file
    override_path = Path("docker-compose.override.yml")
    if override_path.exists() and not force and not dry_run:
        prompt = f"\n⚠️  {override_path} already exists. Overwrite? (y/N): "
        overwrite = input(prompt).strip().lower()
        if overwrite != "y":
            print("❌ Setup cancelled")
            return False

    if dry_run:
        print(f"\n📋 Dry run: Would write to {override_path}")
        print("--- Content preview ---")
        if len(override_content) > 500:
            preview = override_content[:500] + "..."
        else:
            preview = override_content
        print(preview)

        # Also preview devcontainer updates
        update_devcontainer_config(env_type, dry_run=True)
        return True

    # Write the override file
    try:
        override_path.write_text(override_content)
        print(f"✅ Created {override_path}")
    except Exception as e:
        print(f"❌ Error writing {override_path}: {e}")
        return False

    # Update devcontainer.json for the selected environment
    update_devcontainer_config(env_type, dry_run)

    print(f"\n🌐 Your {env_name} environment is ready!")
    print(f"   Access Django at: http://localhost:{port}")
    print(f"   Container naming: {project_name}_{container_suffix}[service]-1")
    print("\n💡 Next steps:")
    print("   1. Start containers: docker-compose up -d")
    print("   2. Check status: docker ps")
    print("   3. Run migrations:")
    print("      docker-compose run --rm manage python manage.py migrate")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Unified Boundlexx container setup script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python setup_containers.py                       # Interactive mode
  python setup_containers.py --env dev             # Development setup
  python setup_containers.py --env test            # Test setup
  python setup_containers.py --env production      # Production setup
  python setup_containers.py --env dev --dry-run   # Preview dev setup
""",
    )

    parser.add_argument(
        "--env",
        choices=["dev", "test", "production"],
        help="Environment type: dev (28001), test (28002), or production (28000)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview configuration without writing files",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files without prompting",
    )

    args = parser.parse_args()

    # Interactive mode if no environment specified
    if not args.env:
        args.env = get_environment_choice()

    success = setup_environment(args.env, dry_run=args.dry_run, force=args.force)

    if not success:
        sys.exit(1)

    print("\n✨ Setup complete!")


if __name__ == "__main__":
    main()
