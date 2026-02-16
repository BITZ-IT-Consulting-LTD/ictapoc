import os
import django
import json
import random

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig, MDA, ServiceCategory, ServiceDomain, WorkflowStep, DesktopReview

def run_json_seed():
    print("=" * 80)
    print("🚀 JSON-DRIVEN WOG SEEDER v1 (Desktop Reviews + To-Be BPMN)")
    print("=" * 80)

    json_path = os.path.join(os.path.dirname(__file__), 'combined_data.json')
    if not os.path.exists(json_path):
        print(f"❌ JSON file not found at {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        master_data = json.load(f)

    processes = master_data.get('processes', [])
    print(f"📦 Found {len(processes)} processes in JSON.")

    # 1. Base Domain for WOG
    domain, _ = ServiceDomain.objects.get_or_create(
        name="Whole of Government",
        defaults={"description": "Integrated government services catalogue"}
    )

    for proc in processes:
        mda_name_raw = proc.get('mda_name', '')
        # Sanitize name: remove bullets, non-breaking spaces, and extra whitespace
        mda_name = mda_name_raw.replace('·', '').replace('\xa0', ' ').strip()
        
        if not mda_name: continue

        print(f"\n🏢 Processing MDA: {mda_name}")

        # Find or Create MDA (Avoid duplication)
        mda = MDA.objects.filter(name=mda_name).first()
        if not mda:
            base_code = ''.join(c for c in mda_name[:10].upper() if c.isalnum())
            unique_code = f"MDA-{base_code}-{random.randint(100, 999)}"
            while MDA.objects.filter(code=unique_code).exists():
                unique_code = f"MDA-{base_code}-{random.randint(1000, 9999)}"
            
            mda = MDA.objects.create(
                name=mda_name,
                code=unique_code
            )
            print(f"  ✅ Created new MDA: {mda.name} ({unique_code})")
        else:
            print(f"  🤝 Using existing MDA: {mda.name}")

        # 2. Create Desktop Review
        DesktopReview.objects.update_or_create(
            mda=mda,
            process_id=proc.get('process_id', ''),
            defaults={
                "executive_summary": proc.get('executive_summary'),
                "process_overview": proc.get('process_overview'),
                "stakeholders": proc.get('stakeholders'),
                "inputs_outputs_dependencies": proc.get('inputs_outputs_dependencies'),
                "process_maturity": proc.get('process_maturity'),
                "as_is_narrative": proc.get('as_is_narrative'),
                "as_is_steps": proc.get('as_is_steps'),
                "pain_points_bottlenecks_risks": proc.get('pain_points_bottlenecks_risks'),
                "to_be_process": proc.get('to_be_process'),
                "digitization_opportunities": proc.get('digitization_opportunities'),
                "metadata": proc.get('metadata')
            }
        )
        print(f"  📝 Saved Desktop Review for {mda.name}")

        # 3. Create Service Category (Business Process)
        process_name_raw = proc.get('cover_page', {}).get('process_name') or mda_name
        process_name = process_name_raw.replace('·', '').replace('\xa0', ' ').strip()
        
        category, _ = ServiceCategory.objects.get_or_create(
            name=process_name,
            domain=domain,
            defaults={"description": proc.get('executive_summary')}
        )

        # 4. Create Service Config
        service_code = proc.get('process_id') or f"WOG-{mda.id}-{random.randint(1000, 9999)}"
        
        # Default Form Schema for G2C Services
        default_form_schema = {
            "type": "object",
            "required": ["full_name", "id_number", "application_details"],
            "properties": {
                "full_name": {"type": "string", "title": "Full Name", "description": "As it appears on your ID"},
                "id_number": {"type": "string", "title": "National ID / Passport Number"},
                "phone_number": {"type": "string", "title": "Phone Number", "format": "tel"},
                "email_address": {"type": "string", "title": "Email Address", "format": "email"},
                "application_details": {"type": "string", "title": "Application Details", "format": "textarea", "description": "Explain the specifics of your request"},
                "declaration": {"type": "boolean", "title": "I declare that the information provided is true.", "const": True}
            }
        }

        service, _ = ServiceConfig.objects.update_or_create(
            service_name=process_name,
            mda=mda,
            defaults={
                "service_code": service_code,
                "description": proc.get('executive_summary'),
                "category": category,
                "digitization_level": 4, # Target level for WOG
                "service_type": "G2C",
                "catalogue_visible": True,
                "form_schema": default_form_schema
            }
        )

        # 5. Seed Workflow Steps (To-Be BPMN)
        WorkflowStep.objects.filter(service_config=service).delete()

        # To-Be Steps
        to_be_steps = proc.get('to_be_process', {}).get('steps', [])
        for i, step_data in enumerate(to_be_steps):
            role = step_data.get('actor', 'Officer')
            bpmn_type = 'user_task'
            if i == 0: bpmn_type = 'start_event'
            elif i == len(to_be_steps) - 1: bpmn_type = 'end_event'
            elif 'System' in step_data.get('actor', ''): bpmn_type = 'service_task'

            WorkflowStep.objects.create(
                service_config=service,
                step_name=step_data.get('description'),
                step_type='api_call' if bpmn_type == 'service_task' else 'manual',
                bpmn_element_type=bpmn_type,
                lifecycle_stage='to_be',
                role=role,
                sequence=i + 1,
                action='AUTOMATED' if bpmn_type == 'service_task' else 'REVIEW'
            )

        # As-Is Steps
        as_is_steps = proc.get('as_is_steps', [])
        for i, step_data in enumerate(as_is_steps):
            WorkflowStep.objects.create(
                service_config=service,
                step_name=step_data.get('description'),
                step_type='manual',
                bpmn_element_type='user_task',
                lifecycle_stage='as_is',
                role=step_data.get('actor', 'Officer'),
                sequence=i + 1
            )
        
        print(f"  ⚙️ Seeded {len(to_be_steps)} To-Be and {len(as_is_steps)} As-Is workflow steps.")

    print("\n✅ JSON Seeding Complete.")

if __name__ == "__main__":
    run_json_seed()
