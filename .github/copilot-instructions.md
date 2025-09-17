# Copilot Instructions f### ✅ Automated VS Code Tasks (Recommended)
- **"Boundlexx: Complete Setup (Ingest + Core + Skills + Recipes - All Languages)"** - Complete automation: ingest game data → core data → skills → recipes (all 5 languages)
- **"Boundlexx: Fast Complete Setup (Ingest + Core + Skills + Recipes - English Only)"** - Fast development setup with English localizations only (80% faster)
- **"Boundlexx: Create Game Objects (Core + Skills + Recipes - All Languages)"** - Runs core → skills → recipes automatically in correct order (all languages)
- **"Boundlexx: Fast Create Game Objects (Core + Skills + Recipes - English Only)"** - Runs core → skills → recipes with English only for faster setup
- **"Boundlexx: Create Game Objects (Core Data - English Only)"** - Import core data with English only for faster setup
- **"Boundlexx: Add Remaining Languages"** - Add remaining localizations after English-only setupndlexx Modernization

## Authentication & User Management
- To create an admin user, use the VS Code task "Boundlexx: Manage" and enter `createsuperuser` when prompted for the management command.
- Log in at http://127.0.0.1:28000/admin/ with the credentials you create.

## Starting the Django Development Server

- Before starting the server for the first time, you must apply all database migrations:

  ```sh
  python manage.py migrate
  ```

- Then start the Django development server inside the dev container:

  ```sh
  python manage.py runserver 0.0.0.0:28000
  ```
- This will make the site available at http://127.0.0.1:28000 on your host machine.
- For production or multi-service setups, use Docker Compose as described in the main documentation.

## Game Data Ingestion Workflow (IMPORTANT)

### ✅ Automated VS Code Tasks (Recommended)
- **"Boundlexx: Complete Setup (Game Data + Full Ingestion)"** - Complete automation: game data → core data → skills → recipes
- **"Boundlexx: Fast Setup - English Only"** - Quick development setup with English localizations only (80% faster)
- **"Boundlexx: Create Game Objects (Full Ingestion)"** - Runs core → skills → recipes automatically in correct order
- **"Boundlexx: Create Game Objects (Core Data - English Only)"** - Import core data with English only for faster setup
- **"Boundlexx: Add Remaining Languages"** - Add remaining localizations after English-only setup

### 🚀 Fast Development Setup (Recommended)
For faster development iterations, use English-only setup which reduces database size by ~80% (2,190 vs 10,964 LocalizedString objects):

1. **English-only setup:** "Boundlexx: Fast Setup - English Only" 
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
## Modernization & Migration Plan (2025)

### Policy Clarification
- The directory `docs/modernization/template_examples` is for research/reference only. No tracking or documentation of work for this build should occur there. All tracking must be in `MODERNIZATION_TRACKING.md` and related main docs.

### Sequenced Steps
1. **Preparation**
  - Backup database, Redis, Docker images.
  - Use feature branches and tag before/after each major step.
  - Only run commands in the correct Docker/VS Code devcontainer environment.
  - Use VS Code tasks for all management commands.

2. **Issue-by-Issue Plan**
  - Update Github Actions: Review modern workflows, update, and validate.
  - Simplify/Update Project Structure: Refactor to match modern standards, test all commands.
  - Replace DRF with Django Ninja: Prototype v2 API, maintain compatibility, or create v3 if needed.
  - Replace Celery with TaskIQ: Migrate tasks incrementally, validate, keep Celery until proven.
  - Update Requirements Management: Move to `pyproject.toml` and `uv`, keep old files until validated.
  - Update Linters: Add Ruff and mypy, incrementally fix issues, then remove old linters.
  - Raise Code Coverage: Add/expand tests to reach 85%+.
  - Remove Huey: Convert tasks to Celery/TaskIQ, validate, then remove Huey.
  - Move setup.cfg into pyproject.toml: Migrate configs, test, remove old config after validation.
  - Rename Container Images: Update Dockerfiles/Compose, test builds and runs.
  - Fix Steam Login: Update scripts for Steam login, test with 2FA/session tickets.
  - Update to Django 4.2+: Upgrade incrementally, resolve deprecations, update dependencies, test after each step.
  - Update to Python 3.10+: Update Dockerfiles, CI, and envs, test all services and dependencies.
  - Ensure Containers Build in GHA: Update workflows to build/test containers on push.

3. **Research & Conflict Mitigation**
  - Review official docs for Django, Python, TaskIQ, Django Ninja, Ruff, uv, Docker, and CI/CD.
  - Upgrade incrementally, resolve deprecation warnings, check third-party compatibility.
  - Validate all jobs in PRs before merging.

4. **Rollback & Documentation**
  - Tag before/after each major migration for rollback.
  - Restore database/Redis from backup if migrations fail.
  - Keep old configs/scripts until new ones are fully validated.
  - Log all actions, rationale, and rollback steps in `MODERNIZATION_TRACKING.md`.

5. **Next Steps**
  - Archive or remove `template_examples` to avoid confusion.
  - Begin with environment backup and branch setup.
  - Start with the first actionable issue (GHA update), documenting every step.

**Pause before making any environment changes.**

## Container Management - COMPLETE ✅

### Production-Ready Container Scripts:
- `setup_development_container_improved.py` - Main development environments (Django port 28000)
- `setup_test_container.py` - Test environments (Django port 28001, others internal)  
- `container_status.py` - Status monitoring utility

### Container Setup:
1. **Copy template files:** `cp .env .local.env` and `cp docker-compose.override.example.yml docker-compose.override.yml`
2. **Development:** `python setup_development_container_improved.py` (creates folder-prefixed containers)
3. **Test environments:** `python setup_test_container.py` (port offsets for parallel testing)
4. **All scripts support `--dry-run`** for safe preview before applying changes

### Automatic Folder-Based Naming

All container and service names are automatically generated using the name of the current project folder as a prefix. For example, if your project is located in `C:\VSCode\boundlexx-yatesjj\boundlexx-yatesjj\`, all containers and networks will be named with the prefix `boundlexx-yatesjj-` (e.g., `boundlexx-yatesjj-django-1`, `boundlexx-yatesjj-postgres-1`). If you create a test or parallel environment in a different folder, such as `C:\VSCode\boundlexx-yatesjj-test-2\boundlexx-yatesjj-test-2\`, the containers will be named with the prefix `boundlexx-yatesjj-test-2-` (e.g., `boundlexx-yatesjj-test-2-django-1`).

This folder-based naming ensures complete isolation between environments, prevents naming conflicts, and makes it easy to identify which containers belong to which project or test instance. The naming scheme is applied automatically by the setup scripts and does not require manual configuration. Both development and test setup scripts now use the current folder name for the prefix.

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
   - Port isolation (dev: 28000, test: 28001)
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
  - Main service: `django` (port 28000). Use VS Code devcontainer for pre-configured setup.
  - Run management commands: `docker-compose run --rm manage python manage.py <command>`
- **Hybrid Local:**
  - Create `.venv` and install from `requirements/dev.txt` (see `SETUP_LOCAL_VENV.md`).
  - Run: `python manage.py <command>`
- **VS Code Tasks (Recommended):**
  - Use "Tasks: Run Task" from Command Palette for all common operations
  - Key tasks: "Boundlexx: Manage", "Boundlexx: Migrate Database", "Boundlexx: Ingest Game Data"
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


## Project-Specific Conventions
- All modernization and troubleshooting steps must be logged in `docs/modernization/` with rationale and rollback.
- The `docs/modernization/template_examples/` directory is for research/reference only and must NOT be used to track or document any work in this build. All tracking and documentation must be done in the main modernization files (e.g., `MODERNIZATION_TRACKING.md`).
- Use `pip-compile` to update requirements; never edit `dev.txt` or `production.txt` directly.
- Dockerfiles may use Debian archive workarounds (see modernization log).
- Exclude migrations, static cache, and some utility files from linting/formatting (see config files).
- Use feature branches and reference modernization logs in PRs (see `docs/modernization/GIT_WORKFLOW.md`).

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
