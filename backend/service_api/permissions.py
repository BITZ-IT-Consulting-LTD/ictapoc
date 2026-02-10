from rest_framework import permissions

class IsAdminOrAuthenticatedReadOnly(permissions.BasePermission):
    """
    Allow any authenticated user to read (GET), but only Admins or MDA Admins (for their scoped data) to write.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
            
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write Operations
        user = request.user
        perms = user.user_role.permissions if user.user_role else []
        
        # Global Admin
        if user.role == 'admin' or user.is_staff or 'all' in perms or 'global_manage' in perms:
            return True
            
        # MDA Admin (Partial support here, object-level check needed for specific MDA)
        if user.role == 'mda_admin' or 'mda_manage_services' in perms:
            return True
            
        return False

class IsParticipantOrAdmin(permissions.BasePermission):
    """
    Grants access to:
    - Citizens: Create requests, View OWN requests.
    - Officers: View assigned requests.
    - Supervisors: View team/escalated requests.
    - Admins: View/Manage Everything.
    """
    def has_permission(self, request, view):
        # Allow any authenticated user to hit the endpoint.
        # Object-level permissions will restrict access to specific IDs.
        if not request.user or not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # 1. Global Support / Admin Override
        if user.role == 'admin' or user.is_superuser:
            return True
            
        perms = user.user_role.permissions if user.user_role else []
        if 'all' in perms or 'global_view' in perms:
            return True

        # 2. MDA Scoped Permissions
        if 'mda_view' in perms or user.role in ['mda_admin', 'supervisor', 'officer', 'registrar']:
            # Ensure the object belongs to the same MDA
            if hasattr(obj, 'service_config') and obj.service_config.mda == user.mda:
                return True
            if hasattr(obj, 'current_step') and obj.current_step and obj.current_step.target_mda == user.mda:
                return True

        # 3. Citizen / Own Data Check
        if 'request_view_own' in perms or user.role == 'citizen':
             # For ServiceRequest
             if hasattr(obj, 'citizen') and obj.citizen == user:
                 return True
             # For AuditLog
             if hasattr(obj, 'service_request') and obj.service_request.citizen == user:
                 return True
            
        return False

class AuditLogPermission(permissions.BasePermission):
    """
    Admins: See all.
    Others: See logs for requests they own or participate in.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == 'admin' or user.is_superuser:
            return True
        
        # User's own requests
        if obj.service_request.citizen == user:
            return True
            
        # MDA Scoped Access
        perms = user.user_role.permissions if user.user_role else []
        if 'mda_view' in perms or user.role in ['mda_admin', 'supervisor', 'officer']:
            return obj.service_request.service_config.mda == user.mda
            
        return False
