# Archived Scripts

This directory contains scripts that were developed during the modernization process but are not currently used in the recommended workflow. They are preserved for reference and potential future use.

## Scripts in this directory:

### `archive_run_for_parallel_test_containers.py`
- **Purpose**: Complex parallel testing with temporary docker-compose files
- **Why archived**: The separate folders approach is simpler and more reliable for testing
- **Alternative**: Use separate folders for each test environment (recommended)
- **Complexity**: High - manages temporary files, dynamic port offsets, complex naming
- **Status**: Functional but overkill for current workflow

## When to consider using archived scripts:

- If you need to run many parallel test instances from a single repo copy
- If disk space becomes a major constraint  
- If the workflow changes to require more complex testing scenarios

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
