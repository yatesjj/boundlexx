#!/usr/bin/env python3
"""
setup_development_container.py

Prefixes all service/container/network names with the current folder name for clear
identification as the development container. Does not change any ports.

Usage: Run this script from the root of your development repo after cloning or to
reset names.
"""
import argparse
import re
from pathlib import Path


def setup_development_containers(dry_run=False, prefix=None):
    """Set up development container with folder name prefixes."""
    # Get current folder name for prefixing
    repo_dir = Path(__file__).resolve().parent

    # Use provided prefix or derive from parent folder context
    if prefix:
        folder_name = prefix
    else:
        # Use parent folder name for meaningful prefixes
        # This handles user's workflow: C:\VSCode\boundlexx-yatesjj\boundlexx\
        # where we want "boundlexx-yatesjj" as the prefix
        folder_name = repo_dir.parent.name

    # Files to update
    compose_files = [
        repo_dir / 'docker-compose.yml',
        repo_dir / 'docker-compose.override.yml',
    ]
    env_file = repo_dir / '.env'

    # Only prefix names, do not change ports
    name_pattern = re.compile(r'(container_name|service|network|name):\s*([\w-]+)')

    def prefix_name(match):
        key, value = match.groups()
        if value.startswith(folder_name):
            return match.group(0)
        return f'{key}: {folder_name}-{value}'

    def update_yaml_file(path):
        if not path.exists():
            print(f"Warning: {path} does not exist, skipping...")
            return

        text = path.read_text(encoding='utf-8')
        original_text = text

        # Only prefix names
        text = name_pattern.sub(prefix_name, text)

        if dry_run:
            if text != original_text:
                print(f"Would update {path}")
            else:
                print(f"No changes needed for {path}")
        else:
            path.write_text(text, encoding='utf-8')
            print(f'Updated {path}')

    def update_env_file(path):
        if not path.exists():
            print(f"Warning: {path} does not exist, skipping...")
            return

        lines = path.read_text(encoding='utf-8').splitlines()
        new_lines = []
        changes_made = False

        for line in lines:
            # Only prefix names in env vars
            m2 = re.match(r'([A-Z_]+)=(.+)', line)
            if m2 and not m2.group(2).startswith(folder_name):
                key, value = m2.groups()
                if 'NAME' in key or 'SERVICE' in key or 'NETWORK' in key:
                    new_lines.append(f'{key}={folder_name}-{value}')
                    changes_made = True
                    continue
            new_lines.append(line)

        if dry_run:
            if changes_made:
                print(f"Would update {path}")
            else:
                print(f"No changes needed for {path}")
        else:
            path.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
            print(f'Updated {path}')

    # Process files
    for f in compose_files:
        update_yaml_file(f)
    update_env_file(env_file)

    if not dry_run:
        print(f'All done! Development container is now unique to "{folder_name}" and uses original ports.')
    else:
        print(f'Dry run complete. Would configure development container for "{folder_name}".')


def main():
    parser = argparse.ArgumentParser(
        description='Set up development container with folder-prefixed names and original ports'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without making any modifications'
    )
    parser.add_argument(
        '--prefix',
        type=str,
        help='Custom prefix for container names (default: auto-detect from git or folder)'
    )

    args = parser.parse_args()
    setup_development_containers(dry_run=args.dry_run, prefix=args.prefix)


if __name__ == '__main__':
    main()
