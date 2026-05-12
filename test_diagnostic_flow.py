"""
Diagnostika jarayonini test qilish scripti.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.patients.models import Patient
from apps.diagnostics.services import DiagnosticService
from apps.agents.coordinator_agent import CoordinatorAgent

print("=" * 60)
print("DIAGNOSTIKA JARAYONINI TEST QILISH")
print("=" * 60)

# Bemorni olish
try:
    patient = Patient.objects.first()
    if not patient:
        print("❌ Bemor topilmadi! Avval bemor yarating.")
        exit(1)
    
    print(f"\n✅ Bemor: {patient.get_full_name()}")
    print(f"   Yosh: {patient.get_age()} yosh")
    print(f"   Jins: {patient.get_gender_display()}")
    
    # Simptomlar
    symptoms = ["isitma", "bosh og'rig'i", "yo'tal", "mushak og'rig'i"]
    print(f"\n📋 Simptomlar: {', '.join(symptoms)}")
    
    # Session yaratish
    print("\n🔄 Diagnostika sessiyasini yaratish...")
    session = DiagnosticService.create_session(patient, symptoms)
    print(f"✅ Session yaratildi: {session.session_id}")
    
    # Test results
    test_results = {
        'temperature': 38.5
    }
    print(f"🌡️  Harorat: {test_results['temperature']}°C")
    
    # Diagnostika jarayonini boshlash
    print("\n🤖 Agentlar ishga tushmoqda...")
    print("   1/4: Simptomlar tahlili...")
    print("   2/4: Tahlillar baholash...")
    print("   3/4: Diagnoz qo'yish...")
    print("   4/4: Davolash rejasi...")
    
    coordinator = CoordinatorAgent()
    result = coordinator.execute({
        'session_id': session.session_id,
        'patient_id': patient.id,
        'symptoms': symptoms,
        'test_results': test_results
    })
    
    print("\n" + "=" * 60)
    print("✅ DIAGNOSTIKA MUVAFFAQIYATLI YAKUNLANDI!")
    print("=" * 60)
    
    # Natijalarni ko'rsatish
    session.refresh_from_db()
    results = session.results.all()
    
    print(f"\n📊 Topilgan kasalliklar: {results.count()}")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.disease.name}")
        print(f"   Ishonch darajasi: {result.get_confidence_percentage():.1f}%")
        print(f"   Og'irlik: {result.disease.get_severity_display()}")
        print(f"   Tavsif: {result.disease.description}")
    
    print(f"\n🔗 Natijalarni ko'rish: http://127.0.0.1:8080/dashboard/session/{session.session_id}/")
    print("\n" + "=" * 60)
    
except Exception as e:
    print(f"\n❌ Xatolik: {str(e)}")
    import traceback
    traceback.print_exc()
