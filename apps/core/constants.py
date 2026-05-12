"""
Core constants - Agent va ACL konstantalari.
"""

# Agent turlari
AGENT_TYPES = {
    'SYMPTOM': 'symptom_agent',
    'ANALYSIS': 'analysis_agent',
    'DIAGNOSIS': 'diagnosis_agent',
    'TREATMENT': 'treatment_agent',
    'COORDINATOR': 'coordinator_agent',
}

# ACL Performatives (FIPA-ACL standarti)
ACL_PERFORMATIVES = {
    'INFORM': 'INFORM',
    'REQUEST': 'REQUEST',
    'QUERY': 'QUERY',
    'PROPOSE': 'PROPOSE',
    'ACCEPT': 'ACCEPT',
    'REJECT': 'REJECT',
    'CONFIRM': 'CONFIRM',
    'FAILURE': 'FAILURE',
}

# Agent holatlari
AGENT_STATES = {
    'IDLE': 'idle',
    'PROCESSING': 'processing',
    'WAITING': 'waiting',
    'COMPLETED': 'completed',
    'FAILED': 'failed',
}

# Diagnostika holatlari
DIAGNOSTIC_STATES = {
    'PENDING': 'pending',
    'IN_PROGRESS': 'in_progress',
    'COMPLETED': 'completed',
    'FAILED': 'failed',
}

# Kasallik darajasi
SEVERITY_LEVELS = {
    'LOW': 'low',
    'MEDIUM': 'medium',
    'HIGH': 'high',
    'CRITICAL': 'critical',
}
