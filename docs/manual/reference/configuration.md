# Configuration Reference

Complete reference for all Boundlexx configuration options and environment variables.

## 🔧 Environment Variables

### Required Variables

#### Database Configuration
```bash
# PostgreSQL connection
DATABASE_URL=postgresql://postgres:password@postgres:5432/boundlexx
POSTGRES_DB=boundlexx
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

#### Django Core
```bash
# Security (REQUIRED in production)
SECRET_KEY=your-super-secret-key-here
DEBUG=True  # Set to False in production

# Allowed hosts (comma-separated)
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0

# Site configuration
SITE_ID=1
DJANGO_PORT=28001
```

#### Redis/Caching
```bash
# Redis connection
REDIS_URL=redis://redis:6379/0
CACHE_URL=redis://redis:6379/1
CELERY_BROKER_URL=redis://redis:6379/2
```

### Authentication & API Keys

#### Steam Authentication
```bash
# Steam credentials (for game data ingestion)
STEAM_USERNAMES=steam_user1,steam_user2
STEAM_PASSWORDS=password1,password2
STEAM_WEB_API_KEY=your_steam_api_key  # Optional but recommended
```

#### Boundless Game Authentication
```bash
# Boundless credentials
BOUNDLESS_USERNAMES=boundless_user1,boundless_user2
BOUNDLESS_PASSWORDS=password1,password2
```

#### OAuth Providers
```bash
# Discord OAuth (optional)
DISCORD_CLIENT_ID=your_discord_client_id
DISCORD_CLIENT_SECRET=your_discord_client_secret

# GitHub OAuth (optional)
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# Google OAuth (optional)
GOOGLE_OAUTH2_CLIENT_ID=your_google_client_id
GOOGLE_OAUTH2_CLIENT_SECRET=your_google_client_secret
```

### Optional Configuration

#### Email Settings
```bash
# Email backend
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

#### Logging & Monitoring
```bash
# Sentry error tracking (optional)
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id

# Log level
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

#### Performance & Scaling
```bash
# Worker configuration
WEB_CONCURRENCY=4
CELERY_WORKER_CONCURRENCY=2
HUEY_WORKER_COUNT=2

# Database connection pooling
DATABASE_POOL_SIZE=10
DATABASE_MAX_CONNECTIONS=20
```

### Development-Specific

#### Debug Tools
```bash
# Django Debug Toolbar
ENABLE_DEBUG_TOOLBAR=True

# SQL query logging
LOG_SQL_QUERIES=True

# Development overrides
INTERNAL_IPS=127.0.0.1,localhost
```

#### Testing Configuration
```bash
# Test database (automatically created)
TEST_DATABASE_NAME=test_boundlexx

# Fast testing (skip migrations)
SKIP_MIGRATIONS=True

# Test runner options
PYTEST_ADDOPTS=--reuse-db --nomigrations
```

## ⚙️ Django Settings Modules

### Settings Architecture
```
config/settings/
├── __init__.py
├── base.py         # Common settings
├── local.py        # Development settings
├── production.py   # Production settings
└── test.py         # Test settings
```

### Setting Selection
```bash
# Environment variable controls which settings module
DJANGO_SETTINGS_MODULE=config.settings.local    # Development
DJANGO_SETTINGS_MODULE=config.settings.production  # Production
DJANGO_SETTINGS_MODULE=config.settings.test     # Testing
```

### Key Settings by Module

#### Base Settings (`base.py`)
- **Database**: PostgreSQL configuration
- **Cache**: Redis configuration
- **Security**: CORS, CSRF, authentication backends
- **Apps**: All Django apps and third-party packages
- **Middleware**: Common middleware stack
- **Templates**: Template engine configuration
- **Static Files**: Static and media file handling
- **Internationalization**: Language and timezone settings

#### Local Settings (`local.py`)
- **Debug**: `DEBUG = True`
- **Allowed Hosts**: Permissive for development
- **Debug Toolbar**: Enabled with IP allowlist
- **Logging**: Console logging with DEBUG level
- **Email**: Console backend for testing
- **CORS**: Allow all origins for development

#### Production Settings (`production.py`)
- **Security**: Strict security headers and HTTPS
- **Performance**: Optimized caching and database settings
- **Logging**: File-based logging with rotation
- **Static Files**: CDN/S3 configuration
- **Email**: Production SMTP configuration
- **Error Tracking**: Sentry integration

#### Test Settings (`test.py`)
- **Database**: In-memory SQLite or test PostgreSQL
- **Cache**: Dummy cache backend
- **Email**: Locmem backend
- **Celery**: Eager task execution
- **Media**: Temporary file storage

## 🐳 Docker Configuration

### Docker Compose Variables

#### Core Services
```yaml
# .env file variables used in docker-compose.yml
COMPOSE_PROJECT_NAME=boundlexx-dev
DJANGO_PORT=28001
POSTGRES_PORT=25432
REDIS_PORT=26379

# Container naming
CONTAINER_PREFIX=boundlexx
ENVIRONMENT=dev  # dev, test, production
```

#### Volume Configuration
```yaml
# Persistent data volumes
POSTGRES_DATA_VOLUME=boundlexx_postgres_data
REDIS_DATA_VOLUME=boundlexx_redis_data
MEDIA_VOLUME=boundlexx_media
STATIC_VOLUME=boundlexx_static
```

#### Build Configuration
```yaml
# Build arguments
PYTHON_VERSION=3.12
NODE_VERSION=18
BUILD_ENVIRONMENT=development
```

### Development Overrides
```yaml
# docker-compose.override.yml
# - Volume mounts for live reload
# - Debug port exposure
# - Development-specific environment variables
```

## 📦 Package Configuration

### Core Dependencies
```ini
# requirements/in/base.in
Django>=5.2,<5.3
psycopg2-binary>=2.9.0
redis>=4.0.0
celery>=5.3.0
djangorestframework>=3.14.0
django-cors-headers>=4.0.0
Pillow>=10.0.0
```

### Development Dependencies
```ini
# requirements/in/dev.in
-r base.in
django-debug-toolbar>=4.0.0
pytest-django>=4.5.0
black>=23.0.0
flake8>=6.0.0
isort>=5.12.0
coverage>=7.0.0
```

### Production Dependencies
```ini
# requirements/in/production.in
-r base.in
gunicorn>=21.0.0
whitenoise>=6.5.0
sentry-sdk[django]>=1.32.0
```

### Build Tools
```bash
# Update requirements
pip-compile requirements/in/base.in requirements/in/dev.in -o requirements/dev.txt
pip-compile requirements/in/base.in requirements/in/production.in -o requirements/production.txt
```

## 🎛️ Feature Flags & Toggles

### API Configuration
```python
# API versioning
API_VERSION_DEFAULT = 'v2'
API_VERSION_DEPRECATION_WARNINGS = True

# Features
ENABLE_API_THROTTLING = True
ENABLE_API_CACHING = True
ENABLE_WEBHOOK_SUPPORT = False
```

### Data Ingestion
```python
# Game data ingestion
AUTO_INGEST_ENABLED = False
INGEST_BATCH_SIZE = 1000
INGEST_RATE_LIMIT_DELAY = 1.0  # seconds

# Language support
SUPPORTED_LANGUAGES = ['english', 'french', 'german', 'italian', 'spanish']
DEFAULT_LANGUAGE = 'english'
ENGLISH_ONLY_MODE = False
```

### Background Tasks
```python
# Task queue selection
USE_CELERY = True
USE_HUEY = False  # Legacy support

# Task configuration
CELERY_TASK_ALWAYS_EAGER = False  # True for testing
CELERY_TASK_EAGER_PROPAGATES = True
TASK_RETRY_DELAYS = [60, 300, 900]  # seconds
```

## 🔒 Security Configuration

### Authentication Settings
```python
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    'django.contrib.auth.password_validation.MinimumLengthValidator',
    'django.contrib.auth.password_validation.CommonPasswordValidator',
    'django.contrib.auth.password_validation.NumericPasswordValidator',
]

# Session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
```

### CORS & CSRF
```python
# CORS configuration
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://api.yourdomain.com",
]

# CSRF protection
CSRF_COOKIE_SECURE = True  # Production only
CSRF_COOKIE_HTTPONLY = True
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS
```

### Security Headers
```python
# Security middleware
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

## 📊 Performance Configuration

### Database Optimization
```python
# Connection pooling
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'MAX_CONNS': 20,
            'CONN_MAX_AGE': 600,
        }
    }
}

# Query optimization
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DATABASE_ROUTERS = ['boundlexx.utils.routers.DatabaseRouter']
```

### Caching Strategy
```python
# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            'SERIALIZER': 'django_redis.serializers.msgpack.MSGPackSerializer',
        },
        'TIMEOUT': 300,
        'KEY_PREFIX': 'boundlexx',
    }
}

# Cache timeout configuration
CACHE_TIMEOUT_SHORT = 300      # 5 minutes
CACHE_TIMEOUT_MEDIUM = 3600    # 1 hour
CACHE_TIMEOUT_LONG = 86400     # 24 hours
```

### Static Files & Media
```python
# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = '/app/staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = '/app/media'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Production: Use S3 or CDN
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

## 🔧 Advanced Configuration

### Custom Middleware
```python
# Custom middleware stack
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'boundlexx.utils.middleware.RequestLoggingMiddleware',  # Custom
]
```

### API Configuration
```python
# DRF configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'boundlexx.api.pagination.CustomPageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/hour',
        'user': '5000/hour'
    }
}
```

### Logging Configuration
```python
# Comprehensive logging setup
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/app/logs/django.log',
            'maxBytes': 15728640,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'boundlexx': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

---

**Note**: Always use environment variables for sensitive configuration. Never commit secrets to version control.
