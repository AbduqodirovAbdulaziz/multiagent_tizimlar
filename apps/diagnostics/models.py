"""
Diagnostics models - Diagnostika sessiyalari va natijalar.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.patients.models import Patient
from apps.core.constants import DIAGNOSTIC_STATES, SEVERITY_LEVELS


class DiseasePattern(models.Model):
    """
    Kasallik naqshlari bazasi.
    
    Bu model kasallik simptomlarini va ularning og'irlik darajasini saqlaydi.
    Agent'lar bu ma'lumotlardan foydalanib diagnoz qo'yadi.
    """
    
    # Kasallik nomi
    name = models.CharField('Kasallik nomi', max_length=200, unique=True)
    
    # ICD-10 kod (International Classification of Diseases)
    icd_code = models.CharField('ICD-10 Kod', max_length=10, blank=True)
    
    # Tavsif
    description = models.TextField('Tavsif')
    
    # Simptomlar (JSON format: {"simptom": weight})
    symptoms = models.JSONField('Simptomlar', default=dict)
    
    # Og'irlik darajasi
    severity = models.CharField(
        'Og\'irlik darajasi',
        max_length=20,
        choices=[(k, v) for k, v in SEVERITY_LEVELS.items()],
        default='MEDIUM'
    )
    
    # Tavsiya etiladigan tahlillar
    recommended_tests = models.JSONField('Tavsiya etiladigan tahlillar', default=list)
    
    # Davolash yo'llari
    treatment_options = models.TextField('Davolash yo\'llari', blank=True)
    
    # Oldini olish choralari
    prevention = models.TextField('Oldini olish', blank=True)
    
    # Faol holat
    is_active = models.BooleanField('Faol', default=True)
    
    # Vaqt belgilari
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Kasallik Naqshi'
        verbose_name_plural = 'Kasallik Naqshlari'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def calculate_match_score(self, patient_symptoms: list) -> float:
        """
        Bemor simptomlariga mos kelish darajasini hisoblash.
        
        Args:
            patient_symptoms: Bemor simptomlar ro'yxati
        
        Returns:
            Match score (0.0 - 1.0)
        """
        if not self.symptoms or not patient_symptoms:
            return 0.0
        
        total_weight = 0
        matched_weight = 0
        
        for symptom, weight in self.symptoms.items():
            total_weight += weight
            if symptom.lower() in [s.lower() for s in patient_symptoms]:
                matched_weight += weight
        
        if total_weight == 0:
            return 0.0
        
        return matched_weight / total_weight


class DiagnosticSession(models.Model):
    """
    Diagnostika sessiyasi modeli.
    
    Har bir diagnostika jarayoni uchun alohida sessiya yaratiladi.
    """
    
    STATUS_CHOICES = [
        ('PENDING', 'Kutilmoqda'),
        ('IN_PROGRESS', 'Jarayonda'),
        ('COMPLETED', 'Yakunlandi'),
        ('FAILED', 'Xatolik'),
    ]
    
    # Session ID
    session_id = models.CharField(
        'Session ID',
        max_length=100,
        unique=True,
        db_index=True
    )
    
    # Bemor
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='diagnostic_sessions'
    )
    
    # Holat
    status = models.CharField(
        'Holat',
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    
    # Simptomlar (JSON)
    symptoms = models.JSONField('Simptomlar', default=list)
    
    # Tahlil natijalari (JSON)
    test_results = models.JSONField('Tahlil natijalari', default=dict, blank=True)
    
    # Agent holatlari (JSON)
    agent_states = models.JSONField('Agent holatlari', default=dict)
    
    # Xatolik xabari
    error_message = models.TextField('Xatolik xabari', blank=True)
    
    # Vaqt belgilari
    started_at = models.DateTimeField('Boshlangan vaqt', auto_now_add=True)
    completed_at = models.DateTimeField('Yakunlangan vaqt', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Diagnostika Sessiyasi'
        verbose_name_plural = 'Diagnostika Sessiyalari'
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['session_id']),
            models.Index(fields=['status', 'started_at']),
        ]
    
    def __str__(self):
        return f"{self.session_id} - {self.patient.get_full_name()}"
    
    def mark_as_in_progress(self):
        """Sessiyani jarayonda deb belgilash."""
        self.status = 'IN_PROGRESS'
        self.save(update_fields=['status'])
    
    def mark_as_completed(self):
        """Sessiyani yakunlangan deb belgilash."""
        from django.utils import timezone
        self.status = 'COMPLETED'
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'completed_at'])
    
    def mark_as_failed(self, error_message: str):
        """Sessiyani xatolik bilan yakunlash."""
        from django.utils import timezone
        self.status = 'FAILED'
        self.error_message = error_message
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'error_message', 'completed_at'])
    
    def get_duration(self):
        """Sessiya davomiyligini hisoblash."""
        if self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None


class DiagnosticResult(models.Model):
    """
    Diagnostika natijasi modeli.
    
    Har bir sessiya uchun bir yoki bir nechta diagnoz natijasi bo'lishi mumkin.
    """
    
    session = models.ForeignKey(
        DiagnosticSession,
        on_delete=models.CASCADE,
        related_name='results'
    )
    
    # Kasallik
    disease = models.ForeignKey(
        DiseasePattern,
        on_delete=models.CASCADE,
        related_name='diagnostic_results'
    )
    
    # Ishonch darajasi (0.0 - 1.0)
    confidence_score = models.FloatField(
        'Ishonch darajasi',
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    
    # Tavsiya etilgan tahlillar
    recommended_tests = models.JSONField('Tavsiya etilgan tahlillar', default=list)
    
    # Davolash rejasi
    treatment_plan = models.TextField('Davolash rejasi', blank=True)
    
    # Agent tavsiyalari (JSON)
    agent_recommendations = models.JSONField('Agent tavsiyalari', default=dict)
    
    # Vaqt belgisi
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Diagnostika Natijasi'
        verbose_name_plural = 'Diagnostika Natijalari'
        ordering = ['-confidence_score']
    
    def __str__(self):
        return f"{self.disease.name} ({self.confidence_score:.2%})"
    
    def get_confidence_percentage(self):
        """Ishonch darajasini foizda qaytarish."""
        return self.confidence_score * 100
