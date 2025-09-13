# Container Management Scripts

This document describes the container management scripts available in the Boundlexx project for managing different development and testing environments.

## Overview

The Boundlexx project includes three Python scripts that help manage Docker container environments:

1. **`setup_development_container.py`** - Development environment setup
2. **`setup_test_container.py`** - Test environment setup
3. **`run_for_parallel_test_containers.py`** - Parallel test instance management

## Scripts Description

### setup_development_container.py

**Purpose:** Sets up a development container environment with clear identification.

**What it does:**
- Prefixes all service/container/network names with the current folder name
- Maintains original ports (8000, 5432, 6379, etc.)
- Updates both docker-compose files and environment variables

**Usage:**
```bash
python setup_development_container.py
```

**Example output:**
- Container names: `boundlexx-app-django`, `boundlexx-app-postgres`
- Ports: 8000:8000, 5432:5432 (unchanged)

### setup_test_container.py

**Purpose:** Sets up a test container environment that can run alongside development.

**What it does:**
- Prefixes all service/container/network names with the current folder name
- Offsets all host ports by +1 (8000→8001, 5432→5433, etc.)
- Updates both docker-compose files and environment variables

**Usage:**
```bash
python setup_test_container.py
```

**Example output:**
- Container names: `boundlexx-test-django`, `boundlexx-test-postgres`
- Ports: 8001:8000, 5433:5432 (offset by +1)

### run_for_parallel_test_containers.py

**Purpose:** Dynamically creates and manages multiple parallel test instances.

**What it does:**
- Creates temporary docker-compose and .env files for each instance
- Offsets ports by the instance number (instance 1 = +1, instance 2 = +2, etc.)
- Prefixes names with folder name + instance suffix
- Automatically cleans up temporary files when containers are stopped

**Usage:**
```bash
# Start instance 1 (ports offset by +1)
python run_for_parallel_test_containers.py --instance 1

# Start instance 2 (ports offset by +2)
python run_for_parallel_test_containers.py --instance 2

# Run specific docker-compose command
python run_for_parallel_test_containers.py --instance 3 logs django

# Stop and cleanup
python run_for_parallel_test_containers.py --instance 1 down

# Cleanup only (without running containers)
python run_for_parallel_test_containers.py --instance 2 --cleanup-only
```

**Example output for instance 2:**
- Container names: `boundlexx-app-instance2-django`, `boundlexx-app-instance2-postgres`
- Ports: 8002:8000, 5434:5432 (offset by +2)
- Temporary files: `docker-compose.instance2.yml`, `.env.instance2`

## Use Cases

### Development Workflow
1. Run `setup_development_container.py` once after cloning
2. Use standard docker-compose commands for development
3. Access at http://localhost:8000

### Testing Workflow
1. Keep development environment running
2. Run `setup_test_container.py` in a separate clone/branch
3. Access test environment at http://localhost:8001

### Parallel Testing
1. Use `run_for_parallel_test_containers.py` for CI/CD or multiple test scenarios
2. Each instance gets unique ports and names
3. No interference between instances

## Port Mapping Examples

| Environment | Script | Django | Postgres | Redis | Access URL |
|-------------|--------|--------|----------|-------|------------|
| Development | `setup_development_container.py` | 8000 | 5432 | 6379 | http://localhost:8000 |
| Test | `setup_test_container.py` | 8001 | 5433 | 6380 | http://localhost:8001 |
| Parallel Instance 1 | `run_for_parallel_test_containers.py --instance 1` | 8001 | 5433 | 6380 | http://localhost:8001 |
| Parallel Instance 2 | `run_for_parallel_test_containers.py --instance 2` | 8002 | 5434 | 6381 | http://localhost:8002 |
| Parallel Instance 3 | `run_for_parallel_test_containers.py --instance 3` | 8003 | 5435 | 6382 | http://localhost:8003 |

## File Modifications

### What Files Are Modified

**Development and Test Scripts:**
- `docker-compose.yml`
- `docker-compose.override.yml`
- `.env`

**Parallel Script:**
- Creates temporary files: `docker-compose.instance{N}.yml`, `.env.instance{N}`
- Does not modify original files

### Regex Patterns Used

**Port Pattern:** `(["\']?)(\d{4,5})(["\']?):(\d{4,5})`
- Matches port mappings like `"8000:8000"`, `8001:8000`

**Name Pattern:** `(container_name|service|network|name):\s*([\w-]+)`
- Matches container names, service names, network names

**Environment Variable Patterns:**
- Port variables: `([A-Z_]+)=(\d{4,5})`
- Name variables: `([A-Z_]+)=(.+)` where key contains 'NAME', 'SERVICE', or 'NETWORK'

## Rollback Instructions

### Development/Test Scripts
If you need to undo changes made by the setup scripts:

1. **Git rollback (recommended):**
   ```bash
   git checkout -- docker-compose.yml docker-compose.override.yml .env
   ```

2. **Manual rollback:**
   - Remove folder name prefixes from container names
   - Reset ports to original values (8000, 5432, 6379, etc.)
   - Update environment variables accordingly

### Parallel Script
The parallel script automatically cleans up temporary files when you run:
```bash
python run_for_parallel_test_containers.py --instance {N} down
```

Or manually cleanup:
```bash
python run_for_parallel_test_containers.py --instance {N} --cleanup-only
```

## Best Practices

1. **Use development script once** after cloning the repo for your main development environment
2. **Use test script** in separate clones or branches for testing
3. **Use parallel script** for automated testing, CI/CD, or when you need multiple test instances
4. **Always specify instance numbers** starting from 1 for the parallel script
5. **Clean up parallel instances** when done to free up ports and resources
6. **Keep track of which ports are in use** to avoid conflicts

## Troubleshooting

### Port Already in Use
If you get port binding errors:
- Check what's running on the port: `lsof -i :8000`
- Use a different instance number for parallel testing
- Stop other containers using the same ports

### Container Name Conflicts
If you get container name conflicts:
- The scripts should handle this automatically with prefixing
- Check if containers from previous runs are still running: `docker ps -a`
- Remove conflicting containers: `docker rm container-name`

### Temporary Files Not Cleaned
If parallel script temporary files remain:
```bash
# Manual cleanup
rm -f docker-compose.instance*.yml .env.instance*

# Or use the cleanup flag
python run_for_parallel_test_containers.py --instance {N} --cleanup-only
```
