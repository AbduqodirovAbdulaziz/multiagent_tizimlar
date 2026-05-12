"""
Diagnostics admin - Admin interface konfiguratsiyasi.
"""
from django.contrib import admin
from .models import DiseasePattern, DiagnosticSession, DiagnosticResult


@admin.register(DiseasePattern)
class DiseasePatternAdmin(admin.ModelAdmin):
    """Kasallik naqshlari admin interface."""
    
    list_display = [
        'name',
        'icd_code',
        'severity',
        'symptom_count',
        'is_active',
        'created_at',
    ]
    
    list_filter = [
        'severity',
        'is_active',
        'created_at',
    ]
    
    search_fields = [
        'name',
        'icd_code',
        'description',
    ]
    
    readonly_fields = ['created_at', 'updated_at', 'symptom_count', 'test_count']
    
    fieldsets = (
        ('Asosiy Malumotlar', {
            'fields': ('name', 'icd_code', 'description', 'severity')
        }),
        ('Simptomlar va Tahlillar', {
            'fields': ('symptoms', 'symptom_count', 'recommended_tests', 'test_count'),
            'description': 'Simptomlar va tahlillarni vergul bilan ajratib kiriting'
        }),
        ('Davolash', {
            'fields': ('treatment_options', 'prevention')
        }),
        ('Holat', {
            'fields': ('is_active',)
        }),
        ('Vaqt', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'created_at'
    
    def symptom_count(self, obj):
        """Simptomlar soni."""
        return len(obj.symptoms) if obj.symptoms else 0
    symptom_count.short_description = 'Simptomlar soni'
    
    def test_count(self, obj):
        """Tahlillar soni."""
        return len(obj.recommended_tests) if obj.recommended_tests else 0
    test_count.short_description = 'Tahlillar soni'


class DiagnosticResultInline(admin.TabularInline):
    """Diagnostika natijalari inline."""
    model = DiagnosticResult
    extra = 0
    readonly_fields = ['disease', 'confidence_score', 'get_confidence_percentage', 'created_at']
    fields = ['disease', 'confidence_score', 'get_confidence_percentage', 'created_at']
    can_delete = False
    
    def get_confidence_percentage(self, obj):
        """Ishonch foizda."""
        if obj.pk:
            return f"{obj.get_confidence_percentage():.1f}%"
        return '-'
    get_confidence_percentage.short_description = 'Ishonch (%)'
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(DiagnosticSession)
class DiagnosticSessionAdmin(admin.ModelAdmin):
    """Diagnostika sessiyalari admin interface."""
    
    list_display = [
        'session_id',
        'patient',
        'status',
        'symptom_count',
        'result_count',
        'started_at',
        'get_duration_display',
    ]
    
    list_filter = [
        'status',
        'started_at',
        'completed_at',
    ]
    
    search_fields = [
        'session_id',
        'patient__first_name',
        'patient__last_name',
    ]
    
    readonly_fields = [
        'session_id',
        'started_at',
        'completed_at',
        'get_duration_display',
        'symptom_count',
        'result_count',
    ]
    
    fieldsets = (
        ('Session Malumotlari', {
            'fields': ('session_id', 'patient', 'status')
        }),
        ('Simptomlar va Tahlillar', {
            'fields': ('symptoms', 'symptom_count', 'test_results'),
            'description': 'Simptomlarni list formatida kiriting: ["simptom1", "simptom2"]'
        }),
        ('Statistika', {
            'fields': ('result_count', 'get_duration_display')
        }),
        ('Agent Holatlari', {
            'fields': ('agent_states',),
            'classes': ('collapse',)
        }),
        ('Xatolik', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
        ('Vaqt', {
            'fields': ('started_at', 'completed_at')
        }),
    )
    
    inlines = [DiagnosticResultInline]
    
    date_hierarchy = 'started_at'
    
    autocomplete_fields = ['patient']
    
    def get_duration_display(self, obj):
        """Davomiylikni ko'rsatish."""
        duration = obj.get_duration()
        if duration:
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            return f"{minutes}m {seconds}s"
        return '-'
    get_duration_display.short_description = 'Davomiyligi'
    
    def symptom_count(self, obj):
        """Simptomlar soni."""
        return len(obj.symptoms) if obj.symptoms else 0
    symptom_count.short_description = 'Simptomlar'
    
    def result_count(self, obj):
        """Natijalar soni."""
        return obj.results.count()
    result_count.short_description = 'Natijalar'
    
    def has_add_permission(self, request):
        """Qo'lda sessiya qo'shishni cheklash."""
        # API orqali yaratilishi kerak
        return False


@admin.register(DiagnosticResult)
class DiagnosticResultAdmin(admin.ModelAdmin):
    """Diagnostika natijalari admin interface."""
    
    list_display = [
        'session',
        'disease',
        'get_confidence_display',
        'created_at',
    ]
    
    list_filter = [
        'disease',
        'created_at',
    ]
    
    search_fields = [
        'session__session_id',
        'disease__name',
    ]
    
    readonly_fields = [
        'session',
        'disease',
        'confidence_score',
        'get_confidence_display',
        'created_at',
    ]
    
    fieldsets = (
        ('Asosiy Malumotlar', {
            'fields': ('session', 'disease', 'confidence_score', 'get_confidence_display')
        }),
        ('Tavsiyalar', {
            'fields': ('recommended_tests', 'treatment_plan')
        }),
        ('Agent Tavsiyalari', {
            'fields': ('agent_recommendations',),
            'classes': ('collapse',)
        }),
        ('Vaqt', {
            'fields': ('created_at',)
        }),
    )
    
    date_hierarchy = 'created_at'
    
    def get_confidence_display(self, obj):
        """Ishonch darajasini foizda ko'rsatish."""
        return f"{obj.get_confidence_percentage():.1f}%"
    get_confidence_display.short_description = 'Ishonch (%)'
    
    def has_add_permission(self, request):
        """Qo'lda natija qo'shishni cheklash."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Natijani o'zgartirishni cheklash."""
        return False
