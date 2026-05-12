"""
Core views - Health check va utility views.
"""
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import redis
from django.conf import settings


def health_check(request):
    """
    Health check endpoint - Docker va monitoring uchun.
    
    Database, Redis va Cache holatini tekshiradi.
    """
    health_status = {
        'status': 'healthy',
        'database': False,
        'cache': False,
        'redis': False,
    }
    
    # Database check
    try:
        connection.ensure_connection()
        health_status['database'] = True
    except Exception:
        health_status['status'] = 'unhealthy'
    
    # Cache check
    try:
        cache.set('health_check', 'ok', 10)
        health_status['cache'] = cache.get('health_check') == 'ok'
    except Exception:
        health_status['status'] = 'unhealthy'
    
    # Redis check
    try:
        redis_client = redis.from_url(settings.REDIS_URL)
        redis_client.ping()
        health_status['redis'] = True
    except Exception:
        health_status['status'] = 'unhealthy'
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return JsonResponse(health_status, status=status_code)
