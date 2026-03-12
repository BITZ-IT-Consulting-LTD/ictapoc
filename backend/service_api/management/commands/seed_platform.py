from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Aggregated command to seed the entire government platform in the correct order'

    def handle(self, *args, **options):
        self.stdout.write("🏛  Starting Full Platform Seeding...")
        
        # 1. Base Framework
        call_command('seed_rbac_roles')
        call_command('seed_initial_data')
        
        # 2. Catalogs & Services
        call_command('seed_mdas_from_docs')
        
        # 3. Priority MDA Batch Seeding (27 MDAs)
        self.stdout.write("🚀 Seeding Priority MDA Batches...")
        import subprocess
        scripts = [
            'seed_nema_eia.py',
            'seed_crs_birth.py',
            'seed_knqa_validation.py',
            'seed_children_services.py',
            'seed_government_coordination.py',
            'seed_batch_1.py',
            'seed_batch_2.py',
            'seed_batch_3.py',
            'seed_cradle_to_death_batch_1.py',
            'seed_cradle_to_death_batch_2.py',
            'seed_cradle_to_death_batch_3.py',
            'seed_cradle_to_death_batch_4.py'
        ]
        for script in scripts:
            self.stdout.write(f"  - Running {script}...")
            subprocess.run(['python3', script], check=True)

        # 4. Integrations
        call_command('seed_registry_adapters')
        
        # 5. BPR-documented form schemas for priority & cradle-to-death services
        call_command('seed_priority_forms')
        
        # 6. Auto-generate form schemas for remaining services still missing one
        call_command('seed_missing_schemas')
        
        # 7. Users & Demos
        call_command('seed_demo_users')
        
        self.stdout.write(self.style.SUCCESS("✨ FULL PLATFORM SEEDING COMPLETE."))
