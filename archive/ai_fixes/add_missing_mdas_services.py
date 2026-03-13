import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, ServiceDomain, ServiceCategory, WorkflowStep

# Complete MDA and Service data from Government_Service_Catalogue.md
NEW_MDAS_WITH_SERVICES = [
    {
        "mda": {
            "name": "State Department for Correctional Services",
            "code": "SDCS",
            "description": "Safe custody & inmate management and rehabilitation services",
            "head": "Principal Secretary",
            "email": "ps@correctional.go.ke",
            "phone": "+254-20-2211120",
            "website": "https://www.correctional.go.ke"
        },
        "services": [
            {
                "code": "SDCS-001",
                "name": "Safe Custody & Inmate Management",
                "category": "Correctional Services",
                "domain": "Ministry of Interior and National Administration",
                "type": "Internal",
                "maturity": 3,
                "channels": ["In-person"],
                "complexity": "Simple",
                "pain_points": ["Manual forms", "Paper-based files", "Lack of system integration"]
            },
            {
                "code": "SDCS-002",
                "name": "Inmate Rehabilitation & Welfare Services",
                "category": "Correctional Services",
                "domain": "Ministry of Interior and National Administration",
                "type": "Internal",
                "maturity": 3,
                "channels": ["In-person", "Contact Centre"],
                "complexity": "Complex",
                "pain_points": ["Manual forms", "Paper-based files"]
            }
        ]
    },
    {
        "mda": {
            "name": "State Department for Housing and Urban Development",
            "code": "SDHUD",
            "description": "Housing and urban development services",
            "head": "Principal Secretary",
            "email": "ps@housing.go.ke",
            "phone": "+254-20-2211120",
            "website": "https://www.housing.go.ke"
        },
        "services": [
            {
                "code": "SDHUD-001",
                "name": "Civil Servant Rent Payment System",
                "category": "Housing Services",
                "domain": "Ministry of Lands, Housing and Urban Development",
                "type": "C2G",
                "maturity": 2,
                "channels": ["Mobile App", "USSD"],
                "complexity": "Moderate",
                "pain_points": ["Paper-based files"]
            },
            {
                "code": "SDHUD-002",
                "name": "Housing Inventory Management Register",
                "category": "Housing Services",
                "domain": "Ministry of Lands, Housing and Urban Development",
                "type": "C2G",
                "maturity": 1,
                "channels": ["Mobile App", "USSD"],
                "complexity": "Simple",
                "pain_points": ["Manual forms"]
            },
            {
                "code": "SDHUD-003",
                "name": "Housing Maintenance Management",
                "category": "Housing Services",
                "domain": "Ministry of Lands, Housing and Urban Development",
                "type": "C2G",
                "maturity": 1,
                "channels": ["In-person"],
                "complexity": "Simple",
                "pain_points": ["Manual forms"]
            },
            {
                "code": "SDHUD-004",
                "name": "Civil Servants Housing Scheme Management",
                "category": "Housing Services",
                "domain": "Ministry of Lands, Housing and Urban Development",
                "type": "C2G",
                "maturity": 2,
                "channels": ["In-person", "USSD"],
                "complexity": "Moderate",
                "pain_points": ["Manual forms", "Paper-based files"]
            },
            {
                "code": "SDHUD-005",
                "name": "Slum Upgrading Housing Management",
                "category": "Housing Services",
                "domain": "Ministry of Lands, Housing and Urban Development",
                "type": "C2G",
                "maturity": 2,
                "channels": ["Web", "Mobile App"],
                "complexity": "Simple",
                "pain_points": []
            }
        ]
    },
    {
        "mda": {
            "name": "State Department for Medical Services",
            "code": "SDMS",
            "description": "Medical services and health records management",
            "head": "Principal Secretary",
            "email": "ps@health.go.ke",
            "phone": "+254-20-2717077",
            "website": "https://www.health.go.ke"
        },
        "services": [
            {
                "code": "SDMS-001",
                "name": "Health Records Management",
                "category": "Health Services",
                "domain": "Ministry of Health",
                "type": "C2G",
                "maturity": 1,
                "channels": ["In-person", "Web"],
                "complexity": "Complex",
                "pain_points": ["Manual forms", "Paper-based files", "Lack of system integration"]
            }
        ]
    },
    {
        "mda": {
            "name": "State Department for Broadcasting and Telecommunications",
            "code": "SDBT",
            "description": "Broadcasting and telecommunications regulation",
            "head": "Principal Secretary",
            "email": "ps@broadcasting.go.ke",
            "phone": "+254-20-2211120",
            "website": "https://www.broadcasting.go.ke"
        },
        "services": [
            {
                "code": "SDBT-001",
                "name": "KNA Office Space Leasing",
                "category": "Administrative Services",
                "domain": "Ministry of ICT Innovation and Digital Economy",
                "type": "C2G",
                "maturity": 3,
                "channels": ["USSD"],
                "complexity": "Moderate",
                "pain_points": ["Manual forms", "Lack of system integration"]
            },
            {
                "code": "SDBT-002",
                "name": "Sale of Historical and Current Photos",
                "category": "Information Services",
                "domain": "Ministry of ICT Innovation and Digital Economy",
                "type": "C2G",
                "maturity": 1,
                "channels": ["In-person"],
                "complexity": "Simple",
                "pain_points": ["Manual forms", "Slow approvals", "Paper-based files"]
            }
        ]
    },
    {
        "mda": {
            "name": "State Department for Public Works",
            "code": "SDPW",
            "description": "Public works and infrastructure development",
            "head": "Principal Secretary",
            "email": "ps@publicworks.go.ke",
            "phone": "+254-20-2211120",
            "website": "https://www.publicworks.go.ke"
        },
        "services": [
            {
                "code": "SDPW-001",
                "name": "Pre-Construction of Built Environment",
                "category": "Infrastructure Services",
                "domain": "Ministry of Roads and Transport",
                "type": "G2G",
                "maturity": 4,
                "channels": ["In-person"],
                "complexity": "Complex",
                "pain_points": ["Manual forms", "Slow approvals", "Paper-based files"]
            }
        ]
    },
    {
        "mda": {
            "name": "State Department for Science, Research and Innovation",
            "code": "SDSRI",
            "description": "Promotion of science, research and innovation",
            "head": "Principal Secretary",
            "email": "ps@research.go.ke",
            "phone": "+254-20-2211120",
            "website": "https://www.research.go.ke"
        },
        "services": [
            {
                "code": "SDSRI-001",
                "name": "Science Research and Innovation Promotion",
                "category": "Research Services",
                "domain": "Ministry of Education",
                "type": "G2G",
                "maturity": 1,
                "channels": ["In-person", "Web"],
                "complexity": "Complex",
                "pain_points": ["Manual forms", "Slow approvals", "High error rate"]
            }
        ]
    },
    # Water Works Development Agencies
    {
        "mda": {
            "name": "Athi Water Works Development Agency",
            "code": "AWWDA",
            "description": "Water infrastructure development in Athi region",
            "head": "Chief Executive Officer",
            "email": "info@awwda.go.ke",
            "phone": "+254-20-2211120",
            "website": "https://www.awwda.go.ke"
        },
        "services": [
            {
                "code": "AWWDA-001",
                "name": "Water Infrastructure Development",
                "category": "Water Services",
                "domain": "Ministry of Water, Sanitation and Irrigation",
                "type": "G2C",
                "maturity": 2,
                "channels": ["In-person", "Web"],
                "complexity": "Complex",
                "pain_points": ["Manual forms", "Slow approvals", "Dependency on other MDAs"]
            },
            {
                "code": "AWWDA-002",
                "name": "Water Project Management",
                "category": "Water Services",
                "domain": "Ministry of Water, Sanitation and Irrigation",
                "type": "G2G",
                "maturity": 2,
                "channels": ["In-person"],
                "complexity": "Complex",
                "pain_points": ["Paper-based files", "Lack of system integration"]
            }
        ]
    },
    {
        "mda": {
            "name": "Tana Water Works Development Agency",
            "code": "TWWDA",
            "description": "Water infrastructure development in Tana region",
            "head": "Chief Executive Officer",
            "email": "info@twwda.go.ke",
            "phone": "+254-20-2211120",
            "website": "https://www.twwda.go.ke"
        },
        "services": [
            {
                "code": "TWWDA-001",
                "name": "Water Infrastructure Development",
                "category": "Water Services",
                "domain": "Ministry of Water, Sanitation and Irrigation",
                "type": "G2C",
                "maturity": 2,
                "channels": ["In-person", "Web"],
                "complexity": "Complex",
                "pain_points": ["Manual forms", "Slow approvals"]
            }
        ]
    },
    # Transport and Infrastructure
    {
        "mda": {
            "name": "Kenya Airports Authority",
            "code": "KAA",
            "description": "Airport management and operations",
            "head": "Managing Director",
            "email": "info@kaa.go.ke",
            "phone": "+254-20-6661000",
            "website": "https://www.kaa.go.ke"
        },
        "services": [
            {
                "code": "KAA-001",
                "name": "Airport Landing Permits",
                "category": "Aviation Services",
                "domain": "Ministry of Roads and Transport",
                "type": "B2G",
                "maturity": 3,
                "channels": ["Web", "In-person"],
                "complexity": "Moderate",
                "pain_points": ["Slow approvals"]
            },
            {
                "code": "KAA-002",
                "name": "Airport Parking Services",
                "category": "Aviation Services",
                "domain": "Ministry of Roads and Transport",
                "type": "C2G",
                "maturity": 3,
                "channels": ["Mobile App", "In-person"],
                "complexity": "Simple",
                "pain_points": []
            }
        ]
    },
    {
        "mda": {
            "name": "Kenya Ports Authority",
            "code": "KPA",
            "description": "Port management and operations",
            "head": "Managing Director",
            "email": "info@kpa.co.ke",
            "phone": "+254-41-3491200",
            "website": "https://www.kpa.co.ke"
        },
        "services": [
            {
                "code": "KPA-001",
                "name": "Port Clearance Services",
                "category": "Maritime Services",
                "domain": "Ministry of Roads and Transport",
                "type": "B2G",
                "maturity": 3,
                "channels": ["Web", "In-person"],
                "complexity": "Complex",
                "pain_points": ["Manual forms", "Dependency on other MDAs"]
            },
            {
                "code": "KPA-002",
                "name": "Cargo Handling Services",
                "category": "Maritime Services",
                "domain": "Ministry of Roads and Transport",
                "type": "B2G",
                "maturity": 3,
                "channels": ["Web"],
                "complexity": "Complex",
                "pain_points": ["Lack of system integration"]
            }
        ]
    },
    {
        "mda": {
            "name": "Kenya Railways Corporation",
            "code": "KRC",
            "description": "Railway services and operations",
            "head": "Managing Director",
            "email": "info@krc.co.ke",
            "phone": "+254-20-2211120",
            "website": "https://www.krc.co.ke"
        },
        "services": [
            {
                "code": "KRC-001",
                "name": "Passenger Train Booking",
                "category": "Railway Services",
                "domain": "Ministry of Roads and Transport",
                "type": "C2G",
                "maturity": 3,
                "channels": ["Web", "Mobile App", "In-person"],
                "complexity": "Simple",
                "pain_points": []
            },
            {
                "code": "KRC-002",
                "name": "Freight Transport Services",
                "category": "Railway Services",
                "domain": "Ministry of Roads and Transport",
                "type": "B2G",
                "maturity": 2,
                "channels": ["In-person", "Web"],
                "complexity": "Moderate",
                "pain_points": ["Manual forms"]
            }
        ]
    },
    {
        "mda": {
            "name": "National Construction Authority",
            "code": "NCA",
            "description": "Construction industry regulation and contractor registration",
            "head": "Executive Director",
            "email": "info@nca.go.ke",
            "phone": "+254-20-2211120",
            "website": "https://www.nca.go.ke"
        },
        "services": [
            {
                "code": "NCA-001",
                "name": "Contractor Registration",
                "category": "Construction Regulation",
                "domain": "Ministry of Lands, Housing and Urban Development",
                "type": "B2G",
                "maturity": 3,
                "channels": ["Web", "In-person"],
                "complexity": "Moderate",
                "pain_points": ["Manual forms", "Slow approvals"]
            },
            {
                "code": "NCA-002",
                "name": "Construction Permit Approval",
                "category": "Construction Regulation",
                "domain": "Ministry of Lands, Housing and Urban Development",
                "type": "B2G",
                "maturity": 2,
                "channels": ["In-person", "Web"],
                "complexity": "Complex",
                "pain_points": ["Slow approvals", "Dependency on other MDAs"]
            }
        ]
    },
    {
        "mda": {
            "name": "National Land Commission",
            "code": "NLC",
            "description": "Land administration and management",
            "head": "Chairperson",
            "email": "info@landcommission.go.ke",
            "phone": "+254-20-2718050",
            "website": "https://www.landcommission.go.ke"
        },
        "services": [
            {
                "code": "NLC-001",
                "name": "Public Land Management",
                "category": "Land Services",
                "domain": "Ministry of Lands, Housing and Urban Development",
                "type": "G2G",
                "maturity": 2,
                "channels": ["In-person", "Web"],
                "complexity": "Complex",
                "pain_points": ["Manual forms", "Paper-based files", "Slow approvals"]
            },
            {
                "code": "NLC-002",
                "name": "Land Dispute Resolution",
                "category": "Land Services",
                "domain": "Ministry of Lands, Housing and Urban Development",
                "type": "C2G",
                "maturity": 2,
                "channels": ["In-person"],
                "complexity": "Complex",
                "pain_points": ["Manual forms", "Slow approvals", "Lack of system integration"]
            }
        ]
    }
]

if __name__ == "__main__":
    print("=" * 80)
    print("ADDING MISSING MDAs AND SERVICES")
    print("=" * 80)

    added_mdas = 0
    added_services = 0

    for entry in NEW_MDAS_WITH_SERVICES:
        mda_data = entry["mda"]
        
        # Check if MDA already exists
        existing_mda = MDA.objects.filter(code=mda_data["code"]).first()
        
        if existing_mda:
            print(f"\n⚠️  MDA already exists: {mda_data['name']} ({mda_data['code']})")
            mda = existing_mda
        else:
            # Create MDA
            mda = MDA.objects.create(
                name=mda_data["name"],
                code=mda_data["code"],
                description=mda_data["description"],
                head_of_mda=mda_data.get("head", ""),
                contact_email=mda_data.get("email", ""),
                contact_phone=mda_data.get("phone", ""),
                website=mda_data.get("website", "")
            )
            added_mdas += 1
            print(f"\n✓ Added MDA: {mda.name} ({mda.code})")
        
        # Add services
        for svc_data in entry["services"]:
            # Get or create domain
            domain, _ = ServiceDomain.objects.get_or_create(
                name=svc_data["domain"]
            )
            
            # Get or create category
            category, _ = ServiceCategory.objects.get_or_create(
                name=svc_data["category"],
                domain=domain
            )
            
            # Check if service already exists
            existing_service = ServiceConfig.objects.filter(
                service_code=svc_data["code"]
            ).first()
            
            if existing_service:
                print(f"  ⚠️  Service exists: {svc_data['name']}")
            else:
                # Create service
                service = ServiceConfig.objects.create(
                    service_code=svc_data["code"],
                    service_name=svc_data["name"],
                    mda=mda,
                    category=category,
                    service_type=svc_data["type"],
                    digitization_level=svc_data["maturity"],
                    delivery_channels=svc_data["channels"],
                    process_complexity=svc_data["complexity"],
                    pain_points=svc_data["pain_points"],
                    service_status='active',
                    catalogue_visible=True
                )
                
                # Add basic workflow
                WorkflowStep.objects.create(
                    service_config=service,
                    step_name="Citizen Application",
                    step_type="manual",
                    bpmn_element_type="start_event",
                    lifecycle_stage="to_be",
                    role="citizen",
                    sequence=1,
                    action="submit"
                )
                WorkflowStep.objects.create(
                    service_config=service,
                    step_name="Officer Processing",
                    step_type="manual",
                    bpmn_element_type="user_task",
                    lifecycle_stage="to_be",
                    role="officer",
                    sequence=2,
                    action="process"
                )
                WorkflowStep.objects.create(
                    service_config=service,
                    step_name="Service Delivery",
                    step_type="manual",
                    bpmn_element_type="end_event",
                    lifecycle_stage="to_be",
                    role="system",
                    sequence=3,
                    action="complete"
                )
                
                added_services += 1
                print(f"  ✓ Added service: {svc_data['name']}")

    print(f"\n{'=' * 80}")
    print(f"SUMMARY:")
    print(f"  MDAs added: {added_mdas}")
    print(f"  Services added: {added_services}")
    print(f"{'=' * 80}")
