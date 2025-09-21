# Copilot Instructions for Boundlexx Modernization

## Game Data Ingestion Workflow (IMPORTANT)

### ✅ Automated VS Code Tasks (Recommended)
- **"Boundlexx: Complete Setup (Ingest + Core + Skills + Recipes - All Languages)"** - Complete automation: ingest game data → core data → skills → recipes (all 5 languages)
- **"Boundlexx: Fast Complete Setup (Ingest + Core + Skills + Recipes - English Only)"** - Fast development setup with English localizations only (80% faster)
- **"Boundlexx: Create Game Objects (Core + Skills + Recipes - All Languages)"** - Runs core → skills → recipes automatically in correct order (all languages)
- **"Boundlexx: Fast Create Game Objects (Core + Skills + Recipes - English Only)"** - Runs core → skills → recipes with English only for faster setup
- **"Boundlexx: Create Game Objects (Core Data - English Only)"** - Import core data with English only for faster setup
- **"Boundlexx: Add Remaining Languages"** - Add remaining localizations after English-only setup

# Copilot Instructions for Boundlexx Modernization

## Authentication & User Management
- To create an admin user, use the VS Code task "Boundlexx: Manage" and enter `createsuperuser` when prompted for the management command.
- Log in at http://127.0.0.1:28001/admin/ with the credentials you create.

## Starting the Django Development Server

- Before starting the server for the first time, you must apply all database migrations:

  ```sh
  python manage.py migrate
  ```

- **If you see "have changes that are not yet reflected in a migration":**
  ```sh
  python manage.py makemigrations
  python manage.py migrate
  ```
  This is normal in fresh environments and indicates model changes that need new migration files.

- Then start the Django development server inside the dev container:

  ```sh
  python manage.py runserver 0.0.0.0:28001
  ```

- This will make the site available at http://127.0.0.1:28001 on your host machine.
- For production or multi-service setups, use Docker Compose as described in the main documentation.

## Game Data Ingestion Workflow (IMPORTANT)

### ✅ Automated VS Code Tasks (Recommended)
- **"Boundlexx: Complete Setup (Ingest + Core + Skills + Recipes - All Languages)"** - Complete automation: ingest game data → core data → skills → recipes (all 5 languages)
- **"Boundlexx: Fast Complete Setup (Ingest + Core + Skills + Recipes - English Only)"** - Fast development setup with English localizations only (80% faster)
- **"Boundlexx: Create Game Objects (Core + Skills + Recipes - All Languages)"** - Runs core → skills → recipes automatically in correct order (all languages)
- **"Boundlexx: Fast Create Game Objects (Core + Skills + Recipes - English Only)"** - Runs core → skills → recipes with English only for faster setup
- **"Boundlexx: Create Game Objects (Core Data - English Only)"** - Import core data with English only for faster setup
- **"Boundlexx: Add Remaining Languages"** - Add remaining localizations after English-only setup

### 🚀 Fast Development Setup (Recommended)
For faster development iterations, use English-only setup which reduces database size by ~80% (2,190 vs 10,964 LocalizedString objects):

1. **English-only setup:** "Boundlexx: Fast Complete Setup (Ingest + Core + Skills + Recipes - English Only)"
2. **Add languages later:** "Boundlexx: Add Remaining Languages" when needed

### 🚨 Critical Requirements
1. **Core data MUST be imported before skills/recipes** - creates required LocalizedString objects
2. **Skills MUST be imported before recipes** - recipes have foreign key dependencies on skills
3. **Never use the legacy task** marked "DO NOT USE" - it's unreliable
4. **Use separate commands** - running `--skill --recipe` together doesn't work due to transaction visibility issues

### Manual Command Workflow
```sh
# Fast setup (English only - recommended for development)
python manage.py ingest_game_data 249.4.0
python manage.py create_game_objects --core --english-only
python manage.py create_game_objects --skill
python manage.py create_game_objects --recipe

# Add remaining languages later if needed
python manage.py create_game_objects --core

# Full setup (all 5 languages)
python manage.py ingest_game_data 249.4.0
python manage.py create_game_objects --core
python manage.py create_game_objects --skill
python manage.py create_game_objects --recipe
```

### Troubleshooting
- **KeyError during ingestion:** Ensure game data import completed successfully
- **`Skill.DoesNotExist` error:** Skills must be imported before recipes
- **Carriage return warnings:** Environment file has Windows line endings - run `sed -i 's/\r$//' .local.env`

### ✅ Recent Fixes & Improvements (September 2025)

#### Fixed: Duplicate --color Parameter Warning
**Issue**: Click framework warning about duplicate `--color` parameter in `create_game_objects` command.
**Root Cause**: Django management commands automatically provide `--color/--no-color` for output colorization, conflicting with our custom `--color` parameter for color group processing.
**Solution**: Renamed custom parameter from `--color` to `--colors` in the command definition.

```sh
# BEFORE (generated warnings):
python manage.py create_game_objects --color

# AFTER (clean execution):
python manage.py create_game_objects --colors  # For color group processing
# Django's built-in --color/--no-color still available for output colorization
```

**Impact**: Eliminates Click parameter conflict warnings, provides clearer parameter intent, maintains full backward compatibility.

#### Verified: Django 5.2 LTS + Container Setup
**Status**: Complete fresh environment setup successfully validated:
- ✅ Clean Docker container restart and rebuilds working
- ✅ Django 5.2.6 LTS running successfully with Python 3.12
- ✅ Issue #25 container naming (`boundlexx-django-dev`, `boundlexx-postgres-dev`) operational
- ✅ Database migrations, game data ingestion, and full application stack functional
- ✅ Admin interface accessible at http://127.0.0.1:28001/admin/
- ✅ All modernization infrastructure preserved and reproducible

#### Development Environment Reproducibility
**Validated**: Complete setup automation works reliably:
1. Clean container environment can be established from scratch
2. All game data ingestion (core → skills → recipes) functions correctly
3. Issue #25 container naming modernization is stable and persistent
4. openpyxl compatibility fixes are preserved and functional
5. English-only setup provides 80% faster development iterations (2,190 vs 10,964 LocalizedString objects)

#### ✅ Steam Authentication Implementation WORKING (September 2025)
**Status**: Production-ready Steam authentication with Python 3.12 compatibility
- **File**: `boundlexx/boundless/game/steam_auth_pure_python.py`
- **Dependencies**: `steam[client]==1.4.4` (properly compiled in requirements)
- **Integration**: BoundlessClient compatible via `get_steam_session_ticket_pure_python()`
- **Features**: 2FA support, credential persistence, proper error handling
- **Configuration**: Uses `.local.env` credentials (STEAM_USERNAMES, STEAM_PASSWORDS)

**Working Implementation Details:**
- **Method**: `client.get_app_ticket(324510)` for Boundless app authentication
- **Response**: Protobuf object with `.ticket` field containing session data
- **Output**: 356-character hex session ticket for API authentication
- **2FA**: Interactive Steam Guard support via `cli_login()`

**Normal Operation Flow (Automatic):**
```python
# Celery Background Tasks → BoundlessClient → Steam Authentication → Boundless Discovery Server

# 1. Scheduled tasks (discover_worlds, poll_*_worlds) create BoundlessClient()
# 2. Client rotates through multiple Steam accounts (round-robin)
# 3. Authentication chain triggers on first API call:
query_token = client.query_token  # Lazy loading triggers auth

# 4. Dual authentication to Boundless Discovery Server:
data = {
    "authToken": self._get_game_jwt(boundless_user, boundless_pass),        # Boundless JWT
    "steamTicket": self._get_steam_session_ticket(steam_user, steam_pass),  # Steam ticket
    "vcplatform": 1,
}

# 5. Query token cached for 12 hours, used for all subsequent API calls
```

**Steam Guard 2FA Setup (One-time):**
```bash
python manage.py prompt_steam_guard  # Interactive setup, stores sentry files in .steam/
```

**Production Requirements:**
- Multiple Steam accounts for load distribution
- Persistent `.steam/` directory for sentry files
- Environment variables: `STEAM_USERNAMES`, `STEAM_PASSWORDS`, `BOUNDLESS_USERNAMES`, `BOUNDLESS_PASSWORDS`
- Setting: `BOUNDLESS_DS_REQUIRES_AUTH=True`

**Testing Verified**: Full authentication chain working with real Steam credentials, automatic 2FA, and live world discovery tasks.

## Modernization & Migration Plan (2025) - FORWARD-LOOKING

### CRITICAL: Migration-Aware Development Policy
- **All code changes must consider forward migration compatibility** with the planned modernization stack
- **Django 5.2 LTS + Python 3.12** is the target foundation (LTS support until April 2028)
- **Modern stack targets**: TaskIQ (async tasks), Django Ninja (fast APIs), uv (dependency management), Ruff (linting)
- **Container-first approach**: All development and testing must use Docker containers to avoid host environment conflicts

### Policy Clarification
- The directory `docs/modernization/template_examples` is for research/reference only. No tracking or documentation of work for this build should occur there. All tracking must be in `MODERNIZATION_TRACKING.md` and related main docs.

### Current Status: Phase 3 - Django 5.2 LTS Core Upgrade & Container Modernization COMPLETED
**Phases 1 & 2 COMPLETED**: Python 3.12 infrastructure and database compatibility successfully implemented and committed (tag: post-database-upgrade)
**Container Modernization COMPLETED**: Clean single-prefix naming strategy with environment-specific prefixes and explicit container names implemented
**Dependency Optimization COMPLETED**: django-filter downgraded from 25.1 to 24.3 for DRF OpenAPI compatibility (LTS strategy until Django Ninja migration)

### Migration Sequence (Forward-Looking)
1. ✅ **Phase 1 & 2 COMPLETE**: Python 3.12 + Database Compatibility
2. ✅ **Phase 3 COMPLETE**: Django 5.2 LTS Core Upgrade + Container Modernization + Dependency Optimization - stable foundation established
3. 📋 **Phase 4**: uv + pyproject.toml migration (Issue #30) - leverages Django 5.2 async capabilities
4. 📋 **Phase 5**: Ruff + mypy setup (Issue #29) - enhanced by Django 5.2 type support
5. 📋 **Phase 6**: Remove Huey → Celery consolidation (Issue #27)
6. 📋 **Phase 7**: TaskIQ parallel setup + gradual migration (Issue #31) - benefits from Django 5.2 async
7. 📋 **Phase 8**: Django Ninja v3 API or v2 rebuild (Issue #32) - optimized for Django 5.2 performance
8. ✅ **Phase 9 COMPLETE**: Steam authentication WORKING + Python 3.12 compatibility RESOLVED
9. 📋 **Phase 10**: Project structure modernization (Issue #33) using ark-operator patterns as reference

### Repository Relationships:
- **yatesjj/boundlexx** (your fork) → sophisticated container setup with port management
- **AngellusMortis/boundlexx** (upstream) → minimal Docker setup, simple patterns
- **AngellusMortis/ark-operator** (modernization reference) → modern tooling patterns for Issue #33

### Forward Migration Compatibility Requirements
**When making ANY code changes, verify compatibility with:**
- ✅ **Django 5.2 LTS**: All model changes, admin customizations, URL patterns must be Django 5.2 compatible
- ✅ **TaskIQ async**: Background tasks should be designed for eventual TaskIQ migration
- ✅ **Django Ninja**: API endpoints should consider eventual DRF → Django Ninja migration
- ✅ **uv dependency management**: Requirements changes must work with future pyproject.toml structure
- ✅ **Ruff linting**: Code style should follow modern Python standards that Ruff enforces

### Dependency Version Strategy
- **Django**: `>=5.2,<5.3` (LTS until April 2028)
- **Python**: `3.12` (modern standard, excellent performance)
- **Celery**: `<6` (prepare for TaskIQ migration)
- **psycopg2-binary**: For reliable container builds
- **steam[client]**: `==1.4.4` (WORKING - Python 3.12 compatible, 2FA authentication functional)

## Container Management - COMPLETE ✅

### Container Naming Modernization:
- **Issue #25 COMPLETE**: All container images now use kebab-case naming (boundlexx-django, boundlexx-postgres)
- **Clean Single-Prefix Strategy**: Environment-specific prefixes with explicit container names
- **setup_containers.py**: Automated environment setup with clean naming patterns and port allocation

### Production-Ready Container Scripts:
- `setup_containers.py` - **Primary setup script** with automated environment-specific configuration generation
- **Three Environment Support**: Production (28000), Development (28001), Test (28002)
- **Clean Container Names**: `boundlexx-django-dev`, `boundlexx-postgres-test`, `boundlexx-redis`
- **Value Proposition**: Eliminates redundant naming and provides clean, predictable container names

### Container Setup:
1. **Copy template files:** `cp .env .local.env` and `cp docker-compose.override.example.yml docker-compose.override.yml`
2. **Development:** `python setup_containers.py --env dev` (creates boundlexx-*-dev containers on port 28001)
3. **Test environments:** `python setup_containers.py --env test` (creates boundlexx-*-test containers on port 28002)
4. **Production:** `python setup_containers.py --env production` (creates boundlexx-* containers on port 28000)
5. **All scripts support `--dry-run`** for safe preview before applying changes

### Modern Clean Naming Strategy

The container naming has been modernized to use clean environment-specific prefixes with explicit container names:

- **Production Environment:** `boundlexx-*` services on port 28000 (e.g., `boundlexx-django`, `boundlexx-postgres`)
- **Development Environment:** `boundlexx-*-dev` containers on port 28001 (e.g., `boundlexx-django-dev`, `boundlexx-postgres-dev`)
- **Test Environment:** `boundlexx-*-test` containers on port 28002 (e.g., `boundlexx-django-test`, `boundlexx-postgres-test`)

This approach provides complete environment isolation, eliminates redundant double-prefixes, and ensures clean, predictable naming patterns. All configurations use explicit `container_name` declarations and include comprehensive Kubernetes labels for future orchestration compatibility.

### Documentation Structure
- **Quick setup:** `README.rst` (simple instructions)
- **Complete technical guide:** `docs/modernization/ENVIRONMENT_SETUP.md` (troubleshooting, advanced workflows, and detailed testing workflows)
- **Project tracking:** `docs/modernization/MODERNIZATION_TRACKING.md` (all changes logged)

### Testing Workflow:
**For detailed testing workflows, see:** `docs/modernization/ENVIRONMENT_SETUP.md`

### Multiple Testing Approaches:
The project supports multiple testing strategies for different use cases:

1. **Physical Environment Isolation:**
   - Separate clone directories (e.g., `boundlexx-yatesjj-test`)
   - Container isolation with folder-based naming
   - Port isolation (dev: 28001, test: 28002)
   - Complete environment separation for full integration testing

2. **Database-Level Isolation (.test.env):**
   - Uses `test_boundlexx` database instead of `boundlexx`
   - Same containers and infrastructure as development
   - Ideal for unit tests, CI/CD, and rapid database testing
   - Complements rather than conflicts with physical isolation

3. **Usage Guidelines:**
   - **Quick database testing:** Use `.test.env` for rapid database-focused testing
   - **Full environment testing:** Use separate clone setup for complete isolation
   - **Automated testing/CI:** Use `.test.env` for pipelines where full container isolation isn't needed
   - **Data experimentation:** Use `.test.env` for testing schema changes or ingestion logic

# Copilot Instructions for Boundlexx Modernization

## Project Overview
Boundlexx is a Django monorepo for Boundless game data, supporting both containerized and local hybrid development. The project is being modernized for maintainability and reproducibility, with all changes tracked in `docs/modernization/`.

## Architecture & Key Components
- **Project root**: Contains all main directories: `boundlexx/` (main Django app), `config/`, `docker/`, `docs/`, `requirements/`, etc.
- **Django app**: The `boundlexx/` directory should directly contain app submodules (`admin/`, `api/`, `boundless/`, etc.) and `__init__.py`.
- **No extra nesting**: Avoid `boundlexx/boundlexx/` or similar redundant nesting. If present, move all submodules up one level and remove the extra directory.
- `config/` — Django settings (local, production, test), WSGI, Celery, and Huey config.
- `docker/` — Dockerfiles and bin scripts for dev workflows. See modernization docs for archive/EOL fixes.
- `requirements/` — Dependency management using pip-compile (`in/` for input, `dev.txt`, `production.txt` for output).
- `tests/` — Test suite, organized by app.
- Modernization logs and rollback steps: `docs/modernization/`
## Workspace Setup Guidance
- When recreating the workspace, ensure the project root contains all main folders and files (see above).
- The main Django app (`boundlexx/`) should not be nested inside another `boundlexx/` directory.
- If you see duplicate or nested folders, correct the structure before proceeding with development or modernization.

## Developer Workflows
- **Containerized:**
  - **Required setup:** Copy `.env` to `.local.env` for local environment configuration
  - Use `docker-compose` with `.env`/`.local.env` for environment variables.
  - Main service: `django` (port 28001). Use VS Code devcontainer for pre-configured setup.
  - Run management commands: `docker-compose run --rm manage python manage.py <command>`
- **Hybrid Local:**
  - Create `.venv` and install from `requirements/dev.txt` (see `SETUP_LOCAL_VENV.md`).
  - Run: `python manage.py <command>`
- **VS Code Tasks (Recommended):**
  - Use "Tasks: Run Task" from Command Palette for all common operations
  - Key tasks: "Boundlexx: Manage", "Boundlexx: Migrate Database", "Boundlexx: Ingest Game Data"
  - **Migration workflow:** If migration warns about pending changes, run "Boundlexx: Make Migrations" then "Boundlexx: Migrate Database"
  - **Ingestion:** Use "Boundlexx: Create Game Objects (Full Ingestion)" for automated skills+recipes workflow
  - Avoid tasks marked "LEGACY, DO NOT USE"
- **Lint/Format:**
  - `docker-compose run lint` (Black, Flake8, isort, Bandit)
  - `docker-compose run format` (Black, isort)
- **Testing:**
  - `docker-compose run test` (pytest, coverage)
  - Test config: `[tool.pytest.ini_options]` in `pyproject.toml`
  - **Database isolation:** Use `.test.env` for isolated test database (`test_boundlexx`)
  - **Environment isolation:** Use separate clone directories for complete test environments
- **Background Tasks:**
  - Celery: `docker-compose up celery celerybeat`
  - Huey: `docker-compose up huey-consumer huey-scheduler`


## Project-Specific Conventions & Forward Migration Policy
- All modernization and troubleshooting steps must be logged in `docs/modernization/` with rationale and rollback.
- The `docs/modernization/template_examples/` directory is for research/reference only and must NOT be used to track or document any work in this build. All tracking and documentation must be done in the main modernization files (e.g., `MODERNIZATION_TRACKING.md`).
- Use `pip-compile` to update requirements; never edit `dev.txt` or `production.txt` directly.
- Dockerfiles may use Debian archive workarounds (see modernization log).
- Exclude migrations, static cache, and some utility files from linting/formatting (see config files).
- Use feature branches and reference modernization logs in PRs (see `docs/modernization/GIT_WORKFLOW.md`).

### Forward Migration Requirements (CRITICAL)
**All code changes must verify compatibility with target modernization stack:**
- **Django 5.2 LTS compatibility**: Model changes, admin customizations, URL patterns, middleware
- **TaskIQ readiness**: Background tasks designed for async migration from Celery
- **Django Ninja preparation**: API endpoints ready for DRF → Django Ninja transition
- **uv dependency management**: Requirements structured for pyproject.toml migration
- **Ruff + mypy standards**: Code follows modern Python linting/typing practices
- **Container-first development**: All testing in Docker to prevent environment conflicts

### Migration Impact Assessment Required
Before implementing any feature, assess impact on:
1. **Issue #31 (TaskIQ)**: Will this task need async migration?
2. **Issue #32 (Django Ninja)**: Does this API endpoint need DRF → Ninja compatibility?
3. **Issue #30 (uv/pyproject.toml)**: Are dependency changes compatible with modern structure?
4. **Issue #29 (Ruff/mypy)**: Does code follow modern linting standards?
5. **Issue #27 (Remove Huey)**: Will this conflict with Huey → Celery consolidation?

## Git Workflow for Modernization
- **Remotes:**
  - `origin` should point to your fork (e.g., https://github.com/yatesjj/boundlexx)
  - `upstream` should point to the original (e.g., https://github.com/AngellusMortis/boundlexx)
  - Example setup:
    ```sh
    git remote set-url origin https://github.com/yatesjj/boundlexx.git
    git remote add upstream https://github.com/AngellusMortis/boundlexx.git
    ```
- **Syncing with upstream:**
  - Regularly fetch and merge changes:
    ```sh
    git fetch upstream
    git checkout master
    git merge upstream/master
    git push origin master
    ```
- **Feature branch workflow:**
  - Create a new branch for each change:
    ```sh
    git checkout -b feature/short-description
    # make changes
    git add .
    git commit -m "Short, descriptive message"
    git push origin feature/short-description
    ```
  - Open a Pull Request (PR) from your branch to `master` in your fork.
- **Rollback and history:**
  - Use `git log` to view history.
  - Use `git revert <commit>` to undo a commit.
  - Use `git checkout <commit> -- <file>` to restore a file from history.
- **Best practices:**
  - Keep PRs focused and small for easier review.
  - Reference the modernization tracking log in PR descriptions.
  - Tag releases or milestones for major steps.

## Integration Points
- **External:** Postgres, Redis (via Docker Compose), Discord/Github OAuth, Boundless game data ingest.
- **Custom scripts:** See `docker/bin/` for all workflow automation.

## Examples
- Lint: `docker-compose run lint`
- Test: `docker-compose run test`
- Start Celery: `docker-compose up celery`
- Ingest game data: Use VS Code Tasks or management commands

---
For all modernization/migration documentation, see `docs/modernization/`. For local venv setup, see `SETUP_LOCAL_VENV.md`. For git workflow, see `docs/modernization/GIT_WORKFLOW.md`.

---
**Note:** If you are recreating the workspace, double-check the directory structure before running setup or migration commands. The correct structure is essential for Django imports, Docker builds, and all developer workflows.
