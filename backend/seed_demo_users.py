import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import User, Role, MDA

def create_demo_users():
    print("🚀 Creating Demo Users for RBAC validation...")
    
    # 1. Ensure Roles Exist
    try:
        roles = {
            "GLOBAL_OFFICER": Role.objects.get(name="GLOBAL_OFFICER"),
            "GLOBAL_SUPERVISOR": Role.objects.get(name="GLOBAL_SUPERVISOR"),
            "MDA_OFFICER": Role.objects.get(name="MDA_OFFICER"),
            "MDA_SUPERVISOR": Role.objects.get(name="MDA_SUPERVISOR"),
            "Hospital_Staff": Role.objects.get(name="Hospital_Staff"),
        }
    except Role.DoesNotExist:
        print("❌ RBAC Roles not seeded. Please run seed_rbac_roles.py first.")
        return
    
    # 2. Get existing MDAs or create fallback ones
    moh = MDA.objects.filter(code__in=["MOH", "T-MOH"]).first()
    if not moh:
        moh, _ = MDA.objects.get_or_create(code="MOH", defaults={"name": "Ministry of Health"})
        
    moe = MDA.objects.filter(code__in=["MOE", "T-MOE"]).first()
    if not moe:
        moe, _ = MDA.objects.get_or_create(code="MOE", defaults={"name": "Ministry of Education"})

    # 3. User Definitions
    users_to_create = [
        {
            "username": "global.officer",
            "password": "Starten1@",
            "role_name": "GLOBAL_OFFICER",
            "mda": None,
            "assigned_mdas": []
        },
        {
            "username": "global.supervisor",
            "password": "Starten1@",
            "role_name": "GLOBAL_SUPERVISOR",
            "mda": None,
            "assigned_mdas": []
        },
        {
            "username": "moh.officer",
            "password": "Starten1@",
            "role_name": "MDA_OFFICER",
            "mda": moh,
            "assigned_mdas": [moh]
        },
        {
            "username": "moh.supervisor",
            "password": "Starten1@",
            "role_name": "MDA_SUPERVISOR",
            "mda": moh,
            "assigned_mdas": [moh]
        },
        {
            "username": "moe.officer",
            "password": "Starten1@",
            "role_name": "MDA_OFFICER",
            "mda": moe,
            "assigned_mdas": [moe]
        },
        {
            "username": "nurse.jane",
            "password": "Starten1@",
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
                "mda": u_data["mda"]
            }
        )
        user.set_password(u_data["password"])
        user.save()
        
        if u_data["assigned_mdas"]:
            user.assigned_mdas.set(u_data["assigned_mdas"])
            
        print(f"✓ Configured user: {user.username} (Password: {u_data['password']})")

if __name__ == "__main__":
    create_demo_users()
