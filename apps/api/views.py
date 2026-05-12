"""
API Views - DRF ViewSets.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from apps.patients.models import Patient, Symptom, MedicalHistory
from apps.diagnostics.models import DiseasePattern, DiagnosticSession, DiagnosticResult
from apps.diagnostics.services import DiagnosticService
from apps.agents.models import AgentState
from apps.core.models import ACLMessage, AgentLog

from .serializers import (
    PatientSerializer, SymptomSerializer, MedicalHistorySerializer,
    DiseasePatternSerializer, DiagnosticSessionSerializer,
    DiagnosticSessionCreateSerializer, DiagnosticResultSerializer,
    AgentStateSerializer, AgentLogSerializer, ACLMessageSerializer
)


class PatientViewSet(viewsets.ModelViewSet):
    """Bemor ViewSet."""
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['gender', 'blood_type', 'is_active']
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    ordering_fields = ['created_at', 'last_name']
    ordering = ['-created_at']


class SymptomViewSet(viewsets.ModelViewSet):
    """Simptom ViewSet."""
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['patient', 'severity']
    ordering = ['-created_at']


class MedicalHistoryViewSet(viewsets.ModelViewSet):
    """Tibbiy tarix ViewSet."""
    queryset = MedicalHistory.objects.all()
    serializer_class = MedicalHistorySerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['patient']
    ordering = ['-diagnosed_at']


class DiseasePatternViewSet(viewsets.ReadOnlyModelViewSet):
    """Kasallik naqshlari ViewSet (faqat o'qish)."""
    queryset = DiseasePattern.objects.filter(is_active=True)
    serializer_class = DiseasePatternSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['severity']
    search_fields = ['name', 'icd_code', 'description']
    ordering = ['name']


class DiagnosticSessionViewSet(viewsets.ModelViewSet):
    """Diagnostika sessiyalari ViewSet."""
    queryset = DiagnosticSession.objects.all()
    serializer_class = DiagnosticSessionSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'patient']
    ordering = ['-started_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DiagnosticSessionCreateSerializer
        return DiagnosticSessionSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Yangi diagnostika sessiyasini yaratish.
        
        POST /api/v1/diagnostics/
        {
            "patient_id": 1,
            "symptoms": ["bosh og'rig'i", "isitma"],
            "test_results": {"temperature": 38.5}
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        patient_id = serializer.validated_data['patient_id']
        symptoms = serializer.validated_data['symptoms']
        test_results = serializer.validated_data.get('test_results', {})
        
        # Bemorni tekshirish
        patient = get_object_or_404(Patient, id=patient_id)
        
        # Sessiya yaratish
        session = DiagnosticService.create_session(patient, symptoms)
        
        # Diagnostika jarayonini boshlash (asinxron - Celery task)
        # Hozircha oddiy sinxron
        from apps.agents.coordinator_agent import CoordinatorAgent
        coordinator = CoordinatorAgent()
        
        try:
            result = coordinator.execute({
                'session_id': session.session_id,
                'patient_id': patient.id,
                'symptoms': symptoms,
                'test_results': test_results
            })
            
            # Yangilangan sessionni olish
            session.refresh_from_db()
            
            response_serializer = DiagnosticSessionSerializer(session)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """
        Sessiya holatini olish.
        
        GET /api/v1/diagnostics/{id}/status/
        """
        session = self.get_object()
        return Response({
            'session_id': session.session_id,
            'status': session.status,
            'agent_states': session.agent_states,
            'started_at': session.started_at,
            'completed_at': session.completed_at
        })
    
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """
        Sessiya natijalarini olish.
        
        GET /api/v1/diagnostics/{id}/results/
        """
        session = self.get_object()
        results = session.results.all()
        serializer = DiagnosticResultSerializer(results, many=True)
        return Response(serializer.data)


class AgentStateViewSet(viewsets.ReadOnlyModelViewSet):
    """Agent holatlari ViewSet (faqat o'qish)."""
    queryset = AgentState.objects.all()
    serializer_class = AgentStateSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def health(self, request):
        """
        Barcha agentlar holati.
        
        GET /api/v1/agents/health/
        """
        agents = AgentState.objects.all()
        data = {
            'total_agents': agents.count(),
            'agents': AgentStateSerializer(agents, many=True).data
        }
        return Response(data)


class AgentLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Agent loglar ViewSet (faqat o'qish)."""
    queryset = AgentLog.objects.all()
    serializer_class = AgentLogSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['agent_name', 'level']
    ordering = ['-timestamp']


class ACLMessageViewSet(viewsets.ReadOnlyModelViewSet):
    """ACL xabarlar ViewSet (faqat o'qish)."""
    queryset = ACLMessage.objects.all()
    serializer_class = ACLMessageSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['sender', 'receiver', 'performative', 'is_processed']
    ordering = ['-created_at']
