from django.core.management.base import BaseCommand
from service_api.models import Role

class Command(BaseCommand):
    help = 'Seeds RBAC Roles for the platform'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Seeding RBAC Roles...")
        roles_to_create = [
            {
                "name": "GLOBAL_OFFICER",
                "description": "Cross-MDA authority to view and claim any process.",
                "permissions": ["all_mdas.view", "all_mdas.claim"]
            },
            {
                "name": "GLOBAL_SUPERVISOR",
                "description": "Cross-MDA authority to view, claim, and supervise any process.",
                "permissions": ["all_mdas.view", "all_mdas.claim", "all_mdas.supervise"]
            },
            {
                "name": "MDA_OFFICER",
                "description": "Restricted authority to view and claim processes within assigned MDAs.",
                "permissions": ["mda.view", "mda.claim"]
            },
            {
                "name": "MDA_SUPERVISOR",
                "description": "Restricted authority to view, claim, and supervise processes within assigned MDAs.",
                "permissions": ["mda.view", "mda.claim", "mda.supervise"]
            },
            {
                "name": "Hospital_Staff",
                "description": "Specialized role for hospital personnel to initiate notifications.",
                "permissions": ["mda.view", "mda.claim", "mda.initiate"]
            },
            {
                 'name': 'admin',
                 'description': 'Global System Administrator', 
                 'permissions': ['all', 'global_view', 'global_manage', 'reports_view']
            },
            {
                 'name': 'citizen',
                 'description': 'Public User / Citizen', 
                 'permissions': ['request_create', 'request_view_own', 'saved_docs_manage']
            },
        ]

        for role_data in roles_to_create:
            role, created = Role.objects.update_or_create(
                name=role_data["name"],
                defaults={
                    "description": role_data["description"],
                    "permissions": role_data["permissions"]
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✓ Created role: {role.name}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"✓ Updated role: {role.name}"))
