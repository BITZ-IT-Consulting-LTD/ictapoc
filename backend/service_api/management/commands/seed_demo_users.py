from django.core.management.base import BaseCommand
from service_api.models import User, Role, MDA

class Command(BaseCommand):
    help = 'Seeds demo users for RBAC validation'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Creating Demo Users for RBAC validation...")
        
        # 1. Ensure Roles Exist
        try:
            roles = {
                "GLOBAL_OFFICER": Role.objects.get(name="GLOBAL_OFFICER"),
                "GLOBAL_SUPERVISOR": Role.objects.get(name="GLOBAL_SUPERVISOR"),
                "MDA_OFFICER": Role.objects.get(name="MDA_OFFICER"),
                "MDA_SUPERVISOR": Role.objects.get(name="MDA_SUPERVISOR"),
                "Hospital_Staff": Role.objects.get(name="Hospital_Staff"),
                "admin": Role.objects.get(name="admin"),
                "citizen": Role.objects.get(name="citizen"),
                "officer": Role.objects.get(name="officer"),
                "supervisor": Role.objects.get(name="supervisor"),
                "registrar": Role.objects.get(name="registrar"),
                "mda_admin": Role.objects.get(name="mda_admin"),
                "system_admin": Role.objects.get(name="system_admin"),
                "employee": Role.objects.get(name="employee"),
            }
        except Role.DoesNotExist:
            self.stdout.write(self.style.ERROR("❌ RBAC Roles not seeded. Please run seed_rbac_roles first."))
            return
        
        # 2. Get existing MDAs or create fallback ones
        moh, _ = MDA.objects.get_or_create(code="MOH", defaults={"name": "Ministry of Health"})
        moe, _ = MDA.objects.get_or_create(code="MOE", defaults={"name": "Ministry of Education"})
        moi, _ = MDA.objects.get_or_create(code="MOI", defaults={"name": "Ministry of Interior"})
        icta, _ = MDA.objects.get_or_create(code="ICTA", defaults={"name": "ICT Authority"})

        # 3. User Definitions
        users_to_create = [
            {
                "username": "admin",
                "role_name": "admin",
                "mda": None,
                "assigned_mdas": [],
                "is_staff": True,
                "is_superuser": True
            },
            {
                "username": "system.admin",
                "role_name": "system_admin",
                "mda": None,
                "assigned_mdas": [],
                "is_staff": True
            },
            {
                "username": "citizen1",
                "role_name": "citizen",
                "mda": None,
                "assigned_mdas": []
            },
            {
                "username": "officer1",
                "role_name": "officer",
                "mda": moi,
                "assigned_mdas": [moi]
            },
            {
                "username": "supervisor1",
                "role_name": "supervisor",
                "mda": moi,
                "assigned_mdas": [moi]
            },
            {
                "username": "registrar1",
                "role_name": "registrar",
                "mda": moi,
                "assigned_mdas": [moi]
            },
            {
                "username": "moh.admin",
                "role_name": "mda_admin",
                "mda": moh,
                "assigned_mdas": [moh]
            },
            {
                "username": "employee1",
                "role_name": "employee",
                "mda": icta,
                "assigned_mdas": [icta]
            },
            {
                "username": "global.officer",
                "role_name": "GLOBAL_OFFICER",
                "mda": None,
                "assigned_mdas": []
            },
            {
                "username": "global.supervisor",
                "role_name": "GLOBAL_SUPERVISOR",
                "mda": None,
                "assigned_mdas": []
            },
            {
                "username": "moh.officer",
                "role_name": "MDA_OFFICER",
                "mda": moh,
                "assigned_mdas": [moh]
            },
            {
                "username": "moh.supervisor",
                "role_name": "MDA_SUPERVISOR",
                "mda": moh,
                "assigned_mdas": [moh]
            },
            {
                "username": "moe.officer",
                "role_name": "MDA_OFFICER",
                "mda": moe,
                "assigned_mdas": [moe]
            },
            {
                "username": "nurse.jane",
                "role_name": "Hospital_Staff",
                "mda": moh,
                "assigned_mdas": [moh]
            }
        ]

        for u_data in users_to_create:
            user, created = User.objects.update_or_create(
                username=u_data["username"],
                defaults={
                    "role": u_data["role_name"],
                    "user_role": roles[u_data["role_name"]],
                    "mda": u_data["mda"],
                    "is_staff": u_data.get("is_staff", False),
                    "is_superuser": u_data.get("is_superuser", False)
                }
            )
            user.set_password("Starten1@")
            user.save()
            
            user.assigned_mdas.set(u_data["assigned_mdas"])
                
            self.stdout.write(self.style.SUCCESS(f"✓ Configured user: {user.username}"))
