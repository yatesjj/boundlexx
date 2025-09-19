# Forward Migration Compatibility Guide

This document provides specific guidance for ensuring all code changes are compatible with the planned modernization stack. Use this as a checklist before implementing any feature or fix.

## Overview
Boundlexx is undergoing comprehensive modernization across multiple phases. All code changes must be designed with forward compatibility in mind to ensure smooth transitions.

## Target Technology Stack

### Core Infrastructure
- **Python**: 3.12 (modern, high-performance)
- **Django**: 5.2 LTS (long-term support until April 2028)
- **Database**: PostgreSQL with psycopg2-binary
- **Container**: Docker with python:3.12-slim-bookworm

### Async & Task Management
- **Current**: Celery 5.5.3 + Huey (transitional)
- **Target**: TaskIQ (asyncio-native, high performance)
- **Migration**: Gradual Celery → TaskIQ, remove Huey first

### API Framework
- **Current**: Django REST Framework (DRF)
- **Target**: Django Ninja (pydantic, high performance)
- **Migration**: v2 API rebuild or v3 API creation

### Dependency Management
- **Current**: pip + pip-tools + requirements/*.txt
- **Target**: uv + pyproject.toml (modern, fast)
- **Migration**: Consolidate all dependencies into pyproject.toml

### Code Quality
- **Current**: flake8, pycodestyle, mypy, pylint, isort, black
- **Target**: Ruff + mypy (comprehensive, fast)
- **Migration**: Incremental adoption, remove old tools after validation

## Pre-Implementation Checklist

### For Any Code Change
- [ ] Will this code work with Django 5.2 LTS?
- [ ] Does this follow modern Python 3.12 patterns?
- [ ] Is this compatible with container-first development?
- [ ] Have I avoided deprecated Django features?

### For Background Tasks
- [ ] Can this task be easily migrated to TaskIQ async?
- [ ] Have I avoided Huey-specific features?
- [ ] Is the task designed for potential parallelization?
- [ ] Does the task follow async-friendly patterns?

### For API Endpoints
- [ ] Can this endpoint be rebuilt in Django Ninja?
- [ ] Are the serializers compatible with pydantic models?
- [ ] Have I avoided DRF-specific features that don't translate?
- [ ] Is the API designed for high performance?

### For Dependencies
- [ ] Is this package compatible with Python 3.12?
- [ ] Will this work with uv dependency resolution?
- [ ] Can this be specified in pyproject.toml format?
- [ ] Have I avoided version constraints that conflict with the target stack?

### For Code Style
- [ ] Does this code pass Ruff linting rules?
- [ ] Are type hints compatible with mypy?
- [ ] Have I followed modern Python conventions?
- [ ] Is the code structured for automated formatting?

## Migration Phase Considerations

### Phase 3: Django 5.2 LTS (Current)
- Use Django 5.2 compatible model fields and admin customizations
- Avoid deprecated URL patterns and middleware
- Leverage Django 5.2 async capabilities where appropriate
- Ensure all custom commands work with Django 5.2

### Phase 4: uv + pyproject.toml
- Structure requirements for easy pyproject.toml migration
- Avoid complex pip-tools specific configurations
- Use standard dependency specification formats
- Consider optional dependencies and extras

### Phase 5: Ruff + mypy
- Follow Ruff's default rule set where possible
- Add appropriate type hints for mypy compatibility
- Structure code to minimize linting exceptions
- Use modern Python idioms that Ruff encourages

### Phase 6: Remove Huey
- Avoid adding new Huey tasks
- Design tasks for Celery compatibility
- Consider task consolidation opportunities
- Plan for single task queue architecture

### Phase 7: TaskIQ Migration
- Design tasks with async patterns in mind
- Avoid blocking operations in task logic
- Structure tasks for easy async conversion
- Consider task result handling patterns

### Phase 8: Django Ninja
- Design API schemas for pydantic compatibility
- Structure endpoints for high performance
- Avoid DRF-specific customizations
- Plan for API versioning strategy

## Common Pitfalls to Avoid

### Django Version Issues
- Don't use Django 4.x specific features that were removed in 5.2
- Avoid deprecated URL patterns like `url()`
- Don't rely on Django features that conflict with async patterns

### Task Queue Issues
- Don't create Huey-specific task implementations
- Avoid blocking I/O in task functions
- Don't design tasks that require synchronous execution patterns

### API Design Issues
- Don't create DRF customizations that can't be migrated
- Avoid complex serializer inheritance that won't translate to pydantic
- Don't design APIs that require DRF-specific features

### Dependency Issues
- Don't add packages that conflict with Python 3.12
- Avoid packages that don't support modern dependency resolution
- Don't create complex requirement constraints that can't be migrated

## Testing Strategy

### Container-First Testing
- All testing must be done in Docker containers
- Use the configured dev container for consistency
- Test with the target Python and Django versions
- Validate container builds before committing

### Migration Readiness Testing
- Test with the target technology versions when possible
- Validate API compatibility with pydantic models
- Test task execution patterns with async concepts
- Verify linting with Ruff rules

## Documentation Requirements

### Change Documentation
- Log all changes in `MODERNIZATION_TRACKING.md`
- Include forward migration considerations
- Document any compatibility assumptions
- Provide rollback instructions

### Code Documentation
- Include type hints for mypy compatibility
- Document async compatibility considerations
- Explain migration strategy for complex features
- Reference related modernization issues

## Getting Help

### Issue References
- **Issue #23**: Django 5.2+ upgrade
- **Issue #27**: Remove Huey
- **Issue #29**: Update linters (Ruff + mypy)
- **Issue #30**: uv + pyproject.toml migration
- **Issue #31**: TaskIQ migration
- **Issue #32**: Django Ninja migration
- **Issue #33**: Project structure modernization

### Resource Links
- Django 5.2 documentation: https://docs.djangoproject.com/en/5.2/
- TaskIQ documentation: https://taskiq-python.github.io/
- Django Ninja documentation: https://django-ninja.dev/
- Ruff documentation: https://docs.astral.sh/ruff/
- uv documentation: https://docs.astral.sh/uv/

### Testing Resources
- Use VS Code tasks for consistent testing
- Refer to `docs/modernization/ENVIRONMENT_SETUP.md` for testing workflows
- Use container-based testing for environment consistency