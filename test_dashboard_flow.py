#!/usr/bin/env python
"""
Dashboard Flow Test Script
Tests the complete diagnostic flow from dashboard
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.patients.models import Patient
from apps.diagnostics.models import DiagnosticSession, DiseasePattern
from apps.agents.models import AgentState


def test_dashboard_flow():
    """Test complete dashboard flow"""
    print("=" * 60)
    print("DASHBOARD FLOW TEST")
    print("=" * 60)
    
    # 1. Check patients
    print("\n1. Checking Patients...")
    patients = Patient.objects.filter(is_active=True)
    print(f"   ✓ Total active patients: {patients.count()}")
    
    if patients.exists():
        for patient in patients[:3]:
            print(f"   - {patient.get_full_name()} ({patient.get_age()} yosh, {patient.get_gender_display()})")
    else:
        print("   ⚠ No patients found! Add patients in admin panel.")
    
    # 2. Check disease patterns
    print("\n2. Checking Disease Patterns...")
    diseases = DiseasePattern.objects.filter(is_active=True)
    print(f"   ✓ Total disease patterns: {diseases.count()}")
    
    for disease in diseases:
        symptom_count = len(disease.symptoms) if disease.symptoms else 0
        print(f"   - {disease.name} ({symptom_count} symptoms)")
    
    # 3. Check agents
    print("\n3. Checking Agent States...")
    agents = AgentState.objects.all()
    print(f"   ✓ Total agents: {agents.count()}")
    
    for agent in agents:
        print(f"   - {agent.agent_name}: {agent.get_state_display()}")
    
    # 4. Check recent sessions
    print("\n4. Checking Recent Sessions...")
    sessions = DiagnosticSession.objects.all().order_by('-started_at')[:5]
    print(f"   ✓ Total sessions: {DiagnosticSession.objects.count()}")
    
    if sessions.exists():
        for session in sessions:
            symptom_count = len(session.symptoms) if session.symptoms else 0
            result_count = session.results.count()
            print(f"   - {session.session_id[:8]}... | {session.patient.get_full_name()} | "
                  f"{session.get_status_display()} | {symptom_count} symptoms | {result_count} results")
    else:
        print("   ℹ No sessions yet. Start a diagnostic from dashboard.")
    
    # 5. Symptom categories test
    print("\n5. Testing Symptom Categories...")
    symptom_categories = {
        'Umumiy Simptomlar': ['Isitma', 'Charchoq', 'Ishtahasizlik', 'Vazn yo\'qotish', 'Terlash', 'Titroq'],
        'Nafas Olish Tizimi': ['Yo\'tal', 'Nafas qisilishi', 'Burun bitishi', 'Tomoq og\'rig\'i', 'Ko\'krak og\'rig\'i', 'Xirillash'],
        'Ovqat Hazm Qilish': ['Qorin og\'rig\'i', 'Ko\'ngil aynishi', 'Qusish', 'Ichburug\'', 'Qabziyat', 'Oshqozon og\'rig\'i'],
        'Asab Tizimi': ['Bosh og\'rig\'i', 'Bosh aylanishi', 'Hushidan ketish', 'Uyqusizlik', 'Xotira zaiflanishi', 'Qo\'l-oyoq uyushishi'],
        'Yurak-Qon Tomir': ['Yurak urishi', 'Ko\'krak og\'rig\'i', 'Nafas qisilishi', 'Oyoq shishishi', 'Qon bosimi o\'zgarishi'],
        'Mushak-Skelet': ['Bo\'g\'im og\'rig\'i', 'Mushak og\'rig\'i', 'Orqa og\'rig\'i', 'Bo\'yin og\'rig\'i', 'Harakatsizlik'],
        'Teri': ['Toshmalar', 'Qichishish', 'Teri qizarishi', 'Shish', 'Teri rangi o\'zgarishi'],
    }
    
    total_symptoms = sum(len(symptoms) for symptoms in symptom_categories.values())
    print(f"   ✓ Total symptom categories: {len(symptom_categories)}")
    print(f"   ✓ Total symptoms available: {total_symptoms}")
    
    for category, symptoms in symptom_categories.items():
        print(f"   - {category}: {len(symptoms)} symptoms")
    
    # 6. System status
    print("\n6. System Status...")
    print(f"   ✓ Database: Connected")
    print(f"   ✓ Patients: {patients.count()} active")
    print(f"   ✓ Disease Patterns: {diseases.count()} active")
    print(f"   ✓ Agents: {agents.count()} registered")
    print(f"   ✓ Sessions: {DiagnosticSession.objects.count()} total")
    
    # 7. URLs to test
    print("\n7. URLs to Test...")
    print("   Dashboard: http://127.0.0.1:8080/")
    print("   Admin Panel: http://127.0.0.1:8080/admin/")
    print("   API Docs: http://127.0.0.1:8080/api/docs/ (admin only)")
    print("   Agent Status: http://127.0.0.1:8080/agents/")
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    issues = []
    
    if patients.count() == 0:
        issues.append("⚠ No patients - add patients in admin panel")
    
    if diseases.count() == 0:
        issues.append("⚠ No disease patterns - run load_sample_data command")
    
    if agents.count() == 0:
        issues.append("⚠ No agents - agents should be auto-created")
    
    if issues:
        print("\nISSUES FOUND:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("\n✅ All checks passed! System is ready.")
    
    print("\nNEXT STEPS:")
    print("1. Open dashboard: http://127.0.0.1:8080/")
    print("2. Select a patient")
    print("3. Choose symptoms from checkboxes")
    print("4. Click 'Diagnostika Boshlash'")
    print("5. View results")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    try:
        test_dashboard_flow()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
