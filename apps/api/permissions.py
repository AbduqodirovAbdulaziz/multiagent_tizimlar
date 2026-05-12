"""
API Permissions - Custom permissions.
"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Faqat owner o'zgartirishi mumkin, boshqalar faqat o'qiy oladi.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions faqat owner uchun
        return obj.user == request.user


class IsPatientOwner(permissions.BasePermission):
    """
    Faqat bemor o'z ma'lumotlarini ko'rishi va o'zgartirishi mumkin.
    """
    
    def has_object_permission(self, request, view, obj):
        # Staff foydalanuvchilar hamma narsani ko'rishi mumkin
        if request.user.is_staff:
            return True
        
        # Bemor faqat o'z ma'lumotlarini ko'rishi mumkin
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'patient'):
            return obj.patient.user == request.user
        
        return False
