"""
Core admin - Admin interface konfiguratsiyasi.
"""
from django.contrib import admin
from .models import ACLMessage, AgentLog


@admin.register(ACLMessage)
class ACLMessageAdmin(admin.ModelAdmin):
    """ACL xabarlar admin interface."""
    
    list_display = [
        'message_id',
        'performative',
        'sender',
        'receiver',
        'is_processed',
        'created_at',
    ]
    
    list_filter = [
        'performative',
        'is_processed',
        'created_at',
    ]
    
    search_fields = [
        'message_id',
        'sender',
        'receiver',
    ]
    
    readonly_fields = [
        'message_id',
        'created_at',
        'read_at',
    ]
    
    fieldsets = (
        ('Xabar Malumotlari', {
            'fields': ('message_id', 'performative', 'sender', 'receiver')
        }),
        ('Kontent', {
            'fields': ('content', 'in_reply_to')
        }),
        ('Holat', {
            'fields': ('is_processed', 'expires_at')
        }),
        ('Vaqt', {
            'fields': ('created_at', 'read_at')
        }),
    )
    
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        """Qo'lda xabar qo'shishni cheklash."""
        return False


@admin.register(AgentLog)
class AgentLogAdmin(admin.ModelAdmin):
    """Agent log admin interface."""
    
    list_display = [
        'agent_name',
        'level',
        'message_preview',
        'timestamp',
    ]
    
    list_filter = [
        'agent_name',
        'level',
        'timestamp',
    ]
    
    search_fields = [
        'agent_name',
        'message',
    ]
    
    readonly_fields = [
        'agent_name',
        'level',
        'message',
        'extra_data',
        'timestamp',
    ]
    
    date_hierarchy = 'timestamp'
    
    def message_preview(self, obj):
        """Xabar preview."""
        return obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
    
    message_preview.short_description = 'Xabar'
    
    def has_add_permission(self, request):
        """Qo'lda log qo'shishni cheklash."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Log o'zgartirishni cheklash."""
        return False
