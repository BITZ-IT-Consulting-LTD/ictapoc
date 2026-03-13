import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep, Role, ServiceDomain, ServiceCategory

print("=== SEEDING ICT PRIORITY MDAS ===")

ict_mdas = [
    {
        "mda_name": "State Department for ICT and the Digital Economy",
        "mda_code": "SD-ICT",
        "type": "State Department",
        "sector": "ICT",
        "service_name": "Digital Government Infrastructure and ICT Policy Coordination",
        "as_is": [
            {"name": "MDA: Identifies need for digital service or ICT project", "role": "citizen", "type": "manual", "bpmn": "start_event", "seq": 1},
            {"name": "State Department ICT: Develops ICT policy, strategy, or framework", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 2},
            {"name": "ICT Authority: Reviews proposed ICT project for standards compliance", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 3},
            {"name": "MDA / Vendor: Procures and develops ICT system", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 4},
            {"name": "MDA: Deploys and operates ICT system", "role": "officer", "type": "manual", "bpmn": "end_event", "seq": 5}
        ],
        "to_be": [
            {"name": "MDA: Designs digital service aligned with GEA", "role": "citizen", "type": "api", "bpmn": "start_event", "seq": 1},
            {"name": "ICT Authority: Validates architecture and integration requirements", "role": "officer", "type": "api", "bpmn": "user_task", "seq": 2},
            {"name": "System: Integrates with authoritative registries via KeSEL / X-Road", "role": "system", "type": "api", "bpmn": "service_task", "seq": 3},
            {"name": "Government Cloud: Hosts the digital service platform", "role": "system", "type": "api", "bpmn": "service_task", "seq": 4},
            {"name": "Citizen: Accesses service digitally via portal or mobile device", "role": "citizen", "type": "api", "bpmn": "end_event", "seq": 5}
        ]
    },
    {
        "mda_name": "ICT Authority",
        "mda_code": "ICTA",
        "type": "Agency",
        "sector": "ICT",
        "service_name": "Government ICT Project Implementation and Digital Infrastructure Management",
        "as_is": [
            {"name": "MDA: Identifies need for ICT system", "role": "citizen", "type": "manual", "bpmn": "start_event", "seq": 1},
            {"name": "MDA: Develops project concept and submits to ICT Authority", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 2},
            {"name": "ICT Authority: Reviews architecture and compliance with standards", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 3},
            {"name": "ICT Authority: Approves or rejects project", "role": "supervisor", "type": "manual", "bpmn": "user_task", "seq": 4},
            {"name": "MDA / Vendor: Procures vendor and develops system", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 5},
            {"name": "MDA: Deploys and operates system", "role": "officer", "type": "manual", "bpmn": "end_event", "seq": 6}
        ],
        "to_be": [
            {"name": "MDA: Designs digital service aligned with GEA", "role": "citizen", "type": "api", "bpmn": "start_event", "seq": 1},
            {"name": "ICT Authority: Reviews architecture and integration", "role": "officer", "type": "api", "bpmn": "user_task", "seq": 2},
            {"name": "System: Integrates with national registries via KeSEL Bridge", "role": "system", "type": "api", "bpmn": "service_task", "seq": 3},
            {"name": "Government Cloud: Hosts digital service platform", "role": "system", "type": "api", "bpmn": "service_task", "seq": 4},
            {"name": "Citizen/Business: Accesses service through digital government portals", "role": "citizen", "type": "api", "bpmn": "end_event", "seq": 5}
        ]
    }
]

# Common Registry Domain/Category
registry_domain, _ = ServiceDomain.objects.get_or_create(name="Government Administration")
registry_cat, _ = ServiceCategory.objects.get_or_create(name="ICT infrastructure & Systems", domain=registry_domain)

for data in ict_mdas:
    mda_name = data["mda_name"]
    mda_code = data["mda_code"]
    service_name = data["service_name"]
    
    # 1. Ensure MDA
    flags = {
        "EDRMS": "NOT CONFIGURED",
        "MIS": "UNKNOWN",
        "Integration": "PENDING",
        "Infrastructure": "NOT VALIDATED",
        "type": data["type"],
        "sector": data["sector"],
        "seeded_for": "POC"
    }

    mda, created_mda = MDA.objects.get_or_create(
        code=mda_code,
        defaults={
            "name": mda_name,
            "description": json.dumps(flags)
        }
    )
    if not created_mda:
        mda.name = mda_name
        mda.save()
        
    print(f"[{mda_code}] MDA Ready. (Created: {created_mda})")
    
    # 2. Add / Find Service config
    service, created_service = ServiceConfig.objects.get_or_create(
        mda=mda,
        service_name=service_name,
        defaults={
            "service_code": f"{mda_code}-SRV-01",
            "description": "Seeded workflow for " + mda_name,
            "category": registry_cat
        }
    )
    print(f"[{mda_code}] Service '{service_name}' Ready. (Created: {created_service})")
    
    # 3. Apply the custom standard workflows!
    WorkflowStep.objects.filter(service_config=service).delete()
    
    for step_data in data["as_is"]:
        WorkflowStep.objects.create(
            service_config=service,
            step_name=step_data["name"],
            role=step_data["role"],
            step_type=step_data["type"],
            bpmn_element_type=step_data["bpmn"],
            lifecycle_stage="as_is",
            sequence=step_data["seq"]
        )
    print(f"[{mda_code}]  ✓ Added {len(data['as_is'])} As-Is steps")
    
    for step_data in data["to_be"]:
        WorkflowStep.objects.create(
            service_config=service,
            step_name=step_data["name"],
            role=step_data["role"],
            step_type=step_data["type"],
            bpmn_element_type=step_data["bpmn"],
            lifecycle_stage="to_be",
            sequence=step_data["seq"]
        )
    print(f"[{mda_code}]  ✓ Added {len(data['to_be'])} To-Be steps")

print("\n=== SUCCESS ===")
