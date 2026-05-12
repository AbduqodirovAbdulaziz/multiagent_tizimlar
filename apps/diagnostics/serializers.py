"""
Diagnostics serializers - Additional serializers for diagnostics app.
"""
from rest_framework import serializers
from .models import DiseasePattern, DiagnosticSession, DiagnosticResult


class DiseasePatternListSerializer(serializers.ModelSerializer):
    """Kasallik ro'yxati uchun serializer (qisqacha)."""
    
    symptom_count = serializers.SerializerMethodField()
    
    class Meta:
        model = DiseasePattern
        fields = [
            'id', 'name', 'icd_code', 'severity',
            'symptom_count', 'is_active'
        ]
    
    def get_symptom_count(self, obj):
        return len(obj.symptoms) if obj.symptoms else 0


class DiagnosticSessionListSerializer(serializers.ModelSerializer):
    """Sessiya ro'yxati uchun serializer (qisqacha)."""
    
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    duration = serializers.SerializerMethodField()
    result_count = serializers.SerializerMethodField()
    
    class Meta:
        model = DiagnosticSession
        fields = [
            'id', 'session_id', 'patient_name', 'status',
            'started_at', 'completed_at', 'duration', 'result_count'
        ]
    
    def get_duration(self, obj):
        return obj.get_duration()
    
    def get_result_count(self, obj):
        return obj.results.count()


class DiagnosticResultDetailSerializer(serializers.ModelSerializer):
    """Natija detallari uchun serializer."""
    
    disease_name = serializers.CharField(source='disease.name', read_only=True)
    disease_icd = serializers.CharField(source='disease.icd_code', read_only=True)
    confidence_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = DiagnosticResult
        fields = [
            'id', 'disease_name', 'disease_icd',
            'confidence_score', 'confidence_percentage',
            'recommended_tests', 'treatment_plan',
            'agent_recommendations', 'created_at'
        ]
    
    def get_confidence_percentage(self, obj):
        return obj.get_confidence_percentage()
