# Boundlexx Modernization & Migration Plan (2025)

## Policy Clarification
The directory `docs/modernization/template_examples` is for research/reference only. No tracking or documentation of work for this build should occur there. All tracking must be in `MODERNIZATION_TRACKING.md` and related main docs.

## 1. Preparation
- Backup database, Redis, Docker images.
- Use feature branches and tag before/after each major step.
- Only run commands in the correct Docker/VS Code devcontainer environment.
- Use VS Code tasks for all management commands.

## 2. Issue-by-Issue Plan
- **Update Github Actions**: Review modern workflows, update, and validate.
- **Simplify/Update Project Structure**: Refactor to match modern standards, test all commands.
- **Replace DRF with Django Ninja**: Prototype v2 API, maintain compatibility, or create v3 if needed.
- **Replace Celery with TaskIQ**: Migrate tasks incrementally, validate, keep Celery until proven.
- **Update Requirements Management**: Move to `pyproject.toml` and `uv`, keep old files until validated.
- **Update Linters**: Add Ruff and mypy, incrementally fix issues, then remove old linters.
- **Raise Code Coverage**: Add/expand tests to reach 85%+.
- **Remove Huey**: Convert tasks to Celery/TaskIQ, validate, then remove Huey.
- **Move setup.cfg into pyproject.toml**: Migrate configs, test, remove old config after validation.
- **Rename Container Images**: Update Dockerfiles/Compose, test builds and runs.
- **Fix Steam Login**: Update scripts for Steam login, test with 2FA/session tickets.
- **Update to Django 4.2+**: Upgrade incrementally, resolve deprecations, update dependencies, test after each step.
- **Update to Python 3.10+**: Update Dockerfiles, CI, and envs, test all services and dependencies.
- **Ensure Containers Build in GHA**: Update workflows to build/test containers on push.

## 3. Research & Conflict Mitigation
- Review official docs for Django, Python, TaskIQ, Django Ninja, Ruff, uv, Docker, and CI/CD.
- Upgrade incrementally, resolve deprecation warnings, check third-party compatibility.
- Validate all jobs in PRs before merging.

## 4. Rollback & Documentation
- Tag before/after each major migration for rollback.
- Restore database/Redis from backup if migrations fail.
- Keep old configs/scripts until new ones are fully validated.
- Log all actions, rationale, and rollback steps in `MODERNIZATION_TRACKING.md`.

## 5. Next Steps
- Archive or remove `template_examples` to avoid confusion.
- Begin with environment backup and branch setup.
- Start with the first actionable issue (GHA update), documenting every step.

**Pause before making any environment changes.**
