import os
import django
import time
from unittest.mock import patch
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
from service_api.models import ServiceConfig, User, ServiceRequest, WorkflowStep, AuditLog, WorkflowStepExecution
from service_api.workflow import WorkflowEngine

class Command(BaseCommand):
    help = 'Simulates a full lifecycle activity with branching and officer intervention.'

    def handle(self, *args, **options):
        # Force synchronous execution for the demo
        settings.CELERY_TASK_ALWAYS_EAGER = True
        
        # Patch on_commit to execute immediately
        with patch('django.db.transaction.on_commit', lambda f: f()):
             self.simulate_lifecycle_activity()

    def simulate_lifecycle_activity(self):
        self.stdout.write("--- 👶 Simulating Lifecycle Activity: Birth Registration ---")
        
        with transaction.atomic():
            # 1. Setup Data
            try:
                citizen = User.objects.get(username='mary')
                service = ServiceConfig.objects.get(service_code='CRS-BIRTH-REG')
                officer = User.objects.get(username='officer1')
                
                # FORCE Step 1 to use KeSEL instead of internal:// for this demo
                step1 = WorkflowStep.objects.get(service_config=service, sequence=1)
                step1.api_config['url'] = 'HUDUMA_BRIDGE/IPRS/verify'
                step1.save()
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Setup Error: {e}"))
                return

            payload = {
                "child_name": "Antigravity Jr.",
                "birth_date": "2026-03-07",
                "hospital_name": "Nairobi Hospital",
                "parent1_id": "ID-FAIL-999",
            }

            # --- SCENARIO 1: Automated Verification Fails ---
            self.stdout.write("\n[Scenario 1] Parent Identity Verification Fails (Mocked Registry)")
            
            with patch('service_api.kesel.KeSEL.exchange') as mock_exchange:
                mock_exchange.return_value = {"status": "FAILED", "message": "Fingerprint discrepancy found in IPRS."}
                
                engine = WorkflowEngine()
                request = engine.create_service_request(citizen, service, payload)
                request_id = request.request_id
                
                request.refresh_from_db()
                self.stdout.write(f"  -> Request ID: {request_id}")
                self.stdout.write(f"  -> Status: {request.status}")
                self.stdout.write(f"  -> Current Step: {request.current_step.step_name if request.current_step else 'None'}")
                
                # Check if it landed on Step 3 (Fallback) - Note: my repair script might have pointed Step 1 fail to Step 3
                if request.current_step and request.current_step.sequence == 3:
                    self.stdout.write(self.style.SUCCESS("  ✅ SUCCESS: Workflow correctly branched to Manual Fallback (Step 3)."))
                else:
                    self.stdout.write(self.style.WARNING(f"  ⚠️ ALERT: Workflow landed on Step {request.current_step.sequence if request.current_step else 'None'} instead of 3."))

            # --- SCENARIO 2: Officer Approval ---
            self.stdout.write("\n[Scenario 2] Officer Reviews and Overrides Fallback")
            
            # Refresh request object for the next phase
            request.refresh_from_db()
            request.assigned_to = officer
            request.save()
            
            # Re-init engine within the SAME transaction
            engine = WorkflowEngine(request_id)
            engine.complete_manual_step(officer, action='approve', details="Parents physically presented original ID cards. Verified.")
            
            request.refresh_from_db()
            self.stdout.write(f"  -> New Status: {request.status}")
            self.stdout.write(f"  -> New Current Step: {request.current_step.step_name if request.current_step else 'None'}")
            
            if request.current_step and request.current_step.sequence == 4:
                self.stdout.write(self.style.SUCCESS("  ✅ SUCCESS: Officer intervention advanced the lifecycle to 'Mint Maisha Namba'."))
            else:
                self.stdout.write(self.style.ERROR("  ❌ FAILURE: Workflow did not advance as expected."))

            # --- Final Audit Log ---
            self.stdout.write(f"\n--- 📜 Lifecycle Audit Trail for {request_id} ---")
            for log in AuditLog.objects.filter(service_request=request).order_by('timestamp'):
                self.stdout.write(f"  [{log.timestamp.strftime('%H:%M:%S')}] {log.action}: {log.details}")
            
            # Rollback at the end so we don't pollute the actual DB with demo data
            transaction.set_rollback(True)
            self.stdout.write("\n✨ Demo simulated in transient transaction (Rollback successful).")
