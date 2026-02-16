import json

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'

# Priority MDAs from the provided list
priority_updates = {
    "IMMIGRATION": {
        "process_name": "Passport Application Service",
        "narrative": "The To-Be Passport process integrates directly with the Civil Registration Service (Births) and National ID Registry (IPRS) via the Government Service Bus, eliminating the need for physical document verification. Biometrics are validated in real-time.",
        "steps": [
            {"step_number": 1, "description": "Applicant logs in via Single Sign-On (eCitizen) using National ID.", "actor": "Applicant", "system": "SSO / IPRS"},
            {"step_number": 2, "description": "System retrieves Birth Certificate details automatically from Civil Registration Services via Service Bus.", "actor": "System", "system": "Service Bus / CRS API"},
            {"step_number": 3, "description": "Applicant selects appointment for biometric capture (if not already in IPRS).", "actor": "Applicant", "system": "Booking System"},
            {"step_number": 4, "description": "Payment is processed via Government Payment Gateway; receipt auto-generated.", "actor": "System", "system": "Payment Gateway"},
            {"step_number": 5, "description": "Immigration Officer retrieves verified data; approves for printing.", "actor": "Officer", "system": "Passport Production System"},
            {"step_number": 6, "description": "Passport is printed and applicant notified via SMS.", "actor": "System", "system": "Notification Service"}
        ]
    },
    "REFUGEE": {
        "process_name": "Refugee Registration Service",
        "narrative": "The To-Be process creates a unified 'Refugee Digital Identity' by synchronizing UNHCR data with the National Population Register via the Service Bus, ensuring refugees can access services like banking and mobile SIMs.",
        "steps": [
            {"step_number": 1, "description": "Refugee presents themselves at registration center; Biometrics captured.", "actor": "Refugee", "system": "Biometric Kit"},
            {"step_number": 2, "description": "System validates biometrics against UNHCR Database and IPRS (to prevent double registration).", "actor": "System", "system": "Service Bus / ABIS"},
            {"step_number": 3, "description": "Refugee status is determined; 'Alien ID' number generated automatically.", "actor": "System", "system": "IPRS"},
            {"step_number": 4, "description": "Digital Refugee ID (QR Code) is issued immediately to the applicant.", "actor": "System", "system": "Digital Wallet"}
        ]
    },
    "CIVIL REGISTRATION": {
        "process_name": "Registration of Births",
        "narrative": "The To-Be process moves verification to the point of birth. Health facilities push notification data directly to CRS via the Service Bus, triggering auto-generation of the Birth Certificate and unique identifier (Maisha Namba).",
        "steps": [
            {"step_number": 1, "description": "Hospital records birth details in the Health Information System (HIS).", "actor": "Health Officer", "system": "HIS"},
            {"step_number": 2, "description": "HIS pushes data payload to Civil Registration System (CRS) via Service Bus.", "actor": "System", "system": "Service Bus"},
            {"step_number": 3, "description": "Parent validates details via USSD/Portal prompt and confirms name.", "actor": "Parent", "system": "Citizen Portal"},
            {"step_number": 4, "description": "CRS System generates Birth Certificate and Unique Personal Identifier (UPI).", "actor": "System", "system": "CRS Registry"},
            {"step_number": 5, "description": "Digital Birth Certificate is deposited in Parent's Digital Wallet.", "actor": "System", "system": "Digital Wallet"}
        ]
    },
    "MICRO, SMALL": {
        "process_name": "Hustler Fund / Nyayo Application",
        "narrative": "The To-Be process is purely algorithmic. It utilizes data from MNOs (Mobile Network Operators) and BRS (Business Registry) to perform instant credit scoring and disbursement without human intervention.",
        "steps": [
            {"step_number": 1, "description": "MSME Applicant dials USSD or uses App to request fund.", "actor": "Applicant", "system": "USSD/App"},
            {"step_number": 2, "description": "System calls Credit Scoring Engine (using Telco/CRB data) via Service Bus.", "actor": "System", "system": "Credit Algorithm"},
            {"step_number": 3, "description": "System verifies Business Registration status via BRS API.", "actor": "System", "system": "Service Bus / BRS"},
            {"step_number": 4, "description": "Loan limit is calculated and presented to user.", "actor": "System", "system": "Rule Engine"},
            {"step_number": 5, "description": "User accepts terms; Funds disbursed instantly to Mobile Money wallet.", "actor": "System", "system": "Disbursement Engine"}
        ]
    },
    "CULTURE": {
        "process_name": "Artists & Culture Management (UKI)",
        "narrative": "The To-Be process establishes a National Creative Registry. Artists register once, and their work is authenticated against the Copyright Board, enabling access to royalties and government grants.",
        "steps": [
            {"step_number": 1, "description": "Artist registers on 'Talanta Hela' / Culture Portal.", "actor": "Artist", "system": "Culture Portal"},
            {"step_number": 2, "description": "System verifies identity via IPRS API.", "actor": "System", "system": "Service Bus / IPRS"},
            {"step_number": 3, "description": "Artist uploads portfolio/work; System checks Copyright Board database for IP ownership.", "actor": "System", "system": "Service Bus / KECOBO"},
            {"step_number": 4, "description": "Artist is issued a 'Creative ID' card.", "actor": "System", "system": "Registry"},
            {"step_number": 5, "description": "Grants/Royalties are processed automatically based on registered works.", "actor": "System", "system": "Payment Engine"}
        ]
    },
    "PUBLIC SERVICE COMMISSION": {
        "process_name": "Recruitment & Job Applications",
        "narrative": "The To-Be process eliminates manual shortlisting. The system integrates with KNEC (Exams) and CUE (Universities) via the Service Bus to auto-verify academic certificates during the application stage.",
        "steps": [
            {"step_number": 1, "description": "Applicant applies for job on PSC Portal.", "actor": "Applicant", "system": "PSC Portal"},
            {"step_number": 2, "description": "Applicant enters Index Numbers; System pulls results from KNEC/CUE via Service Bus.", "actor": "System", "system": "Service Bus / Education Registry"},
            {"step_number": 3, "description": "System performs auto-shortlisting based on job requirements and verified data.", "actor": "System", "system": "Matching Engine"},
            {"step_number": 4, "description": "Shortlisted candidates are auto-scheduled for interviews.", "actor": "System", "system": "Scheduling Module"},
            {"step_number": 5, "description": "Selected candidates are onboarded into GHRIS (HR System) automatically.", "actor": "System", "system": "GHRIS Integration"}
        ]
    },
    "CHILDREN SERVICES": {
        "process_name": "Child Protection & Case Management",
        "narrative": "The To-Be process implements an Inter-Agency Case Management system where Police, Health, and Judiciary share a single view of the child's case via the Service Bus, ensuring rapid response and tracking.",
        "steps": [
            {"step_number": 1, "description": "Officer reports case in Child Protection Information System (CPIMS).", "actor": "Officer", "system": "CPIMS"},
            {"step_number": 2, "description": "System validates Child Identity via Civil Registration (Births) API.", "actor": "System", "system": "Service Bus / CRS"},
            {"step_number": 3, "description": "Case file is shared securely with Police and Judiciary systems.", "actor": "System", "system": "Service Bus / Inter-Agency"},
            {"step_number": 4, "description": "Social Workers update case notes digitally from the field.", "actor": "Social Worker", "system": "Mobile App"},
            {"step_number": 5, "description": "System generates alerts for case delays or high-risk indicators.", "actor": "System", "system": "Analytics Engine"}
        ]
    },
    "SPORTS": {
        "process_name": "Federation & Player Management",
        "narrative": "The To-Be process creates a 'Digital Athlete Passport' tracking performance, medical history, and federation status, centralized in the Sports Registry.",
        "steps": [
            {"step_number": 1, "description": "Federation/Club registers player on Sports Portal.", "actor": "Federation", "system": "Sports Registry"},
            {"step_number": 2, "description": "System validates player Age and Citizenship via IPRS.", "actor": "System", "system": "Service Bus / IPRS"},
            {"step_number": 3, "description": "Medical personnel update 'Biological Passport' (Anti-Doping) data.", "actor": "Doctor", "system": "Anti-Doping System"},
            {"step_number": 4, "description": "Player license is issued.", "actor": "System", "system": "Registry"}
        ]
    },
    "RONGO": {
        "process_name": "Student Records Management",
        "narrative": "The To-Be process creates a unified Student Digital Profile, integrating admissions, library, and finance into a single view.",
        "steps": [
            {"step_number": 1, "description": "Student accepts admission via Portal.", "actor": "Student", "system": "ERP"},
            {"step_number": 2, "description": "System pulls KCSE results from KNEC via Service Bus for verification.", "actor": "System", "system": "Service Bus / KNEC"},
            {"step_number": 3, "description": "Student pays fees via integrated Payment Gateway.", "actor": "Student", "system": "Payment Gateway"},
            {"step_number": 4, "description": "Smart Student ID is activated for access to Library and Hostels.", "actor": "System", "system": "Access Control"}
        ]
    }
}

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data if isinstance(data, list) else data.get('processes', [])
    count = 0

    for item in items:
        mda_name = item.get('mda_name', '').upper()
        
        # Apply specific priority updates
        matched_key = None
        for key in priority_updates:
            if key in mda_name:
                matched_key = key
                break
        
        if matched_key:
            update = priority_updates[matched_key]
            
            # Update To-Be Process
            item['to_be_process'] = {
                "narrative": update['narrative'],
                "steps": update['steps']
            }
            
            # Update Process Objective to match the priority process name if generic
            current_obj = item.get('process_overview', {}).get('process_objective', '')
            if "Service Delivery" in current_obj or len(current_obj) < 20:
                 item['process_overview']['process_objective'] = f"To facilitate efficient {update['process_name']}."

            # Force specific Opportunities
            item['digitization_opportunities'] = [
                "Integration with Government Service Bus.",
                "Real-time API validation with Authoritative Registries.",
                "Automated Rules Engine for decision making.",
                "Adoption of 'Once-Only' data principle."
            ]
            
            # Tag as High Priority
            if 'metadata' not in item: item['metadata'] = {}
            item['metadata']['priority_status'] = 'High Priority (POC List)'
            
            count += 1

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Successfully updated {count} Priority MDAs with High-Fidelity To-Be Workflows.")

except Exception as e:
    print(f"Error: {e}")
