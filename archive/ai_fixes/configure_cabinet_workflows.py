
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep, ServiceDomain, ServiceCategory, ServiceRequest, User

def configure():
    mda = MDA.objects.filter(name__icontains='Cabinet Affairs').first()
    if not mda:
        print("Cabinet Affairs MDA not found.")
        return

    domain, _ = ServiceDomain.objects.get_or_create(name="Cabinet & Executive Services")
    cat_records, _ = ServiceCategory.objects.get_or_create(name="Records & EDRMS", domain=domain)
    cat_delivery, _ = ServiceCategory.objects.get_or_create(name="Government Delivery", domain=domain)
    cat_fleet, _ = ServiceCategory.objects.get_or_create(name="Support Services", domain=domain)

    # 1. CABINET MEMORANDA & MAIL MANAGEMENT
    wf1_config = {
        "service_name": "Cabinet Correspondence & Memoranda Management",
        "service_code": "CAB-MEM-001",
        "category": cat_records,
        "mda": mda,
        "description": "End-to-end management of classified and ordinary Cabinet correspondence.",
        "config": {"environment": "POC", "lifecycle": "active"}
    }
    svc1, _ = ServiceConfig.objects.get_or_create(service_code=wf1_config["service_code"], defaults=wf1_config)
    
    steps1 = [
        (1, "Receive Incoming Mail", "manual", "registrar", "receive_mail"),
        (2, "Classify Mail", "manual", "supervisor", "classify"),
        (3, "Register Correspondence", "manual", "registrar", "register"),
        (4, "Mark-Out for Action", "manual", "supervisor", "mark_out"),
        (5, "Action and Drafting", "manual", "officer", "draft"),
        (6, "Review and Approval", "manual", "supervisor", "approve"),
        (7, "Dispatch or Submission", "manual", "registrar", "dispatch"),
        (8, "Records Closure & Archiving", "api_call", "system_admin", "archive"),
    ]
    for seq, name, stype, role, act in steps1:
        WorkflowStep.objects.get_or_create(
            service_config=svc1, sequence=seq,
            defaults={"step_name": name, "step_type": stype, "role": role, "action": act}
        )

    # 2. GDMIS REPORTING
    wf2_config = {
        "service_name": "Government Delivery Monitoring & Reporting",
        "service_code": "CAB-GDMIS-001",
        "category": cat_delivery,
        "mda": mda,
        "description": "Tracking implementation of Cabinet decisions and directives.",
        "config": {"environment": "POC", "lifecycle": "active"}
    }
    svc2, _ = ServiceConfig.objects.get_or_create(service_code=wf2_config["service_code"], defaults=wf2_config)
    
    steps2 = [
        (1, "Issue Directive", "manual", "system_admin", "issue"),
        (2, "Communicate to MDAs", "manual", "mda_admin", "communicate"),
        (3, "Committee Review", "manual", "supervisor", "review"),
        (4, "Prepare Progress Report", "manual", "officer", "prepare_report"),
        (5, "Submit Report", "manual", "officer", "submit"),
        (6, "Monitor Implementation", "manual", "officer", "monitor"),
    ]
    for seq, name, stype, role, act in steps2:
        WorkflowStep.objects.get_or_create(
            service_config=svc2, sequence=seq,
            defaults={"step_name": name, "step_type": stype, "role": role, "action": act}
        )

    # 3. FLEET MANAGEMENT
    wf3_config = {
        "service_name": "Fleet & Transport Management",
        "service_code": "CAB-FLEET-001",
        "category": cat_fleet,
        "mda": mda,
        "description": "Digital management of vehicle requests and trip logs.",
        "config": {"environment": "POC", "lifecycle": "active"}
    }
    svc3, _ = ServiceConfig.objects.get_or_create(service_code=wf3_config["service_code"], defaults=wf3_config)
    
    steps3 = [
        (1, "Vehicle Request", "manual", "officer", "request"),
        (2, "Review and Authorize", "manual", "supervisor", "authorize"),
        (3, "Driver Assignment", "manual", "supervisor", "assign_driver"),
        (4, "Trip Preparation", "manual", "officer", "prepare"),
        (5, "Trip Execution", "manual", "officer", "execute"),
        (6, "Record Review & Approval", "manual", "supervisor", "approve_trip"),
    ]
    for seq, name, stype, role, act in steps3:
        WorkflowStep.objects.get_or_create(
            service_config=svc3, sequence=seq,
            defaults={"step_name": name, "step_type": stype, "role": role, "action": act}
        )

    print(f"Workflows configured: {svc1.id}, {svc2.id}, {svc3.id}")

    # Generate test users if missing
    # ... logic already handled in seed_priority_mdas but let's ensure we have some specific ones
    
    # DEPRECATED: User requested clean slate without sample applications.
    """
    # Generate Sample Data (5 instances per workflow)
    citizen = User.objects.filter(role='citizen').first()
    if not citizen:
        citizen = User.objects.create_user(username='sample_citizen', password='Starten1@', email='cit@test.com', role='citizen')

    for svc in [svc1, svc2, svc3]:
        for i in range(5):
            ServiceRequest.objects.create(
                request_id=f"CAB-{svc.service_code}-{i}",
                service_config=svc,
                citizen=citizen,
                status='received',
                current_step=svc.workflow_steps.first(),
                payload={"sample_id": i, "notes": "POC Automated Test Entry"}
            )
    print("Sample test data generated.")
    """
    print("✅ Sample test data generation skipped.")


if __name__ == "__main__":
    configure()
