"""
Diagnostics views - Web views for diagnostics app.
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import DiagnosticSession, DiagnosticResult, DiseasePattern
from apps.patients.models import Patient


@login_required
def session_list(request):
    """
    Diagnostika sessiyalari ro'yxati.
    """
    sessions = DiagnosticSession.objects.select_related('patient').order_by('-started_at')
    
    context = {
        'sessions': sessions,
        'title': 'Diagnostika Sessiyalari'
    }
    
    return render(request, 'diagnostics/session_list.html', context)


@login_required
def session_detail(request, session_id):
    """
    Diagnostika sessiyasi detallari.
    """
    session = get_object_or_404(DiagnosticSession, session_id=session_id)
    results = session.results.select_related('disease').all()
    
    context = {
        'session': session,
        'results': results,
        'title': f'Sessiya: {session_id}'
    }
    
    return render(request, 'diagnostics/session_detail.html', context)


@login_required
def disease_list(request):
    """
    Kasalliklar ro'yxati.
    """
    diseases = DiseasePattern.objects.filter(is_active=True).order_by('name')
    
    context = {
        'diseases': diseases,
        'title': 'Kasalliklar Bazasi'
    }
    
    return render(request, 'diagnostics/disease_list.html', context)


@login_required
def disease_detail(request, pk):
    """
    Kasallik detallari.
    """
    disease = get_object_or_404(DiseasePattern, pk=pk)
    
    context = {
        'disease': disease,
        'title': disease.name
    }
    
    return render(request, 'diagnostics/disease_detail.html', context)


@login_required
@require_http_methods(["GET"])
def session_status_ajax(request, session_id):
    """
    AJAX: Sessiya holatini olish.
    """
    try:
        session = DiagnosticSession.objects.get(session_id=session_id)
        
        data = {
            'session_id': session.session_id,
            'status': session.status,
            'agent_states': session.agent_states,
            'started_at': session.started_at.isoformat() if session.started_at else None,
            'completed_at': session.completed_at.isoformat() if session.completed_at else None,
            'error_message': session.error_message,
        }
        
        return JsonResponse(data)
        
    except DiagnosticSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)
