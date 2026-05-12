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
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Asosiy Malumotlar', {
            'fields': ('name', 'icd_code', 'description', 'severity')
        }),
        ('Simptomlar va Tahlillar', {
            'fields': ('symptoms', 'recommended_tests')
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


class DiagnosticResultInline(admin.TabularInline):
    """Diagnostika natijalari inline."""
    model = DiagnosticResult
    extra = 0
    readonly_fields = ['disease', 'confidence_score', 'created_at']
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(DiagnosticSession)
class DiagnosticSessionAdmin(admin.ModelAdmin):
    """Diagnostika sessiyalari admin interface."""
    
    list_display = [
        'session_id',
        'patient',
        'status',
        'started_at',
        'completed_at',
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
    ]
    
    fieldsets = (
        ('Session Malumotlari', {
            'fields': ('session_id', 'patient', 'status')
        }),
        ('Simptomlar va Tahlillar', {
            'fields': ('symptoms', 'test_results')
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
            'fields': ('started_at', 'completed_at', 'get_duration_display')
        }),
    )
    
    inlines = [DiagnosticResultInline]
    
    date_hierarchy = 'started_at'
    
    def get_duration_display(self, obj):
        """Davomiylikni ko'rsatish."""
        duration = obj.get_duration()
        if duration:
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            return f"{minutes}m {seconds}s"
        return '-'
    get_duration_display.short_description = 'Davomiyligi'
    
    def has_add_permission(self, request):
        """Qo'lda sessiya qo'shishni cheklash."""
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
