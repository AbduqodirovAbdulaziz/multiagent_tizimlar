"""
Agents serializers - Additional serializers for agents app.
"""
from rest_framework import serializers
from .models import AgentState
from apps.core.models import AgentLog, ACLMessage


class AgentStateDetailSerializer(serializers.ModelSerializer):
    """Agent holati detallari uchun serializer."""
    
    uptime = serializers.SerializerMethodField()
    
    class Meta:
        model = AgentState
        fields = [
            'id', 'agent_name', 'state', 'current_task',
            'metadata', 'last_activity', 'created_at', 'uptime'
        ]
        read_only_fields = ['id', 'last_activity', 'created_at']
    
    def get_uptime(self, obj):
        """Agent qancha vaqt ishlab turganini hisoblash."""
        from django.utils import timezone
        if obj.created_at:
            delta = timezone.now() - obj.created_at
            return delta.total_seconds()
        return 0


class AgentLogDetailSerializer(serializers.ModelSerializer):
    """Agent log detallari uchun serializer."""
    
    class Meta:
        model = AgentLog
        fields = [
            'id', 'agent_name', 'level', 'message',
            'extra_data', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']


class ACLMessageDetailSerializer(serializers.ModelSerializer):
    """ACL xabar detallari uchun serializer."""
    
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = ACLMessage
        fields = [
            'id', 'message_id', 'performative', 'sender', 'receiver',
            'content', 'in_reply_to', 'is_processed', 'expires_at',
            'is_expired', 'created_at', 'read_at'
        ]
        read_only_fields = ['id', 'message_id', 'created_at', 'read_at']
    
    def get_is_expired(self, obj):
        """Xabar muddati o'tganmi?"""
        from django.utils import timezone
        if obj.expires_at:
            return timezone.now() > obj.expires_at
        return False
