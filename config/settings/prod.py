"""
Production settings - ishlab chiqarish muhiti uchun.

Bu sozlamalar production serverda ishlatiladi.
Xavfsizlik va performance optimizatsiyalari yoqilgan.
"""
from .base import *

# Debug mode - ALBATTA False
DEBUG = False

# Allowed hosts - muhit o'zgaruvchisidan
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 yil
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])

# Email backend - SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')

# Admin email
ADMINS = [
    ('Admin', env('ADMIN_EMAIL', default='admin@example.com')),
]

# Logging - production level
LOGGING['loggers']['django']['level'] = 'WARNING'
LOGGING['loggers']['apps']['level'] = 'INFO'

# Database connection pooling
DATABASES['default']['CONN_MAX_AGE'] = 600
DATABASES['default']['OPTIONS'] = {
    'connect_timeout': 10,
}

# Sentry (optional - error tracking)
if env('SENTRY_DSN', default=None):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration
    
    sentry_sdk.init(
        dsn=env('SENTRY_DSN'),
        integrations=[
            DjangoIntegration(),
            CeleryIntegration(),
        ],
        traces_sample_rate=0.1,
        send_default_pii=False,
        environment='production',
    )
