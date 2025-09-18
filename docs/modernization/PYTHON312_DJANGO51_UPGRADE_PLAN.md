# Python 3.12 + Django 5.1 Upgrade Plan
## Comprehensive Modernization Strategy

**Target:** Python 3.12.10 + Django 5.1.x + Debian Bookworm
**Branch:** `feature/dependency-upgrade`
**Rollback Tag:** `pre-dependency-upgrade`
**Risk Level:** High (major version jumps)
**Timeline:** Phased approach with validation at each step

---

## Overview & Rationale

This upgrade addresses multiple modernization goals simultaneously:
- **Security:** Resolves 134 Dependabot vulnerabilities (10 critical)
- **Future-proofing:** Python 3.12 supported until 2028, Django 5.1 until ~2026
- **Performance:** Python 3.12 optimizations, Django 5.1 improvements
- **Tooling:** Enables latest Ruff, mypy, uv features
- **Infrastructure:** Modern Debian Bookworm base

## Pre-Flight Analysis

### Current State
- Python 3.9.x on Debian Buster (EOL)
- Django 3.2.x (approaching EOL)
- PostgreSQL backend (version TBD)
- 134 security vulnerabilities
- Requirements managed via pip-compile

### Target State
- Python 3.12.10 on Debian Bookworm
- Django 5.1.x (latest stable)
- Modern dependency management
- Zero critical vulnerabilities
- Enhanced developer experience

---

## Phase 1: Infrastructure Foundation
**Scope:** Core system upgrade before touching Django
**Risk:** Medium (container rebuilds, CI changes)
**Rollback:** `git checkout pre-dependency-upgrade`

### 1.1 Python & Base OS Upgrade
```dockerfile
# Update docker/django/Dockerfile
FROM python:3.12-slim-bookworm AS base
# Remove Buster EOL fixes
# Update python lib paths: /usr/local/lib/python3.12/
```

**Why python:3.12-slim-bookworm?**
- **Performance**: Python 3.12 optimizations, supported until 2028
- **Size**: ~150MB vs ~1GB (full image), faster builds/deploys
- **Security**: Minimal attack surface, fewer packages to patch
- **Modernity**: Debian Bookworm (active support), no EOL workarounds
- **Future-proof**: Easy upgrade path to 3.13, modern tooling support

### 1.2 System Package Updates
```bash
# Verify these packages exist in Bookworm
libpq-dev gettext nodejs npm git
python3-mpltoolkits.basemap python3-pillow lsb-release
```

### 1.3 CI/CD Updates
```yaml
# .github/workflows/ci.yml
# Update any Python version references
# Test container builds with new base
```

### 1.4 Validation Steps
- [ ] Local `docker build` succeeds
- [ ] CI/CD workflow passes
- [ ] Dev container starts
- [ ] Basic Python functionality works

**Exit Criteria:** Clean container builds, no Python import errors
**Tag:** `post-python-upgrade`

---

## Phase 2: Database Compatibility
**Scope:** Ensure database stack works with Python 3.12
**Risk:** Medium (connection issues, driver problems, dependency conflicts)
**Rollback:** `git checkout post-python-upgrade`

### 2.1 Critical Issue Identified: Dependency Compatibility
**DISCOVERED:** Docker build failing due to Python 3.12 incompatibilities:
- `gevent==21.12.0` build failures (greenlet compilation errors)
- `django<4.0` constraint blocks modern ecosystem
- `steam[client]` package dependencies need review

### 2.2 Container-First Resolution Strategy
**IMPORTANT:** All Python operations must occur within Docker containers to avoid host pollution.

```bash
# ✅ SAFE - Container operations only
docker-compose run --rm django pip-compile requirements/in/base.in --upgrade
docker-compose run --rm django python manage.py migrate
docker-compose run --rm django python manage.py test

# ❌ UNSAFE - Host operations (NEVER run these)
python manage.py migrate  # Would affect Windows host Python
pip install -r requirements.txt  # Would pollute host environment
```

### 2.3 Dependency Resolution Steps
1. **Update base requirements** for Python 3.12 compatibility:
   ```bash
   # requirements/in/base.in changes needed:
   django>=4.0,<4.1  # Intermediate step, then upgrade to 5.1
   # gevent will be updated via pip-compile resolution
   ```

2. **Test Docker build** with updated dependencies
3. **Verify database connectivity** using container-based connections

### 2.4 Database Driver Updates
```bash
# Check current psycopg2 version compatibility
# May need to update or switch to psycopg3
psycopg2 --no-binary psycopg2  # Current
# vs
psycopg[binary]>=3.1  # For Django 5.1 features
```

### 2.5 Database Version Verification
- [ ] PostgreSQL version ≥ 13 (Django 5.1 requirement)
- [ ] Connection pooling compatibility
- [ ] Transaction isolation levels

### 2.3 Redis & Celery Connectivity
- [ ] Redis connections work
- [ ] Celery can connect to broker
- [ ] Background task execution

**Exit Criteria:** All database connections functional
**Tag:** `post-database-upgrade`

---

## Phase 3: Django 5.1 Core Upgrade
**Scope:** Major Django upgrade with breaking changes
**Risk:** High (API changes, admin changes, template changes)
**Rollback:** `git checkout post-database-upgrade`

### 3.1 Django Version Update
```python
# requirements/in/base.in
django>=5.1,<5.2  # Was: django<4.0
```

### 3.2 Breaking Changes to Address

#### Admin Interface Changes
```python
# Admin fieldsets now use <details>/<summary>
# Navigation uses <nav> tags
# Footer uses <footer> tags
# May need custom admin template updates
```

#### Template System Updates
```django
{# New {% querystring %} template tag available #}
{# HTML parser changes in truncation filters #}
{# Update any custom template tags/filters #}
```

#### Model & QuerySet Changes
```python
# Model.save() - positional args deprecated
# Model.refresh_from_db() - new from_queryset arg
# QuerySet.explain() - new generic_plan option
# Review all model usage patterns
```

### 3.3 Settings Updates
```python
# config/settings/base.py
# Remove deprecated settings
# Add new Django 5.1 features as needed
# Update middleware if using auth changes
```

### 3.4 Migration Strategy
```bash
# Check for migration issues
python manage.py makemigrations --dry-run
python manage.py migrate --plan
# Test with empty database
# Test with production data backup
```

**Exit Criteria:** Django 5.1 runs, admin accessible, basic views work
**Tag:** `post-django-upgrade`

---

## Phase 4: Dependency Ecosystem
**Scope:** Update all Django-related packages
**Risk:** Medium (version conflicts, API changes)
**Rollback:** `git checkout post-django-upgrade`

### 4.1 Django REST Framework
```python
# Current: djangorestframework (unknown version)
# Target: djangorestframework>=3.15
# Check for DRF + Django 5.1 compatibility
# Test API endpoints still work
```

### 4.2 Django Extensions
```python
# Update all django-* packages:
django-celery-results
django-cors-headers
django-crispy-forms
django-environ
django-filter
django-json-widget
django-model-utils
django-polymorphic
django-prometheus
django-redis
django-rest-fuzzysearch
django-robots
django-storages[azure]  # Remove <1.12 pin
```

### 4.3 Celery & Background Tasks
```python
# Current: celery<6
# Target: celery>=5.3 (Django 5.1 compatible)
# Test all background tasks
# Verify Huey still works (if keeping)
```

### 4.4 Azure & Storage
```python
# azure-identity, azure-mgmt-cdn updates
# django-storages compatibility
# Test file uploads/downloads
```

**Exit Criteria:** All major packages updated, APIs functional
**Tag:** `post-dependency-ecosystem`

---

## Phase 5: Development Tools
**Scope:** Linters, type checkers, testing tools
**Risk:** Low (mostly tooling)
**Rollback:** `git checkout post-dependency-ecosystem`

### 5.1 Linting & Formatting
```python
# Update to latest versions:
black>=24.0
ruff>=0.6.0  # Enhanced features
mypy>=1.11
django-stubs>=5.1  # Critical for Django 5.1
```

### 5.2 Testing Tools
```python
# Update testing stack:
pytest
coverage[toml]
django-coverage-plugin
factory-boy
django-extensions
```

### 5.3 pyproject.toml Migration
```toml
# Move configurations from setup.cfg
[tool.black]
[tool.ruff]
[tool.mypy]
[tool.coverage.run]
# Keep setup.cfg until fully validated
```

**Exit Criteria:** All linting passes, type checking clean
**Tag:** `post-development-tools`

---

## Phase 6: Critical Workflow Testing
**Scope:** Boundlexx-specific functionality
**Risk:** High (game data, business logic)
**Rollback:** `git checkout post-development-tools`

### 6.1 Game Data Ingestion
```bash
# Test full workflow:
python manage.py ingest_game_data 249.4.0
python manage.py create_game_objects --core --english-only
python manage.py create_game_objects --skill
python manage.py create_game_objects --recipe
```

### 6.2 Admin Interface Testing
- [ ] Login/logout works
- [ ] All admin models accessible
- [ ] Filtering, searching functional
- [ ] Bulk actions work
- [ ] Custom admin views operational

### 6.3 API Endpoint Testing
- [ ] All API endpoints respond
- [ ] Authentication works
- [ ] Pagination functional
- [ ] Data serialization correct

### 6.4 Background Task Testing
- [ ] Celery workers start
- [ ] Tasks execute successfully
- [ ] Scheduled tasks run
- [ ] Error handling works

**Exit Criteria:** All core workflows pass end-to-end tests
**Tag:** `post-workflow-testing`

---

## Phase 7: Security & Cleanup
**Scope:** Final validation and cleanup
**Risk:** Low (cosmetic changes)
**Rollback:** `git checkout post-workflow-testing`

### 7.1 Security Validation
- [ ] Run `pip audit` - vulnerabilities resolved
- [ ] Check Dependabot alerts - should be minimal
- [ ] Security headers still functional
- [ ] Authentication/authorization unchanged

### 7.2 Performance Testing
```bash
# Basic performance checks:
python manage.py check --deploy
python manage.py migrate --plan  # Should be clean
# Load testing on key endpoints
```

### 7.3 Documentation Updates
- [ ] Update README.rst with new requirements
- [ ] Update MODERNIZATION_TRACKING.md
- [ ] Update developer setup instructions
- [ ] Update deployment notes

### 7.4 Code Cleanup
```python
# Remove deprecated code usage
# Clean up any compatibility shims
# Update docstrings with new features
# Remove old version pins
```

**Exit Criteria:** Production-ready state
**Tag:** `post-security-cleanup`

---

## Upstream Issues Analysis & Integration

### Issues Directly Addressed by This Plan

| Issue | Status | Integration Strategy |
|-------|---------|---------------------|
| **#21** | ✅ **RESOLVED** | Container builds working with GHCR |
| **#22** | ✅ **EXCEEDED** | Python 3.10+ → Our target: 3.12.10 |
| **#23** | ✅ **EXCEEDED** | Django 4.2+ → Our target: 5.1.x |
| **#30** | 🎯 **ALIGNED** | Requirements → pyproject.toml + uv (Phase 5) |
| **#34** | ✅ **COMPLETED** | GitHub Actions updated with modern workflows |

### Issues Requiring Separate Implementation
| Issue | Priority | Recommendation |
|-------|---------|----------------|
| **#24** | 🔄 **ACTIVE** | Steam Login (Node.js) - independent of upgrade |
| **#25** | 🔧 **SIMPLE** | Container naming (kebab-case) - post-upgrade |
| **#26** | 📝 **CONFIG** | setup.cfg → pyproject.toml (Phase 5) |
| **#27** | 🗑️ **CLEANUP** | Remove Huey (post-Phase 7) |
| **#28** | 📊 **QUALITY** | Code coverage 85%+ (ongoing) |
| **#29** | 🔍 **LINTING** | Ruff + mypy (Phase 5) |
| **#31** | ⚡ **FUTURE** | Celery → TaskIQ (major change, separate project) |
| **#32** | 🚀 **FUTURE** | DRF → Django Ninja (API overhaul, separate project) |
| **#33** | 🏗️ **STRUCTURE** | Project structure (references ark-operator) |

### Implementation Sequencing
1. **✅ Complete current upgrade plan** (Python 3.12 + Django 5.1)
2. **📝 Configuration modernization** (#26, #29, #30) - integrate with Phase 5
3. **🗑️ Technical debt cleanup** (#27, #28) - post-upgrade activities
4. **🚀 Major architecture changes** (#31, #32) - separate planning cycles

### Synergies & Conflicts
- **✅ No conflicts:** Our upgrade plan complements all upstream priorities
- **📈 Synergistic:** Modern linting (#29) + pyproject.toml (#30) align with our Phase 5
- **🎯 Strategic:** Complete this upgrade first → solid foundation for future changes

---

## Risk Mitigation Strategies

### Backup & Rollback Plan
1. **Git Tags:** At each phase boundary
2. **Database Backup:** Before any migration testing
3. **Container Images:** Tag working images
4. **Requirements Backup:** Keep old files until validated

### Issue Anticipation

#### High-Probability Issues
1. **psycopg2 → psycopg3:** Driver compatibility changes
2. **Admin Templates:** Custom templates may break
3. **DRF Compatibility:** API serialization changes
4. **Migration Conflicts:** Schema changes

#### Mitigation Strategies
```bash
# Test migrations on copy of production data
# Keep old psycopg2 as fallback
# Run comprehensive test suite at each phase
```

### Testing Strategy
1. **Unit Tests:** Must pass at each phase
2. **Integration Tests:** Focus on game data workflows
3. **End-to-End Tests:** Admin + API + background tasks
4. **Performance Tests:** No significant regression

---

## Success Metrics

### Technical Goals
- [ ] Zero critical Dependabot vulnerabilities
- [ ] All tests passing
- [ ] CI/CD pipeline functional
- [ ] Performance within 10% of baseline

### Business Goals
- [ ] Game data ingestion works
- [ ] Admin interface functional
- [ ] API responses correct
- [ ] Background tasks operational

### Modernization Goals
- [ ] Python 3.12 active
- [ ] Django 5.1 operational
- [ ] Modern tooling integrated
- [ ] Documentation updated

---

## Post-Completion Actions

1. **Merge Strategy:** Squash commits or keep detailed history?
2. **Upstream PR:** Prepare changes for upstream contribution
3. **Deployment Plan:** Staging → Production rollout
4. **Monitoring:** Enhanced logging during initial deployment
5. **Team Training:** New features and workflow changes

---

*This plan provides a structured, reversible approach to a major modernization effort. Each phase builds on the previous, with clear validation criteria and rollback points.*
