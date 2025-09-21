# Django Management Commands

Complete reference for all Boundlexx Django management commands.

## 🎮 Game Data Commands

### `ingest_game_data`
Downloads and processes Boundless game data from the official source.

```bash
python manage.py ingest_game_data <version>
```

**Arguments:**
- `version` (required): Game version to ingest (e.g., `249.4.0`)

**Options:**
- `--force`: Force re-download even if data exists
- `--no-cache`: Skip cache validation

**Examples:**
```bash
# Basic ingestion
python manage.py ingest_game_data 249.4.0

# Force re-download
python manage.py ingest_game_data 249.4.0 --force

# Skip cache checks
python manage.py ingest_game_data 249.4.0 --no-cache
```

**Output:** Downloads game files to `data/` directory and prepares for object creation.

---

### `create_game_objects`
Creates Django model instances from ingested game data.

```bash
python manage.py create_game_objects [options]
```

**Primary Options:**
- `--core`: Create core game objects (items, blocks, colors, etc.)
- `--skill`: Create skill objects and skill groups
- `--recipe`: Create recipe objects and dependencies
- `--colors`: Process color group data

**Language Options:**
- `--english-only`: Process only English localizations (80% faster)
- `--all-languages`: Process all 5 supported languages (default)

**Utility Options:**
- `--force`: Recreate objects even if they exist
- `--dry-run`: Show what would be created without making changes
- `--verbose`: Detailed output during processing

**Examples:**
```bash
# Fast development setup (English only)
python manage.py create_game_objects --core --english-only
python manage.py create_game_objects --skill
python manage.py create_game_objects --recipe

# Full production setup (all languages)
python manage.py create_game_objects --core
python manage.py create_game_objects --skill
python manage.py create_game_objects --recipe

# Create specific object types
python manage.py create_game_objects --colors --verbose
```

**Critical Order:** Core → Skills → Recipes (recipes depend on skills)

**Performance:** English-only reduces LocalizedString objects from ~10,964 to ~2,190

---

## 🔐 Authentication Commands

### `prompt_steam_guard`
Manages Steam authentication for game data access.

```bash
python manage.py prompt_steam_guard [options]
```

**Options:**
- `--test-tickets`: Test existing authentication tickets
- `--clear-session`: Clear all cached Steam sessions
- `--username <user>`: Authenticate specific Steam user

**Examples:**
```bash
# Interactive authentication (21-day tickets)
python manage.py prompt_steam_guard

# Test current authentication status
python manage.py prompt_steam_guard --test-tickets

# Clear sessions and re-authenticate
python manage.py prompt_steam_guard --clear-session

# Authenticate specific user
python manage.py prompt_steam_guard --username mysteamuser
```

**Features:**
- **21-day encrypted app tickets**: Reduces 2FA prompts by 95%
- **Multi-account support**: Round-robin authentication
- **Session persistence**: Cached in `.steam/` directory
- **Graceful fallback**: 24-hour tickets if encrypted tickets fail

---

## 🗃️ Database Commands

### Standard Django Commands

#### `migrate`
Apply database migrations.

```bash
python manage.py migrate [app_label] [migration_name]
```

**Examples:**
```bash
# Apply all pending migrations
python manage.py migrate

# Apply migrations for specific app
python manage.py migrate boundless

# Migrate to specific migration
python manage.py migrate boundless 0001_initial

# Show migration status
python manage.py showmigrations
```

#### `makemigrations`
Create new database migrations.

```bash
python manage.py makemigrations [app_label]
```

**Examples:**
```bash
# Create migrations for all apps
python manage.py makemigrations

# Create migrations for specific app
python manage.py makemigrations api

# Create empty migration for data migration
python manage.py makemigrations --empty api

# Dry run to see what would be created
python manage.py makemigrations --dry-run
```

#### `dbshell`
Open database shell.

```bash
python manage.py dbshell
```

**Examples:**
```bash
# PostgreSQL shell
python manage.py dbshell

# Execute SQL command
python manage.py dbshell --command="SELECT COUNT(*) FROM boundless_item;"
```

---

## 👤 User Management Commands

### `createsuperuser`
Create Django admin superuser.

```bash
python manage.py createsuperuser
```

**Examples:**
```bash
# Interactive creation
python manage.py createsuperuser

# Non-interactive creation
python manage.py createsuperuser \
    --username admin \
    --email admin@example.com \
    --noinput
```

### `changepassword`
Change user password.

```bash
python manage.py changepassword <username>
```

---

## 🧹 Maintenance Commands

### `collectstatic`
Collect static files for production.

```bash
python manage.py collectstatic [options]
```

**Options:**
- `--noinput`: Don't prompt for confirmation
- `--clear`: Clear existing files before collecting
- `--dry-run`: Show what would be collected

**Examples:**
```bash
# Standard collection
python manage.py collectstatic --noinput

# Clear and recollect
python manage.py collectstatic --clear --noinput
```

### `shell`
Open Django shell with project context.

```bash
python manage.py shell [options]
```

**Options:**
- `-c <command>`: Execute command and exit
- `--interface <shell>`: Choose shell interface (ipython, bpython, python)

**Examples:**
```bash
# Interactive shell
python manage.py shell

# Execute one-liner
python manage.py shell -c "
from boundlexx.boundless.models import Item
print(f'Items: {Item.objects.count()}')
"

# Use IPython interface
python manage.py shell --interface ipython
```

### `flush`
Remove all data from database.

```bash
python manage.py flush
```

**⚠️ Warning:** This removes ALL data. Use with extreme caution.

---

## 🔍 Debugging Commands

### `check`
Check for common Django issues.

```bash
python manage.py check [options]
```

**Options:**
- `--list-tags`: Show available check tags
- `--tag <tag>`: Run specific checks only
- `--deploy`: Include deployment checks

**Examples:**
```bash
# Basic health check
python manage.py check

# Deployment readiness check
python manage.py check --deploy

# Security-specific checks
python manage.py check --tag security
```

### `validate_templates`
Check template syntax.

```bash
python manage.py validate_templates
```

### Custom Debug Commands

#### `show_environment`
Display current environment configuration.

```bash
python manage.py show_environment
```

**Output:** Key environment variables and Django settings

#### `health_check`
Comprehensive system health check.

```bash
python manage.py health_check
```

**Checks:**
- Database connectivity
- Redis connectivity
- Game data integrity
- External service availability

---

## 📊 Data Analysis Commands

### `stats`
Show database statistics.

```bash
python manage.py stats [options]
```

**Options:**
- `--detailed`: Show detailed breakdown
- `--export <file>`: Export to JSON/CSV

**Examples:**
```bash
# Basic statistics
python manage.py stats

# Detailed breakdown
python manage.py stats --detailed

# Export to file
python manage.py stats --export stats.json
```

### `validate_data`
Validate game data integrity.

```bash
python manage.py validate_data [options]
```

**Options:**
- `--fix`: Attempt to fix issues automatically
- `--verbose`: Detailed validation output

---

## 🔄 Background Task Commands

### Celery Commands

#### `celery_status`
Check Celery worker status.

```bash
python manage.py celery_status
```

#### `celery_purge`
Purge all Celery tasks.

```bash
python manage.py celery_purge
```

### Huey Commands (Legacy)

#### `run_huey`
Start Huey consumer.

```bash
python manage.py run_huey
```

**Options:**
- `--workers <n>`: Number of worker processes
- `--periodic`: Enable periodic task scheduler

---

## 🏃‍♂️ Quick Command Combinations

### Fresh Development Setup
```bash
# Complete fresh setup
python manage.py migrate
python manage.py ingest_game_data 249.4.0
python manage.py create_game_objects --core --english-only
python manage.py create_game_objects --skill
python manage.py create_game_objects --recipe
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### Production Deployment
```bash
# Production setup
python manage.py check --deploy
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py compress  # If using django-compressor
```

### Data Refresh
```bash
# Update game data
python manage.py ingest_game_data 249.4.0 --force
python manage.py create_game_objects --core --force
python manage.py create_game_objects --skill --force
python manage.py create_game_objects --recipe --force
```

### Troubleshooting
```bash
# Diagnostic commands
python manage.py check
python manage.py health_check
python manage.py stats --detailed
python manage.py validate_data
python manage.py prompt_steam_guard --test-tickets
```

---

## 📝 Command Development

### Creating Custom Commands
```python
# boundlexx/management/commands/my_command.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'My custom command description'

    def add_arguments(self, parser):
        parser.add_argument('--option', help='Option description')

    def handle(self, *args, **options):
        self.stdout.write('Command output')
```

### Testing Commands
```python
# tests/test_commands.py
from django.core.management import call_command
from django.test import TestCase

class CommandTestCase(TestCase):
    def test_my_command(self):
        call_command('my_command', '--option=value')
```

---

**Note**: All commands support `--help` for detailed usage information:
```bash
python manage.py <command> --help
```
