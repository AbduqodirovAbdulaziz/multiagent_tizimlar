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
        'current_task',
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
            'classes': ('collapse',)
        }),
        ('Vaqt', {
            'fields': ('last_activity', 'created_at')
        }),
    )
    
    def has_add_permission(self, request):
        """Qo'lda agent holati qo'shishni cheklash."""
        return False
