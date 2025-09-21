# How to Use the New Documentation System

## 🎯 Primary Documentation: Master Manual

**Always start here**: [Master Manual](docs/manual/index.md)

The Master Manual is now the **single source of truth** for all Boundlexx documentation. It replaces all scattered documentation with a comprehensive, well-organized guide.

## 📚 Master Manual Structure

### For New Developers
- **[Quick Start Guide](docs/manual/getting-started/quick-start.md)** - Get running in 5 minutes
- **[Complete Installation](docs/manual/getting-started/installation.md)** - Detailed setup for all scenarios
- **[Environment Setup](docs/manual/getting-started/environment-setup.md)** - Development, test, production environments

### For Daily Development
- **[Development Workflows](docs/manual/workflows/development.md)** - VS Code tasks, testing, debugging
- **[Data Ingestion](docs/manual/workflows/data-ingestion.md)** - Game data import process
- **[Testing](docs/manual/workflows/testing.md)** - Running tests and validation

### For System Understanding
- **[Architecture Overview](docs/manual/architecture/overview.md)** - System design and components
- **[Data Flow](docs/manual/architecture/data-flow.md)** - How game data becomes APIs
- **[Security Model](docs/manual/architecture/security.md)** - Authentication and rate limiting

### For Migration & Upgrades
- **[Modernization Roadmap](docs/manual/migration/roadmap.md)** - Current Phase 3 → Phase 10 plan
- **[Django Upgrade](docs/manual/migration/django-upgrade.md)** - LTS upgrade process
- **[Breaking Changes](docs/manual/migration/breaking-changes.md)** - Version compatibility

### For Reference
- **[API Documentation](docs/manual/reference/api.md)** - Complete REST API reference
- **[Configuration](docs/manual/reference/configuration.md)** - Environment variables and settings
- **[Troubleshooting](docs/manual/reference/troubleshooting.md)** - Common issues and solutions

## 🔄 How to Use Different Documentation Types

### 1. Starting a New Task
1. **Check Master Manual first** - [workflows section](docs/manual/workflows/)
2. **Use VS Code Tasks** - documented in [Development Workflows](docs/manual/workflows/development.md)
3. **Reference troubleshooting** - if you encounter issues

### 2. Setting Up Environment
1. **Quick setup**: [Quick Start Guide](docs/manual/getting-started/quick-start.md) (5 minutes)
2. **Complete setup**: [Installation Guide](docs/manual/getting-started/installation.md)
3. **Advanced scenarios**: [Environment Setup](docs/manual/getting-started/environment-setup.md)

### 3. Understanding the System
1. **High-level overview**: [Architecture Overview](docs/manual/architecture/overview.md)
2. **Specific components**: Browse [Architecture section](docs/manual/architecture/)
3. **API usage**: [API Documentation](docs/manual/reference/api.md)

### 4. Migration Work
1. **Current status**: [Migration Roadmap](docs/manual/migration/roadmap.md)
2. **Active tracking**: `docs/modernization/MODERNIZATION_TRACKING.md` (still maintained)
3. **Breaking changes**: [Breaking Changes](docs/manual/migration/breaking-changes.md)

## 📋 What Documentation to Use When

| Task | Use This Documentation | Don't Use |
|------|----------------------|-----------|
| **New developer setup** | [Quick Start Guide](docs/manual/getting-started/quick-start.md) | README.rst (now just a pointer) |
| **Daily development** | [Development Workflows](docs/manual/workflows/development.md) | Scattered VS Code task docs |
| **Game data ingestion** | [Data Workflows](docs/manual/workflows/data-ingestion.md) | Copilot instructions (AI-only) |
| **Container setup** | [Environment Setup](docs/manual/getting-started/environment-setup.md) | Legacy setup docs |
| **API reference** | [API Documentation](docs/manual/reference/api.md) | Old API docs |
| **Troubleshooting** | [Troubleshooting Guide](docs/manual/reference/troubleshooting.md) | Scattered issue docs |
| **Migration planning** | [Migration Roadmap](docs/manual/migration/roadmap.md) | Individual modernization files |

## 🚫 What NOT to Use

### Obsolete Documentation (Now in /docs/legacy/)
- Old README.rst instructions (now just points to manual)
- `docs/modernization/ENVIRONMENT_SETUP.md` (superseded by manual)
- Scattered setup guides (consolidated into manual)

### AI-Only Documentation
- `.github/copilot-instructions.md` - For GitHub Copilot AI only, not humans
- Template examples - Research/reference only

### Active Technical Tracking (Still Valid)
- `docs/modernization/MODERNIZATION_TRACKING.md` - Active change log
- `docs/modernization/GIT_WORKFLOW.md` - Git procedures

## 🔍 Finding Information

### Search Strategy
1. **Start with Manual index** - [Master Manual](docs/manual/index.md)
2. **Use browser search** - Ctrl+F in manual pages
3. **Check troubleshooting** - [Common issues](docs/manual/reference/troubleshooting.md)
4. **Look in reference** - [Reference section](docs/manual/reference/)

### Common Questions
- **"How do I set up the project?"** → [Quick Start Guide](docs/manual/getting-started/quick-start.md)
- **"How do I run tests?"** → [Development Workflows](docs/manual/workflows/development.md)
- **"How do I ingest game data?"** → [Data Workflows](docs/manual/workflows/data-ingestion.md)
- **"What's the current migration status?"** → [Migration Roadmap](docs/manual/migration/roadmap.md)
- **"How do I configure authentication?"** → [Security Model](docs/manual/architecture/security.md)

## 🛠️ Building the Documentation

### Local Development
```bash
# Install Sphinx dependencies
pip install sphinx sphinx-rtd-theme myst-parser sphinx-copybutton sphinx-design

# Build the manual
cd docs/manual
sphinx-build . _build/html

# Live preview with auto-reload
sphinx-autobuild . _build/html --open-browser
```

### VS Code Integration
Use VS Code Task: "Docs: Build Manual" or "Docs: Live Preview"

## 📝 Contributing to Documentation

### When to Update the Manual
- **Adding new workflows** → Add to appropriate workflow section
- **Changing setup procedures** → Update getting-started section
- **Adding features** → Update architecture and reference sections
- **Migration progress** → Update migration roadmap

### How to Update
1. **Edit the relevant manual section** - don't create new scattered docs
2. **Test all instructions** - ensure they work
3. **Update cross-references** - maintain internal links
4. **Build and review** - check formatting and navigation

## 🎯 Success Indicators

**You're using the documentation correctly when:**
- ✅ You find all information you need in the Master Manual
- ✅ You don't need to search through multiple files
- ✅ Setup and workflow instructions work correctly
- ✅ You understand the system architecture
- ✅ Troubleshooting guides solve your issues

**If you find yourself:**
- ❌ Looking through legacy docs in `/docs/legacy/`
- ❌ Reading AI-only copilot instructions for human guidance
- ❌ Searching through scattered modernization files
- ❌ Unable to find clear workflow instructions

**Then**: Check the [Master Manual](docs/manual/index.md) first, and if information is missing, contribute to improve it.

---

📚 **Remember: The Master Manual is your single source of truth. Everything else is either legacy (archived) or AI-specific (copilot instructions).**
