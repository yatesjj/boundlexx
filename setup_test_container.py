#!/usr/bin/env python3
"""
setup_test_container.py

Automatically updates docker-compose.yml, docker-compose.override.yml, and .env to:
- Offset all host ports by +1 (e.g., 8000→8001, 5432→5433)
- Prefix all service/container/network names with the current folder name
- Update environment variables referencing ports/names

Usage: Run this script from the root of your cloned test repo after cloning.
"""
import argparse
import re
from pathlib import Path


def setup_test_container(dry_run=False):
    """Set up test container with port offsets and folder name prefixes."""
    # Get current folder name for prefixing
    repo_dir = Path(__file__).resolve().parent
    folder_name = repo_dir.parent.name

    # Files to update
    compose_files = [
        repo_dir / "docker-compose.yml",
        repo_dir / "docker-compose.override.yml",
    ]
    env_file = repo_dir / ".env"

    # Regex patterns
    port_pattern = re.compile(
        r'(["\']?)(\d{4,5})(["\']?):(\d{4,5})'
    )  # e.g., "8001:8000"
    name_pattern = re.compile(r"(container_name|service|network|name):\s*([\w-]+)")

    def offset_port(match):
        prefix, host_port, suffix, container_port = match.groups()
        try:
            new_host_port = str(int(host_port) + 1)
        except Exception:
            new_host_port = host_port
        return f"{prefix}{new_host_port}{suffix}:{container_port}"

    def prefix_name(match):
        key, value = match.groups()
        if value.startswith(folder_name):
            return match.group(0)
        return f"{key}: {folder_name}-{value}"

    def update_yaml_file(path):
        if not path.exists():
            print(f"Warning: {path} does not exist, skipping...")
            return

        text = path.read_text(encoding="utf-8")
        original_text = text

        # Offset ports
        text = port_pattern.sub(offset_port, text)
        # Prefix names
        text = name_pattern.sub(prefix_name, text)

        if dry_run:
            if text != original_text:
                print(f"Would update {path}")
            else:
                print(f"No changes needed for {path}")
        else:
            path.write_text(text, encoding="utf-8")
            print(f"Updated {path}")

    def update_env_file(path):
        if not path.exists():
            print(f"Warning: {path} does not exist, skipping...")
            return

        lines = path.read_text(encoding="utf-8").splitlines()
        new_lines = []
        changes_made = False

        for line in lines:
            # Offset port numbers in env vars
            m = re.match(r"([A-Z_]+)=(\d{4,5})", line)
            if m:
                key, port = m.groups()
                try:
                    new_port = str(int(port) + 1)
                    new_lines.append(f"{key}={new_port}")
                    changes_made = True
                    continue
                except Exception:
                    pass
            # Prefix names in env vars
            m2 = re.match(r"([A-Z_]+)=(.+)", line)
            if m2 and not m2.group(2).startswith(folder_name):
                key, value = m2.groups()
                if "NAME" in key or "SERVICE" in key or "NETWORK" in key:
                    new_lines.append(f"{key}={folder_name}-{value}")
                    changes_made = True
                    continue
            new_lines.append(line)

        if dry_run:
            if changes_made:
                print(f"Would update {path}")
            else:
                print(f"No changes needed for {path}")
        else:
            path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
            print(f"Updated {path}")

    # Process files
    for f in compose_files:
        update_yaml_file(f)
    update_env_file(env_file)

    if not dry_run:
        print(
            f'All done! Test container is now unique to "{folder_name}" with port offsets.'
        )
    else:
        print(
            f'Dry run complete. Would configure test container for "{folder_name}" with port offsets.'
        )


def main():
    parser = argparse.ArgumentParser(
        description="Set up test container with port offsets and folder-prefixed names"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making any modifications",
    )

    args = parser.parse_args()
    setup_test_container(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
