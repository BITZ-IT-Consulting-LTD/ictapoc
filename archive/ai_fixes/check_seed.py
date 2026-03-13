import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig, WorkflowStep

def check_seed_status():
    print("--- SEEDING STATUS CHECK ---")
    services = ServiceConfig.objects.all()
    print(f"Total Services: {services.count()}")
    print(f"Total Workflow Steps: {WorkflowStep.objects.count()}")
    
    print("\nService Breakdown:")
    for svc in services:
        as_is_count = svc.workflow_steps.filter(lifecycle_stage='as_is').count()
        to_be_count = svc.workflow_steps.filter(lifecycle_stage='to_be').count()
        print(f" - {svc.service_name} ({svc.service_code}):")
        print(f"   * As-Is Steps: {as_is_count}")
        print(f"   * To-Be Steps: {to_be_count}")
        if as_is_count == 0 and to_be_count == 0:
            print("   !!! WARNING: NO WORKFLOW STEPS FOUND !!!")

if __name__ == '__main__':
    check_seed_status()
