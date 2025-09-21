# Quick Start Guide

Get Boundlexx running in 5 minutes using the containerized approach.

## Prerequisites

- Docker Engine and Compose
- VS Code with Remote Containers extension
- Git

## 1. Clone and Setup

```bash
# Clone your fork
git clone https://github.com/yatesjj/boundlexx.git
cd boundlexx

# Create local environment files
cp .env .local.env
cp docker-compose.override.example.yml docker-compose.override.yml
```

## 2. Container Setup

```bash
# Setup development environment
python setup_containers.py --env dev

# Verify configuration
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}"
```

Expected output: `boundlexx-django-dev`, `boundlexx-postgres-dev` containers.

## 3. Start Services

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps
```

## 4. Database Setup

Use VS Code Task: "Boundlexx: Migrate Database" or:

```bash
# Apply migrations
docker-compose run --rm manage python manage.py migrate

# Create admin user (optional)
docker-compose run --rm manage python manage.py createsuperuser
```

## 5. Ingest Game Data (Fast Setup)

Use VS Code Task: "Boundlexx: Fast Complete Setup" or:

```bash
# Fast English-only setup (recommended for development)
docker-compose run --rm manage python manage.py ingest_game_data 249.4.0
docker-compose run --rm manage python manage.py create_game_objects --core --english-only
docker-compose run --rm manage python manage.py create_game_objects --skill
docker-compose run --rm manage python manage.py create_game_objects --recipe
```

## 6. Verify Installation

- **API**: http://127.0.0.1:28001/api/v1/
- **Admin**: http://127.0.0.1:28001/admin/
- **Docs**: http://127.0.0.1:28001/api/v1/schema/redoc/

## 🎉 Success!

You now have a fully functional Boundlexx development environment.

## Next Steps

- [Complete Installation Guide](installation.md) - For detailed setup options
- [Development Workflows](../workflows/development.md) - Daily development tasks
- [Data Ingestion](../workflows/data-ingestion.md) - Complete game data import

## Troubleshooting

- **Container Issues**: [Environment Setup Guide](environment-setup.md)
- **Migration Errors**: Run `docker-compose run --rm manage python manage.py makemigrations` first
- **Port Conflicts**: Edit `.local.env` to change `DJANGO_PORT`
