import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import WorkflowStep

def fix_and_enrich_workflows():
    print("--- FIXING & ENRICHING WORKFLOW STEPS ---")
    
    steps = WorkflowStep.objects.all()
    count_fixed = 0
    count_enriched = 0
    
    for step in steps:
        modified = False
        
        # 1. Fix BPMN Element Types
        # Some were seeded as 'gateway', but model/frontend expect 'exclusive_gateway'
        if step.bpmn_element_type == 'gateway':
            step.bpmn_element_type = 'exclusive_gateway'
            modified = True
            
        if step.bpmn_element_type == 'user_task' and step.step_type == 'api_call':
            step.bpmn_element_type = 'service_task'
            modified = True

        # 2. Functional Enrichment
        # If the step name implies an automated process, upgrade it from 'manual'
        auto_keywords = ['verify', 'validation', 'check', 'query', 'registry', 'iprs', 'itax', 'knec', 'match']
        name_lower = step.step_name.lower()
        
        if any(kw in name_lower for kw in auto_keywords) and step.step_type == 'manual':
            # Only upgrade if it sounds like a system check
            if 'officer' not in name_lower and 'manual' not in name_lower:
                step.step_type = 'api_call'
                step.bpmn_element_type = 'service_task'
                if not step.role or step.role == 'officer':
                    step.role = 'system'
                count_enriched += 1
                modified = True
        
        # If it's a Gateway, ensure it's a gateway type
        if '?' in step.step_name or '{' in step.step_name or 'OK' in step.step_name:
             if step.bpmn_element_type != 'exclusive_gateway':
                 step.bpmn_element_type = 'exclusive_gateway'
                 modified = True

        if modified:
            step.save()
            count_fixed += 1
            
    print(f"Fixed/Updated {count_fixed} steps.")
    print(f"Functionally Enriched {count_enriched} manual steps to automated tasks.")
    print("--- DONE ---")

if __name__ == '__main__':
    fix_and_enrich_workflows()
