import os
import django
import uuid
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import User, MDA, ServiceConfig, ServiceRequest, WorkflowStep

def seed_test_requests():
    print("🚀 Seeding test requests for RBAC demo...")
    
    citizen, _ = User.objects.get_or_create(username="maggy1", defaults={"role": "citizen"})
    
    # Get MDAs
    moh = MDA.objects.filter(code="MOH").first()
    moe = MDA.objects.filter(code="MOE").first()
    
    if not moh or not moe:
        print("❌ MOH or MOE MDA missing. Ensure you ran seed_demo_users.py first.")
        return

    # Create/Get ServiceConfigs
    svc_health, _ = ServiceConfig.objects.get_or_create(
        service_code="MOH-TEST-01",
        defaults={"service_name": "Health Facility License", "mda": moh, "description": "Annual licensing for health facilities."}
    )
    
    svc_edu, _ = ServiceConfig.objects.get_or_create(
        service_code="MOE-TEST-01",
        defaults={"service_name": "School Registration", "mda": moe, "description": "Registering new private schools."}
    )

    # Ensure Workflow Steps exist for these (minimal)
    for svc in [svc_health, svc_edu]:
        if not WorkflowStep.objects.filter(service_config=svc).exists():
           WorkflowStep.objects.create(
               service_config=svc,
               step_name="Officer Review",
               sequence=1,
               role="officer",
               action="review",
               lifecycle_stage="to_be"
           )
           WorkflowStep.objects.create(
               service_config=svc,
               step_name="Supervisor Approval",
               sequence=2,
               role="supervisor",
               action="approve",
               lifecycle_stage="to_be"
           )

    # Create Requests (Idempotent check)
    # DEPRECATED: User requested to remove service request seeding data
    """
    if ServiceRequest.objects.filter(service_config=svc_health).count() < 5:
        for i in range(5):
            # Health Requests
            ServiceRequest.objects.create(
                request_id=f"MOH-{uuid.uuid4().hex[:6].upper()}",
                citizen=citizen,
                service_config=svc_health,
                current_step=svc_health.workflow_steps.first(),
                status="in_progress",
                payload={"facility_name": f"Clinic {i}", "location": "Nairobi"}
            )
    
    if ServiceRequest.objects.filter(service_config=svc_edu).count() < 5:
        for i in range(5):
            # Education Requests
            ServiceRequest.objects.create(
                request_id=f"MOE-{uuid.uuid4().hex[:6].upper()}",
                citizen=citizen,
                service_config=svc_edu,
                current_step=svc_edu.workflow_steps.first(),
                status="in_progress",
                payload={"school_name": f"Academy {i}", "students": 100}
            )
    
    print(f"✅ Created 10 requests (5 MOH, 5 MOE).")
    """
    print("✅ Skipped service request seeding as per request.")


if __name__ == "__main__":
    seed_test_requests()
