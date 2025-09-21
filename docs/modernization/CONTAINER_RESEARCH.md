# Boundlexx Naming Convention & Environment Detection Research

**Source**: This research was conducted in the test chat environment (`boundlexx-yatesjj-test`) and represents findings from extensive analysis of upstream repositories and naming convention patterns. The dev chat should analyze these findings and implement the recommended changes in the development environment.

## Executive Summary

Through comprehensive analysis of the AngellusMortis/boundlexx upstream repository and ARK operator patterns, significant issues with naming conventions and environment detection have been identified. The current boundlexx-yatesjj fork has inconsistent naming patterns that create confusion across chat sessions and deviate from modern containerization best practices. This document provides detailed findings and actionable recommendations for standardization.

## Research Methodology

### Repositories Analyzed
1. **AngellusMortis/boundlexx** (upstream) - Standard Docker/Django patterns
2. **AngellusMortis/ark-operator** - Modern Kubernetes-native patterns and tooling
3. **Current boundlexx-yatesjj implementation** - Hybrid approach with isolation benefits

### Analysis Scope
- Container naming conventions
- Service orchestration patterns
- Environment detection mechanisms
- Cross-chat session context preservation
- Modern tooling integration (uv, pyproject.toml, Kubernetes labels)

## Key Findings

### 1. Upstream Repository Patterns (AngellusMortis/boundlexx)

**Service Naming**: Standard Docker Compose patterns
- Services: `django`, `postgres`, `redis`, `celery workers`
- Binary scripts: `start-huey-consumer`, `start-huey-scheduler`, `start-celerybeat`, `start-celeryworker`
- Environment variables: `CELERY_WORKER_QUEUES`, `CELERY_WORKER_NAME`, `HUEY_WORKER_COUNT`

**Container Architecture**: Minimal Docker setup with basic patterns
- Simple service definitions
- Standard Docker Compose networking
- Production/dev stage differentiation in Dockerfile
- Azure integration for storage and CDN

### 2. ARK Operator Modern Patterns

**Kubernetes-Native Approach**: Sophisticated container orchestration
```yaml
# Modern labeling standards
labels:
  app.kubernetes.io/name: ark-operator
  app.kubernetes.io/component: service-account
  app.kubernetes.io/part-of: {{ instance_name }}
```

**Resource Naming Convention**:
- Pattern: `{{ instance_name }}-{{ component }}`
- Examples: `ark-cluster-secrets`, `ark-data`, `ark-server-a`
- Services: `{{ instance_name }}` (game), `{{ instance_name }}-rcon`

**Pod/Container Naming**:
- Format: `{{ instance_name }}-{{ map_slug }}`
- Container names: Simple descriptive (`ark`, `job`, `init-perms`)

**Modern Technology Stack**:
- **uv** for dependency management (`uv==0.5.29`)
- **pyproject.toml** structure for Python projects
- **Ruff** for fast Python linting
- **Python 3.12** with async patterns
- **Kubernetes-first** design philosophy

### 3. Current boundlexx-yatesjj Issues

**Naming Inconsistencies** (Fixed in test chat):
- Template inconsistencies in `setup_containers.py`
- Mixed network naming patterns (`boundlexx-test-network` vs `test-app-network`)
- Inconsistent container naming schemes

**Environment Detection Limitations**:
- Simple folder-based detection only
- No cross-chat session context preservation
- Missing workspace identification metadata
- Basic environment type inference

**Advantages of Current Approach**:
- **Superior isolation**: Folder-based container separation
- **Port conflict prevention**: Automatic port allocation (dev: 28000, test: 28001)
- **Environment separation**: Complete isolation between dev/test instances

## Comparative Analysis

| **Aspect** | **AngellusMortis/boundlexx** | **ARK Operator** | **Current boundlexx-yatesjj** | **Recommended** |
|------------|------------------------------|------------------|--------------------------------|-----------------|
| **Service Names** | `django`, `postgres`, `redis` | `{{ instance_name }}`, `{{ instance_name }}-rcon` | `django-1`, `postgres-1` | `boundlexx-django`, `boundlexx-postgres` |
| **Container Names** | Standard Docker Compose | `{{ instance_name }}-{{ component }}` | `test-django-1` (folder-prefixed) | Keep folder-prefix for isolation |
| **Network Names** | Default compose networks | Kubernetes services | `test-app-network` | `{{ folder }}-boundlexx-network` |
| **Labels** | Basic | Kubernetes standard | None | Implement Kubernetes labels |
| **Environment Detection** | None | Kubernetes metadata | Folder-based only | Multi-method detection |
| **Tooling** | pip-compile | uv, pyproject.toml, Ruff | pip-compile | Migrate to modern stack |

## Recommended Unified Naming Scheme

### Core Principles
1. **Kubernetes-Inspired**: Use modern labeling and metadata patterns
2. **Environment Isolation**: Maintain folder-based separation advantage
3. **Upstream Alignment**: Stay compatible with AngellusMortis/boundlexx patterns
4. **Future-Proof**: Ready for ARK operator-style modernization

### Service Naming Pattern
```yaml
services:
  boundlexx-django:     # Descriptive, upstream-aligned
  boundlexx-postgres:   # Clear component identification
  boundlexx-redis:      # Consistent with Django ecosystem
  boundlexx-celery:     # Task queue service
  boundlexx-huey:       # Alternative task queue
```

### Container Naming Pattern (Docker Compose auto-generates)
```yaml
containers:
  {{ folder_name }}-boundlexx-django-1     # Isolation + service + instance
  {{ folder_name }}-boundlexx-postgres-1   # Environment separation maintained
```

### Network Naming Pattern
```yaml
networks:
  {{ folder_name }}-boundlexx-network      # Clear ownership and scope
```

### Volume Naming Pattern
```yaml
volumes:
  {{ folder_name }}-postgres-data          # Environment + component + purpose
  {{ folder_name }}-redis-data
```

### Labels (Kubernetes-inspired)
```yaml
labels:
  app.kubernetes.io/name: boundlexx
  app.kubernetes.io/component: django      # or postgres, redis, etc.
  app.kubernetes.io/part-of: boundlexx
  app.kubernetes.io/instance: "{{ folder_name }}"
  app.kubernetes.io/environment: "{{ env_type }}"  # dev, test, production
```

## Unified Environment Detection System

### Multi-Method Context Detection
```python
class BoundlexxEnvironmentDetector:
    """Unified environment detection for cross-chat session consistency."""
    
    @staticmethod
    def detect_environment():
        """Comprehensive environment detection using multiple methods."""
        context = {
            'workspace_path': Path.cwd(),
            'folder_name': Path.cwd().name,
            'environment_type': None,
            'port_base': None,
            'network_name': None,
            'service_prefix': None
        }
        
        # Method 1: Folder name patterns
        folder_name = context['folder_name'].lower()
        if 'test' in folder_name:
            context['environment_type'] = 'test'
            context['port_base'] = 28001
        else:
            context['environment_type'] = 'dev'
            context['port_base'] = 28000
            
        # Method 2: Environment files detection
        env_files = {
            '.test.env': 'test',
            '.dev.env': 'dev',
            '.local.env': 'dev'  # Default to dev
        }
        
        for env_file, env_type in env_files.items():
            if (context['workspace_path'] / env_file).exists():
                context['environment_type'] = env_type
                break
                
        # Method 3: Git branch detection
        try:
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  capture_output=True, text=True, check=True)
            branch = result.stdout.strip()
            if 'test' in branch or 'testing' in branch:
                context['environment_type'] = 'test'
        except:
            pass
            
        # Set derived values
        context['network_name'] = f"{context['folder_name']}-boundlexx-network"
        context['service_prefix'] = 'boundlexx'
        
        return context
```

### Context Persistence
```python
def save_environment_context(context):
    """Save detected context for cross-session consistency."""
    context_file = Path('.boundlexx-context.json')
    with open(context_file, 'w') as f:
        json.dump(context, f, indent=2, default=str)

def load_environment_context():
    """Load saved context or detect fresh."""
    context_file = Path('.boundlexx-context.json')
    if context_file.exists():
        with open(context_file, 'r') as f:
            return json.load(f)
    return BoundlexxEnvironmentDetector.detect_environment()
```

## Implementation Roadmap

### Phase 1: Immediate Fixes ✅ (Completed in Test Chat)
- **Template inconsistencies** in `setup_containers.py` fixed
- **Network naming standardization** implemented
- **Container naming consistency** established

### Phase 2: Naming Standardization (Next Steps for Dev Chat)
1. **Update service names** in docker-compose templates:
   ```yaml
   # From: django, postgres, redis
   # To: boundlexx-django, boundlexx-postgres, boundlexx-redis
   ```

2. **Implement Kubernetes-style labels**:
   ```yaml
   labels:
     app.kubernetes.io/name: boundlexx
     app.kubernetes.io/component: ${service}
     app.kubernetes.io/part-of: boundlexx
   ```

3. **Standardize network naming**:
   ```yaml
   # Pattern: {{ folder_name }}-boundlexx-network
   networks:
     boundlexx-yatesjj-boundlexx-network:  # For dev environment
   ```

### Phase 3: Environment Detection Enhancement
1. **Implement multi-method detection** system in `setup_containers.py`
2. **Add context persistence** (`.boundlexx-context.json`)
3. **Create validation** and consistency checks
4. **Update all scripts** to use unified detection

### Phase 4: Documentation & Training
1. **Update all documentation** with new patterns
2. **Create migration guide** for existing environments
3. **Establish naming convention** enforcement in CI/CD
4. **Train team** on new patterns

## Specific Recommendations for Development Environment

### Current State Analysis
- **Environment**: Development (`boundlexx-yatesjj`)
- **Port**: 28000 (standard development)
- **Current naming**: Mixed patterns with some inconsistencies

### Recommended Changes for Dev Chat Implementation

1. **Service Naming Update**:
   ```yaml
   # Current:
   services:
     django: &django
       container_name: django-1
   
   # Recommended:
   services:
     boundlexx-django: &django
       container_name: boundlexx-yatesjj-boundlexx-django-1
   ```

2. **Network Naming Consistency**:
   ```yaml
   # Current:
   networks:
     default:
   
   # Recommended:
   networks:
     boundlexx-yatesjj-boundlexx-network:
   ```

3. **Add Modern Labels**:
   ```yaml
   services:
     boundlexx-django:
       labels:
         app.kubernetes.io/name: boundlexx
         app.kubernetes.io/component: django
         app.kubernetes.io/part-of: boundlexx
         app.kubernetes.io/instance: boundlexx-yatesjj
         app.kubernetes.io/environment: dev
   ```

## Migration Strategy

### Backward Compatibility Approach
1. **Phase rollout** - implement changes gradually to avoid breaking existing setups
2. **Alias support** - maintain old names during transition period
3. **Validation tools** - create scripts to verify naming consistency
4. **Documentation** - provide clear migration paths for all environments

### Risk Mitigation
- **Test in isolation** first (test environment proves this approach works)
- **Rollback procedures** documented for each phase
- **Incremental changes** rather than wholesale replacement
- **Validation at each step** to ensure no broken configurations

## Strategic Value Proposition

This standardization effort positions the boundlexx-yatesjj fork as:

1. **More Sophisticated** than upstream:
   - Better environment isolation
   - Modern container patterns
   - Automated port conflict prevention

2. **Future-Ready** for modernization:
   - Kubernetes-compatible naming
   - ARK operator pattern alignment
   - Modern Python tooling preparation (uv, pyproject.toml)

3. **Consistent** across environments:
   - Unified naming conventions
   - Cross-chat session context preservation
   - Predictable container behavior

4. **Maintainable** with clear conventions:
   - Documented patterns
   - Automated environment detection
   - Validation and consistency checking

## Next Steps for Dev Chat

1. **Review this research document** thoroughly
2. **Analyze current development environment** naming patterns
3. **Implement Phase 2 changes** (service naming standardization)
4. **Update `setup_containers.py`** with unified environment detection
5. **Test migration** in development environment
6. **Document changes** in modernization tracking files
7. **Plan rollout** to other environments

## Files Requiring Updates

### Primary Implementation Files
- `setup_containers.py` - Add environment detection and new naming patterns
- `docker-compose.yml` - Update service names and add labels
- `docker-compose.override.example.yml` - Template updates
- `.devcontainer/devcontainer.json` - Port and service name updates

### Documentation Files
- `docs/modernization/MODERNIZATION_TRACKING.md` - Log all changes
- `docs/modernization/ENVIRONMENT_SETUP.md` - Update setup instructions
- `README.rst` - Update quick start with new patterns
- `.github/copilot-instructions.md` - Update naming convention guidance

### Configuration Files
- `.local.env` - Environment type indicators
- `.test.env` - Test environment configuration
- `pyproject.toml` - Future modernization preparation

This research provides a comprehensive foundation for implementing consistent, modern naming conventions that align with industry best practices while maintaining the sophisticated environment isolation advantages of the current boundlexx-yatesjj implementation.