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
    print("🚀 JSON-DRIVEN WOG SEEDER v2 (Lifecycle Optimization)")
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
        mda_name = mda_name_raw.replace('·', '').replace('\xa0', ' ').strip()
        
        if not mda_name: continue

        # Find or Create MDA
        mda = MDA.objects.filter(name=mda_name).first()
        if not mda:
            base_code = ''.join(c for c in mda_name[:10].upper() if c.isalnum())
            unique_code = f"MDA-{base_code}-{random.randint(100, 999)}"
            mda = MDA.objects.create(name=mda_name, code=unique_code)
        
        # Desktop Review
        DesktopReview.objects.update_or_create(
            mda=mda,
            process_id=proc.get('process_id', ''),
            defaults={
                "executive_summary": proc.get('executive_summary'),
                "process_overview": proc.get('process_overview'),
                # ... other fields ...
            }
        )

        # Service Category
        process_name_raw = proc.get('cover_page', {}).get('process_name') or mda_name
        process_name = process_name_raw.replace('·', '').replace('\xa0', ' ').strip()
        
        category, _ = ServiceCategory.objects.get_or_create(
            name=process_name,
            domain=domain,
            defaults={"description": proc.get('executive_summary')}
        )

        # ---------------------------------------------------------------------
        # 🚀 LIFECYCLE OVERRIDES (The "To-Be" Optimization)
        # ---------------------------------------------------------------------
        
        service_code = proc.get('process_id') or f"WOG-{mda.id}-{random.randint(1000, 9999)}"
        form_schema = {}
        workflow_steps = []
        is_lifecycle_service = False

        # 1. BIRTH REGISTRATION (Civil Registration Services)
        if "Civil Registration" in mda_name or "Birth" in process_name:
            print(f"  👶 Configuring Optimized Birth Registration for {mda_name}")
            is_lifecycle_service = True
            service_code = "CRS-BIRTH-001"
            form_schema = {
                "type": "object",
                "required": ["child_name", "date_of_birth", "gender", "hospital_notification"],
                "properties": {
                    "child_name": {"type": "string", "title": "Child's Full Name"},
                    "date_of_birth": {"type": "string", "format": "date", "title": "Date of Birth"},
                    "gender": {"type": "string", "enum": ["Male", "Female"], "title": "Gender"},
                    "hospital_notification": {"type": "string", "title": "Notification No.", "description": "From Hospital (D1)"},
                    "mother_id": {"type": "string", "title": "Mother's ID", "readOnly": True, "default": "PREFILLED"},
                    "father_id": {"type": "string", "title": "Father's ID (Optional)"}
                }
            }
            workflow_steps = [
                {"name": "Verify Hospital Notification", "type": "api_call", "role": "System", "action": "VERIFY_HOSPITAL"},
                {"name": "Verify Parent Identities", "type": "api_call", "role": "System", "action": "VERIFY_IPRS"},
                {"name": "Registrar Approval", "type": "manual", "role": "Registrar", "action": "APPROVE"},
                {"name": "Generate Birth Certificate", "type": "api_call", "role": "System", "action": "GENERATE_CERT"}
            ]

        # 2. NATIONAL ID (IPRS / NRB)
        elif "National Registration" in mda_name or "National Identity" in process_name:
            print(f"  🆔 Configuring Optimized ID Application for {mda_name}")
            is_lifecycle_service = True
            service_code = "IPRS-ID-001"
            form_schema = {
                "type": "object",
                "required": ["birth_certificate_number", "polling_station"],
                "properties": {
                    "birth_certificate_number": {"type": "string", "title": "Birth Certificate No."},
                    "applicant_photo": {"type": "string", "format": "data-url", "title": "Passport Photo"},
                    "polling_station": {"type": "string", "title": "Preferred Collection Centre"}
                }
            }
            workflow_steps = [
                {"name": "Verify Birth Certificate", "type": "api_call", "role": "System", "action": "VERIFY_CRS"},
                {"name": "Biometric Capture", "type": "manual", "role": "Officer", "action": "CAPTURE_BIOMETRICS"},
                {"name": "Vetting & Approval", "type": "manual", "role": "Supervisor", "action": "APPROVE"},
                {"name": "Print & Dispatch ID", "type": "api_call", "role": "System", "action": "ISSUE_ID"}
            ]

        # 3. KRA PIN (Revenue Authority)
        elif "Revenue" in mda_name or "Tax" in process_name:
            print(f"  💰 Configuring Optimized KRA PIN for {mda_name}")
            is_lifecycle_service = True
            service_code = "KRA-PIN-001"
            form_schema = {
                "type": "object",
                "required": ["national_id_number", "pin_type"],
                "properties": {
                    "national_id_number": {"type": "string", "title": "National ID Number"},
                    "pin_type": {"type": "string", "enum": ["Individual", "Company"], "default": "Individual"},
                    "email": {"type": "string", "format": "email", "title": "Email Address"}
                }
            }
            workflow_steps = [
                {"name": "Verify National ID", "type": "api_call", "role": "System", "action": "VERIFY_IPRS"},
                {"name": "Generate PIN", "type": "api_call", "role": "System", "action": "GENERATE_PIN"},
                {"name": "Email PIN Certificate", "type": "api_call", "role": "System", "action": "SEND_EMAIL"}
            ]

        # Default Fallback
        if not is_lifecycle_service:
            form_schema = {
                "type": "object",
                "required": ["application_details"],
                "properties": {
                    "full_name": {"type": "string", "title": "Full Name"},
                    "id_number": {"type": "string", "title": "ID Number"},
                    "application_details": {"type": "string", "title": "Details", "format": "textarea"}
                }
            }

        # Save Service
        service, _ = ServiceConfig.objects.update_or_create(
            service_name=process_name,
            mda=mda,
            defaults={
                "service_code": service_code,
                "description": proc.get('executive_summary'),
                "category": category,
                "digitization_level": 5 if is_lifecycle_service else 4,
                "service_type": "G2C",
                "catalogue_visible": True,
                "form_schema": form_schema
            }
        )

        # Seed Workflow Steps
        WorkflowStep.objects.filter(service_config=service).delete()
        
        # Use Optimized Steps if Lifecycle, else use JSON data
        steps_to_seed = workflow_steps if is_lifecycle_service else proc.get('to_be_process', {}).get('steps', [])
        
        for i, step_data in enumerate(steps_to_seed):
            # Normalize dict keys (JSON uses 'actor', our custom list uses 'role')
            role = step_data.get('role') or step_data.get('actor', 'Officer')
            name = step_data.get('name') or step_data.get('description', f'Step {i+1}')
            type_ = step_data.get('type') or ('api_call' if 'System' in role else 'manual')
            
            WorkflowStep.objects.create(
                service_config=service,
                step_name=name,
                step_type=type_,
                bpmn_element_type='service_task' if type_ == 'api_call' else 'user_task',
                lifecycle_stage='to_be',
                role=role,
                sequence=i + 1,
                action=step_data.get('action', 'REVIEW')
            )

    print("\n✅ Lifecycle Seeding Complete.")

if __name__ == "__main__":
    run_json_seed()
