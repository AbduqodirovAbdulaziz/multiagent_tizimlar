"""
API Serializers - DRF serializers.
"""
from rest_framework import serializers
from apps.patients.models import Patient, Symptom, MedicalHistory
from apps.diagnostics.models import DiseasePattern, DiagnosticSession, DiagnosticResult
from apps.agents.models import AgentState
from apps.core.models import ACLMessage, AgentLog


# Patient Serializers
class PatientSerializer(serializers.ModelSerializer):
    """Bemor serializer."""
    age = serializers.SerializerMethodField()
    bmi = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = [
            'id', 'first_name', 'last_name', 'middle_name',
            'date_of_birth', 'age', 'gender', 'phone', 'email',
            'blood_type', 'height', 'weight', 'bmi',
            'allergies', 'chronic_diseases', 'is_active'
        ]
        read_only_fields = ['id']
    
    def get_age(self, obj):
        return obj.get_age()
    
    def get_bmi(self, obj):
        return obj.get_bmi()


class SymptomSerializer(serializers.ModelSerializer):
    """Simptom serializer."""
    
    class Meta:
        model = Symptom
        fields = [
            'id', 'patient', 'name', 'description',
            'severity', 'started_at', 'duration_days'
        ]
        read_only_fields = ['id']


class MedicalHistorySerializer(serializers.ModelSerializer):
    """Tibbiy tarix serializer."""
    
    class Meta:
        model = MedicalHistory
        fields = [
            'id', 'patient', 'disease_name', 'diagnosed_at',
            'treatment', 'outcome', 'doctor_name', 'notes'
        ]
        read_only_fields = ['id']


# Diagnostics Serializers
class DiseasePatternSerializer(serializers.ModelSerializer):
    """Kasallik naqshi serializer."""
    
    class Meta:
        model = DiseasePattern
        fields = [
            'id', 'name', 'icd_code', 'description',
            'symptoms', 'severity', 'recommended_tests',
            'treatment_options', 'prevention', 'is_active'
        ]
        read_only_fields = ['id']


class DiagnosticResultSerializer(serializers.ModelSerializer):
    """Diagnostika natijasi serializer."""
    disease = DiseasePatternSerializer(read_only=True)
    confidence_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = DiagnosticResult
        fields = [
            'id', 'disease', 'confidence_score', 'confidence_percentage',
            'recommended_tests', 'treatment_plan', 'agent_recommendations'
        ]
        read_only_fields = ['id']
    
    def get_confidence_percentage(self, obj):
        return obj.get_confidence_percentage()


class DiagnosticSessionSerializer(serializers.ModelSerializer):
    """Diagnostika sessiyasi serializer."""
    patient = PatientSerializer(read_only=True)
    results = DiagnosticResultSerializer(many=True, read_only=True)
    duration = serializers.SerializerMethodField()
    
    class Meta:
        model = DiagnosticSession
        fields = [
            'id', 'session_id', 'patient', 'status',
            'symptoms', 'test_results', 'agent_states',
            'error_message', 'started_at', 'completed_at',
            'duration', 'results'
        ]
        read_only_fields = ['id', 'session_id', 'started_at', 'completed_at']
    
    def get_duration(self, obj):
        return obj.get_duration()


class DiagnosticSessionCreateSerializer(serializers.Serializer):
    """Yangi diagnostika sessiyasi yaratish uchun serializer."""
    patient_id = serializers.IntegerField()
    symptoms = serializers.ListField(
        child=serializers.CharField(max_length=200),
        min_length=1
    )
    test_results = serializers.DictField(required=False, default=dict)


# Agent Serializers
class AgentStateSerializer(serializers.ModelSerializer):
    """Agent holati serializer."""
    
    class Meta:
        model = AgentState
        fields = [
            'id', 'agent_name', 'state', 'current_task',
            'metadata', 'last_activity'
        ]
        read_only_fields = ['id', 'last_activity']


class AgentLogSerializer(serializers.ModelSerializer):
    """Agent log serializer."""
    
    class Meta:
        model = AgentLog
        fields = [
            'id', 'agent_name', 'level', 'message',
            'extra_data', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']


class ACLMessageSerializer(serializers.ModelSerializer):
    """ACL xabar serializer."""
    
    class Meta:
        model = ACLMessage
        fields = [
            'id', 'message_id', 'performative', 'sender',
            'receiver', 'content', 'in_reply_to',
            'is_processed', 'expires_at', 'created_at', 'read_at'
        ]
        read_only_fields = ['id', 'message_id', 'created_at', 'read_at']
