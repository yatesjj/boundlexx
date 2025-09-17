# Boundlexx Environment Setup - Complete Technical Guide

This document provides comprehensive technical documentation for setting up, configuring, and troubleshooting Boundlexx development and test environments.

**For quick setup, see:** `README.rst`
**For project tracking, see:** `MODERNIZATION_TRACKING.md`

## 🏗️ Architecture Overview

### Base Files (Committed)
- **`docker-compose.yml`** - Base service definitions, clean and committable
- **`.env`** - Base environment variables, safe defaults
- **`docker-compose.override.example.yml`** - Template for local customizations

### Local Files (Not Committed)
- **`docker-compose.override.yml`** - Your personal local customizations
- **`.local.env`** - Your personal environment variables (paths, API keys, etc.)

## 🚀 Initial Setup Process

### Step 1: Clone and Enter Repository
```bash
# Example folder structure:
C:\VSCode\boundlexx-yatesjj\boundlexx\     # Main development
C:\VSCode\boundlexx-test-pr2\boundlexx\    # Test environment
```

### Step 2: Create Local Environment Files
```bash
# Copy template files to create your local versions
cp .env .local.env
cp docker-compose.override.example.yml docker-compose.override.yml
```


### Step 3: Run the Container Setup Script

Use the unified setup script to configure your environment:

```bash
# Interactive mode (prompts for environment choice)
python setup_containers.py

# Direct environment selection:
python setup_containers.py --env dev     # Development (boundlexx-*, port 28000)
python setup_containers.py --env test    # Test (boundlexx-test-*, port 28001)

# Preview without writing files:
python setup_containers.py --env dev --dry-run
```

This will create a `docker-compose.override.yml` file with the appropriate container names and port mappings for your chosen environment.

### Step 4: Customize Your Local Environment
Edit `.local.env` and `docker-compose.override.yml` for your specific setup:
- Local file paths (Steam, boundless icons, etc.)
- Port preferences
- Additional environment variables

> **Note:** Container setup is now handled by the unified `setup_containers.py` script with simplified naming (boundlexx vs boundlexx-test).

## 🎯 Container Setup Script

### `setup_containers.py`
- **Unified script** for both development and test environments
- **Simple naming:** `boundlexx` for dev, `boundlexx-test` for test
- **Fixed ports:** 28000 for dev, 28001 for test (no offset calculations)
- **Interactive mode** prompts you to choose environment type
- **Complete isolation** with separate networks, volumes, and containers
- **Safe defaults:** Won't overwrite files without confirmation
- **Auto-setup:** Copies `.env` to `.local.env` if missing
- **Does NOT start containers automatically** - you review and start manually

## 🔍 Verification

After setup, verify your containers are properly named:
```bash
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}"
```

Expected output for **development**:
```
NAMES                    IMAGE                PORTS
boundlexx-django-1       boundlexx_dev_django 28000/tcp
boundlexx-postgres-1     boundlexx_postgres   5432/tcp
boundlexx-redis-1        redis:5.0            6379/tcp
```

Expected output for **test**:
```
NAMES                         IMAGE                PORTS
boundlexx-test-django-1       boundlexx_dev_django 28001/tcp
boundlexx-test-postgres-1     boundlexx_postgres   5432/tcp
boundlexx-test-redis-1        redis:5.0            6379/tcp
```

## ✅ Best Practices

1. **Never commit** `docker-compose.override.yml` or `.local.env`
2. **Always use** the setup script for consistent naming
3. **Keep base files clean** - put customizations in override files
4. **Choose your environment** clearly (dev vs test)
5. **Document** any custom setup in your override files


## CI/CD & Automated Container Builds

Boundlexx uses a modern GitHub Actions workflow to automate building, testing, and linting of all Docker containers on every push to the default branch. This ensures that the project is always in a deployable state and that container builds are reproducible and reliable.

- The workflow is defined in `.github/workflows/ci.yml`.
- On every push, GitHub Actions will:
   - Build all Docker images using Docker Buildx with advanced caching.
   - Run all linters (e.g., ruff, mypy) and tests (pytest) inside containers.
   - Automatically tag and push images to the GitHub Container Registry if configured.
- Workflow status and logs can be monitored in the GitHub Actions tab.
- For troubleshooting, see `docs/modernization/WORKFLOW_MONITORING.md`.

For a detailed breakdown of the workflow, changes, and rollback instructions, see `docs/modernization/GITHUB_ACTIONS_UPDATE.md`.

## 🔄 Multi-Environment Workflow (Recommended)

For testing multiple branches/PRs, use **separate folders** for complete isolation:

```bash
# Create separate folders for each environment
C:\VSCode\boundlexx-main\           # Main development (boundlexx-*)
C:\VSCode\boundlexx-test-pr2\       # Test PR #2 (boundlexx-test-*)
C:\VSCode\boundlexx-experiment\     # Experimental branch

# Each gets its own environment type:
cd C:\VSCode\boundlexx-main && python setup_containers.py --env dev
cd C:\VSCode\boundlexx-test-pr2 && python setup_containers.py --env test
cd C:\VSCode\boundlexx-experiment && python setup_containers.py --env test
```

### Setup Process for Each Environment:

1. **Clone into meaningful folder structure**
2. **Copy template files**: `cp .env .local.env` and `cp docker-compose.override.example.yml docker-compose.override.yml`
3. **Run the unified setup script**:
   - `python setup_containers.py --env dev` for main development
   - `python setup_containers.py --env test` for test environments
4. **Customize local files** as needed

### Benefits of This Approach:

This prevents container name conflicts and makes it easy to run multiple environments simultaneously.

This prevents container name conflicts and makes it easy to run multiple environments simultaneously.

## 🧪 Testing Container Management Changes


When making changes to container management scripts or Docker configuration, use the following workflow:

1. **Setup Test Environment:**
   - Clone the repo to a test location
   - Copy `.env` to `.local.env` and `docker-compose.override.example.yml` to `docker-compose.override.yml`
2. **Test the unified setup script:**
   - Run `python setup_containers.py --env test --dry-run` to preview changes
   - Run `python setup_containers.py --env test` to apply changes
3. **Verify Isolation:**
   - Start the test environment with `docker-compose up -d`
   - Check containers with `docker ps --format "table {{.Names}}\t{{.Ports}}"`
   - Ensure no conflicts with main development
4. **Test Functionality:**
   - Test database and web application as needed
5. **Cleanup:**
   - Stop and remove test containers with `docker-compose down` and `docker system prune -f`
   - Remove the test directory when done

### Environment Comparison


| Environment Type | Container Names | Ports | Script | Use Case |
|------------------|----------------|-------|--------|----------|
| **Development**  | `boundlexx-django-1`, `boundlexx-postgres-1` | Django: 28000, Others: internal | `setup_containers.py --env dev` | Daily development |
| **Test**         | `boundlexx-test-django-1`, `boundlexx-test-postgres-1` | Django: 28001, Others: internal | `setup_containers.py --env test` | PR testing, parallel dev |

### Benefits of Test Environment Approach:
- ✅ **Safe testing** - No risk to main development data
- ✅ **Port isolation** - Automatic port offsets prevent conflicts
- ✅ **Quick setup** - Standardized testing workflow
- ✅ **Easy cleanup** - Complete environment removal in one command
- ✅ **Parallel development** - Run main and test environments simultaneously

## 📊 Container Management Scripts Reference


### Available Script

| Script | Purpose | Port Strategy | Container Names | Use Case |
|--------|---------|---------------|-----------------|----------|
| `setup_containers.py` | Unified dev/test setup | Dev: 28000, Test: 28001 | `boundlexx-django-1`, `boundlexx-test-django-1` | All environment setup |

### Port Mapping Details


**Development Environment:**
- **Django:** `28000:8000` (external access)
- **PostgreSQL:** Internal only (`5432`)
- **Redis:** Internal only (`6379`)
- **MailHog:** Internal only (`8025`)

**Test Environment:**
- **Django:** `28001:8000` (external access)
- **PostgreSQL:** Internal only (`5432`)
- **Redis:** Internal only (`6379`)
- **MailHog:** Internal only (`8025`)

### Folder-Based Automatic Naming

## 🔧 Troubleshooting

### Common Issues

**Issue: "Container name already exists"**
```bash
# Solution: Check for existing containers
docker ps -a --filter name=boundlexx

# Remove conflicting containers
docker rm -f container-name-here
```

**Issue: "Port already in use"**
```bash
# Solution: Check what's using the port
netstat -an | findstr 28000

# Or use different folder names for different environments
```

**Issue: "Permission denied" on Windows**
```bash
# Solution: Ensure Docker Desktop is running and has proper permissions
# Check Windows volume sharing settings in Docker Desktop
```

**Issue: "No such file docker-compose.yml"**
```bash
# Solution: Ensure you're in the project root directory
ls docker-compose.yml  # Should exist
```

### Script Debugging

All scripts support `--dry-run` for safe testing:

```bash
# Preview what would happen without making changes
python setup_development_container_improved.py --dry-run
python setup_test_container.py --dry-run
```

### Container Network Architecture

Each environment creates its own Docker network:

```bash
# Main development
boundlexx-yatesjj-network

# Test environments
boundlexx-test-1-network
boundlexx-test-pr3-network
```

This provides complete network isolation between environments while allowing all services within each environment to communicate internally.
