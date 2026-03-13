import os
import django
import sys
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Q
from django.db import transaction

# Setup Django environment
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceRequest, WorkflowStep, AuditLog, User, MDA
from service_api.workflow import WorkflowEngine

def fix_workflow_engine():
    print("=" * 80)
    print("🛠️  WORKFLOW ENGINE AUDIT & AUTO-HEAL SCRIPT")
    print("=" * 80)

    now = timezone.now()
    stuck_threshold = now - timedelta(hours=24)
    
    stats = {
        "total_audited": 0,
        "stuck_tasks_found": 0,
        "consistency_fixes": 0,
        "next_step_repairs": 0,
        "auto_assignments": 0,
        "errors": 0
    }

    # 1. AUDIT STUCK TASKS (> 24h in user_task)
    print(f"\n🔍 1. Auditing tasks stuck since {stuck_threshold}...")
    stuck_requests = ServiceRequest.objects.filter(
        status__in=['in_progress', 'received'],
        current_step__bpmn_element_type='user_task',
        updated_at__lt=stuck_threshold
    )
    stats["stuck_tasks_found"] = stuck_requests.count()
    print(f"Found {stats['stuck_tasks_found']} potentially stuck human tasks.")

    # 2. VERIFY ACTION CONSISTENCY
    # Check if a human already clicked "Approve" but DB didn't advance
    for req in stuck_requests:
        stats["total_audited"] += 1
        # Find latest action log for this request
        last_action = AuditLog.objects.filter(
            service_request=req,
            action__icontains='OFFICER_ACTION'
        ).order_by('-timestamp').first()

        if last_action and last_action.timestamp > req.current_step.id: # Rough check if it happened during this step
            # More precise: check if action happened after req.updated_at (when step was assigned)
            # But updated_at might have changed. Let's check against latest STEP_TRANSITION
            last_transition = AuditLog.objects.filter(
                service_request=req,
                action='STEP_TRANSITION'
            ).order_by('-timestamp').first()
            
            if last_transition and last_action.timestamp > last_transition.timestamp:
                print(f"  ✨ HEAL: Request {req.request_id} has completed action '{last_action.action}' but is still on Step {req.current_step.sequence}. Advancing...")
                try:
                    engine = WorkflowEngine(request_id=req.request_id)
                    engine.process_workflow_step()
                    stats["consistency_fixes"] += 1
                except Exception as e:
                    print(f"  ❌ Error advancing {req.request_id}: {e}")
                    stats["errors"] += 1

    # 3. FIX SYSTEM TASKS STUCK IN IN_PROGRESS
    # Often happens if a background process failed during api_call
    print("\n🔍 2. Repairing system tasks stuck in transit...")
    system_stuck = ServiceRequest.objects.filter(
        status='in_progress',
        current_step__step_type='api_call',
        updated_at__lt=now - timedelta(minutes=30) # System tasks shouldn't take > 30 mins
    )
    
    for req in system_stuck:
        print(f"  ⚙️  REPAIR: Request {req.request_id} stuck at API Call '{req.current_step.step_name}'. Retrying...")
        try:
            engine = WorkflowEngine(request_id=req.request_id)
            # Re-calling workflow step logic will re-trigger the API call or advance
            engine.process_workflow_step()
            stats["next_step_repairs"] += 1
        except Exception as e:
             print(f"  ❌ Error repairing {req.request_id}: {e}")
             stats["errors"] += 1

    # 4. AUTO-ASSIGN UNASSIGNED TASKS
    print("\n🔍 3. Auto-assigning unassigned human tasks...")
    unassigned = ServiceRequest.objects.filter(
        status='in_progress',
        current_step__bpmn_element_type='user_task',
        assigned_to__isnull=True
    )

    for req in unassigned:
        target_role = req.current_step.role
        target_mda = req.current_step.target_mda
        
        # Build queryset for eligible officers
        eligible_query = Q(role__icontains=target_role) | Q(user_role__name__icontains=target_role)
        if target_mda:
            eligible_query &= (Q(mda=target_mda) | Q(assigned_mdas=target_mda))
        
        eligible_officers = User.objects.filter(eligible_query).annotate(
            task_load=Count('assigned_tasks', filter=Q(assigned_tasks__status='in_progress'))
        ).order_by('task_load')

        if eligible_officers.exists():
            best_officer = eligible_officers.first()
            req.assigned_to = best_officer
            req.save()
            
            AuditLog.objects.create(
                service_request=req,
                action='AUTO_ASSIGNMENT',
                details=f"Task auto-assigned to {best_officer.username} (Current Load: {best_officer.task_load})"
            )
            print(f"  👤 ASSIGN: Request {req.request_id} -> {best_officer.username} ({target_role})")
            stats["auto_assignments"] += 1
        else:
            print(f"  ⚠️ Warning: No eligible officers found for {req.request_id} with role '{target_role}'")

    # 5. FINAL REPORT
    print("\n" + "=" * 80)
    print("📊 FINAL AUDIT REPORT")
    print("-" * 80)
    print(f"Total Requests Audited:      {stats['total_audited']}")
    print(f"Stuck Human Tasks Found:     {stats['stuck_tasks_found']}")
    print(f"Consistency Fixes (Action):  {stats['consistency_fixes']}")
    print(f"System Task Repairs:         {stats['next_step_repairs']}")
    print(f"Auto-Assignments Made:       {stats['auto_assignments']}")
    print(f"Processing Errors:           {stats['errors']}")
    print("=" * 80)
    print("✅ Workflow Engine Optimized.")

if __name__ == "__main__":
    fix_workflow_engine()
