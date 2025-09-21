# Reference Guide

Comprehensive reference documentation for Boundlexx configuration, commands, and APIs.

## 📚 Reference Sections

### [🔧 Configuration Reference](configuration.md)
Complete guide to all configuration options, environment variables, and settings modules.

**Key Topics:**
- Environment variables (required and optional)
- Django settings by module (base, local, production, test)
- Docker and container configuration
- Security, performance, and feature flag settings
- Package dependencies and build configuration

### [📋 Django Management Commands](commands.md)
Complete reference for all Boundlexx management commands.

**Key Commands:**
- `ingest_game_data` - Download and process Boundless game data
- `create_game_objects` - Create Django models from game data
- `prompt_steam_guard` - Manage Steam authentication (21-day tickets)
- Standard Django commands (migrate, createsuperuser, etc.)
- Custom debugging and maintenance commands

### [🌐 API Reference](api.md)
Complete REST API documentation with examples and schemas.

**Key Resources:**
- Items, Colors, Skills, Recipes, Worlds
- Authentication (Token and Session)
- Advanced queries, filtering, and search
- Rate limiting and performance features
- WebSocket and webhook support

### [🚨 Troubleshooting Guide](troubleshooting.md)
Common issues and their solutions with diagnostic commands.

**Key Areas:**
- Container startup and networking issues
- Database connection and migration problems
- Game data ingestion errors
- Steam authentication and rate limiting
- Performance and memory issues
- Emergency recovery procedures

## 🔗 Quick Reference

### Essential Commands
```bash
# Development setup
python manage.py migrate
python manage.py ingest_game_data 249.4.0
python manage.py create_game_objects --core --english-only
python manage.py create_game_objects --skill
python manage.py create_game_objects --recipe

# Authentication
python manage.py prompt_steam_guard
python manage.py createsuperuser

# Diagnostics
python manage.py check
python manage.py health_check
```

### Essential Environment Variables
```bash
# Database
DATABASE_URL=postgresql://postgres:password@postgres:5432/boundlexx

# Security
SECRET_KEY=your-super-secret-key
DEBUG=True

# Authentication
STEAM_USERNAMES=user1,user2
STEAM_PASSWORDS=pass1,pass2
BOUNDLESS_USERNAMES=user1,user2
BOUNDLESS_PASSWORDS=pass1,pass2

# Containers
DJANGO_PORT=28001
```

### Essential API Endpoints
```bash
# Health check
GET /api/v2/health/

# Search items
GET /api/v2/items/?search=stone&tier=0

# Get world data
GET /api/v2/worlds/?active=true

# Authentication
POST /api/auth/token/
```

## 📖 Related Documentation

- **Setup**: [Installation Guide](../getting-started/installation.md)
- **Workflows**: [Development Guide](../workflows/development.md)
- **Architecture**: [System Overview](../architecture/index.md)
- **Migration**: [Modernization Roadmap](../migration/roadmap.md)
