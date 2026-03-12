import os
import json
import re
from django.core.management.base import BaseCommand
from service_api.models import MDA, ServiceConfig, ServiceCategory, ServiceDomain, WorkflowStep, ServiceFamily, ServiceGroup

class Command(BaseCommand):
    help = "Seeds priority MDA services and processes from parsed docs (Focus: TO-BE workflows and priority flags)"

    def get_unique_mda_code(self, name):
        words = [w for w in re.split(r'\W+', name) if len(w) > 2]
        if len(words) >= 3:
            base_code = (words[0][0] + words[1][0] + words[2][0]).upper()
        elif len(words) == 2:
            base_code = (words[0][:2] + words[1][0]).upper()
        else:
            base_code = (name[:3]).upper()
        
        mda_code = f"{base_code}-PRI"
        counter = 1
        while MDA.objects.filter(code=mda_code).exists():
            mda_code = f"{base_code}{counter}-PRI"
            counter += 1
        return mda_code

    def handle(self, *args, **options):
        json_path = "/app/mda_data.json"
        if not os.path.exists(json_path):
            json_path = "mda_data.json"
            if not os.path.exists(json_path):
                self.stdout.write(self.style.ERROR(f"Data file not found: {json_path}"))
                return

        with open(json_path, 'r') as f:
            full_data = json.load(f)

        priority_mda_names = full_data.get('priority_mdas', [])
        services_data = full_data.get('services', [])

        self.stdout.write(self.style.MIGRATE_HEADING(f"\nUPDATING PRIORITY MDAs AND {len(services_data)} DIGITAL SERVICES..."))
        
        domain, _ = ServiceDomain.objects.get_or_create(name="Digital Government Services")
        category, _ = ServiceCategory.objects.get_or_create(name="Priority MDAs", domain=domain)
        family, _ = ServiceFamily.objects.get_or_create(name="Priority MDA Documents")
        group, _ = ServiceGroup.objects.get_or_create(name="Priority MDAs")

        # 1. Broad Update for MDAs from Matrix
        for mda_name in priority_mda_names:
            # Search by name fragments for better matching
            mda = MDA.objects.filter(name__icontains=mda_name).first()
            if not mda:
                mda_code = self.get_unique_mda_code(mda_name)
                mda, _ = MDA.objects.get_or_create(
                    name=mda_name,
                    defaults={'code': mda_code, 'is_priority': True}
                )
            else:
                mda.is_priority = True
                mda.save(update_fields=['is_priority'])
                # Mark all their services as high priority if they are in the matrix
                ServiceConfig.objects.filter(mda=mda).update(priority='high')

        # 2. Specific Seeding for Services with Documentation
        for r in services_data:
            mda_name = r['mda_name']
            mda = MDA.objects.filter(name__icontains=mda_name).first()
            if not mda:
                mda_code = self.get_unique_mda_code(mda_name)
                mda, _ = MDA.objects.get_or_create(
                    name=mda_name,
                    defaults={'code': mda_code, 'is_priority': True}
                )
            else:
                mda.is_priority = True
                mda.save(update_fields=['is_priority'])

            svc_name = r['process_name']
            svc_code = f"DOC-{mda.code}-{svc_name[:10].upper().replace(' ', '')}"
            
            svc, created = ServiceConfig.objects.update_or_create(
                service_code=svc_code,
                defaults={
                    'service_name': svc_name,
                    'mda': mda,
                    'category': category,
                    'service_family': family,
                    'service_type': r['service_model'],
                    'pain_points': r.get('pain_points', []),
                    'is_public_facing': True,
                    'catalogue_visible': True,
                    'priority': 'high'
                }
            )
            svc.service_groups.add(group)

            # --- KEY FIX: SEED ONLY THE TO-BE STEPS AS THE RUNNING WORKFLOW ---
            WorkflowStep.objects.filter(service_config=svc).delete()
            
            steps = r.get('steps', [])
            if steps:
                for step in steps:
                    # We seed them as 'as_is' so they are the "current" primary journey
                    WorkflowStep.objects.create(
                        service_config=svc,
                        step_name=step['step_name'],
                        role=step['role'],
                        logic_config={'tool': step['tool']},
                        sequence=step['sequence'],
                        lifecycle_stage='as_is' 
                    )
            else:
                self.stdout.write(self.style.WARNING(f"  ⚠  No workflow steps found for: {svc_name}"))

        self.stdout.write(self.style.SUCCESS("\n✅ Priority MDAs updated and digital TO-BE journeys seeded as primary workflows."))
