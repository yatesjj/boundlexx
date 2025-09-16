# Archived Container Setup Scripts

This folder contains the previous version of the container setup scripts that were replaced by the unified `setup_containers.py` script.

## Archived Files

- `archive_setup_development_container_improved.py` - Original development environment setup script
- `archive_setup_test_container.py` - Original test environment setup script

## Why They Were Replaced

The original scripts used folder-based automatic naming which created confusion and complexity:
- Containers were named based on the current folder (e.g., `boundlexx-yatesjj-django-1`)
- Port management was complex with configurable offsets
- Two separate scripts to maintain

## New Unified Approach

The new `setup_containers.py` script simplifies this with:
- Fixed naming: `boundlexx` for development, `boundlexx-test` for test environments
- Fixed ports: 28000 for dev, 28001 for test
- Single script with environment selection
- Clear separation between development and test setups

## Migration

If you were using the old scripts:
1. Stop any running containers: `docker-compose down`
2. Use the new script: `python setup_containers.py --env dev` or `python setup_containers.py --env test`
3. Start containers: `docker-compose up -d`

The new approach ensures consistent naming and eliminates confusion between parallel environments.