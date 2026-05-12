"""
Clear demo data from database.

This script removes all demo/test data from the database.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.patients.models import Patient, Symptom, MedicalHistory
from apps.diagnostics.models import DiagnosticSession, DiagnosticResult, DiseasePattern
from apps.agents.models import AgentState
from apps.core.models import ACLMessage, AgentLog


def clear_demo_data():
    """Clear all demo data."""
    
    print("=" * 60)
    print("DEMO MA'LUMOTLARNI O'CHIRISH")
    print("=" * 60)
    
    # Confirm
    print("\n⚠️  DIQQAT: Barcha ma'lumotlar o'chiriladi!")
    print("   - Bemorlar")
    print("   - Simptomlar")
    print("   - Tibbiy tarix")
    print("   - Diagnostika sessiyalari")
    print("   - Diagnostika natijalari")
    print("   - Agent loglar")
    print("   - ACL xabarlar")
    print("\n❗ Kasallik naqshlari (Disease Patterns) saqlanadi!")
    
    confirm = input("\nDavom etishni xohlaysizmi? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("\n❌ Bekor qilindi.")
        return False
    
    print("\n🗑️  O'chirilmoqda...")
    
    # Count before
    patients_count = Patient.objects.count()
    symptoms_count = Symptom.objects.count()
    history_count = MedicalHistory.objects.count()
    sessions_count = DiagnosticSession.objects.count()
    results_count = DiagnosticResult.objects.count()
    logs_count = AgentLog.objects.count()
    messages_count = ACLMessage.objects.count()
    
    print(f"\n📊 Hozirgi holat:")
    print(f"   • Bemorlar: {patients_count}")
    print(f"   • Simptomlar: {symptoms_count}")
    print(f"   • Tibbiy tarix: {history_count}")
    print(f"   • Sessiyalar: {sessions_count}")
    print(f"   • Natijalar: {results_count}")
    print(f"   • Agent loglar: {logs_count}")
    print(f"   • ACL xabarlar: {messages_count}")
    
    # Delete
    print("\n🗑️  O'chirilmoqda...")
    
    # Order matters due to foreign keys
    DiagnosticResult.objects.all().delete()
    print("   ✓ Diagnostika natijalari o'chirildi")
    
    DiagnosticSession.objects.all().delete()
    print("   ✓ Diagnostika sessiyalari o'chirildi")
    
    MedicalHistory.objects.all().delete()
    print("   ✓ Tibbiy tarix o'chirildi")
    
    Symptom.objects.all().delete()
    print("   ✓ Simptomlar o'chirildi")
    
    Patient.objects.all().delete()
    print("   ✓ Bemorlar o'chirildi")
    
    AgentLog.objects.all().delete()
    print("   ✓ Agent loglar o'chirildi")
    
    ACLMessage.objects.all().delete()
    print("   ✓ ACL xabarlar o'chirildi")
    
    # Agent states - reset to IDLE
    AgentState.objects.all().update(state='IDLE', current_task='')
    print("   ✓ Agent holatlari reset qilindi")
    
    # Count after
    print(f"\n✅ Bajarildi!")
    print(f"\n📊 Yangi holat:")
    print(f"   • Bemorlar: {Patient.objects.count()}")
    print(f"   • Simptomlar: {Symptom.objects.count()}")
    print(f"   • Tibbiy tarix: {MedicalHistory.objects.count()}")
    print(f"   • Sessiyalar: {DiagnosticSession.objects.count()}")
    print(f"   • Natijalar: {DiagnosticResult.objects.count()}")
    print(f"   • Agent loglar: {AgentLog.objects.count()}")
    print(f"   • ACL xabarlar: {ACLMessage.objects.count()}")
    
    # Disease patterns
    disease_count = DiseasePattern.objects.count()
    print(f"\n💾 Saqlanganlar:")
    print(f"   • Kasallik naqshlari: {disease_count}")
    
    print("\n" + "=" * 60)
    print("DEMO MA'LUMOTLAR O'CHIRILDI! ✓")
    print("=" * 60)
    print("\n💡 Endi yangi bemorlar qo'shib, diagnostika qilishingiz mumkin!")
    print("   Dashboard: http://127.0.0.1:8080/")
    print("   Admin: http://127.0.0.1:8080/admin/")
    
    return True


if __name__ == '__main__':
    success = clear_demo_data()
    exit(0 if success else 1)
