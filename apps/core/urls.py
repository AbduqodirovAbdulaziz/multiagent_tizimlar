"""
Core app URL configuration - Health check endpoint.
"""
from django.urls import path
from .views import health_check

app_name = 'core'

urlpatterns = [
    path('', health_check, name='health_check'),
]
