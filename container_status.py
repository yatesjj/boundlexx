#!/usr/bin/env python3
"""
container_status.py

Utility script to check the status of container management configurations.
Shows which scripts have been run and current port/name configurations.
"""
import argparse
import re
from pathlib import Path


def check_container_status():
    """Check current container configuration status."""
    repo_dir = Path(__file__).resolve().parent
    folder_name = repo_dir.name

    compose_file = repo_dir / 'docker-compose.yml'
    override_file = repo_dir / 'docker-compose.override.yml'
    env_file = repo_dir / '.env'

    print(f"Container Status for '{folder_name}'")
    print("=" * 50)

    # Check if files exist
    files_status = {
        'docker-compose.yml': compose_file.exists(),
        'docker-compose.override.yml': override_file.exists(),
        '.env': env_file.exists()
    }

    print("Files present:")
    for file, exists in files_status.items():
        status = "✅" if exists else "❌"
        print(f"  {status} {file}")

    if not compose_file.exists():
        print("\n❌ Main docker-compose.yml not found!")
        return

    # Check for container name prefixes
    compose_content = compose_file.read_text()

    # Look for container names
    container_names = re.findall(r'container_name:\s*([\w-]+)', compose_content)

    print(f"\nContainer Names Found ({len(container_names)}):")
    has_prefixes = False
    for name in container_names:
        prefixed = name.startswith(folder_name)
        if prefixed:
            has_prefixes = True
        status = "✅" if prefixed else "⚠️"
        print(f"  {status} {name}")

    # Check for port mappings in override
    ports_found = []
    if override_file.exists():
        override_content = override_file.read_text()
        port_matches = re.findall(r'"?(\d{4,5}):(\d{4,5})"?', override_content)
        ports_found = port_matches

    print(f"\nPort Mappings Found ({len(ports_found)}):")
    for host_port, container_port in ports_found:
        offset = int(host_port) - int(container_port) if host_port != container_port else 0
        offset_info = f" (+{offset})" if offset > 0 else ""
        print(f"  📡 {host_port}:{container_port}{offset_info}")

    # Determine configuration type
    print(f"\nConfiguration Analysis:")
    if has_prefixes and not ports_found:
        print("  🔧 Development setup detected (prefixed names, no port offsets)")
    elif has_prefixes and any(int(hp) != int(cp) for hp, cp in ports_found):
        print("  🧪 Test setup detected (prefixed names + port offsets)")
    elif not has_prefixes and not ports_found:
        print("  📦 Default setup (no customization)")
    else:
        print("  ❓ Mixed/custom configuration")

    # Check for parallel test files
    parallel_files = list(repo_dir.glob('*.instance*'))
    if parallel_files:
        print(f"\nParallel Test Files ({len(parallel_files)}):")
        for pfile in parallel_files:
            print(f"  🔄 {pfile.name}")

    print(f"\nRecommendations:")
    if not has_prefixes:
        print("  • Run setup_development_container.py to add name prefixes")
    if not container_names:
        print("  • Add explicit container_name fields to docker-compose.yml")
    if parallel_files:
        print("  • Consider cleaning up old parallel test files")


def main():
    parser = argparse.ArgumentParser(
        description='Check container management configuration status'
    )
    args = parser.parse_args()
    check_container_status()


if __name__ == '__main__':
    main()
