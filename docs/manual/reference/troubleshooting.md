# Common Issues & Troubleshooting

Comprehensive troubleshooting guide for Boundlexx development and deployment.

## 🚨 Quick Fixes for Common Issues

### Container Startup Issues

#### "Port already in use" Error
**Error**: `bind: address already in use`
**Cause**: Another service using the same port
**Solution**:
```bash
# Check what's using the port
netstat -tulpn | grep :28001
# Or on macOS
lsof -i :28001

# Option 1: Stop conflicting service
sudo systemctl stop service_name

# Option 2: Change port in .local.env
DJANGO_PORT=28101
```

#### "Container name already exists"
**Error**: `container name "boundlexx-django-dev" already in use`
**Cause**: Previous containers not cleaned up
**Solution**:
```bash
# Stop and remove existing containers
docker-compose down
docker container rm boundlexx-django-dev boundlexx-postgres-dev boundlexx-redis-dev

# Or force remove all
docker container prune -f
```

### Database Issues

#### "No such table" Errors
**Error**: `relation "boundless_world" does not exist`
**Cause**: Migrations not applied
**Solution**:
```bash
# Apply migrations
docker-compose run --rm manage python manage.py migrate

# If migrations are missing
docker-compose run --rm manage python manage.py makemigrations
docker-compose run --rm manage python manage.py migrate
```

#### Database Connection Refused
**Error**: `could not connect to server: Connection refused`
**Cause**: PostgreSQL container not ready
**Solution**:
```bash
# Check container status
docker-compose ps

# Wait for PostgreSQL to be ready
docker-compose logs postgres

# Restart if needed
docker-compose restart postgres
```

### Game Data Ingestion Issues

#### "KeyError during ingestion"
**Error**: `KeyError: 'some_game_property'`
**Cause**: Game data format changed or incomplete download
**Solution**:
```bash
# Clear cache and re-ingest
docker-compose run --rm manage python manage.py shell -c "
from django.core.cache import cache
cache.clear()
"

# Re-run ingestion
docker-compose run --rm manage python manage.py ingest_game_data 249.4.0
```

#### "Skill.DoesNotExist" Error
**Error**: `Skill matching query does not exist`
**Cause**: Skills not imported before recipes
**Solution**:
```bash
# Import skills first
docker-compose run --rm manage python manage.py create_game_objects --skill

# Then import recipes
docker-compose run --rm manage python manage.py create_game_objects --recipe
```

## 🔧 Steam Authentication Issues

### Steam Login Problems

#### "Invalid password" for Steam
**Cause**: 2FA token expired or incorrect credentials
**Solution**:
```bash
# Clear Steam sessions
docker-compose run --rm manage python manage.py prompt_steam_guard --clear-session

# Re-authenticate
docker-compose run --rm manage python manage.py prompt_steam_guard
```

#### "Rate limited" Errors
**Cause**: Too many Steam API calls
**Solution**:
```bash
# Check authentication status
docker-compose run --rm manage python manage.py prompt_steam_guard --test-tickets

# Wait for rate limit to reset (usually 1-5 minutes)
# Or use different Steam account
```

### Boundless Discovery Server Issues

#### "Authentication failed" for Boundless
**Cause**: Invalid Boundless credentials or server issues
**Solution**:
```bash
# Test credentials
docker-compose run --rm manage python manage.py shell -c "
from boundlexx.boundless.game.client import BoundlessClient
client = BoundlessClient()
print('User:', client.user)
"

# Check Discovery Server status
curl https://ds.playboundless.com:8902/
```

## 🐳 Docker-Specific Issues

### Build Failures

#### "No space left on device"
**Cause**: Docker disk usage too high
**Solution**:
```bash
# Clean up Docker
docker system prune -a
docker volume prune

# Check disk usage
docker system df
```

#### "Failed to solve with frontend dockerfile.v0"
**Cause**: BuildKit issues or syntax errors
**Solution**:
```bash
# Disable BuildKit temporarily
export DOCKER_BUILDKIT=0
docker-compose build

# Or check Dockerfile syntax
docker-compose config
```

### Performance Issues

#### Slow Container Startup
**Cause**: Resource constraints or image size
**Solution**:
```bash
# Increase Docker memory/CPU in Docker Desktop settings
# Or use development image instead of full build

# Check resource usage
docker stats
```

#### Slow Database Queries
**Cause**: Missing indexes or large dataset
**Solution**:
```bash
# Check slow queries
docker-compose exec postgres psql -U postgres -d boundlexx -c "
SELECT query, mean_time, calls
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;"

# Add database indexes if needed
```

## 🔍 Development Environment Issues

### VS Code Issues

#### "Cannot connect to container"
**Cause**: Container not running or VS Code extension issues
**Solution**:
```bash
# Ensure container is running
docker-compose ps

# Restart VS Code
# Reload window: Ctrl+Shift+P → "Developer: Reload Window"

# Rebuild container
# Ctrl+Shift+P → "Remote-Containers: Rebuild Container"
```

#### "Python interpreter not found"
**Cause**: VS Code not using container Python
**Solution**:
```bash
# In VS Code:
# Ctrl+Shift+P → "Python: Select Interpreter"
# Choose: /usr/local/bin/python (container path)
```

### Task Execution Issues

#### "Task not found" in VS Code
**Cause**: `.vscode/tasks.json` not loaded
**Solution**:
```bash
# Reload VS Code window
# Ctrl+Shift+P → "Developer: Reload Window"

# Or run task manually
docker-compose run --rm manage python manage.py <command>
```

#### "Permission denied" on Scripts
**Cause**: Execute permissions not set
**Solution**:
```bash
# Fix permissions
chmod +x docker/bin/*
chmod +x *.py
```

## 🌐 Network and Connectivity Issues

### API Access Problems

#### "Connection refused" to API
**Cause**: Django not running or wrong port
**Solution**:
```bash
# Check Django is running
docker-compose logs django

# Check port mapping
docker-compose ps

# Test connectivity
curl http://127.0.0.1:28001/api/v1/health/
```

#### "CORS errors" in Browser
**Cause**: Cross-origin request issues
**Solution**:
```bash
# Check CORS settings in config/settings/local.py
CORS_ALLOW_ALL_ORIGINS = True  # For development only

# Or add specific origin
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### External Service Issues

#### "SSL certificate verify failed"
**Cause**: Corporate firewall or proxy
**Solution**:
```bash
# For development only - disable SSL verification
export PYTHONHTTPSVERIFY=0

# Or configure corporate certificates
# Add certificates to container in Dockerfile
```

## 📊 Performance Troubleshooting

### Memory Issues

#### "Out of memory" Errors
**Cause**: Insufficient Docker memory allocation
**Solution**:
```bash
# Increase Docker memory limit (Docker Desktop)
# Or use swap file

# Monitor memory usage
docker stats
free -h
```

#### Memory Leaks
**Cause**: Circular references or cache buildup
**Solution**:
```bash
# Clear Django cache
docker-compose run --rm manage python manage.py shell -c "
from django.core.cache import cache
cache.clear()
"

# Restart services
docker-compose restart
```

### Database Performance

#### Slow Queries
**Cause**: Missing indexes or inefficient queries
**Solution**:
```bash
# Enable query logging
# Add to config/settings/local.py:
LOGGING = {
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}

# Check slow queries
docker-compose logs django | grep "SELECT"
```

## 🛠️ Diagnostic Commands

### System Health Check
```bash
# Overall system status
docker-compose ps
docker-compose logs --tail=10

# Django health
curl http://127.0.0.1:28001/api/v1/health/

# Database connectivity
docker-compose run --rm manage python manage.py dbshell --command="SELECT 1;"

# Redis connectivity
docker-compose run --rm manage python manage.py shell -c "
from django.core.cache import cache
cache.set('test', 'working')
print('Redis:', cache.get('test'))
"
```

### Data Validation
```bash
# Check ingested data
docker-compose run --rm manage python manage.py shell -c "
from boundlexx.boundless.models import *
print(f'Items: {Item.objects.count()}')
print(f'Skills: {Skill.objects.count()}')
print(f'Recipes: {Recipe.objects.count()}')
print(f'Worlds: {World.objects.count()}')
print(f'LocalizedStrings: {LocalizedString.objects.count()}')
"
```

### Performance Monitoring
```bash
# Resource usage
docker stats

# Disk usage
docker system df
df -h

# Network connectivity
ping -c 3 ds.playboundless.com
curl -I https://ds.playboundless.com:8902/
```

## 🆘 Emergency Procedures

### Complete Environment Reset
```bash
# Nuclear option - complete reset
docker-compose down -v
docker system prune -a -f
docker volume prune -f

# Remove all project files and re-clone
cd ..
rm -rf boundlexx
git clone https://github.com/yatesjj/boundlexx.git
cd boundlexx

# Start fresh setup
python setup_containers.py --env dev
docker-compose up -d
```

### Database Recovery
```bash
# Backup current database
docker-compose exec postgres pg_dump -U postgres boundlexx > backup.sql

# Reset database
docker-compose down
docker volume rm boundlexx_postgres_data
docker-compose up -d postgres

# Wait for PostgreSQL to start
sleep 10

# Restore from backup
docker-compose exec -T postgres psql -U postgres boundlexx < backup.sql
```

### Quick Development Reset
```bash
# Reset development environment while keeping data
docker-compose restart
docker-compose run --rm manage python manage.py migrate
docker-compose run --rm manage python manage.py collectstatic --noinput
```

## 📞 Getting Additional Help

### Log Collection
```bash
# Collect all relevant logs
mkdir debug-logs
docker-compose logs > debug-logs/docker-compose.log
docker logs $(docker ps -q) > debug-logs/all-containers.log
docker system df > debug-logs/disk-usage.txt
```

### System Information
```bash
# System specs
docker version
docker-compose version
uname -a
df -h
free -h
```

### Useful Resources
- **Django Debug Toolbar**: Available in development at any page with `?debug=1`
- **PostgreSQL logs**: `docker-compose logs postgres`
- **Redis monitoring**: `docker-compose exec redis redis-cli monitor`
- **Container shells**: `docker-compose exec django bash`

---

**If issues persist**: Create an issue with relevant logs and system information from the diagnostic commands above.
