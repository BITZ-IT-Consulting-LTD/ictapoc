import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, ServiceDomain, ServiceCategory, WorkflowStep

def force_seed_catalog():
    print("--- FORCING CLEAN SLATE & SEEDING FROM MD FILES ---")

    # Clear EVERYTHING related to the catalogue
    print("Deleting all existing catalogue records...")
    WorkflowStep.objects.all().delete()
    ServiceConfig.objects.all().delete()
    # ServiceCategory.objects.all().delete() # Careful with cascades
    # ServiceDomain.objects.all().delete()
    # MDA.objects.all().delete()

    
    DATA = [
        {
            "sector": "Public Service & Administration",
            "mda": "Athi Water Works Development Agency (AWWDA)",
            "category": "Standard Government Services",
            "service": "Planning",
            "type": "G2C",
            "maturity": 2,
            "complexity": "4-7 steps",
            "description": "Standardized process for Planning.",
            "bpmn_data": {
                "as_is": [
                    {
                        "name": "(Mobilize Team",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Establish Office",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Review Programme",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Monitor Activities",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Site Inspections",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Material Testing",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Work OK?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Non-Conformance Issued",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Measure Works",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Prepare IPC",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Certify Payment",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Process Payment",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Progress Reports",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Completion?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "(Handover",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ],
                "to_be": [
                    {
                        "name": "Digital Submission",
                        "role": "citizen",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Automated Validation",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Digital Approval",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Electronic Issuance",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    }
                ]
            }
        },
        {
            "sector": "Public Service & Administration",
            "mda": "Authority",
            "category": "Standard Government Services",
            "service": "Registration",
            "type": "G2C",
            "maturity": 2,
            "complexity": "4-7 steps",
            "description": "Standardized process for Registration.",
            "bpmn_data": {
                "as_is": [
                    {
                        "name": "(Start",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Complete Form",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Attach License & Certs",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Submit via IMIS",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "System Receives",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Route to Directorate",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Verify Trader",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Verify Origin",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Check Quality",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Verified?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Reject Application",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "(End",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Approve",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Generate Permit",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Transmit to KENTRADE",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Link Customs",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Notify Exporter",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ],
                "to_be": [
                    {
                        "name": "Digital Submission",
                        "role": "citizen",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Automated Validation",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Digital Approval",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Electronic Issuance",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    }
                ]
            }
        },
        {
            "sector": "Public Service & Administration",
            "mda": "Ministry of Children Services",
            "category": "Standard Government Services",
            "service": "Child Protection",
            "type": "G2C",
            "maturity": 2,
            "complexity": "4-7 steps",
            "description": "Standardized process for Child Protection.",
            "bpmn_data": {
                "as_is": [
                    {
                        "name": "(From Reporting",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Review Report",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Check History",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Contact Reporter",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Assess Safety",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Risk Level",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Police/Medical/Removal",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "To Investigation",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "To Support/Referral",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ],
                "to_be": [
                    {
                        "name": "Digital Submission",
                        "role": "citizen",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Automated Validation",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Digital Approval",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Electronic Issuance",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    }
                ]
            }
        },
        {
            "sector": "Education & Training",
            "mda": "Ministry of Education (KNQA)",
            "category": "Standard Government Services",
            "service": "Qualification Validation",
            "type": "G2C",
            "maturity": 4,
            "complexity": "4-7 steps",
            "description": "Standardized process for Qualification Validation.",
            "bpmn_data": {
                "as_is": [
                    {
                        "name": "(Start",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Submit Application",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Pay Fee",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Complete?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Request Missing Info",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Authenticate Certificates",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Verify Institution",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Assess Against KNQF",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Determine Level",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Document Rationale",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Committee Review",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Notify Applicant",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "(End",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Officer Approval",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Generate Letter",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Digital Signature",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Issue to Applicant",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Update Registry",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ],
                "to_be": [
                    {
                        "name": "(Start",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Unified Intake Portal",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Registry Check",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Return Existing Validation",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "(Instant",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Process New Application",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "KNQA Decision",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Publish to Registry",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "API Access for Employers/PSC",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "(End",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ]
            }
        },
        {
            "sector": "Public Service & Administration",
            "mda": "National Government Co-ordination",
            "category": "Standard Government Services",
            "service": "Coordination Trigger",
            "type": "G2C",
            "maturity": 2,
            "complexity": "4-7 steps",
            "description": "Standardized process for Coordination Trigger.",
            "bpmn_data": {
                "as_is": [
                    {
                        "name": "(Start",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Coordination Trigger",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Prepare Brief & Define Scope",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Issue Requests & Set Deadlines",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Track Compliance",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Receive & Consolidate Data",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Analyse Information & Identify Issues",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Critical Issues?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Escalate to Leadership",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Produce & Share Reports",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Archive Data",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "(End",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ],
                "to_be": [
                    {
                        "name": "Digital Submission",
                        "role": "citizen",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Automated Validation",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Digital Approval",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Electronic Issuance",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    }
                ]
            }
        },
        {
            "sector": "Public Service & Administration",
            "mda": "National Government Co-ordination",
            "category": "Standard Government Services",
            "service": "Information Tasking",
            "type": "G2C",
            "maturity": 2,
            "complexity": "4-7 steps",
            "description": "Standardized process for Information Tasking.",
            "bpmn_data": {
                "as_is": [
                    {
                        "name": "(From Trigger",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Draft Request",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Define Template",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Submit for Clearance",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Approved?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Finalize Documents",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Issue to MDAs & Regions",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Log Distribution",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Monitor Acknowledgments",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Received?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Send Reminder",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "(To Collection",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ],
                "to_be": [
                    {
                        "name": "Digital Submission",
                        "role": "citizen",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Automated Validation",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Digital Approval",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Electronic Issuance",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    }
                ]
            }
        },
        {
            "sector": "Public Service & Administration",
            "mda": "National Government Co-ordination",
            "category": "Standard Government Services",
            "service": "Data Collection",
            "type": "G2C",
            "maturity": 2,
            "complexity": "4-7 steps",
            "description": "Standardized process for Data Collection.",
            "bpmn_data": {
                "as_is": [
                    {
                        "name": "(From Tasking",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Receive Submissions",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Log All Submissions",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Complete & Valid?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Request Resubmission",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Extract & Merge Data",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Standardize Formats",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Generate Dashboards & SitReps",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "(To Review",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ],
                "to_be": [
                    {
                        "name": "Digital Submission",
                        "role": "citizen",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Automated Validation",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Digital Approval",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Electronic Issuance",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    }
                ]
            }
        },
        {
            "sector": "Public Service & Administration",
            "mda": "Office of the Head of Public Service",
            "category": "Standard Government Services",
            "service": "Executive Coordination",
            "type": "G2C",
            "maturity": 2,
            "complexity": "4-7 steps",
            "description": "Standardized process for Executive Coordination.",
            "bpmn_data": {
                "as_is": [
                    {
                        "name": "(Start",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Receive Presidential Directive",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Translate to Instructions",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Issue to MDAs",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Define Requirements & Deadlines",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Receive Submissions",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Complete?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Follow Up with MDAs",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Consolidate Data",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Analyse & Prepare Summary",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Make Recommendations",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Brief Leadership",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Issue Strategic Guidance",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Monitor Implementation",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "(End",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ],
                "to_be": [
                    {
                        "name": "Digital Submission",
                        "role": "citizen",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Automated Validation",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Digital Approval",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Electronic Issuance",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    }
                ]
            }
        },
        {
            "sector": "Interior & National Administration",
            "mda": "State Department Civil Registration Services",
            "category": "Standard Government Services",
            "service": "Birth Registration",
            "type": "G2C",
            "maturity": 2,
            "complexity": "4-7 steps",
            "description": "Standardized process for Birth Registration.",
            "bpmn_data": {
                "as_is": [
                    {
                        "name": "(Start",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Submit Request & Pay Fee",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Search Registry",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Found?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Notify Not Found",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "(End",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Entitled?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Reject Request",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Quality Check",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Print & Issue Certificate",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ],
                "to_be": [
                    {
                        "name": "Digital Submission",
                        "role": "citizen",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Automated Validation",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Digital Approval",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Electronic Issuance",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    }
                ]
            }
        },
        {
            "sector": "Interior & National Administration",
            "mda": "State Department Civil Registration Services",
            "category": "Standard Government Services",
            "service": "Death Registration",
            "type": "G2C",
            "maturity": 2,
            "complexity": "4-7 steps",
            "description": "Standardized process for Death Registration.",
            "bpmn_data": {
                "as_is": [
                    {
                        "name": "(Start",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Location?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Medical Certificate",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Chief Report",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Complete Form",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Attach ID of Deceased & Informant",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Submit",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Verified?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Request More Info",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Enter in Register",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Issue Burial Permit",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Registrar Signs",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Issue Death Certificate",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "(End",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ],
                "to_be": [
                    {
                        "name": "Digital Submission",
                        "role": "citizen",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Automated Validation",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Digital Approval",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Electronic Issuance",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    }
                ]
            }
        },
        {
            "sector": "Sports, Culture & the Arts",
            "mda": "State Department for Culture, Arts and Heritage (Ushanga Kenya)",
            "category": "Standard Government Services",
            "service": "Product Facilitation",
            "type": "G2C",
            "maturity": 2,
            "complexity": "4-7 steps",
            "description": "Standardized process for Product Facilitation.",
            "bpmn_data": {
                "as_is": [
                    {
                        "name": "(Start",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Receive Products",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Issue Receipt",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Log Inventory",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Inspect Products",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Grade Outcome",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Reject & Feedback",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "(End",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Return for Rework",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Photograph & Assign Codes",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Update Digital Catalog",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Place in Outlets / Exhibitions",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Product Sold?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Re-evaluate Placement",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Record Sale & Reconcile",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Calculate Earnings",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Process Disbursement",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Notify Cooperative",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ],
                "to_be": [
                    {
                        "name": "Digital Submission",
                        "role": "citizen",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Automated Validation",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Digital Approval",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Electronic Issuance",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    }
                ]
            }
        },
        {
            "sector": "Sports, Culture & the Arts",
            "mda": "State Department for Sports",
            "category": "Standard Government Services",
            "service": "Federation Management",
            "type": "G2C",
            "maturity": 2,
            "complexity": "4-7 steps",
            "description": "Standardized process for Federation Management.",
            "bpmn_data": {
                "as_is": [
                    {
                        "name": "(Start",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Complete Grant Form",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Attach Records & Endorsement",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Submit to Department",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Verify Registration & Performance",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Info Sufficient?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Request Additional Info",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Assess Purpose & Budget",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Submit to Review Committee",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Committee Decision",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Notify Athlete",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "(End",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Prepare Grant Agreement",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Athlete Signs",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Process Disbursement",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Notify Athlete & Monitor",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ],
                "to_be": [
                    {
                        "name": "Digital Submission",
                        "role": "citizen",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Automated Validation",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Digital Approval",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Electronic Issuance",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    }
                ]
            }
        },
        {
            "sector": "Public Service & Administration",
            "mda": "State Department for MSME Development",
            "category": "Standard Government Services",
            "service": "Hustler Fund (Digital Credit)",
            "type": "G2C",
            "maturity": 2,
            "complexity": "4-7 steps",
            "description": "Standardized process for Hustler Fund (Digital Credit).",
            "bpmn_data": {
                "as_is": [
                    {
                        "name": "(Start",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Register Group & Verify Members",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Approve Group Registration",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Submit Loan Request & Proposal",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Review Application & Assess Proposal",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Credit Committee",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "(End",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Sign Agreement",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Disburse to Group Account",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Track Utilization & Repayment",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ],
                "to_be": [
                    {
                        "name": "Digital Submission",
                        "role": "citizen",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Automated Validation",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Digital Approval",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Electronic Issuance",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    }
                ]
            }
        },
        {
            "sector": "Public Service & Administration",
            "mda": "State Department for Science, Research and Innovation",
            "category": "Standard Government Services",
            "service": "Research Application",
            "type": "G2C",
            "maturity": 2,
            "complexity": "4-7 steps",
            "description": "Standardized process for Research Application.",
            "bpmn_data": {
                "as_is": [
                    {
                        "name": "(Start",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Complete Form & Attach Docs",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Submit to Office",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Receive & Assign Reference",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Log in Register",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Examiner Review",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Approved?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Return for Revision",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Generate Payment Request",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Process Payment",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Verify Receipt",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Contact Institution & Coordinate",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Develop Final Proposal",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "(End",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ],
                "to_be": [
                    {
                        "name": "Digital Submission",
                        "role": "citizen",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Automated Validation",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Digital Approval",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Electronic Issuance",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    }
                ]
            }
        },
        {
            "sector": "Public Service & Administration",
            "mda": "State Department for Cabinet Affairs",
            "category": "Standard Government Services",
            "service": "Information Management (EDRMS)",
            "type": "G2C",
            "maturity": 2,
            "complexity": "4-7 steps",
            "description": "Standardized process for Information Management (EDRMS).",
            "bpmn_data": {
                "as_is": [
                    {
                        "name": "(Start",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Submit Request",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Specify Trip Details",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Vehicle Available?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Notify Rejection",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "(End",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Allocate Vehicle & Driver",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Issue Work Ticket",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Trip Commences",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Track Movement",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Return Vehicle & Record Mileage",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Close Ticket",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ],
                "to_be": [
                    {
                        "name": "Digital Submission",
                        "role": "citizen",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Automated Validation",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Digital Approval",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Electronic Issuance",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    }
                ]
            }
        },
        {
            "sector": "Public Service & Administration",
            "mda": "State Department for Youth Affairs and Creative Economy",
            "category": "Standard Government Services",
            "service": "Youth Employment Facilitation",
            "type": "G2C",
            "maturity": 2,
            "complexity": "4-7 steps",
            "description": "Standardized process for Youth Employment Facilitation.",
            "bpmn_data": {
                "as_is": [
                    {
                        "name": "(Start",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Access NYOTA Portal",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Create Account & Upload Docs",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Review Application & Assess Skills",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Match Apprentice with Master",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Sign Training Agreement",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Start Training & Track Progress",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Assess Periodically",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Final Assessment",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Issue Certificate",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Update Registry",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "(End",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ],
                "to_be": [
                    {
                        "name": "Digital Submission",
                        "role": "citizen",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Automated Validation",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Digital Approval",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Electronic Issuance",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    }
                ]
            }
        },
        {
            "sector": "Public Service & Administration",
            "mda": "State Department for Youth Affairs and Creative Economy",
            "category": "Standard Government Services",
            "service": "AGPO Registration",
            "type": "G2C",
            "maturity": 2,
            "complexity": "4-7 steps",
            "description": "Standardized process for AGPO Registration.",
            "bpmn_data": {
                "as_is": [
                    {
                        "name": "(Start",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Complete Form & Attach ID/Reg",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Review Docs",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Ownership & Age 18-35?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Reject Application",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "(End",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Approve Registration",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Generate AGPO Certificate",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Notify Applicant",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Issue Certificate & Update Registry",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ],
                "to_be": [
                    {
                        "name": "Digital Submission",
                        "role": "citizen",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Automated Validation",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Digital Approval",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Electronic Issuance",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    }
                ]
            }
        },
        {
            "sector": "Public Service & Administration",
            "mda": "State Department for Energy (Records Management Unit)",
            "category": "Standard Government Services",
            "service": "Mail Handling",
            "type": "G2C",
            "maturity": 2,
            "complexity": "4-7 steps",
            "description": "Standardized process for Mail Handling.",
            "bpmn_data": {
                "as_is": [
                    {
                        "name": "(Start",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Receive File Request",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Verify Authorization",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Search Index & Locate File",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Found?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Notify Not Found",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "(End",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Record Movement & Log Request",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Issue File & Set Return Date",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Receive Return",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Check Completeness",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Re-shelve & Update Register",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ],
                "to_be": [
                    {
                        "name": "Digital Submission",
                        "role": "citizen",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Automated Validation",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Digital Approval",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Electronic Issuance",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    }
                ]
            }
        },
        {
            "sector": "Public Service & Administration",
            "mda": "Department of Refugee Services",
            "category": "Standard Government Services",
            "service": "Registration",
            "type": "G2C",
            "maturity": 2,
            "complexity": "4-7 steps",
            "description": "Standardized process for Registration.",
            "bpmn_data": {
                "as_is": [
                    {
                        "name": "(From Registration",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Prepare Case File",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Applicant Attends RSD",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Conduct Formal Interview",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Record Detailed Testimony",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Apply Criteria & Assess Credibility",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Recommend Decision to Committee",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Committee Review & Validation",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Final Decision",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Notify Applicant of Grant",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Notify Applicant of Denial",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "(End",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ],
                "to_be": [
                    {
                        "name": "Digital Submission",
                        "role": "citizen",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Automated Validation",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Digital Approval",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Electronic Issuance",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    }
                ]
            }
        },
        {
            "sector": "Interior & National Administration",
            "mda": "Directorate of Immigration Services (Passport Division)",
            "category": "Standard Government Services",
            "service": "First-Time Passport Application",
            "type": "G2C",
            "maturity": 2,
            "complexity": "4-7 steps",
            "description": "Standardized process for First-Time Passport Application.",
            "bpmn_data": {
                "as_is": [
                    {
                        "name": "(Start",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Access e-Citizen Portal",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Complete Form & Upload Docs",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Pay Processing Fee",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "System Validation",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Query IPRS: Verified?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Flag for Manual Review",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Officer Verification",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Schedule Biometric Appointment",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Visit Immigration Office",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Capture Digital Photo",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Capture Fingerprints",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Quality Check OK?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Approval Queue",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Print Passport",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Verify Print Quality",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Notify Applicant for Collection",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Collect Passport & Verify Identity",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "(End",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ],
                "to_be": [
                    {
                        "name": "Digital Submission",
                        "role": "citizen",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Automated Validation",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Digital Approval",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Electronic Issuance",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    }
                ]
            }
        },
        {
            "sector": "Interior & National Administration",
            "mda": "Directorate of Immigration Services (Passport Division)",
            "category": "Standard Government Services",
            "service": "Passport Renewal",
            "type": "G2C",
            "maturity": 2,
            "complexity": "4-7 steps",
            "description": "Standardized process for Passport Renewal.",
            "bpmn_data": {
                "as_is": [
                    {
                        "name": "(Start",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Access e-Citizen Renewal",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Enter Old Passport & Info",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Pay Fee",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Old Passport Valid?",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "gateway"
                    },
                    {
                        "name": "Reject & Refer to Replacement",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "(End",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Visit Office for New Biometrics",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Update Photo & Prints",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Production Queue",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Print New Passport",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Notify for Collection",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    },
                    {
                        "name": "Surrender Old & Issue New",
                        "role": "officer",
                        "type": "manual",
                        "bpmn": "user_task"
                    }
                ],
                "to_be": [
                    {
                        "name": "Digital Submission",
                        "role": "citizen",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Automated Validation",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Digital Approval",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    },
                    {
                        "name": "Electronic Issuance",
                        "role": "system",
                        "type": "api_call",
                        "bpmn": "service_task"
                    }
                ]
            }
        }
    ]
    

    for entry in DATA:
        domain_obj, _ = ServiceDomain.objects.get_or_create(name=entry["sector"])
        cat_obj, _ = ServiceCategory.objects.get_or_create(name=entry["category"], domain=domain_obj)
        mda_obj, _ = MDA.objects.get_or_create(name=entry["mda"])
        
        # Ensure we use a unique svc_code by combining MDA and Service name
        mda_initials = "".join([w[0] for w in entry["mda"].split() if w[0].isalnum()])[:5]
        clean_svc = entry["service"].upper()
        for char in [' ', '&', '(', ')', '/', '-', '.', ',', '\'']:
            clean_svc = clean_svc.replace(char, '_')
        
        svc_code = f"{mda_initials}_{clean_svc}".strip('_')[:40]
        
        # Final check for uniqueness in this run
        base_code = svc_code
        counter = 1
        while ServiceConfig.objects.filter(service_code=svc_code).exists():
            svc_code = f"{base_code[:35]}_{counter}"
            counter += 1

        svc_obj = ServiceConfig.objects.create(
            service_code=svc_code,
            service_name=entry["service"],
            description=entry["description"],
            mda=mda_obj,
            category=cat_obj,
            service_type=entry["type"],
            digitization_level=entry["maturity"],
            delivery_channels=["Web", "Mobile"],
            process_complexity=entry["complexity"],
            catalogue_visible=True,
            service_status='active',
            config={"rules": {"workflow": []}, "output": "Service fulfillment"}
        )
        
        # Add Steps
        for i, step in enumerate(entry["bpmn_data"]["as_is"]):
            WorkflowStep.objects.create(
                service_config=svc_obj,
                step_name=step["name"][:100],
                step_type=step["type"],
                role=step["role"],
                bpmn_element_type=step["bpmn"],
                lifecycle_stage="as_is",
                sequence=i+1
            )
        for i, step in enumerate(entry["bpmn_data"]["to_be"]):
            WorkflowStep.objects.create(
                service_config=svc_obj,
                step_name=step["name"][:100],
                step_type=step["type"],
                role=step["role"],
                bpmn_element_type=step["bpmn"],
                lifecycle_stage="to_be",
                sequence=i+1
            )
        
        print(f"Success: Seeded {entry['service']} from {entry['mda']}.")

    print(f"Total services in DB: {ServiceConfig.objects.count()}")
    print(f"Total workflow steps in DB: {WorkflowStep.objects.count()}")

if __name__ == '__main__':
    force_seed_catalog()
