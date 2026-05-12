"""
Patients URL Configuration.
"""
from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    # Patient URLs
    path('', views.patient_list, name='patient_list'),
    path('<int:pk>/', views.patient_detail, name='patient_detail'),
    path('search/', views.patient_search, name='patient_search'),
    
    # Symptom URLs
    path('symptoms/', views.symptom_list, name='symptom_list'),
    
    # Medical History URLs
    path('history/', views.medical_history_list, name='medical_history_list'),
]
