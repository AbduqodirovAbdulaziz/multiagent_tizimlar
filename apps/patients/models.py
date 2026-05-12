"""
Patients models - Bemor ma'lumotlari modellari.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from .managers import PatientManager, SymptomManager


class Patient(models.Model):
    """
    Bemor modeli.
    
    Bemorning shaxsiy ma'lumotlari va tibbiy tarixini saqlaydi.
    """
    
    GENDER_CHOICES = [
        ('M', 'Erkak'),
        ('F', 'Ayol'),
        ('O', 'Boshqa'),
    ]
    
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    # User bilan bog'lanish (ixtiyoriy)
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patient_profile'
    )
    
    # Shaxsiy ma'lumotlar
    first_name = models.CharField('Ism', max_length=100)
    last_name = models.CharField('Familiya', max_length=100)
    middle_name = models.CharField('Otasining ismi', max_length=100, blank=True)
    
    date_of_birth = models.DateField('Tug\'ilgan sana')
    gender = models.CharField('Jins', max_length=1, choices=GENDER_CHOICES)
    
    # Aloqa ma'lumotlari
    phone = PhoneNumberField('Telefon', blank=True)
    email = models.EmailField('Email', blank=True)
    address = models.TextField('Manzil', blank=True)
    emergency_contact = models.CharField('Favqulodda aloqa', max_length=100, blank=True)
    
    # Tibbiy ma'lumotlar
    blood_type = models.CharField(
        'Qon guruhi',
        max_length=3,
        choices=BLOOD_TYPE_CHOICES,
        blank=True
    )
    
    height = models.PositiveIntegerField(
        'Bo\'yi (sm)',
        null=True,
        blank=True,
        validators=[MinValueValidator(50), MaxValueValidator(250)]
    )
    
    weight = models.DecimalField(
        'Vazni (kg)',
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(2), MaxValueValidator(500)]
    )
    
    # Allergiyalar (JSON field)
    allergies = models.JSONField('Allergiyalar', default=list, blank=True)
    
    # Surunkali kasalliklar (JSON field)
    chronic_diseases = models.JSONField('Surunkali kasalliklar', default=list, blank=True)
    
    # Qo'shimcha ma'lumotlar
    notes = models.TextField('Qo\'shimcha ma\'lumotlar', blank=True)
    
    # Vaqt belgilari
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Faol holat
    is_active = models.BooleanField('Faol', default=True)
    
    # Custom manager
    objects = PatientManager()
    
    class Meta:
        verbose_name = 'Bemor'
        verbose_name_plural = 'Bemorlar'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['date_of_birth']),
        ]
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    def get_full_name(self):
        """To'liq ismni qaytarish."""
        parts = [self.last_name, self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        return ' '.join(parts)
    
    def get_age(self):
        """Yoshni hisoblash."""
        from django.utils import timezone
        today = timezone.now().date()
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month or \
           (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
            age -= 1
        return age
    
    def get_bmi(self):
        """BMI (Body Mass Index) ni hisoblash."""
        if self.height and self.weight:
            height_m = self.height / 100
            return float(self.weight) / (height_m ** 2)
        return None


class Symptom(models.Model):
    """
    Simptom modeli.
    
    Bemorning hozirgi simptomlarini saqlaydi.
    """
    
    SEVERITY_CHOICES = [
        ('LOW', 'Engil'),
        ('MEDIUM', 'O\'rtacha'),
        ('HIGH', 'Og\'ir'),
        ('CRITICAL', 'Kritik'),
    ]
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='symptoms'
    )
    
    # Simptom nomi
    name = models.CharField('Simptom', max_length=200)
    
    # Tavsif
    description = models.TextField('Tavsif', blank=True)
    
    # Og'irlik darajasi
    severity = models.CharField(
        'Og\'irlik darajasi',
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='MEDIUM'
    )
    
    # Boshlanish vaqti
    started_at = models.DateTimeField('Boshlanish vaqti')
    
    # Davomiyligi (kunlarda)
    duration_days = models.PositiveIntegerField(
        'Davomiyligi (kun)',
        null=True,
        blank=True
    )
    
    # Vaqt belgilari
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Custom manager
    objects = SymptomManager()
    
    class Meta:
        verbose_name = 'Simptom'
        verbose_name_plural = 'Simptomlar'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.patient.get_full_name()}: {self.name}"


class MedicalHistory(models.Model):
    """
    Tibbiy tarix modeli.
    
    Bemorning o'tmishdagi kasalliklari va davolanish tarixini saqlaydi.
    """
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='medical_history'
    )
    
    # Kasallik nomi
    disease_name = models.CharField('Kasallik', max_length=200)
    
    # Tashxis sanasi
    diagnosed_at = models.DateField('Tashxis sanasi')
    
    # Davolash
    treatment = models.TextField('Davolash', blank=True)
    
    # Natija
    outcome = models.TextField('Natija', blank=True)
    
    # Shifokor
    doctor_name = models.CharField('Shifokor', max_length=200, blank=True)
    
    # Qo'shimcha ma'lumotlar
    notes = models.TextField('Qo\'shimcha ma\'lumotlar', blank=True)
    
    # Vaqt belgilari
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Tibbiy Tarix'
        verbose_name_plural = 'Tibbiy Tarix'
        ordering = ['-diagnosed_at']
    
    def __str__(self):
        return f"{self.patient.get_full_name()}: {self.disease_name}"
