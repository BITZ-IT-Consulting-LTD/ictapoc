import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import Role

def seed_rbac_roles():
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
    ]

    for role_data in roles_to_create:
        role, created = Role.objects.get_or_create(
            name=role_data["name"],
            defaults={
                "description": role_data["description"],
                "permissions": role_data["permissions"]
            }
        )
        if created:
            print(f"✓ Created role: {role.name}")
        else:
            role.description = role_data["description"]
            role.permissions = role_data["permissions"]
            role.save()
            print(f"✓ Updated role: {role.name}")

if __name__ == "__main__":
    seed_rbac_roles()
