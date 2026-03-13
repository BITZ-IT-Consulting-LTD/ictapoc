import os
import django
import logging
from unittest.mock import patch

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.conf import settings
settings.CELERY_TASK_ALWAYS_EAGER = True
# Mock transaction.on_commit to run immediately (simulating post-commit in test)
from django.db import transaction
from unittest.mock import MagicMock
transaction.on_commit = lambda f: f()

from service_api.models import ServiceConfig, User, ServiceRequest, WorkflowStep, AuditLog, WorkflowStepExecution
from service_api.workflow import WorkflowEngine

def simulate_lifecycle_activity():
    print("--- 👶 Simulating Lifecycle Activity: Birth Registration (CRS-BIRTH-REG) ---")
    
    with transaction.atomic():
        # Identify the citizen (e.g., 'mary') and officer
        try:
            citizen = User.objects.get(username='mary')
            service = ServiceConfig.objects.get(service_code='CRS-BIRTH-REG')
            officer = User.objects.get(username='officer1')
        except (User.DoesNotExist, ServiceConfig.DoesNotExist) as e:
            print(f"ERROR: Essential test data missing. {e}")
            return

        payload = {
            "child_name": "Antigravity Jr.",
            "birth_date": "2026-03-07",
            "hospital_name": "Nairobi National Hospital",
            "parent1_id": "ID-MOM-X123", # This will fail in our mock below
        }

        # --- SCENARIO 1: Automated Verification Fails (Transition to Manual Fallback) ---
        print("\n[Scenario 1] Parent Identity Verification Fails (KeSEL Mock)")
        
        with patch('service_api.kesel.KeSEL.exchange') as mock_exchange:
            # Mock failure (e.g. ID not found or discrepancy found)
            mock_exchange.return_value = {"status": "FAILED", "message": "ID Record found but Biometric discrepancy identified."}
            
            engine = WorkflowEngine()
            request = engine.create_service_request(citizen, service, payload)
            request_id = request.request_id
            
            # Verify landing at Step 3 (Fallback)
            request.refresh_from_db()
            print(f"  -> Request ID: {request_id}")
            print(f"  -> Current Status: {request.status}")
            print(f"  -> Current Step Sequence: {request.current_step.sequence if request.current_step else 'None'}")
            print(f"  -> Current Step Name: {request.current_step.step_name if request.current_step else 'None'}")
            
            if request.current_step and "failed" in request.current_step.step_name.lower():
                print("  ✅ SUCCESS: Request correctly routed to Manual Fallback after API failure.")
            else:
                print("  ❌ FAILURE: Routing logic did not land on fallback step.")

        # --- SCENARIO 2: Officer Overrides and Fixes the Workflow ---
        print("\n[Scenario 2] Officer Reviews and Approves After Manual Correction")
        
        # Reset engine with the request context
        engine = WorkflowEngine(request_id)
        
        # Simulate officer claiming the task
        request.assigned_to = officer
        request.save()
        
        # Re-initialize engine to refresh its internal service_request with the assignment
        engine = WorkflowEngine(request_id)
        
        # Simulate officer's review and approval action
        engine.complete_manual_step(officer, action='approve', details="Parents identity manually verified via physical documents.")
        
        request.refresh_from_db()
        print(f"  -> Current status: {request.status}")
        print(f"  -> Current Step: {request.current_step.step_name if request.current_step else 'None'}")
        
        if request.current_step and request.current_step.sequence == 4:
            print("  ✅ SUCCESS: Officer approval advanced the workflow from fallback to 'Mint Maisha Namba'.")
        else:
            print("  ❌ FAILURE: Workflow did not advance to expected next step.")

        # --- Audit Log View ---
        print(f"\n--- Final Lifecycle Audit Trail for Request {request_id} ---")
        logs = AuditLog.objects.filter(service_request=request).order_from_timestamp() if hasattr(AuditLog.objects, 'order_from_timestamp') else AuditLog.objects.filter(service_request=request).order_by('timestamp')
        for log in logs:
            print(f"  [{log.timestamp.strftime('%H:%M:%S')}] {log.action}: {log.details}")

if __name__ == "__main__":
    simulate_lifecycle_activity()
