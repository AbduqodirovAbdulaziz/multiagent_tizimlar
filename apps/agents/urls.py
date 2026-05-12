"""
Agents URL Configuration.
"""
from django.urls import path
from . import views

app_name = 'agents'

urlpatterns = [
    # Agent URLs
    path('', views.agent_list, name='agent_list'),
    path('<str:agent_name>/', views.agent_detail, name='agent_detail'),
    path('<str:agent_name>/status/', views.agent_status_ajax, name='agent_status_ajax'),
    
    # Logs and Messages
    path('logs/all/', views.agent_logs, name='agent_logs'),
    path('messages/acl/', views.acl_messages, name='acl_messages'),
    
    # Health Check
    path('health/check/', views.agents_health_check, name='health_check'),
]
