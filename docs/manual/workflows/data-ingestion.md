# Data Ingestion Workflows

Complete guide for importing Boundless game data into Boundlexx.

## 🎯 Quick Data Ingestion (Recommended)

**Use VS Code Task: "Boundlexx: Fast Complete Setup"**

This automated task runs the complete workflow with English-only data (80% faster than full setup).

### Manual Fast Setup
```bash
# 1. Ingest raw game data
docker-compose run --rm manage python manage.py ingest_game_data 249.4.0

# 2. Create core objects (English only for speed)
docker-compose run --rm manage python manage.py create_game_objects --core --english-only

# 3. Create skills (dependencies for recipes)
docker-compose run --rm manage python manage.py create_game_objects --skill

# 4. Create recipes (final step)
docker-compose run --rm manage python manage.py create_game_objects --recipe
```

## 🌍 Complete Data Ingestion (All Languages)

**Use VS Code Task: "Boundlexx: Complete Setup"**

### Manual Complete Setup
```bash
# 1. Ingest raw game data
docker-compose run --rm manage python manage.py ingest_game_data 249.4.0

# 2. Create core objects (all 5 languages)
docker-compose run --rm manage python manage.py create_game_objects --core

# 3. Create skills
docker-compose run --rm manage python manage.py create_game_objects --skill

# 4. Create recipes
docker-compose run --rm manage python manage.py create_game_objects --recipe
```

## 🚨 Critical Requirements

### Execution Order (MUST Follow)
1. **Core data FIRST** - Creates required LocalizedString objects
2. **Skills BEFORE recipes** - Recipes have foreign key dependencies on skills
3. **Never combine** `--skill --recipe` - Transaction visibility issues

### Performance Comparison
| Setup Type | LocalizedString Objects | Time | Use Case |
|------------|------------------------|------|----------|
| **English Only** | 2,190 objects | ~5 minutes | Development |
| **All Languages** | 10,964 objects | ~25 minutes | Production |

## 📋 Available VS Code Tasks

### Automated Workflows (Recommended)
- **"Boundlexx: Fast Complete Setup"** - English-only full automation
- **"Boundlexx: Complete Setup"** - All languages full automation
- **"Boundlexx: Create Game Objects"** - Core → Skills → Recipes (all languages)
- **"Boundlexx: Fast Create Game Objects"** - Core → Skills → Recipes (English only)

### Individual Steps
- **"Boundlexx: Ingest Game Data"** - Download and process raw game data
- **"Boundlexx: Create Game Objects (Core Data - English Only)"** - Fast core setup
- **"Boundlexx: Create Game Objects (Skills Only)"** - Import skills only
- **"Boundlexx: Create Game Objects (Recipes Only)"** - Import recipes only
- **"Boundlexx: Add Remaining Languages"** - Add languages after English-only setup

## 🔧 Manual Commands Reference

### Game Data Ingestion
```bash
# Ingest specific game version
python manage.py ingest_game_data <version>

# Example with current version
python manage.py ingest_game_data 249.4.0
```

### Object Creation
```bash
# Core objects
python manage.py create_game_objects --core [--english-only]

# Skills
python manage.py create_game_objects --skill

# Recipes
python manage.py create_game_objects --recipe

# Colors (if needed)
python manage.py create_game_objects --colors

# Multiple (NOT RECOMMENDED - use separate commands)
python manage.py create_game_objects --core --skill --recipe
```

## 🐛 Troubleshooting

### Common Issues

#### "KeyError during ingestion"
**Cause**: Game data import incomplete or failed
**Solution**: Re-run `python manage.py ingest_game_data 249.4.0`

#### "Skill.DoesNotExist error"
**Cause**: Skills not imported before recipes
**Solution**: Run `python manage.py create_game_objects --skill` first

#### "Carriage return warnings"
**Cause**: Windows line endings in `.local.env`
**Solution**: `sed -i 's/\r$//' .local.env`

#### "No LocalizedString objects"
**Cause**: Core data not imported
**Solution**: Run `python manage.py create_game_objects --core` first

### Validation Commands
```bash
# Check ingested data
python manage.py shell
>>> from boundlexx.boundless.models import *
>>> print(f"Items: {Item.objects.count()}")
>>> print(f"Skills: {Skill.objects.count()}")
>>> print(f"Recipes: {Recipe.objects.count()}")

# Check LocalizedStrings
>>> print(f"LocalizedStrings: {LocalizedString.objects.count()}")
```

## 📊 Data Processing Workflow

### 1. Raw Game Data (`ingest_game_data`)
- Downloads game assets from Boundless
- Processes JSON/binary game files
- Stores raw data in database tables
- Creates base game object references

### 2. Core Objects (`--core`)
- Creates LocalizedString objects for all text
- Processes items, blocks, colors
- Sets up base relationships
- **Required for all other processing**

### 3. Skills (`--skill`)
- Creates Skill objects and relationships
- Links to items and prerequisites
- **Required before recipes**

### 4. Recipes (`--recipe`)
- Creates Recipe objects
- Links ingredients and outputs
- Requires skills for foreign key relationships

## 🔄 Incremental Updates

### Adding Languages After English-Only Setup
```bash
# If you started with English-only, add remaining languages:
python manage.py create_game_objects --core
```

### Updating Game Data
```bash
# When new game version is released:
python manage.py ingest_game_data <new_version>
python manage.py create_game_objects --core
python manage.py create_game_objects --skill
python manage.py create_game_objects --recipe
```

## 🚀 Production Considerations

### Authentication Requirements
- **Steam Authentication**: Required for live Discovery Server
- **Multi-Account Setup**: Use multiple Steam/Boundless accounts for rate limiting
- **Session Management**: 21-day Steam sessions reduce 2FA prompts

### Performance Optimization
- **English-only for development**: 80% faster, sufficient for most development
- **Staged deployments**: Test with English-only, deploy with all languages
- **Database indexing**: Ensure proper indexes for large datasets

### Monitoring
```bash
# Check processing progress
docker-compose logs django | grep "Processing"

# Monitor database size
docker-compose exec postgres psql -U postgres -d boundlexx -c "
  SELECT schemaname,tablename,pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
  FROM pg_tables
  WHERE schemaname='public'
  ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;"
```

## 🔗 Related Documentation

- [Development Workflows](development.md) - Daily development tasks
- [Architecture Overview](../architecture/overview.md) - System design
- [Troubleshooting](../reference/troubleshooting.md) - Common issues
