import os
import django
import json

# Set up Django environment targeting Docker DB
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.host_settings')
django.setup()

from service_api.models import ServiceConfig

def seed_advanced_forms():
    print("--- SEEDING ADVANCED TO-BE FORM SCHEMAS ---")

    # 1. PSC Job Application (Commission Core and support Services)
    psc_schema = {
        "rules": {
            "schema": {
                "type": "object",
                "required": ["vacancy_no", "full_name", "id_number", "highest_qualification"],
                "properties": {
                    "header_1": {"type": "section_header", "title": "Vacancy Details"},
                    "vacancy_no": {"type": "string", "title": "Vacancy Number", "description": "e.g. PSC/001/2024"},
                    "post_applied": {"type": "string", "title": "Post Applied For"},
                    "header_2": {"type": "section_header", "title": "Personal Bio-Data"},
                    "full_name": {"type": "string", "title": "Full Name", "description": "As per ID Card"},
                    "id_number": {"type": "string", "title": "ID Number", "lookup_service": "IPRS"},
                    "gender": {"type": "string", "enum": ["Male", "Female", "Other"]},
                    "ethnicity": {"type": "string", "title": "Ethnicity/Community"},
                    "disability_status": {"type": "string", "enum": ["None", "Physical", "Visual", "Hearing", "Other"]},
                    "header_3": {"type": "section_header", "title": "Academic & Professional"},
                    "highest_qualification": {"type": "string", "enum": ["PhD", "Masters", "Bachelors", "Higher Diploma", "Diploma", "Certificate"]},
                    "institution": {"type": "string", "title": "Awarding Institution"},
                    "professional_body": {"type": "string", "title": "Professional Body Membership (e.g. LSK, KMPDC)"},
                    "header_4": {"type": "section_header", "title": "Documents"},
                    "cv_upload": {"type": "string", "format": "data-url", "title": "Curriculum Vitae (PDF)"},
                    "cert_upload": {"type": "string", "format": "data-url", "title": "Academic Certificates (Merged PDF)"}
                }
            }
        }
    }

    # 2. iTax - Individual Income Tax Return
    itax_schema = {
        "rules": {
            "schema": {
                "type": "object",
                "required": ["kra_pin", "return_period", "gross_pay"],
                "properties": {
                    "header_1": {"type": "section_header", "title": "Taxpayer Information"},
                    "kra_pin": {"type": "string", "title": "KRA PIN", "lookup_service": "KRA_REGISTRY"},
                    "return_period": {"type": "string", "title": "Return Year", "enum": ["2023", "2024"]},
                    "header_2": {"type": "section_header", "title": "Employment Income (P9 Details)"},
                    "employer_pin": {"type": "string", "title": "Employer KRA PIN"},
                    "gross_pay": {"type": "number", "title": "Total Gross Pay (Ksh)"},
                    "nssf_contribution": {"type": "number", "title": "NSSF Contributions"},
                    "nhif_contribution": {"type": "number", "title": "NHIF Contributions"},
                    "header_3": {"type": "section_header", "title": "Reliefs & Deductions"},
                    "personal_relief": {"type": "number", "title": "Personal Relief (Monthly 2400)", "default": 28800},
                    "insurance_relief": {"type": "number", "title": "Insurance Relief"},
                    "mortgage_interest": {"type": "number", "title": "Mortgage Interest Deduction"},
                    "header_4": {"type": "section_header", "title": "Digital Proof"},
                    "p9_form": {"type": "string", "format": "data-url", "title": "Signed P9 Form"}
                }
            }
        }
    }

    # 3. BRS - Business / Company Registration
    brs_schema = {
        "rules": {
            "schema": {
                "type": "object",
                "required": ["proposed_name", "business_type", "primary_director_id"],
                "properties": {
                    "header_1": {"type": "section_header", "title": "Entity Information"},
                    "proposed_name": {"type": "string", "title": "Proposed Company Name (Option 1)"},
                    "proposed_name_2": {"type": "string", "title": "Proposed Company Name (Option 2)"},
                    "business_type": {"type": "string", "enum": ["Private Limited Company", "Public Limited Company", "Business Name (Sole Prop)", "Partnership"]},
                    "nature_of_business": {"type": "string", "format": "textarea", "title": "Description of Activities"},
                    "header_2": {"type": "section_header", "title": "Registered Office"},
                    "county": {"type": "string", "title": "County of Operation"},
                    "physical_address": {"type": "string", "title": "Building/Plot/Road"},
                    "header_3": {"type": "section_header", "title": "Directors & Shareholding"},
                    "primary_director_name": {"type": "string", "title": "Full Name of Primary Director"},
                    "primary_director_id": {"type": "string", "title": "ID/Passport Number", "lookup_service": "IPRS"},
                    "share_capital": {"type": "number", "title": "Nominal Share Capital (Ksh)"},
                    "header_4": {"type": "section_header", "title": "Uploads"},
                    "memo_articles": {"type": "string", "format": "data-url", "title": "Memorandum & Articles of Association"}
                }
            }
        }
    }

    # 4. NEMIS - Student Registration
    nemis_schema = {
        "rules": {
            "schema": {
                "type": "object",
                "required": ["student_name", "birth_cert_no", "current_grade"],
                "properties": {
                    "header_1": {"type": "section_header", "title": "Learner Details"},
                    "student_name": {"type": "string", "title": "Full Name of Student (As per Birth Cert)"},
                    "birth_cert_no": {"type": "string", "title": "Birth Certificate Entry Number", "lookup_service": "CRS_REGISTRY"},
                    "gender": {"type": "string", "enum": ["Male", "Female"]},
                    "date_of_birth": {"type": "string", "format": "date"},
                    "header_2": {"type": "section_header", "title": "School Placement"},
                    "school_code": {"type": "string", "title": "School NEMIS Code", "lookup_service": "SCHOOL_REGISTRY"},
                    "current_grade": {"type": "string", "enum": ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", "JSS 1", "JSS 2", "JSS 3", "Form 1", "Form 2", "Form 3", "Form 4"]},
                    "header_3": {"type": "section_header", "title": "Parental Info"},
                    "guardian_name": {"type": "string", "title": "Parent/Guardian Name"},
                    "guardian_id": {"type": "string", "title": "Guardian ID Number", "lookup_service": "IPRS"}
                }
            }
        }
    }

    # 5. Civil Servant Rent Payment
    housing_schema = {
        "rules": {
            "schema": {
                "type": "object",
                "required": ["payroll_no", "estate_name", "house_no"],
                "properties": {
                    "header_1": {"type": "section_header", "title": "Civil Servant Identity"},
                    "full_name": {"type": "string", "title": "Full Name"},
                    "payroll_no": {"type": "string", "title": "P/No (Payroll Number)", "lookup_service": "GHRIS"},
                    "mda": {"type": "string", "title": "Ministry/Department/Agency"},
                    "header_2": {"type": "section_header", "title": "Property Details"},
                    "estate_name": {"type": "string", "title": "Government Estate Name"},
                    "house_no": {"type": "string", "title": "House/Flat Number"},
                    "header_3": {"type": "section_header", "title": "Payment Instruction"},
                    "payment_mode": {"type": "string", "enum": ["Check-off (Payroll Deduction)", "Direct Deposit", "MPESA"]},
                    "amount": {"type": "number", "title": "Rent Amount (Confirmed by Estate Dept)"}
                }
            }
        }
    }

    # 6. KNEC Examination Registration
    knec_schema = {
        "rules": {
            "schema": {
                "type": "object",
                "required": ["exam_type", "index_number", "subject_choices"],
                "properties": {
                    "header_1": {"type": "section_header", "title": "Candidate Information"},
                    "full_name": {"type": "string", "title": "Full Name"},
                    "id_or_birth_cert": {"type": "string", "title": "ID or Birth Cert Number", "lookup_service": "IPRS"},
                    "header_2": {"type": "section_header", "title": "Exam Details"},
                    "exam_type": {"type": "string", "enum": ["KCSE", "KPSEA", "Technical", "Business", "Teacher Education"]},
                    "center_code": {"type": "string", "title": "Examination Center Code"},
                    "index_number": {"type": "string", "title": "Candidate Index Number (Repeaters)"},
                    "header_3": {"type": "section_header", "title": "Subject Selection"},
                    "subject_choices": {"type": "array", "title": "Select Subjects", "widget": "checkbox-group", "items": {"type": "string", "enum": ["Mathematics", "English", "Kiswahili", "Chemistry", "Biology", "Physics", "History", "Geography", "CRE", "Business Studies"]}},
                    "header_4": {"type": "section_header", "title": "Photo Upload"},
                    "photo": {"type": "string", "format": "data-url", "title": "Passport Photo (300x300)"}
                }
            }
        }
    }

    # 7. Tourism Returns (TRS)
    tourism_schema = {
        "rules": {
            "schema": {
                "type": "object",
                "required": ["establishment_name", "return_month", "gross_sales"],
                "properties": {
                    "header_1": {"type": "section_header", "title": "Establishment Details"},
                    "establishment_name": {"type": "string", "title": "Name of Hotel/Agency"},
                    "tra_license_no": {"type": "string", "title": "TRA License Number", "lookup_service": "TRA_REGISTRY"},
                    "return_month": {"type": "string", "enum": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]},
                    "header_2": {"type": "section_header", "title": "Financial Figures"},
                    "gross_sales": {"type": "number", "title": "Total Sales for the Month (Ksh)"},
                    "levy_deductible": {"type": "number", "title": "Amount Subject to 2% Tourism Levy"},
                    "header_3": {"type": "section_header", "title": "Occupancy Stats (Hotels Only)"},
                    "total_beds": {"type": "number", "title": "Total Bed Capacity"},
                    "beds_occupied": {"type": "number", "title": "Total Beds Occupied (Monthly Sum)"}
                }
            }
        }
    }

    # 8. Seafarers Service
    seafarers_schema = {
        "rules": {
            "schema": {
                "type": "object",
                "required": ["identity_no", "rank", "cdc_number"],
                "properties": {
                    "header_1": {"type": "section_header", "title": "Seafarer Identity"},
                    "full_name": {"type": "string", "title": "Full Name"},
                    "identity_no": {"type": "string", "title": "ID/Passport Number", "lookup_service": "IPRS"},
                    "cdc_number": {"type": "string", "title": "Continuous Discharge Certificate (CDC) No"},
                    "header_2": {"type": "section_header", "title": "Professional Rank"},
                    "rank": {"type": "string", "enum": ["Master", "Chief Officer", "Engineer", "Deck Hand", "Rating", "Steward"]},
                    "vessel_name": {"type": "string", "title": "Current/Last Vessel Name"},
                    "header_3": {"type": "section_header", "title": "Certifications"},
                    "bst_cert": {"type": "string", "format": "data-url", "title": "Basic Safety Training Certificate"},
                    "medical_cert": {"type": "string", "format": "data-url", "title": "Medical Fitness Certificate"}
                }
            }
        }
    }

    # 9. Passport (Refined To-Be)
    passport_to_be = {
        "rules": {
            "schema": {
                "type": "object",
                "required": ["passport_type", "delivery_center"],
                "properties": {
                    "header_1": {"type": "section_header", "title": "Authoritative Identity Verification"},
                    "full_name": {"type": "string", "title": "Full Name", "description": "Auto-filled from IPRS", "lookup_service": "IPRS"},
                    "id_number": {"type": "string", "title": "ID Number", "lookup_service": "IPRS"},
                    "header_2": {"type": "section_header", "title": "Passport Configuration"},
                    "passport_type": {"type": "string", "enum": ["32 Pages (Series A)", "48 Pages (Series B)", "64 Pages (Series C)", "Diplomatic"]},
                    "delivery_center": {"type": "string", "enum": ["Nairobi (Nyayo House)", "Mombasa", "Kisumu", "Eldoret", "Nakuru", "Embu", "Kisii"]},
                    "header_3": {"type": "section_header", "title": "Digital Evidence"},
                    "photo": {"type": "string", "format": "data-url", "title": "Digital Passport Photo"},
                    "id_scan": {"type": "string", "format": "data-url", "title": "National ID Scan (Front/Back Combined)"}
                }
            }
        }
    }

    # Apply Schemas
    mappings = [
        ("Commission  Core and support Services", psc_schema),
        ("Filing of Income Tax Return - Individual", itax_schema),
        ("Business / Company Registration", brs_schema),
        ("National Education Management Information System (NEMIS)", nemis_schema),
        ("Learner Registration via KEMIS", nemis_schema),
        ("Student Registration & Admission (via NEMIS)", nemis_schema),
        ("Civil Servant Rent Payment System", housing_schema),
        ("Kenya National Examinations Council (KNEC) Digital Examination Management System", knec_schema),
        ("Tourism Returns System (TRS)", tourism_schema),
        ("Seafarers service", seafarers_schema),
        ("First-Time Passport Application", passport_to_be),
        ("Passport Renewal", passport_to_be),
    ]

    count = 0
    for name_pattern, schema in mappings:
        try:
            # Try exact match first
            svc = ServiceConfig.objects.get(service_name=name_pattern)
            svc.config = schema
            svc.save()
            print(f"  [Advanced] Applied schema to: {name_pattern}")
            count += 1
        except ServiceConfig.DoesNotExist:
            # Try partial match
            svcs = ServiceConfig.objects.filter(service_name__icontains=name_pattern)
            for s in svcs:
                s.config = schema
                s.save()
                print(f"  [Advanced] Applied schema to (partial): {s.service_name}")
                count += 1
        except ServiceConfig.MultipleObjectsReturned:
            svcs = ServiceConfig.objects.filter(service_name=name_pattern)
            for s in svcs:
                s.config = schema
                s.save()
                print(f"  [Advanced] Applied schema to (duplicate): {s.service_name}")
                count += 1

    print(f"--- COMPLETE: Configured advanced forms for {count} services ---")

if __name__ == '__main__':
    seed_advanced_forms()
