import os
import django
import logging

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig, WorkflowStep, AuditLog

def repair_all_workflows():
    print("--- 🛠 Starting Automated Workflow Repair for 27 Priority MDAs ---")
    services = ServiceConfig.objects.all()
    repaired_count = 0
    step_fixes = 0

    for service in services:
        for stage in ['as_is', 'to_be']:
            steps = WorkflowStep.objects.filter(service_config=service, lifecycle_stage=stage).order_by('sequence')
            if not steps.exists():
                continue

            # Identify existing manual review steps for heuristic mapping
            manual_steps = list(steps.filter(step_type='manual'))
            
            # Find or Create a Generic Fallback Step for the service
            fallback_step = None
            for m in manual_steps:
                if any(word in m.step_name.lower() for word in ['fallback', 'failed', 'review', 'exception', 'gateway']):
                    fallback_step = m
                    break
            
            if not fallback_step:
                # Append a generic manual fallback step at the end
                last_seq = steps.last().sequence
                fallback_step = WorkflowStep.objects.create(
                    service_config=service,
                    step_name="[AUTOMATED FALLBACK] Manual Exception Review Required",
                    step_type='manual',
                    lifecycle_stage=stage,
                    sequence=last_seq + 10,  # Far enough apart
                    role='officer'
                )
                print(f"  [+] Created Global Fallback for {service.service_code}: Step {fallback_step.sequence}")

            # Repair API Steps
            api_steps = steps.filter(step_type='api_call')
            for step in api_steps:
                api_config = step.api_config or {}
                outcomes = api_config.get('outcomes', [])
                
                # Check if we already have a failure outcome
                has_failure = any(o.get('label', '').lower() in ['failure', 'failed', 'rejected', 'manual', 'fallback', 'no'] for o in outcomes)
                has_success = any(o.get('label', '').lower() in ['verified', 'success', 'approved', 'yes'] for o in outcomes)

                if not has_failure or not has_success:
                    # Find the immediate next step for the happy path
                    next_step = steps.filter(sequence__gt=step.sequence).first()
                    success_target = next_step.sequence if next_step else None
                    
                    # Heuristic: If Step n+1 is a gateway and Step n+2 contains "Failed", map failure to n+2
                    failure_target = fallback_step.sequence
                    potential_fail = steps.filter(sequence=step.sequence + 2).first()
                    if potential_fail and 'fail' in potential_fail.step_name.lower():
                        failure_target = potential_fail.sequence
                    
                    # Update configuration
                    new_outcomes = [
                        {'label': 'verified', 'target_sequence': success_target},
                        {'label': 'failed', 'target_sequence': failure_target}
                    ]
                    
                    api_config['outcomes'] = new_outcomes
                    step.api_config = api_config
                    step.save()
                    step_fixes += 1
            
            repaired_count += 1

    print(f"\n✨ Repair Complete: {repaired_count} Services Checked, {step_fixes} API Call steps updated with explicit branching.")
    print("--- 🏁 Re-running Validator to Confirm ---")

if __name__ == "__main__":
    repair_all_workflows()
    # Execute validator logic directly via management command
    from django.core.management import call_command
    call_command('validate_workflows')
