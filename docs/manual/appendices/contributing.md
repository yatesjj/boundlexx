# Contributing to Boundlexx Documentation

**STRICT GOVERNANCE STANDARDS FOR ALL CONTRIBUTORS**

## 🚨 Critical Rules - NO EXCEPTIONS

### **Documentation Creation Rules**

#### ✅ **ALLOWED: Master Manual Hierarchy Only**
```
docs/manual/
├── getting-started/    # Setup, installation, environment
├── workflows/          # Daily development, data ingestion, testing
├── architecture/       # System design, data flow, security
├── migration/          # Upgrades, modernization, breaking changes
├── reference/          # Commands, API, configuration, troubleshooting
└── appendices/         # Historical context, contributing, legacy
```

#### ❌ **FORBIDDEN: Documentation Outside Master Manual**
- **NO** markdown files in root directory
- **NO** scattered documentation in random folders
- **NO** duplicate documentation
- **NO** personal documentation folders

#### ⚠️ **EXCEPTION: Technical Modernization Only**
```
docs/modernization/     # ONLY for active technical tracking
├── MODERNIZATION_TRACKING.md      # Change tracking
├── STEAM_AUTHENTICATION.md        # Production technical guides
├── FORWARD_MIGRATION_GUIDE.md     # Migration compatibility
├── archived_plans/                # Historical research with READMEs
└── archived_research/              # Technical findings with context
```

### **File Creation Rules**

#### **Where Files MUST Go:**

| File Type | Location | Examples | Approval |
|-----------|----------|----------|----------|
| **User Documentation** | `docs/manual/` | Guides, tutorials, references | PR Review |
| **Technical Tracking** | `docs/modernization/` | Research, migration plans | PR Review |
| **Utility Scripts** | `scripts/utilities/` | Data fixes, one-off tools | Code Review |
| **Configuration** | `config/`, `.github/` | Settings, workflows | Code Review |
| **Application Code** | `boundlexx/`, `tests/` | Features, tests | Code Review |

#### **Root Directory - HIGHLY RESTRICTED**
Only these patterns allowed in root:
- `README.md`, `LICENSE`, `CHANGELOG.md`
- `manage.py`, `setup.py`, `pyproject.toml`
- `docker-compose*.yml`, `.env*`
- `setup_containers.py` (our setup script)

**Everything else goes in subdirectories!**

## 🔧 Development Workflow

### **Before Creating ANY File:**

1. **Ask: "Does this belong in Master Manual?"**
   - User-facing? → `docs/manual/`
   - Technical tracking? → `docs/modernization/`
   - Neither? → Proper subdirectory

2. **Check the Master Manual hierarchy**
   - Does appropriate section exist?
   - Should this extend existing documentation?
   - Would this duplicate existing content?

3. **Follow the approval process**
   - Documentation changes require PR review
   - Root directory changes require explicit approval
   - When in doubt, ask in PR description

### **Adding Documentation:**

#### **Step 1: Determine Category**
- **Getting Started**: Setup, installation, environment configuration
- **Workflows**: Daily development tasks, common operations
- **Architecture**: System design, how components work
- **Migration**: Upgrades, breaking changes, modernization
- **Reference**: Commands, API specs, configuration options
- **Appendices**: Historical context, contributing guidelines

#### **Step 2: Check for Existing Content**
- Search Master Manual for related content
- Check if this extends or replaces existing documentation
- Ensure no duplication across categories

#### **Step 3: Follow Naming Conventions**
```
kebab-case-filenames.md
clear-descriptive-names.md
category-specific-prefixes.md  # if needed
```

#### **Step 4: Use Proper Cross-References**
```markdown
# Internal links
[Development Workflows](../workflows/development.md)

# External links with context
[Django Documentation](https://docs.djangoproject.com/en/5.2/)

# Master Manual hierarchy references
See [Reference/Commands](../reference/commands.md) for complete command list.
```

## 🚀 Quality Standards

### **Documentation Requirements:**

1. **Single Source of Truth**: No duplicate information
2. **Industry Standards**: Follow Django, FastAPI, Kubernetes patterns
3. **Forward Compatible**: Consider modernization roadmap
4. **Tested Instructions**: Every procedure must be validated
5. **Clear Navigation**: Proper cross-references and hierarchy

### **Content Standards:**

1. **Complete Examples**: Working code snippets with context
2. **Error Handling**: Common issues and troubleshooting
3. **Environment Specific**: Development vs production differences
4. **Version Specific**: Django 5.2 LTS, Python 3.12 compatibility

## 🔒 Enforcement Mechanisms

### **Automated Checks:**
- **Pre-commit hook**: Prevents documentation sprawl
- **CI/CD validation**: Checks all PRs for governance compliance
- **File pattern matching**: Enforces location rules

### **Manual Review:**
- **PR review required**: All documentation changes
- **Approval required**: Root directory modifications
- **Standards validation**: Quality and hierarchy compliance

## ❌ Common Violations & Fixes

### **Violation: Creating `PROJECT_NOTES.md` in root**
```bash
# ❌ Wrong
echo "# Notes" > PROJECT_NOTES.md

# ✅ Correct
echo "# Development Notes" > docs/manual/workflows/development-notes.md
# Then add to appropriate workflow section
```

### **Violation: Scattered utility documentation**
```bash
# ❌ Wrong
mkdir utils/docs/
echo "# Utility Guide" > utils/docs/README.md

# ✅ Correct
# Add to Master Manual reference section
echo "## Utility Scripts" >> docs/manual/reference/commands.md
```

### **Violation: Personal development guides**
```bash
# ❌ Wrong
mkdir my-setup/
echo "# My Setup Process" > my-setup/README.md

# ✅ Correct
# Improve existing getting started guide
echo "## Alternative Setup" >> docs/manual/getting-started/installation.md
```

## 🎯 Success Metrics

Your contribution is successful when:

1. ✅ **Zero governance violations** in pre-commit check
2. ✅ **No documentation outside Master Manual** hierarchy
3. ✅ **Clear navigation** from Master Manual index
4. ✅ **No duplicate content** across documentation
5. ✅ **Industry-standard quality** following established patterns

## 🆘 Getting Help

- **Unsure about placement?** Open draft PR with question
- **Need new Manual category?** Discuss in issue first
- **Complex documentation?** Reference existing examples
- **Governance questions?** Check modernization tracking docs

## 🔗 References

- [Master Manual Index](../manual/index.md) - Complete documentation hierarchy
- [Modernization Tracking](../modernization/MODERNIZATION_TRACKING.md) - Technical change history
- [Forward Migration Guide](../modernization/FORWARD_MIGRATION_GUIDE.md) - Compatibility requirements

---

**Remember: Our documentation system is our competitive advantage. Protect it with strict governance!**
