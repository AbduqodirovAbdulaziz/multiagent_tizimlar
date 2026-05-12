"""
Test script to verify logical flow and data integrity.

This script tests:
1. Patient creation with all fields
2. Symptom and medical history
3. Disease pattern matching logic
4. Diagnostic session workflow
5. Agent coordination logic
6. Result generation and storage
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from datetime import date, datetime, timedelta
from apps.patients.models import Patient, Symptom, MedicalHistory
from apps.diagnostics.models import DiseasePattern, DiagnosticSession
from apps.agents.coordinator_agent import CoordinatorAgent
from apps.diagnostics.services import DiagnosticService


def test_logic_flow():
    """Test complete logical flow."""
    
    print("=" * 70)
    print("MEDICAL MULTIAGENT SYSTEM - LOGIC FLOW TEST")
    print("=" * 70)
    
    # 1. Test Patient Creation with Full Data
    print("\n1. Testing Patient Creation...")
    patient, created = Patient.objects.get_or_create(
        first_name="Ali",
        last_name="Valiyev",
        defaults={
            'middle_name': "Karimovich",
            'date_of_birth': date(1985, 5, 15),
            'gender': 'M',
            'phone': '+998901234567',
            'email': 'ali.valiyev@example.com',
            'blood_type': 'A+',
            'height': 175.0,
            'weight': 75.0,
            'address': 'Toshkent, Chilonzor tumani',
            'emergency_contact': '+998901234568',
            'allergies': ['Penitsil', 'Yong\'oq'],
            'chronic_diseases': ['Gipertoniya'],
            'notes': 'Muntazam tekshiruvdan o\'tadi',
        }
    )
    
    if created:
        print(f"   ✓ Yangi bemor yaratildi: {patient.get_full_name()}")
    else:
        print(f"   ✓ Mavjud bemor: {patient.get_full_name()}")
    
    print(f"   • Yosh: {patient.get_age()} yosh")
    print(f"   • BMI: {patient.get_bmi():.1f}")
    print(f"   • Qon guruhi: {patient.blood_type}")
    print(f"   • Allergiyalar: {', '.join(patient.allergies)}")
    
    # 2. Test Symptom Creation
    print("\n2. Testing Symptom Creation...")
    symptoms_data = [
        {
            'name': 'Yuqori isitma',
            'description': '39°C atrofida isitma, 3 kundan beri',
            'severity': 'HIGH',
            'started_at': datetime.now() - timedelta(days=3),
            'duration_days': 3
        },
        {
            'name': 'Bosh og\'rig\'i',
            'description': 'Doimiy bosh og\'rig\'i, og\'riq qoldiruvchilar yordam bermayapti',
            'severity': 'MEDIUM',
            'started_at': datetime.now() - timedelta(days=3),
            'duration_days': 3
        },
        {
            'name': 'Mushak og\'rig\'i',
            'description': 'Butun tanada mushak og\'rig\'i',
            'severity': 'MEDIUM',
            'started_at': datetime.now() - timedelta(days=2),
            'duration_days': 2
        }
    ]
    
    for symptom_data in symptoms_data:
        symptom, created = Symptom.objects.get_or_create(
            patient=patient,
            name=symptom_data['name'],
            defaults=symptom_data
        )
        if created:
            print(f"   ✓ Simptom qo'shildi: {symptom.name} ({symptom.severity})")
    
    # 3. Test Medical History
    print("\n3. Testing Medical History...")
    history, created = MedicalHistory.objects.get_or_create(
        patient=patient,
        disease_name="Shamollash",
        defaults={
            'diagnosed_at': date(2024, 1, 15),
            'treatment': 'Simptomatik davolash, dam olish',
            'outcome': 'RECOVERED',
            'doctor_name': 'Dr. Karimov',
            'notes': 'To\'liq tuzalib ketdi'
        }
    )
    if created:
        print(f"   ✓ Tibbiy tarix qo'shildi: {history.disease_name}")
    
    # 4. Test Disease Pattern Logic
    print("\n4. Testing Disease Pattern Matching Logic...")
    
    # Gripp kasalligi
    gripp, _ = DiseasePattern.objects.get_or_create(
        name="Gripp",
        defaults={
            'icd_code': 'J11',
            'description': 'Gripp virusli infeksiya',
            'symptoms': ['yuqori isitma', 'bosh og\'rig\'i', 'mushak og\'rig\'i', 'charchoq'],
            'severity': 'MEDIUM',
            'recommended_tests': ['Gripp testi', 'Umumiy qon tahlili', 'CRP'],
            'treatment_options': 'Antivirusli dorilar, dam olish, ko\'p suyuqlik ichish',
            'prevention': 'Emlash, gigiyena qoidalariga rioya qilish',
            'is_active': True
        }
    )
    
    # Test matching logic
    test_symptoms = ['yuqori isitma', 'bosh og\'rig\'i', 'mushak og\'rig\'i']
    match_score = gripp.calculate_match_score(test_symptoms)
    print(f"   ✓ Kasallik: {gripp.name}")
    print(f"   ✓ Simptomlar soni: {len(gripp.symptoms)}")
    print(f"   ✓ Match score: {match_score:.2%}")
    
    # 5. Test Diagnostic Service
    print("\n5. Testing Diagnostic Service...")
    
    # Find matching diseases
    matches = DiagnosticService.find_matching_diseases(test_symptoms, min_score=0.1)
    print(f"   ✓ Topilgan kasalliklar: {len(matches)}")
    for match in matches[:3]:
        print(f"      • {match['disease'].name}: {match['score']:.2%}")
    
    # 6. Test Complete Diagnostic Flow
    print("\n6. Testing Complete Diagnostic Flow...")
    
    # Create session
    session = DiagnosticService.create_session(patient, test_symptoms)
    print(f"   ✓ Session yaratildi: {session.session_id}")
    print(f"   ✓ Status: {session.status}")
    print(f"   ✓ Agent states: {list(session.agent_states.keys())}")
    
    # Run diagnostic
    coordinator = CoordinatorAgent()
    
    try:
        result = coordinator.execute({
            'session_id': session.session_id,
            'patient_id': patient.id,
            'symptoms': test_symptoms,
            'test_results': {
                'temperature': 39.0,
                'heart_rate': 95,
                'blood_pressure_systolic': 130,
                'blood_pressure_diastolic': 85
            }
        })
        
        print(f"   ✓ Diagnostika tugallandi!")
        print(f"   ✓ Status: {result['status']}")
        
        # 7. Test Results
        print("\n7. Testing Results and Data Integrity...")
        
        session.refresh_from_db()
        results = session.results.all()
        
        print(f"   ✓ Natijalar soni: {results.count()}")
        
        for idx, result in enumerate(results, 1):
            print(f"\n   Diagnoz #{idx}:")
            print(f"      • Kasallik: {result.disease.name}")
            print(f"      • ICD: {result.disease.icd_code}")
            print(f"      • Ishonch: {result.get_confidence_percentage():.1f}%")
            print(f"      • Og'irlik: {result.disease.severity}")
            print(f"      • Tavsiya etilgan tahlillar: {len(result.recommended_tests)}")
            
            # Check data integrity
            assert result.session == session, "Session bog'lanishi noto'g'ri"
            assert result.disease is not None, "Kasallik mavjud emas"
            assert 0 <= result.confidence_score <= 1, "Ishonch darajasi noto'g'ri"
            assert result.recommended_tests, "Tahlillar ro'yxati bo'sh"
            assert result.treatment_plan, "Davolash rejasi bo'sh"
        
        # 8. Test Agent States
        print("\n8. Testing Agent States...")
        for agent_name, state in session.agent_states.items():
            status_icon = "✓" if state == "completed" else "✗"
            print(f"   {status_icon} {agent_name}: {state}")
            assert state == "completed", f"{agent_name} tugallanmagan"
        
        # 9. Test Statistics
        print("\n9. Testing Statistics...")
        stats = DiagnosticService.get_session_statistics(session)
        print(f"   ✓ Jami natijalar: {stats['total_results']}")
        print(f"   ✓ O'rtacha ishonch: {stats['avg_confidence']:.2%}")
        print(f"   ✓ Eng yuqori diagnoz: {stats['top_disease']}")
        print(f"   ✓ Davomiyligi: {stats['duration']:.2f} soniya")
        
        # 10. Test Data Relationships
        print("\n10. Testing Data Relationships...")
        
        # Patient -> Symptoms
        patient_symptoms = patient.symptoms.count()
        print(f"   ✓ Bemor simptomlar: {patient_symptoms}")
        
        # Patient -> Medical History
        patient_history = patient.medical_history.count()
        print(f"   ✓ Bemor tibbiy tarix: {patient_history}")
        
        # Patient -> Diagnostic Sessions
        patient_sessions = patient.diagnostic_sessions.count()
        print(f"   ✓ Bemor sessiyalar: {patient_sessions}")
        
        # Session -> Results
        session_results = session.results.count()
        print(f"   ✓ Session natijalar: {session_results}")
        
        # Disease -> Results
        disease_results = gripp.diagnostic_results.count()
        print(f"   ✓ Kasallik natijalar: {disease_results}")
        
        # 11. Test Business Logic
        print("\n11. Testing Business Logic...")
        
        # Test session status transitions
        assert session.status == 'COMPLETED', "Session holati noto'g'ri"
        assert session.started_at is not None, "Boshlanish vaqti yo'q"
        assert session.completed_at is not None, "Tugash vaqti yo'q"
        assert session.completed_at > session.started_at, "Vaqt mantiqsiz"
        print("   ✓ Session holat o'zgarishlari to'g'ri")
        
        # Test confidence scores
        for result in results:
            assert 0 <= result.confidence_score <= 1, "Ishonch darajasi chegaradan tashqari"
        print("   ✓ Ishonch darajalari to'g'ri")
        
        # Test symptom severity logic
        for symptom in Symptom.objects.filter(patient=patient):
            assert symptom.severity in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'], "Og'irlik noto'g'ri"
        print("   ✓ Simptom og'irliklari to'g'ri")
        
        print("\n" + "=" * 70)
        print("LOGIC FLOW TEST COMPLETED SUCCESSFULLY! ✓")
        print("=" * 70)
        print("\n✅ Barcha mantiqiy tekshiruvlar o'tdi!")
        print("✅ Ma'lumotlar yaxlitligi tasdiqlandi!")
        print("✅ Agent koordinatsiyasi ishlayapti!")
        print("✅ Natijalar to'g'ri saqlanmoqda!")
        
        return True
        
    except Exception as e:
        print(f"\n   ✗ Xatolik: {str(e)}")
        import traceback
        traceback.print_exc()
        
        print("\n" + "=" * 70)
        print("LOGIC FLOW TEST FAILED! ✗")
        print("=" * 70)
        
        return False


if __name__ == '__main__':
    success = test_logic_flow()
    exit(0 if success else 1)
