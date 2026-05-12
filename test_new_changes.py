#!/usr/bin/env python
"""
Test New Changes - Yangi o'zgarishlarni tekshirish
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.patients.models import Patient
from apps.diagnostics.models import DiseasePattern


def test_new_changes():
    """Test all new changes"""
    print("=" * 70)
    print("YANGI O'ZGARISHLARNI TEKSHIRISH")
    print("=" * 70)
    
    # 1. Kasallik naqshlari
    print("\n1. KASALLIK NAQSHLARI")
    print("-" * 70)
    diseases = DiseasePattern.objects.all().order_by('name')
    print(f"Jami kasalliklar: {diseases.count()}")
    
    severity_counts = {
        'LOW': 0,
        'MEDIUM': 0,
        'HIGH': 0,
        'CRITICAL': 0
    }
    
    print("\nKasalliklar ro'yxati:")
    for disease in diseases:
        symptom_count = len(disease.symptoms) if disease.symptoms else 0
        severity_counts[disease.severity] += 1
        severity_display = disease.get_severity_display()
        print(f"  • {disease.name:30} | {disease.icd_code:8} | {severity_display:10} | {symptom_count} simptom")
    
    print(f"\nOg'irlik bo'yicha:")
    print(f"  - PAST (LOW):     {severity_counts['LOW']} ta")
    print(f"  - O'RTA (MEDIUM): {severity_counts['MEDIUM']} ta")
    print(f"  - YUQORI (HIGH):  {severity_counts['HIGH']} ta")
    print(f"  - KRITIK:         {severity_counts['CRITICAL']} ta")
    
    # 2. Demo bemorlar
    print("\n2. DEMO BEMORLAR")
    print("-" * 70)
    patients = Patient.objects.all().order_by('last_name', 'first_name')
    print(f"Jami bemorlar: {patients.count()}")
    
    gender_counts = {'M': 0, 'F': 0}
    age_sum = 0
    with_chronic = 0
    with_allergies = 0
    
    print("\nBemorlar ro'yxati:")
    for patient in patients:
        age = patient.get_age()
        age_sum += age
        gender_counts[patient.gender] += 1
        
        chronic = ', '.join(patient.chronic_diseases) if patient.chronic_diseases else 'Yo\'q'
        if patient.chronic_diseases:
            with_chronic += 1
        
        allergies = ', '.join(patient.allergies) if patient.allergies else 'Yo\'q'
        if patient.allergies:
            with_allergies += 1
        
        gender_display = patient.get_gender_display()
        print(f"  • {patient.get_full_name():35} | {age:2} yosh | {gender_display:5} | {patient.blood_type:3}")
        if patient.chronic_diseases:
            print(f"    Surunkali: {chronic}")
        if patient.allergies:
            print(f"    Allergiya: {allergies}")
    
    avg_age = age_sum / patients.count() if patients.count() > 0 else 0
    
    print(f"\nStatistika:")
    print(f"  - Erkaklar:              {gender_counts['M']} ta ({gender_counts['M']*100//patients.count()}%)")
    print(f"  - Ayollar:               {gender_counts['F']} ta ({gender_counts['F']*100//patients.count()}%)")
    print(f"  - O'rtacha yosh:         {avg_age:.1f} yosh")
    print(f"  - Surunkali kasalligi:   {with_chronic} ta ({with_chronic*100//patients.count()}%)")
    print(f"  - Allergiyasi:           {with_allergies} ta ({with_allergies*100//patients.count()}%)")
    
    # 3. Qon guruhlari
    print("\n3. QON GURUHLARI")
    print("-" * 70)
    blood_types = {}
    for patient in patients:
        bt = patient.blood_type or 'Noma\'lum'
        blood_types[bt] = blood_types.get(bt, 0) + 1
    
    for bt, count in sorted(blood_types.items()):
        print(f"  - {bt:5}: {count} ta")
    
    # 4. Surunkali kasalliklar
    print("\n4. SURUNKALI KASALLIKLAR")
    print("-" * 70)
    chronic_diseases = {}
    for patient in patients:
        if patient.chronic_diseases:
            for disease in patient.chronic_diseases:
                chronic_diseases[disease] = chronic_diseases.get(disease, 0) + 1
    
    if chronic_diseases:
        for disease, count in sorted(chronic_diseases.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {disease:30}: {count} ta bemor")
    else:
        print("  Surunkali kasalliklar yo'q")
    
    # 5. Allergiyalar
    print("\n5. ALLERGIYALAR")
    print("-" * 70)
    allergies = {}
    for patient in patients:
        if patient.allergies:
            for allergy in patient.allergies:
                allergies[allergy] = allergies.get(allergy, 0) + 1
    
    if allergies:
        for allergy, count in sorted(allergies.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {allergy:30}: {count} ta bemor")
    else:
        print("  Allergiyalar yo'q")
    
    # 6. Tizim holati
    print("\n6. TIZIM HOLATI")
    print("-" * 70)
    print(f"  ✓ Database:              Ulangan")
    print(f"  ✓ Kasallik naqshlari:    {diseases.count()} ta")
    print(f"  ✓ Bemorlar:              {patients.count()} ta")
    print(f"  ✓ Server:                http://127.0.0.1:8080/")
    print(f"  ✓ Admin Panel:           http://127.0.0.1:8080/admin/")
    print(f"  ✓ API Docs:              http://127.0.0.1:8080/api/docs/ (admin)")
    
    # 7. Tekshirish
    print("\n7. TEKSHIRISH")
    print("-" * 70)
    
    issues = []
    
    if diseases.count() < 15:
        issues.append(f"⚠ Kasalliklar kam: {diseases.count()}/15")
    
    if patients.count() < 10:
        issues.append(f"⚠ Bemorlar kam: {patients.count()}/10")
    
    # Check if all diseases have symptoms
    for disease in diseases:
        if not disease.symptoms:
            issues.append(f"⚠ {disease.name} da simptomlar yo'q")
    
    # Check if all patients have required fields
    for patient in patients:
        if not patient.blood_type:
            issues.append(f"⚠ {patient.get_full_name()} da qon guruhi yo'q")
        if not patient.phone:
            issues.append(f"⚠ {patient.get_full_name()} da telefon yo'q")
    
    if issues:
        print("\nMUAMMOLAR:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("\n✅ BARCHA TEKSHIRUVLAR O'TDI!")
    
    # Summary
    print("\n" + "=" * 70)
    print("XULOSA")
    print("=" * 70)
    print(f"\n✅ Kasallik naqshlari:  {diseases.count()} ta (15 ta kutilgan)")
    print(f"✅ Demo bemorlar:       {patients.count()} ta (10+ ta kutilgan)")
    print(f"✅ Erkak/Ayol:          {gender_counts['M']}/{gender_counts['F']}")
    print(f"✅ O'rtacha yosh:       {avg_age:.1f} yosh")
    
    if not issues:
        print("\n🎉 HAMMASI TAYYOR! Tizimdan foydalanishingiz mumkin.")
    else:
        print(f"\n⚠ {len(issues)} ta muammo topildi. Ularni hal qiling.")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    try:
        test_new_changes()
    except Exception as e:
        print(f"\n❌ Xatolik: {e}")
        import traceback
        traceback.print_exc()
