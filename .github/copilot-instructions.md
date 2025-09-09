

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
  - Use `docker-compose` with `.env`/`.local.env` for environment variables.
  - Main service: `django` (port 8000). Use VS Code devcontainer for pre-configured setup.
  - Run management commands: `docker-compose run --rm manage python manage.py <command>`
- **Hybrid Local:**
  - Create `.venv` and install from `requirements/dev.txt` (see `SETUP_LOCAL_VENV.md`).
  - Run: `python manage.py <command>`
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
