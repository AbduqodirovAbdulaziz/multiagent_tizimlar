"""
Core utilities - Helper functions.
"""
import uuid
import hashlib
from datetime import timedelta
from django.utils import timezone


def generate_message_id(sender: str, receiver: str) -> str:
    """
    Unique xabar ID generatsiya qilish.
    
    Args:
        sender: Yuboruvchi agent nomi
        receiver: Qabul qiluvchi agent nomi
    
    Returns:
        Unique message ID
    """
    timestamp = timezone.now().isoformat()
    unique_string = f"{sender}-{receiver}-{timestamp}-{uuid.uuid4()}"
    return hashlib.md5(unique_string.encode()).hexdigest()


def generate_session_id() -> str:
    """
    Unique session ID generatsiya qilish.
    
    Returns:
        Unique session ID
    """
    return f"session-{uuid.uuid4().hex[:16]}"


def calculate_expiry_time(ttl_seconds: int) -> timezone.datetime:
    """
    Xabar amal qilish muddatini hisoblash.
    
    Args:
        ttl_seconds: Time to live (soniyalarda)
    
    Returns:
        Expiry datetime
    """
    return timezone.now() + timedelta(seconds=ttl_seconds)


def format_agent_name(agent_type: str) -> str:
    """
    Agent nomini formatlash.
    
    Args:
        agent_type: Agent turi
    
    Returns:
        Formatlangan agent nomi
    """
    return f"{agent_type}_agent"


def parse_symptoms(symptoms_text: str) -> list:
    """
    Simptomlar matnini parse qilish.
    
    Args:
        symptoms_text: Simptomlar matni (vergul bilan ajratilgan)
    
    Returns:
        Simptomlar ro'yxati
    """
    if not symptoms_text:
        return []
    
    symptoms = [s.strip() for s in symptoms_text.split(',')]
    return [s for s in symptoms if s]


def calculate_confidence_score(factors: dict) -> float:
    """
    Ishonch darajasini hisoblash.
    
    Args:
        factors: Omillar dictionary (key: weight)
    
    Returns:
        Confidence score (0.0 - 1.0)
    """
    if not factors:
        return 0.0
    
    total_weight = sum(factors.values())
    if total_weight == 0:
        return 0.0
    
    return min(total_weight / len(factors), 1.0)
