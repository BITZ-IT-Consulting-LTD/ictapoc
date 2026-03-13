
import os
import django
import json
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep, ServiceDomain, ServiceCategory, ServiceRequest, User, Role

def get_or_create_mda(name, code, sector):
    mda = MDA.objects.filter(name__icontains=name).first()
    if not mda:
        flags = {
            "EDRMS": "NOT CONFIGURED",
            "MIS": "UNKNOWN",
            "Integration": "PENDING",
            "Infrastructure": "NOT VALIDATED",
            "type": "State Department",
            "sector": sector,
            "seeded_for": "POC"
        }
        mda = MDA.objects.create(
            name=name,
            code=code,
            description=json.dumps(flags)
        )
        print(f"Created MDA: {name}")
    return mda

def configure_workflows():
    # 1. SPECIAL PROGRAMMES
    mda_special = get_or_create_mda("State Department for Special Programmes", "SD-SPEC", "Social Protection")
    dom_social, _ = ServiceDomain.objects.get_or_create(name="Social Assistance & Beneficiary Programmes")
    cat_social, _ = ServiceCategory.objects.get_or_create(name="Beneficiary Management", domain=dom_social)
    
    wf1_config = {
        "service_name": "Social Assistance Beneficiary Lifecycle Management",
        "service_code": "SPEC-SOC-001",
        "category": cat_social,
        "mda": mda_special,
        "description": "L3 Actor-based registry-driven lifecycle for social assistance beneficiaries.",
        "config": {"environment": "POC", "mapping_level": "L3", "lifecycle": ["Active", "Semi-active"]}
    }
    svc1, _ = ServiceConfig.objects.get_or_create(service_code=wf1_config["service_code"], defaults=wf1_config)
    svc1.workflow_steps.all().delete()
    steps1 = [
        (1, "Initiate Application", "manual", "citizen", "initiate"),
        (2, "Register & Capture Data", "manual", "officer", "capture_data"),
        (3, "Eligibility Assessment", "manual", "officer", "assess"),
        (4, "Validate & Approve", "manual", "supervisor", "approve"),
        (5, "Disburse Assistance", "api_call", "system_admin", "disburse"),
        (6, "Monitor & Report", "manual", "supervisor", "monitor"),
        (7, "Close & Classify", "manual", "registrar", "archive")
    ]
    for seq, name, stype, role, act in steps1:
        WorkflowStep.objects.create(service_config=svc1, sequence=seq, step_name=name, step_type=stype, role=role, action=act)

    # 2. CHILDREN SERVICES
    mda_children = MDA.objects.get(id=52)
    dom_child, _ = ServiceDomain.objects.get_or_create(name="Child Protection & Case Management")
    cat_child, _ = ServiceCategory.objects.get_or_create(name="Case Management", domain=dom_child)
    
    wf2_config = {
        "service_name": "Child Protection Case Management",
        "service_code": "CHI-CASE-02",
        "category": cat_child,
        "mda": mda_children,
        "description": "L3 Case-based, high sensitivity workflow for child protection.",
        "config": {"environment": "POC", "mapping_level": "L3", "security": "Confidential", "audit": "Strict"}
    }
    svc2, _ = ServiceConfig.objects.get_or_create(service_code=wf2_config["service_code"], defaults=wf2_config)
    svc2.workflow_steps.all().delete()
    steps2 = [
        (1, "Report & Trigger Case", "manual", "citizen", "report"),
        (2, "Register & Intake", "manual", "officer", "intake"),
        (3, "Assess & Evaluate", "manual", "officer", "assess"),
        (4, "Plan & Approve", "manual", "supervisor", "approve_plan"),
        (5, "Intervene & Deliver", "manual", "officer", "intervene"),
        (6, "Monitor & Review", "manual", "supervisor", "review"),
        (7, "Close & Classify", "manual", "registrar", "archive")
    ]
    for seq, name, stype, role, act in steps2:
        WorkflowStep.objects.create(service_config=svc2, sequence=seq, step_name=name, step_type=stype, role=role, action=act)

    # 3. CHIEF OF STAFF
    mda_cos = get_or_create_mda("Office of the Chief of Staff & Head of Public Service", "COS-HPS", "Executive")
    dom_exec, _ = ServiceDomain.objects.get_or_create(name="Executive Coordination & Oversight")
    cat_exec, _ = ServiceCategory.objects.get_or_create(name="Coordination", domain=dom_exec)
    
    wf3_config = {
        "service_name": "Executive Coordination & Directive Oversight",
        "service_code": "COS-EXEC-001",
        "category": cat_exec,
        "mda": mda_cos,
        "description": "L2 High-level coordination workflow for executive directives.",
        "config": {"environment": "POC", "mapping_level": "L2"}
    }
    svc3, _ = ServiceConfig.objects.get_or_create(service_code=wf3_config["service_code"], defaults=wf3_config)
    svc3.workflow_steps.all().delete()
    steps3 = [
        (1, "Issue Identification", "manual", "supervisor", "identify"),
        (2, "Info Request & Coordination", "manual", "officer", "coordinate"),
        (3, "Consolidate & Review", "manual", "supervisor", "review"),
        (4, "Issue Executive Direction", "manual", "mda_admin", "direct"),
        (5, "Monitor & Follow-up", "manual", "officer", "follow_up"),
        (6, "Close & Reference", "manual", "registrar", "close")
    ]
    for seq, name, stype, role, act in steps3:
        WorkflowStep.objects.create(service_config=svc3, sequence=seq, step_name=name, step_type=stype, role=role, action=act)

    # 4. NATIONAL GOV COORDINATION
    mda_ngc = MDA.objects.get(id=53)
    dom_inter, _ = ServiceDomain.objects.get_or_create(name="Inter-MDA Coordination & Reporting")
    cat_inter, _ = ServiceCategory.objects.get_or_create(name="Reporting", domain=dom_inter)
    
    wf4_config = {
        "service_name": "National Coordination & Reporting",
        "service_code": "NGC-COORD-001",
        "category": cat_inter,
        "mda": mda_ngc,
        "description": "L2 Inter-MDA tasking and reporting coordination.",
        "config": {"environment": "POC", "mapping_level": "L2"}
    }
    svc4, _ = ServiceConfig.objects.get_or_create(service_code=wf4_config["service_code"], defaults=wf4_config)
    svc4.workflow_steps.all().delete()
    steps4 = [
        (1, "Coordination Trigger", "manual", "supervisor", "trigger"),
        (2, "Issue Tasking", "manual", "supervisor", "task"),
        (3, "Collect & Consolidate", "manual", "officer", "collect"),
        (4, "Review & Escalate", "manual", "supervisor", "review"),
        (5, "Report & Feedback", "manual", "mda_admin", "report"),
        (6, "Close & Retain", "manual", "registrar", "archive")
    ]
    for seq, name, stype, role, act in steps4:
        WorkflowStep.objects.create(service_config=svc4, sequence=seq, step_name=name, step_type=stype, role=role, action=act)

    # 5. CULTURE, ARTS & HERITAGE
    mda_culture = MDA.objects.get(id=25)
    dom_culture, _ = ServiceDomain.objects.get_or_create(name="Culture, Arts & Heritage")
    cat_culture_reg, _ = ServiceCategory.objects.get_or_create(name="Practitioner Registration", domain=dom_culture)
    cat_ushanga, _ = ServiceCategory.objects.get_or_create(name="Ushanga Kenya Initiative", domain=dom_culture)
    
    # 5.1 Registration
    wf5_config = {
        "service_name": "Cultural Practitioner Registration",
        "service_code": "CUL-REG-001",
        "category": cat_culture_reg,
        "mda": mda_culture,
        "description": "L2 process for registering cultural practitioners.",
        "config": {"environment": "POC", "mapping_level": "L2"}
    }
    svc5, _ = ServiceConfig.objects.get_or_create(service_code=wf5_config["service_code"], defaults=wf5_config)
    svc5.workflow_steps.all().delete()
    steps5 = [
        (1, "Application Submission", "manual", "citizen", "apply"),
        (2, "Verification", "manual", "officer", "verify"),
        (3, "Approval", "manual", "supervisor", "approve"),
        (4, "Certificate Generation", "api_call", "system_admin", "generate_cert"),
        (5, "Certificate Dispatch", "manual", "registrar", "dispatch")
    ]
    for seq, name, stype, role, act in steps5:
        WorkflowStep.objects.create(service_config=svc5, sequence=seq, step_name=name, step_type=stype, role=role, action=act)
        
    # 5.2 USHANGA
    wf6_config = {
        "service_name": "UKI Product Purchase Facilitation",
        "service_code": "CUL-UKI-001",
        "category": cat_ushanga,
        "mda": mda_culture,
        "description": "L2 process for Ushanga Kenya Initiative product purchase and sales.",
        "config": {"environment": "POC", "mapping_level": "L2"}
    }
    svc6, _ = ServiceConfig.objects.get_or_create(service_code=wf6_config["service_code"], defaults=wf6_config)
    svc6.workflow_steps.all().delete()
    steps6 = [
        (1, "Receive Products", "manual", "officer", "receive"),
        (2, "Prepare & Check", "manual", "officer", "check"),
        (3, "Place on Market", "manual", "supervisor", "list"),
        (4, "Execute Sale", "manual", "officer", "sell"),
        (5, "Pay Seller", "api_call", "system_admin", "pay")
    ]
    for seq, name, stype, role, act in steps6:
        WorkflowStep.objects.create(service_config=svc6, sequence=seq, step_name=name, step_type=stype, role=role, action=act)

    print(f"All workflows configured for MDAs 19, 52, 53, 25 and COS-HPS.")

    # DEPRECATED: User requested clean slate without sample applications.
    """
    # Generate test data
    citizen = User.objects.filter(role='citizen').first()
    if not citizen:
        citizen_role = Role.objects.get(name='citizen')
        citizen = User.objects.create_user(username='gen_tester', password='Starten1@', email='gen@test.com', role='citizen', user_role=citizen_role)

    all_svcs = [svc1, svc2, svc3, svc4, svc5, svc6]
    for svc in all_svcs:
        for i in range(5):
            ServiceRequest.objects.create(
                request_id=f"{svc.service_code}-{1000+i}",
                service_config=svc,
                citizen=citizen,
                status='received' if i % 2 == 0 else 'in_progress',
                current_step=svc.workflow_steps.first() if i % 2 == 0 else svc.workflow_steps.get(sequence=2),
                payload={"sample_data": f"Workflow test {i}", "notes": "Automated POC Seed"}
            )
    
    print("Sample test data generated for all new workflows.")
    """
    print("✅ Sample test data generation skipped.")


if __name__ == "__main__":
    configure_workflows()
