import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig

# Form schemas for each service
FORM_SCHEMAS = {
    "MOE": {
        "title": "Scholarship & Bursary Application",
        "description": "Apply for government scholarships and bursaries",
        "fields": [
            {
                "name": "applicant_name",
                "label": "Full Name",
                "type": "text",
                "required": True,
                "validation": {"minLength": 3, "maxLength": 100}
            },
            {
                "name": "id_number",
                "label": "National ID Number",
                "type": "text",
                "required": True,
                "validation": {"pattern": "^[0-9]{8}$"}
            },
            {
                "name": "phone",
                "label": "Phone Number",
                "type": "tel",
                "required": True,
                "validation": {"pattern": "^\\+254[0-9]{9}$"}
            },
            {
                "name": "email",
                "label": "Email Address",
                "type": "email",
                "required": True
            },
            {
                "name": "institution",
                "label": "Educational Institution",
                "type": "text",
                "required": True
            },
            {
                "name": "course",
                "label": "Course of Study",
                "type": "text",
                "required": True
            },
            {
                "name": "level",
                "label": "Level of Study",
                "type": "select",
                "required": True,
                "options": [
                    {"value": "certificate", "label": "Certificate"},
                    {"value": "diploma", "label": "Diploma"},
                    {"value": "degree", "label": "Undergraduate Degree"},
                    {"value": "masters", "label": "Masters"},
                    {"value": "phd", "label": "PhD"}
                ]
            },
            {
                "name": "year_of_study",
                "label": "Year of Study",
                "type": "number",
                "required": True,
                "validation": {"min": 1, "max": 7}
            },
            {
                "name": "family_income",
                "label": "Annual Family Income (KES)",
                "type": "number",
                "required": True
            },
            {
                "name": "admission_letter",
                "label": "Admission Letter",
                "type": "file",
                "required": True,
                "validation": {"accept": ".pdf,.jpg,.png", "maxSize": 5242880}
            },
            {
                "name": "fee_structure",
                "label": "Fee Structure",
                "type": "file",
                "required": True,
                "validation": {"accept": ".pdf", "maxSize": 2097152}
            },
            {
                "name": "id_copy",
                "label": "Copy of National ID",
                "type": "file",
                "required": True,
                "validation": {"accept": ".pdf,.jpg,.png", "maxSize": 2097152}
            }
        ]
    },
    "DIS": {
        "title": "Passport Application",
        "description": "Apply for a new Kenyan passport",
        "fields": [
            {
                "name": "application_type",
                "label": "Application Type",
                "type": "select",
                "required": True,
                "options": [
                    {"value": "new", "label": "New Passport"},
                    {"value": "renewal", "label": "Renewal"},
                    {"value": "replacement", "label": "Replacement (Lost/Damaged)"}
                ]
            },
            {
                "name": "passport_type",
                "label": "Passport Type",
                "type": "select",
                "required": True,
                "options": [
                    {"value": "ordinary_32", "label": "Ordinary (32 pages)"},
                    {"value": "ordinary_48", "label": "Ordinary (48 pages)"},
                    {"value": "ordinary_64", "label": "Ordinary (64 pages)"}
                ]
            },
            {
                "name": "full_name",
                "label": "Full Name (as per ID)",
                "type": "text",
                "required": True,
                "validation": {"minLength": 3, "maxLength": 100}
            },
            {
                "name": "id_number",
                "label": "National ID Number",
                "type": "text",
                "required": True,
                "validation": {"pattern": "^[0-9]{8}$"}
            },
            {
                "name": "birth_entry_number",
                "label": "Birth Entry Number (BEN)",
                "type": "text",
                "required": True,
                "lookup_service": "CRS",
                "lookup_action": "fetch",
                "description": "Enter BEN from your Birth Certificate"
            },
            {
                "name": "date_of_birth",
                "label": "Date of Birth",
                "type": "date",
                "required": True
            },
            {
                "name": "place_of_birth",
                "label": "Place of Birth",
                "type": "text",
                "required": True
            },
            {
                "name": "gender",
                "label": "Gender",
                "type": "select",
                "required": True,
                "options": [
                    {"value": "male", "label": "Male"},
                    {"value": "female", "label": "Female"}
                ]
            },
            {
                "name": "phone",
                "label": "Phone Number",
                "type": "tel",
                "required": True,
                "validation": {"pattern": "^\\+254[0-9]{9}$"}
            },
            {
                "name": "email",
                "label": "Email Address",
                "type": "email",
                "required": True
            },
            {
                "name": "postal_address",
                "label": "Postal Address",
                "type": "text",
                "required": True
            },
            {
                "name": "physical_address",
                "label": "Physical Address",
                "type": "textarea",
                "required": True
            },
            {
                "name": "occupation",
                "label": "Occupation",
                "type": "text",
                "required": True
            },
            {
                "name": "id_copy",
                "label": "Copy of National ID",
                "type": "file",
                "required": True,
                "validation": {"accept": ".pdf,.jpg,.png", "maxSize": 2097152}
            },
            {
                "name": "birth_certificate",
                "label": "Birth Certificate",
                "type": "file",
                "required": True,
                "validation": {"accept": ".pdf,.jpg,.png", "maxSize": 2097152}
            },
            {
                "name": "passport_photo",
                "label": "Passport Photo",
                "type": "file",
                "required": True,
                "validation": {"accept": ".jpg,.png", "maxSize": 1048576}
            },
            {
                "name": "old_passport",
                "label": "Old Passport (if renewal)",
                "type": "file",
                "required": False,
                "validation": {"accept": ".pdf,.jpg,.png", "maxSize": 2097152}
            }
        ]
    },
    "SDSRI": {
        "title": "Research & Innovation Grant Application",
        "description": "Apply for research and innovation funding",
        "fields": [
            {
                "name": "project_title",
                "label": "Project Title",
                "type": "text",
                "required": True,
                "validation": {"minLength": 10, "maxLength": 200}
            },
            {
                "name": "principal_investigator",
                "label": "Principal Investigator Name",
                "type": "text",
                "required": True
            },
            {
                "name": "id_number",
                "label": "ID Number",
                "type": "text",
                "required": True,
                "validation": {"pattern": "^[0-9]{8}$"}
            },
            {
                "name": "phone",
                "label": "Phone Number",
                "type": "tel",
                "required": True,
                "validation": {"pattern": "^\\+254[0-9]{9}$"}
            },
            {
                "name": "email",
                "label": "Email Address",
                "type": "email",
                "required": True
            },
            {
                "name": "institution",
                "label": "Institution/Organization",
                "type": "text",
                "required": True
            },
            {
                "name": "research_area",
                "label": "Research Area",
                "type": "select",
                "required": True,
                "options": [
                    {"value": "agriculture", "label": "Agriculture & Food Security"},
                    {"value": "health", "label": "Health & Medicine"},
                    {"value": "energy", "label": "Energy & Environment"},
                    {"value": "ict", "label": "ICT & Digital Innovation"},
                    {"value": "manufacturing", "label": "Manufacturing & Industry"},
                    {"value": "education", "label": "Education"},
                    {"value": "other", "label": "Other"}
                ]
            },
            {
                "name": "project_summary",
                "label": "Project Summary",
                "type": "textarea",
                "required": True,
                "validation": {"minLength": 100, "maxLength": 500}
            },
            {
                "name": "duration_months",
                "label": "Project Duration (months)",
                "type": "number",
                "required": True,
                "validation": {"min": 6, "max": 36}
            },
            {
                "name": "budget_requested",
                "label": "Budget Requested (KES)",
                "type": "number",
                "required": True,
                "validation": {"min": 100000, "max": 50000000}
            },
            {
                "name": "proposal_document",
                "label": "Full Proposal Document",
                "type": "file",
                "required": True,
                "validation": {"accept": ".pdf", "maxSize": 10485760}
            },
            {
                "name": "budget_breakdown",
                "label": "Detailed Budget Breakdown",
                "type": "file",
                "required": True,
                "validation": {"accept": ".pdf,.xlsx", "maxSize": 5242880}
            },
            {
                "name": "cv",
                "label": "Principal Investigator CV",
                "type": "file",
                "required": True,
                "validation": {"accept": ".pdf", "maxSize": 2097152}
            }
        ]
    },
    "AWWDA": {
        "title": "Water Infrastructure Project Application",
        "description": "Apply for water infrastructure development project",
        "fields": [
            {
                "name": "project_name",
                "label": "Project Name",
                "type": "text",
                "required": True,
                "validation": {"minLength": 10, "maxLength": 200}
            },
            {
                "name": "applicant_type",
                "label": "Applicant Type",
                "type": "select",
                "required": True,
                "options": [
                    {"value": "county", "label": "County Government"},
                    {"value": "wsp", "label": "Water Service Provider"},
                    {"value": "community", "label": "Community Organization"},
                    {"value": "private", "label": "Private Entity"}
                ]
            },
            {
                "name": "organization_name",
                "label": "Organization Name",
                "type": "text",
                "required": True
            },
            {
                "name": "contact_person",
                "label": "Contact Person",
                "type": "text",
                "required": True
            },
            {
                "name": "phone",
                "label": "Phone Number",
                "type": "tel",
                "required": True,
                "validation": {"pattern": "^\\+254[0-9]{9}$"}
            },
            {
                "name": "email",
                "label": "Email Address",
                "type": "email",
                "required": True
            },
            {
                "name": "project_location",
                "label": "Project Location",
                "type": "text",
                "required": True
            },
            {
                "name": "county",
                "label": "County",
                "type": "select",
                "required": True,
                "options": [
                    {"value": "nairobi", "label": "Nairobi"},
                    {"value": "kiambu", "label": "Kiambu"},
                    {"value": "machakos", "label": "Machakos"},
                    {"value": "kajiado", "label": "Kajiado"},
                    {"value": "murang'a", "label": "Murang'a"}
                ]
            },
            {
                "name": "project_type",
                "label": "Project Type",
                "type": "select",
                "required": True,
                "options": [
                    {"value": "dam", "label": "Dam Construction"},
                    {"value": "borehole", "label": "Borehole Drilling"},
                    {"value": "pipeline", "label": "Pipeline Extension"},
                    {"value": "treatment", "label": "Water Treatment Plant"},
                    {"value": "rehabilitation", "label": "Infrastructure Rehabilitation"}
                ]
            },
            {
                "name": "beneficiaries",
                "label": "Estimated Beneficiaries",
                "type": "number",
                "required": True,
                "validation": {"min": 100}
            },
            {
                "name": "project_cost",
                "label": "Estimated Project Cost (KES)",
                "type": "number",
                "required": True,
                "validation": {"min": 1000000}
            },
            {
                "name": "project_description",
                "label": "Project Description",
                "type": "textarea",
                "required": True,
                "validation": {"minLength": 100, "maxLength": 1000}
            },
            {
                "name": "feasibility_study",
                "label": "Feasibility Study Report",
                "type": "file",
                "required": True,
                "validation": {"accept": ".pdf", "maxSize": 10485760}
            },
            {
                "name": "technical_drawings",
                "label": "Technical Drawings",
                "type": "file",
                "required": True,
                "validation": {"accept": ".pdf,.dwg", "maxSize": 20971520}
            },
            {
                "name": "environmental_impact",
                "label": "Environmental Impact Assessment",
                "type": "file",
                "required": True,
                "validation": {"accept": ".pdf", "maxSize": 10485760}
            },
            {
                "name": "registration_certificate",
                "label": "Organization Registration Certificate",
                "type": "file",
                "required": True,
                "validation": {"accept": ".pdf,.jpg,.png", "maxSize": 2097152}
            }
        ]
    },
    "BIRTH_REG": {
        "title": "Birth Registration & Certificate",
        "description": "Root identity registration. Standalone service.",
        "fields": [
            {"name": "child_name", "label": "Child's Full Name", "type": "text", "required": True},
            {"name": "date_of_birth", "label": "Date of Birth", "type": "date", "required": True},
            {"name": "gender", "label": "Gender", "type": "select", "required": True, "options": [{"value": "male", "label": "Male"}, {"value": "female", "label": "Female"}]},
            {"name": "mother_id", "label": "Mother's ID Number", "type": "text", "required": True, "lookup_service": "IPRS", "lookup_action": "fetch"},
            {"name": "mother_name", "label": "Mother's Full Name", "type": "text", "required": True, "read_only": True},
            {"name": "father_id", "label": "Father's ID Number", "type": "text", "required": False, "lookup_service": "IPRS", "lookup_action": "fetch"},
            {"name": "father_name", "label": "Father's Full Name", "type": "text", "required": False, "read_only": True}
        ]
    },
    "NEMIS": {
        "title": "School Enrollment (NEMIS Registration)",
        "description": "Requires prior Birth Registration.",
        "fields": [
            {"name": "birth_entry_number", "label": "Birth Entry Number (BEN)", "type": "text", "required": True, "lookup_service": "CRS", "lookup_action": "fetch", "description": "Fetches data from Birth Registry"},
            {"name": "full_name", "label": "Full Name", "type": "text", "required": True, "read_only": True},
            {"name": "date_of_birth", "label": "Date of Birth", "type": "date", "required": True, "read_only": True},
            {"name": "gender", "label": "Gender", "type": "text", "required": True, "read_only": True},
            {"name": "school_name", "label": "Target School Name", "type": "text", "required": True}
        ]
    },
    "NRB": {
        "title": "National ID Registration",
        "description": "Requires Birth Certificate + NEMIS Enrollment.",
        "fields": [
            {"name": "birth_entry_number", "label": "Birth Entry Number (BEN)", "type": "text", "required": True, "lookup_service": "CRS", "lookup_action": "fetch"},
            {"name": "nemis_upi", "label": "NEMIS UPI / Admission No", "type": "text", "required": True, "lookup_service": "NEMIS", "lookup_action": "validate_admission"},
            {"name": "full_name", "label": "Full Name", "type": "text", "required": True, "read_only": True},
            {"name": "date_of_birth", "label": "Date of Birth", "type": "date", "required": True, "read_only": True},
            {"name": "gender", "label": "Gender", "type": "text", "required": True, "read_only": True},
            {"name": "home_county", "label": "Home County", "type": "text", "required": True}
        ]
    },
    "KRA": {
        "title": "KRA PIN Registration",
        "description": "Requires National ID.",
        "fields": [
            {"name": "national_id", "label": "National ID Number", "type": "text", "required": True, "lookup_service": "IPRS", "lookup_action": "fetch"},
            {"name": "full_name", "label": "Full Name", "type": "text", "required": True, "read_only": True},
            {"name": "date_of_birth", "label": "Date of Birth", "type": "date", "required": True, "read_only": True},
            {"name": "tax_payer_type", "label": "Taxpayer Type", "type": "select", "required": True, "options": [{"value": "individual", "label": "Individual"}]}
        ]
    },
    "ROC": {
        "title": "Business Registration",
        "description": "Requires KRA PIN of Primary Owner.",
        "fields": [
            {"name": "owner_kra_pin", "label": "Owner KRA PIN", "type": "text", "required": True, "lookup_service": "KRA", "lookup_action": "verify", "description": "Verifies owner against Taxpayer Registry"},
            {"name": "owner_name", "label": "Owner Name", "type": "text", "required": True, "read_only": True},
            {"name": "business_name", "label": "Proposed Business Name", "type": "text", "required": True},
            {"name": "business_type", "label": "Business Type", "type": "select", "required": True, "options": [{"value": "pvt", "label": "Private Limited Company"}, {"value": "sole", "label": "Sole Proprietorship"}]}
        ]
    },
    "NTSA": {
        "title": "Driving Licence Application",
        "description": "Requires National ID.",
        "fields": [
            {"name": "national_id", "label": "National ID Number", "type": "text", "required": True, "lookup_service": "IPRS", "lookup_action": "fetch"},
            {"name": "full_name", "label": "Full Name", "type": "text", "required": True, "read_only": True},
            {"name": "blood_group", "label": "Blood Group", "type": "select", "required": True, "options": [{"value": "a+", "label": "A+"}, {"value": "o+", "label": "O+"}, {"value": "ab-", "label": "AB-"}]},
            {"name": "driving_school", "label": "Driving School Name", "type": "text", "required": True}
        ]
    },
    "ONBOARD": {
        "title": "Maisha Platform Onboarding (Legacy Migration)",
        "description": "Onboard from legacy paper-based systems to the Digital Maisha Platform.",
        "fields": [
            {
                "name": "header_1",
                "label": "1. Legacy Identity Information",
                "type": "section_header"
            },
            {
                "name": "legacy_id_number",
                "label": "Legacy ID / Serial Number",
                "type": "text",
                "required": True,
                "description": "Enter the number from your physical green ID or Birth Notification"
            },
            {
                "name": "full_name",
                "label": "Full Name",
                "type": "text",
                "required": True
            },
            {
                "name": "date_of_birth",
                "label": "Date of Birth",
                "type": "date",
                "required": True
            },
            {
                "name": "header_2",
                "label": "2. Contact & Digital Setup",
                "type": "section_header"
            },
            {
                "name": "phone_number",
                "label": "Primary Phone Number",
                "type": "tel",
                "required": True
            },
            {
                "name": "email",
                "label": "Email Address",
                "type": "email",
                "required": True
            },
            {
                "name": "header_3",
                "label": "3. Legacy Document Verification",
                "type": "section_header"
            },
            {
                "name": "legacy_doc_scans",
                "label": "Upload Scan of Legacy Document (ID/Birth Cert)",
                "type": "file",
                "required": True,
                "validation": {"accept": ".pdf,.jpg,.png", "maxSize": 5242880}
            }
        ]
    }
}

if __name__ == "__main__":
    print("=" * 80)
    print("ADDING FORM SCHEMAS TO SERVICES")
    print("=" * 80)

    updated_count = 0

    for key, form_schema in FORM_SCHEMAS.items():
        # Try matching by service_code first, then MDA code
        service = ServiceConfig.objects.filter(service_code=key).first()
        
        if not service:
            service = ServiceConfig.objects.filter(mda__code=key).first()
            
        if not service:
            print(f"\n⚠️  Service not found for key: {key}")
            continue
        
        # Update the service with form schema
        service.form_schema = form_schema
        service.save()
        
        print(f"\n✓ Updated: {service.service_name} ({key})")
        print(f"  Form Title: {form_schema['title']}")
        print(f"  Fields: {len(form_schema['fields'])}")
        
        # List some key fields
        field_names = [f['name'] for f in form_schema['fields'][:5]]
        print(f"  Sample Fields: {', '.join(field_names)}...")
        
        updated_count += 1

    print(f"\n{'=' * 80}")
    print(f"SUMMARY:")
    print(f"  Services Updated: {updated_count}")
    print(f"  Total Form Fields Created: {sum(len(s['fields']) for s in FORM_SCHEMAS.values())}")
    print(f"{'=' * 80}")
