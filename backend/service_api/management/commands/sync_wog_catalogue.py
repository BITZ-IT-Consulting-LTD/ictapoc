import json
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from service_api.models import MDA, ServiceConfig, ServiceDomain, ServiceCategory, WorkflowStep

class Command(BaseCommand):
    help = 'Synchronizes the Service Catalogue with a Master JSON file'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='Path to the master JSON file', default='wog_master.json')

    def handle(self, *args, **options):
        file_path = options['file']
        
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        with open(file_path, 'r') as f:
            data = json.load(f)

        self.stdout.write(self.style.SUCCESS(f"Starting sync from {file_path}..."))

        with transaction.atomic():
            for domain_data in data:
                # 1. Sync Domain
                domain_obj, _ = ServiceDomain.objects.get_or_create(
                    name=domain_data['domain_name']
                )

                for process_data in domain_data.get('processes', []):
                    # 2. Sync Category (Process)
                    cat_obj, _ = ServiceCategory.objects.get_or_create(
                        name=process_data['process_name'],
                        domain=domain_obj
                    )

                    for svc_data in process_data.get('services', []):
                        # 3. Handle MDA
                        mda_name = svc_data.get('mda', 'Unknown MDA')
                        mda_obj, _ = MDA.objects.get_or_create(name=mda_name)

                        # 4. Sync Service Config
                        # We try to match by name or by a code derived from the name
                        svc_name = svc_data['service_name']
                        svc_code = svc_name.upper().replace(' ', '_')[:40]
                        
                        svc_obj, created = ServiceConfig.objects.get_or_create(
                            service_name=svc_name,
                            defaults={
                                'service_code': svc_code,
                                'mda': mda_obj,
                                'category': cat_obj
                            }
                        )

                        # Update fields from JSON
                        svc_obj.description = svc_data.get('description', svc_obj.description)
                        svc_obj.digitization_level = svc_data.get('maturity', 1)
                        svc_obj.service_type = svc_data.get('service_type')
                        svc_obj.delivery_channels = svc_data.get('delivery_channels', [])
                        svc_obj.process_complexity = svc_data.get('process_complexity')
                        svc_obj.pain_points = svc_data.get('pain_points', [])
                        svc_obj.associated_systems = svc_data.get('systems', [])
                        svc_obj.associated_actors = svc_data.get('actors', [])
                        svc_obj.category = cat_obj # Ensure category is correct
                        
                        svc_obj.save()

                        # 5. Sync Workflows (if configured in JSON)
                        if svc_data.get('workflow_configured') and svc_data.get('workflow_steps'):
                            # For automation, we clear existing steps for this service to ensure sequence matches JSON
                            WorkflowStep.objects.filter(service_config=svc_obj).delete()
                            
                            for step_data in svc_data['workflow_steps']:
                                WorkflowStep.objects.create(
                                    service_config=svc_obj,
                                    step_name=step_data['step_name'],
                                    role=step_data.get('role', 'officer'),
                                    step_type=step_data.get('step_type', 'manual'),
                                    bpmn_element_type=step_data.get('bpmn_element_type', 'user_task'),
                                    lifecycle_stage=step_data.get('lifecycle_stage', 'as_is'),
                                    sequence=step_data['sequence']
                                )

                        status = "Created" if created else "Updated"
                        self.stdout.write(f"  [{status}] {svc_name}")

        self.stdout.write(self.style.SUCCESS("Synchronization complete!"))
