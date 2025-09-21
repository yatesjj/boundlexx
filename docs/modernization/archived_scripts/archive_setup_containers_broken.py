#!/usr/bin/env python3
"""
Unified Boundlexx Container Setup Script

Creates Docker Compose override configurations for:
- Development environments (Django on port 28001)
- Test environments (test- prefix, Django on port 28002)

Modern clean naming with explicit container names and environment-specific prefixes.

Usage:
    python setup_containers.py                    # Interactive mode
    python setup_containers.py --env dev          # Development setup
    python setup_containers.py --env test         # Test setup
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
    print("  1. Development (dev-boundlexx-*, Django on port 28001)")
    print("  2. Test (test-boundlexx-*, Django on port 28002)")
    print()

    while True:
        choice = input("Enter choice (1 or 2): ").strip()
        if choice == "1":
            return "dev"
        elif choice == "2":
            return "test"
        else:
            print("Invalid choice. Please enter 1 or 2.")


def create_development_override():
    """Create development environment configuration."""
    return """# Auto-generated development environment override
# Environment: Development
# Django port: 28001 (dev = base + 1)

services:
  boundlexx-django:
    container_name: dev-boundlexx-django-1
    ports:
      - "28001:8000"
    networks:
      - dev-boundlexx-network
    labels:
      app.kubernetes.io/name: boundlexx
      app.kubernetes.io/component: django
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: dev-boundlexx
      app.kubernetes.io/environment: development

  boundlexx-manage:
    container_name: dev-boundlexx-manage-1
    networks:
      - dev-boundlexx-network
    labels:
      app.kubernetes.io/name: boundlexx
      app.kubernetes.io/component: manage
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: dev-boundlexx
      app.kubernetes.io/environment: development

  boundlexx-test:
    container_name: dev-boundlexx-test-1
    networks:
      - dev-boundlexx-network
    labels:
      app.kubernetes.io/name: boundlexx
      app.kubernetes.io/component: test
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: dev-boundlexx
      app.kubernetes.io/environment: development

  boundlexx-lint:
    container_name: dev-boundlexx-lint-1
    networks:
      - dev-boundlexx-network
    labels:
      app.kubernetes.io/name: boundlexx
      app.kubernetes.io/component: lint
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: dev-boundlexx
      app.kubernetes.io/environment: development

  boundlexx-format:
    container_name: dev-boundlexx-format-1
    networks:
      - dev-boundlexx-network
    labels:
      app.kubernetes.io/name: boundlexx
      app.kubernetes.io/component: format
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: dev-boundlexx
      app.kubernetes.io/environment: development

  boundlexx-celery:
    container_name: dev-boundlexx-celery-1
    depends_on:
      - boundlexx-postgres
      - boundlexx-redis
    networks:
      - dev-boundlexx-network
    labels:
      app.kubernetes.io/name: boundlexx
      app.kubernetes.io/component: celery
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: dev-boundlexx
      app.kubernetes.io/environment: development

  boundlexx-celerybeat:
    container_name: dev-boundlexx-celerybeat-1
    depends_on:
      - boundlexx-postgres
      - boundlexx-redis
    networks:
      - dev-boundlexx-network
    labels:
      app.kubernetes.io/name: boundlexx
      app.kubernetes.io/component: celerybeat
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: dev-boundlexx
      app.kubernetes.io/environment: development

  boundlexx-huey-consumer:
    container_name: dev-boundlexx-huey-consumer-1
    depends_on:
      - boundlexx-redis
    networks:
      - dev-boundlexx-network
    labels:
      app.kubernetes.io/name: boundlexx
      app.kubernetes.io/component: huey-consumer
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: dev-boundlexx
      app.kubernetes.io/environment: development

  boundlexx-huey-scheduler:
    container_name: dev-boundlexx-huey-scheduler-1
    depends_on:
      - boundlexx-redis
    networks:
      - dev-boundlexx-network
    labels:
      app.kubernetes.io/name: boundlexx
      app.kubernetes.io/component: huey-scheduler
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: dev-boundlexx
      app.kubernetes.io/environment: development

  boundlexx-postgres:
    container_name: dev-boundlexx-postgres-1
    volumes:
      - dev-boundlexx-postgres-data:/var/lib/postgresql/data
    networks:
      - dev-boundlexx-network
    labels:
      app.kubernetes.io/name: boundlexx
      app.kubernetes.io/component: postgres
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: dev-boundlexx
      app.kubernetes.io/environment: development

  boundlexx-redis:
    container_name: dev-boundlexx-redis-1
    volumes:
      - dev-boundlexx-redis-data:/data
    networks:
      - dev-boundlexx-network
    labels:
      app.kubernetes.io/name: boundlexx
      app.kubernetes.io/component: redis
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: dev-boundlexx
      app.kubernetes.io/environment: development

volumes:
  dev-boundlexx-postgres-data:
  dev-boundlexx-redis-data:

networks:
  dev-boundlexx-network:
    name: dev-boundlexx-network
    driver: bridge
"""
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
      - dev-boundlexx-postgres
      - dev-boundlexx-redis
    networks:
      - dev-boundlexx-network
    labels:
      app.kubernetes.io/name: boundlexx
      app.kubernetes.io/component: django
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: dev-boundlexx
      app.kubernetes.io/environment: development

  dev-boundlexx-manage:
    <<: *django
    container_name: dev-boundlexx-manage-1
    ports: []

  dev-boundlexx-test:
    <<: *django
    container_name: dev-boundlexx-test-1
    ports: []

  dev-boundlexx-lint:
    <<: *django
    container_name: dev-boundlexx-lint-1
    ports: []

  dev-boundlexx-format:
    <<: *django
    container_name: dev-boundlexx-format-1
    ports: []

  dev-boundlexx-celery:
    <<: *django
    container_name: dev-boundlexx-celery-1
    ports: []

  dev-boundlexx-celerybeat:
    <<: *django
    container_name: dev-boundlexx-celerybeat-1
    ports: []

  dev-boundlexx-huey-consumer:
    <<: *django
    container_name: dev-boundlexx-huey-consumer-1
    ports: []

  dev-boundlexx-huey-scheduler:
    <<: *django
    container_name: dev-boundlexx-huey-scheduler-1
    ports: []

  dev-boundlexx-postgres:
    container_name: dev-boundlexx-postgres-1
    volumes:
      - dev-boundlexx-postgres-data:/var/lib/postgresql/data
    env_file:
      - ./.env
      - ./.local.env
    networks:
      - dev-boundlexx-network
    labels:
      app.kubernetes.io/name: boundlexx
      app.kubernetes.io/component: postgres
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: dev-boundlexx
      app.kubernetes.io/environment: development

  dev-boundlexx-redis:
    container_name: dev-boundlexx-redis-1
    networks:
      - dev-boundlexx-network
    labels:
      app.kubernetes.io/name: boundlexx
      app.kubernetes.io/component: redis
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: dev-boundlexx
      app.kubernetes.io/environment: development

volumes:
  dev-boundlexx-postgres-data:

networks:
  dev-boundlexx-network:
    name: dev-boundlexx-network
    driver: bridge
"""


def create_test_override():
    """Create test environment configuration."""
    return """# Auto-generated test environment override
# Environment: Test
# Django port: 28002 (test = base + 2)

services:
  test-boundlexx-django: &django
    container_name: test-boundlexx-django-1
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
      - test-boundlexx-postgres
      - test-boundlexx-redis
    networks:
      - test-boundlexx-network
    labels:
      app.kubernetes.io/name: boundlexx
      app.kubernetes.io/component: django
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: test-boundlexx
      app.kubernetes.io/environment: test

  test-boundlexx-manage:
    <<: *django
    container_name: test-boundlexx-manage-1
    ports: []

  test-boundlexx-test:
    <<: *django
    container_name: test-boundlexx-test-1
    ports: []

  test-boundlexx-lint:
    <<: *django
    container_name: test-boundlexx-lint-1
    ports: []

  test-boundlexx-format:
    <<: *django
    container_name: test-boundlexx-format-1
    ports: []

  test-boundlexx-celery:
    <<: *django
    container_name: test-boundlexx-celery-1
    ports: []

  test-boundlexx-celerybeat:
    <<: *django
    container_name: test-boundlexx-celerybeat-1
    ports: []

  test-boundlexx-huey-consumer:
    <<: *django
    container_name: test-boundlexx-huey-consumer-1
    ports: []

  test-boundlexx-huey-scheduler:
    <<: *django
    container_name: test-boundlexx-huey-scheduler-1
    ports: []

  test-boundlexx-postgres:
    container_name: test-boundlexx-postgres-1
    volumes:
      - test-boundlexx-postgres-data:/var/lib/postgresql/data
    env_file:
      - ./.env
      - ./.local.env
    networks:
      - test-boundlexx-network
    labels:
      app.kubernetes.io/name: boundlexx
      app.kubernetes.io/component: postgres
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: test-boundlexx
      app.kubernetes.io/environment: test

  test-boundlexx-redis:
    container_name: test-boundlexx-redis-1
    networks:
      - test-boundlexx-network
    labels:
      app.kubernetes.io/name: boundlexx
      app.kubernetes.io/component: redis
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: test-boundlexx
      app.kubernetes.io/environment: test

volumes:
  test-boundlexx-postgres-data:

networks:
  test-boundlexx-network:
    name: test-boundlexx-network
    driver: bridge
"""


def create_production_override():
    """Create production environment configuration."""
    return """# Auto-generated production environment override
# Environment: Production
# Django port: 28000 (production base)

services:
  boundlexx-django:
    container_name: boundlexx-django-1
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
      - boundlexx-network
    labels:
      app.kubernetes.io/name: boundlexx
      app.kubernetes.io/component: django
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx
      app.kubernetes.io/environment: production

  boundlexx-postgres:
    container_name: boundlexx-postgres-1
    volumes:
      - boundlexx-postgres-data:/var/lib/postgresql/data
    env_file:
      - ./.env
      - ./.local.env
    networks:
      - boundlexx-network
    labels:
      app.kubernetes.io/name: boundlexx
      app.kubernetes.io/component: postgres
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx
      app.kubernetes.io/environment: production

  boundlexx-redis:
    container_name: boundlexx-redis-1
    networks:
      - boundlexx-network
    labels:
      app.kubernetes.io/name: boundlexx
      app.kubernetes.io/component: redis
      app.kubernetes.io/part-of: boundlexx
      app.kubernetes.io/instance: boundlexx
      app.kubernetes.io/environment: production

volumes:
  boundlexx-postgres-data:

networks:
  boundlexx-network:
    name: boundlexx-network
    driver: bridge
"""


def preview_changes(environment, override_content):
    """Show what would be written without actually writing."""
    filename = "docker-compose.override.yml"
    
    print(f"\n🔍 Preview mode - {environment.upper()} environment")
    print("=" * 50)
    print(f"Would write to: {filename}")
    print(f"Content length: {len(override_content)} characters")
    print()
    print("Content preview (first 500 characters):")
    print("-" * 40)
    print(override_content[:500])
    if len(override_content) > 500:
        print("...")
        print(f"({len(override_content) - 500} more characters)")
    print()


def write_override_file(environment, override_content, dry_run=False):
    """Write the Docker Compose override file."""
    override_file = Path("docker-compose.override.yml")
    
    if dry_run:
        preview_changes(environment, override_content)
        return True
    
    try:
        override_file.write_text(override_content, encoding='utf-8')
        print(f"✅ Created {override_file} for {environment} environment")
        print(f"   Django port: {28001 if environment == 'dev' else 28002 if environment == 'test' else 28000}")
        print(f"   Container prefix: {environment + '-' if environment != 'production' else ''}boundlexx-")
        return True
    except Exception as e:
        print(f"❌ Error writing {override_file}: {e}")
        return False


def main():
    """Main script execution."""
    parser = argparse.ArgumentParser(
        description="Setup Boundlexx Docker Compose environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python setup_containers.py                    # Interactive mode
    python setup_containers.py --env dev          # Development setup
    python setup_containers.py --env test         # Test setup
    python setup_containers.py --env production   # Production setup
    python setup_containers.py --dry-run          # Preview without writing
        """
    )
    
    parser.add_argument(
        "--env", 
        choices=["dev", "test", "production"],
        help="Environment type to setup"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Preview changes without writing files"
    )
    
    args = parser.parse_args()
    
    # Determine environment
    if args.env:
        environment = args.env
    else:
        environment = get_environment_choice()
    
    # Generate configuration
    if environment == "dev":
        override_content = create_development_override()
    elif environment == "test":
        override_content = create_test_override()
    elif environment == "production":
        override_content = create_production_override()
    else:
        print(f"❌ Unknown environment: {environment}")
        return 1
    
    # Write or preview
    success = write_override_file(environment, override_content, dry_run=args.dry_run)
    
    if success and not args.dry_run:
        print()
        print("🚀 Next steps:")
        print("   1. Review the generated docker-compose.override.yml")
        print("   2. Update volume paths if needed (Boundless install, icon renderer)")
        print("   3. Start services: docker-compose up -d")
        print()
        
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())