"""
Test script to verify the complete diagnostic flow.

This script tests:
1. Patient creation
2. Symptom recording
3. Diagnostic session creation
4. Agent coordination
5. Results generation
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.patients.models import Patient
from apps.diagnostics.models import DiseasePattern, DiagnosticSession
from apps.agents.coordinator_agent import CoordinatorAgent
from apps.diagnostics.services import DiagnosticService


def test_diagnostic_flow():
    """Test complete diagnostic flow."""
    
    print("=" * 60)
    print("MEDICAL MULTIAGENT SYSTEM - DIAGNOSTIC FLOW TEST")
    print("=" * 60)
    
    # 1. Create or get test patient
    print("\n1. Creating test patient...")
    patient, created = Patient.objects.get_or_create(
        first_name="Test",
        last_name="Patient",
        defaults={
            'date_of_birth': '1990-01-01',
            'gender': 'M',
            'phone': '+998901234567',
            'email': 'test@example.com',
            'blood_type': 'A+',
            'height': 175.0,
            'weight': 70.0,
        }
    )
    
    if created:
        print(f"   ✓ New patient created: {patient.get_full_name()}")
    else:
        print(f"   ✓ Using existing patient: {patient.get_full_name()}")
    
    # 2. Create test disease patterns if not exist
    print("\n2. Checking disease patterns...")
    disease_count = DiseasePattern.objects.count()
    
    if disease_count == 0:
        print("   ! No disease patterns found. Creating sample diseases...")
        
        DiseasePattern.objects.create(
            name="Shamollash (ARVI)",
            icd_code="J06.9",
            description="Yuqori nafas yo'llari virusli infeksiyasi",
            symptoms=["isitma", "bosh og'rig'i", "yo'tal", "burun bitishi"],
            severity="MEDIUM",
            recommended_tests=["Umumiy qon tahlili", "Temperatura o'lchash"],
            treatment_options="Dam olish, ko'p suyuqlik ichish, simptomatik davolash",
            prevention="Gigiyena qoidalariga rioya qilish, immunitetni mustahkamlash",
            is_active=True
        )
        
        DiseasePattern.objects.create(
            name="Gripp",
            icd_code="J11.1",
            description="Gripp virusli infeksiya",
            symptoms=["yuqori isitma", "bosh og'rig'i", "mushak og'rig'i", "charchoq"],
            severity="HIGH",
            recommended_tests=["Gripp testi", "Umumiy qon tahlili"],
            treatment_options="Antivirusli dorilar, dam olish, ko'p suyuqlik",
            prevention="Emlash, gigiyena",
            is_active=True
        )
        
        print(f"   ✓ Created 2 sample disease patterns")
    else:
        print(f"   ✓ Found {disease_count} disease patterns")
    
    # 3. Create diagnostic session
    print("\n3. Creating diagnostic session...")
    symptoms = ["isitma", "bosh og'rig'i", "yo'tal"]
    session = DiagnosticService.create_session(patient, symptoms)
    print(f"   ✓ Session created: {session.session_id}")
    print(f"   ✓ Status: {session.status}")
    print(f"   ✓ Symptoms: {', '.join(symptoms)}")
    
    # 4. Run diagnostic process
    print("\n4. Running diagnostic process...")
    print("   → Initializing coordinator agent...")
    
    coordinator = CoordinatorAgent()
    
    try:
        print("   → Starting agent coordination...")
        result = coordinator.execute({
            'session_id': session.session_id,
            'patient_id': patient.id,
            'symptoms': symptoms,
            'test_results': {'temperature': 38.5}
        })
        
        print(f"   ✓ Diagnostic process completed!")
        print(f"   ✓ Status: {result['status']}")
        
        # 5. Display results
        print("\n5. Diagnostic Results:")
        print("-" * 60)
        
        session.refresh_from_db()
        results = session.results.all()
        
        if results.exists():
            for idx, result in enumerate(results, 1):
                print(f"\n   Diagnosis #{idx}:")
                print(f"   • Disease: {result.disease.name}")
                print(f"   • ICD Code: {result.disease.icd_code}")
                print(f"   • Confidence: {result.get_confidence_percentage():.1f}%")
                print(f"   • Severity: {result.disease.severity}")
                print(f"   • Recommended Tests: {', '.join(result.recommended_tests)}")
        else:
            print("   ! No diagnostic results found")
        
        # 6. Agent states
        print("\n6. Agent States:")
        print("-" * 60)
        for agent_name, state in session.agent_states.items():
            status_icon = "✓" if state == "completed" else "✗"
            print(f"   {status_icon} {agent_name}: {state}")
        
        # 7. Session statistics
        print("\n7. Session Statistics:")
        print("-" * 60)
        stats = DiagnosticService.get_session_statistics(session)
        print(f"   • Total Results: {stats['total_results']}")
        print(f"   • Average Confidence: {stats['avg_confidence']:.2f}")
        print(f"   • Top Disease: {stats['top_disease']}")
        print(f"   • Duration: {stats['duration']:.2f} seconds")
        
        print("\n" + "=" * 60)
        print("TEST COMPLETED SUCCESSFULLY! ✓")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n   ✗ Error during diagnostic process: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        
        print("\n" + "=" * 60)
        print("TEST FAILED! ✗")
        print("=" * 60)
        
        return False


if __name__ == '__main__':
    success = test_diagnostic_flow()
    exit(0 if success else 1)
