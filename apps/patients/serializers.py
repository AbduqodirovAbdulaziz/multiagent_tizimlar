"""
Patients serializers - Additional serializers for patients app.
"""
from rest_framework import serializers
from .models import Patient, Symptom, MedicalHistory


class PatientListSerializer(serializers.ModelSerializer):
    """Bemor ro'yxati uchun serializer (qisqacha)."""
    
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    age = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = [
            'id', 'full_name', 'age', 'gender',
            'phone', 'email', 'is_active'
        ]
    
    def get_age(self, obj):
        return obj.get_age()


class PatientDetailSerializer(serializers.ModelSerializer):
    """Bemor detallari uchun serializer."""
    
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    age = serializers.SerializerMethodField()
    bmi = serializers.SerializerMethodField()
    symptom_count = serializers.SerializerMethodField()
    session_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = [
            'id', 'first_name', 'last_name', 'middle_name', 'full_name',
            'date_of_birth', 'age', 'gender', 'phone', 'email',
            'blood_type', 'height', 'weight', 'bmi',
            'allergies', 'chronic_diseases', 'emergency_contact',
            'address', 'notes', 'is_active',
            'symptom_count', 'session_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_age(self, obj):
        return obj.get_age()
    
    def get_bmi(self, obj):
        return obj.get_bmi()
    
    def get_symptom_count(self, obj):
        return obj.symptoms.count()
    
    def get_session_count(self, obj):
        return obj.diagnostic_sessions.count()


class SymptomDetailSerializer(serializers.ModelSerializer):
    """Simptom detallari uchun serializer."""
    
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    
    class Meta:
        model = Symptom
        fields = [
            'id', 'patient', 'patient_name', 'name', 'description',
            'severity', 'started_at', 'duration_days', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class MedicalHistoryDetailSerializer(serializers.ModelSerializer):
    """Tibbiy tarix detallari uchun serializer."""
    
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    
    class Meta:
        model = MedicalHistory
        fields = [
            'id', 'patient', 'patient_name', 'disease_name',
            'diagnosed_at', 'treatment', 'outcome',
            'doctor_name', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
