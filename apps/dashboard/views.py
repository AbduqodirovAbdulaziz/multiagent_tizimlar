"""
Dashboard views - monitoring va vizualizatsiya.
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from apps.diagnostics.models import DiagnosticSession, DiagnosticResult
from apps.agents.models import AgentState
from apps.patients.models import Patient


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
    
    # So'nggi sessiyalar
    recent_sessions = DiagnosticSession.objects.select_related('patient').order_by('-started_at')[:10]
    
    # Agent holatlari
    agents = AgentState.objects.all()
    
    context = {
        'total_patients': total_patients,
        'total_sessions': total_sessions,
        'completed_sessions': completed_sessions,
        'pending_sessions': pending_sessions,
        'recent_sessions': recent_sessions,
        'agents': agents,
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
