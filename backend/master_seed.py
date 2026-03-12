import os
import django
import sys
import json

# Set up Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA
from service_api.seed_utils import get_canonical_mdas

def seed_canonical_registry():
    print("--- 📂 Initializing Canonical MDA Registry ---")
    canonical_list = get_canonical_mdas()
    count = 0
    for item in canonical_list:
        mda, created = MDA.objects.get_or_create(
            code=item['code'],
            defaults={
                'name': item['name'],
                'description': item.get('description'),
                'head_of_mda': item.get('head'),
                'contact_email': item.get('email'),
                'contact_phone': item.get('phone')
            }
        )
        if created:
            count += 1
    print(f"✅ Created {count} new MDAs from canonical registry.")

def run_master_seed():
    print("=" * 80)
    print("🏛️  WHOLE-OF-GOVERNMENT MASTER SEEDER v1.0")
    print("=" * 80)

    # 1. Initialize Registry
    seed_canonical_registry()

    # 2. Run Priority MDAs & Services
    print("\n--- 🏢 Seeding Priority MDAs ---")
    from seed_priority_mdas import seed
    seed()

    # 3. Run Cradle-to-Death Lifecycle
    print("\n--- 👶 Lifecycle: Cradle-to-Death Seeding ---")
    from seed_wog_v2 import run_lifecycle_seed_v3
    run_lifecycle_seed_v3()

    print("\n" + "=" * 80)
    print("🎯 MASTER SEEDING COMPLETE: Environment is now ready.")
    print("=" * 80)

if __name__ == "__main__":
    run_master_seed()
