"""
Test settings - pytest uchun.

Bu sozlamalar test muhitida ishlatiladi.
Tezlik va izolyatsiya uchun optimizatsiya qilingan.
"""
from .base import *

# Debug mode
DEBUG = False

# Test database - in-memory SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Password hashers - tezroq test uchun
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Cache - dummy cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Celery - eager mode (asinxron emas)
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Email - memory backend
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Logging - minimal
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
    },
}

# Media files - temporary directory
MEDIA_ROOT = '/tmp/medical_mas_test_media'

# Static files
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
