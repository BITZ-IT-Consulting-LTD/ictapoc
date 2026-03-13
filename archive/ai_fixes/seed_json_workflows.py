import os
import django
import json
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep, ServiceCategory, ServiceDomain

print("=== SEEDING TO-BE & AS-IS EXPLICIT WORKFLOWS FROM JSON ===")

with open("/app/priority_workflows.json", "r", encoding="utf-8") as f:
    data = json.load(f)

updated_services = 0
not_found_services = []
created_services = 0

registry_domain, _ = ServiceDomain.objects.get_or_create(name="Public Service & Administration")
general_cat, _ = ServiceCategory.objects.get_or_create(name="General Priority Services", domain=registry_domain)

def get_role_and_type(actor, action):
    actor_l = actor.lower()
    action_l = action.lower()
    if "system" in actor_l or "engine" in actor_l or "automated" in action_l or "auto" in action_l or "kesel" in actor_l:
        return "system", "api", "service_task"
    if "citizen" in actor_l or "applicant" in actor_l or "farmer" in actor_l or "user" in actor_l or "customer" in actor_l:
        return "citizen", "api" if "digital" in action_l or "online" in action_l or "portal" in action_l or "app" in action_l else "manual", "user_task"
    if "director" in actor_l or "supervisor" in actor_l or "committee" in actor_l or "head" in actor_l:
         return "supervisor", "manual", "user_task"
    return "officer", "manual", "user_task"

for item in data:
    filename = item["filename"]
    process_name = item["process_name"]
    mda_name = item["mda_name"]
    as_is_table = item["as_is"]
    to_be_table = item["to_be"]
    
    # Try finding exact process name matching
    service = ServiceConfig.objects.filter(service_name__iexact=process_name).first()
    
    if not service:
        service = ServiceConfig.objects.filter(service_name__icontains=process_name).first()
        if not service and mda_name:
             # Just try to grab any service under that MDA mapping as fallback if needed
             mda = MDA.objects.filter(name__icontains=mda_name).first()
             if not mda:
                  mda_short = filename.replace("___Service_Delivery.md", "").replace("_", " ")
                  mda = MDA.objects.filter(name__icontains=mda_short[:10]).first()
             if mda:
                 service = ServiceConfig.objects.filter(mda=mda).first()

    if not service:
        # Create it if it doesn't exist, linked to a generic MDA or the closest MDA match
        mda = MDA.objects.filter(name__icontains=mda_name).first()
        if not mda:
             mda_short = filename.replace("___Service_Delivery.md", "").replace("_", " ")
             mda = MDA.objects.filter(name__icontains=mda_short[:10]).first()
             
        if not mda:
             # Create the MDA as well
             type_val = "State Department" if "State Department" in mda_name else "Agency"
             flags = {
                 "EDRMS": "NOT CONFIGURED",
                 "type": type_val,
                 "sector": "Public Sector",
                 "seeded_for": "POC"
             }
             code_str = "".join([w[0] for w in mda_name.split() if w[0].isalnum()])[:5]
             mda = MDA.objects.create(
                 name=mda_name,
                 code=f"SD-{code_str}" if type_val == "State Department" else code_str,
                 description=json.dumps(flags)
             )
             
        service = ServiceConfig.objects.create(
             mda=mda,
             service_name=process_name,
             service_code=f"SRV-{uuid.uuid4().hex[:6].upper()}",
             description="Priority Service Seeded from Markdown doc: " + filename,
             category=general_cat
        )
        created_services += 1
        
    print(f"\n📋 Updating: {service.service_name} (MDA: {service.mda.name})")
    
    WorkflowStep.objects.filter(service_config=service).delete()
    
    count_as = 0
    for i, row in enumerate(as_is_table):
        if len(row) < 3: continue
        actor = row[1]
        action = row[2]
        
        c_role, c_type, c_bpmn = get_role_and_type(actor, action)
        if i == 0: c_bpmn = "start_event"
        if i == len(as_is_table) - 1: c_bpmn = "end_event"
        
        step_name = f"{actor}: {action}"[:250]
        
        WorkflowStep.objects.create(
            service_config=service,
            step_name=step_name,
            role=c_role,
            step_type="manual",
            bpmn_element_type=c_bpmn,
            lifecycle_stage="as_is",
            sequence=i + 1
        )
        count_as += 1
        
    print(f"  ✓ Added {count_as} As-Is steps")
        
    count_to = 0
    for i, row in enumerate(to_be_table):
        if len(row) < 3: continue
        actor = row[1]
        action = row[2]
        
        c_role, c_type, c_bpmn = get_role_and_type(actor, action)
        
        if i == 0: c_bpmn = "start_event"
        if i == len(to_be_table) - 1: c_bpmn = "end_event"
        
        step_name = f"{actor}: {action}"[:250]
        
        WorkflowStep.objects.create(
            service_config=service,
            step_name=step_name,
            role=c_role,
            step_type=c_type,
            bpmn_element_type=c_bpmn,
            lifecycle_stage="to_be",
            sequence=i + 1
        )
        count_to += 1
        
    print(f"  ✓ Added {count_to} To-Be steps")
    updated_services += 1

print(f"\n=== SUMMARY ===")
print(f"Created missing services: {created_services}")
print(f"Updated services with workflows: {updated_services}")
