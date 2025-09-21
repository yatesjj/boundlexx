# Complete Installation Guide

Comprehensive setup instructions for all development scenarios.

## 🎯 Choose Your Setup Method

### 1. Quick Containerized Setup (Recommended)
**Best for**: New developers, CI/CD, consistent environments
**Time**: 5-10 minutes
**See**: [Quick Start Guide](quick-start.md)

### 2. Complete Containerized Setup
**Best for**: Full development, production-like testing
**Time**: 15-30 minutes
**Details**: This guide

### 3. Hybrid Local Setup
**Best for**: Advanced developers, custom tooling
**Time**: 30-60 minutes
**See**: [Hybrid Setup Section](#hybrid-local-setup)

## 🐳 Complete Containerized Setup

### Prerequisites
- **Docker Engine & Compose** v20.10+ with BuildKit enabled
- **VS Code** with Remote Containers extension
- **Git** for version control
- **8GB+ RAM** recommended for full stack

### Step 1: Clone and Environment Setup
```bash
# Clone your fork
git clone https://github.com/yatesjj/boundlexx.git
cd boundlexx

# Create local environment files
cp .env .local.env
cp docker-compose.override.example.yml docker-compose.override.yml
```

### Step 2: Container Configuration
```bash
# Run container setup script
python setup_containers.py --env dev

# For test environment
python setup_containers.py --env test

# For production
python setup_containers.py --env production
```

**Container Naming Results:**
- **Dev**: `boundlexx-django-dev`, `boundlexx-postgres-dev`, `boundlexx-redis-dev`
- **Test**: `boundlexx-django-test`, `boundlexx-postgres-test`, `boundlexx-redis-test`
- **Production**: `boundlexx-django`, `boundlexx-postgres`, `boundlexx-redis`

### Step 3: Environment Customization

Edit `.local.env` for your specific setup:

```bash
# Database settings (usually defaults are fine)
POSTGRES_DB=boundlexx
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password

# Django settings
DEBUG=True
DJANGO_SECRET_KEY=your_secret_key_here
DJANGO_PORT=28001  # Dev: 28001, Test: 28002, Production: 28000

# Steam authentication (for production data)
STEAM_USERNAMES=your_steam_username
STEAM_PASSWORDS=your_steam_password

# Boundless authentication (for live Discovery Server)
BOUNDLESS_USERNAMES=your_boundless_username
BOUNDLESS_PASSWORDS=your_boundless_password
BOUNDLESS_DS_REQUIRES_AUTH=True  # For live server

# Local paths (if needed)
BOUNDLESS_LOCATION=/path/to/boundless/install
BOUNDLESS_ICONS_LOCATION=/path/to/boundless/icons
```

### Step 4: Start Services
```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# Expected output:
# boundlexx-django-dev    Up    0.0.0.0:28001->8000/tcp
# boundlexx-postgres-dev  Up    5432/tcp
# boundlexx-redis-dev     Up    6379/tcp
```

### Step 5: Database Setup
```bash
# Apply migrations
docker-compose run --rm manage python manage.py migrate

# Create superuser (optional)
docker-compose run --rm manage python manage.py createsuperuser
```

### Step 6: Game Data Ingestion

**Fast Setup (English Only - Recommended for Development):**
```bash
# Use VS Code Task: "Boundlexx: Fast Complete Setup"
# Or manually:
docker-compose run --rm manage python manage.py ingest_game_data 249.4.0
docker-compose run --rm manage python manage.py create_game_objects --core --english-only
docker-compose run --rm manage python manage.py create_game_objects --skill
docker-compose run --rm manage python manage.py create_game_objects --recipe
```

**Complete Setup (All Languages):**
```bash
# Use VS Code Task: "Boundlexx: Complete Setup"
# Or manually:
docker-compose run --rm manage python manage.py ingest_game_data 249.4.0
docker-compose run --rm manage python manage.py create_game_objects --core
docker-compose run --rm manage python manage.py create_game_objects --skill
docker-compose run --rm manage python manage.py create_game_objects --recipe
```

### Step 7: Verification
- **API**: http://127.0.0.1:28001/api/v1/
- **Admin**: http://127.0.0.1:28001/admin/
- **API Docs**: http://127.0.0.1:28001/api/v1/schema/redoc/
- **OpenAPI Schema**: http://127.0.0.1:28001/api/v1/schema/

## 🔧 Hybrid Local Setup

### Prerequisites
- **Python 3.12** (exact version required)
- **PostgreSQL 15+**
- **Redis 7+**
- **Git**

### Step 1: Python Environment
```bash
# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements/dev.txt
```

### Step 2: Database Setup
```bash
# PostgreSQL (Ubuntu/Debian)
sudo apt install postgresql postgresql-contrib
sudo -u postgres createdb boundlexx
sudo -u postgres createuser -s boundlexx

# PostgreSQL (macOS with Homebrew)
brew install postgresql
brew services start postgresql
createdb boundlexx
```

### Step 3: Redis Setup
```bash
# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis

# macOS with Homebrew
brew install redis
brew services start redis
```

### Step 4: Environment Configuration
```bash
# Copy and edit environment file
cp .env .local.env

# Edit for local setup
DATABASE_URL=postgres://boundlexx:password@localhost/boundlexx
REDIS_URL=redis://localhost:6379/0
DEBUG=True
```

### Step 5: Django Setup
```bash
# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver 0.0.0.0:28001
```

## 🌐 Production Setup

### Prerequisites
- **Docker Swarm or Kubernetes**
- **Load balancer** (nginx, traefik)
- **SSL certificates**
- **Monitoring** (prometheus, grafana)

### Production Environment
```bash
# Production container setup
python setup_containers.py --env production

# Production environment variables
DJANGO_SETTINGS_MODULE=config.settings.production
DEBUG=False
DJANGO_SECRET_KEY=production_secret_key
DATABASE_URL=postgres://user:pass@prod-db:5432/boundlexx
REDIS_URL=redis://prod-redis:6379/0
```

### Production Deployment
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start production stack
docker-compose -f docker-compose.prod.yml up -d

# Apply migrations
docker-compose -f docker-compose.prod.yml run --rm manage python manage.py migrate

# Collect static files
docker-compose -f docker-compose.prod.yml run --rm manage python manage.py collectstatic --noinput
```

## 🔄 Multiple Environment Setup

### Development + Test Environment
```bash
# Main development
git clone https://github.com/yatesjj/boundlexx.git boundlexx-dev
cd boundlexx-dev
python setup_containers.py --env dev

# Test environment
git clone https://github.com/yatesjj/boundlexx.git boundlexx-test
cd boundlexx-test
python setup_containers.py --env test
```

### Environment Isolation
- **Ports**: Dev (28001), Test (28002), Production (28000)
- **Containers**: Environment-specific naming prevents conflicts
- **Data**: Separate databases and Redis instances
- **Networks**: Isolated Docker networks per environment

## 🛠️ Development Tools Setup

### VS Code Integration
1. **Install Extensions**:
   - Remote - Containers
   - Python
   - Django
   - Docker

2. **Open in Container**:
   - `Ctrl+Shift+P` → "Remote-Containers: Reopen in Container"
   - Or use the green remote icon in bottom-left

### Git Configuration
```bash
# Configure remotes
git remote set-url origin https://github.com/yatesjj/boundlexx.git
git remote add upstream https://github.com/AngellusMortis/boundlexx.git

# Sync with upstream
git fetch upstream
git checkout master
git merge upstream/master
git push origin master
```

## 🐛 Troubleshooting Installation

### Container Issues
```bash
# Reset containers
docker-compose down -v
docker system prune -f

# Rebuild containers
docker-compose build --no-cache
docker-compose up -d
```

### Database Issues
```bash
# Reset database
docker-compose down
docker volume rm boundlexx_postgres_data  # Adjust volume name
docker-compose up -d
```

### Permission Issues
```bash
# Fix file permissions (Linux/macOS)
sudo chown -R $USER:$USER .
chmod +x docker/bin/*
```

### Network Issues
```bash
# Check port conflicts
netstat -tulpn | grep :28001

# Use different port in .local.env
DJANGO_PORT=28101
```

## 📊 Installation Verification

### Health Checks
```bash
# API endpoints
curl http://127.0.0.1:28001/api/v1/health/
curl http://127.0.0.1:28001/api/v1/worlds/

# Database connectivity
docker-compose run --rm manage python manage.py dbshell --command="SELECT 1;"

# Redis connectivity
docker-compose run --rm manage python manage.py shell -c "
from django.core.cache import cache
cache.set('test', 'working')
print(cache.get('test'))
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
"
```

## 🔗 Next Steps

After successful installation:
1. **[Development Workflows](../workflows/development.md)** - Daily development tasks
2. **[Data Ingestion](../workflows/data-ingestion.md)** - Complete game data workflows
3. **[Architecture Overview](../architecture/overview.md)** - Understand the system
4. **[API Documentation](../reference/api.md)** - Start using the APIs
