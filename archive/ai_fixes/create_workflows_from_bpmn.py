import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep

# Mapping of BPMN file keywords to actual MDA codes in database
MDA_KEYWORDS = {
    "athi water": "AWWDA",
    "agriculture": "AFA",
    "children": "DCS",
    "education": "MOE",
    "health": "MOH",
    "immigration": "DIS",
    "science research": "SDSRI",
    "sports": "SDS",
    "youth": "SDYA",
    "refugee": "SDRS",
    "energy": "SDE",
    "msme": "SDMSME",
    "culture": "SDCAH",
    "cabinet": "SDCA",
    "civil registration": "SDCRS",
}

def extract_steps_from_mermaid(content):
    """Extract workflow steps from mermaid flowchart"""
    steps = []
    
    # Find mermaid blocks
    mermaid_blocks = re.findall(r'```mermaid\n(.*?)```', content, re.DOTALL)
    
    if not mermaid_blocks:
        return steps
    
    # Use the first mermaid block (usually the main process)
    flowchart = mermaid_blocks[0]
    
    # Extract nodes from flowchart
    # Pattern: NodeID[Node Label] or NodeID((Node Label)) or NodeID{Node Label}
    nodes = re.findall(r'(\w+)[\[\(\{]([^\]\)\}]+)[\]\)\}]', flowchart)
    
    seq = 1
    for node_id, node_label in nodes:
        node_label = node_label.strip()
        
        # Skip empty labels
        if not node_label or len(node_label) < 3:
            continue
        
        # Determine BPMN element type based on syntax
        if '((' in flowchart and f'{node_id}((' in flowchart:
            if 'start' in node_label.lower() or seq == 1:
                bpmn_type = 'start_event'
            else:
                bpmn_type = 'end_event'
        elif '{' in flowchart and f'{node_id}{{' in flowchart:
            bpmn_type = 'exclusive_gateway'
        else:
            # Determine if it's a user task or service task
            if any(word in node_label.lower() for word in ['system', 'automated', 'auto', 'api']):
                bpmn_type = 'service_task'
            else:
                bpmn_type = 'user_task'
        
        # Determine role
        if any(word in node_label.lower() for word in ['committee', 'review', 'approval', 'approve']):
            role = 'supervisor'
        elif any(word in node_label.lower() for word in ['applicant', 'citizen', 'submit']):
            role = 'citizen'
        elif any(word in node_label.lower() for word in ['system', 'automated', 'generate', 'update']):
            role = 'system'
        elif any(word in node_label.lower() for word in ['engineer', 'technical', 'assess']):
            role = 'engineer'
        else:
            role = 'officer'
        
        # Determine step type
        if bpmn_type == 'service_task' or role == 'system':
            step_type = 'api_call'
        else:
            step_type = 'manual'
        
        steps.append({
            'name': node_label,
            'description': f'{node_label} - extracted from BPMN',
            'sequence': seq,
            'bpmn_type': bpmn_type,
            'role': role,
            'step_type': step_type
        })
        seq += 1
    
    return steps

def create_to_be_workflow(service_name):
    """Generate optimized To-Be workflow"""
    to_be_steps = []
    
    # Generic digital transformation workflow
    workflows = [
        {'name': 'Online Application', 'role': 'citizen', 'bpmn': 'start_event', 'type': 'api_call'},
        {'name': 'Automated Validation', 'role': 'system', 'bpmn': 'service_task', 'type': 'api_call'},
        {'name': 'Officer Review', 'role': 'officer', 'bpmn': 'user_task', 'type': 'api_call'},
        {'name': 'Digital Approval', 'role': 'supervisor', 'bpmn': 'exclusive_gateway', 'type': 'api_call'},
        {'name': 'Automated Notification', 'role': 'system', 'bpmn': 'service_task', 'type': 'api_call'},
        {'name': 'Process Complete', 'role': 'system', 'bpmn': 'end_event', 'type': 'api_call'},
    ]
    
    for seq, step in enumerate(workflows, 1):
        to_be_steps.append({
            'name': step['name'],
            'description': f'Digital {service_name} - {step["name"]}',
            'sequence': seq,
            'bpmn_type': step['bpmn'],
            'role': step['role'],
            'step_type': step['type']
        })
    
    return to_be_steps

print("=" * 80)
print("CREATING WORKFLOWS FROM BPMN FILES")
print("=" * 80)

bpmn_dir = '/app/as-is-bpmn'
updated_count = 0
skipped_count = 0

for filename in os.listdir(bpmn_dir):
    if not filename.endswith('.md'):
        continue
    
    # Read file
    filepath = os.path.join(bpmn_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find MDA by matching keywords
    filename_lower = filename.lower()
    mda_code = None
    
    for keyword, code in MDA_KEYWORDS.items():
        if keyword in filename_lower:
            mda_code = code
            break
    
    if not mda_code:
        print(f"\n⚠️  Skipping {filename}: No MDA keyword match")
        skipped_count += 1
        continue
    
    # Find MDA in database
    mda = MDA.objects.filter(code=mda_code).first()
    if not mda:
        print(f"\n⚠️  Skipping {filename}: MDA {mda_code} not found in database")
        skipped_count += 1
        continue
    
    # Extract steps from mermaid
    as_is_steps = extract_steps_from_mermaid(content)
    
    if not as_is_steps or len(as_is_steps) < 3:
        print(f"\n⚠️  Skipping {filename}: Insufficient steps found ({len(as_is_steps)})")
        skipped_count += 1
        continue
    
    # Find first service for this MDA
    service = ServiceConfig.objects.filter(mda=mda).first()
    
    if not service:
        print(f"\n⚠️  Skipping {filename}: No services found for {mda.name}")
        skipped_count += 1
        continue
    
    print(f"\n📋 Updating: {service.service_name} ({mda.code})")
    print(f"   MDA: {mda.name}")
    
    # Delete existing workflows
    deleted = WorkflowStep.objects.filter(service_config=service).delete()[0]
    if deleted > 0:
        print(f"   Deleted {deleted} existing workflow steps")
    
    # Create As-Is workflow
    for step_data in as_is_steps:
        WorkflowStep.objects.create(
            service_config=service,
            step_name=step_data['name'],
            role=step_data['role'],
            step_type=step_data['step_type'],
            bpmn_element_type=step_data['bpmn_type'],
            lifecycle_stage='as_is',
            sequence=step_data['sequence']
        )
    
    print(f"   ✓ Added {len(as_is_steps)} As-Is steps")
    
    # Generate To-Be workflow
    to_be_steps = create_to_be_workflow(service.service_name)
    
    # Create To-Be workflow
    for step_data in to_be_steps:
        WorkflowStep.objects.create(
            service_config=service,
            step_name=step_data['name'],
            role=step_data['role'],
            step_type=step_data['step_type'],
            bpmn_element_type=step_data['bpmn_type'],
            lifecycle_stage='to_be',
            sequence=step_data['sequence']
        )
    
    print(f"   ✓ Added {len(to_be_steps)} To-Be steps")
    updated_count += 1

print(f"\n{'=' * 80}")
print(f"SUMMARY:")
print(f"  Updated: {updated_count} services")
print(f"  Skipped: {skipped_count} files")
print(f"{'=' * 80}")
