"""
Management command - Test malumotlarni yuklash.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.patients.models import Patient, Symptom
from apps.diagnostics.models import DiseasePattern


class Command(BaseCommand):
    help = "Test malumotlarni yuklash"
    
    def handle(self, *args, **options):
        self.stdout.write("Test malumotlarni yuklash boshlandi...")
        
        # Kasallik naqshlarini yaratish
        diseases = [
            {
                'name': 'Shamollash (ORVI)',
                'icd_code': 'J06.9',
                'description': 'Yuqori nafas yollari virusli infeksiyasi',
                'symptoms': {
                    'yotal': 0.8,
                    'burun bitishi': 0.9,
                    'tomoq ogrigi': 0.7,
                    'isitma': 0.6,
                    'bosh ogrigi': 0.5,
                    'charchoq': 0.6
                },
                'severity': 'LOW',
                'recommended_tests': ['Umumiy qon tahlili', 'CRP'],
                'treatment_options': 'Dam olish, kop suyuqlik ichish, simptomatik davolash',
                'prevention': 'Shaxsiy gigiena, immunitetni mustahkamlash'
            },
            {
                'name': 'Gripp',
                'icd_code': 'J11',
                'description': 'Gripp virusi infeksiyasi',
                'symptoms': {
                    'isitma': 0.9,
                    'bosh ogrigi': 0.8,
                    'mushak ogrigi': 0.8,
                    'charchoq': 0.9,
                    'yotal': 0.7,
                    'tomoq ogrigi': 0.6
                },
                'severity': 'MEDIUM',
                'recommended_tests': ['Gripp testi', 'Umumiy qon tahlili'],
                'treatment_options': 'Antivirus dorilar, dam olish, simptomatik davolash',
                'prevention': 'Emlash, shaxsiy gigiena'
            },
            {
                'name': 'Bronxit',
                'icd_code': 'J20',
                'description': 'Bronxlar yalliglanishi',
                'symptoms': {
                    'yotal': 0.9,
                    'balgam': 0.8,
                    'nafas qisilishi': 0.6,
                    'kokrak ogrigi': 0.5,
                    'isitma': 0.4
                },
                'severity': 'MEDIUM',
                'recommended_tests': ['Rentgen', 'Spirometriya', 'Balgam tahlili'],
                'treatment_options': 'Antibiotiklar (bakterial bolsa), bronxolitiklar, muqolitiklar',
                'prevention': 'Chekishni tashlab qoyish, immunitetni mustahkamlash'
            },
            {
                'name': 'Gastrit',
                'icd_code': 'K29',
                'description': 'Oshqozon shilliq qavatining yalliglanishi',
                'symptoms': {
                    'qorin ogrigi': 0.9,
                    'kongil aynishi': 0.7,
                    'ishtahasizlik': 0.6,
                    'qusish': 0.5,
                    'kokrak qafasida yonish': 0.6
                },
                'severity': 'MEDIUM',
                'recommended_tests': ['FGDS', 'Helicobacter pylori testi', 'Qon tahlili'],
                'treatment_options': 'Parhez, kislotani kamaytiruvchi dorilar, antibiotiklar (H.pylori bolsa)',
                'prevention': 'Togri ovqatlanish, stressdan qochish'
            },
            {
                'name': 'Migren',
                'icd_code': 'G43',
                'description': 'Kuchli bosh ogrigi',
                'symptoms': {
                    'bosh ogrigi': 1.0,
                    'kongil aynishi': 0.7,
                    'yoruglikdan qorqish': 0.6,
                    'shovqindan qorqish': 0.6,
                    'korish buzilishi': 0.4
                },
                'severity': 'MEDIUM',
                'recommended_tests': ['MRT', 'Nevrologik tekshiruv'],
                'treatment_options': 'Ogri qoldiruvchilar, triptanlar, profilaktik dorilar',
                'prevention': 'Stressdan qochish, muntazam uxlash, triggerlardan qochish'
            }
        ]
        
        for disease_data in diseases:
            disease, created = DiseasePattern.objects.get_or_create(
                name=disease_data['name'],
                defaults=disease_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ {disease.name} yaratildi'))
            else:
                self.stdout.write(f'  {disease.name} allaqachon mavjud')
        
        # Test bemorlarni yaratish
        patients_data = [
            {
                'first_name': 'Alisher',
                'last_name': 'Navoiy',
                'date_of_birth': timezone.now().date() - timedelta(days=365*35),
                'gender': 'M',
                'phone': '+998901234567',
                'email': 'alisher@example.uz'
            },
            {
                'first_name': 'Nodira',
                'last_name': 'Begim',
                'date_of_birth': timezone.now().date() - timedelta(days=365*28),
                'gender': 'F',
                'phone': '+998901234568',
                'email': 'nodira@example.uz'
            },
            {
                'first_name': 'Abdulla',
                'last_name': 'Qodiriy',
                'date_of_birth': timezone.now().date() - timedelta(days=365*42),
                'gender': 'M',
                'phone': '+998901234569',
                'email': 'abdulla@example.uz'
            }
        ]
        
        for patient_data in patients_data:
            patient, created = Patient.objects.get_or_create(
                email=patient_data['email'],
                defaults=patient_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ {patient.get_full_name()} yaratildi'))
                
                # Simptomlar qoshish
                Symptom.objects.create(
                    patient=patient,
                    name='Bosh ogrigi',
                    severity='MEDIUM',
                    started_at=timezone.now() - timedelta(days=2)
                )
            else:
                self.stdout.write(f'  {patient.get_full_name()} allaqachon mavjud')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Test malumotlar muvaffaqiyatli yuklandi!'))
        self.stdout.write(f'\nKasalliklar: {DiseasePattern.objects.count()}')
        self.stdout.write(f'Bemorlar: {Patient.objects.count()}')
