"""
Patients managers - Custom model managers.
"""
from django.db import models
from django.utils import timezone


class PatientManager(models.Manager):
    """Patient model uchun custom manager."""
    
    def active(self):
        """Faol bemorlar."""
        return self.filter(is_active=True)
    
    def with_recent_symptoms(self, days=30):
        """So'nggi N kun ichida simptom ko'rsatgan bemorlar."""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        return self.filter(
            symptoms__created_at__gte=cutoff_date
        ).distinct()
    
    def by_age_range(self, min_age, max_age):
        """Yosh oralig'i bo'yicha bemorlar."""
        today = timezone.now().date()
        max_birth_date = today.replace(year=today.year - min_age)
        min_birth_date = today.replace(year=today.year - max_age)
        
        return self.filter(
            date_of_birth__gte=min_birth_date,
            date_of_birth__lte=max_birth_date
        )


class SymptomManager(models.Manager):
    """Symptom model uchun custom manager."""
    
    def by_severity(self, severity):
        """Og'irlik darajasi bo'yicha simptomlar."""
        return self.filter(severity=severity)
    
    def critical(self):
        """Kritik simptomlar."""
        return self.filter(severity='CRITICAL')
    
    def recent(self, days=7):
        """So'nggi N kun ichidagi simptomlar."""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        return self.filter(created_at__gte=cutoff_date)
