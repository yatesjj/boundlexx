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
3. **Run appropriate setup script**:
   - **Main development**: `python setup_development_container_improved.py`
   - **Test environments**: `python setup_test_container.py` (adds port offsets)
4. **Customize local files** as needed

### Benefits of This Approach:
- ✅ **Complete isolation** between environments
- ✅ **No port conflicts** (automatic container prefixes + test offsets)
- ✅ **Git-friendly** (each folder can be on different branches)
- ✅ **Safe testing** (can't accidentally affect main development)
- ✅ **Easy cleanup** (just delete folder when done)
- ✅ **Clear separation** of concerns

This prevents container name conflicts and makes it easy to run multiple environments simultaneously.

## 🧪 Testing Container Management Changes

When making changes to container management scripts or Docker configuration, follow this testing workflow:

### Quick Testing Workflow

1. **Setup Test Environment:**
   ```bash
   # Clone to test location
   git clone https://github.com/yatesjj/boundlexx.git C:\VSCode\boundlexx-test-1\boundlexx
   cd C:\VSCode\boundlexx-test-1\boundlexx
   
   # Setup local files
   cp .env .local.env
   cp docker-compose.override.example.yml docker-compose.override.yml
   ```

2. **Test Container Scripts:**
   ```bash
   # Test with dry-run first
   python setup_test_container.py --dry-run
   
   # Apply changes (creates boundlexx-test-1-* containers with port offsets)
   python setup_test_container.py
   
   # Verify container setup
   python container_status.py
   ```

3. **Verify Isolation:**
   ```bash
   # Start test environment
   docker-compose up -d
   
   # Check containers (should see Django on port 28001, others internal)
   docker ps --format "table {{.Names}}\t{{.Ports}}"
   
   # Verify no conflicts with main development
   # (your main boundlexx-yatesjj-* containers should still be running)
   ```

4. **Test Functionality:**
   ```bash
   # Test database connection
   docker-compose run --rm manage dbshell
   
   # Test web application (should be on port 28001)
   curl http://127.0.0.1:28001
   ```

5. **Cleanup:**
   ```bash
   # Stop and remove test containers
   docker-compose down
   docker system prune -f
   
   # Remove test directory
   cd ..
   rm -rf C:\VSCode\boundlexx-test-1
   ```

### Environment Comparison

| Environment Type | Container Names | Ports | Script | Use Case |
|-----------------|----------------|-------|--------|----------|
| **Main Development** | `boundlexx-yatesjj-*` | Django: 28000, Others: internal | `setup_development_container_improved.py` | Daily development work |
| **Test Environment** | `boundlexx-test-1-*` | Django: 28001, Others: internal | `setup_test_container.py` | Testing changes, PR verification |
| **Experiment** | `boundlexx-experiment-*` | Django: 28000, Others: internal | `setup_development_container_improved.py` | Feature experiments |

### Benefits of Test Environment Approach:
- ✅ **Safe testing** - No risk to main development data
- ✅ **Port isolation** - Automatic port offsets prevent conflicts  
- ✅ **Quick setup** - Standardized testing workflow
- ✅ **Easy cleanup** - Complete environment removal in one command
- ✅ **Parallel development** - Run main and test environments simultaneously

## 📊 Container Management Scripts Reference

### Available Scripts

| Script | Purpose | Port Strategy | Container Names | Use Case |
|--------|---------|---------------|-----------------|----------|
| `setup_development_container_improved.py` | Main development | Django: 28000, Others: internal | `{folder}-django-1`, `{folder}-postgres-1` | Daily development |
| `setup_test_container.py` | Test environments | Django: 28001, Others: internal | `{folder}-django-1`, `{folder}-postgres-1` | PR testing, parallel dev |
| `container_status.py` | Status monitoring | N/A | N/A | Check current setup |

### Port Mapping Details

**Development Environment (Original Upstream Ports):**
- **Django:** `28000:8000` (external access)
- **PostgreSQL:** Internal only (`5432`)
- **Redis:** Internal only (`6379`) 
- **MailHog:** Internal only (`8025`)

**Test Environment (Default: Same as Dev, Optional Port Offsets):**
- **Django:** `28000:8000` (default, no offset) or `28001+:8000` (with --port-offset)
- **PostgreSQL:** Internal only (`5432`)
- **Redis:** Internal only (`6379`)
- **MailHog:** Internal only (`8025`)

### Folder-Based Automatic Naming

Both scripts automatically detect your current project folder name and use it as the container prefix:

```bash
C:\VSCode\boundlexx-yatesjj\boundlexx-yatesjj\     → boundlexx-yatesjj-django-1
C:\VSCode\boundlexx-yatesjj-test-2\boundlexx-yatesjj-test-2\    → boundlexx-yatesjj-test-2-django-1  
C:\VSCode\boundlexx-experiment\boundlexx-experiment\  → boundlexx-experiment-django-1
```

This ensures:
- ✅ **Unique container names** across all environments
- ✅ **Clear identification** of which environment containers belong to
- ✅ **No naming conflicts** when running multiple environments
- ✅ **Automatic network isolation** with prefixed network names

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
