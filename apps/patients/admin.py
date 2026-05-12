"""
Patients admin - Admin interface konfiguratsiyasi.
"""
from django.contrib import admin
from .models import Patient, Symptom, MedicalHistory


class SymptomInline(admin.TabularInline):
    """Simptomlar inline."""
    model = Symptom
    extra = 1
    fields = ['name', 'severity', 'started_at', 'duration_days']


class MedicalHistoryInline(admin.TabularInline):
    """Tibbiy tarix inline."""
    model = MedicalHistory
    extra = 0
    fields = ['disease_name', 'diagnosed_at', 'treatment']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """Bemor admin interface."""
    
    list_display = [
        'get_full_name',
        'date_of_birth',
        'get_age',
        'gender',
        'phone',
        'is_active',
        'created_at',
    ]
    
    list_filter = [
        'gender',
        'blood_type',
        'is_active',
        'created_at',
    ]
    
    search_fields = [
        'first_name',
        'last_name',
        'middle_name',
        'phone',
        'email',
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'get_age',
        'get_bmi',
    ]
    
    fieldsets = (
        ('Shaxsiy Malumotlar', {
            'fields': (
                'user',
                'first_name',
                'last_name',
                'middle_name',
                'date_of_birth',
                'gender',
            )
        }),
        ('Aloqa', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Tibbiy Malumotlar', {
            'fields': (
                'blood_type',
                'height',
                'weight',
                'get_bmi',
                'allergies',
                'chronic_diseases',
            )
        }),
        ('Qoshimcha', {
            'fields': ('notes', 'is_active')
        }),
        ('Vaqt', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [SymptomInline, MedicalHistoryInline]
    
    date_hierarchy = 'created_at'
    
    def get_age(self, obj):
        """Yoshni ko'rsatish."""
        return f"{obj.get_age()} yosh"
    get_age.short_description = 'Yosh'
    
    def get_bmi(self, obj):
        """BMI ni ko'rsatish."""
        bmi = obj.get_bmi()
        if bmi:
            return f"{bmi:.1f}"
        return '-'
    get_bmi.short_description = 'BMI'


@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    """Simptom admin interface."""
    
    list_display = [
        'patient',
        'name',
        'severity',
        'started_at',
        'duration_days',
        'created_at',
    ]
    
    list_filter = [
        'severity',
        'started_at',
        'created_at',
    ]
    
    search_fields = [
        'patient__first_name',
        'patient__last_name',
        'name',
        'description',
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    date_hierarchy = 'started_at'


@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    """Tibbiy tarix admin interface."""
    
    list_display = [
        'patient',
        'disease_name',
        'diagnosed_at',
        'doctor_name',
        'created_at',
    ]
    
    list_filter = [
        'diagnosed_at',
        'created_at',
    ]
    
    search_fields = [
        'patient__first_name',
        'patient__last_name',
        'disease_name',
        'doctor_name',
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    date_hierarchy = 'diagnosed_at'
