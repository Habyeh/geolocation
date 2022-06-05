"""User permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from providers.models.providers import Provider


class IsProviderOwner(BasePermission):
    """Allow access only to objects owned by the requesting user."""
    
    def has_object_permission(self, request, view, obj):
        """Check if the obj owner and request user are the same."""
        
        if isinstance(obj, Provider):
            return request.user == obj.user
        else:
            return request.user == obj.provider.user