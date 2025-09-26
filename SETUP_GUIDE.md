# Boundlexx Development Setup Guide

**Complete Validated Orientation, Setup, Testing, and Troubleshooting Guide**

*Last Updated: September 25, 2025*
*Game Version: 249.4.0 (Boundless Client 1.18.94.0)*

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Environment Setup](#environment-setup)
4. [Container Architecture](#container-architecture)
5. [Initial Setup Process](#initial-setup-process)
6. [Data Ingestion Pipeline](#data-ingestion-pipeline)
7. [Troubleshooting & Known Issues](#troubleshooting--known-issues)
8. [Validation & Testing](#validation--testing)
9. [Development Workflow](#development-workflow)

## Overview

Boundlexx is a Django-based API for Boundless game data, utilizing a multi-container Docker architecture with PostgreSQL, Redis, and Celery workers. This guide provides a complete walkthrough based on real-world testing and issue resolution.

### What You'll Have After Setup
- **API Server**: Running at http://localhost:28000
- **Database**: PostgreSQL with complete game data (4,209+ files)
- **Cache Layer**: Redis for API performance
- **Background Jobs**: Celery workers for data processing
- **Game Objects**: 1,192+ items, 836+ recipes, 76+ skills, 1,391+ emojis
- **Blocks & Liquids**: 1,487 blocks, 5 liquids for world data

## Prerequisites

### Required Software
- **Docker Desktop**: Latest version with Docker Compose
- **Python 3.12+**: For container management scripts
- **Git**: For version control
- **PowerShell/Terminal**: Windows PowerShell or equivalent

### System Requirements
- **RAM**: 8GB+ recommended (containers can be memory-intensive)
- **Storage**: 10GB+ free space for game data and images
- **Network**: Internet connection for image downloads and dependencies

## Environment Setup

### 1. Create Virtual Environment (Recommended)

```powershell
# Navigate to project root
cd c:\VSCode\boundlexx-yatesjj\dev-boundlexx-2\boundlexx

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Verify activation (should show .venv path)
python -c "import sys; print(sys.executable)"
```

### 2. Verify Container Management Scripts

```powershell
# Check container status
python container_status.py

# Setup containers if needed
python setup_containers.py
```

## Container Architecture

### Service Overview
```yaml
services:
  django:      # Main API server (port 28000)
  postgres:    # Database server
  redis:       # Cache and message broker
  celery:      # Background task worker
  celerybeat:  # Task scheduler
  huey-consumer: # Alternative task queue
  huey-scheduler: # Huey task scheduler
```

### Volume Mounts
- `/boundless`: Game data files (read-only)
- `/boundless-icons`: Generated icon images
- `postgres_data`: Database persistence
- `redis_data`: Cache persistence

### Key Configuration Files
- `docker-compose.yml`: Base service definitions
- `docker-compose.override.yml`: Development overrides
- `.local.env`: Environment variables

## Initial Setup Process

### Phase 0: Configuration Files Setup

Before starting containers, ensure your local configuration files are properly set up:

```powershell
# 1. Create .local.env if it doesn't exist
if (!(Test-Path ".local.env")) {
    Copy-Item ".env" ".local.env"
    Write-Host "Created .local.env from template"
}

# 2. Create docker-compose.override.yml if it doesn't exist  
if (!(Test-Path "docker-compose.override.yml")) {
    Copy-Item "docker-compose.override.example.yml" "docker-compose.override.yml"
    Write-Host "Created docker-compose.override.yml from template"
}
```

**Critical Configuration Steps:**

1. **Edit `docker-compose.override.yml`**:
   ```yaml
   # Update the Boundless game data path (REQUIRED)
   volumes:
     - "C:/Path/To/Your/Boundless/Install:/boundless:ro"
     - "C:/Path/To/Boundless/Icons:/boundless-icons:ro"
   ```

2. **Edit `.local.env`** (if needed):
   ```bash
   # Most defaults are fine, but you can customize:
   DJANGO_DEBUG=True
   DJANGO_SECRET_KEY=your-development-key-here
   # Database and Redis URLs are typically fine as defaults
   ```

3. **Verify Paths**:
   ```powershell
   # Ensure your Boundless paths exist and contain game data
   Test-Path "C:/Path/To/Your/Boundless/Install"  # Should be True
   Get-ChildItem "C:/Path/To/Your/Boundless/Install" | Select-Object -First 5
   ```

**Alternative: Use Container Setup Script**:
```powershell
# This script handles the file creation and configuration
python setup_containers.py --env dev
```

### Phase 1: Container Startup

```powershell
# Start all services
docker-compose up -d

# Verify all services are running
docker-compose ps

# Check logs for issues
docker-compose logs --tail=50
```

**Expected Output**: All services should show "Up" status

### Phase 2: Database Setup

```powershell
# Apply database migrations
docker-compose exec django python manage.py migrate

# Create superuser (optional)
docker-compose exec django python manage.py createsuperuser
```

### Phase 3: Game Data Ingestion

```powershell
# Ingest raw game data (4,209 files)
docker-compose exec django python manage.py ingest_game_data 249.4.0

# Verify ingestion
docker-compose exec django python manage.py shell -c "from boundlexx.ingest.models import GameFile; print(f'Game files: {GameFile.objects.count()}')"
```

**Expected Output**: ~4,209 game files imported

## Data Ingestion Pipeline

### Complete Setup Sequence

```powershell
# 1. Core game objects (items, metals, colors, localization)
docker-compose exec django python manage.py create_game_objects --core

# 2. Process items and create blocks/liquids (CRITICAL STEP)
docker-compose exec django python manage.py create_game_objects --item

# 3. Create skill tree
docker-compose exec django python manage.py create_game_objects --skill

# 4. Create crafting recipes
docker-compose exec django python manage.py create_game_objects --recipe

# 5. Create emoji data
docker-compose exec django python manage.py create_game_objects --emoji

# 6. Create color data
docker-compose exec django python manage.py create_game_objects --color

# 7. Resources (world-specific resource distribution)
docker-compose exec django python manage.py create_game_objects --resources
```

### Fast Setup Alternative

```powershell
# English-only setup (faster)
docker-compose exec django python manage.py create_game_objects --core --english-only
docker-compose exec django python manage.py create_game_objects --item
docker-compose exec django python manage.py create_game_objects --skill
docker-compose exec django python manage.py create_game_objects --recipe
docker-compose exec django python manage.py create_game_objects --emoji
```

### Available Task Shortcuts

The project includes pre-configured VS Code tasks:
- **"Boundlexx: Fast Complete Setup"**: Full English-only setup
- **"Boundlexx: Complete Setup"**: Full all-languages setup
- **"Boundlexx: Add Remaining Languages"**: Add non-English after fast setup

## Troubleshooting & Known Issues

### Issue 1: Resources Import Failure (SOLVED ✅)

**Problem**: `create_game_objects --resources` fails with `KeyError: 0`

**Root Cause**: Game version 249.4.0 changed `resourcetiers.json` format from array to flat dictionary

**Solution**: Implemented backward-compatible format detection in `resources.py`:
- Detects both old array format and new flat dictionary format
- Graceful fallback for missing fields (bestType/bestWorld)
- Maintains compatibility with all game versions

**Status**: Fixed and validated - resources import now works correctly

**Impact**: All resource distribution data now available (56 resources imported)

### Issue 2: Missing Blocks/Liquids (SOLVED ✅)

**Problem**: Resources failed with "Liquid.DoesNotExist" error

**Root Cause**: `--core` flag doesn't create Block/Liquid objects

**Solution**: Must run `--item` flag which creates:
- 1,487 Block objects
- 5 Liquid objects (including Petrolim/Resin needed for resources)

**Critical Learning**: The `--item` step is REQUIRED even after `--core`

### Issue 3: Container Memory Issues

**Problem**: Containers exit with out-of-memory errors

**Solution**: 
```powershell
# Increase Docker Desktop memory allocation
# Settings → Resources → Memory → 8GB+

# Monitor memory usage
docker stats
```

### Issue 4: Permission Errors on Windows

**Problem**: Volume mount permission issues

**Solution**:
```powershell
# Ensure Docker has access to drive
# Docker Desktop → Settings → Resources → File Sharing

# Fix .local.env permissions if needed
icacls .local.env /grant Everyone:F
```

## Validation & Testing

### API Health Check

```powershell
# Test API endpoint
curl http://localhost:28000/api/v2/

# Check database objects
docker-compose exec django python manage.py shell -c "
from boundlexx.boundless.models import Item, Recipe, Skill, Color, Block, Liquid;
print(f'Items: {Item.objects.count()}');
print(f'Recipes: {Recipe.objects.count()}');
print(f'Skills: {Skill.objects.count()}');
print(f'Colors: {Color.objects.count()}');
print(f'Blocks: {Block.objects.count()}');
print(f'Liquids: {Liquid.objects.count()}')
"
```

**Expected Output** (Game Version 249.4.0):
- Items: 1,192
- Recipes: 836  
- Skills: 76
- Colors: 255
- Blocks: 1,487
- Liquids: 5

### Service Health Check

```powershell
# Check all services
docker-compose exec django python manage.py check

# Test Celery worker
docker-compose exec django python manage.py shell -c "
from celery import current_app;
print('Celery workers:', current_app.control.active())
"

# Test Redis connection
docker-compose exec django python manage.py shell -c "
from django.core.cache import cache;
cache.set('test', 'working');
print('Redis test:', cache.get('test'))
"
```

## Development Workflow

### Daily Startup

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Start containers
docker-compose up -d

# Check status
python container_status.py
```

### Making Changes

```powershell
# Database migrations
docker-compose exec django python manage.py makemigrations
docker-compose exec django python manage.py migrate

# Restart specific service
docker-compose restart django

# View logs
docker-compose logs -f django
```

### Shutdown

```powershell
# Stop containers (preserves data)
docker-compose down

# Complete cleanup (removes data)
docker-compose down -v
```

## Performance Optimization

### Recommended Settings

```yaml
# docker-compose.override.yml additions
services:
  django:
    environment:
      - DJANGO_DEBUG=False  # Production mode
      - CELERY_TASK_ALWAYS_EAGER=False  # Async tasks
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
```

### Monitoring

```powershell
# Container resource usage
docker stats

# Database performance
docker-compose exec postgres psql -U boundlexx -c "
SELECT schemaname,tablename,attname,n_distinct,correlation 
FROM pg_stats WHERE tablename='boundless_item' LIMIT 10;
"
```

## Next Steps

1. **Live Data**: Configure real-time world data updates
2. **API Documentation**: Generate OpenAPI specs  
3. **Performance**: Implement caching strategies
4. **Monitoring**: Add application metrics
5. **Testing**: Expand automated test coverage

## Appendix

### Useful Commands

```powershell
# Django management
docker-compose exec django python manage.py <command>

# Database access
docker-compose exec postgres psql -U boundlexx

# Redis access  
docker-compose exec redis redis-cli

# Container logs
docker-compose logs -f <service_name>

# Clean restart
docker-compose down && docker-compose up -d
```

### File Structure

```
boundlexx/
├── docker-compose.yml           # Base services
├── docker-compose.override.yml  # Dev overrides
├── .local.env                   # Environment variables
├── container_status.py          # Status checker
├── setup_containers.py          # Setup helper
├── boundlexx/                   # Django app
│   ├── api/                     # API endpoints
│   ├── boundless/               # Game models
│   └── ingest/                  # Data ingestion
└── requirements/                # Python dependencies
```

### Environment Variables

```bash
# .local.env
DJANGO_SECRET_KEY=your-secret-key
DATABASE_URL=postgres://boundlexx:password@postgres:5432/boundlexx
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
```

---

*This guide is maintained based on real-world setup experiences. Please update as new issues are discovered and resolved.*