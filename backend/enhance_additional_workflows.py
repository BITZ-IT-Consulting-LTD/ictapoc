import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep

# Additional enhanced workflows for remaining priority services
ADDITIONAL_WORKFLOWS = {
    "PIN Registration": {
        "mda_code": "KRA",
        "as_is": [
            {"name": "Download PIN Application Form", "role": "citizen", "type": "manual", "bpmn": "start_event", "seq": 1},
            {"name": "Fill Form Manually", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 2},
            {"name": "Photocopy ID and Supporting Docs", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 3},
            {"name": "Visit KRA Office or Huduma Centre", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 4},
            {"name": "Queue for Service", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 5},
            {"name": "Submit at Counter", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 6},
            {"name": "Manual Document Verification", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 7},
            {"name": "Manual Data Entry into iTax", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 8},
            {"name": "PIN Generation", "role": "system", "type": "manual", "bpmn": "service_task", "seq": 9},
            {"name": "Print PIN Certificate", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 10},
            {"name": "Collect PIN Certificate", "role": "citizen", "type": "manual", "bpmn": "end_event", "seq": 11}
        ],
        "to_be": [
            {"name": "Online Registration via iTax Portal", "role": "citizen", "type": "api", "bpmn": "start_event", "seq": 1},
            {"name": "Auto-fetch ID Details from NRB", "role": "system", "type": "api", "bpmn": "service_task", "seq": 2},
            {"name": "Fill Online Form (Pre-populated)", "role": "citizen", "type": "api", "bpmn": "user_task", "seq": 3},
            {"name": "Upload ID Photo (Auto-validated)", "role": "citizen", "type": "api", "bpmn": "user_task", "seq": 4},
            {"name": "Automated Duplicate Check", "role": "system", "type": "api", "bpmn": "service_task", "seq": 5},
            {"name": "Instant PIN Generation", "role": "system", "type": "api", "bpmn": "service_task", "seq": 6},
            {"name": "Email PIN Certificate (PDF)", "role": "system", "type": "api", "bpmn": "service_task", "seq": 7},
            {"name": "SMS Confirmation", "role": "system", "type": "api", "bpmn": "service_task", "seq": 8},
            {"name": "Download Digital Certificate", "role": "citizen", "type": "api", "bpmn": "end_event", "seq": 9}
        ]
    },
    "Teacher Registration": {
        "mda_code": "TSC",
        "as_is": [
            {"name": "Download TSC Registration Form", "role": "citizen", "type": "manual", "bpmn": "start_event", "seq": 1},
            {"name": "Fill Form Manually", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 2},
            {"name": "Gather Academic Certificates", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 3},
            {"name": "Get Certified Copies", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 4},
            {"name": "Visit TSC County Office", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 5},
            {"name": "Submit Application Physically", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 6},
            {"name": "Manual Document Verification", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 7},
            {"name": "Manual Data Entry", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 8},
            {"name": "Forward to HQ for Processing", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 9},
            {"name": "HQ Verification and Approval", "role": "supervisor", "type": "manual", "bpmn": "user_task", "seq": 10},
            {"name": "TSC Number Generation", "role": "system", "type": "manual", "bpmn": "service_task", "seq": 11},
            {"name": "Postal Notification", "role": "system", "type": "manual", "bpmn": "service_task", "seq": 12},
            {"name": "Collect Certificate at County Office", "role": "citizen", "type": "manual", "bpmn": "end_event", "seq": 13}
        ],
        "to_be": [
            {"name": "Online Registration via TSC Portal", "role": "citizen", "type": "api", "bpmn": "start_event", "seq": 1},
            {"name": "Auto-fetch ID Details from NRB", "role": "system", "type": "api", "bpmn": "service_task", "seq": 2},
            {"name": "Upload Academic Certificates (PDF)", "role": "citizen", "type": "api", "bpmn": "user_task", "seq": 3},
            {"name": "Auto-verify Certificates with KNEC", "role": "system", "type": "api", "bpmn": "service_task", "seq": 4},
            {"name": "Auto-verify University Certs with CUE", "role": "system", "type": "api", "bpmn": "service_task", "seq": 5},
            {"name": "Automated Eligibility Check", "role": "system", "type": "api", "bpmn": "service_task", "seq": 6},
            {"name": "Digital Approval Workflow", "role": "supervisor", "type": "manual", "bpmn": "user_task", "seq": 7},
            {"name": "Instant TSC Number Generation", "role": "system", "type": "api", "bpmn": "service_task", "seq": 8},
            {"name": "Email Certificate (PDF)", "role": "system", "type": "api", "bpmn": "service_task", "seq": 9},
            {"name": "SMS Notification", "role": "system", "type": "api", "bpmn": "service_task", "seq": 10},
            {"name": "Download Digital Certificate", "role": "citizen", "type": "api", "bpmn": "end_event", "seq": 11}
        ]
    },
    "HELB Loan Application": {
        "mda_code": "HELB",
        "as_is": [
            {"name": "Download HELB Application Form", "role": "citizen", "type": "manual", "bpmn": "start_event", "seq": 1},
            {"name": "Fill Form Manually", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 2},
            {"name": "Gather Supporting Documents (Admission, ID, KRA PIN)", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 3},
            {"name": "Get Guarantor Signatures", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 4},
            {"name": "Submit at HELB Office or University", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 5},
            {"name": "Manual Document Verification", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 6},
            {"name": "Manual Data Entry", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 7},
            {"name": "Means Testing Assessment", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 8},
            {"name": "Approval Committee Review", "role": "supervisor", "type": "manual", "bpmn": "user_task", "seq": 9},
            {"name": "Loan Amount Determination", "role": "supervisor", "type": "manual", "bpmn": "user_task", "seq": 10},
            {"name": "Postal Notification", "role": "system", "type": "manual", "bpmn": "service_task", "seq": 11},
            {"name": "Loan Disbursement to University", "role": "system", "type": "manual", "bpmn": "end_event", "seq": 12}
        ],
        "to_be": [
            {"name": "Online Application via HELB Portal", "role": "citizen", "type": "api", "bpmn": "start_event", "seq": 1},
            {"name": "Auto-fetch ID Details from NRB", "role": "system", "type": "api", "bpmn": "service_task", "seq": 2},
            {"name": "Auto-fetch KRA PIN Details", "role": "system", "type": "api", "bpmn": "service_task", "seq": 3},
            {"name": "Auto-verify University Admission with CUE", "role": "system", "type": "api", "bpmn": "service_task", "seq": 4},
            {"name": "Upload Supporting Documents (PDF)", "role": "citizen", "type": "api", "bpmn": "user_task", "seq": 5},
            {"name": "Digital Guarantor Consent (SMS/Email)", "role": "system", "type": "api", "bpmn": "service_task", "seq": 6},
            {"name": "Automated Means Testing (KRA Data)", "role": "system", "type": "api", "bpmn": "service_task", "seq": 7},
            {"name": "AI-Assisted Loan Scoring", "role": "system", "type": "api", "bpmn": "service_task", "seq": 8},
            {"name": "Digital Approval Workflow", "role": "supervisor", "type": "manual", "bpmn": "user_task", "seq": 9},
            {"name": "Automated Loan Calculation", "role": "system", "type": "api", "bpmn": "service_task", "seq": 10},
            {"name": "SMS/Email Notification", "role": "system", "type": "api", "bpmn": "service_task", "seq": 11},
            {"name": "Automated Disbursement to University", "role": "system", "type": "api", "bpmn": "end_event", "seq": 12}
        ]
    },
    "NHIF Registration": {
        "mda_code": "NHIF",
        "as_is": [
            {"name": "Download NHIF Registration Form", "role": "citizen", "type": "manual", "bpmn": "start_event", "seq": 1},
            {"name": "Fill Form Manually", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 2},
            {"name": "Attach ID Copy and Passport Photo", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 3},
            {"name": "Visit NHIF Office or Huduma Centre", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 4},
            {"name": "Queue for Service", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 5},
            {"name": "Submit at Counter", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 6},
            {"name": "Manual Document Verification", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 7},
            {"name": "Manual Data Entry", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 8},
            {"name": "NHIF Number Generation", "role": "system", "type": "manual", "bpmn": "service_task", "seq": 9},
            {"name": "Print NHIF Card", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 10},
            {"name": "Collect NHIF Card", "role": "citizen", "type": "manual", "bpmn": "end_event", "seq": 11}
        ],
        "to_be": [
            {"name": "Online Registration via NHIF Portal", "role": "citizen", "type": "api", "bpmn": "start_event", "seq": 1},
            {"name": "Auto-fetch ID Details from NRB", "role": "system", "type": "api", "bpmn": "service_task", "seq": 2},
            {"name": "Upload Photo (Auto-validated)", "role": "citizen", "type": "api", "bpmn": "user_task", "seq": 3},
            {"name": "Select Contribution Category", "role": "citizen", "type": "api", "bpmn": "user_task", "seq": 4},
            {"name": "Automated Duplicate Check", "role": "system", "type": "api", "bpmn": "service_task", "seq": 5},
            {"name": "Instant NHIF Number Generation", "role": "system", "type": "api", "bpmn": "service_task", "seq": 6},
            {"name": "Digital NHIF Card (PDF)", "role": "system", "type": "api", "bpmn": "service_task", "seq": 7},
            {"name": "SMS/Email Notification", "role": "system", "type": "api", "bpmn": "service_task", "seq": 8},
            {"name": "Download Digital Card", "role": "citizen", "type": "api", "bpmn": "end_event", "seq": 9}
        ]
    },
    "Business Registration": {
        "mda_code": "ROC",
        "as_is": [
            {"name": "Name Search at Sheria House", "role": "citizen", "type": "manual", "bpmn": "start_event", "seq": 1},
            {"name": "Pay Name Search Fee", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 2},
            {"name": "Wait for Name Approval (Manual)", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 3},
            {"name": "Download Registration Forms", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 4},
            {"name": "Fill Forms Manually", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 5},
            {"name": "Prepare Memorandum and Articles", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 6},
            {"name": "Submit at Sheria House", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 7},
            {"name": "Pay Registration Fees", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 8},
            {"name": "Manual Document Review", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 9},
            {"name": "Manual Data Entry", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 10},
            {"name": "Certificate Generation", "role": "system", "type": "manual", "bpmn": "service_task", "seq": 11},
            {"name": "Wait for Notification (7-14 days)", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 12},
            {"name": "Physical Collection at Sheria House", "role": "citizen", "type": "manual", "bpmn": "end_event", "seq": 13}
        ],
        "to_be": [
            {"name": "Online Name Search via eCitizen", "role": "citizen", "type": "api", "bpmn": "start_event", "seq": 1},
            {"name": "Automated Name Availability Check", "role": "system", "type": "api", "bpmn": "service_task", "seq": 2},
            {"name": "Online Payment via M-Pesa", "role": "citizen", "type": "api", "bpmn": "service_task", "seq": 3},
            {"name": "Instant Name Reservation", "role": "system", "type": "api", "bpmn": "service_task", "seq": 4},
            {"name": "Online Form Filling (Guided)", "role": "citizen", "type": "api", "bpmn": "user_task", "seq": 5},
            {"name": "Upload Memorandum & Articles (PDF)", "role": "citizen", "type": "api", "bpmn": "user_task", "seq": 6},
            {"name": "Auto-fetch Director ID Details from NRB", "role": "system", "type": "api", "bpmn": "service_task", "seq": 7},
            {"name": "Online Registration Fee Payment", "role": "citizen", "type": "api", "bpmn": "service_task", "seq": 8},
            {"name": "Automated Document Validation", "role": "system", "type": "api", "bpmn": "service_task", "seq": 9},
            {"name": "Digital Approval (Officer Review)", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 10},
            {"name": "Instant Certificate Generation", "role": "system", "type": "api", "bpmn": "service_task", "seq": 11},
            {"name": "Email Certificate (PDF + QR Code)", "role": "system", "type": "api", "bpmn": "service_task", "seq": 12},
            {"name": "Download Digital Certificate", "role": "citizen", "type": "api", "bpmn": "end_event", "seq": 13}
        ]
    }
}

print("=== ENHANCING ADDITIONAL PRIORITY SERVICE WORKFLOWS ===\n")

updated_services = 0

for service_name, workflow_data in ADDITIONAL_WORKFLOWS.items():
    try:
        # Find the MDA
        mda = MDA.objects.filter(code=workflow_data["mda_code"]).first()
        if not mda:
            print(f"✗ MDA not found: {workflow_data['mda_code']}")
            continue
        
        # Find the service (exact match)
        service = ServiceConfig.objects.filter(
            service_name__iexact=service_name,
            mda=mda
        ).first()
        
        # Try partial match if exact fails
        if not service:
            service = ServiceConfig.objects.filter(
                service_name__icontains=service_name.split()[0],
                mda=mda
            ).first()
        
        if service:
            print(f"\n📋 Updating: {service.service_name} ({mda.code})")
            
            # Delete existing workflow steps
            WorkflowStep.objects.filter(service_config=service).delete()
            
            # Add As-Is workflow
            for step_data in workflow_data["as_is"]:
                WorkflowStep.objects.create(
                    service_config=service,
                    step_name=step_data["name"],
                    role=step_data["role"],
                    step_type=step_data["type"],
                    bpmn_element_type=step_data["bpmn"],
                    lifecycle_stage="as_is",
                    sequence=step_data["seq"]
                )
            print(f"  ✓ Added {len(workflow_data['as_is'])} As-Is steps")
            
            # Add To-Be workflow
            for step_data in workflow_data["to_be"]:
                WorkflowStep.objects.create(
                    service_config=service,
                    step_name=step_data["name"],
                    role=step_data["role"],
                    step_type=step_data["type"],
                    bpmn_element_type=step_data["bpmn"],
                    lifecycle_stage="to_be",
                    sequence=step_data["seq"]
                )
            print(f"  ✓ Added {len(workflow_data['to_be'])} To-Be steps")
            
            updated_services += 1
        else:
            print(f"✗ Service not found: {service_name} under {mda.name}")
            
    except Exception as e:
        print(f"✗ Error updating {service_name}: {str(e)}")

print(f"\n=== SUMMARY ===")
print(f"Updated additional services: {updated_services}/{len(ADDITIONAL_WORKFLOWS)}")
