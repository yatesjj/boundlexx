# Development Workflows

Daily development tasks and VS Code integration for Boundlexx.

## 🎯 VS Code Tasks (Recommended)

Access via Command Palette → "Tasks: Run Task"

### Core Development Tasks

| Task | Purpose | When to Use |
|------|---------|-------------|
| **Boundlexx: Manage** | Run any Django management command | Daily operations |
| **Boundlexx: Migrate Database** | Apply database migrations | After pulling changes |
| **Boundlexx: Make Migrations** | Create new migrations | After model changes |

### Data Management Tasks

| Task | Purpose | Performance |
|------|---------|-------------|
| **Boundlexx: Fast Complete Setup** | English-only full setup | 80% faster (recommended) |
| **Boundlexx: Complete Setup** | All languages setup | Complete but slower |
| **Boundlexx: Create Game Objects** | Core → Skills → Recipes | Full workflow |

### Testing & Quality

| Task | Purpose | Frequency |
|------|---------|-----------|
| **Boundlexx: Install Requirements** | Update dependencies | After requirements changes |
| **Boundlexx: Update Requirements** | Compile new requirements | When adding packages |

## 🔄 Daily Development Workflow

### 1. Start Your Day

```bash
# Pull latest changes
git pull upstream master

# Update dependencies if needed
# Use VS Code Task: "Boundlexx: Install Requirements"

# Apply any new migrations
# Use VS Code Task: "Boundlexx: Migrate Database"
```

### 2. Model Changes

```bash
# After changing models in boundlexx/boundless/models/
# Use VS Code Task: "Boundlexx: Make Migrations"
# Use VS Code Task: "Boundlexx: Migrate Database"
```

### 3. Testing Changes

```bash
# Run tests
docker-compose run test

# Check linting
docker-compose run lint

# Format code
docker-compose run format
```

### 4. Game Data Updates

```bash
# Fast development setup (English only)
# Use VS Code Task: "Boundlexx: Fast Complete Setup"

# Or manual workflow:
python manage.py ingest_game_data 249.4.0
python manage.py create_game_objects --core --english-only
python manage.py create_game_objects --skill
python manage.py create_game_objects --recipe
```

## 🐛 Debugging Workflows

### Django Shell

```bash
# Interactive Django shell
docker-compose run --rm manage python manage.py shell
```

### Log Analysis

```bash
# View Django logs
docker-compose logs django

# Follow logs in real-time
docker-compose logs -f django

# View specific service logs
docker-compose logs postgres
docker-compose logs redis
```

### Database Inspection

```bash
# Database shell
docker-compose run --rm manage python manage.py dbshell

# Or connect directly
docker-compose exec postgres psql -U postgres boundlexx
```

## 🔧 Performance Workflows

### Monitoring Tasks

```bash
# Check Celery status
docker-compose run --rm manage python manage.py celery inspect active

# View cache statistics
docker-compose run --rm manage python manage.py shell
>>> from django.core.cache import cache
>>> cache.get_stats()
```

### Rate Limiting Analysis

```bash
# Check Steam authentication status
docker-compose run --rm manage python manage.py prompt_steam_guard --test-tickets

# View API rate limiting logs
docker-compose logs django | grep "403 error"
```

## 🚀 Production Deployment Workflow

### Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Migrations applied and tested
- [ ] Static files collected
- [ ] Environment variables configured
- [ ] Backup database

### Deployment Steps

```bash
# Production environment setup
python setup_containers.py --env production

# Production migrations
docker-compose -f docker-compose.prod.yml run --rm manage python manage.py migrate

# Collect static files
docker-compose -f docker-compose.prod.yml run --rm manage python manage.py collectstatic --noinput

# Start production services
docker-compose -f docker-compose.prod.yml up -d
```

## 🔄 Background Task Workflows

### Celery Management

```bash
# Start Celery workers
docker-compose up celery celerybeat

# Monitor Celery tasks
docker-compose run --rm manage python manage.py celery monitor

# Restart workers (after code changes)
docker-compose restart celery
```

### Huey Management (Legacy)

```bash
# Start Huey consumers
docker-compose up huey-consumer huey-scheduler

# View Huey status
docker-compose logs huey-consumer
```

## 📊 Monitoring Workflows

### Health Checks

```bash
# Check all services
docker-compose ps

# Test API endpoints
curl http://127.0.0.1:28001/api/v1/worlds/
curl http://127.0.0.1:28001/api/v1/health/

# Check database connectivity
docker-compose run --rm manage python manage.py dbshell --command="SELECT 1;"
```

### Performance Monitoring

```bash
# View Django debug toolbar (development)
# Visit any page with ?debug=1

# Check memory usage
docker stats

# Monitor disk usage
docker system df
```

## 🆘 Emergency Procedures

### Quick Rollback

```bash
# Stop all services
docker-compose down

# Restore from backup
docker-compose run --rm postgres pg_restore -U postgres -d boundlexx /backup/latest.dump

# Restart services
docker-compose up -d
```

### Reset Development Environment

```bash
# Complete reset
docker-compose down -v
docker system prune -f
git clean -fdx
python setup_containers.py --env dev
docker-compose up -d
```

## 🔗 Related Documentation

- [Testing Workflows](testing.md) - Detailed testing procedures
- [Data Ingestion](data-ingestion.md) - Complete game data workflows
- [Troubleshooting](../reference/troubleshooting.md) - Common issues and solutions
