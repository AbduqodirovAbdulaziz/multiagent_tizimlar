"""
Diagnostics signals - Django signals for diagnostics app.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.core.models import AgentLog
from .models import DiagnosticSession, DiagnosticResult


@receiver(post_save, sender=DiagnosticSession)
def log_session_status_change(sender, instance, created, **kwargs):
    """
    Diagnostika sessiyasi holati o'zgarganda log yozish.
    """
    if created:
        AgentLog.objects.create(
            agent_name='coordinator_agent',
            level='INFO',
            message=f"Yangi diagnostika sessiyasi yaratildi: {instance.session_id}",
            extra_data={
                'session_id': instance.session_id,
                'patient_id': instance.patient.id,
                'symptoms_count': len(instance.symptoms)
            }
        )
    elif instance.status == 'COMPLETED':
        AgentLog.objects.create(
            agent_name='coordinator_agent',
            level='INFO',
            message=f"Diagnostika sessiyasi yakunlandi: {instance.session_id}",
            extra_data={
                'session_id': instance.session_id,
                'duration': instance.get_duration(),
                'results_count': instance.results.count()
            }
        )
    elif instance.status == 'FAILED':
        AgentLog.objects.create(
            agent_name='coordinator_agent',
            level='ERROR',
            message=f"Diagnostika sessiyasi xatolik bilan yakunlandi: {instance.session_id}",
            extra_data={
                'session_id': instance.session_id,
                'error': instance.error_message
            }
        )


@receiver(post_save, sender=DiagnosticResult)
def log_result_creation(sender, instance, created, **kwargs):
    """
    Yangi diagnostika natijasi yaratilganda log yozish.
    """
    if created:
        AgentLog.objects.create(
            agent_name='diagnosis_agent',
            level='INFO',
            message=f"Yangi diagnoz qo'shildi: {instance.disease.name}",
            extra_data={
                'session_id': instance.session.session_id,
                'disease': instance.disease.name,
                'confidence': instance.confidence_score
            }
        )
