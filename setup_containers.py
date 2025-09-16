#!/usr/bin/env python3
"""
Unified Boundlexx Container Setup Script

Creates Docker Compose override configurations for:
- Development environments (boundlexx prefix, Django on port 28000)
- Test environments (boundlexx-test prefix, Django on port 28001)

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
    print("  1. Development (boundlexx-*, Django on port 28000)")
    print("  2. Test (boundlexx-test-*, Django on port 28001)")
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
# Prefix: boundlexx
# Django port: 28000

services:
  django: &django
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
      - postgres
      - redis
    networks:
      - boundlexx-network

  manage:
    <<: *django
    container_name: boundlexx-manage-1
    ports: []

  test:
    <<: *django
    container_name: boundlexx-test-1
    ports: []

  lint:
    <<: *django
    container_name: boundlexx-lint-1
    ports: []

  format:
    <<: *django
    container_name: boundlexx-format-1
    ports: []

  celery:
    <<: *django
    container_name: boundlexx-celery-1
    ports: []

  celerybeat:
    <<: *django
    container_name: boundlexx-celerybeat-1
    ports: []

  huey-consumer:
    <<: *django
    container_name: boundlexx-huey-consumer-1
    ports: []

  huey-scheduler:
    <<: *django
    container_name: boundlexx-huey-scheduler-1
    ports: []

  postgres:
    container_name: boundlexx-postgres-1
    volumes:
      - boundlexx_postgres_data:/var/lib/postgresql/data
    env_file:
      - ./.env
      - ./.local.env
    networks:
      - boundlexx-network

  redis:
    container_name: boundlexx-redis-1
    networks:
      - boundlexx-network

volumes:
  boundlexx_postgres_data:

networks:
  boundlexx-network:
    name: boundlexx-network
    driver: bridge
"""


def create_test_override():
    """Create test environment configuration."""
    return """# Auto-generated test environment override
# Environment: Test
# Prefix: boundlexx-test
# Django port: 28001

services:
  django:
    container_name: boundlexx-test-django-1
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
      - postgres
      - redis
    networks:
      - boundlexx-test-network

  manage:
    container_name: boundlexx-test-manage-1
    env_file:
      - ./.env
      - ./.local.env
    depends_on:
      - postgres
      - redis
    networks:
      - boundlexx-test-network

  test:
    container_name: boundlexx-test-test-1
    env_file:
      - ./.env
      - ./.local.env
    depends_on:
      - postgres
      - redis
    networks:
      - boundlexx-test-network

  lint:
    container_name: boundlexx-test-lint-1
    env_file:
      - ./.env
      - ./.local.env
    depends_on: []
    networks:
      - boundlexx-test-network

  format:
    container_name: boundlexx-test-format-1
    env_file:
      - ./.env
      - ./.local.env
    depends_on: []
    networks:
      - boundlexx-test-network

  celery:
    container_name: boundlexx-test-celery-1
    env_file:
      - ./.env
      - ./.local.env
    depends_on:
      - postgres
      - redis
    networks:
      - boundlexx-test-network

  celerybeat:
    container_name: boundlexx-test-celerybeat-1
    env_file:
      - ./.env
      - ./.local.env
    depends_on:
      - postgres
      - redis
    networks:
      - boundlexx-test-network

  huey-consumer:
    container_name: boundlexx-test-huey-consumer-1
    entrypoint: /usr/local/bin/start-huey-consumer
    env_file:
      - ./.env
      - ./.local.env
    depends_on:
      - postgres
      - redis
    networks:
      - boundlexx-test-network

  huey-scheduler:
    container_name: boundlexx-test-huey-scheduler-1
    entrypoint: /usr/local/bin/start-huey-scheduler
    env_file:
      - ./.env
      - ./.local.env
    depends_on:
      - postgres
      - redis
    networks:
      - boundlexx-test-network

  postgres:
    container_name: boundlexx-test-postgres-1
    volumes:
      - boundlexx-test_postgres_data:/var/lib/postgresql/data
    env_file:
      - ./.env
      - ./.local.env
    networks:
      - boundlexx-test-network

  redis:
    container_name: boundlexx-test-redis-1
    networks:
      - boundlexx-test-network

volumes:
  boundlexx-test_postgres_data:

networks:
  boundlexx-test-network:
    name: boundlexx-test-network
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
        with open(devcontainer_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Determine new port based on environment
        new_port = 28000 if env_type == "dev" else 28001
        
        # Use regex to find and update forwardPorts
        import re
        port_pattern = r'"forwardPorts"\s*:\s*\[\s*(\d+)\s*\]'
        match = re.search(port_pattern, content)
        
        if match:
            old_port = int(match.group(1))
            if old_port == new_port:
                if not dry_run:
                    print(f"ℹ️  devcontainer.json already configured for "
                          f"port {new_port}")
                return True
            
            if dry_run:
                print("📋 Would update devcontainer.json:")
                print(f"   forwardPorts: [{old_port}] → [{new_port}]")
            else:
                # Replace the port in the content
                new_content = re.sub(
                    port_pattern,
                    f'"forwardPorts": [\n        {new_port}\n    ]',
                    content
                )
                
                with open(devcontainer_path, 'w', encoding='utf-8') as f:
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
    
    # Auto-copy .env to .local.env if missing
    env_file = Path(".env")
    local_env_file = Path(".local.env")
    if not local_env_file.exists() and env_file.exists():
        if not dry_run:
            local_env_file.write_text(env_file.read_text())
            print(f"✅ Created {local_env_file} from {env_file}")
        else:
            print(f"📋 Would create {local_env_file} from {env_file}")

    # Determine configuration
    if env_type == "dev":
        prefix = "boundlexx"
        port = 28000
        override_content = create_development_override()
    else:  # test
        prefix = "boundlexx-test"
        port = 28001
        override_content = create_test_override()

    print(f"\n🛠️ Setting up {env_type} environment")
    print(f"   Prefix: {prefix}")
    print(f"   Django port: {port}")
    print(f"   Network: {prefix}-network")
    print(f"   Volumes: {prefix}_postgres_data")

    # Check for existing override file
    override_path = Path("docker-compose.override.yml")
    if override_path.exists() and not force and not dry_run:
        prompt = f"\n⚠️  {override_path} already exists. Overwrite? (y/N): "
        overwrite = input(prompt).strip().lower()
        if overwrite != 'y':
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

    print(f"\n🌐 Your {env_type} environment is ready!")
    print(f"   Access Django at: http://localhost:{port}")
    print(f"   Container prefix: {prefix}")
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
  python setup_containers.py                    # Interactive mode
  python setup_containers.py --env dev          # Development setup
  python setup_containers.py --env test         # Test setup
  python setup_containers.py --env dev --dry-run  # Preview dev setup
"""
    )
    
    parser.add_argument(
        '--env', choices=['dev', 'test'],
        help='Environment type: dev (port 28000) or test (port 28001)'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Preview configuration without writing files'
    )
    parser.add_argument(
        '--force', action='store_true',
        help='Overwrite existing files without prompting'
    )

    args = parser.parse_args()

    # Interactive mode if no environment specified
    if not args.env:
        args.env = get_environment_choice()

    success = setup_environment(args.env, dry_run=args.dry_run, force=args.force)
    
    if not success:
        sys.exit(1)

    print("\n✨ Setup complete!")


if __name__ == '__main__':
    main()
