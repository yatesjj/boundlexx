# Dependency Upgrade Decision Matrix
## Quick Reference for Python 3.12 + Django 5.1 Upgrade

### Go/No-Go Decision Points

| Phase | Criteria | Go | No-Go | Action |
|-------|----------|----|----|--------|
| **Phase 1** | Container builds successfully | ✓ Container starts, Python imports work | ✗ Build fails, Python errors | Rollback to `pre-dependency-upgrade` |
| **Phase 2** | Database connections work | ✓ All DBs connect, basic queries work | ✗ Connection failures, driver issues | Rollback to `post-python-upgrade` |
| **Phase 3** | Django 5.1 basic functionality | ✓ Admin loads, migrations run | ✗ Critical Django errors | Rollback to `post-database-upgrade` |
| **Phase 4** | Dependency ecosystem stable | ✓ All packages install/import | ✗ Major version conflicts | Rollback to `post-django-upgrade` |
| **Phase 5** | Development tools operational | ✓ Linting/testing works | ✗ CI/CD fails | Continue (non-critical) |
| **Phase 6** | Core workflows functional | ✓ Game data ingestion works | ✗ Business logic broken | Rollback to `post-development-tools` |
| **Phase 7** | Security/performance acceptable | ✓ Vulns resolved, performance OK | ✗ New security issues | Address before merge |

### Critical Dependencies by Risk Level

#### **HIGH RISK** (Business Critical)
- Django core (5.1.x)
- psycopg2/3 (database connectivity)
- djangorestframework (API layer)
- celery (background tasks)

#### **MEDIUM RISK** (Functionality Impact)
- django-storages (file handling)
- django-redis (caching)
- django-cors-headers (API access)
- All admin-related packages

#### **LOW RISK** (Development/Tooling)
- Black, Ruff, mypy
- django-stubs
- pytest, coverage
- Development utilities

### Version Compatibility Matrix

| Package | Current | Target | Django 5.1 Compat | Notes |
|---------|---------|--------|--------------------|-------|
| Python | 3.9 | 3.12.10 | ✓ | Core requirement |
| Django | <4.0 | >=5.1,<5.2 | ✓ | Major upgrade |
| DRF | Unknown | >=3.15 | ✓ | Verify latest |
| psycopg2 | Current | psycopg3? | ✓ | May need switch |
| Celery | <6 | >=5.3 | ✓ | Check Django 5.1 |
| django-storages | <1.12 | Latest | ✓ | Remove pin |

### Rollback Commands Quick Reference

```bash
# Emergency rollback to start
git checkout pre-dependency-upgrade
git branch -D feature/dependency-upgrade  # if needed
git checkout -b feature/dependency-upgrade-retry

# Phase-specific rollbacks
git checkout post-python-upgrade      # After Phase 1
git checkout post-database-upgrade    # After Phase 2
git checkout post-django-upgrade      # After Phase 3
git checkout post-dependency-ecosystem # After Phase 4
git checkout post-development-tools   # After Phase 5
git checkout post-workflow-testing    # After Phase 6
```

### Common Issues & Solutions

#### Django 5.1 Breaking Changes
```python
# Issue: Admin template changes
# Solution: Update custom admin templates to use new HTML structure

# Issue: Model.save() positional args deprecated
# Solution: Use keyword arguments only
instance.save(update_fields=['field1'])  # Not: instance.save(['field1'])

# Issue: Template filter changes
# Solution: Review custom template filters for HTML parser updates
```

#### Database Issues
```python
# Issue: PostgreSQL version too old
# Solution: Upgrade PostgreSQL to 13+ before Django upgrade

# Issue: psycopg2 compatibility
# Solution: Test psycopg3 if issues arise
pip install psycopg[binary]>=3.1
```

#### Package Conflicts
```bash
# Issue: Version conflicts during pip install
# Solution: Use pip-compile resolution
pip-compile requirements/in/base.in --upgrade

# Issue: Package not yet Django 5.1 compatible
# Solution: Find alternative or pin to compatible version temporarily
```

### Validation Checklist

#### Phase 1 ✓ Python 3.12 Infrastructure
- [ ] `python --version` shows 3.12.x
- [ ] Container builds without errors
- [ ] Basic imports work (`import django`)
- [ ] CI workflow passes

#### Phase 2 ✓ Database Compatibility
- [ ] PostgreSQL connection successful
- [ ] Redis connection successful
- [ ] Basic queries execute
- [ ] Migration planning works

#### Phase 3 ✓ Django 5.1 Core
- [ ] `python manage.py check` passes
- [ ] Admin interface loads
- [ ] Basic views render
- [ ] Migration creates/applies successfully

#### Phase 4 ✓ Dependency Ecosystem
- [ ] All packages install cleanly
- [ ] No version conflicts
- [ ] API endpoints respond
- [ ] Background tasks can be queued

#### Phase 5 ✓ Development Tools
- [ ] Linting passes (or issues documented)
- [ ] Type checking works
- [ ] Tests run successfully
- [ ] CI/CD pipeline functional

#### Phase 6 ✓ Critical Workflows
- [ ] Game data ingestion complete
- [ ] Admin CRUD operations work
- [ ] API authentication functional
- [ ] Celery tasks execute

#### Phase 7 ✓ Security & Cleanup
- [ ] Dependabot alerts reduced significantly
- [ ] Performance within acceptable range
- [ ] Documentation updated
- [ ] Ready for production

### Emergency Contacts & Resources

- **Django 5.1 Release Notes:** https://docs.djangoproject.com/en/5.1/releases/5.1/
- **Python 3.12 Changes:** https://docs.python.org/3/whatsnew/3.12.html
- **Upgrade Guide:** `docs/modernization/PYTHON312_DJANGO51_UPGRADE_PLAN.md`
- **Issue Tracking:** `docs/modernization/MODERNIZATION_TRACKING.md`
