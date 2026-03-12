import json
from django.core.management.base import BaseCommand
from service_api.models import ServiceConfig, WorkflowStep

class Command(BaseCommand):
    help = 'Validates the structural integrity and BPMN compliance of all WorkflowStep sequences.'

    def handle(self, *args, **options):
        errors_found = False
        services = ServiceConfig.objects.all()

        for service in services:
            for stage in ['as_is', 'to_be']:
                steps = WorkflowStep.objects.filter(service_config=service, lifecycle_stage=stage).order_by('sequence')
                if not steps.exists():
                    continue

                sequences = [s.sequence for s in steps]
                
                # 1. Check for Duplicate Sequences
                seen = set()
                duplicates = [x for x in sequences if x in seen or seen.add(x)]
                if duplicates:
                    errors_found = True
                    for dup in set(duplicates):
                        self.stdout.write(f'[AI_FIX_REQUIRED] Service: "{service.service_code}", Error: "Duplicate Sequence", Detail: "Sequence {dup} appears multiple times in {stage} lifecycle."')

                # 2. BPMN Renderer Compliance Checks
                start_events = steps.filter(bpmn_element_type='start_event').count()
                end_events = steps.filter(bpmn_element_type='end_event').count()

                if start_events != 1:
                    errors_found = True
                    self.stdout.write(f'[AI_FIX_REQUIRED] Service: "{service.service_code}", Error: "BPMN Renderer Compliance", Detail: "Workflow in {stage} stage has {start_events} start_events (exactly 1 required). Frontend renderer may fail."')
                
                if end_events < 1:
                    errors_found = True
                    self.stdout.write(f'[AI_FIX_REQUIRED] Service: "{service.service_code}", Error: "BPMN Renderer Compliance", Detail: "Workflow in {stage} stage has 0 end_events (at least 1 required). Frontend renderer may fail."')

                # 3. Step-specific checks
                for step in steps:
                    # Check API/BPMN alignment
                    if step.step_type == 'api_call' and step.bpmn_element_type != 'service_task':
                         errors_found = True
                         self.stdout.write(f'[AI_FIX_REQUIRED] Service: "{service.service_code}", Error: "BPMN Renderer Compliance", Detail: "Step {step.sequence} is an api_call but not labeled as a service_task. Found: {step.bpmn_element_type}."')

                    if step.step_type == 'api_call':
                        api_config = step.api_config or {}
                        outcomes = api_config.get('outcomes', [])
                        
                        # Check for Missing Target Sequences
                        has_fallback = False
                        for outcome in outcomes:
                            target_seq = outcome.get('target_sequence')
                            if target_seq:
                                if not WorkflowStep.objects.filter(service_config=service, lifecycle_stage=stage, sequence=target_seq).exists():
                                    errors_found = True
                                    self.stdout.write(f'[AI_FIX_REQUIRED] Service: "{service.service_code}", Error: "Missing Target", Detail: "Step {step.sequence} ({step.step_name}) points to target_sequence {target_seq}, but it does not exist in {stage} lifecycle."')
                            
                            label = outcome.get('label', '').lower()
                            if label in ['failure', 'failed', 'rejected', 'manual', 'fallback']:
                                has_fallback = True

                        # Check for Missing Fallbacks for API Calls
                        if not has_fallback:
                            errors_found = True
                            self.stdout.write(f'[AI_FIX_REQUIRED] Service: "{service.service_code}", Error: "Missing Fallback", Detail: "Step {step.sequence} (api_call) lacks a designated failure/manual fallback route in api_config[\'outcomes\']."')

        if not errors_found:
            self.stdout.write(self.style.SUCCESS('All workflows validated successfully.'))
        else:
            self.stdout.write(self.style.ERROR('Workflow validation failed with errors.'))
