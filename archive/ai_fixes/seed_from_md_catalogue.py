import os
import re
import django

# Set up Django environment targeting Docker DB
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.host_settings')
django.setup()

from service_api.models import ServiceConfig, MDA, ServiceCategory, ServiceDomain, WorkflowStep

def parse_catalogue_md():
    print("--- PARSING GOVERNMENT SERVICE CATALOGUE MD ---")
    path = "/Users/mac/ictapoc/Government_Service_Catalogue.md"
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by MDA (##)
    mda_sections = re.split(r'\n##\s+', content)
    
    count_mda = 0
    count_svc = 0
    
    # Common Domain for Generic Services
    general_domain, _ = ServiceDomain.objects.get_or_create(name="Public Service & Administration")

    for section in mda_sections[1:]: # Skip the intro
        lines = section.strip().split('\n')
        if not lines: continue
        
        mda_name = lines[0].strip()
        mda_obj, _ = MDA.objects.get_or_create(name=mda_name)
        count_mda += 1
        
        # Split by Service (###)
        svc_sections = re.split(r'\n###\s+', section)
        
        for svc_section in svc_sections[1:]:
            svc_lines = svc_section.strip().split('\n')
            if not svc_lines: continue
            
            svc_name = svc_lines[0].strip()
            
            # Check if this service name exists in the 21 seeded ones
            if ServiceConfig.objects.filter(service_name__icontains=svc_name).exists():
                print(f"  [Skip] {svc_name} (Already exists)")
                continue

            # Extract details
            details = {}
            for line in svc_lines[1:]:
                match = re.search(r'-\s*\*\*(.*?)\*\*:\s*(.*)', line)
                if match:
                    details[match.group(1).strip()] = match.group(2).strip()

            # Map maturity
            maturity_str = details.get('Digital Maturity', '1')
            maturity = 1
            try:
                maturity = int(maturity_str.split('-')[0].strip())
            except:
                pass

            # Create Service
            mda_initials = "".join([w[0] for w in mda_name.split() if w[0].isalnum()])[:5]
            svc_code = f"{mda_initials}_{svc_name.upper().replace(' ', '_')}"[:40].strip('_')
            
            # Handle duplicates in code
            base_code = svc_code
            counter = 1
            while ServiceConfig.objects.filter(service_code=svc_code).exists():
                svc_code = f"{base_code[:35]}_{counter}"
                counter += 1

            # Default Category based on MDA if not specified
            cat_obj, _ = ServiceCategory.objects.get_or_create(name="General Services", domain=general_domain)

            svc_obj = ServiceConfig.objects.create(
                service_name=svc_name,
                service_code=svc_code,
                mda=mda_obj,
                category=cat_obj,
                description=details.get('Description', f"Authoritative service for {svc_name}"),
                digitization_level=maturity,
                service_type=details.get('Service Type'),
                delivery_channels=details.get('Delivery Channels', '').split(),
                pain_points=details.get('Pain Points', '').split('  '),
                process_complexity=details.get('Process Complexity'),
                catalogue_visible=True,
                service_status='active'
            )
            
            # Seed default 3-step workflow for the matrix view
            # As-Is
            WorkflowStep.objects.create(
                service_config=svc_obj,
                step_name="Form Intake",
                lifecycle_stage="as_is",
                sequence=1,
                role="officer",
                bpmn_element_type="user_task"
            )
            WorkflowStep.objects.create(
                service_config=svc_obj,
                step_name="Manual Verification",
                lifecycle_stage="as_is",
                sequence=2,
                role="officer",
                bpmn_element_type="user_task"
            )
            WorkflowStep.objects.create(
                service_config=svc_obj,
                step_name="Output Generation",
                lifecycle_stage="as_is",
                sequence=3,
                role="officer",
                bpmn_element_type="user_task"
            )
            
            # To-Be
            WorkflowStep.objects.create(
                service_config=svc_obj,
                step_name="Digital Application",
                lifecycle_stage="to_be",
                sequence=1,
                role="citizen",
                bpmn_element_type="user_task"
            )
            WorkflowStep.objects.create(
                service_config=svc_obj,
                step_name="Automated Registry Check",
                lifecycle_stage="to_be",
                sequence=2,
                role="system",
                step_type="api_call",
                bpmn_element_type="service_task"
            )
            WorkflowStep.objects.create(
                service_config=svc_obj,
                step_name="Digital Issuance",
                lifecycle_stage="to_be",
                sequence=3,
                role="system",
                step_type="api_call",
                bpmn_element_type="service_task"
            )

            count_svc += 1
            print(f"  [Seeded] {svc_name} (MDA: {mda_name})")

    print(f"--- COMPLETE: Seeded {count_svc} new services across {count_mda} MDAs ---")

if __name__ == '__main__':
    parse_catalogue_md()
