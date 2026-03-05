
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import Role

ROLES_CONFIG = {
    'admin': ['all', 'global_manage', 'global_view', 'manage_mdas', 'manage_services', 'manage_lifecycle_groups', 'view_priority_mdas', 'access_g2g_services'],
    'system_admin': ['all', 'global_manage', 'global_view', 'manage_mdas', 'manage_services', 'manage_lifecycle_groups', 'view_priority_mdas', 'access_g2g_services'],
    'GLOBAL_OFFICER': ['all_mdas.view', 'all_mdas.claim', 'view_request', 'verify_document', 'access_g2g_services'],
    'GLOBAL_SUPERVISOR': ['all_mdas.view', 'all_mdas.claim', 'all_mdas.supervise', 'view_request', 'verify_document', 'approve_request', 'access_g2g_services'],
    'mda_admin': ['mda_view', 'mda_manage_users', 'mda_manage_services', 'reports_view', 'request_action', 'manage_services', 'view_priority_mdas'],
    'officer': ['mda_view', 'request_action', 'view_request'],
    'supervisor': ['mda_view', 'request_action', 'request_approve', 'reports_view', 'view_request'],
    'citizen': ['request_create', 'request_view_own', 'saved_docs_manage'],
}

for name, perms in ROLES_CONFIG.items():
    role, created = Role.objects.get_or_create(name=name)
    role.permissions = list(set(role.permissions + perms))
    role.save()
    print(f"Updated role: {name}")
