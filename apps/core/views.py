"""
Core views - Health check va utility views.
"""
from django.http import JsonResponse
from django.db import connection


def health_check(request):
    """
    Health check endpoint - monitoring uchun.
    Database va Cache holatini tekshiradi.
    """
    health_status = {
        'status': 'healthy',
        'database': False,
        'cache': False,
    }

    # Database check
    try:
        connection.ensure_connection()
        health_status['database'] = True
    except Exception:
        health_status['status'] = 'unhealthy'

    # Cache check
    try:
        from django.core.cache import cache
        cache.set('health_check', 'ok', 10)
        health_status['cache'] = cache.get('health_check') == 'ok'
    except Exception:
        health_status['cache'] = False

    # Redis check (ixtiyoriy - xato bo'lsa ham davom etadi)
    try:
        import redis
        from django.conf import settings
        redis_url = getattr(settings, 'REDIS_URL', None)
        if redis_url:
            redis_client = redis.from_url(redis_url, socket_connect_timeout=2)
            redis_client.ping()
            health_status['redis'] = True
        else:
            health_status['redis'] = 'not_configured'
    except Exception:
        health_status['redis'] = False
        # Redis yo'q bo'lsa ham unhealthy demaymiz

    status_code = 200 if health_status['status'] == 'healthy' else 503
    return JsonResponse(health_status, status=status_code)
