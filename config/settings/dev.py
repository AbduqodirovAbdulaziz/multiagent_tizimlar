"""
Development settings - lokal ishlab chiqish uchun.

Bu sozlamalar faqat development muhitida ishlatiladi.
Debug rejimi yoqilgan va qo'shimcha debug tool'lar mavjud.
"""
from .base import *

# Debug mode
DEBUG = True

# Allowed hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Debug Toolbar - faqat DEBUG=True bo'lganda
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    
    INTERNAL_IPS = ['127.0.0.1', 'localhost']
    
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
    }

# Email backend - console output
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CORS - barcha originlarga ruxsat (faqat dev)
CORS_ALLOW_ALL_ORIGINS = True

# Celery - eager mode (asinxron emas, test uchun qulay)
# CELERY_TASK_ALWAYS_EAGER = True
# CELERY_TASK_EAGER_PROPAGATES = True

# Logging - ko'proq ma'lumot
LOGGING['loggers']['django']['level'] = 'DEBUG'
LOGGING['loggers']['apps']['level'] = 'DEBUG'

# Static files - development server uchun
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Security settings - development uchun yumshatilgan
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Cache - dummy cache (test uchun)
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     }
# }
