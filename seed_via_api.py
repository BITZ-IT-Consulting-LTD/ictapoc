import requests
import json
import time

base_url = 'http://localhost:5173/api'

def check_and_seed():
    print(f"Connecting to {base_url}...")
    
    # 1. Login
    try:
        auth_resp = requests.post(f"{base_url}/token/", json={'username': 'admin', 'password': 'Starten1@'}, timeout=5)
        if auth_resp.status_code != 200:
            print(f"Login Failed: {auth_resp.status_code} {auth_resp.text}")
            return
            
        token = auth_resp.json()['access']
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        print("Login Successful.")

        # 2. Check/Add MDA (Ministry of Education)
        mdas_resp = requests.get(f"{base_url}/mdas/", headers=headers)
        mdas = mdas_resp.json()
        moe_exists = any(m['code'] == 'MOE' for m in mdas)
        
        moe_id = None
        if not moe_exists:
            print("Creating Ministry of Education...")
            moe_data = {
                "name": "Ministry of Education",
                "code": "MOE",
                "description": "Responsible for national education policy and leadership.",
                "head_of_mda": "Cabinet Secretary",
                "contact_email": "info@education.go.ke",
                "website": "https://www.education.go.ke",
                "address": "Jogoo House, Nairobi"
            }
            create_resp = requests.post(f"{base_url}/mdas/", json=moe_data, headers=headers)
            if create_resp.status_code == 201:
                moe_id = create_resp.json()['id']
                print(f"MOE Created with ID: {moe_id}")
            else:
                print(f"Failed to create MOE: {create_resp.text}")
        else:
            moe = next(m for m in mdas if m['code'] == 'MOE')
            moe_id = moe['id']
            print(f"MOE already exists (ID: {moe_id}).")

        if not moe_id:
            print("Cannot proceed without MOE ID.")
            return

        # 3. Check/Add Service (Scholarships)
        services_resp = requests.get(f"{base_url}/service-configs/", headers=headers)
        services = services_resp.json()
        scholarship_exists = any(s['service_code'] == 'SCHOLARSHIPS' for s in services)
        
        if not scholarship_exists:
            print("Creating Scholarships Service...")
            # Use the config from seed_data.py
            service_data = {
                "service_code": "SCHOLARSHIPS",
                "service_name": "Scholarships & Bursaries Coordination",
                "mda": moe_id,
                "config": {
                    "rules": {
                        "schema": {
                            "type": "object",
                            "title": "Scholarship & Bursary Application",
                            "properties": {
                                 "header_1": {"type": "section_header", "title": "1. Personal Details"},
                                 "full_name": {"type": "string", "title": "Applicant Full Name"},
                                 "id_number": {"type": "string", "title": "ID Number / Birth Cert No"},
                                 "date_of_birth": {"type": "string", "format": "date", "title": "Date of Birth"},
                                 "gender": {"type": "string", "title": "Gender", "enum": ["Male", "Female"], "widget": "radio"},
                                 
                                 "header_2": {"type": "section_header", "title": "2. Education Details"},
                                 "institution": {"type": "string", "title": "Institution Name"},
                                 "admission_number": {"type": "string", "title": "Admission Number"},
                                 "course_of_study": {"type": "string", "title": "Course of Study"},
                                 "year_of_study": {"type": "number", "title": "Year of Study"},
                                 
                                 "header_3": {"type": "section_header", "title": "3. Financial Need Assessment"},
                                 "maternal_status": {"type": "string", "enum": ["Alive", "Deceased", "Unknown"], "title": "Mother's Status", "widget": "radio"},
                                 "paternal_status": {"type": "string", "enum": ["Alive", "Deceased", "Unknown"], "title": "Father's Status", "widget": "radio"},
                                 "financial_need_desc": {"type": "string", "format": "textarea", "title": "Explain Financial Need"},
                                 
                                 "header_4": {"type": "section_header", "title": "4. Supporting Documents"},
                                 "admission_letter": {"type": "string", "format": "data-url", "title": "Admission Letter"},
                                 "fees_structure": {"type": "string", "format": "data-url", "title": "Fee Structure"},
                                 "id_copy": {"type": "string", "format": "data-url", "title": "ID/Birth Cert Copy"}
                            },
                            "required": ["full_name", "id_number", "institution", "financial_need_desc", "admission_letter"]
                        },
                        "workflow": [
                            {"sequence": 1, "step_name": "Application Submission", "step_type": "manual", "role": "citizen", "action": "submit"},
                            {"sequence": 2, "step_name": "Preliminary Screening", "step_type": "manual", "role": "officer", "action": "screen"},
                            {"sequence": 3, "step_name": "Verification & Due Diligence", "step_type": "manual", "role": "officer", "action": "verify"},
                            {"sequence": 4, "step_name": "Evaluation & Scoring", "step_type": "manual", "role": "supervisor", "action": "score"},
                            {"sequence": 5, "step_name": "Approval & Award Decision", "step_type": "manual", "role": "supervisor", "action": "approve"},
                            {"sequence": 6, "step_name": "Funds Disbursement", "step_type": "manual", "role": "officer", "action": "disburse"},
                            {"sequence": 7, "step_name": "Utilization Monitoring", "step_type": "manual", "role": "officer", "action": "monitor"}
                        ]
                    },
                    "output": "Scholarship Award Letter"
                }
            }
            create_svc = requests.post(f"{base_url}/service-configs/", json=service_data, headers=headers)
            if create_svc.status_code == 201:
                print("Scholarships Service Created.")
                # We also need to create workflow steps since the API creates ServiceConfig but not nested steps automatically usually?
                # Wait, my `seed_data.py` logic created steps manually.
                # `ServiceConfigSerializer` is read-only for `workflow_steps`.
                # So we must create steps separately.
                svc_id = create_svc.json()['id']
                steps = service_data['config']['rules']['workflow']
                print(f"Creating {len(steps)} workflow steps for Service ID {svc_id}...")
                
                for step in steps:
                    step_payload = {
                        "service_config": svc_id,
                        "sequence": step['sequence'],
                        "step_name": step['step_name'],
                        "step_type": step['step_type'],
                        "role": step.get('role'),
                        "action": step.get('action'),
                        "api_config": step.get('api_config'),
                        "target_mda": None # Simplified
                    }
                    requests.post(f"{base_url}/workflow-steps/", json=step_payload, headers=headers)
                print("Workflow steps created.")
            else:
                print(f"Failed to create Service: {create_svc.text}")
        else:
            print("Scholarships Service already exists.")

    except Exception as e:
        print(f"Error during seeding: {e}")

if __name__ == "__main__":
    check_and_seed()
