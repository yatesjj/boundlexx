## 2025-09-09: Initial Migrations and Server Startup

- **Description:** After container setup, ran `python manage.py migrate` to apply all database migrations, then started the Django development server with `python manage.py runserver 0.0.0.0:8000`. Confirmed the site is available at http://127.0.0.1:8000.
- **Rationale:** Required to initialize the database and make the web application accessible for development and testing.
- **How to Reproduce:**
  1. Run `python manage.py migrate` inside the dev container.
  2. Run `python manage.py runserver 0.0.0.0:8000`.
  3. Access the site at http://127.0.0.1:8000.
- **How to Roll Back:**
  - If migrations cause issues, restore the database from backup or use Django's migration rollback commands.
## 2025-09-09: Superuser Creation and Login Clarification

- **Description:** Verified that the only available login is Django's standard username/password login. There is no Discord, Github, or other social login in the codebase. Created a superuser using the VS Code task "Boundlexx: Manage" with the `createsuperuser` command.
- **Rationale:** Required for admin access and user management. README previously referenced social login, which is not implemented.
- **How to Reproduce:**
  1. Open the Command Palette and select "Tasks: Run Task".
  2. Choose "Boundlexx: Manage".
  3. When prompted, enter `createsuperuser` and follow the prompts.
- **How to Log In:**
  - Visit http://127.0.0.1:8000/admin/ and log in with the superuser credentials you created.
- **How to Roll Back:**
  - Remove the superuser via the Django admin or database if needed.
# Modernization & Migration Plan (2025)

See the full plan in `docs/modernization/MODERNIZATION_PLAN.md` and the instructions in `.github/copilot-instructions.md`.

**Summary:**
- All tracking and documentation must be done in this file and other main modernization docs. `template_examples` is for research/reference only.
- Follow the sequenced steps for each issue, with backups, feature branches, and incremental upgrades.
- Research and resolve deprecations, validate all changes, and document every step and rollback.

Refer to the plan document for details on each step and best practices.

# 2025 Modernization & Migration Plan

**Note:** The `docs/modernization/template_examples/` directory is for research/reference only and must NOT be used to track or document any work in this build. All tracking and documentation must be done in this file and other main modernization docs.

This section summarizes the comprehensive plan to address all open modernization issues (see `ISSUES.md`) and safely complete all migrations. All steps are to be logged here with rationale, references, and rollback instructions.

## General Principles
- Research and plan each step using official documentation and `template_examples/`.
- Back up all databases, Redis, and Docker images before major changes.
- Use feature branches and tag before/after major migrations for rollback.
- Only run commands in the correct Docker/VS Code devcontainer environment.
- Use VS Code tasks for all management commands.
- Document every step, rationale, and rollback here.

## Issue-by-Issue Plan

1. **Update Github Actions (#34):** Update workflows, test, and document. Reference: [ark-operator workflows](https://github.com/AngellusMortis/ark-operator/tree/master/.github/workflows)
2. **Simplify/Update Project Structure (#33):** Refactor to match modern standards. Reference: [ark-operator](https://github.com/AngellusMortis/ark-operator)
3. **Replace DRF with Django Ninja (#32):** Prototype v2 API in Django Ninja, deprecate v1 if successful, else create v3. Maintain compatibility during transition.
4. **Replace Celery with TaskIQ (#31):** Set up TaskIQ, migrate tasks incrementally, validate, and remove Celery only after success.
5. **Update Requirements Management (#30):** Move to `pyproject.toml` and `uv`, keep old files until validated.
6. **Update Linters (#29):** Add Ruff and mypy, incrementally fix issues, then remove old linters.
7. **Raise Code Coverage (#28):** Add/expand tests to reach 85%+ coverage.
8. **Remove Huey (#27):** Convert Huey tasks back to Celery/TaskIQ, validate, and remove Huey only after success.
9. **Move setup.cfg into pyproject.toml (#26):** Migrate tool configs, test, and remove old config after validation.
10. **Rename Container Images (#25):** Update Dockerfiles/Compose, test, and document.
11. **Fix Steam Login (#24):** Update management command/scripts, test, and document.
12. **Update to Django 4.2+ (#23):** Upgrade Django and dependencies, test, and document.
13. **Update to Python 3.10+ (#22):** Update Dockerfiles/CI/envs, test, and document.
14. **Ensure Containers Build in GHA (#21):** Update workflows to build/test containers on push.

## Migration & Rollback Strategy
- Tag before/after each major migration for rollback.
- Restore database/Redis from backup if migrations fail.
- Keep old configs/scripts until new ones are fully validated.

## Documentation
- Reference `template_examples/` for prior research and validated strategies.
- Log all actions, rationale, and rollback steps here as each issue is addressed.
#
## 2025-09-08: Dockerfile EOL Fix and .local.env Recreation

### 1. Debian Buster Archive Fix in Dockerfile (Reapplied)
  - `docker/django/Dockerfile`
  - Remove the `sed` lines that update apt sources to the archive URLs and the apt.conf.d line.

### 2. Recreated .local.env File
  - `.local.env`
  - Delete `.local.env` from the project root.

### 3. Created and Configured docker-compose.override.yml
- **Description:** Added and configured `docker-compose.override.yml` in the project root to enable local environment overrides, port mapping, and volume mounts for Boundless and icon renderer paths. Ensured correct Windows paths and enabled `.local.env` for all relevant services.
- **Rationale:** Required for proper dev container and Docker Compose startup, especially on Windows. Ensures correct service configuration and local development compatibility.
- **Files Changed:**
  - `docker-compose.override.yml`
- **How to Roll Back:**
  - Delete or rename `docker-compose.override.yml` from the project root, or revert to a previous version if misconfigured.



# 2025-09-09: Ingestion Debugging (Create Game Objects)

  - Print-debugging in `_create_colors` showed that all `color_id` values and `colors` keys matched, and the color import step completed successfully.
  - The process now fails at the recipe import step with a `Skill.DoesNotExist` error in `boundlexx.boundless.models.game.Skill`, specifically when looking up a skill by name during `_get_requirements` in `ingest/recipe.py`.
  - Print-debugging revealed the missing Skill is 'Decoration Crafting'.
  - Root cause: Skill ingestion is not included in the default core group. Skills must be imported before recipes to avoid missing Skill errors.
  - Solution: Always run `python manage.py create_game_objects --skill` and then `python manage.py create_game_objects --recipe` as separate commands. Running both in the same command does not work due to transaction/visibility issues.
  - Documentation and VS Code task instructions updated to enforce this two-step process.
  - How to Roll Back: Revert documentation and task changes if needed.

## 2025-09-09: VS Code Tasks Improvement and Workflow Automation

- **Description:** Added new VS Code tasks to automate the ingestion workflow and provide a reliable, one-click solution for developers:
  - "Boundlexx: Create Game Objects (Skills Only)" - runs `--skill` only
  - "Boundlexx: Create Game Objects (Recipes Only)" - runs `--recipe` only
  - "Boundlexx: Create Game Objects (Full Ingestion)" - compound task that runs skills then recipes in sequence
  - Marked the original "Create Game Objects" task as legacy to avoid confusion
- **Rationale:** The two-step ingestion process (skills first, then recipes) is now automated via VS Code tasks, ensuring developers can easily run the correct workflow without manual commands.
- **Files Changed:**
  - `.vscode/tasks.json` - Added new tasks with proper `dependsOn` and `dependsOrder` properties
  - Documentation updated to reflect the new workflow options
- **How to Use:**
  1. For full ingestion: Run "Boundlexx: Create Game Objects (Full Ingestion)" from VS Code task picker
  2. For individual steps: Run "Skills Only" or "Recipes Only" tasks as needed
  3. Avoid using the legacy task marked "DO NOT USE"
- **How to Roll Back:**
  - Remove the new tasks from `.vscode/tasks.json` and restore the original task definition if needed
  - Revert documentation changes to the previous manual command instructions

## 2025-09-09: Environment File Line Endings Fix

- **Description:** Fixed Windows carriage return (CRLF) line endings in `.local.env` that were causing `/dev/fd/63: line X: $'\r': command not found` warnings during task execution.
- **Rationale:** Clean task execution without spurious warnings improves developer experience and reduces confusion during debugging.
- **Technical Details:** Used `sed -i 's/\r$//' /app/.local.env` to convert Windows line endings (CRLF) to Unix line endings (LF).
- **Files Changed:**
  - `.local.env` - Line endings converted from CRLF to LF
- **Verification:** Environment variable loading now works without carriage return warnings in VS Code tasks.
- **How to Roll Back:**
  - If needed, convert back to Windows line endings with `sed -i 's/$/\r/' /app/.local.env`, though this is not recommended.

## 2025-09-09: Complete Ingestion Workflow Solution

- **Status:** ✅ **COMPLETED** - Robust, automated ingestion workflow established
- **Summary:** Successfully resolved all ingestion issues and created a production-ready workflow:
  1. **Root Cause Analysis:** Identified that skills must be imported before recipes due to foreign key dependencies
  2. **Debugging Process:** Used print-debugging to trace KeyErrors through subtitles, colors, and finally skill dependencies
  3. **Solution Implementation:** Created separate VS Code tasks for skills and recipes, plus a compound task for full automation
  4. **Environment Optimization:** Fixed line ending issues for clean task execution
  5. **Documentation Updates:** Updated README.rst and tracking docs to reflect new workflow

- **Key Learnings:**
  - Django management commands with `--skill --recipe` don't work reliably due to transaction/visibility issues
  - Separate command execution is required: `--skill` first, then `--recipe`
  - VS Code compound tasks with `dependsOn` and `dependsOrder` provide excellent workflow automation
  - Environment file line endings can cause spurious warnings in containerized environments

- **Final Workflow:**
  - **Recommended:** Use "Boundlexx: Create Game Objects (Full Ingestion)" VS Code task
  - **Manual Alternative:** Run "Skills Only" then "Recipes Only" tasks individually
  - **Command Line:** `python manage.py create_game_objects --skill` then `python manage.py create_game_objects --recipe`

- **How to Roll Back:**
  - Revert to original single task if the compound workflow needs modification
  - All debug prints are commented out and can be re-enabled if further troubleshooting is needed


- **Findings (Print Debug Info):**
  - Print-debugging in `_create_items` showed that all `subtitle_id` values and `subtitles` keys matched and were of type `int`.
  - The ingestion step for items completed successfully after this check, confirming the subtitles mapping is correct and not the source of the original KeyError.
  - The process now fails at the next step, `Creating Colors...`, with a new `KeyError: 1` in `_create_colors`, specifically at `color=colors[color_id]`.
- **Next Steps:**
  - Add print-debug statements to `_create_colors` to log `color_id` and `colors.keys()` before the KeyError line, to diagnose the missing color mapping.
  - Continue documenting all findings and rationale for each debugging step.


- **Description:** Encountered a `KeyError` during the "Create Game Objects" ingestion step, traced to a missing or mismatched subtitle ID in the subtitles dictionary in `boundlexx/ingest/ingest/core.py`.
- **Rationale:** Robust ingestion is critical for reproducible setup. The error is likely due to a type mismatch or missing data in the subtitles mapping.
- **Debugging Plan:**
  1. Add print-debug statements to log subtitle IDs and dictionary keys during item creation. This will help identify the exact cause (type mismatch, missing key, or data issue) without altering ingestion logic.
  2. If needed, add a fallback to avoid crashing on missing subtitles, but only after root cause is confirmed.
- **How to Reproduce:**
  1. Run the "Boundlexx: Ingest Game Data" task.
  2. Run the "Boundlexx: Create Game Objects" task.
  3. Observe the KeyError in the logs.
- **How to Roll Back:**
  - Remove or comment out print-debug statements after diagnosis.
  - If fallback logic is added, ensure it is documented and justified, or revert if not needed.

# Boundlexx Modernization & Migration Tracking Log

This document tracks all technical changes, findings, and decisions made during the Boundlexx migration and modernization effort. Each entry includes the date, description, rationale, affected files, and rollback instructions. This log is intended to be detailed and technical to help others reproduce or understand the process.

---

## 2025-09-08: Project Initialization

### 1. Debian Buster Archive Fix in Dockerfile
- **Description:** Updated `docker/django/Dockerfile` to use Debian archive URLs for Buster, resolving apt-get update failures due to EOL repositories.
- **Rationale:** Debian Buster repositories are EOL and moved to archive; this fix restores package installation.
- **Files Changed:**
  - `docker/django/Dockerfile`
- **How to Roll Back:**
  - Remove the `sed` lines that update apt sources to the archive URLs.

### 2. Created .local.env File
- **Description:** Added `.local.env` to satisfy Docker Compose and dev container requirements for environment variables.
- **Rationale:** Required for container startup and configuration.
- **Files Changed:**
  - `.local.env`
- **How to Roll Back:**
  - Delete `.local.env` from the project root.

### 3. Set Up Local Python Virtual Environment
- **Description:** Added instructions for creating and using a `.venv` for hybrid local + Docker development.
- **Rationale:** Allows safe local development without affecting global Python install.
- **Files Changed:**
  - `SETUP_LOCAL_VENV.md`
- **How to Roll Back:**
  - Delete `.venv` directory and related instructions if not needed.

---

## 2025-09-08: Successful Dev Container Startup

### 4. Verified Dev Container Startup
- **Description:** Successfully started the VS Code dev container after configuring `docker-compose.override.yml` and ensuring all required files and paths were present. Confirmed that the development environment is now operational.
- **Rationale:** Confirms that the modernization and troubleshooting steps were effective and the dev workflow is unblocked.
- **Files Verified:**
  - `docker-compose.override.yml`
  - `.local.env`
  - `docker/django/Dockerfile`
- **How to Roll Back:**
  - If future container startup issues occur, review recent changes to these files and consult previous troubleshooting steps in this log.

---

## Documentation Guidelines
- Log every significant change, including rationale and rollback steps.
- Document all findings, issues, and solutions in detail.
- Keep this file up to date as the migration progresses.

---

For all modernization documentation, keep files in this directory (`docs/modernization/`).
