
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep, ServiceDomain, ServiceCategory, ServiceRequest, User

def update_passport_workflow():
    mda = MDA.objects.get(id=2)
    print(f"Updating Passport Workflow for {mda.name}")

    # Ensure Category exists
    domain = ServiceDomain.objects.filter(name__icontains="Interior").first()
    if not domain:
        domain = ServiceDomain.objects.create(name="Interior & National Administration")
    
    cat, _ = ServiceCategory.objects.get_or_create(name="Passport & Travel Documents", domain=domain)

    # 1. Update Service Configuration
    svc_config = {
        "service_name": "Passport Application (First Time Application)",
        "service_code": "PASSPORT_APP",
        "category": cat,
        "mda": mda,
        "description": "Digitized end-to-end passport issuance process eliminating physical files and mandatory prints. Integrated with EDRMS for electronic document management.",
        "digitization_level": 5,
        "config": {
            "environment": "POC",
            "digitization_strategy": "Zero-Paper",
            "edrms_integration": True,
            "biometric_verification": "Mandatory",
            "delivery_type": "Collection"
        }
    }
    
    svc, created = ServiceConfig.objects.update_or_create(
        service_code="PASSPORT_APP",
        defaults=svc_config
    )
    
    # 2. Reset and Define Digitized Workflow Steps
    svc.workflow_steps.all().delete()
    
    steps = [
        (1, "Start Passport Application", "manual", "citizen", "start", "start_event"),
        (2, "Online Application (e-Citizen)", "manual", "citizen", "online_apply", "user_task"),
        (3, "Biometric Capture & Verification", "manual", "registrar", "biometrics_capture", "user_task"),
        (4, "Index Digital File", "api_call", "system_admin", "index_digital_file", "service_task"),
        (5, "Electronic Recommendation", "manual", "officer", "recommend", "user_task"),
        (6, "Approval Decision Gateway", "manual", "supervisor", "approve", "exclusive_gateway"),
        (7, "Passport Production", "manual", "officer", "produce", "user_task"),
        (8, "Dispatch & Collection", "manual", "registrar", "collect", "user_task"),
        (9, "End Process", "manual", "system_admin", "end", "end_event")
    ]
    
    for seq, name, stype, role, act, btype in steps:
        WorkflowStep.objects.create(
            service_config=svc,
            sequence=seq,
            step_name=name,
            step_type=stype,
            role=role,
            action=act,
            bpmn_element_type=btype
        )

    print(f"Passport Workflow updated successfully. Service ID: {svc.id}")

    # Generate fresh test data for this new flow
    citizen = User.objects.filter(role='citizen').first()
    if citizen:
        # Create a few new requests
        for i in range(5):
            ref_num = f"DIS-PAS-2026-{1000+i}"
            ServiceRequest.objects.create(
                request_id=ref_num,
                service_config=svc,
                citizen=citizen,
                status='received' if i < 2 else 'in_progress',
                current_step=svc.workflow_steps.get(sequence=1) if i < 2 else svc.workflow_steps.get(sequence=2),
                payload={
                    "applicant_name": f"Citizen {i}",
                    "biometrics_status": "Pending" if i < 2 else "Captured",
                    "file_status": "Digital-Only",
                    "priority": "Normal"
                }
            )
        print("Generated 5 new digitized passport test requests.")

if __name__ == "__main__":
    update_passport_workflow()
