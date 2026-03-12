"""
Management command to seed form_schema for Priority & Cradle-to-Death services.

Targets only ServiceConfig records with priority in ('high', 'critical') and
populates form_schema based on the official BPR documentation found in
/mdas/docs_final/priority_mdas/.

This command uses a two-tier matching strategy:
  1. Exact service_code match (for known Cradle-to-Death lifecycle services)
  2. MDA name + service_name pattern match (for Priority MDA services)

All identity fields include KeSEL "Once-Only" lookup_service attributes.

Usage:
    python manage.py seed_priority_forms
    python manage.py seed_priority_forms --dry-run
    python manage.py seed_priority_forms --force
"""
from collections import defaultdict

from django.core.management.base import BaseCommand
from service_api.models import ServiceConfig


# ─────────────────────────────────────────────────────────────────────────────
# Schema builder helpers (same convention as seed_missing_schemas)
# ─────────────────────────────────────────────────────────────────────────────

def _s(title, description=None):
    """Section header entry."""
    entry = {"type": "section_header", "title": title}
    if description:
        entry["description"] = description
    return entry


def _f(title, field_type="string", **kwargs):
    """Field entry."""
    entry = {"type": field_type, "title": title}
    entry.update(kwargs)
    return entry


# ─────────────────────────────────────────────────────────────────────────────
# TIER 1: Exact service_code → schema
# Source: Cradle_to_Death_MDAs.md + individual BPR TO-BE process docs
# ─────────────────────────────────────────────────────────────────────────────

CODE_SCHEMAS = {
    # ── CRS: Birth Registration ──
    # Source: _CIVIL_REGISTRATION_SERVICES_CRS____Service_Delivery.md
    "INT-CIV-001": {
        "title": "Birth Registration",
        "type": "object",
        "required": ["mother_id", "date_of_birth", "place_of_birth", "county", "phone_number"],
        "properties": {
            "header_1": _s("Child Information", "Details of the newborn"),
            "child_name": _f("Full Name of Child"),
            "date_of_birth": _f("Date of Birth", format="date"),
            "gender": _f("Gender", enum=["Male", "Female"]),
            "place_of_birth": _f("Place of Birth (Hospital / Location)"),
            "header_2": _s("Parental Information", "Once-Only: Bio-data auto-fetched from IPRS"),
            "mother_id": _f("Mother's National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
            "father_id": _f("Father's National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
            "header_3": _s("Location & Contact"),
            "county": _f("County"),
            "sub_county": _f("Sub-County"),
            "phone_number": _f("Parent/Guardian Phone Number"),
        },
    },
    # ── CRS: Death Registration ──
    "INT-CIV-002": {
        "title": "Death Registration",
        "type": "object",
        "required": ["deceased_name", "date_of_death", "place_of_death", "cause_of_death", "informant_id", "informant_phone"],
        "properties": {
            "header_1": _s("Deceased Information"),
            "deceased_name": _f("Full Name of Deceased"),
            "deceased_id": _f("Deceased National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
            "date_of_death": _f("Date of Death", format="date"),
            "place_of_death": _f("Place of Death (Hospital / Location)"),
            "cause_of_death": _f("Cause of Death"),
            "gender": _f("Gender", enum=["Male", "Female"]),
            "header_2": _s("Informant (Next of Kin)"),
            "informant_name": _f("Informant's Full Name"),
            "informant_id": _f("Informant's ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
            "informant_phone": _f("Informant's Phone Number"),
            "relationship_to_deceased": _f("Relationship to Deceased"),
            "header_3": _s("Location"),
            "county": _f("County"),
        },
    },
    # ── CRS: Issuance of Birth Certificate ──
    "INT-CIV-003": {
        "title": "Issuance of Birth Certificate",
        "type": "object",
        "required": ["applicant_id", "childs_full_name", "date_of_birth", "county", "phone_number"],
        "properties": {
            "header_1": _s("Applicant Information", "Person requesting the certificate"),
            "applicant_id": _f("Applicant National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
            "relationship_to_child": _f("Relationship to Child", enum=["Parent", "Guardian", "Self", "Government Agency"]),
            "header_2": _s("Child Details"),
            "childs_full_name": _f("Child's Full Name"),
            "date_of_birth": _f("Child's Date of Birth", format="date"),
            "birth_notification_number": _f("Birth Notification Number"),
            "upi": _f("Unique Personal Identifier (Maisha Namba)", lookup_service="CRS", lookup_action="verify_birth"),
            "header_3": _s("Location & Contact"),
            "county": _f("County of Registration"),
            "phone_number": _f("Phone Number"),
        },
    },
    # ── Immigration: Passport Application ──
    # Source: STATE_DEPARTMENT_FOR_IMMIGRATION_AND_CITIZEN_SERVICES___Passport_Application.md
    "INT-IMM-001": {
        "title": "Passport Application & Issuance",
        "type": "object",
        "required": ["id_number", "passport_type", "phone_number"],
        "properties": {
            "header_1": _s("Personal Identity", "Once-Only: Bio-data auto-fetched from IPRS/Maisha Namba"),
            "id_number": _f("Citizen ID (Maisha Namba)", lookup_service="IPRS", lookup_action="get_person_details"),
            "birth_cert_no": _f("Birth Certificate Number", lookup_service="CRS", lookup_action="verify_birth"),
            "header_2": _s("Passport Configuration"),
            "passport_type": _f("Passport Type", enum=["32 Pages", "50 Pages", "66 Pages"]),
            "application_type": _f("Application Type", enum=["First Time", "Renewal", "Replacement", "Change of Details"]),
            "reason_for_travel": _f("Reason for Travel", enum=["Tourism", "Business", "Medical", "Education", "Other"]),
            "header_3": _s("Delivery & Contact"),
            "delivery_address": _f("Delivery Address"),
            "county": _f("County of Residence"),
            "phone_number": _f("Phone Number"),
            "email": _f("Email Address"),
            "emergency_contact": _f("Emergency Contact"),
            "header_4": _s("Digital Uploads"),
            "photo": _f("Passport Photo (ICAO Compliant)", format="data-url"),
            "recommender_id": _f("Recommender ID (Optional)"),
            "header_5": _s("Verification (Internal Use Only)"),
            "security_clearance_status": _f("Security Clearance Status", enum=["Clear", "Flagged", "Under Investigation"], internal_only=True),
            "intelligence_notes": _f("Internal Intelligence Notes", field_type="textarea", internal_only=True),
        },
    },
    # ── NRB: National ID Application ──
    "INT-REG-001": {
        "title": "National Identity Card Registration",
        "type": "object",
        "required": ["birth_certificate_number", "date_of_birth", "county_of_birth", "county_of_residence", "phone_number"],
        "properties": {
            "header_1": _s("Personal Details", "Once-Only: Verified against CRS birth record"),
            "birth_certificate_number": _f("Birth Certificate Number", lookup_service="CRS", lookup_action="verify_birth"),
            "date_of_birth": _f("Date of Birth", format="date"),
            "gender": _f("Gender", enum=["Male", "Female"]),
            "header_2": _s("Parentage"),
            "fathers_name": _f("Father's Full Name"),
            "fathers_id": _f("Father's ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
            "mothers_name": _f("Mother's Full Name"),
            "mothers_id": _f("Mother's ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
            "header_3": _s("Location"),
            "county_of_birth": _f("County of Birth"),
            "county_of_residence": _f("County of Residence"),
            "sub_county": _f("Sub-County"),
            "ward": _f("Ward"),
            "phone_number": _f("Phone Number"),
            "header_4": _s("Security Vetting (Staff Only)"),
            "criminal_record_check": _f("Criminal Record Status", enum=["No Record", "Record Found", "Action Required"], internal_only=True),
            "fingerprint_verification": _f("Fingerprint Match Probability (%)", field_type="number", internal_only=True),
        },
    },
    # ── BRS: Business Name Registration ──
    # Source: Business_Registration_Service___Service_Delivery.md (Cradle_to_Death_MDAs.md)
    "TRD-BUS-001": {
        "title": "Business Name Registration",
        "type": "object",
        "required": ["proposed_business_name", "business_type", "nature_of_business", "applicant_id", "kra_pin", "phone_number", "email"],
        "properties": {
            "header_1": _s("Business Details"),
            "proposed_business_name": _f("Proposed Business Name"),
            "business_type": _f("Business Type", enum=["Sole Proprietor", "Partnership"]),
            "nature_of_business": _f("Nature of Business / Activity"),
            "business_physical_address": _f("Business Physical Address"),
            "county": _f("County"),
            "postal_address": _f("Postal Address"),
            "header_2": _s("Proprietor / Partner", "Once-Only: Identity verified via IPRS, tax via KRA"),
            "applicant_name": _f("Proprietor / Partner Full Name"),
            "applicant_id": _f("National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
            "kra_pin": _f("KRA PIN", lookup_service="KRA", lookup_action="verify_pin"),
            "header_3": _s("Contact"),
            "phone_number": _f("Phone Number"),
            "email": _f("Email Address"),
        },
    },
    # ── BRS: Company Incorporation ──
    "TRD-BUS-002": {
        "title": "Company Incorporation",
        "type": "object",
        "required": ["proposed_company_name", "company_type", "nature_of_business", "director1_id", "director1_kra_pin", "share_capital", "phone_number", "email"],
        "properties": {
            "header_1": _s("Company Details"),
            "proposed_company_name": _f("Proposed Company Name"),
            "company_type": _f("Company Type", enum=["Private Limited (Ltd)", "Public Limited (PLC)", "Company Limited by Guarantee"]),
            "nature_of_business": _f("Nature of Business"),
            "registered_office_address": _f("Registered Office Address"),
            "county": _f("County"),
            "share_capital": _f("Authorised Share Capital (KES)", field_type="number"),
            "header_2": _s("Director 1", "Once-Only: Identity & tax compliance verified automatically"),
            "director1_name": _f("Director 1 – Full Name"),
            "director1_id": _f("Director 1 – ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
            "director1_kra_pin": _f("Director 1 – KRA PIN", lookup_service="KRA", lookup_action="verify_pin"),
            "header_3": _s("Director 2 (Optional)"),
            "director2_name": _f("Director 2 – Full Name"),
            "director2_id": _f("Director 2 – ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
            "header_4": _s("Contact"),
            "phone_number": _f("Contact Phone Number"),
            "email": _f("Contact Email Address"),
        },
    },
    # ── KRA: Tax Return Filing / PIN Registration ──
    # Source: Kenya_Revenue_Authority___Tax_Return_Filing.md
    "TRE-REV-001": {
        "title": "KRA PIN Registration & Tax Return Filing",
        "type": "object",
        "required": ["taxpayer_type", "id_number", "phone_number", "email", "county"],
        "properties": {
            "header_1": _s("Taxpayer Details", "Once-Only: Identity auto-verified via IPRS"),
            "taxpayer_type": _f("Taxpayer Type", enum=["Individual", "Non-Individual / Business"]),
            "id_number": _f("National ID / Passport Number", lookup_service="IPRS", lookup_action="get_person_details"),
            "date_of_birth": _f("Date of Birth (Individuals)", format="date"),
            "header_2": _s("Location & Employment"),
            "county": _f("County"),
            "physical_address": _f("Physical / Business Address"),
            "business_nature": _f("Nature of Business (Non-Individual)"),
            "header_3": _s("Contact"),
            "phone_number": _f("Phone Number"),
            "email": _f("Email Address"),
            "header_4": _s("Risk Assessment (Staff Only)"),
            "tax_risk_profile": _f("Tax Compliance Risk Profile", enum=["Low Risk", "Medium Risk", "High Risk / Auditable"], internal_only=True),
            "internal_compliance_notes": _f("Compliance Officer Rationale", field_type="textarea", internal_only=True),
        },
    },
    # ── KRA: Tax Compliance Certificate ──
    "TRE-REV-004": {
        "title": "Tax Compliance Certificate",
        "type": "object",
        "required": ["kra_pin", "tax_types", "tax_period_from", "tax_period_to", "phone_number", "email"],
        "properties": {
            "header_1": _s("Taxpayer Information", "Once-Only: Compliance status auto-scored via iTax"),
            "taxpayer_name": _f("Taxpayer / Business Name"),
            "kra_pin": _f("KRA PIN (Personal or Business)", lookup_service="KRA", lookup_action="verify_pin"),
            "id_number": _f("National ID Number (for individuals)", lookup_service="IPRS", lookup_action="get_person_details"),
            "header_2": _s("Compliance Period"),
            "tax_types": _f("Tax Types Covered (e.g. Income Tax, VAT)"),
            "tax_period_from": _f("Compliance Period From", format="date"),
            "tax_period_to": _f("Compliance Period To", format="date"),
            "purpose_of_certificate": _f("Purpose (e.g. Tender, Loan)"),
            "header_3": _s("Contact"),
            "phone_number": _f("Phone Number"),
            "email": _f("Email Address"),
        },
    },
    # ── NTSA: Driving License Renewal ──
    # Source: NATIONAL_TRANSPORT_AND_SAFETY_AUTHORITY_NTSA____Driving_License_Renewal.md
    "TRN-DRV-001": {
        "title": "Driving License Renewal",
        "type": "object",
        "required": ["id_number", "licence_class", "phone_number", "county"],
        "properties": {
            "header_1": _s("Personal Identity", "Once-Only: Bio-data & photo fetched from IPRS/Maisha Namba"),
            "id_number": _f("National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
            "date_of_birth": _f("Date of Birth", format="date"),
            "gender": _f("Gender", enum=["Male", "Female"]),
            "header_2": _s("Licence Details"),
            "licence_class": _f("Licence Class", enum=["Class A (Motorcycle)", "Class B (Light Vehicle)", "Class C (Heavy Vehicle)", "Class D (Bus/PSV)", "Class E (Trailer)"]),
            "is_renewal": _f("Is this a Renewal?", field_type="boolean"),
            "existing_licence_number": _f("Existing Licence Number (Renewal Only)"),
            "blood_group": _f("Blood Group", enum=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"]),
            "header_3": _s("Contact"),
            "county": _f("County of Residence"),
            "phone_number": _f("Phone Number"),
        },
    },
    # ── NTSA: Vehicle Registration ──
    "TRN-VEH-001": {
        "title": "Motor Vehicle Registration",
        "type": "object",
        "required": ["owner_id", "owner_kra_pin", "vehicle_make", "chassis_number", "phone_number"],
        "properties": {
            "header_1": _s("Owner Details", "Once-Only: Identity & KRA PIN verified via X-Road"),
            "owner_name": _f("Vehicle Owner Full Name"),
            "owner_id": _f("Owner National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
            "owner_kra_pin": _f("Owner KRA PIN", lookup_service="KRA", lookup_action="verify_pin"),
            "header_2": _s("Vehicle Details"),
            "vehicle_make": _f("Vehicle Make (e.g. Toyota)"),
            "vehicle_model": _f("Vehicle Model (e.g. Corolla)"),
            "year_of_manufacture": _f("Year of Manufacture", field_type="number"),
            "engine_number": _f("Engine Number"),
            "chassis_number": _f("Chassis Number"),
            "vehicle_color": _f("Vehicle Colour"),
            "fuel_type": _f("Fuel Type", enum=["Petrol", "Diesel", "Electric", "Hybrid"]),
            "header_3": _s("Contact"),
            "phone_number": _f("Contact Phone Number"),
        },
    },
    # ── Lands: Transfer of Land Ownership ──
    # Source: STATE_DEPARTMENT_FOR_LANDS_AND_PHYSICAL_PLANNING___Service_Delivery.md
    "LND-ADM-003": {
        "title": "Transfer of Land Ownership",
        "type": "object",
        "required": ["title_deed_number", "land_reference_number", "seller_id", "buyer_id", "agreed_purchase_price", "phone_number"],
        "properties": {
            "header_1": _s("Land Details", "Auto-verified against Ardhisasa land registry"),
            "title_deed_number": _f("Title Deed Number"),
            "land_reference_number": _f("Land Reference Number (LR No.)"),
            "county": _f("County"),
            "header_2": _s("Seller / Transferor", "Once-Only: Biometric consent & encumbrance check"),
            "seller_name": _f("Seller Full Name"),
            "seller_id": _f("Seller National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
            "seller_kra_pin": _f("Seller KRA PIN", lookup_service="KRA", lookup_action="verify_pin"),
            "header_3": _s("Buyer / Transferee"),
            "buyer_name": _f("Buyer Full Name"),
            "buyer_id": _f("Buyer National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
            "buyer_kra_pin": _f("Buyer KRA PIN", lookup_service="KRA", lookup_action="verify_pin"),
            "header_4": _s("Transaction"),
            "agreed_purchase_price": _f("Agreed Purchase Price (KES)", field_type="number"),
            "advocate_name": _f("Conveyancing Advocate Name"),
            "phone_number": _f("Contact Phone Number"),
        },
    },
    # ── NHIF/SHA: Registration ──
    # Source: Ministry_of_Health___Service_Delivery.md (SHA auto-enrollment)
    "HLT-INS-001": {
        "title": "Social Health Authority (SHA) Registration",
        "type": "object",
        "required": ["id_number", "employment_type", "phone_number", "county"],
        "properties": {
            "header_1": _s("Personal Information", "Once-Only: Bio-data auto-fetched from IPRS/Maisha Namba"),
            "id_number": _f("National ID / Passport Number", lookup_service="IPRS", lookup_action="get_person_details"),
            "date_of_birth": _f("Date of Birth", format="date"),
            "gender": _f("Gender", enum=["Male", "Female"]),
            "header_2": _s("Employment & Residence"),
            "employment_type": _f("Employment Type", enum=["Formal Employment", "Self-Employed", "Unemployed", "Student"]),
            "employer_name": _f("Employer Name (if employed)"),
            "county": _f("County of Residence"),
            "header_3": _s("Health Preferences"),
            "preferred_hospital": _f("Preferred Health Facility"),
            "has_dependants": _f("Do you have dependants to add?", field_type="boolean"),
            "header_4": _s("Contact"),
            "phone_number": _f("Phone Number"),
            "email": _f("Email Address"),
        },
    },
    # ── NHIF/SHA: Dependant Addition ──
    "HLT-INS-002": {
        "title": "SHA Dependant Addition",
        "type": "object",
        "required": ["member_id", "dependant_full_name", "relationship", "dependant_date_of_birth", "phone_number"],
        "properties": {
            "header_1": _s("Member Information"),
            "member_id": _f("NHIF/SHA Member Number or ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
            "header_2": _s("Dependant Details"),
            "dependant_full_name": _f("Dependant's Full Name"),
            "relationship": _f("Relationship", enum=["Spouse", "Child", "Parent", "Sibling"]),
            "dependant_date_of_birth": _f("Dependant's Date of Birth", format="date"),
            "dependant_id": _f("Dependant's ID / Birth Cert Number", lookup_service="CRS", lookup_action="verify_birth"),
            "header_3": _s("Contact"),
            "phone_number": _f("Phone Number"),
        },
    },
    # ── Education: Registration of Basic Education Institutions ──
    "EDU-BAS-001": {
        "title": "Registration of Basic Education Institutions",
        "type": "object",
        "required": ["institution_name", "institution_type", "county", "proprietor_id", "phone_number", "email"],
        "properties": {
            "header_1": _s("Institution Details"),
            "institution_name": _f("Institution Name"),
            "institution_type": _f("Institution Type", enum=["Pre-Primary", "Primary", "Junior Secondary", "Special Needs School"]),
            "header_2": _s("Location"),
            "county": _f("County"),
            "sub_county": _f("Sub-County"),
            "ward": _f("Ward"),
            "postal_address": _f("Postal Address"),
            "header_3": _s("Proprietor / Sponsor", "Once-Only: Identity verified via IPRS"),
            "proprietor_name": _f("Proprietor / Sponsor Name"),
            "proprietor_id": _f("Proprietor ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
            "land_ownership_type": _f("Land Ownership Type", enum=["Owned", "Leased", "Government-Allocated"]),
            "expected_enrolment": _f("Expected Initial Enrolment", field_type="number"),
            "header_4": _s("Contact"),
            "phone_number": _f("Contact Phone Number"),
            "email": _f("Email Address"),
        },
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# TIER 2: MDA name / service_name pattern → schema
# Source: Individual BPR docs in /mdas/docs_final/priority_mdas/
# ─────────────────────────────────────────────────────────────────────────────

MDA_SCHEMAS = [
    # ── NEMA: EIA Licensing ──
    # Source: National_Environment_Management_Authority___Service_Delivery.md
    (
        ["nema", "environment management authority", "eia", "environmental impact"],
        "nema_eia",
        {
            "title": "Environmental Impact Assessment (EIA) Licensing",
            "type": "object",
            "required": ["applicant_name", "applicant_id", "project_name", "project_location", "county", "phone_number"],
            "properties": {
                "header_1": _s("Proponent Details", "Once-Only: Business registration verified via BRS, tax via KRA"),
                "applicant_name": _f("Proponent / Company Name"),
                "applicant_id": _f("National ID / Registration Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "kra_pin": _f("KRA PIN", lookup_service="KRA", lookup_action="verify_pin"),
                "business_registration": _f("Business Registration Number", lookup_service="BRS", lookup_action="verify_registration"),
                "header_2": _s("Project Details", "Cadastral data auto-fetched from Ardhisasa"),
                "project_name": _f("Project Name"),
                "project_type": _f("Project Type", enum=["Residential", "Commercial", "Industrial", "Infrastructure", "Mining", "Agricultural"]),
                "project_location": _f("Project Location (GPS / Address)"),
                "county": _f("County"),
                "land_reference": _f("Land Reference Number"),
                "estimated_cost": _f("Estimated Project Cost (KES)", field_type="number"),
                "header_3": _s("Expert & Contact"),
                "expert_name": _f("Registered Environmental Expert Name"),
                "expert_nema_number": _f("Expert NEMA Registration Number"),
                "phone_number": _f("Contact Phone Number"),
                "email": _f("Email Address"),
                "header_4": _s("Attachments"),
                "eia_report": _f("EIA Project Report (PDF)", format="data-url"),
            },
        },
    ),
    # ── AFA: Farmer Registration & Licensing ──
    # Source: Agriculture_and_Food_Authority___Service_Delivery.md
    (
        ["agriculture and food authority", "afa", "farmer registration"],
        "afa_licensing",
        {
            "title": "AFA Farmer Registration & Licensing",
            "type": "object",
            "required": ["applicant_id", "kra_pin", "license_type", "county", "phone_number"],
            "properties": {
                "header_1": _s("Applicant Details", "Once-Only: Business via BRS, tax via KRA, farm data via KIAMIS"),
                "applicant_name": _f("Applicant / Business Name"),
                "applicant_id": _f("National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "kra_pin": _f("KRA PIN", lookup_service="KRA", lookup_action="verify_pin"),
                "header_2": _s("Licence Details"),
                "license_type": _f("Licence Type", enum=["Farmer Registration", "Trading Licence", "Export Permit", "Processing Licence"]),
                "crop_type": _f("Scheduled Crop", enum=["Coffee", "Tea", "Nuts", "Pyrethrum", "Sisal", "Other"]),
                "header_3": _s("Farm / Activity Location"),
                "farm_location": _f("Farm / Activity Location"),
                "farm_size": _f("Farm Size (Acres)"),
                "county": _f("County"),
                "header_4": _s("Contact"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
            },
        },
    ),
    # ── Children Services: Child Protection Case Management ──
    # Source: State_Department_for_Children_Services___Service_Delivery.md
    (
        ["children services", "child protection", "cpims"],
        "child_protection",
        {
            "title": "Child Protection Case Reporting",
            "type": "object",
            "required": ["reporter_id", "child_name", "incident_type", "county", "phone_number"],
            "properties": {
                "header_1": _s("Reporter Information", "Once-Only: Identity verified via IPRS"),
                "reporter_id": _f("Reporter's National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "reporter_relationship": _f("Relationship to Child", enum=["Parent", "Guardian", "Teacher", "Neighbour", "Health Worker", "Police", "Other"]),
                "header_2": _s("Child Details"),
                "child_name": _f("Child's Full Name"),
                "child_date_of_birth": _f("Child's Date of Birth (Approximate)", format="date"),
                "child_gender": _f("Child's Gender", enum=["Male", "Female"]),
                "child_upi": _f("Child's Maisha Namba / UPI (if known)", lookup_service="CRS", lookup_action="verify_birth"),
                "header_3": _s("Incident Details"),
                "incident_type": _f("Incident Type", enum=["Neglect", "Physical Abuse", "Sexual Abuse", "Child Labour", "Abandonment", "Trafficking", "Other"]),
                "incident_description": _f("Incident Description", format="textarea"),
                "incident_date": _f("Date of Incident (Approximate)", format="date"),
                "header_4": _s("Location & Contact"),
                "county": _f("County"),
                "sub_county": _f("Sub-County"),
                "location_details": _f("Location Details"),
                "phone_number": _f("Reporter Phone Number"),
            },
        },
    ),
    # ── Energy: Energy Licensing ──
    # Source: Energy___Service_Delivery.md
    (
        ["state department for energy", "energy licensing", "epra"],
        "energy_licensing",
        {
            "title": "Energy Permit Application",
            "type": "object",
            "required": ["applicant_id", "permit_type", "phone_number"],
            "properties": {
                "header_1": _s("Applicant Details", "Once-Only: Entity verified via EPRA & BRS"),
                "applicant_name": _f("Applicant / Entity Name"),
                "applicant_id": _f("National ID / Registration Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "kra_pin": _f("KRA PIN", lookup_service="KRA", lookup_action="verify_pin"),
                "header_2": _s("Permit Details"),
                "permit_type": _f("Permit Type", enum=["Generation Licence", "Transmission Licence", "Distribution Licence", "Retail Supply Licence", "Import/Export Permit"]),
                "facility_location": _f("Facility / Premises Address"),
                "county": _f("County"),
                "header_3": _s("Contact"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
                "header_4": _s("Attachments"),
                "supporting_document": _f("Supporting Document (PDF)", format="data-url"),
            },
        },
    ),
    # ── KNQA: Qualification Validation ──
    # Source: Kenya_National_Qualifications_Authority___Service_Delivery.md
    (
        ["national qualifications authority", "knqa", "qualification validation", "recognition of prior learning"],
        "knqa_validation",
        {
            "title": "Qualification Validation & Recognition",
            "type": "object",
            "required": ["id_number", "institution_name", "qualification_name", "year_obtained", "phone_number"],
            "properties": {
                "header_1": _s("Applicant Identity", "Once-Only: Credentials auto-fetched from national registries"),
                "id_number": _f("National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_2": _s("Qualification Details"),
                "institution_name": _f("Name of Awarding Institution", lookup_service="KNQA_REGISTRY", lookup_action="verify_institution"),
                "institution_country": _f("Country of Institution"),
                "qualification_type": _f("Qualification Type", enum=["Certificate", "Diploma", "Higher Diploma", "Bachelors Degree", "Masters Degree", "Doctorate (PhD)"]),
                "qualification_name": _f("Exact Title of Qualification"),
                "year_obtained": _f("Year Obtained", field_type="number"),
                "certificate_number": _f("Certificate / Transcript Number"),
                "header_3": _s("Validation Purpose"),
                "purpose": _f("Purpose of Validation", enum=["Employment", "Further Study", "Immigration", "Professional Registration", "Other"]),
                "header_4": _s("Contact"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
                "header_5": _s("Attachments"),
                "certificate_upload": _f("Certificate / Transcript Scan (PDF)", format="data-url"),
            },
        },
    ),
    # ── NACOSTI: Research Licensing ──
    # Source: National_Commission_For_Science_Technology_and_Innovation___Service_Delivery.md
    (
        ["nacosti", "science, technology and innovation", "research licen"],
        "nacosti_research",
        {
            "title": "Research Licence Application",
            "type": "object",
            "required": ["id_number", "research_title", "institution_name", "phone_number"],
            "properties": {
                "header_1": _s("Researcher Details", "Once-Only: Personal & institutional data pre-populated via IPRS/CUE"),
                "id_number": _f("National ID / Passport Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_2": _s("Research Details"),
                "research_title": _f("Research Title"),
                "research_area": _f("Research Area", enum=["Health Sciences", "Social Sciences", "Natural Sciences", "Technology", "Education", "Agriculture", "Other"]),
                "institution_name": _f("Affiliated Institution", lookup_service="KNQA_REGISTRY", lookup_action="verify_institution"),
                "ethics_clearance_status": _f("Ethics Clearance Status", enum=["Obtained", "Pending", "Not Required"]),
                "study_county": _f("County of Study"),
                "expected_duration": _f("Expected Duration (Months)", field_type="number"),
                "header_3": _s("Contact"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
                "header_4": _s("Attachments"),
                "research_proposal": _f("Research Proposal (PDF)", format="data-url"),
            },
        },
    ),
    # ── KBC: Archival Access & Content Licensing ──
    # Source: Kenya_Broadcasting_Corporation___Service_Delivery.md
    (
        ["broadcasting corporation", "kbc", "archival access", "content licen"],
        "kbc_archival",
        {
            "title": "KBC Archival Access & Content Licensing",
            "type": "object",
            "required": ["id_number", "content_description", "license_type", "phone_number"],
            "properties": {
                "header_1": _s("Applicant Details"),
                "applicant_name": _f("Applicant / Organisation Name"),
                "id_number": _f("National ID / Registration Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_2": _s("Content Request"),
                "content_description": _f("Content Description / Keywords"),
                "content_period": _f("Content Period (Year Range)"),
                "content_format": _f("Preferred Format", enum=["Video (MP4)", "Audio (MP3)", "Photograph", "Transcript"]),
                "license_type": _f("Licence Type", enum=["Commercial", "Academic / Research", "Personal", "Government"]),
                "header_3": _s("Contact"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
            },
        },
    ),
    # ── Youth Affairs: Youth Internship & AGPO ──
    # Source: Youth_Affairs___Service_Delivery.md
    (
        ["youth affairs", "youth internship", "agpo", "psip"],
        "youth_affairs",
        {
            "title": "Youth Internship Placement & AGPO Registration",
            "type": "object",
            "required": ["id_number", "application_type", "phone_number"],
            "properties": {
                "header_1": _s("Applicant Identity", "Once-Only: Personal & education details pre-populated via IPRS/NEMIS"),
                "id_number": _f("Maisha Namba / National ID", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_2": _s("Application Details"),
                "application_type": _f("Application Type", enum=["PSIP Youth Internship", "AGPO Registration"]),
                "highest_qualification": _f("Highest Qualification", enum=["Certificate", "Diploma", "Degree", "Masters", "PhD"]),
                "field_of_study": _f("Field of Study"),
                "header_3": _s("AGPO Details (if applicable)"),
                "business_name": _f("Youth-Owned Business Name"),
                "business_registration_no": _f("Business Registration Number", lookup_service="BRS", lookup_action="verify_registration"),
                "header_4": _s("Contact"),
                "county": _f("County of Residence"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
            },
        },
    ),
    # ── Culture & Heritage: Ushanga Kenya ──
    # Source: Culture_and_Heritage___Service_Delivery.md
    (
        ["culture, arts and heritage", "culture and heritage", "ushanga"],
        "ushanga_kenya",
        {
            "title": "Ushanga Kenya – Cooperative & Product Registration",
            "type": "object",
            "required": ["cooperative_name", "representative_id", "county", "phone_number"],
            "properties": {
                "header_1": _s("Cooperative Details"),
                "cooperative_name": _f("Cooperative / Group Name"),
                "cooperative_registration_no": _f("Cooperative Registration Number"),
                "header_2": _s("Representative", "Once-Only: Identity verified via IPRS"),
                "representative_name": _f("Representative Full Name"),
                "representative_id": _f("Representative National ID", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_3": _s("Product Details"),
                "product_category": _f("Product Category", enum=["Beadwork", "Weaving", "Pottery", "Woodwork", "Other"]),
                "estimated_quantity": _f("Estimated Quantity (Units)", field_type="number"),
                "header_4": _s("Location & Contact"),
                "county": _f("County"),
                "phone_number": _f("Phone Number"),
            },
        },
    ),
    # ── Sports: Federation Registration, Grants & Facility Booking ──
    # Source: Sports_and_the_Arts___Service_Delivery.md
    (
        ["state department for sports", "sports and the arts", "federation registration", "athlete grant", "facility booking"],
        "sports_services",
        {
            "title": "Sports Services – Registration, Grants & Facilities",
            "type": "object",
            "required": ["id_number", "service_type", "phone_number"],
            "properties": {
                "header_1": _s("Applicant Identity", "Once-Only: Athlete data fetched via IPRS/NEMIS/KNQA"),
                "id_number": _f("Maisha Namba / National ID", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_2": _s("Service Request"),
                "service_type": _f("Service Type", enum=["Federation Registration", "Athlete Grant Application", "Facility Booking"]),
                "federation_name": _f("Federation / Association Name (if applicable)"),
                "sport_discipline": _f("Sport Discipline"),
                "header_3": _s("Facility Booking (if applicable)"),
                "facility_name": _f("Facility Name"),
                "preferred_date": _f("Preferred Date", format="date"),
                "duration_hours": _f("Duration (Hours)", field_type="number"),
                "header_4": _s("Contact"),
                "county": _f("County"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
            },
        },
    ),
    # ── MSME: Credit & Fund Management ──
    # Source: Micro_Small_and_Medium_Enterprise_Development___Service_Delivery.md
    (
        ["msme development", "micro, small", "hustler fund", "uwezo fund"],
        "msme_credit",
        {
            "title": "MSME Credit & Fund Application",
            "type": "object",
            "required": ["id_number", "fund_type", "phone_number"],
            "properties": {
                "header_1": _s("Applicant Identity", "Once-Only: Business history fetched from BRS, tax from KRA"),
                "id_number": _f("Maisha Namba / National ID", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_2": _s("Fund Details"),
                "fund_type": _f("Fund Type", enum=["Hustler Fund (Individual)", "Uwezo Fund (Group)", "MSME Fund", "NYOTA Apprenticeship"]),
                "requested_amount": _f("Requested Amount (KES)", field_type="number"),
                "header_3": _s("Business Details"),
                "business_name": _f("Business Name (if registered)"),
                "business_registration_no": _f("Business Registration No", lookup_service="BRS", lookup_action="verify_registration"),
                "kra_pin": _f("KRA PIN", lookup_service="KRA", lookup_action="verify_pin"),
                "business_sector": _f("Business Sector", enum=["Agriculture", "Manufacturing", "Trade", "Services", "Technology", "Other"]),
                "header_4": _s("Group Details (Uwezo Fund Only)"),
                "group_name": _f("Group Name"),
                "member_count": _f("Number of Members", field_type="number"),
                "header_5": _s("Contact"),
                "county": _f("County"),
                "phone_number": _f("Phone Number"),
            },
        },
    ),
    # ── Correctional Services: Inmate Case Management (G2G) ──
    # Source: STATE_DEPARTMENT_FOR_CORRECTIONAL_SERVICES___Service_Delivery.md
    (
        ["correctional services", "inmate", "prison"],
        "correctional_g2g",
        {
            "title": "Inmate Case Management (G2G)",
            "type": "object",
            "required": ["inmate_id", "warrant_reference", "facility_name", "officer_id"],
            "properties": {
                "header_1": _s("Inmate Identity", "Once-Only: Biometric verification against IPRS"),
                "inmate_name": _f("Inmate Full Name"),
                "inmate_id": _f("Inmate National ID / Maisha Namba", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_2": _s("Case Details"),
                "warrant_reference": _f("Court Committal Warrant Reference"),
                "offense_category": _f("Offense Category", enum=["Petty", "Misdemeanor", "Felony", "Capital"]),
                "sentence_duration": _f("Sentence Duration (Months)", field_type="number"),
                "header_3": _s("Facility Assignment"),
                "facility_name": _f("Correctional Facility"),
                "security_classification": _f("Security Classification", enum=["Minimum", "Medium", "Maximum"]),
                "header_4": _s("Admitting Officer"),
                "officer_id": _f("Admitting Officer ID", lookup_service="IPRS", lookup_action="get_person_details"),
            },
        },
    ),
    # ── Refugee Services: Refugee Status Determination ──
    # Source: _REFUGEE_SERVICES___Service_Delivery.md
    (
        ["refugee services", "refugee status", "asylum"],
        "refugee_rsd",
        {
            "title": "Refugee Status Determination & Documentation",
            "type": "object",
            "required": ["full_name", "nationality", "date_of_birth", "gender", "phone_number"],
            "properties": {
                "header_1": _s("Personal Information"),
                "full_name": _f("Full Name (as in Travel Document)"),
                "nationality": _f("Country of Origin"),
                "date_of_birth": _f("Date of Birth", format="date"),
                "gender": _f("Gender", enum=["Male", "Female"]),
                "passport_number": _f("Passport / Travel Document Number"),
                "header_2": _s("Application Details"),
                "entry_point": _f("Point of Entry into Kenya"),
                "date_of_entry": _f("Date of Entry", format="date"),
                "reason_for_asylum": _f("Reason for Seeking Asylum", format="textarea"),
                "header_3": _s("Family Details"),
                "accompanied_by": _f("Number of Accompanying Family Members", field_type="number"),
                "header_4": _s("Contact & Location"),
                "current_location": _f("Current Location / Camp"),
                "phone_number": _f("Phone Number (if available)"),
            },
        },
    ),
    # ── Special Programmes: Social Protection & Beneficiary Management ──
    # Source: State_Department_for_Special_Programmes___Service_Delivery.md
    (
        ["special programmes", "social protection", "beneficiary management", "safety net"],
        "social_protection",
        {
            "title": "Social Protection Beneficiary Registration",
            "type": "object",
            "required": ["id_number", "programme_type", "county", "phone_number"],
            "properties": {
                "header_1": _s("Beneficiary Identity", "Once-Only: Identity verified biometrically via IPRS/Maisha Namba"),
                "id_number": _f("National ID / Maisha Namba", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_2": _s("Programme Details"),
                "programme_type": _f("Programme Type", enum=["Cash Transfer – Elderly", "Cash Transfer – OVC", "Cash Transfer – PWD", "Emergency Relief", "Hunger Safety Net"]),
                "header_3": _s("Household Information"),
                "household_size": _f("Household Size", field_type="number"),
                "monthly_income_estimate": _f("Estimated Monthly Income (KES)", field_type="number"),
                "header_4": _s("Location & Contact"),
                "county": _f("County"),
                "sub_county": _f("Sub-County"),
                "ward": _f("Ward"),
                "phone_number": _f("Phone Number (for M-Pesa disbursement)"),
            },
        },
    ),
    # ── Cabinet Office: Cabinet Memorandum Processing (G2G) ──
    # Source: CABINET_OFFICE___Service_Delivery.md
    (
        ["cabinet affairs", "cabinet office", "cabinet memorandum", "cabmemo"],
        "cabinet_g2g",
        {
            "title": "Cabinet Memorandum Submission (G2G)",
            "type": "object",
            "required": ["memo_title", "originating_ministry", "cs_name", "officer_id"],
            "properties": {
                "header_1": _s("Memorandum Details"),
                "memo_title": _f("Memorandum Title"),
                "memo_category": _f("Category", enum=["Policy", "Legislation", "Budget", "International Agreement", "Administrative"]),
                "originating_ministry": _f("Originating Ministry / Department"),
                "header_2": _s("Sponsoring Officials"),
                "cs_name": _f("Cabinet Secretary Name"),
                "ps_name": _f("Principal Secretary Name"),
                "officer_id": _f("Submitting Officer ID", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_3": _s("Fiscal Impact"),
                "has_fiscal_impact": _f("Has Fiscal Impact?", field_type="boolean"),
                "estimated_cost": _f("Estimated Cost (KES)", field_type="number"),
                "header_4": _s("Attachments"),
                "memo_document": _f("Signed Memorandum (PDF)", format="data-url"),
            },
        },
    ),
    # ── NGC: Inter-Agency Coordination (G2G) ──
    # Source: National_Government_Coordination___Service_Delivery.md
    (
        ["national government coordination", "inter-agency coordination", "information tasking"],
        "ngc_coordination_g2g",
        {
            "title": "Inter-Agency Coordination & Information Tasking (G2G)",
            "type": "object",
            "required": ["tasking_title", "priority_level", "target_mdas", "officer_id"],
            "properties": {
                "header_1": _s("Tasking Details"),
                "tasking_title": _f("Tasking Title"),
                "priority_level": _f("Priority", enum=["National Security", "Presidential Directive", "Routine Reporting", "Ad-Hoc"]),
                "description": _f("Scope & Deliverables", format="textarea"),
                "target_mdas": _f("Target MDAs (comma separated)"),
                "deadline": _f("Submission Deadline", format="date"),
                "header_2": _s("Originating Officer"),
                "officer_id": _f("Coordinator Officer ID", lookup_service="IPRS", lookup_action="get_person_details"),
            },
        },
    ),
    # ── ICT Authority: ICT Project Implementation (G2G) ──
    # Source: ICT_Authority___Service_Delivery.md
    (
        ["ict authority", "icta", "ict project", "digital infrastructure"],
        "icta_project_g2g",
        {
            "title": "Government ICT Project Submission (G2G)",
            "type": "object",
            "required": ["project_name", "requesting_mda", "estimated_budget", "officer_id"],
            "properties": {
                "header_1": _s("Project Overview"),
                "project_name": _f("Project Name"),
                "project_type": _f("Project Type", enum=["New System Development", "System Enhancement", "Infrastructure", "Cloud Migration", "Interoperability / X-Road", "Cybersecurity"]),
                "requesting_mda": _f("Requesting MDA"),
                "estimated_budget": _f("Estimated Budget (KES)", field_type="number"),
                "header_2": _s("Architecture Alignment"),
                "gea_aligned": _f("GEA Aligned?", field_type="boolean"),
                "shared_services_required": _f("Shared Services Required"),
                "header_3": _s("Responsible Officer"),
                "officer_id": _f("MDA ICT Officer ID", lookup_service="IPRS", lookup_action="get_person_details"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
            },
        },
    ),
    # ── OHPS / Chief of Staff: Executive Coordination (G2G) ──
    # Source: Office_of_the_Chief_of_Staff___Service_Delivery.md
    (
        ["head of public service", "ohps", "executive coordination", "presidential directive"],
        "ohps_executive_g2g",
        {
            "title": "Presidential Directive Tracking (G2G)",
            "type": "object",
            "required": ["directive_title", "lead_mda", "officer_id"],
            "properties": {
                "header_1": _s("Directive Details"),
                "directive_title": _f("Directive Title"),
                "directive_source": _f("Source", enum=["Presidential Speech", "Cabinet Decision", "Executive Order", "Inter-Ministerial"]),
                "lead_mda": _f("Lead MDA"),
                "supporting_mdas": _f("Supporting MDAs (comma separated)"),
                "deadline": _f("Target Completion Date", format="date"),
                "header_2": _s("KPIs & Milestones"),
                "kpis": _f("Key Performance Indicators", format="textarea"),
                "header_3": _s("Coordinating Officer"),
                "officer_id": _f("Coordinator ID", lookup_service="IPRS", lookup_action="get_person_details"),
            },
        },
    ),
    # ── PSC / Public Service Commission (G2G) ──
    (
        ["public service commission", "psc"],
        "psc_g2g",
        {
            "title": "Public Service Commission Directive (G2G)",
            "type": "object",
            "required": ["directive_title", "lead_mda", "officer_id"],
            "properties": {
                "header_1": _s("Directive Details"),
                "directive_title": _f("Directive / Policy Title"),
                "directive_type": _f("Type", enum=["HR Policy", "Recruitment", "Discipline", "Performance Review", "Training"]),
                "lead_mda": _f("Lead MDA"),
                "deadline": _f("Compliance Deadline", format="date"),
                "description": _f("Description & Requirements", format="textarea"),
                "header_2": _s("Originating Officer"),
                "officer_id": _f("PSC Officer ID", lookup_service="IPRS", lookup_action="get_person_details"),
            },
        },
    ),
    # ── Government Spokesperson: Public Communication (G2G) ──
    # Source: Government_Spokesperson___Service_Delivery.md
    (
        ["government spokesperson", "public communication"],
        "spokesperson_g2g",
        {
            "title": "Government Public Communication (G2G)",
            "type": "object",
            "required": ["message_title", "originating_office", "officer_id"],
            "properties": {
                "header_1": _s("Communication Details"),
                "message_title": _f("Communication Title"),
                "communication_type": _f("Type", enum=["Press Release", "Press Briefing", "Public Notice", "Advisory", "Response to Inquiry"]),
                "originating_office": _f("Originating Office / MDA"),
                "target_audience": _f("Target Audience", enum=["General Public", "Media", "Specific Sector", "International"]),
                "header_2": _s("Clearance"),
                "officer_id": _f("Communication Officer ID", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_3": _s("Attachments"),
                "communication_document": _f("Signed Communication (PDF)", format="data-url"),
            },
        },
    ),
    # ── Athi Water: Infrastructure Development ──
    # Source: Athi_Water_Works_Development_Agency___Service_Delivery.md
    (
        ["athi water", "awwda", "water works development"],
        "awwda_infrastructure",
        {
            "title": "Water Infrastructure Project Submission",
            "type": "object",
            "required": ["project_name", "project_location", "estimated_cost", "officer_id", "phone_number"],
            "properties": {
                "header_1": _s("Project Details"),
                "project_name": _f("Project Name"),
                "project_type": _f("Project Type", enum=["Water Supply", "Sewerage", "Dam Construction", "Pipeline", "Borehole", "Treatment Plant"]),
                "project_location": _f("Project Location (GPS / Area)"),
                "county": _f("County"),
                "estimated_cost": _f("Estimated Cost (KES)", field_type="number"),
                "header_2": _s("Approval & Compliance"),
                "nema_approval": _f("NEMA EIA Approval Status", enum=["Approved", "Pending", "Not Required"]),
                "treasury_approval": _f("Treasury Budget Approval", enum=["Approved", "Pending"]),
                "header_3": _s("Responsible Officer"),
                "officer_id": _f("Project Officer ID", lookup_service="IPRS", lookup_action="get_person_details"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
            },
        },
    ),
    # ── Assets Recovery Agency (G2G) ──
    # Source: Assets_Recovery_Agency___Service_Delivery.md
    (
        ["assets recovery", "ara", "asset forfeiture"],
        "ara_g2g",
        {
            "title": "Asset Recovery Investigation (G2G)",
            "type": "object",
            "required": ["suspect_id", "case_reference", "officer_id"],
            "properties": {
                "header_1": _s("Suspect Details", "Once-Only: Asset trace via BRS, NTSA, Ardhisasa"),
                "suspect_name": _f("Suspect Full Name"),
                "suspect_id": _f("Suspect Maisha Namba", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_2": _s("Case Details"),
                "case_reference": _f("Case Reference Number"),
                "investigation_type": _f("Investigation Type", enum=["Corruption", "Money Laundering", "Drug Trafficking", "Tax Evasion", "Other"]),
                "estimated_value": _f("Estimated Asset Value (KES)", field_type="number"),
                "header_3": _s("Investigating Officer"),
                "officer_id": _f("ARA Analyst ID", lookup_service="IPRS", lookup_action="get_person_details"),
            },
        },
    ),
    # ── State Law Office: Marriage Registration ──
    # Source: State_Law_Office_The___Service_Delivery.md (Cradle_to_Death_MDAs.md)
    (
        ["state law office", "attorney general", "marriage registration", "societies registration"],
        "state_law_office",
        {
            "title": "Marriage / Societies Registration",
            "type": "object",
            "required": ["registration_type", "applicant_id", "phone_number"],
            "properties": {
                "header_1": _s("Registration Type"),
                "registration_type": _f("Type", enum=["Marriage Registration", "Society Registration"]),
                "header_2": _s("Applicant / Party 1", "Once-Only: Identity verified & bigamy check via IPRS"),
                "applicant_name": _f("Applicant / Party 1 Full Name"),
                "applicant_id": _f("Party 1 National ID", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_3": _s("Party 2 (Marriage Only)"),
                "party2_name": _f("Party 2 Full Name"),
                "party2_id": _f("Party 2 National ID", lookup_service="IPRS", lookup_action="get_person_details"),
                "marriage_type": _f("Marriage Type", enum=["Civil", "Customary", "Christian", "Islamic", "Hindu"]),
                "date_of_event": _f("Date of Event", format="date"),
                "header_4": _s("Society Details (Society Registration Only)"),
                "society_name": _f("Society / Association Name"),
                "society_objectives": _f("Objectives", format="textarea"),
                "header_5": _s("Contact"),
                "county": _f("County"),
                "phone_number": _f("Phone Number"),
            },
        },
    ),
    # ── Judiciary: Succession & Probate ──
    # Source: THE_JUDICIARY___Service_Delivery.md (Cradle_to_Death_MDAs.md)
    (
        ["judiciary", "succession", "probate"],
        "judiciary_succession",
        {
            "title": "Succession & Probate Administration",
            "type": "object",
            "required": ["applicant_id", "deceased_name", "court_station", "phone_number"],
            "properties": {
                "header_1": _s("Applicant Information", "Once-Only: Identity verified via IPRS"),
                "applicant_name": _f("Applicant (Petitioner) Full Name"),
                "applicant_id": _f("Applicant National ID", lookup_service="IPRS", lookup_action="get_person_details"),
                "relationship_to_deceased": _f("Relationship to Deceased", enum=["Spouse", "Child", "Parent", "Sibling", "Administrator", "Legal Representative"]),
                "header_2": _s("Deceased Details"),
                "deceased_name": _f("Full Name of Deceased"),
                "deceased_id": _f("Deceased National ID", lookup_service="IPRS", lookup_action="get_person_details"),
                "date_of_death": _f("Date of Death", format="date"),
                "death_certificate_no": _f("Death Certificate Number", lookup_service="CRS", lookup_action="verify_death"),
                "header_3": _s("Case Details"),
                "case_type": _f("Case Type", enum=["Grant of Probate (Testate)", "Grant of Administration (Intestate)"]),
                "court_station": _f("Court Station"),
                "has_will": _f("Does the deceased have a Will?", field_type="boolean"),
                "header_4": _s("Contact & Attachments"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
                "supporting_doc": _f("Supporting Document / Will (PDF)", format="data-url"),
            },
        },
    ),
    # ── UFAA: Unclaimed Financial Assets ──
    # Source: Unclaimed_Financial_Assets_Authority___Service_Delivery.md
    (
        ["unclaimed financial assets", "ufaa"],
        "ufaa_claims",
        {
            "title": "Claim for Unclaimed Financial Assets",
            "type": "object",
            "required": ["claimant_id", "asset_type", "phone_number"],
            "properties": {
                "header_1": _s("Claimant Identity", "Once-Only: Identity verified via IPRS"),
                "claimant_name": _f("Claimant Full Name"),
                "claimant_id": _f("Claimant National ID", lookup_service="IPRS", lookup_action="get_person_details"),
                "relationship_to_owner": _f("Relationship to Account Holder", enum=["Self", "Spouse", "Child", "Legal Administrator", "Other"]),
                "header_2": _s("Asset Details"),
                "asset_type": _f("Asset Type", enum=["Bank Account", "Insurance Policy", "Shares / Securities", "Pension", "Other"]),
                "original_holder_name": _f("Original Account Holder Name"),
                "original_holder_id": _f("Original Holder ID (if known)", lookup_service="IPRS", lookup_action="get_person_details"),
                "institution_name": _f("Financial Institution Name"),
                "account_reference": _f("Account / Policy Reference Number"),
                "header_3": _s("Contact & Proof"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
                "proof_document": _f("Proof of Claim (PDF)", format="data-url"),
            },
        },
    ),
    # ── NSSF: Social Security Registration ──
    # Source: National_Social_Security_Fund___Service_Delivery.md
    (
        ["national social security fund", "nssf"],
        "nssf_registration",
        {
            "title": "NSSF Registration & Contribution",
            "type": "object",
            "required": ["id_number", "employment_status", "phone_number"],
            "properties": {
                "header_1": _s("Personal Identity", "Once-Only: Bio-data auto-fetched from IPRS/Maisha Namba"),
                "id_number": _f("National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "date_of_birth": _f("Date of Birth", format="date"),
                "header_2": _s("Employment Details"),
                "employment_status": _f("Employment Status", enum=["Formal Employment", "Self-Employed", "Informal Sector"]),
                "employer_name": _f("Employer Name (if applicable)"),
                "kra_pin": _f("KRA PIN", lookup_service="KRA", lookup_action="verify_pin"),
                "header_3": _s("Contact"),
                "county": _f("County"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
            },
        },
    ),
    # ── Ministry of Health: Health Information Exchange ──
    # Source: Ministry_of_Health___Service_Delivery.md
    (
        ["ministry of health", "health information exchange", "khie", "patient registration"],
        "moh_health",
        {
            "title": "Health Service Notification",
            "type": "object",
            "required": ["patient_id", "facility_name", "event_type", "officer_id"],
            "properties": {
                "header_1": _s("Patient Identity", "Once-Only: Patient identified via Maisha Namba / MPI"),
                "patient_id": _f("Patient Maisha Namba / National ID", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_2": _s("Event Details"),
                "event_type": _f("Event Type", enum=["Birth Notification", "Death Notification", "Immunization", "Outpatient Visit", "Inpatient Admission"]),
                "facility_name": _f("Health Facility Name"),
                "facility_code": _f("Facility Code (MFL)"),
                "event_date": _f("Event Date", format="date"),
                "header_3": _s("Clinical Summary (Optional)"),
                "diagnosis_code": _f("Diagnosis Code (ICD-10)"),
                "notes": _f("Clinical Notes", format="textarea"),
                "header_4": _s("Health Worker"),
                "officer_id": _f("Health Worker ID", lookup_service="IPRS", lookup_action="get_person_details"),
            },
        },
    ),
    # ── State Department of ICT ──
    (
        ["state department of ict", "state department for ict", "digital economy"],
        "sd_ict_g2g",
        {
            "title": "ICT Policy & Digital Economy Submission (G2G)",
            "type": "object",
            "required": ["submission_title", "submission_type", "officer_id"],
            "properties": {
                "header_1": _s("Submission Details"),
                "submission_title": _f("Submission Title"),
                "submission_type": _f("Type", enum=["Policy Proposal", "Standards Request", "Compliance Report", "Infrastructure Request"]),
                "requesting_mda": _f("Requesting MDA"),
                "description": _f("Description", format="textarea"),
                "header_2": _s("Submitting Officer"),
                "officer_id": _f("Officer ID", lookup_service="IPRS", lookup_action="get_person_details"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
            },
        },
    ),
    # ── Lands: Land Registration / Title Deed Issuance ──
    (
        ["lands and physical planning", "land registration", "title deed issuance", "ardhisasa"],
        "lands_registration",
        {
            "title": "Land Registration / Title Deed Issuance",
            "type": "object",
            "required": ["applicant_id", "land_reference", "county", "phone_number"],
            "properties": {
                "header_1": _s("Applicant Details", "Once-Only: Identity verified via IPRS"),
                "applicant_name": _f("Applicant Full Name"),
                "applicant_id": _f("National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "applicant_kra_pin": _f("KRA PIN", lookup_service="KRA", lookup_action="verify_pin"),
                "header_2": _s("Land Details", "Auto-verified against Ardhisasa"),
                "land_reference": _f("Land Reference / LR Number"),
                "county": _f("County"),
                "sub_county": _f("Sub-County"),
                "registration_type": _f("Registration Type", enum=["First Registration", "Subdivision", "Amalgamation", "Lease"]),
                "header_3": _s("Contact & Attachments"),
                "phone_number": _f("Contact Phone Number"),
                "survey_plan": _f("Survey Plan (PDF)", format="data-url"),
            },
        },
    ),
]


def _match_mda_pattern(service):
    """
    Match a service against MDA_SCHEMAS using service_name, MDA name,
    life_event_group, and service_family name.
    Returns (category, schema) or (None, None) if no match.
    """
    search_text = (service.service_name or "").lower()
    if service.mda:
        search_text += " " + (service.mda.name or "").lower()
    if service.life_event_group:
        search_text += " " + service.life_event_group.lower()
    if service.service_family:
        search_text += " " + (service.service_family.name or "").lower()

    for keywords, category, schema in MDA_SCHEMAS:
        for kw in keywords:
            if kw.lower() in search_text:
                return category, schema

    return None, None


def _has_form_schema(service):
    """Check if the service already has a populated form_schema."""
    if service.form_schema and isinstance(service.form_schema, dict) and service.form_schema.get("properties"):
        return True
    return False


# ─────────────────────────────────────────────────────────────────────────────
# Management command
# ─────────────────────────────────────────────────────────────────────────────

class Command(BaseCommand):
    help = (
        "Seed form_schema for Priority & Cradle-to-Death services based on "
        "official BPR documentation. Targets only services with priority "
        "in ('high', 'critical')."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview which services would be updated without saving.",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite existing form_schema (default: skip services that already have one).",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        force = options["force"]
        mode_label = "DRY RUN" if dry_run else "LIVE"

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"\n=== Seed Priority & Cradle-to-Death Form Schemas ({mode_label}) ==="
        ))

        services = ServiceConfig.objects.select_related(
            "service_family", "mda"
        ).filter(
            priority__in=["high", "critical"]
        )

        total = services.count()
        self.stdout.write(f"  Found {total} priority/critical services\n")

        updated = 0
        skipped_existing = 0
        skipped_no_match = 0
        category_counts = defaultdict(int)

        for idx, svc in enumerate(services, 1):
            if not force and _has_form_schema(svc):
                skipped_existing += 1
                continue

            schema = None
            category = None

            # Tier 1: Exact service_code match
            if svc.service_code and svc.service_code in CODE_SCHEMAS:
                schema = CODE_SCHEMAS[svc.service_code]
                category = f"code:{svc.service_code}"

            # Tier 2: MDA / service_name pattern match
            if schema is None:
                category, schema = _match_mda_pattern(svc)

            if schema is None:
                skipped_no_match += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"  [{idx}/{total}] ⚠  No BPR match: "
                        f"{svc.service_code or '???'} – {svc.service_name} "
                        f"(MDA: {svc.mda.name if svc.mda else 'N/A'})"
                    )
                )
                continue

            field_count = len([
                k for k in schema.get("properties", {})
                if not k.startswith("header")
            ])

            if not dry_run:
                svc.form_schema = schema
                svc.save(update_fields=["form_schema"])

            category_counts[category] += 1
            updated += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f"  [{idx}/{total}] ✅ {svc.service_code or '???'} – "
                    f"{svc.service_name} → \"{category}\" ({field_count} fields)"
                )
            )

        # Summary
        self.stdout.write(self.style.MIGRATE_HEADING("\n── Summary ──"))
        self.stdout.write(f"  Total priority/critical services: {total}")
        self.stdout.write(f"  Already had form_schema (skipped): {skipped_existing}")
        self.stdout.write(
            self.style.WARNING(f"  No BPR match found: {skipped_no_match}")
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"  {'Would update' if dry_run else 'Updated'}: {updated}"
            )
        )

        if category_counts:
            self.stdout.write(self.style.MIGRATE_HEADING("\n── By Source ──"))
            for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
                self.stdout.write(f"  {cat}: {count}")

        self.stdout.write(self.style.SUCCESS(
            f"\n✅  {'DRY RUN complete – no changes saved.' if dry_run else 'Priority form schemas populated.'}"
        ))
