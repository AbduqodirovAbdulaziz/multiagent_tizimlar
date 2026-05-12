"""
Diagnostics URL Configuration.
"""
from django.urls import path
from . import views

app_name = 'diagnostics'

urlpatterns = [
    # Session URLs
    path('sessions/', views.session_list, name='session_list'),
    path('sessions/<str:session_id>/', views.session_detail, name='session_detail'),
    path('sessions/<str:session_id>/status/', views.session_status_ajax, name='session_status_ajax'),
    
    # Disease URLs
    path('diseases/', views.disease_list, name='disease_list'),
    path('diseases/<int:pk>/', views.disease_detail, name='disease_detail'),
]
