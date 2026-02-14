import json

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'

# --- To-Be Optimization Logic ---

def generate_tobe_workflow(mda_name, category):
    # Core Optimizations
    registry = "IPRS (Identity Registry)" if category == "G2C" else "BRS (Business Registry)"
    id_type = "National ID" if category == "G2C" else "Business Registration Number"
    
    narrative = (
        f"The To-Be process leverages the Government Service Bus to integrate with {registry} "
        f"and the Payment Gateway. Manual data entry and document uploads are replaced by real-time "
        f"API validations, enabling a paperless, cashless, and presence-less service experience."
    )
    
    steps = [
        {
            "step_number": 1,
            "description": "Applicant logs in via Single Sign-On (SSO) and selects the service.",
            "actor": "Applicant",
            "system": "Citizen Portal / SSO"
        },
        {
            "step_number": 2,
            "description": f"Applicant enters {id_type}; System auto-populates details from {registry} via the Service Bus.",
            "actor": "System",
            "system": "Service Bus / Registry API"
        },
        {
            "step_number": 3,
            "description": "System performs auto-validation of compliance (e.g., KRA Tax Status) via Inter-Agency APIs.",
            "actor": "System",
            "system": "Service Bus / Compliance Engine"
        },
        {
            "step_number": 4,
            "description": "Applicant pays fees via the Government Payment Gateway; System auto-receipts.",
            "actor": "Applicant",
            "system": "Payment Gateway"
        },
        {
            "step_number": 5,
            "description": "Application is processed by the Rules Engine. (Low-risk cases are Auto-Approved).",
            "actor": "System",
            "system": "Workflow Engine"
        },
        {
            "step_number": 6,
            "description": "Complex cases are routed to the Officer Workbench for digital review and approval.",
            "actor": "Officer",
            "system": "Officer Workbench"
        },
        {
            "step_number": 7,
            "description": "System generates a Verifiable Digital Certificate (QR Code) and notifies the applicant.",
            "actor": "System",
            "system": "Output Generator"
        }
    ]
    
    return narrative, steps

# --- Execution ---

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data if isinstance(data, list) else data.get('processes', [])
    count = 0

    for item in items:
        mda_name = item.get('mda_name', '').upper()
        
        # Determine Category
        category = "G2B"
        if any(x in mda_name for x in ["UNIVERSITY", "HOSPITAL", "IMMIGRATION", "PERSONS", "EDUCATION", "HEALTH"]):
            category = "G2C"
        
        # Generate To-Be
        narrative, steps = generate_tobe_workflow(mda_name, category)
        
        # Update JSON
        if 'to_be_process' not in item:
            item['to_be_process'] = {}
            
        item['to_be_process']['narrative'] = narrative
        item['to_be_process']['steps'] = steps
        
        # Also update digitization opportunities to reflect this
        item['digitization_opportunities'] = [
            "Integration with IPRS/BRS via Service Bus.",
            "Adoption of Government Payment Gateway.",
            "Implementation of Automated Rules Engine.",
            "Issuance of Digital Verifiable Credentials."
        ]
        
        count += 1

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Updated To-Be Processes for {count} MDAs.")

except Exception as e:
    print(f"Error: {e}")
