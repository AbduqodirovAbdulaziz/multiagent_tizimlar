"""
Agents models - Agent holati modellari.
"""
from django.db import models


class AgentState(models.Model):
    """
    Agent holati modeli.
    
    Har bir agentning real-vaqt holatini saqlaydi.
    """
    
    STATE_CHOICES = [
        ('IDLE', 'Bo\'sh'),
        ('PROCESSING', 'Ishlamoqda'),
        ('WAITING', 'Kutmoqda'),
        ('COMPLETED', 'Yakunlandi'),
        ('FAILED', 'Xatolik'),
    ]
    
    # Agent nomi
    agent_name = models.CharField('Agent nomi', max_length=100, unique=True)
    
    # Holat
    state = models.CharField(
        'Holat',
        max_length=20,
        choices=STATE_CHOICES,
        default='IDLE'
    )
    
    # Hozirgi vazifa
    current_task = models.CharField('Hozirgi vazifa', max_length=200, blank=True)
    
    # Qo'shimcha ma'lumotlar
    metadata = models.JSONField('Metadata', default=dict)
    
    # Oxirgi faoliyat vaqti
    last_activity = models.DateTimeField('Oxirgi faoliyat', auto_now=True)
    
    # Yaratilgan vaqt
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Agent Holati'
        verbose_name_plural = 'Agent Holatlari'
        ordering = ['agent_name']
    
    def __str__(self):
        return f"{self.agent_name}: {self.state}"
