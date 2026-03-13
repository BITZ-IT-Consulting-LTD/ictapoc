import os
import django
import uuid
import logging
import time
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# Configure Celery to run always eager for this test
settings.CELERY_TASK_ALWAYS_EAGER = True

from service_api.models import ServiceConfig, User, ServiceRequest, WorkflowStep, AuditLog, WorkflowStepExecution
from service_api.workflow import WorkflowEngine

def verify_celery_workflow():
    print("--- Starting Celery Workflow Verification ---")
    
    # 1. Setup Data
    try:
        citizen = User.objects.get(username='mary')
        service = ServiceConfig.objects.get(service_code='CRS-BIRTH-REG')
    except (User.DoesNotExist, ServiceConfig.DoesNotExist) as e:
        print(f"Error setting up test data: {e}")
        return

    payload = {
        "child_name": "Test Baby",
        "birth_date": "2026-01-01",
        "hospital_name": "Nairobi Hospital",
        "parent1_id": "ID12345678"
    }

    # 2. Trigger Workflow
    engine = WorkflowEngine()
    print(f"Creating Service Request for {service.service_name}...")
    request = engine.create_service_request(citizen, service, payload)
    
    request_id = request.request_id
    print(f"Request {request_id} created.")

    # Trigger the background task manually via delay (sync due to EAGER)
    print("Manually triggering Celery task for the first api_call step...")
    from service_api.tasks import execute_system_step_task
    execute_system_step_task.delay(request_id, request.current_step.id)

    time.sleep(1) # Extra buffer for Celery eager execution

    # 3. Verify Initial State
    # Since CELERY_TASK_ALWAYS_EAGER is True, the first step (api_call) 
    # should have already executed synchronously via the Celery task.
    
    request.refresh_from_db()
    print(f"Current Status: {request.status}")
    print(f"Current Step: {request.current_step.step_name if request.current_step else 'None'}")
    
    # 4. Check Audit Logs
    logs = AuditLog.objects.filter(service_request=request).order_by('timestamp')
    print("\n--- Audit Logs ---")
    for log in logs:
        print(f"[{log.timestamp.strftime('%H:%M:%S')}] {log.action}: {log.details}")

    # 5. Check Execution Records
    executions = WorkflowStepExecution.objects.filter(service_request=request).order_by('started_at')
    print("\n--- Execution Records ---")
    for ex in executions:
        print(f"Step {ex.step.sequence} ({ex.step.step_name}): Status={ex.status}, Action={ex.action_taken}")

    # Success criteria:
    # 1. First step (Sequence 1) was an api_call.
    # 2. It should have transitioned to sequence 2 (manual check).
    
    if request.current_step and request.current_step.sequence == 2:
        print("\n✅ SUCCESS: Workflow transitioned to Step 2 after background API call.")
    else:
        print("\n❌ FAILURE: Workflow did not reach Step 2 as expected.")

if __name__ == "__main__":
    verify_celery_workflow()
