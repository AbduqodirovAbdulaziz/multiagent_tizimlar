"""
API URL Configuration - DRF endpoints.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet, SymptomViewSet, MedicalHistoryViewSet,
    DiseasePatternViewSet, DiagnosticSessionViewSet,
    AgentStateViewSet, AgentLogViewSet, ACLMessageViewSet
)

app_name = 'api'

router = DefaultRouter()

# Patient endpoints
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'symptoms', SymptomViewSet, basename='symptom')
router.register(r'medical-history', MedicalHistoryViewSet, basename='medical-history')

# Diagnostics endpoints
router.register(r'diseases', DiseasePatternViewSet, basename='disease')
router.register(r'diagnostics', DiagnosticSessionViewSet, basename='diagnostic')

# Agent endpoints
router.register(r'agents', AgentStateViewSet, basename='agent')
router.register(r'agent-logs', AgentLogViewSet, basename='agent-log')
router.register(r'acl-messages', ACLMessageViewSet, basename='acl-message')

urlpatterns = router.urls
