"""
Dashboard views - monitoring va vizualizatsiya.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Q
from django.http import JsonResponse
from apps.diagnostics.models import DiagnosticSession, DiagnosticResult, DiseasePattern
from apps.agents.models import AgentState
from apps.patients.models import Patient
from apps.diagnostics.services import DiagnosticService
from apps.agents.coordinator_agent import CoordinatorAgent


@login_required
def index(request):
    """
    Dashboard asosiy sahifa.
    """
    # Statistika
    total_patients = Patient.objects.filter(is_active=True).count()
    total_sessions = DiagnosticSession.objects.count()
    completed_sessions = DiagnosticSession.objects.filter(status='COMPLETED').count()
    pending_sessions = DiagnosticSession.objects.filter(status='PENDING').count()
    in_progress_sessions = DiagnosticSession.objects.filter(status='IN_PROGRESS').count()
    
    # So'nggi sessiyalar
    recent_sessions = DiagnosticSession.objects.select_related('patient').order_by('-started_at')[:5]
    
    # Agent holatlari
    agents = AgentState.objects.all()
    
    # Bemorlar ro'yxati (diagnostika uchun)
    patients = Patient.objects.filter(is_active=True).order_by('-created_at')[:20]
    
    # Kasalliklar statistikasi
    top_diseases = DiagnosticResult.objects.values('disease__name').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Simptomlar ro'yxati (kategoriyalar bo'yicha)
    symptom_categories = {
        'Umumiy Simptomlar': [
            'Isitma',
            'Charchoq',
            'Ishtahasizlik',
            'Vazn yo\'qotish',
            'Terlash',
            'Titroq',
        ],
        'Nafas Olish Tizimi': [
            'Yo\'tal',
            'Nafas qisilishi',
            'Burun bitishi',
            'Tomoq og\'rig\'i',
            'Ko\'krak og\'rig\'i',
            'Xirillash',
        ],
        'Ovqat Hazm Qilish': [
            'Qorin og\'rig\'i',
            'Ko\'ngil aynishi',
            'Qusish',
            'Ichburug\'',
            'Qabziyat',
            'Oshqozon og\'rig\'i',
        ],
        'Asab Tizimi': [
            'Bosh og\'rig\'i',
            'Bosh aylanishi',
            'Hushidan ketish',
            'Uyqusizlik',
            'Xotira zaiflanishi',
            'Qo\'l-oyoq uyushishi',
        ],
        'Yurak-Qon Tomir': [
            'Yurak urishi',
            'Ko\'krak og\'rig\'i',
            'Nafas qisilishi',
            'Oyoq shishishi',
            'Qon bosimi o\'zgarishi',
        ],
        'Mushak-Skelet': [
            'Bo\'g\'im og\'rig\'i',
            'Mushak og\'rig\'i',
            'Orqa og\'rig\'i',
            'Bo\'yin og\'rig\'i',
            'Harakatsizlik',
        ],
        'Teri': [
            'Toshmalar',
            'Qichishish',
            'Teri qizarishi',
            'Shish',
            'Teri rangi o\'zgarishi',
        ],
    }
    
    context = {
        'total_patients': total_patients,
        'total_sessions': total_sessions,
        'completed_sessions': completed_sessions,
        'pending_sessions': pending_sessions,
        'in_progress_sessions': in_progress_sessions,
        'recent_sessions': recent_sessions,
        'agents': agents,
        'patients': patients,
        'top_diseases': top_diseases,
        'symptom_categories': symptom_categories,
    }
    
    return render(request, 'dashboard/index.html', context)


@login_required
def session_detail(request, session_id):
    """
    Diagnostika sessiyasi detallari.
    """
    session = get_object_or_404(DiagnosticSession, session_id=session_id)
    results = session.results.all()
    
    context = {
        'session': session,
        'results': results,
    }
    
    return render(request, 'dashboard/session_detail.html', context)


@login_required
def agent_status(request):
    """
    Agentlar holati sahifasi.
    """
    agents = AgentState.objects.all()
    
    context = {
        'agents': agents,
    }
    
    return render(request, 'dashboard/agent_status.html', context)


@login_required
def start_diagnostic(request):
    """
    Yangi diagnostika sessiyasini boshlash.
    """
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        temperature = request.POST.get('temperature', '')
        
        # Validate
        if not patient_id:
            messages.error(request, 'Bemorni tanlang!')
            return redirect('dashboard:index')
        
        # Simptomlarni checkbox'lardan olish
        symptoms = request.POST.getlist('symptoms')
        
        if not symptoms:
            messages.error(request, 'Kamida bitta simptom tanlang!')
            return redirect('dashboard:index')
        
        try:
            patient = Patient.objects.get(id=patient_id)
            
            # Test results
            test_results = {}
            if temperature:
                try:
                    test_results['temperature'] = float(temperature)
                except ValueError:
                    pass
            
            # Session yaratish
            session = DiagnosticService.create_session(patient, symptoms)
            
            # Diagnostika jarayonini boshlash
            coordinator = CoordinatorAgent()
            
            try:
                result = coordinator.execute({
                    'session_id': session.session_id,
                    'patient_id': patient.id,
                    'symptoms': symptoms,
                    'test_results': test_results
                })
                
                messages.success(request, f'Diagnostika muvaffaqiyatli yakunlandi! Session ID: {session.session_id}')
                return redirect('dashboard:session_detail', session_id=session.session_id)
                
            except Exception as e:
                messages.error(request, f'Diagnostika xatosi: {str(e)}')
                return redirect('dashboard:index')
                
        except Patient.DoesNotExist:
            messages.error(request, 'Bemor topilmadi!')
            return redirect('dashboard:index')
        except Exception as e:
            messages.error(request, f'Xatolik: {str(e)}')
            return redirect('dashboard:index')
    
    return redirect('dashboard:index')
