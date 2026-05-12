"""
PythonAnywhere settings - production deployment uchun.

PythonAnywhere platformasiga moslashtirilgan sozlamalar.
Redis o'rniga DB cache ishlatiladi (bepul plan uchun).
"""
from .base import *
import os

# Debug mode - ALBATTA False
DEBUG = False

# PythonAnywhere username
PYTHONANYWHERE_USERNAME = os.environ.get('PYTHONANYWHERE_USERNAME', 'multiagent')

ALLOWED_HOSTS = [
    f'{PYTHONANYWHERE_USERNAME}.pythonanywhere.com',
    'localhost',
    '127.0.0.1',
]

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    f'https://{PYTHONANYWHERE_USERNAME}.pythonanywhere.com'
]

# Security - PythonAnywhere SSL ni o'zi boshqaradi
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Cache - Redis yo'q, DB cache ishlatamiz
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'django_cache_table',
    }
}

# Email backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static files - WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Logging - production
if 'LOGGING' in locals():
    LOGGING['loggers']['django']['level'] = 'WARNING'
    LOGGING['loggers']['apps']['level'] = 'INFO'

# Debug toolbar o'chirish
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'debug_toolbar']
MIDDLEWARE = [m for m in MIDDLEWARE if 'debug_toolbar' not in m]
