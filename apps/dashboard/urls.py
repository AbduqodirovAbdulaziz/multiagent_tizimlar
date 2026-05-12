"""
Dashboard URL Configuration.
"""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('session/<str:session_id>/', views.session_detail, name='session_detail'),
    path('agents/', views.agent_status, name='agent_status'),
    path('diagnostic/start/', views.start_diagnostic, name='start_diagnostic'),
]
