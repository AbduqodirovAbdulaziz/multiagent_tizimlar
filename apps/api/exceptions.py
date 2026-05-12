"""
API Exception Handler - Custom exception handling.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF.
    
    Bu handler barcha exception'larni bir xil formatda qaytaradi.
    """
    # DRF default handler
    response = exception_handler(exc, context)
    
    if response is not None:
        # Custom format
        custom_response_data = {
            'error': True,
            'message': str(exc),
            'details': response.data if isinstance(response.data, dict) else {'detail': response.data},
            'status_code': response.status_code
        }
        response.data = custom_response_data
    else:
        # Unhandled exceptions
        custom_response_data = {
            'error': True,
            'message': 'Server xatosi',
            'details': {'detail': str(exc)},
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
        }
        response = Response(custom_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response
