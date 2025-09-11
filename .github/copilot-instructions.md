## Authenticat### FINAL CONTAINER MANAGEMENT ARCHITECTURE ✅

**Production Scripts (2 total):**
- `setup_development_container_improved.py` - Main development setup with dry-run
- `setup_test_container.py` - Test environments with port offsets and dry-run

**Archived Scripts (for reference):**
- `docs/modernization/archived_scripts/run_for_parallel_test_containers.py` - Complex parallel testing (archived)

**Recommended Workflow:**
- **Main development**: `C:\VSCode\boundlexx-yatesjj\boundlexx-yatesjj\` → use development script
- **Test environments**: `C:\VSCode\boundlexx-test-*\boundlexx\` → use test script  
- **Each folder gets unique container prefixes automatically**

### FILES READY FOR PRODUCTION ✅
- `setup_development_container_improved.py` (✅ production ready with dry-run)
- `setup_test_container.py` (✅ enhanced with dry-run capability) 
- `docker-compose.override.example.yml` (✅ enhanced with all container names)
- `docs/modernization/ENVIRONMENT_SETUP.md` (✅ complete documentation)
- `docs/modernization/archived_scripts/` (✅ complex scripts archived for reference)up

- Boundlexx uses Django's standard authentication (username/password). There is **Setup Process:**
1. Clone repo with meaningful folder structure (e.g., `C:\VSCode\boundlexx-yatesjj\boundlexx\`)
2. Copy template files: `cp .env .local.env` and `cp docker-compose.override.example.yml docker-compose.override.yml`
3. Run: `python setup_development_container_improved.py` (prefixes containers with "boundlexx-yatesjj")
4. Customize local files for personal setup

### VERIFICATION COMPLETE ✅
- Base files remain clean and committable
- Container names follow pattern: `boundlexx-yatesjj-django-1`, `boundlexx-yatesjj-postgres-1`, etc.
- Multi-environment support (different folder names = different prefixes)
- Documentation updated in README.rst and new ENVIRONMENT_SETUP.md

### FINAL CONTAINER MANAGEMENT ARCHITECTURE ✅

**Production Scripts (2 total):**
- `setup_development_container_improved.py` - Main development setup with dry-run
- `setup_test_container.py` - Test environments with port offsets and dry-run

**Archived Scripts (for reference):**
- `docs/modernization/archived_scripts/archive_run_for_parallel_test_containers.py` - Complex parallel testing (archived)

**Recommended Workflow:**
- **Main development**: `C:\VSCode\boundlexx-yatesjj\boundlexx-yatesjj\` → use development script
- **Test environments**: `C:\VSCode\boundlexx-test-*\boundlexx\` → use test script  
- **Each folder gets unique container prefixes automatically**

### FILES READY FOR PRODUCTION ✅
- `setup_development_container_improved.py` (✅ production ready with dry-run)
- `setup_test_container.py` (✅ enhanced with dry-run capability) 
- `docker-compose.override.example.yml` (✅ enhanced with all container names)
- `docs/modernization/ENVIRONMENT_SETUP.md` (✅ complete documentation)
- `docs/modernization/archived_scripts/` (✅ complex scripts archived for reference)b, or other social login enabled by default.
- To create an admin user, use the VS Code task "Boundlexx: Manage" and enter `createsuperuser` when prompted for the management command.
- Log in at http://127.0.0.1:8000/admin/ with the credentials you create.

## Starting the Django Development Server

- Before starting the server for the first time, you must apply all database migrations:

  ```sh
  python manage.py migrate
  ```

- Then start the Django development server inside the dev container:

  ```sh
  python manage.py runserver 0.0.0.0:8000
  ```
- This will make the site available at http://127.0.0.1:8000 on your host machine.
- For production or multi-service setups, use Docker Compose as described in the main documentation.

## Game Data Ingestion Workflow (IMPORTANT)

### ✅ Automated VS Code Tasks (Recommended)
- **"Boundlexx: Create Game Objects (Full Ingestion)"** - Runs skills then recipes automatically in correct order
- **"Boundlexx: Create Game Objects (Skills Only)"** - Import skills only
- **"Boundlexx: Create Game Objects (Recipes Only)"** - Import recipes only (run after skills)

### 🚨 Critical Requirements
1. **Skills MUST be imported before recipes** - recipes have foreign key dependencies on skills
2. **Never use the legacy task** marked "DO NOT USE" - it's unreliable
3. **Use separate commands** - running `--skill --recipe` together doesn't work due to transaction visibility issues

### Manual Command Workflow
```sh
# Step 1: Import game data first
python manage.py ingest_game_data 249.4.0

# Step 2: Import skills (required first!)
python manage.py create_game_objects --skill

# Step 3: Import recipes (only after skills)
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

## CURRENT SESSION STATUS (2025-09-10)

### Container Management Scripts - COMPLETE ✅
- ✅ Created 3 container management scripts with comprehensive functionality
- ✅ Added comprehensive documentation and VS Code tasks
- ✅ Fixed port mapping inconsistency in docker-compose.override.yml (28000→8000)
- ✅ Added explicit container names and networks to docker-compose.yml
- ✅ Created container_status.py utility and setup_development_container_improved.py
- ✅ Fixed prefix logic to use parent folder name for meaningful prefixes
- ✅ **ENVIRONMENT ARCHITECTURE COMPLETE**: Implemented proper Docker Compose best practices

### CLEAN ENVIRONMENT ARCHITECTURE ✅
**Base Files (Committed & Clean):**
- `docker-compose.yml` - Base service definitions (no container names, no local paths)
- `.env` - Base environment variables with safe defaults
- `docker-compose.override.example.yml` - Template for developers

**Local Files (Not Committed):**
- `docker-compose.override.yml` - Personal customizations (container names, local paths)
- `.local.env` - Personal environment variables

**Setup Process:**
1. Clone repo with meaningful folder structure (e.g., `C:\VSCode\boundlexx-yatesjj\boundlexx`)
2. Copy template files: `cp .env .local.env` and `cp docker-compose.override.example.yml docker-compose.override.yml`
3. Run: `python setup_development_container_improved.py` (prefixes containers with "boundlexx-yatesjj")
4. Customize local files for personal setup

### VERIFICATION COMPLETE ✅
- Base files remain clean and committable
- Container names follow pattern: `boundlexx-yatesjj-django-1`, `boundlexx-yatesjj-postgres-1`, etc.
- Multi-environment support (different folder names = different prefixes)
- Documentation updated in README.rst and new ENVIRONMENT_SETUP.md

### FILES READY FOR PRODUCTION ✅
- `setup_development_container_improved.py` (✅ production ready)
- `setup_test_container.py` (✅ production ready) 
- `docker-compose.override.template.yml` (✅ comprehensive template)
- `docs/modernization/ENVIRONMENT_SETUP.md` (✅ complete documentation)

### NEXT MODERNIZATION STEP:
**Container Management: COMPLETE ✅** 
**Ready for next issue**: GitHub Actions modernization, Project Structure simplification, or Django Ninja API migration
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
  - Main service: `django` (port 8000). Use VS Code devcontainer for pre-configured setup.
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
