import os
import csv
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig, MDA, ServiceCategory, ServiceDomain, WorkflowStep

def seed_full_catalogue():
    print("--- SEEDING FULL CATALOGUE FROM CSV ---")
    csv_path = "/Users/mac/ictapoc/Government_Services_List.csv"
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count_added = 0
        
        for row in reader:
            mda_name = row.get('MDA Name', 'Unknown MDA').strip()
            service_name = row.get('Service Name', '').strip()
            maturity_str = row.get('Digital Maturity', '1').strip()
            bottlenecks = row.get('Key Bottlenecks', '').strip()
            
            if not service_name: continue
            
            # 1. Handle MDA
            mda_obj, _ = MDA.objects.get_or_create(name=mda_name)
            
            # 2. Extract Maturity Level (Int)
            maturity = 1
            try:
                maturity = int(maturity_str[0]) 
            except:
                pass
                
            # 3. Handle Code
            mda_initials = "".join([w[0] for w in mda_name.split() if w[0].isalnum()])[:5]
            svc_code = f"{mda_initials}_{service_name.upper().replace(' ', '_')}"[:40].strip('_')
            
            # 4. Create Service if not exists
            if ServiceConfig.objects.filter(service_name=service_name).exists():
                continue
                
            base_code = svc_code
            counter = 1
            while ServiceConfig.objects.filter(service_code=svc_code).exists():
                svc_code = f"{base_code[:35]}_{counter}"
                counter += 1

            svc_obj = ServiceConfig.objects.create(
                service_name=service_name,
                service_code=svc_code,
                mda=mda_obj,
                digitization_level=maturity,
                description=f"Authoritative service for {service_name}.",
                pain_points=[bottlenecks] if bottlenecks and bottlenecks != 'N/A' else [],
                catalogue_visible=True,
                service_status='active'
            )
            
            count_added += 1
            # Seed a default workflow so it doesn't show as "Missing"
            # As-Is (Basic)
            WorkflowStep.objects.create(
                service_config=svc_obj,
                step_name="Manual Intake & Form Submission",
                lifecycle_stage="as_is",
                sequence=1,
                role="citizen",
                bpmn_element_type="user_task"
            )
            WorkflowStep.objects.create(
                service_config=svc_obj,
                step_name="Officer Verification & Internal Routing",
                lifecycle_stage="as_is",
                sequence=2,
                role="officer",
                bpmn_element_type="user_task"
            )
            WorkflowStep.objects.create(
                service_config=svc_obj,
                step_name="Manual Decision & Issuance",
                lifecycle_stage="as_is",
                sequence=3,
                role="officer",
                bpmn_element_type="user_task"
            )
            
            # To-Be (Digital First)
            WorkflowStep.objects.create(
                service_config=svc_obj,
                step_name="Digital Application (e-Citizen SSO)",
                lifecycle_stage="to_be",
                sequence=1,
                role="citizen",
                bpmn_element_type="user_task"
            )
            WorkflowStep.objects.create(
                service_config=svc_obj,
                step_name="Automated Registry Validation",
                lifecycle_stage="to_be",
                sequence=2,
                role="system",
                step_type="api_call",
                bpmn_element_type="service_task"
            )
            WorkflowStep.objects.create(
                service_config=svc_obj,
                step_name="Digital Approval & Issuance to Wallet",
                lifecycle_stage="to_be",
                sequence=3,
                role="system",
                step_type="api_call",
                bpmn_element_type="service_task"
            )

    print(f"Added {count_added} new services from CSV.")
    print("--- DONE ---")

if __name__ == '__main__':
    seed_full_catalogue()
