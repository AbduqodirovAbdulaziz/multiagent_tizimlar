"""
Core exceptions - Custom exception sinflar.
"""


class AgentException(Exception):
    """Bazaviy agent exception."""
    pass


class AgentCommunicationError(AgentException):
    """Agent kommunikatsiya xatosi."""
    pass


class AgentTimeoutError(AgentException):
    """Agent timeout xatosi."""
    pass


class AgentProcessingError(AgentException):
    """Agent qayta ishlash xatosi."""
    pass


class InvalidACLMessageError(AgentException):
    """Noto'g'ri ACL xabar formati."""
    pass


class DiagnosticException(Exception):
    """Bazaviy diagnostika exception."""
    pass


class DiagnosticNotFoundError(DiagnosticException):
    """Diagnostika topilmadi."""
    pass


class DiagnosticProcessingError(DiagnosticException):
    """Diagnostika qayta ishlash xatosi."""
    pass
