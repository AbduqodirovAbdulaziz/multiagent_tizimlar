"""
Core models - Bazaviy agent sinfi va ACL xabar modeli.

Bu modul FIPA-ACL protokoli va BDI arxitekturasini amalga oshiradi.
"""
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError


class ACLMessage(models.Model):
    """
    FIPA-ACL (Foundation for Intelligent Physical Agents - Agent Communication Language) xabar modeli.
    
    Bu model agentlar o'rtasida standartlashtirilgan xabar almashishni ta'minlaydi.
    Har bir xabar performative (harakat turi), sender, receiver va content'ga ega.
    """
    
    PERFORMATIVE_CHOICES = [
        ('INFORM', 'Inform - Ma\'lumot berish'),
        ('REQUEST', 'Request - So\'rov yuborish'),
        ('QUERY', 'Query - Savol berish'),
        ('PROPOSE', 'Propose - Taklif qilish'),
        ('ACCEPT', 'Accept - Qabul qilish'),
        ('REJECT', 'Reject - Rad etish'),
        ('CONFIRM', 'Confirm - Tasdiqlash'),
        ('FAILURE', 'Failure - Xatolik haqida xabar'),
    ]
    
    # Xabar identifikatori
    message_id = models.CharField(max_length=100, unique=True, db_index=True)
    
    # Performative - xabar turi (FIPA-ACL standarti)
    performative = models.CharField(
        max_length=20,
        choices=PERFORMATIVE_CHOICES,
        default='INFORM'
    )
    
    # Yuboruvchi agent
    sender = models.CharField(max_length=100, db_index=True)
    
    # Qabul qiluvchi agent
    receiver = models.CharField(max_length=100, db_index=True)
    
    # Xabar mazmuni (JSON format)
    content = models.JSONField(default=dict)
    
    # Javob uchun xabar ID (agar bu javob bo'lsa)
    in_reply_to = models.CharField(max_length=100, blank=True, null=True)
    
    # Xabar yaratilgan vaqt
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Xabar o'qilgan vaqt
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Xabar holati
    is_processed = models.BooleanField(default=False, db_index=True)
    
    # TTL (Time To Live) - xabar amal qilish muddati
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'ACL Xabar'
        verbose_name_plural = 'ACL Xabarlar'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['sender', 'receiver']),
            models.Index(fields=['performative', 'is_processed']),
        ]
    
    def __str__(self):
        return f"{self.performative}: {self.sender} -> {self.receiver}"
    
    def clean(self):
        """Model validatsiyasi."""
        if self.sender == self.receiver:
            raise ValidationError("Sender va receiver bir xil bo'lishi mumkin emas")
    
    def mark_as_read(self):
        """Xabarni o'qilgan deb belgilash."""
        self.read_at = timezone.now()
        self.save(update_fields=['read_at'])
    
    def mark_as_processed(self):
        """Xabarni qayta ishlangan deb belgilash."""
        self.is_processed = True
        self.save(update_fields=['is_processed'])
    
    def is_expired(self):
        """Xabar muddati o'tganligini tekshirish."""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False


class AgentLog(models.Model):
    """
    Agent faoliyati log modeli.
    
    Har bir agent harakati va hodisasi bu yerda saqlanadi.
    """
    
    LOG_LEVEL_CHOICES = [
        ('DEBUG', 'Debug'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]
    
    # Agent nomi
    agent_name = models.CharField(max_length=100, db_index=True)
    
    # Log darajasi
    level = models.CharField(
        max_length=20,
        choices=LOG_LEVEL_CHOICES,
        default='INFO'
    )
    
    # Xabar
    message = models.TextField()
    
    # Qo'shimcha ma'lumotlar (JSON)
    extra_data = models.JSONField(default=dict, blank=True)
    
    # Vaqt
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        verbose_name = 'Agent Log'
        verbose_name_plural = 'Agent Logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['agent_name', 'level']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"[{self.level}] {self.agent_name}: {self.message[:50]}"
