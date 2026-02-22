import os
import django
from django.db import transaction

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceRequest, ServiceConfig, WorkflowStep, AuditLog
from service_api.workflow import WorkflowEngine

def fix_dynamic_workflow():
    print("=" * 80)
    print("⚙️ DYNAMIC WORKFLOW ENGINE: AUDIT & REPAIR")
    print("=" * 80)

    # 1. Audit Service Configurations
    print("\n🔍 Auditing Service Configurations...")
    configs = ServiceConfig.objects.all()
    for config in configs:
        steps_count = WorkflowStep.objects.filter(service_config=config).count()
        if steps_count == 0:
            print(f"  [!] ALERT: Service '{config.service_name}' has ZERO workflow steps. It will auto-approve immediately.")
        else:
            print(f"  [OK] '{config.service_name}' has {steps_count} configured steps.")

    # 2. Identify and Repair Hanging Requests
    print("\n🚿 Scanning for 'Hanging' Requests (In Progress without Current Step)...")
    hanging_requests = ServiceRequest.objects.filter(
        status='in_progress',
        current_step__isnull=True
    )
    
    print(f"  Detected {hanging_requests.count()} hanging requests.")
    
    repaired_count = 0
    for req in hanging_requests:
        print(f"  [*] Repairing {req.request_id} ({req.service_config.service_name})")
        engine = WorkflowEngine(request_id=req.request_id)
        
        # Triggering process_workflow_step will find step 1 if it was stuck
        with transaction.atomic():
            engine.process_workflow_step()
            req.refresh_from_db()
            if req.current_step:
                print(f"      -> Advanced to Step {req.current_step.sequence}: {req.current_step.step_name}")
                repaired_count += 1
            else:
                print(f"      -> Still no step found. Finalizing if approved.")

    # 3. Resume 'Received' but Not Started
    print("\n🕒 Scanning for 'Received' requests that haven't initialized...")
    received_requests = ServiceRequest.objects.filter(status='received')
    init_count = 0
    for req in received_requests:
        print(f"  [*] Initializing {req.request_id}")
        engine = WorkflowEngine(request_id=req.request_id)
        engine.process_workflow_step()
        init_count += 1

    print(f"\n✅ REPAIR COMPLETE.")
    print(f"  Total Hanging Repaired: {repaired_count}")
    print(f"  Total Received Initialized: {init_count}")
    print("=" * 80)

if __name__ == "__main__":
    fix_dynamic_workflow()
