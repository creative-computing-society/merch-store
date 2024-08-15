from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Custom permission to grant superuser status based on user position.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check user position
        user_position = request.user.position

        # Grant superuser status for "exbo" position
        if user_position == 'exbo':
            request.user.is_superuser = True
        else:
            request.user.is_superuser = False
        
        return False
