"""
Agents views - Web views for agents app.
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import AgentState
from apps.core.models import AgentLog, ACLMessage


@login_required
def agent_list(request):
    """
    Agentlar ro'yxati va holatlari.
    """
    agents = AgentState.objects.all().order_by('agent_name')
    
    context = {
        'agents': agents,
        'title': 'Agent Holatlari'
    }
    
    return render(request, 'agents/agent_list.html', context)


@login_required
def agent_detail(request, agent_name):
    """
    Agent detallari va loglar.
    """
    agent = get_object_or_404(AgentState, agent_name=agent_name)
    logs = AgentLog.objects.filter(agent_name=agent_name).order_by('-timestamp')[:100]
    
    # Yuborilgan va qabul qilingan xabarlar
    sent_messages = ACLMessage.objects.filter(sender=agent_name).order_by('-created_at')[:20]
    received_messages = ACLMessage.objects.filter(receiver=agent_name).order_by('-created_at')[:20]
    
    context = {
        'agent': agent,
        'logs': logs,
        'sent_messages': sent_messages,
        'received_messages': received_messages,
        'title': f'Agent: {agent_name}'
    }
    
    return render(request, 'agents/agent_detail.html', context)


@login_required
def agent_logs(request):
    """
    Barcha agent loglar.
    """
    agent_name = request.GET.get('agent')
    level = request.GET.get('level')
    
    logs = AgentLog.objects.all()
    
    if agent_name:
        logs = logs.filter(agent_name=agent_name)
    
    if level:
        logs = logs.filter(level=level)
    
    logs = logs.order_by('-timestamp')[:200]
    
    # Agent nomlari ro'yxati
    agent_names = AgentState.objects.values_list('agent_name', flat=True)
    
    context = {
        'logs': logs,
        'agent_names': agent_names,
        'selected_agent': agent_name,
        'selected_level': level,
        'title': 'Agent Loglar'
    }
    
    return render(request, 'agents/agent_logs.html', context)


@login_required
def acl_messages(request):
    """
    ACL xabarlar ro'yxati.
    """
    sender = request.GET.get('sender')
    receiver = request.GET.get('receiver')
    
    messages = ACLMessage.objects.all()
    
    if sender:
        messages = messages.filter(sender=sender)
    
    if receiver:
        messages = messages.filter(receiver=receiver)
    
    messages = messages.order_by('-created_at')[:100]
    
    # Agent nomlari
    agent_names = AgentState.objects.values_list('agent_name', flat=True)
    
    context = {
        'messages': messages,
        'agent_names': agent_names,
        'selected_sender': sender,
        'selected_receiver': receiver,
        'title': 'ACL Xabarlar'
    }
    
    return render(request, 'agents/acl_messages.html', context)


@login_required
@require_http_methods(["GET"])
def agent_status_ajax(request, agent_name):
    """
    AJAX: Agent holatini olish.
    """
    try:
        agent = AgentState.objects.get(agent_name=agent_name)
        
        data = {
            'agent_name': agent.agent_name,
            'state': agent.state,
            'current_task': agent.current_task,
            'last_activity': agent.last_activity.isoformat() if agent.last_activity else None,
            'metadata': agent.metadata,
        }
        
        return JsonResponse(data)
        
    except AgentState.DoesNotExist:
        return JsonResponse({'error': 'Agent not found'}, status=404)


@login_required
@require_http_methods(["GET"])
def agents_health_check(request):
    """
    AJAX: Barcha agentlar health check.
    """
    agents = AgentState.objects.all()
    
    data = {
        'total_agents': agents.count(),
        'agents': [
            {
                'agent_name': agent.agent_name,
                'state': agent.state,
                'current_task': agent.current_task,
                'last_activity': agent.last_activity.isoformat() if agent.last_activity else None,
            }
            for agent in agents
        ]
    }
    
    return JsonResponse(data)
