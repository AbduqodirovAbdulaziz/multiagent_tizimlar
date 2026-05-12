"""
Agents admin - Admin interface konfiguratsiyasi.
"""
from django.contrib import admin
from .models import AgentState


@admin.register(AgentState)
class AgentStateAdmin(admin.ModelAdmin):
    """Agent holati admin interface."""
    
    list_display = [
        'agent_name',
        'state',
        'current_task_preview',
        'last_activity',
    ]
    
    list_filter = [
        'state',
        'last_activity',
    ]
    
    search_fields = [
        'agent_name',
        'current_task',
    ]
    
    readonly_fields = [
        'agent_name',
        'last_activity',
        'created_at',
    ]
    
    fieldsets = (
        ('Agent Malumotlari', {
            'fields': ('agent_name', 'state', 'current_task')
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',),
            'description': 'Agent qo\'shimcha ma\'lumotlari JSON formatida'
        }),
        ('Vaqt', {
            'fields': ('last_activity', 'created_at')
        }),
    )
    
    def current_task_preview(self, obj):
        """Vazifa preview."""
        if obj.current_task:
            return obj.current_task[:50] + '...' if len(obj.current_task) > 50 else obj.current_task
        return '-'
    current_task_preview.short_description = 'Hozirgi Vazifa'
    
    def has_add_permission(self, request):
        """Qo'lda agent holati qo'shishni cheklash."""
        return False
