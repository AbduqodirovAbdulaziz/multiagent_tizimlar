"""
Celery konfiguratsiyasi - Agent vazifalarini asinxron bajarish uchun.

Bu modul Celery ilovasini sozlaydi va Django settings bilan integratsiya qiladi.
Barcha agent vazifalar Celery orqali parallel bajariladi.
"""
import os
from celery import Celery
from django.conf import settings

# Django settings modulini o'rnatish
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

app = Celery('medical_mas')

# Django settings'dan konfiguratsiya yuklash
# namespace='CELERY' - barcha celery sozlamalari CELERY_ prefiksi bilan boshlanadi
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django app'laridan task'larni avtomatik topish
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug uchun test task."""
    print(f'Request: {self.request!r}')
