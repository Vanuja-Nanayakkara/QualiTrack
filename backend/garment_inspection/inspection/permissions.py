# Save this as permissions.py in your inspection app directory
from rest_framework import permissions
from .models import CLIInspector, Supervisor

class IsInspector(permissions.BasePermission):
    """
    Custom permission to only allow CLI Inspectors to access the view.
    """
    message = 'You must be a CLI Inspector to perform this action.'
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Check if user is a CLI Inspector
        return CLIInspector.objects.filter(email=request.user.email).exists()

class IsSupervisor(permissions.BasePermission):
    """
    Custom permission to only allow Supervisors to access the view.
    """
    message = 'You must be a Supervisor to perform this action.'
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Check if user is a Supervisor
        return Supervisor.objects.filter(email=request.user.email).exists()

class IsInspectorOrSupervisor(permissions.BasePermission):
    """
    Custom permission to only allow users with either role to access the view.
    """
    message = 'You must be either a CLI Inspector or a Supervisor to perform this action.'
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Check if user has either role
        email = request.user.email
        return (CLIInspector.objects.filter(email=email).exists() or 
                Supervisor.objects.filter(email=email).exists())