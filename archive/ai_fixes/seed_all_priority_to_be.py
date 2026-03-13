import os
import re
import django
import glob

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep

print("=== SEEDING TO-BE & AS-IS EXPLICIT WORKFLOWS FROM MARKDOWN ===")

md_dir = "/Users/mac/ictapoc/mdas/docs_final/priority_mdas"
files = glob.glob(os.path.join(md_dir, "*.md"))

updated_services = 0
not_found_services = []

def parse_table(content, header_search):
    lines = content.split('\n')
    table_lines = []
    in_table = False
    for i, line in enumerate(lines):
        if header_search in line and '|' in line:
            in_table = True
            continue
        if in_table:
            if re.match(r'^\|[-\s\|]+\|$', line.strip()):
                continue # Skip separator
            if not line.strip().startswith('|'):
                break # End of table
            # Parse row
            cols = [col.strip() for col in line.strip('|').split('|')]
            if len(cols) >= 3:
                table_lines.append(cols)
    return table_lines

for filepath in files:
    filename = os.path.basename(filepath)
    if "Priority_MDAs" in filename or "temp_" in filename:
        continue
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Extract Service Name and MDA Name
    process_match = re.search(r'\-\s*\*\*Process Name:\*\*\s*(.*)', content, re.IGNORECASE)
    mda_match = re.search(r'\-\s*\*\*Ministry/Department/Agency \(MDA\):\*\*\s*(.*)', content, re.IGNORECASE)
    
    if not process_match:
        continue
        
    process_name = process_match.group(1).strip()
    mda_name = mda_match.group(1).strip() if mda_match else ""
    
    # Try to find the ServiceConfig
    # Sometimes process name has extra text or diff casing
    service = ServiceConfig.objects.filter(service_name__iexact=process_name).first()
    
    if not service:
        # Try finding by looking for a partial match
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
        not_found_services.append((filename, process_name))
        continue
        
    # We found the service! Now extract the tables
    as_is_table = parse_table(content, "| Step | Role | Action | Tool")
    if not as_is_table:
         as_is_table = parse_table(content, "| Step | Actor | Action | System |")
         
    to_be_table = parse_table(content, "| Step | Actor | Action | System |")
    if not to_be_table:
         to_be_table = parse_table(content, "| Step | Role | Action | Tool")
         
    if not to_be_table and not as_is_table:
        print(f"[!] No tables found in {filename} for {service.service_name}")
        continue
        
    print(f"\n📋 Updating: {service.service_name} (MDA: {service.mda.name})")
    
    # Delete existing workflow steps
    WorkflowStep.objects.filter(service_config=service).delete()
    
    # Determine step mapping
    def get_role_and_type(actor, action):
        actor_l = actor.lower()
        action_l = action.lower()
        if "system" in actor_l or "engine" in actor_l or "automated" in action_l or "auto" in action_l:
            return "system", "api", "service_task"
        if "citizen" in actor_l or "applicant" in actor_l or "farmer" in actor_l or "user" in actor_l:
            return "citizen", "api" if "digital" in action_l or "online" in action_l or "portal" in action_l else "manual", "user_task"
        if "director" in actor_l or "supervisor" in actor_l or "committee" in actor_l:
             return "supervisor", "manual", "user_task"
        return "officer", "manual", "user_task"
        
    # Insert AS-IS
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
            step_type="manual", # As-is mostly manual
            bpmn_element_type=c_bpmn,
            lifecycle_stage="as_is",
            sequence=i + 1
        )
        count_as += 1
        
    print(f"  ✓ Added {count_as} As-Is steps")
        
    # Insert TO-BE
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
print(f"Updated services: {updated_services}")
if not_found_services:
    print(f"\nServices not found for these files:")
    for fn, proc in not_found_services:
        print(f"  - {fn} ({proc})")
