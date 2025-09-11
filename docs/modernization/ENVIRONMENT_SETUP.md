# Developme**Local Files (Not Committed) 
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
```p

This document outlines the best practices for setting up a clean, customizable development environment.

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

### Step 3: Run Development Container Setup
```bash
# This will prefix all container names with your folder name
python setup_development_container_improved.py
```

### Step 4: Customize Your Local Environment
Edit `.local.env` and `docker-compose.override.yml` for your specific setup:
- Local file paths (Steam, boundless icons, etc.)
- Port preferences  
- Additional environment variables

## 🎯 What Each Script Does

### `setup_development_container_improved.py`
- Adds meaningful prefixes to container names (e.g., `boundlexx-yatesjj-django`)
- Keeps base files clean
- Works with your override files
- Supports `--dry-run` for testing

### `setup_test_container.py` 
- Creates test environments with port offsets
- Useful for parallel testing/PR environments

## 🔍 Verification

After setup, verify your containers are properly named:
```bash
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}"
```

Expected output:
```
NAMES                           IMAGE                PORTS
boundlexx-yatesjj-django-1      boundlexx_dev_django 8000/tcp
boundlexx-yatesjj-postgres-1    boundlexx_postgres   5432/tcp
boundlexx-yatesjj-redis-1       redis:5.0            6379/tcp
```

## ✅ Best Practices

1. **Never commit** `docker-compose.override.yml` or `.local.env`
2. **Always use** the setup scripts for consistent naming
3. **Keep base files clean** - put customizations in override files
4. **Use meaningful folder names** for automatic prefixing
5. **Document** any custom setup in your override files

## 🔄 Multi-Environment Workflow (Recommended)

For testing multiple branches/PRs, use **separate folders** for complete isolation:

```bash
# Create separate folders for each environment
C:\VSCode\boundlexx-yatesjj\boundlexx-yatesjj\     # Main development  
C:\VSCode\boundlexx-test-pr2\boundlexx\            # Test PR #2
C:\VSCode\boundlexx-experiment\boundlexx\          # Experimental branch

# Each gets its own prefixed containers automatically
boundlexx-yatesjj-*           # Main containers
boundlexx-test-pr2-*          # Test containers  
boundlexx-experiment-*        # Experiment containers
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
