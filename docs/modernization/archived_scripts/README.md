# Archived Scripts

This directory contains scripts that were developed during the modernization process but are not currently used in the recommended workflow. They are preserved for reference and potential future use.

## Scripts in this directory:

### Container Setup Scripts (Legacy)
- **`archive_setup_containers_broken.py`**: Corrupted version of setup script (Sept 2025)
- **`archive_setup_development_container_improved.py`**: Early development container setup
- **`archive_setup_test_container.py`**: Early test container setup  
- **`archive_run_for_parallel_test_containers.py`**: Complex parallel testing script

### Utility Scripts (Archived Sept 2025)
- **`archive_container_status.py`**: Container configuration status checker
- **`archive_create_test_environment.py`**: Test environment creation utility
- **`archive_chat_log.json`**: Large chat session log from modernization work

### Django-Filter Testing Scripts (Archived Sept 2025)
- **`archive_check_method.py`**: Testing script for checking django-filter method availability
- **`archive_test_25_1.py`**: Testing script for django-filter 25.1 compatibility
- **`archive_test_25_1_simple.py`**: Simplified version of 25.1 testing script  
- **`archive_test_django_filter.py`**: General django-filter version testing script

### Legacy Scripts Status:

#### `archive_run_for_parallel_test_containers.py`
- **Purpose**: Complex parallel testing with temporary docker-compose files
- **Why archived**: The separate folders approach is simpler and more reliable for testing
- **Alternative**: Use separate folders for each test environment (recommended)
- **Complexity**: High - manages temporary files, dynamic port offsets, complex naming
- **Status**: Functional but overkill for current workflow

#### `archive_setup_containers_broken.py`
- **Purpose**: Early unified container setup script
- **Why archived**: Became corrupted during updates (Sept 2025)
- **Alternative**: Current `setup_containers.py` in project root
- **Status**: Corrupted/broken - kept for reference only

#### `archive_container_status.py` & `archive_create_test_environment.py`
- **Purpose**: Utility scripts created during modernization research phase
- **Why archived**: Functionality integrated into main setup script
- **Alternative**: Current `setup_containers.py` handles all setup scenarios
- **Status**: Superseded by unified approach

#### Django-Filter Testing Scripts
- **Purpose**: Temporary scripts created during django-filter version investigation (Sept 2025)
- **Why archived**: One-time testing to verify compatibility between versions 23.5, 24.1, 24.2, 24.3, and 25.1
- **Alternative**: Direct pip testing commands or container environment testing
- **Status**: Research complete - django-filter 24.3 selected as LTS choice until Django Ninja migration

## When to consider using archived scripts:

- If you need to run many parallel test instances from a single repo copy
- If disk space becomes a major constraint  
- If the workflow changes to require more complex testing scenarios
- For historical reference during troubleshooting

## Current recommended workflow:

```bash
# Simple separate folders approach
C:\VSCode\boundlexx-yatesjj\boundlexx-yatesjj\     # Main development
C:\VSCode\boundlexx-test-pr2\boundlexx\            # Test environment
C:\VSCode\boundlexx-experiment\boundlexx\          # Experiment
```

Each folder uses:
- `setup_development_container_improved.py` for main development
- `setup_test_container.py` for test environments with port offsets
