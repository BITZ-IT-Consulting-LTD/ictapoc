"""
Management command to:
1. Add workflow steps to the 10 services missing them.
2. Seed form schemas for all major citizen-facing services.
"""
from django.core.management.base import BaseCommand
from service_api.models import ServiceConfig, WorkflowStep


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 – Workflow step definitions for the 10 services missing them
# Pattern: as_is (manual paperwork) + to_be (digital/automated future-state)
# ─────────────────────────────────────────────────────────────────────────────
MISSING_STEPS = {
    "EDU-BAS-001": {
        "name": "Registration Of Basic Education Institutions",
        "steps": [
            # AS-IS
            dict(sequence=1, step_name="Application Submission (Paper)", step_type="manual",
                 bpmn_element_type="start_event", role="Applicant / School Owner", lifecycle_stage="as_is"),
            dict(sequence=2, step_name="Document Verification by Sub-County Education Officer", step_type="manual",
                 bpmn_element_type="user_task", role="Sub-County Education Officer", lifecycle_stage="as_is"),
            dict(sequence=3, step_name="Physical Site Inspection", step_type="manual",
                 bpmn_element_type="user_task", role="County Education Inspector", lifecycle_stage="as_is"),
            dict(sequence=4, step_name="Approval & Registration Certificate Issuance", step_type="manual",
                 bpmn_element_type="end_event", role="Director Basic Education", lifecycle_stage="as_is"),
            # TO-BE
            dict(sequence=1, step_name="Online Application via Nemis Portal", step_type="api_call",
                 bpmn_element_type="start_event", role="Applicant", lifecycle_stage="to_be"),
            dict(sequence=2, step_name="Automated Document Validation", step_type="api_call",
                 bpmn_element_type="service_task", role="System", lifecycle_stage="to_be"),
            dict(sequence=3, step_name="Officer Review & Recommendation", step_type="manual",
                 bpmn_element_type="user_task", role="Education Officer", lifecycle_stage="to_be"),
            dict(sequence=4, step_name="Digital Certificate Generation & Dispatch", step_type="api_call",
                 bpmn_element_type="end_event", role="System", lifecycle_stage="to_be"),
        ]
    },
    "TRD-BUS-002": {
        "name": "Company Incorporation",
        "steps": [
            # AS-IS
            dict(sequence=1, step_name="Paper Application Submission (CR1 Forms)", step_type="manual",
                 bpmn_element_type="start_event", role="Applicant / Advocate", lifecycle_stage="as_is"),
            dict(sequence=2, step_name="Name Search & Reservation", step_type="manual",
                 bpmn_element_type="user_task", role="BRS Officer", lifecycle_stage="as_is"),
            dict(sequence=3, step_name="Document Review & Verification", step_type="manual",
                 bpmn_element_type="user_task", role="BRS Senior Officer", lifecycle_stage="as_is"),
            dict(sequence=4, step_name="Certificate of Incorporation Issuance", step_type="manual",
                 bpmn_element_type="end_event", role="BRS Registrar", lifecycle_stage="as_is"),
            # TO-BE
            dict(sequence=1, step_name="Online Name Search & Reservation (eCitizen)", step_type="api_call",
                 bpmn_element_type="start_event", role="Applicant", lifecycle_stage="to_be"),
            dict(sequence=2, step_name="Digital Form Submission & KRA PIN Validation", step_type="api_call",
                 bpmn_element_type="service_task", role="System", lifecycle_stage="to_be"),
            dict(sequence=3, step_name="Automated Compliance Check", step_type="api_call",
                 bpmn_element_type="service_task", role="System", lifecycle_stage="to_be"),
            dict(sequence=4, step_name="Digital Certificate via Email/eCitizen", step_type="api_call",
                 bpmn_element_type="end_event", role="System", lifecycle_stage="to_be"),
        ]
    },
    "INT-IMM-001": {
        "name": "Passport Application",
        "steps": [
            # AS-IS
            dict(sequence=1, step_name="Paper Form Submission at DS Office", step_type="manual",
                 bpmn_element_type="start_event", role="Citizen", lifecycle_stage="as_is"),
            dict(sequence=2, step_name="Document & Birth Certificate Verification", step_type="manual",
                 bpmn_element_type="user_task", role="Immigration Officer", lifecycle_stage="as_is",
                 api_config={"form_fields": ["security_clearance_status", "intelligence_notes"]}),
            dict(sequence=3, step_name="Biometric Capture (Photo & Fingerprints)", step_type="manual",
                 bpmn_element_type="user_task", role="Biometrics Clerk", lifecycle_stage="as_is"),
            dict(sequence=4, step_name="Passport Book Production & Quality Check", step_type="manual",
                 bpmn_element_type="user_task", role="Production Officer", lifecycle_stage="as_is"),
            dict(sequence=5, step_name="Passport Issuance / Collection", step_type="manual",
                 bpmn_element_type="end_event", role="Issuance Officer", lifecycle_stage="as_is"),
            # TO-BE
            dict(sequence=1, step_name="Online Application via eCitizen", step_type="api_call",
                 bpmn_element_type="start_event", role="Citizen", lifecycle_stage="to_be"),
            dict(sequence=2, step_name="IPRS Identity Verification", step_type="api_call",
                 bpmn_element_type="service_task", role="System", lifecycle_stage="to_be"),
            dict(sequence=3, step_name="Biometric Reuse from Huduma Database", step_type="api_call",
                 bpmn_element_type="service_task", role="System", lifecycle_stage="to_be"),
            dict(sequence=4, step_name="Automated Passport Production", step_type="api_call",
                 bpmn_element_type="service_task", role="System", lifecycle_stage="to_be"),
            dict(sequence=5, step_name="Secure Postal / Courier Delivery", step_type="api_call",
                 bpmn_element_type="end_event", role="System", lifecycle_stage="to_be"),
        ]
    },
    "TRD-BUS-001": {
        "name": "Business Name Registration",
        "steps": [
            # AS-IS
            dict(sequence=1, step_name="Business Name Search at BRS Counter", step_type="manual",
                 bpmn_element_type="start_event", role="Applicant", lifecycle_stage="as_is"),
            dict(sequence=2, step_name="Form BN1 Submission with ID Copy", step_type="manual",
                 bpmn_element_type="user_task", role="BRS Officer", lifecycle_stage="as_is"),
            dict(sequence=3, step_name="Certificate of Business Name Registration", step_type="manual",
                 bpmn_element_type="end_event", role="BRS Registrar", lifecycle_stage="as_is"),
            # TO-BE
            dict(sequence=1, step_name="Name Search on eCitizen Portal", step_type="api_call",
                 bpmn_element_type="start_event", role="Applicant", lifecycle_stage="to_be"),
            dict(sequence=2, step_name="ID & PIN Verification via IPRS/KRA", step_type="api_call",
                 bpmn_element_type="service_task", role="System", lifecycle_stage="to_be"),
            dict(sequence=3, step_name="Instant Digital Certificate Issuance", step_type="api_call",
                 bpmn_element_type="end_event", role="System", lifecycle_stage="to_be"),
        ]
    },
    "LND-ADM-003": {
        "name": "Transfer Of Land Ownership",
        "steps": [
            # AS-IS
            dict(sequence=1, step_name="Application Lodgement at Land Registry", step_type="manual",
                 bpmn_element_type="start_event", role="Advocate / Applicant", lifecycle_stage="as_is"),
            dict(sequence=2, step_name="Land Search & Clearance Check", step_type="manual",
                 bpmn_element_type="user_task", role="Land Registry Officer", lifecycle_stage="as_is"),
            dict(sequence=3, step_name="Stamp Duty Assessment & Payment", step_type="manual",
                 bpmn_element_type="user_task", role="KRA Officer", lifecycle_stage="as_is"),
            dict(sequence=4, step_name="Registration of Instrument of Transfer", step_type="manual",
                 bpmn_element_type="user_task", role="Land Registrar", lifecycle_stage="as_is"),
            dict(sequence=5, step_name="New Title Deed Issuance", step_type="manual",
                 bpmn_element_type="end_event", role="Land Registrar", lifecycle_stage="as_is"),
            # TO-BE
            dict(sequence=1, step_name="Digital Application via Ardhisasa", step_type="api_call",
                 bpmn_element_type="start_event", role="Applicant", lifecycle_stage="to_be"),
            dict(sequence=2, step_name="Automated Land Search & Encumbrance Check", step_type="api_call",
                 bpmn_element_type="service_task", role="System", lifecycle_stage="to_be"),
            dict(sequence=3, step_name="Online Stamp Duty Payment via KRA iTax", step_type="api_call",
                 bpmn_element_type="service_task", role="System", lifecycle_stage="to_be"),
            dict(sequence=4, step_name="Registrar Review & Digital Approval", step_type="manual",
                 bpmn_element_type="user_task", role="Land Registrar", lifecycle_stage="to_be"),
            dict(sequence=5, step_name="Electronic Title Deed Generation", step_type="api_call",
                 bpmn_element_type="end_event", role="System", lifecycle_stage="to_be"),
        ]
    },
    "INT-CIV-003": {
        "name": "Issuance Of Birth Certificate",
        "steps": [
            # AS-IS
            dict(sequence=1, step_name="Application at Sub-County Civil Registrar", step_type="manual",
                 bpmn_element_type="start_event", role="Parent / Guardian", lifecycle_stage="as_is"),
            dict(sequence=2, step_name="Birth Notification Verification", step_type="manual",
                 bpmn_element_type="user_task", role="Civil Registration Officer", lifecycle_stage="as_is"),
            dict(sequence=3, step_name="Certificate Printing & Issuance", step_type="manual",
                 bpmn_element_type="end_event", role="Civil Registrar", lifecycle_stage="as_is"),
            # TO-BE
            dict(sequence=1, step_name="Online Request via eCitizen / CRS Portal", step_type="api_call",
                 bpmn_element_type="start_event", role="Parent / Guardian", lifecycle_stage="to_be"),
            dict(sequence=2, step_name="CRS Birth Record Lookup & Verification", step_type="api_call",
                 bpmn_element_type="service_task", role="System", lifecycle_stage="to_be"),
            dict(sequence=3, step_name="Digital Certificate Generation & SMS Notification", step_type="api_call",
                 bpmn_element_type="end_event", role="System", lifecycle_stage="to_be"),
        ]
    },
    "INT-REG-001": {
        "name": "National Id Application",
        "steps": [
            # AS-IS
            dict(sequence=1, step_name="Application at District Registrar's Office", step_type="manual",
                 bpmn_element_type="start_event", role="Citizen (18+ Yrs)", lifecycle_stage="as_is"),
            dict(sequence=2, step_name="Physical Vetting & Form ID1 Submission", step_type="manual",
                 bpmn_element_type="user_task", role="Registration Officer", lifecycle_stage="as_is",
                 api_config={"form_fields": ["criminal_record_check", "fingerprint_verification"]}),
            dict(sequence=3, step_name="Biometric Capture (Photo & Fingerprints)", step_type="manual",
                 bpmn_element_type="user_task", role="Biometrics Clerk", lifecycle_stage="as_is"),
            dict(sequence=4, step_name="Card Production at Huduma Centre", step_type="manual",
                 bpmn_element_type="user_task", role="Production Officer", lifecycle_stage="as_is"),
            dict(sequence=5, step_name="Card Collection by Applicant", step_type="manual",
                 bpmn_element_type="end_event", role="Issuance Officer", lifecycle_stage="as_is"),
            # TO-BE
            dict(sequence=1, step_name="Online Pre-Registration via Maisha Namba Portal", step_type="api_call",
                 bpmn_element_type="start_event", role="Citizen", lifecycle_stage="to_be"),
            dict(sequence=2, step_name="IPRS Birth Record Cross-Reference", step_type="api_call",
                 bpmn_element_type="service_task", role="System", lifecycle_stage="to_be"),
            dict(sequence=3, step_name="Biometric Capture at Huduma Centre Kiosk", step_type="manual",
                 bpmn_element_type="user_task", role="Kiosk Attendant", lifecycle_stage="to_be"),
            dict(sequence=4, step_name="Automated Card Production", step_type="api_call",
                 bpmn_element_type="service_task", role="System", lifecycle_stage="to_be"),
            dict(sequence=5, step_name="Secure Postal Delivery of ID Card", step_type="api_call",
                 bpmn_element_type="end_event", role="System", lifecycle_stage="to_be"),
        ]
    },
    "TRE-REV-004": {
        "name": "Tax Compliance Certificates",
        "steps": [
            # AS-IS
            dict(sequence=1, step_name="Manual Application at KRA Service Centre", step_type="manual",
                 bpmn_element_type="start_event", role="Taxpayer / Agent", lifecycle_stage="as_is"),
            dict(sequence=2, step_name="Tax Account Review by KRA Officer", step_type="manual",
                 bpmn_element_type="user_task", role="KRA Compliance Officer", lifecycle_stage="as_is"),
            dict(sequence=3, step_name="Certificate Generation & Stamping", step_type="manual",
                 bpmn_element_type="end_event", role="KRA Officer", lifecycle_stage="as_is"),
            # TO-BE
            dict(sequence=1, step_name="iTax Portal Request Submission", step_type="api_call",
                 bpmn_element_type="start_event", role="Taxpayer", lifecycle_stage="to_be"),
            dict(sequence=2, step_name="Automated Tax Compliance Scoring", step_type="api_call",
                 bpmn_element_type="service_task", role="System", lifecycle_stage="to_be"),
            dict(sequence=3, step_name="Digital TCC Issuance & Email Delivery", step_type="api_call",
                 bpmn_element_type="end_event", role="System", lifecycle_stage="to_be"),
        ]
    },
    "INT-CIV-001": {
        "name": "Birth Registration",
        "steps": [
            # AS-IS
            dict(sequence=1, step_name="Notification at Hospital / Sub-County Registrar", step_type="manual",
                 bpmn_element_type="start_event", role="Parent / Midwife", lifecycle_stage="as_is"),
            dict(sequence=2, step_name="Birth Particulars Entry in Physical Register", step_type="manual",
                 bpmn_element_type="user_task", role="Civil Registration Officer", lifecycle_stage="as_is"),
            dict(sequence=3, step_name="Birth Certificate Printed & Issued", step_type="manual",
                 bpmn_element_type="end_event", role="Civil Registrar", lifecycle_stage="as_is"),
            # TO-BE
            dict(sequence=1, step_name="Hospital System Auto-Notification to CRS", step_type="api_call",
                 bpmn_element_type="start_event", role="Hospital System", lifecycle_stage="to_be"),
            dict(sequence=2, step_name="Parent Online Confirmation via eCitizen", step_type="api_call",
                 bpmn_element_type="user_task", role="Parent", lifecycle_stage="to_be"),
            dict(sequence=3, step_name="Maisha Namba Auto-Assignment at Birth", step_type="api_call",
                 bpmn_element_type="service_task", role="System", lifecycle_stage="to_be"),
            dict(sequence=4, step_name="Digital Birth Certificate via G-Notify SMS", step_type="api_call",
                 bpmn_element_type="end_event", role="System", lifecycle_stage="to_be"),
        ]
    },
    "INT-CIV-002": {
        "name": "Death Registration",
        "steps": [
            # AS-IS
            dict(sequence=1, step_name="Death Notification at Hospital / Mortuary", step_type="manual",
                 bpmn_element_type="start_event", role="Next of Kin / Medical Officer", lifecycle_stage="as_is"),
            dict(sequence=2, step_name="Death Particulars Entry in Physical Register", step_type="manual",
                 bpmn_element_type="user_task", role="Civil Registration Officer", lifecycle_stage="as_is"),
            dict(sequence=3, step_name="Death Certificate Issuance", step_type="manual",
                 bpmn_element_type="end_event", role="Civil Registrar", lifecycle_stage="as_is"),
            # TO-BE
            dict(sequence=1, step_name="Hospital System Auto-Notification to CRS", step_type="api_call",
                 bpmn_element_type="start_event", role="Hospital System", lifecycle_stage="to_be"),
            dict(sequence=2, step_name="Next of Kin Online Confirmation via eCitizen", step_type="api_call",
                 bpmn_element_type="user_task", role="Next of Kin", lifecycle_stage="to_be"),
            dict(sequence=3, step_name="IPRS Record Deactivation", step_type="api_call",
                 bpmn_element_type="service_task", role="System", lifecycle_stage="to_be"),
            dict(sequence=4, step_name="Digital Death Certificate via G-Notify", step_type="api_call",
                 bpmn_element_type="end_event", role="System", lifecycle_stage="to_be"),
        ]
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 – Form schema definitions for major citizen-facing services
# ─────────────────────────────────────────────────────────────────────────────
FORM_SCHEMAS = {
    "INT-IMM-001": {
        "rules": {"schema": {"properties": {
            "full_name": {"type": "text", "title": "Full Name (as in ID)", "required": True},
            "id_number": {"type": "text", "title": "National ID / Alien Card Number", "required": True},
            "date_of_birth": {"type": "date", "title": "Date of Birth", "required": True},
            "gender": {"type": "select", "title": "Gender", "options": ["Male", "Female"], "required": True},
            "nationality": {"type": "text", "title": "Nationality", "required": True},
            "county": {"type": "text", "title": "County of Residence", "required": True},
            "phone_number": {"type": "tel", "title": "Phone Number", "required": True},
            "email": {"type": "email", "title": "Email Address", "required": False},
            "passport_type": {"type": "select", "title": "Passport Type",
                              "options": ["East African Passport", "Kenya Passport", "Emergency Travel Document"],
                              "required": True},
            "is_first_passport": {"type": "boolean", "title": "Is this your first passport?", "required": True},
            "previous_passport_number": {"type": "text", "title": "Previous Passport Number (if any)", "required": False},
        }, "required": ["full_name", "id_number", "date_of_birth", "gender", "nationality", "county", "phone_number", "passport_type", "is_first_passport"]}}
    },
    "INT-REG-001": {
        "rules": {"schema": {"properties": {
            "full_name": {"type": "text", "title": "Full Name", "required": True},
            "date_of_birth": {"type": "date", "title": "Date of Birth", "required": True},
            "gender": {"type": "select", "title": "Gender", "options": ["Male", "Female"], "required": True},
            "county_of_birth": {"type": "text", "title": "County of Birth", "required": True},
            "county_of_residence": {"type": "text", "title": "County of Residence", "required": True},
            "sub_county": {"type": "text", "title": "Sub-County", "required": True},
            "ward": {"type": "text", "title": "Ward", "required": True},
            "fathers_name": {"type": "text", "title": "Father's Full Name", "required": True},
            "fathers_id_number": {"type": "text", "title": "Father's ID Number", "required": False},
            "mothers_name": {"type": "text", "title": "Mother's Full Name", "required": True},
            "mothers_id_number": {"type": "text", "title": "Mother's ID Number", "required": False},
            "phone_number": {"type": "tel", "title": "Phone Number", "required": True},
            "birth_certificate_number": {"type": "text", "title": "Birth Certificate Number", "required": True},
        }, "required": ["full_name", "date_of_birth", "gender", "county_of_birth", "county_of_residence", "sub_county", "ward", "fathers_name", "mothers_name", "phone_number", "birth_certificate_number"]}}
    },
    "INT-CIV-001": {
        "rules": {"schema": {"properties": {
            "childs_full_name": {"type": "text", "title": "Child's Full Name", "required": True},
            "date_of_birth": {"type": "date", "title": "Date of Birth", "required": True},
            "place_of_birth": {"type": "text", "title": "Place of Birth (Hospital/Location)", "required": True},
            "gender": {"type": "select", "title": "Gender", "options": ["Male", "Female"], "required": True},
            "fathers_name": {"type": "text", "title": "Father's Full Name", "required": False},
            "fathers_id_number": {"type": "text", "title": "Father's National ID Number", "required": False},
            "mothers_name": {"type": "text", "title": "Mother's Full Name", "required": True},
            "mothers_id_number": {"type": "text", "title": "Mother's National ID Number", "required": True},
            "county": {"type": "text", "title": "County", "required": True},
            "sub_county": {"type": "text", "title": "Sub-County", "required": True},
            "phone_number": {"type": "tel", "title": "Parent/Guardian Phone Number", "required": True},
        }, "required": ["childs_full_name", "date_of_birth", "place_of_birth", "gender", "mothers_name", "mothers_id_number", "county", "sub_county", "phone_number"]}}
    },
    "INT-CIV-002": {
        "rules": {"schema": {"properties": {
            "deceased_full_name": {"type": "text", "title": "Full Name of Deceased", "required": True},
            "id_number": {"type": "text", "title": "National ID Number of Deceased", "required": False},
            "date_of_death": {"type": "date", "title": "Date of Death", "required": True},
            "place_of_death": {"type": "text", "title": "Place of Death (Hospital/Location)", "required": True},
            "cause_of_death": {"type": "text", "title": "Cause of Death", "required": True},
            "gender": {"type": "select", "title": "Gender", "options": ["Male", "Female"], "required": True},
            "county": {"type": "text", "title": "County", "required": True},
            "informant_name": {"type": "text", "title": "Informant's Full Name (Next of Kin)", "required": True},
            "informant_id_number": {"type": "text", "title": "Informant's ID Number", "required": True},
            "informant_phone": {"type": "tel", "title": "Informant's Phone Number", "required": True},
            "relationship_to_deceased": {"type": "text", "title": "Relationship to Deceased", "required": True},
        }, "required": ["deceased_full_name", "date_of_death", "place_of_death", "cause_of_death", "gender", "county", "informant_name", "informant_id_number", "informant_phone", "relationship_to_deceased"]}}
    },
    "INT-CIV-003": {
        "rules": {"schema": {"properties": {
            "applicant_name": {"type": "text", "title": "Applicant Full Name", "required": True},
            "applicant_id_number": {"type": "text", "title": "Applicant National ID Number", "required": True},
            "relationship_to_child": {"type": "select", "title": "Relationship to Child",
                                      "options": ["Parent", "Guardian", "Self", "Government Agency"], "required": True},
            "childs_full_name": {"type": "text", "title": "Child's Full Name", "required": True},
            "date_of_birth": {"type": "date", "title": "Child's Date of Birth", "required": True},
            "birth_notification_number": {"type": "text", "title": "Birth Notification Number", "required": False},
            "county": {"type": "text", "title": "County of Registration", "required": True},
            "phone_number": {"type": "tel", "title": "Phone Number", "required": True},
        }, "required": ["applicant_name", "applicant_id_number", "relationship_to_child", "childs_full_name", "date_of_birth", "county", "phone_number"]}}
    },
    "TRD-BUS-001": {
        "rules": {"schema": {"properties": {
            "proposed_business_name": {"type": "text", "title": "Proposed Business Name", "required": True},
            "business_type": {"type": "select", "title": "Business Type",
                              "options": ["Sole Proprietor", "Partnership"], "required": True},
            "nature_of_business": {"type": "text", "title": "Nature of Business / Activity", "required": True},
            "business_physical_address": {"type": "text", "title": "Business Physical Address", "required": True},
            "county": {"type": "text", "title": "County", "required": True},
            "postal_address": {"type": "text", "title": "Postal Address", "required": False},
            "applicant_full_name": {"type": "text", "title": "Proprietor / Partner Full Name", "required": True},
            "applicant_id_number": {"type": "text", "title": "National ID Number", "required": True},
            "applicant_kra_pin": {"type": "text", "title": "KRA PIN", "required": True},
            "phone_number": {"type": "tel", "title": "Phone Number", "required": True},
            "email": {"type": "email", "title": "Email Address", "required": True},
        }, "required": ["proposed_business_name", "business_type", "nature_of_business", "business_physical_address", "county", "applicant_full_name", "applicant_id_number", "applicant_kra_pin", "phone_number", "email"]}}
    },
    "TRD-BUS-002": {
        "rules": {"schema": {"properties": {
            "proposed_company_name": {"type": "text", "title": "Proposed Company Name", "required": True},
            "company_type": {"type": "select", "title": "Company Type",
                             "options": ["Private Limited (Ltd)", "Public Limited (PLC)", "Company Limited by Guarantee"], "required": True},
            "nature_of_business": {"type": "text", "title": "Nature of Business", "required": True},
            "registered_office_address": {"type": "text", "title": "Registered Office Address", "required": True},
            "county": {"type": "text", "title": "County", "required": True},
            "director1_full_name": {"type": "text", "title": "Director 1 – Full Name", "required": True},
            "director1_id_number": {"type": "text", "title": "Director 1 – ID Number", "required": True},
            "director1_kra_pin": {"type": "text", "title": "Director 1 – KRA PIN", "required": True},
            "director2_full_name": {"type": "text", "title": "Director 2 – Full Name (if any)", "required": False},
            "director2_id_number": {"type": "text", "title": "Director 2 – ID Number", "required": False},
            "share_capital": {"type": "number", "title": "Authorised Share Capital (KES)", "required": True},
            "phone_number": {"type": "tel", "title": "Contact Phone Number", "required": True},
            "email": {"type": "email", "title": "Contact Email Address", "required": True},
        }, "required": ["proposed_company_name", "company_type", "nature_of_business", "registered_office_address", "county", "director1_full_name", "director1_id_number", "director1_kra_pin", "share_capital", "phone_number", "email"]}}
    },
    "LND-ADM-003": {
        "rules": {"schema": {"properties": {
            "title_deed_number": {"type": "text", "title": "Title Deed Number", "required": True},
            "land_reference_number": {"type": "text", "title": "Land Reference Number (LR No.)", "required": True},
            "county": {"type": "text", "title": "County", "required": True},
            "seller_full_name": {"type": "text", "title": "Seller / Transferor Full Name", "required": True},
            "seller_id_number": {"type": "text", "title": "Seller National ID Number", "required": True},
            "seller_kra_pin": {"type": "text", "title": "Seller KRA PIN", "required": True},
            "buyer_full_name": {"type": "text", "title": "Buyer / Transferee Full Name", "required": True},
            "buyer_id_number": {"type": "text", "title": "Buyer National ID Number", "required": True},
            "buyer_kra_pin": {"type": "text", "title": "Buyer KRA PIN", "required": True},
            "agreed_purchase_price": {"type": "number", "title": "Agreed Purchase Price (KES)", "required": True},
            "advocate_name": {"type": "text", "title": "Conveyancing Advocate Name", "required": False},
            "phone_number": {"type": "tel", "title": "Contact Phone Number", "required": True},
        }, "required": ["title_deed_number", "land_reference_number", "county", "seller_full_name", "seller_id_number", "seller_kra_pin", "buyer_full_name", "buyer_id_number", "buyer_kra_pin", "agreed_purchase_price", "phone_number"]}}
    },
    "TRE-REV-004": {
        "rules": {"schema": {"properties": {
            "taxpayer_name": {"type": "text", "title": "Taxpayer / Business Name", "required": True},
            "kra_pin": {"type": "text", "title": "KRA PIN (Personal or Business)", "required": True},
            "id_number": {"type": "text", "title": "National ID Number (for individuals)", "required": False},
            "tax_types": {"type": "text", "title": "Tax Types Covered (e.g. Income Tax, VAT)", "required": True},
            "tax_period_from": {"type": "date", "title": "Tax Compliance Period From", "required": True},
            "tax_period_to": {"type": "date", "title": "Tax Compliance Period To", "required": True},
            "phone_number": {"type": "tel", "title": "Phone Number", "required": True},
            "email": {"type": "email", "title": "Email Address", "required": True},
            "purpose_of_certificate": {"type": "text", "title": "Purpose of Certificate (e.g. Tender, Loan)", "required": False},
        }, "required": ["taxpayer_name", "kra_pin", "tax_types", "tax_period_from", "tax_period_to", "phone_number", "email"]}}
    },
    "EDU-BAS-001": {
        "rules": {"schema": {"properties": {
            "institution_name": {"type": "text", "title": "Institution Name", "required": True},
            "institution_type": {"type": "select", "title": "Institution Type",
                                 "options": ["Pre-Primary", "Primary", "Junior Secondary", "Special Needs School"], "required": True},
            "county": {"type": "text", "title": "County", "required": True},
            "sub_county": {"type": "text", "title": "Sub-County", "required": True},
            "ward": {"type": "text", "title": "Ward", "required": True},
            "postal_address": {"type": "text", "title": "Postal Address", "required": True},
            "proprietor_name": {"type": "text", "title": "Proprietor / Sponsor Name", "required": True},
            "proprietor_id_number": {"type": "text", "title": "Proprietor ID Number", "required": True},
            "phone_number": {"type": "tel", "title": "Contact Phone Number", "required": True},
            "email": {"type": "email", "title": "Email Address", "required": True},
            "land_ownership_type": {"type": "select", "title": "Land Ownership Type",
                                    "options": ["Owned", "Leased", "Government-Allocated"], "required": True},
            "expected_enrolment": {"type": "number", "title": "Expected Initial Enrolment", "required": True},
        }, "required": ["institution_name", "institution_type", "county", "sub_county", "ward", "postal_address", "proprietor_name", "proprietor_id_number", "phone_number", "email", "land_ownership_type", "expected_enrolment"]}}
    },
}

# Additional schemas for common services already having steps
EXTRA_SCHEMAS = {
    # Health
    "HLT-INS-001": {
        "rules": {"schema": {"properties": {
            "full_name": {"type": "text", "title": "Full Name", "required": True},
            "id_number": {"type": "text", "title": "National ID / Passport Number", "required": True},
            "date_of_birth": {"type": "date", "title": "Date of Birth", "required": True},
            "gender": {"type": "select", "title": "Gender", "options": ["Male", "Female"], "required": True},
            "phone_number": {"type": "tel", "title": "Phone Number", "required": True},
            "email": {"type": "email", "title": "Email Address", "required": False},
            "county": {"type": "text", "title": "County of Residence", "required": True},
            "employer_name": {"type": "text", "title": "Employer Name (if employed)", "required": False},
            "employment_type": {"type": "select", "title": "Employment Type",
                                "options": ["Formal Employment", "Self-Employed", "Unemployed", "Student"], "required": True},
            "preferred_hospital": {"type": "text", "title": "Preferred Health Facility", "required": False},
            "has_dependants": {"type": "boolean", "title": "Do you have dependants to add?", "required": True},
        }, "required": ["full_name", "id_number", "date_of_birth", "gender", "phone_number", "county", "employment_type", "has_dependants"]}}
    },
    "HLT-INS-002": {
        "rules": {"schema": {"properties": {
            "nhif_member_id": {"type": "text", "title": "NHIF Member Number / ID Number", "required": True},
            "full_name": {"type": "text", "title": "Full Name", "required": True},
            "dependant_full_name": {"type": "text", "title": "Dependant's Full Name", "required": True},
            "relationship": {"type": "select", "title": "Relationship",
                             "options": ["Spouse", "Child", "Parent", "Sibling"], "required": True},
            "dependant_date_of_birth": {"type": "date", "title": "Dependant's Date of Birth", "required": True},
            "dependant_id_number": {"type": "text", "title": "Dependant's ID / Birth Cert Number", "required": False},
            "phone_number": {"type": "tel", "title": "Phone Number", "required": True},
        }, "required": ["nhif_member_id", "full_name", "dependant_full_name", "relationship", "dependant_date_of_birth", "phone_number"]}}
    },
    "TRE-REV-001": {
        "rules": {"schema": {"properties": {
            "taxpayer_type": {"type": "select", "title": "Taxpayer Type",
                              "options": ["Individual", "Non-Individual / Business"], "required": True},
            "full_name": {"type": "text", "title": "Full Name / Business Name", "required": True},
            "id_number": {"type": "text", "title": "National ID / Passport Number", "required": True},
            "date_of_birth": {"type": "date", "title": "Date of Birth (Individuals Only)", "required": False},
            "phone_number": {"type": "tel", "title": "Phone Number", "required": True},
            "email": {"type": "email", "title": "Email Address", "required": True},
            "county": {"type": "text", "title": "County", "required": True},
            "physical_address": {"type": "text", "title": "Physical / Business Address", "required": True},
            "business_nature": {"type": "text", "title": "Nature of Business (Non-Individual)", "required": False},
        }, "required": ["taxpayer_type", "full_name", "id_number", "phone_number", "email", "county", "physical_address"]}}
    },
    "TRN-DRV-001": {
        "rules": {"schema": {"properties": {
            "full_name": {"type": "text", "title": "Full Name (as in ID)", "required": True},
            "id_number": {"type": "text", "title": "National ID Number", "required": True},
            "date_of_birth": {"type": "date", "title": "Date of Birth", "required": True},
            "gender": {"type": "select", "title": "Gender", "options": ["Male", "Female"], "required": True},
            "phone_number": {"type": "tel", "title": "Phone Number", "required": True},
            "county": {"type": "text", "title": "County of Residence", "required": True},
            "blood_group": {"type": "select", "title": "Blood Group",
                            "options": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"], "required": True},
            "licence_class": {"type": "select", "title": "Licence Class Applying For",
                              "options": ["Class A (Motorcycle)", "Class B (Light Vehicle)", "Class C (Heavy Vehicle)", "Class D (Bus/PSV)", "Class E (Trailer)"],
                              "required": True},
            "is_renewal": {"type": "boolean", "title": "Is this a Renewal?", "required": True},
            "existing_licence_number": {"type": "text", "title": "Existing Licence Number (Renewal Only)", "required": False},
        }, "required": ["full_name", "id_number", "date_of_birth", "gender", "phone_number", "county", "blood_group", "licence_class", "is_renewal"]}}
    },
    "TRN-VEH-001": {
        "rules": {"schema": {"properties": {
            "owner_full_name": {"type": "text", "title": "Vehicle Owner Full Name", "required": True},
            "owner_id_number": {"type": "text", "title": "Owner National ID Number", "required": True},
            "owner_kra_pin": {"type": "text", "title": "Owner KRA PIN", "required": True},
            "vehicle_make": {"type": "text", "title": "Vehicle Make (e.g. Toyota)", "required": True},
            "vehicle_model": {"type": "text", "title": "Vehicle Model (e.g. Corolla)", "required": True},
            "year_of_manufacture": {"type": "number", "title": "Year of Manufacture", "required": True},
            "engine_number": {"type": "text", "title": "Engine Number", "required": True},
            "chassis_number": {"type": "text", "title": "Chassis Number", "required": True},
            "vehicle_color": {"type": "text", "title": "Vehicle Color", "required": True},
            "fuel_type": {"type": "select", "title": "Fuel Type",
                          "options": ["Petrol", "Diesel", "Electric", "Hybrid"], "required": True},
            "phone_number": {"type": "tel", "title": "Contact Phone Number", "required": True},
        }, "required": ["owner_full_name", "owner_id_number", "owner_kra_pin", "vehicle_make", "vehicle_model", "year_of_manufacture", "engine_number", "chassis_number", "vehicle_color", "fuel_type", "phone_number"]}}
    },
}


class Command(BaseCommand):
    help = "Seed missing workflow steps (Step 1) and form schemas (Step 2) for all major services"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("\n=== STEP 1: Add workflow steps to 10 services ===\n"))
        self._seed_missing_steps()

        self.stdout.write(self.style.MIGRATE_HEADING("\n=== STEP 2: Seed form schemas for major citizen-facing services ===\n"))
        self._seed_form_schemas()

        self.stdout.write(self.style.MIGRATE_HEADING("\n=== STEP 3: Seed form schemas for additional common services ===\n"))
        self._seed_extra_schemas()

        self.stdout.write(self.style.SUCCESS("\n✅  All done!\n"))

    def _seed_missing_steps(self):
        seeded = 0
        skipped = 0
        for code, data in MISSING_STEPS.items():
            try:
                svc = ServiceConfig.objects.get(service_code=code)
            except ServiceConfig.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"  ⚠  Service not found: {code} – {data['name']}"))
                continue

            if svc.workflow_steps.exists():
                self.stdout.write(f"  ⏭  [{code}] already has steps – skipping")
                skipped += 1
                continue

            for step_data in data["steps"]:
                WorkflowStep.objects.create(service_config=svc, **step_data)

            self.stdout.write(self.style.SUCCESS(f"  ✅  [{code}] {svc.service_name} → {len(data['steps'])} steps added"))
            seeded += 1

        self.stdout.write(f"\n  Seeded: {seeded}  |  Skipped (already had steps): {skipped}")

    def _seed_form_schemas(self):
        seeded = 0
        for code, schema in FORM_SCHEMAS.items():
            try:
                svc = ServiceConfig.objects.get(service_code=code)
            except ServiceConfig.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"  ⚠  Service not found: {code}"))
                continue

            svc.form_schema = schema["rules"]["schema"]
            svc.config = schema
            svc.save(update_fields=["config", "form_schema"])
            field_count = len(schema["rules"]["schema"]["properties"])
            self.stdout.write(self.style.SUCCESS(f"  ✅  [{code}] {svc.service_name} → {field_count} fields updated"))
            seeded += 1

        self.stdout.write(f"\n  Seeded/Updated: {seeded}")

    def _seed_extra_schemas(self):
        seeded = 0
        not_found = 0
        for code, schema in EXTRA_SCHEMAS.items():
            try:
                svc = ServiceConfig.objects.get(service_code=code)
            except ServiceConfig.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"  ⚠  Service not found: {code} – skipping"))
                not_found += 1
                continue

            svc.form_schema = schema["rules"]["schema"]
            svc.config = schema
            svc.save(update_fields=["config", "form_schema"])
            field_count = len(schema["rules"]["schema"]["properties"])
            self.stdout.write(self.style.SUCCESS(f"  ✅  [{code}] {svc.service_name} → {field_count} fields updated"))
            seeded += 1

        self.stdout.write(f"\n  Seeded/Updated: {seeded}  |  Not found: {not_found}")
