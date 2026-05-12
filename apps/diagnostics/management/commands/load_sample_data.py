"""
Management command - Test malumotlarni yuklash.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.patients.models import Patient
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
                'description': 'Yuqori nafas yollari virusli infeksiyasi. Eng keng tarqalgan kasalliklardan biri.',
                'symptoms': {
                    'Yo\'tal': 0.8,
                    'Burun bitishi': 0.9,
                    'Tomoq og\'rig\'i': 0.7,
                    'Isitma': 0.6,
                    'Bosh og\'rig\'i': 0.5,
                    'Charchoq': 0.6,
                    'Xirillash': 0.4
                },
                'severity': 'LOW',
                'recommended_tests': ['Umumiy qon tahlili', 'CRP', 'ESR'],
                'treatment_options': 'Dam olish, ko\'p suyuqlik ichish (2-3 litr/kun), simptomatik davolash, vitamin C, paratsetamol (isitma uchun)',
                'prevention': 'Shaxsiy gigiena, qo\'llarni tez-tez yuvish, immunitetni mustahkamlash, vitaminlar qabul qilish'
            },
            {
                'name': 'Gripp',
                'icd_code': 'J11',
                'description': 'Gripp virusi infeksiyasi. Yuqori isitma va kuchli intoksikatsiya bilan kechadi.',
                'symptoms': {
                    'Isitma': 0.9,
                    'Bosh og\'rig\'i': 0.8,
                    'Mushak og\'rig\'i': 0.8,
                    'Charchoq': 0.9,
                    'Yo\'tal': 0.7,
                    'Tomoq og\'rig\'i': 0.6,
                    'Titroq': 0.7,
                    'Terlash': 0.6
                },
                'severity': 'MEDIUM',
                'recommended_tests': ['Gripp testi (PCR)', 'Umumiy qon tahlili', 'Ko\'krak qafasi rentgeni'],
                'treatment_options': 'Antivirus dorilar (Oseltamivir, Zanamivir), dam olish, ko\'p suyuqlik ichish, simptomatik davolash',
                'prevention': 'Yillik emlash, shaxsiy gigiena, ommaviy joylarda niqob taqish'
            },
            {
                'name': 'Bronxit',
                'icd_code': 'J20',
                'description': 'Bronxlar shilliq qavatining yallig\'lanishi. O\'tkir va surunkali shakllari mavjud.',
                'symptoms': {
                    'Yo\'tal': 0.9,
                    'Nafas qisilishi': 0.6,
                    'Ko\'krak og\'rig\'i': 0.5,
                    'Isitma': 0.4,
                    'Xirillash': 0.7,
                    'Charchoq': 0.5
                },
                'severity': 'MEDIUM',
                'recommended_tests': ['Ko\'krak qafasi rentgeni', 'Spirometriya', 'Balgam tahlili', 'Umumiy qon tahlili'],
                'treatment_options': 'Antibiotiklar (bakterial bo\'lsa), bronxolitiklar (Salbutamol), muqolitiklar, ko\'p suyuqlik ichish, nafas mashqlari',
                'prevention': 'Chekishni tashlab qo\'yish, immunitetni mustahkamlash, sovuqdan saqlanish'
            },
            {
                'name': 'Gastrit',
                'icd_code': 'K29',
                'description': 'Oshqozon shilliq qavatining yallig\'lanishi. Ko\'pincha noto\'g\'ri ovqatlanish va stress natijasida rivojlanadi.',
                'symptoms': {
                    'Qorin og\'rig\'i': 0.9,
                    'Ko\'ngil aynishi': 0.7,
                    'Ishtahasizlik': 0.6,
                    'Qusish': 0.5,
                    'Oshqozon og\'rig\'i': 0.8
                },
                'severity': 'MEDIUM',
                'recommended_tests': ['FGDS (fibrogastroduodenoskopiya)', 'Helicobacter pylori testi', 'Qon tahlili', 'Koprogramma'],
                'treatment_options': 'Parhez (achchiq, yog\'li, qovurilgan ovqatlardan voz kechish), kislotani kamaytiruvchi dorilar (Omeprazol), antibiotiklar (H.pylori bo\'lsa)',
                'prevention': 'To\'g\'ri ovqatlanish, stressdan qochish, alkogol va chekishni tashlab qo\'yish'
            },
            {
                'name': 'Migren',
                'icd_code': 'G43',
                'description': 'Kuchli, pulsatsiyalanuvchi bosh og\'rig\'i. Ko\'pincha bir tomonlama bo\'ladi.',
                'symptoms': {
                    'Bosh og\'rig\'i': 1.0,
                    'Ko\'ngil aynishi': 0.7,
                    'Qusish': 0.5,
                    'Bosh aylanishi': 0.6,
                    'Uyqusizlik': 0.5
                },
                'severity': 'MEDIUM',
                'recommended_tests': ['MRT (magnit-rezonans tomografiya)', 'Nevrologik tekshiruv', 'Qon bosimi monitoring'],
                'treatment_options': 'Og\'riq qoldiruvchilar (Ibuprofen, Paratsetamol), triptanlar (Sumatriptan), profilaktik dorilar, dam olish, qorong\'i xonada yotish',
                'prevention': 'Stressdan qochish, muntazam uxlash, triggerlardan (shokolad, qizil sharob, sir) qochish'
            },
            {
                'name': 'Pnevmoniya',
                'icd_code': 'J18',
                'description': 'O\'pka to\'qimasining yallig\'lanishi. Bakterial, virusli yoki zamburug\'li bo\'lishi mumkin.',
                'symptoms': {
                    'Yo\'tal': 0.9,
                    'Isitma': 0.9,
                    'Nafas qisilishi': 0.8,
                    'Ko\'krak og\'rig\'i': 0.7,
                    'Charchoq': 0.8,
                    'Terlash': 0.7,
                    'Titroq': 0.6
                },
                'severity': 'HIGH',
                'recommended_tests': ['Ko\'krak qafasi rentgeni', 'Umumiy qon tahlili', 'Balgam tahlili', 'Qon kultura', 'SpO2 monitoring'],
                'treatment_options': 'Antibiotiklar (Amoksitsillin, Azitromitsin), kasalxonaga yotqizish (og\'ir holatlarda), kislorod terapiyasi, ko\'p suyuqlik ichish',
                'prevention': 'Emlash (pnevmokokk vaksinasi), immunitetni mustahkamlash, chekishni tashlab qo\'yish'
            },
            {
                'name': 'Angina (Tonzillit)',
                'icd_code': 'J03',
                'description': 'Bodomsimon bezlarning o\'tkir yallig\'lanishi. Ko\'pincha bakterial infeksiya natijasida.',
                'symptoms': {
                    'Tomoq og\'rig\'i': 0.9,
                    'Isitma': 0.8,
                    'Yutishda og\'riq': 0.9,
                    'Bosh og\'rig\'i': 0.6,
                    'Charchoq': 0.7,
                    'Bo\'g\'im og\'rig\'i': 0.5
                },
                'severity': 'MEDIUM',
                'recommended_tests': ['Tomoq smear', 'Umumiy qon tahlili', 'ASL-O (antistreptolizin)', 'CRP'],
                'treatment_options': 'Antibiotiklar (Amoksitsillin, Azitromitsin), tomoqni chayish (sho\'r suv, antiseptiklar), og\'riq qoldiruvchilar, ko\'p suyuqlik ichish',
                'prevention': 'Shaxsiy gigiena, immunitetni mustahkamlash, sovuqdan saqlanish'
            },
            {
                'name': 'Gipertoniya',
                'icd_code': 'I10',
                'description': 'Arterial qon bosimining doimiy ko\'tarilishi (140/90 mm Hg dan yuqori).',
                'symptoms': {
                    'Bosh og\'rig\'i': 0.8,
                    'Bosh aylanishi': 0.7,
                    'Yurak urishi': 0.6,
                    'Ko\'krak og\'rig\'i': 0.5,
                    'Nafas qisilishi': 0.5,
                    'Qon bosimi o\'zgarishi': 1.0
                },
                'severity': 'HIGH',
                'recommended_tests': ['Qon bosimi monitoring (24 soat)', 'EKG', 'Exo-KG', 'Qon tahlili (lipidlar, glyukoza)', 'Buyrak funksiyasi'],
                'treatment_options': 'Antihipertenziv dorilar (ACE inhibitorlari, beta-blokatorlar, diuretiklar), parhez (tuz cheklash), vazn yo\'qotish, jismoniy faollik',
                'prevention': 'Sog\'lom turmush tarzi, tuzni cheklash, vazn nazorati, stress boshqaruvi, muntazam jismoniy mashqlar'
            },
            {
                'name': 'Diabet (Qandli diabet)',
                'icd_code': 'E11',
                'description': 'Qondagi glyukoza darajasining doimiy ko\'tarilishi. 2-tip diabet eng keng tarqalgan.',
                'symptoms': {
                    'Tashnalik': 0.8,
                    'Tez-tez siydik chiqarish': 0.9,
                    'Vazn yo\'qotish': 0.7,
                    'Charchoq': 0.8,
                    'Ko\'rish buzilishi': 0.6,
                    'Ishtahasizlik': 0.5
                },
                'severity': 'HIGH',
                'recommended_tests': ['Qondagi glyukoza', 'HbA1c (glikirlanган gemoglobin)', 'Siydik tahlili', 'Lipid profili', 'Buyrak funksiyasi'],
                'treatment_options': 'Parhez (uglevodlarni cheklash), jismoniy faollik, og\'iz orqali qabul qilinadigan dorilar (Metformin), insulin (kerak bo\'lsa), qon shakarini monitoring',
                'prevention': 'Sog\'lom ovqatlanish, muntazam jismoniy mashqlar, vazn nazorati, stress boshqaruvi'
            },
            {
                'name': 'Allergik rinit',
                'icd_code': 'J30',
                'description': 'Burun shilliq qavatining allergik yallig\'lanishi. Mavsumiy yoki yil davomida bo\'lishi mumkin.',
                'symptoms': {
                    'Burun bitishi': 0.9,
                    'Aksirish': 0.9,
                    'Burundan suv oqishi': 0.8,
                    'Qichishish': 0.7,
                    'Ko\'z qizarishi': 0.6,
                    'Bosh og\'rig\'i': 0.5
                },
                'severity': 'LOW',
                'recommended_tests': ['Teri prik-testi', 'IgE tahlili', 'Qon tahlili (eozinofil)', 'Allergologik tekshiruv'],
                'treatment_options': 'Antihistamin dorilar (Loratadin, Tsetirizin), burun spreylari (kortikosteroidlar), allergenlardan qochish, immunoterapiya',
                'prevention': 'Allergenlardan qochish, uy tozaligi, havo filtrlari, mavsumiy profilaktika'
            },
            {
                'name': 'Osteoartrit',
                'icd_code': 'M19',
                'description': 'Bo\'g\'imlar xaftasining degenerativ kasalligi. Ko\'pincha keksaroq yoshda uchraydi.',
                'symptoms': {
                    'Bo\'g\'im og\'rig\'i': 0.9,
                    'Harakatsizlik': 0.8,
                    'Bo\'g\'im shishi': 0.6,
                    'Ertalabki qotishish': 0.7,
                    'Mushak og\'rig\'i': 0.5
                },
                'severity': 'MEDIUM',
                'recommended_tests': ['Bo\'g\'im rentgeni', 'MRT', 'Qon tahlili (revmatoid faktor)', 'Sinovial suyuqlik tahlili'],
                'treatment_options': 'Og\'riq qoldiruvchilar (NSAIDs), fizioterapiya, jismoniy mashqlar, vazn yo\'qotish, bo\'g\'im protezlash (og\'ir holatlarda)',
                'prevention': 'Vazn nazorati, muntazam jismoniy mashqlar, bo\'g\'imlarga haddan tashqari yuk bermaslik'
            },
            {
                'name': 'Depressiya',
                'icd_code': 'F32',
                'description': 'Ruhiy kasallik, kayfiyatning doimiy pasayishi va qiziqishlarni yo\'qotish bilan tavsiflanadi.',
                'symptoms': {
                    'Kayfiyat pasayishi': 0.9,
                    'Qiziqishlarni yo\'qotish': 0.8,
                    'Uyqusizlik': 0.7,
                    'Charchoq': 0.8,
                    'Ishtahasizlik': 0.6,
                    'Xotira zaiflanishi': 0.6,
                    'Vazn yo\'qotish': 0.5
                },
                'severity': 'MEDIUM',
                'recommended_tests': ['Psixologik test (Beck depressiya shkalasi)', 'Gormon tahlillari (tiroid)', 'Vitamin D darajasi'],
                'treatment_options': 'Antidepressantlar (SSRI), psixoterapiya (kognitiv-xulq-atvor terapiyasi), jismoniy faollik, ijtimoiy qo\'llab-quvvatlash',
                'prevention': 'Stress boshqaruvi, ijtimoiy aloqalar, muntazam jismoniy mashqlar, sog\'lom uyqu rejimi'
            },
            {
                'name': 'Sistit',
                'icd_code': 'N30',
                'description': 'Siydik pufagining yallig\'lanishi. Ko\'proq ayollarda uchraydi.',
                'symptoms': {
                    'Tez-tez siydik chiqarish': 0.9,
                    'Siydik chiqarishda og\'riq': 0.9,
                    'Qorin og\'rig\'i': 0.7,
                    'Siydikda qon': 0.5,
                    'Isitma': 0.4
                },
                'severity': 'MEDIUM',
                'recommended_tests': ['Umumiy siydik tahlili', 'Siydik kultura', 'Ultratovush (buyrak va siydik pufagi)', 'Qon tahlili'],
                'treatment_options': 'Antibiotiklar (Nitrofurantoin, Fosfomitsin), ko\'p suyuqlik ichish, og\'riq qoldiruvchilar, issiq kompresslar',
                'prevention': 'Shaxsiy gigiena, ko\'p suyuqlik ichish, siydikni ushlab turmaslik, to\'g\'ri kiyinish'
            },
            {
                'name': 'Konjunktivit',
                'icd_code': 'H10',
                'description': 'Ko\'z konyunktivasi (oq qismining) yallig\'lanishi. Virusli, bakterial yoki allergik bo\'lishi mumkin.',
                'symptoms': {
                    'Ko\'z qizarishi': 0.9,
                    'Ko\'zdan ajralma': 0.7,
                    'Qichishish': 0.8,
                    'Yosh kelishi': 0.7,
                    'Yorug\'likdan qorqish': 0.5
                },
                'severity': 'LOW',
                'recommended_tests': ['Ko\'z tekshiruvi', 'Ajralma tahlili (bakterial bo\'lsa)', 'Allergik testlar'],
                'treatment_options': 'Antibiotik tomchilar (bakterial), antivirus dorilar (virusli), antihistamin tomchilar (allergik), ko\'zni toza tutish',
                'prevention': 'Shaxsiy gigiena, qo\'llarni tez-tez yuvish, ko\'zni ishqalamaslik, sochiqlarni almashtirish'
            },
            {
                'name': 'Otit (Quloq yallig\'lanishi)',
                'icd_code': 'H66',
                'description': 'O\'rta quloqning yallig\'lanishi. Ko\'proq bolalarda uchraydi.',
                'symptoms': {
                    'Quloq og\'rig\'i': 0.9,
                    'Isitma': 0.7,
                    'Eshitish pasayishi': 0.6,
                    'Quloqdan ajralma': 0.5,
                    'Bosh og\'rig\'i': 0.5
                },
                'severity': 'MEDIUM',
                'recommended_tests': ['Otoskopiya', 'Timpanometriya', 'Audiometriya', 'Qon tahlili'],
                'treatment_options': 'Antibiotiklar (Amoksitsillin), og\'riq qoldiruvchilar, quloq tomchilari, issiq kompresslar',
                'prevention': 'Shamollashni davolash, quloqni toza tutish, chekish tutunidan qochish'
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
                'middle_name': 'Nizomiddin o\'g\'li',
                'date_of_birth': timezone.now().date() - timedelta(days=365*35),
                'gender': 'M',
                'blood_type': 'A+',
                'phone': '+998901234567',
                'email': 'alisher.navoiy@example.uz',
                'address': 'Toshkent sh., Yunusobod t., Amir Temur ko\'chasi, 15-uy',
                'allergies': ['Penitsil'],
                'chronic_diseases': [],
                'emergency_contact': '+998901234566 (Ona - Dilbar Navoiy)'
            },
            {
                'first_name': 'Nodira',
                'last_name': 'Begim',
                'middle_name': 'Komiljon qizi',
                'date_of_birth': timezone.now().date() - timedelta(days=365*28),
                'gender': 'F',
                'blood_type': 'B+',
                'phone': '+998901234568',
                'email': 'nodira.begim@example.uz',
                'address': 'Toshkent sh., Chilonzor t., Bunyodkor ko\'chasi, 42-uy',
                'allergies': ['Yong\'oq', 'Asal'],
                'chronic_diseases': ['Allergik rinit'],
                'emergency_contact': '+998901234569 (Ota - Komiljon Begimov)'
            },
            {
                'first_name': 'Abdulla',
                'last_name': 'Qodiriy',
                'middle_name': 'Shavkat o\'g\'li',
                'date_of_birth': timezone.now().date() - timedelta(days=365*42),
                'gender': 'M',
                'blood_type': 'O+',
                'phone': '+998901234570',
                'email': 'abdulla.qodiriy@example.uz',
                'address': 'Toshkent sh., Mirzo Ulug\'bek t., Mustaqillik ko\'chasi, 78-uy',
                'allergies': [],
                'chronic_diseases': ['Gipertoniya', 'Diabet 2-tip'],
                'emergency_contact': '+998901234571 (Xotin - Malika Qodiriy)'
            },
            {
                'first_name': 'Zulfiya',
                'last_name': 'Ismoilova',
                'middle_name': 'Rustam qizi',
                'date_of_birth': timezone.now().date() - timedelta(days=365*31),
                'gender': 'F',
                'blood_type': 'AB+',
                'phone': '+998901234572',
                'email': 'zulfiya.ismoilova@example.uz',
                'address': 'Toshkent sh., Yakkasaroy t., Shota Rustaveli ko\'chasi, 23-uy',
                'allergies': ['Antibiotiklar (Penitsil guruhi)'],
                'chronic_diseases': [],
                'emergency_contact': '+998901234573 (Ona - Dilnoza Ismoilova)'
            },
            {
                'first_name': 'Bobur',
                'last_name': 'Mirzo',
                'middle_name': 'Umar o\'g\'li',
                'date_of_birth': timezone.now().date() - timedelta(days=365*38),
                'gender': 'M',
                'blood_type': 'A-',
                'phone': '+998901234574',
                'email': 'bobur.mirzo@example.uz',
                'address': 'Toshkent sh., Sergeli t., Yangi Sergeli ko\'chasi, 56-uy',
                'allergies': [],
                'chronic_diseases': ['Bronxial astma'],
                'emergency_contact': '+998901234575 (Xotin - Gulnora Mirzo)'
            },
            {
                'first_name': 'Saida',
                'last_name': 'Rahimova',
                'middle_name': 'Aziz qizi',
                'date_of_birth': timezone.now().date() - timedelta(days=365*25),
                'gender': 'F',
                'blood_type': 'B-',
                'phone': '+998901234576',
                'email': 'saida.rahimova@example.uz',
                'address': 'Toshkent sh., Uchtepa t., Farobiy ko\'chasi, 89-uy',
                'allergies': ['Qizil meva', 'Sitrus'],
                'chronic_diseases': [],
                'emergency_contact': '+998901234577 (Ota - Aziz Rahimov)'
            },
            {
                'first_name': 'Jamshid',
                'last_name': 'Karimov',
                'middle_name': 'Akbar o\'g\'li',
                'date_of_birth': timezone.now().date() - timedelta(days=365*55),
                'gender': 'M',
                'blood_type': 'O-',
                'phone': '+998901234578',
                'email': 'jamshid.karimov@example.uz',
                'address': 'Toshkent sh., Bektemir t., Navoi ko\'chasi, 34-uy',
                'allergies': [],
                'chronic_diseases': ['Gipertoniya', 'Osteoartrit'],
                'emergency_contact': '+998901234579 (O\'g\'il - Akmal Karimov)'
            },
            {
                'first_name': 'Dilnoza',
                'last_name': 'Tursunova',
                'middle_name': 'Olim qizi',
                'date_of_birth': timezone.now().date() - timedelta(days=365*33),
                'gender': 'F',
                'blood_type': 'A+',
                'phone': '+998901234580',
                'email': 'dilnoza.tursunova@example.uz',
                'address': 'Toshkent sh., Shayxontohur t., Labzak ko\'chasi, 67-uy',
                'allergies': ['Changga allergiya'],
                'chronic_diseases': ['Migren'],
                'emergency_contact': '+998901234581 (Er - Olim Tursunov)'
            },
            {
                'first_name': 'Rustam',
                'last_name': 'Usmonov',
                'middle_name': 'Vali o\'g\'li',
                'date_of_birth': timezone.now().date() - timedelta(days=365*29),
                'gender': 'M',
                'blood_type': 'B+',
                'phone': '+998901234582',
                'email': 'rustam.usmonov@example.uz',
                'address': 'Toshkent sh., Yashnobod t., Qatortol ko\'chasi, 12-uy',
                'allergies': [],
                'chronic_diseases': [],
                'emergency_contact': '+998901234583 (Ona - Malika Usmonova)'
            },
            {
                'first_name': 'Malika',
                'last_name': 'Azimova',
                'middle_name': 'Sardor qizi',
                'date_of_birth': timezone.now().date() - timedelta(days=365*27),
                'gender': 'F',
                'blood_type': 'AB-',
                'phone': '+998901234584',
                'email': 'malika.azimova@example.uz',
                'address': 'Toshkent sh., Olmazor t., Shifokorlar ko\'chasi, 45-uy',
                'allergies': ['Dori allergiyasi (Aspirin)'],
                'chronic_diseases': [],
                'emergency_contact': '+998901234585 (Ota - Sardor Azimov)'
            }
        ]
        
        for patient_data in patients_data:
            patient, created = Patient.objects.get_or_create(
                email=patient_data['email'],
                defaults=patient_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ {patient.get_full_name()} yaratildi'))
            else:
                self.stdout.write(f'  {patient.get_full_name()} allaqachon mavjud')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Test malumotlar muvaffaqiyatli yuklandi!'))
        self.stdout.write(f'\nKasalliklar: {DiseasePattern.objects.count()}')
        self.stdout.write(f'Bemorlar: {Patient.objects.count()}')
        self.stdout.write('\n' + '='*60)
        self.stdout.write('KASALLIK NAQSHLARI:')
        self.stdout.write('='*60)
        for disease in DiseasePattern.objects.all():
            self.stdout.write(f'  • {disease.name} ({disease.icd_code}) - {disease.get_severity_display()}')
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write('DEMO BEMORLAR:')
        self.stdout.write('='*60)
        for patient in Patient.objects.all()[:10]:
            age = patient.get_age()
            chronic = ', '.join(patient.chronic_diseases) if patient.chronic_diseases else 'Yo\'q'
            self.stdout.write(f'  • {patient.get_full_name()} - {age} yosh, {patient.blood_type}, Surunkali: {chronic}')
