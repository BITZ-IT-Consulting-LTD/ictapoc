import os
import django
from django.db import transaction
from django.db.models import Q, F

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceRequest, ServiceConfig, WorkflowStep, AuditLog, User
from service_api.workflow import WorkflowEngine

def fix_approval_chain():
    print("=" * 80)
    print("📋 WORKFLOW APPROVAL CHAIN AUDIT & REPAIR SCRIPT")
    print("=" * 80)

    # 1. VALIDATE SEQUENCES: Generic and Lifecycle Services
    print("\n🔍 Validating WorkflowStep definitions...")
    configs = ServiceConfig.objects.all()
    for config in configs:
        for stage in ['as_is', 'to_be']:
            # Find the highest officer step
            officer_step = WorkflowStep.objects.filter(
                service_config=config, 
                lifecycle_stage=stage,
                role__icontains='officer'
            ).order_by('-sequence').first()

            if officer_step:
                # Check if a supervisor step follows it
                supervisor_exists = WorkflowStep.objects.filter(
                    service_config=config,
                    lifecycle_stage=stage,
                    role__icontains='supervisor',
                    sequence__gt=officer_step.sequence
                ).exists()

                if not supervisor_exists:
                    print(f"  [!] Missing Supervisor step for '{config.service_name}' ({stage}). Patching...")
                    # Insert supervisor step
                    WorkflowStep.objects.create(
                        service_config=config,
                        step_name="Supervisor Final Approval",
                        step_type="manual",
                        role="supervisor",
                        sequence=officer_step.sequence + 1,
                        lifecycle_stage=stage
                    )
                    # Shift any subsequent steps (unlikely but safe)
                    WorkflowStep.objects.filter(
                        service_config=config,
                        lifecycle_stage=stage,
                        sequence__gt=officer_step.sequence
                    ).exclude(role='supervisor').update(sequence=F('sequence') + 1)

    # 2. REPAIR STUCK REQUESTS
    print("\n🚿 Scanning for requests prematurely approved by Officers...")
    # These are approved but AuditLog shows an Officer was the last to click 'approve'
    stuck_requests = ServiceRequest.objects.filter(status__in=['approved', 'closed'])
    repaired_count = 0

    for req in stuck_requests:
        # Get last audit log for approval
        last_log = AuditLog.objects.filter(service_request=req, action__icontains='ACTION_APPROVE').order_by('-timestamp').first()
        
        if last_log and last_log.actor and last_log.actor.role in ['officer', 'MDA_OFFICER']:
            # This was approved by an officer. Check if there are now supervisor steps they skipped.
            # (Note: Since we just patched the definitions above, they will exist now)
            
            # Since the request is terminal, we need to find the step after the officer's step.
            officer_step = WorkflowStep.objects.filter(
                service_config=req.service_config,
                role__icontains='officer'
            ).order_by('-sequence').first()

            if officer_step:
                next_step = WorkflowStep.objects.filter(
                    service_config=req.service_config,
                    sequence__gt=officer_step.sequence
                ).order_by('sequence').first()

                if next_step and next_step.role in ['supervisor', 'MDA_SUPERVISOR', 'system_admin', 'registrar']:
                    print(f"  [*] Repairing Request {req.request_id} ({req.service_config.service_name})")
                    print(f"      Status: {req.status} -> IN_PROGRESS")
                    print(f"      Advancing to: {next_step.role} ({next_step.step_name})")
                    
                    with transaction.atomic():
                        req.status = 'in_progress'
                        req.current_step = next_step
                        req.assigned_to = None # Reset for pool acquisition
                        req.save()

                        AuditLog.objects.create(
                            service_request=req,
                            action='FIX_WORKFLOW_REOPENED',
                            details=f"Request reopened by repair script. Previous '{last_log.actor.role}' approval was missing subsequent 'Supervisor' sign-off."
                        )
                    
                    repaired_count += 1

    # 3. VERIFY HIERARCHY INTEGRITY
    print(f"\n✅ REPAIR COMPLETE. Requests Reopened: {repaired_count}")
    print("=" * 80)

if __name__ == "__main__":
    fix_approval_chain()
