import os
import django
import json

# Set up Django environment targeting Docker DB
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.host_settings')
django.setup()

from service_api.models import ServiceConfig

def seed_schemas():
    print("--- SEEDING FORM SCHEMAS FOR PILOT SERVICES ---")

    # 1. Passport Application
    passport_schema = {
        "rules": {
            "schema": {
                "type": "object",
                "required": ["full_name", "id_number", "passport_type", "birth_cert_no"],
                "properties": {
                    "header_1": {"type": "section_header", "title": "Section 1: Personal Identity", "description": "Information as per National ID"},
                    "full_name": {"type": "string", "title": "Full Name", "description": "As it appears on your ID"},
                    "id_number": {
                        "type": "string", 
                        "title": "National ID Number", 
                        "lookup_service": "IPRS", 
                        "lookup_action": "get_person_details"
                    },
                    "gender": {"type": "string", "title": "Gender", "enum": ["Male", "Female", "Other"]},
                    "header_2": {"type": "section_header", "title": "Section 2: Birth & Citizenship", "description": "Verification of Kenyan Citizenship"},
                    "birth_cert_no": {
                        "type": "string", 
                        "title": "Birth Certificate Number",
                        "lookup_service": "CRS",
                        "lookup_action": "verify_birth"
                    },
                    "county_of_birth": {"type": "string", "title": "County of Birth"},
                    "header_3": {"type": "section_header", "title": "Section 3: Passport Configuration", "description": "Choose your booklet size"},
                    "passport_type": {
                        "type": "string", 
                        "title": "Booklet Size", 
                        "enum": ["Ordinary A (32 Pages) - Ksh 4,500", "Ordinary B (48 Pages) - Ksh 6,000", "Ordinary C (64 Pages) - Ksh 7,500", "Diplomatic - Ksh 7,500"]
                    },
                    "header_4": {"type": "section_header", "title": "Section 4: Digital Uploads", "description": "Clear scans required"},
                    "photo": {"type": "string", "format": "data-url", "title": "Passport Size Photo"},
                    "id_scan": {"type": "string", "format": "data-url", "title": "Scan of National ID"}
                }
            }
        }
    }

    # 2. Birth Registration
    birth_reg_schema = {
        "rules": {
            "schema": {
                "type": "object",
                "required": ["child_name", "mother_id", "date_of_birth"],
                "properties": {
                    "header_1": {"type": "section_header", "title": "Child Information"},
                    "child_name": {"type": "string", "title": "Full Name of Child"},
                    "gender": {"type": "string", "title": "Gender", "enum": ["Male", "Female"]},
                    "date_of_birth": {"type": "string", "format": "date", "title": "Date of Birth"},
                    "hospital_name": {"type": "string", "title": "Health Facility / Hospital"},
                    "header_2": {"type": "section_header", "title": "Parental Information"},
                    "mother_id": {
                        "type": "string", 
                        "title": "Mother's ID Number",
                        "lookup_service": "IPRS",
                        "lookup_action": "get_person_details"
                    },
                    "father_id": {
                        "type": "string", 
                        "title": "Father's ID Number",
                        "lookup_service": "IPRS",
                        "lookup_action": "get_person_details"
                    }
                }
            }
        }
    }

    # 3. Hustler Fund
    hustler_schema = {
        "rules": {
            "schema": {
                "type": "object",
                "required": ["loan_amount", "terms_accepted"],
                "properties": {
                    "header_1": {"type": "section_header", "title": "Loan Application"},
                    "id_number": {"type": "string", "title": "ID Number", "lookup_service": "IPRS"},
                    "phone_number": {"type": "string", "title": "Phone Number", "lookup_service": "TELCO"},
                    "loan_amount": {
                        "type": "string", 
                        "title": "Requested Amount (Ksh)",
                        "enum": ["500", "1,000", "2,000", "5,000", "10,000", "20,000", "50,000"]
                    },
                    "purpose": {"type": "string", "title": "Purpose of Loan", "enum": ["Business Input", "School Fees", "Emergency", "Agriculture", "Other"]},
                    "terms_accepted": {"type": "boolean", "title": "I accept the Hustler Fund Terms & Conditions"}
                }
            }
        }
    }

    # 4. AGPO Registration
    agpo_schema = {
        "rules": {
            "schema": {
                "type": "object",
                "required": ["business_name", "kra_pin", "agpo_category"],
                "properties": {
                    "header_1": {"type": "section_header", "title": "Business Details"},
                    "business_name": {"type": "string", "title": "Registered Business Name"},
                    "kra_pin": {"type": "string", "title": "KRA PIN", "lookup_service": "KRA"},
                    "registration_number": {"type": "string", "title": "Business Registration No (BN/PV)"},
                    "header_2": {"type": "section_header", "title": "Target Group"},
                    "agpo_category": {
                        "type": "string", 
                        "title": "AGPO Category",
                        "enum": ["Women", "Youth", "Persons with Disability"]
                    }
                }
            }
        }
    }

    # 5. Planning (AWWDA)
    planning_schema = {
        "rules": {
            "schema": {
                "type": "object",
                "required": ["project_name", "location", "budget"],
                "properties": {
                    "header_1": {"type": "section_header", "title": "Project Overview"},
                    "project_name": {"type": "string", "title": "Project / Development Name"},
                    "location": {"type": "string", "title": "Specific Location (LR No / Area)"},
                    "project_type": {"type": "string", "enum": ["Residential", "Commercial", "Industrial", "Public Utility"]},
                    "budget": {"type": "number", "title": "Estimated Budget (Ksh)"},
                    "header_2": {"type": "section_header", "title": "Timeline"},
                    "start_date": {"type": "string", "format": "date", "title": "Proposed Start Date"}
                }
            }
        }
    }

    # 6. Qualification Validation (KNQA)
    knqa_schema = {
        "rules": {
            "schema": {
                "type": "object",
                "required": ["institution_name", "qualification_name", "year_obtained"],
                "properties": {
                    "header_1": {"type": "section_header", "title": "Institution Details"},
                    "institution_name": {"type": "string", "title": "Name of Awarding Institution", "lookup_service": "KNQA_REGISTRY"},
                    "qualification_type": {"type": "string", "enum": ["Degree", "Diploma", "Certificate", "PHD", "Masters"]},
                    "qualification_name": {"type": "string", "title": "Exact Title of Qualification"},
                    "year_obtained": {"type": "number", "title": "Year Applied/Obtained"},
                    "header_2": {"type": "section_header", "title": "Identity Mapping"},
                    "id_number": {"type": "string", "title": "ID Number as on Certificate", "lookup_service": "IPRS"}
                }
            }
        }
    }

    # Generic Schema for everything else
    def get_generic_schema(name):
        return {
            "rules": {
                "schema": {
                    "type": "object",
                    "required": ["full_name", "id_number", "details"],
                    "properties": {
                        "header_1": {"type": "section_header", "title": "Applicant Information"},
                        "full_name": {"type": "string", "title": "Full Legal Name"},
                        "id_number": {"type": "string", "title": "National ID Number", "lookup_service": "IPRS"},
                        "header_2": {"type": "section_header", "title": "Service Details", "description": f"Information for {name}"},
                        "details": {"type": "string", "format": "textarea", "title": "Request / Application Details"},
                        "supporting_doc": {"type": "string", "format": "data-url", "title": "Supporting Document (PDF/JPG)"}
                    }
                }
            }
        }

    # Apply Schemas
    mappings = [
        ("passport", passport_schema),
        ("birth registration", birth_reg_schema),
        ("hustler fund", hustler_schema),
        ("agpo", agpo_schema),
        ("planning", planning_schema),
        ("qualification validation", knqa_schema),
    ]

    services = ServiceConfig.objects.all()
    count = 0
    for svc in services:
        applied = False
        for keyword, schema in mappings:
            if keyword.lower() in svc.service_name.lower():
                svc.config = schema
                svc.save()
                print(f"  [Mapped] {svc.service_name} -> {keyword} schema")
                applied = True
                count += 1
                break
        
        if not applied:
            # Check if it was one of the 21 BP pilot ones (they usually have descriptions or specific MDAs)
            # Actually, let's just apply generic to all that don't have one yet
            # but only if they are 'active'
            if not svc.config or 'rules' not in svc.config:
                svc.config = get_generic_schema(svc.service_name)
                svc.save()
                print(f"  [Generic] {svc.service_name}")
                count += 1

    print(f"--- COMPLETE: Configured forms for {count} services ---")

if __name__ == '__main__':
    seed_schemas()
