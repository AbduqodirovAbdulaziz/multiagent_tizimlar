"""
Test bemor yaratish scripti.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.patients.models import Patient
from datetime import date

# Test bemor yaratish
patient = Patient.objects.create(
    first_name="Alisher",
    last_name="Karimov",
    date_of_birth=date(1990, 5, 15),
    gender="M",
    phone="+998901234567",
    email="alisher.karimov@example.com",
    address="Toshkent shahar, Yunusobod tumani",
    blood_type="A+",
    allergies=["Penitsil", "Yong'oq"],
    chronic_diseases=["Astma"],
    emergency_contact="Karimova Nodira, +998901234568, Xotini",
    is_active=True
)

print(f"✅ Test bemor yaratildi:")
print(f"   ID: {patient.id}")
print(f"   Ism: {patient.get_full_name()}")
print(f"   Yosh: {patient.get_age()} yosh")
print(f"   Jins: {patient.get_gender_display()}")
print(f"   Telefon: {patient.phone}")
