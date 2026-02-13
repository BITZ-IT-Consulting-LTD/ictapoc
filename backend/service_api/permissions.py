from rest_framework import permissions
from .models import AuditLog

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
        
        # Centralized Authority: System Admin or Global Admin
        if user.role in ['admin', 'system_admin'] or user.is_staff or 'all' in perms or 'global_manage' in perms:
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
        if user.role in ['admin', 'GLOBAL_OFFICER', 'GLOBAL_SUPERVISOR'] or user.is_superuser:
            return True
            
        role_name = user.user_role.name if user.user_role else user.role
        if role_name in ["GLOBAL_OFFICER", "GLOBAL_SUPERVISOR"]:
            return True

        perms = user.user_role.permissions if user.user_role else []
        if 'all' in perms or 'global_view' in perms:
            return True

        # 2. MDA Scoped Permissions
        if 'mda_view' in perms or user.role in ['mda_admin', 'supervisor', 'officer', 'registrar', 'GLOBAL_OFFICER', 'GLOBAL_SUPERVISOR', 'MDA_OFFICER', 'MDA_SUPERVISOR']:
            # Ensure the object belongs to the same MDA
            if hasattr(obj, 'service_config') and obj.service_config.mda == user.mda:
                return True
            if hasattr(obj, 'current_step') and obj.current_step and obj.current_step.target_mda == user.mda:
                return True
            
            # Check for assigned MDAs (New RBAC)
            if hasattr(obj, 'service_config'):
                assigned_mda_ids = list(user.assigned_mdas.values_list('id', flat=True))
                if obj.service_config.mda.id in assigned_mda_ids:
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
        # 1. Global Support / Admin Override
        if user.role in ['admin', 'GLOBAL_OFFICER', 'GLOBAL_SUPERVISOR'] or user.is_superuser:
            return True
        
        # User's own requests
        if obj.service_request.citizen == user:
            return True
            
        # MDA Scoped Access
        perms = user.user_role.permissions if user.user_role else []
        if 'mda_view' in perms or user.role in ['mda_admin', 'supervisor', 'officer', 'MDA_OFFICER', 'MDA_SUPERVISOR', 'GLOBAL_OFFICER', 'GLOBAL_SUPERVISOR']:
            return True # Logic delegated to queryset or detailed checks
            
        return False

class IsSystemAdmin(permissions.BasePermission):
    """
    Strict permission for platform-level management (MDAs, Service Schemas).
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        user = request.user
        # Only Platform Admins can hit these
        return user.role in ['admin', 'system_admin'] or user.is_staff

class RBACScopeManager:
    """Helper to evaluate and log RBAC decisions"""
    
    @staticmethod
    def evaluate_claim(user, service_request):
        """
        Implements the core RBAC logic:
        - Global Roles can claim anything.
        - MDA Roles can only claim within assigned MDAs.
        """
        # 1. Resolve role name
        role_name = user.user_role.name if user.user_role else user.role
        assigned_mdas = list(user.assigned_mdas.values_list('id', flat=True))
        
        # Metadata for auditing
        audit_context = {
            "actor": user,
            "actor_role": role_name,
            "actor_mdas": assigned_mdas,
            "process_id": service_request.request_id,
            "service_id": service_request.service_config.service_code,
            "owning_mda_id": service_request.service_config.mda.id,
            "service_request": service_request
        }

        # 2. Authorization Logic
        decision = "DENY"
        details = ""

        if role_name in ["GLOBAL_OFFICER", "GLOBAL_SUPERVISOR", "system_admin", "admin"]:
            decision = "ALLOW"
            details = "Global scope authorization"
        
        elif role_name in ["MDA_OFFICER", "MDA_SUPERVISOR", "mda_admin"]:
            if service_request.service_config.mda.id in assigned_mdas:
                decision = "ALLOW"
                details = f"MDA scope authorized for MDA ID: {service_request.service_config.mda.id}"
            else:
                decision = "DENY"
                details = f"MDA scope violation: User NOT assigned to MDA {service_request.service_config.mda.id}"
        
        else:
            decision = "DENY"
            details = f"Unauthorized role: {role_name}"

        # 3. Log the attempt (Immutable Audit)
        AuditLog.objects.create(
            actor=user,
            actor_role=role_name,
            actor_mdas=assigned_mdas,
            action="CLAIM_PROCESS_ATTEMPT",
            decision=decision,
            process_id=audit_context["process_id"],
            service_id=audit_context["service_id"],
            owning_mda_id=audit_context["owning_mda_id"],
            service_request=service_request,
            details=details
        )

        return decision == "ALLOW", details

class IsClaimAuthorized(permissions.BasePermission):
    """
    DRF Permission for claiming/acting on a ServiceRequest.
    Strictly enforces Global vs MDA scopes.
    """
    
    def has_object_permission(self, request, view, obj):
        # Only check on action-based requests (POST/PATCH/PUT) that imply "claiming" or "acting"
        # If it's a list/detail view, we might want different logic, but for "claiming":
        if request.method in permissions.SAFE_METHODS:
            # We still might want to restrict viewing, but let's focus on CLAMING first
            # Following requirement 3: View Process rule
            role_name = request.user.user_role.name if request.user.user_role else request.user.role
            assigned_mdas = list(request.user.assigned_mdas.values_list('id', flat=True))
            
            if role_name in ["GLOBAL_OFFICER", "GLOBAL_SUPERVISOR"]:
                return True
            if obj.service_config.mda.id in assigned_mdas:
                return True
            return False

        allowed, reason = RBACScopeManager.evaluate_claim(request.user, obj)
        return allowed
