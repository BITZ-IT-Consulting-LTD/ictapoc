import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig, WorkflowStep
import json

def audit():
    services = ServiceConfig.objects.all()
    total = services.count()
    missing_workflows = []
    missing_schemas = []
    missing_both = []
    
    print(f"Total Services: {total}")
    
    for s in services:
        has_wf = WorkflowStep.objects.filter(service_config=s).exists()
        
        # Check if form schema exists and has properties
        has_schema = False
        if s.form_schema and isinstance(s.form_schema, dict):
            if s.form_schema.get('properties') or s.form_schema.get('fields'):
                has_schema = True
        
        if not has_wf and not has_schema:
            missing_both.append(s.service_code)
        elif not has_wf:
            missing_workflows.append(s.service_code)
        elif not has_schema:
            missing_schemas.append(s.service_code)

    print(f"\n--- AUDIT RESULTS ---")
    print(f"Services perfectly configured (Both Workflow & Schema): {total - len(missing_workflows) - len(missing_schemas) - len(missing_both)}")
    print(f"Services missing ONLY Workflows: {len(missing_workflows)}")
    print(f"Services missing ONLY Form Schemas: {len(missing_schemas)}")
    print(f"Services missing BOTH Workflows & Schemas: {len(missing_both)}")
    
    if missing_both:
        print("\nSample of services missing both:")
        for c in missing_both[:10]:
            print(f" - {c}")
            
    if missing_workflows:
        print("\nSample of services missing workflows:")
        for c in missing_workflows[:10]:
            print(f" - {c}")
            
    if missing_schemas:
        print("\nSample of services missing schemas:")
        for c in missing_schemas[:10]:
            print(f" - {c}")

if __name__ == '__main__':
    audit()
