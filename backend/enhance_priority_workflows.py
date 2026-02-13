import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep

# Enhanced workflows for key services from the 17 priority MDAs
ENHANCED_WORKFLOWS = {
    "Passport Application": {
        "mda_code": "DIS",
        "as_is": [
            {"name": "Download and Print Application Form", "role": "citizen", "type": "manual", "bpmn": "start_event", "seq": 1},
            {"name": "Fill Physical Form Manually", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 2},
            {"name": "Gather Supporting Documents (Birth Cert, ID, Photos)", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 3},
            {"name": "Queue at Immigration Office", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 4},
            {"name": "Submit Application at Counter", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 5},
            {"name": "Manual Document Verification", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 6},
            {"name": "Biometric Capture (Photo & Fingerprints)", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 7},
            {"name": "Payment at Cashier", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 8},
            {"name": "Manual Data Entry into System", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 9},
            {"name": "Background Security Checks", "role": "supervisor", "type": "manual", "bpmn": "user_task", "seq": 10},
            {"name": "Passport Printing and Personalization", "role": "system", "type": "manual", "bpmn": "service_task", "seq": 11},
            {"name": "Quality Assurance Check", "role": "supervisor", "type": "manual", "bpmn": "user_task", "seq": 12},
            {"name": "Collection Notice (SMS/Email)", "role": "system", "type": "manual", "bpmn": "service_task", "seq": 13},
            {"name": "Physical Collection at Office", "role": "citizen", "type": "manual", "bpmn": "end_event", "seq": 14}
        ],
        "to_be": [
            {"name": "Online Application via eCitizen", "role": "citizen", "type": "api", "bpmn": "start_event", "seq": 1},
            {"name": "Auto-fetch Birth & ID Details", "role": "system", "type": "api", "bpmn": "service_task", "seq": 2},
            {"name": "Biometric Appointment Booking", "role": "citizen", "type": "api", "bpmn": "user_task", "seq": 3},
            {"name": "Biometric Capture at Huduma Centre", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 4},
            {"name": "Vetting & Case Review", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 5},
            {"name": "Director Approval (NPKI Signed)", "role": "supervisor", "type": "manual", "bpmn": "user_task", "seq": 6},
            {"name": "Automated Printing & QA", "role": "system", "type": "api", "bpmn": "service_task", "seq": 7},
            {"name": "Issuance & SMS Notification", "role": "system", "type": "api", "bpmn": "end_event", "seq": 8}
        ]
    },
    "Birth Registration": {
        "mda_code": "CRS",
        "as_is": [
            {"name": "Manual Form B1 Submission", "role": "citizen", "type": "manual", "bpmn": "start_event", "seq": 1},
            {"name": "Verify Parents' IDs Manually", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 2},
            {"name": "Manual Entry in Registry", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 3},
            {"name": "Physical Collection", "role": "citizen", "type": "manual", "bpmn": "end_event", "seq": 4}
        ],
        "to_be": [
            {"name": "Start Birth Registration", "role": "citizen", "type": "api", "bpmn": "start_event", "seq": 1},
            {"name": "Auto-verify Parents (IPRS)", "role": "system", "type": "api", "bpmn": "service_task", "seq": 2},
            {"name": "Registrar Case Review", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 3},
            {"name": "Final Enrollment Approval", "role": "registrar", "type": "manual", "bpmn": "user_task", "seq": 4},
            {"name": "Issue Digital Birth Certificate", "role": "system", "type": "api", "bpmn": "end_event", "seq": 5}
        ]
    },
    "NEMIS Registration": {
        "mda_code": "MOE",
        "as_is": [
            {"name": "Visit School with Birth Cert", "role": "citizen", "type": "manual", "bpmn": "start_event", "seq": 1},
            {"name": "Manual Data Entry", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 2}
        ],
        "to_be": [
            {"name": "Provide BEN for Enrollment", "role": "citizen", "type": "api", "bpmn": "start_event", "seq": 1},
            {"name": "Auto-fetch Birth Details", "role": "system", "type": "api", "bpmn": "service_task", "seq": 2},
            {"name": "School Head Review", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 3},
            {"name": "Ministry Approval (UPI Issuance)", "role": "supervisor", "type": "manual", "bpmn": "user_task", "seq": 4},
            {"name": "Enrollment Confirmation", "role": "system", "type": "api", "bpmn": "end_event", "seq": 5}
        ]
    },
    "National ID Application": {
        "mda_code": "NRB",
        "as_is": [
            {"name": "Queue at Huduma Centre", "role": "citizen", "type": "manual", "bpmn": "start_event", "seq": 1},
            {"name": "Submit Birth Cert & Photos", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 2},
            {"name": "Biometric Capture", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 3},
            {"name": "Physical Card Collection", "role": "citizen", "type": "manual", "bpmn": "end_event", "seq": 4}
        ],
        "to_be": [
            {"name": "Initiate ID Application", "role": "citizen", "type": "api", "bpmn": "start_event", "seq": 1},
            {"name": "Auto-validate BEN & UPI", "role": "system", "type": "api", "bpmn": "service_task", "seq": 2},
            {"name": "NRB Officer Document Verification", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 3},
            {"name": "Biometric Enrollment at NRB Office", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 4},
            {"name": "Central Registry Final Approval", "role": "registrar", "type": "manual", "bpmn": "user_task", "seq": 5},
            {"name": "Card Production & Printing", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 6},
            {"name": "Issue Digital ID & SMS Notification", "role": "system", "type": "api", "bpmn": "end_event", "seq": 7}
        ]
    },
    "PIN Registration": {
        "mda_code": "KRA",
        "as_is": [
            {"name": "Fill iTax Form", "role": "citizen", "type": "manual", "bpmn": "start_event", "seq": 1},
            {"name": "Tax Officer Review", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 2},
            {"name": "Email PIN Certificate", "role": "system", "type": "manual", "bpmn": "end_event", "seq": 3}
        ],
        "to_be": [
            {"name": "Link National ID", "role": "citizen", "type": "api", "bpmn": "start_event", "seq": 1},
            {"name": "Bio-data Sync (NRB/IPRS)", "role": "system", "type": "api", "bpmn": "service_task", "seq": 2},
            {"name": "Compliance Data Review", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 3},
            {"name": "PIN Generation Approval", "role": "supervisor", "type": "manual", "bpmn": "user_task", "seq": 4},
            {"name": "Notify Taxpayer via SMS", "role": "system", "type": "api", "bpmn": "end_event", "seq": 5}
        ]
    },
    "Business Name Registration": {
        "mda_code": "ROC",
        "as_is": [
            {"name": "Submit Name Search Request", "role": "citizen", "type": "manual", "bpmn": "start_event", "seq": 1},
            {"name": "Manual Name Search", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 2},
            {"name": "Name Reservation", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 3}
        ],
        "to_be": [
            {"name": "Enter Owner KRA PIN", "role": "citizen", "type": "api", "bpmn": "start_event", "seq": 1},
            {"name": "Auto-verify Tax Compliance", "role": "system", "type": "api", "bpmn": "service_task", "seq": 2},
            {"name": "Registrar Name Search Review", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 3},
            {"name": "Director Name Reservation", "role": "supervisor", "type": "manual", "bpmn": "user_task", "seq": 4},
            {"name": "Issue Business Reg Number", "role": "system", "type": "api", "bpmn": "end_event", "seq": 5}
        ]
    },
    "Driving Licence Application": {
        "mda_code": "NTSA",
        "as_is": [
            {"name": "Book Driver Test", "role": "citizen", "type": "manual", "bpmn": "start_event", "seq": 1},
            {"name": "Take Physical Test", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 2},
            {"name": "Officer Manual Grading", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 3}
        ],
        "to_be": [
            {"name": "Link National ID for Eligibility", "role": "citizen", "type": "api", "bpmn": "start_event", "seq": 1},
            {"name": "Verify Eligibility (NRB)", "role": "system", "type": "api", "bpmn": "service_task", "seq": 2},
            {"name": "Inspection Review", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 3},
            {"name": "Licence Issuance Approval", "role": "supervisor", "type": "manual", "bpmn": "user_task", "seq": 4},
            {"name": "Issue Interim Driving Licence", "role": "system", "type": "api", "bpmn": "end_event", "seq": 5}
        ]
    },
    "TSC Number Application": {
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
            {"name": "Auto-fetch ID & Academic Data", "role": "system", "type": "api", "bpmn": "service_task", "seq": 2},
            {"name": "Credential Review & Validation", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 3},
            {"name": "Registrar TSC Number Approval", "role": "supervisor", "type": "manual", "bpmn": "user_task", "seq": 4},
            {"name": "Email Digital Certificate", "role": "system", "type": "api", "bpmn": "end_event", "seq": 5}
        ]
    },
    "Platform Onboarding": {
        "mda_code": "MOI",
        "as_is": [
            {"name": "Fill Physical Registration Form", "role": "citizen", "type": "manual", "bpmn": "start_event", "seq": 1},
            {"name": "Submit Form at District HQ", "role": "citizen", "type": "manual", "bpmn": "user_task", "seq": 2},
            {"name": "Manual Ledger Enrichment", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 3},
            {"name": "Wait for Approval Letter", "role": "citizen", "type": "manual", "bpmn": "end_event", "seq": 4}
        ],
        "to_be": [
            {"name": "Initiate Migration Request", "role": "citizen", "type": "api", "bpmn": "start_event", "seq": 1},
            {"name": "Legacy Record Archival Search", "role": "system", "type": "api", "bpmn": "service_task", "seq": 2},
            {"name": "Officer Document Vetting", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 3},
            {"name": "Identity Biometric Calibration", "role": "officer", "type": "manual", "bpmn": "user_task", "seq": 4},
            {"name": "Supervisor Migration Approval", "role": "supervisor", "type": "manual", "bpmn": "user_task", "seq": 5},
            {"name": "Provision Digital Profile & SMS", "role": "system", "type": "api", "bpmn": "end_event", "seq": 6}
        ]
    }
}

if __name__ == "__main__":
    print("=== ENHANCING WORKFLOWS FOR PRIORITY SERVICES ===\n")

    updated_services = 0
    not_found_services = []

    for service_name, workflow_data in ENHANCED_WORKFLOWS.items():
        try:
            # Find the MDA
            mda = MDA.objects.filter(code=workflow_data["mda_code"]).first()
            if not mda:
                print(f"✗ MDA not found: {workflow_data['mda_code']}")
                continue
            
            # Find the service
            service = ServiceConfig.objects.filter(
                service_name__icontains=service_name,
                mda=mda
            ).first()
            
            if not service:
                # Try broader search
                service = ServiceConfig.objects.filter(
                    service_name__icontains=service_name.split()[0]
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
                not_found_services.append(service_name)
                print(f"✗ Service not found: {service_name}")
                
        except Exception as e:
            print(f"✗ Error updating {service_name}: {str(e)}")

    print(f"\n=== SUMMARY ===")
    print(f"Updated services: {updated_services}/{len(ENHANCED_WORKFLOWS)}")
    if not_found_services:
        print(f"\nServices not found:")
        for name in not_found_services:
            print(f"  - {name}")
