
import os
import django
import json
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep, ServiceDomain, ServiceCategory, ServiceRequest, User, Role

def configure_awwda():
    mda = MDA.objects.get(id=45)
    print(f"Configuring AWWDA Workflows for {mda.name}")

    domain, _ = ServiceDomain.objects.get_or_create(name="Public Infrastructure & Water")
    cat_procure, _ = ServiceCategory.objects.get_or_create(name="Procurement & Inventory", domain=domain)
    cat_records, _ = ServiceCategory.objects.get_or_create(name="Corporate Records", domain=domain)

    # 1. Purchasing & Inventory Management
    wf1_config = {
        "service_name": "Procure-to-Pay & Inventory Control",
        "service_code": "AWW-P2P-001",
        "category": cat_procure,
        "mda": mda,
        "description": "Standard Procure-to-Pay workflow including inventory checks and three-way matching.",
        "config": {"environment": "POC", "lifecycle": "active", "integration_points": ["ERP", "Finance"]}
    }
    svc1, _ = ServiceConfig.objects.get_or_create(service_code=wf1_config["service_code"], defaults=wf1_config)
    
    # Remove existing steps if any to avoid ordering issues in POC
    svc1.workflow_steps.all().delete()

    steps1 = [
        (1, "Create Requisition", "manual", "officer", "create_pr"),
        (2, "Requisition Approval", "manual", "supervisor", "approve_pr"),
        (3, "Create Purchase Order", "manual", "officer", "create_po"),
        (4, "Approve and Dispatch PO", "manual", "supervisor", "approve_po"),
        (5, "Receive Goods (GRN)", "manual", "officer", "receive_goods"),
        (6, "Invoice Match & Payment", "manual", "officer", "process_payment"),
    ]
    for seq, name, stype, role, act in steps1:
        WorkflowStep.objects.create(
            service_config=svc1, sequence=seq,
            step_name=name, step_type=stype, role=role, action=act
        )

    # 2. Institutional Records & Mail Management
    wf2_config = {
        "service_name": "Institutional Records & Correspondence Management",
        "service_code": "AWW-RMD-001",
        "category": cat_records,
        "mda": mda,
        "description": "Digitization and management of AWWDA institutional mail and subject files.",
        "config": {"environment": "POC", "lifecycle": "active"}
    }
    svc2, _ = ServiceConfig.objects.get_or_create(service_code=wf2_config["service_code"], defaults=wf2_config)
    
    svc2.workflow_steps.all().delete()

    steps2 = [
        (1, "Receive & Date-Stamp", "manual", "registrar", "receive_mail"),
        (2, "Classify & Register", "manual", "registrar", "classify"),
        (3, "CEO Mark-Out", "manual", "supervisor", "mark_out"),
        (4, "Scan & Digitise", "manual", "registrar", "digitize"),
        (5, "Action & Drafting", "manual", "officer", "draft"),
        (6, "Review & Approval", "manual", "supervisor", "approve"),
        (7, "Dispatch Outgoing", "manual", "registrar", "dispatch"),
        (8, "System Filing & Archiving", "api_call", "system_admin", "archive"),
    ]
    for seq, name, stype, role, act in steps2:
        WorkflowStep.objects.create(
            service_config=svc2, sequence=seq,
            step_name=name, step_type=stype, role=role, action=act
        )

    print(f"Workflows configured: {svc1.id}, {svc2.id}")

    # DEPRECATED: User requested clean slate without sample applications.
    """
    # Generate test data
    citizen = User.objects.filter(role='citizen').first()
    if not citizen:
        # Create a dummy citizen for request tracking if none exists
        citizen_role = Role.objects.get(name='citizen')
        citizen = User.objects.create_user(username='awwda_applicant', password='Starten1@', email='awwda@test.com', role='citizen', user_role=citizen_role)

    # 10 PRs
    for i in range(10):
        ServiceRequest.objects.create(
            request_id=f"AWW-PR-{202600+i}",
            service_config=svc1,
            citizen=citizen,
            status='received',
            current_step=svc1.workflow_steps.first(),
            payload={"item": f"Water Meter Type {random.randint(1,5)}", "quantity": random.randint(10, 500), "urgency": "High"}
        )

    # 15 Correspondence records
    for i in range(15):
        ServiceRequest.objects.create(
            request_id=f"AWW-CORR-{202600+i}",
            service_config=svc2,
            citizen=citizen,
            status='received',
            current_step=svc2.workflow_steps.first(),
            payload={"subject": f"Inquiry regarding project {random.randint(100, 999)}", "confidentiality": "Normal"}
        )
    
    print("Sample test data generated.")
    """
    print("✅ Sample test data generation skipped.")


if __name__ == "__main__":
    configure_awwda()
