"""
Patients views - Web views for patients app.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Patient, Symptom, MedicalHistory


@login_required
def patient_list(request):
    """
    Bemorlar ro'yxati.
    """
    query = request.GET.get('q', '')
    
    patients = Patient.objects.filter(is_active=True)
    
    if query:
        patients = patients.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query)
        )
    
    patients = patients.order_by('-created_at')
    
    context = {
        'patients': patients,
        'query': query,
        'title': 'Bemorlar'
    }
    
    return render(request, 'patients/patient_list.html', context)


@login_required
def patient_detail(request, pk):
    """
    Bemor detallari.
    """
    patient = get_object_or_404(Patient, pk=pk)
    symptoms = patient.symptoms.order_by('-created_at')[:10]
    medical_history = patient.medical_history.order_by('-diagnosed_at')[:10]
    diagnostic_sessions = patient.diagnostic_sessions.order_by('-started_at')[:10]
    
    context = {
        'patient': patient,
        'symptoms': symptoms,
        'medical_history': medical_history,
        'diagnostic_sessions': diagnostic_sessions,
        'title': patient.get_full_name()
    }
    
    return render(request, 'patients/patient_detail.html', context)


@login_required
def symptom_list(request):
    """
    Simptomlar ro'yxati.
    """
    patient_id = request.GET.get('patient')
    
    symptoms = Symptom.objects.select_related('patient')
    
    if patient_id:
        symptoms = symptoms.filter(patient_id=patient_id)
    
    symptoms = symptoms.order_by('-created_at')
    
    context = {
        'symptoms': symptoms,
        'title': 'Simptomlar'
    }
    
    return render(request, 'patients/symptom_list.html', context)


@login_required
def medical_history_list(request):
    """
    Tibbiy tarix ro'yxati.
    """
    patient_id = request.GET.get('patient')
    
    history = MedicalHistory.objects.select_related('patient')
    
    if patient_id:
        history = history.filter(patient_id=patient_id)
    
    history = history.order_by('-diagnosed_at')
    
    context = {
        'history': history,
        'title': 'Tibbiy Tarix'
    }
    
    return render(request, 'patients/medical_history_list.html', context)


@login_required
def patient_search(request):
    """
    Bemor qidirish.
    """
    query = request.GET.get('q', '')
    results = []
    
    if query:
        results = Patient.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query)
        ).filter(is_active=True)[:20]
    
    context = {
        'query': query,
        'results': results,
        'title': 'Bemor Qidirish'
    }
    
    return render(request, 'patients/patient_search.html', context)
