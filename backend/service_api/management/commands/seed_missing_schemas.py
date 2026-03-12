"""
Management command to auto-generate and populate form_schema for all
ServiceConfig records that are currently missing one.

Uses keyword-based inference on service_name (and life_event_group /
service_family) to produce contextual JSON Schema definitions with
KeSEL "Once-Only" lookup_service attributes on identity fields.

Usage:
    python manage.py seed_missing_schemas
    python manage.py seed_missing_schemas --dry-run
"""
from collections import defaultdict

from django.core.management.base import BaseCommand
from service_api.models import ServiceConfig


# ─────────────────────────────────────────────────────────────────────────────
# Schema builder helpers
# ─────────────────────────────────────────────────────────────────────────────

def _s(title, description=None):
    """Shorthand for a section_header entry."""
    entry = {"type": "section_header", "title": title}
    if description:
        entry["description"] = description
    return entry


def _f(title, field_type="string", **kwargs):
    """Shorthand for a field entry."""
    entry = {"type": field_type, "title": title}
    entry.update(kwargs)
    return entry


# ─────────────────────────────────────────────────────────────────────────────
# Keyword → Schema definitions
# Each returns a tuple: (category_label, schema_dict)
# ─────────────────────────────────────────────────────────────────────────────

KEYWORD_SCHEMAS = [
    # ── Civil Registration: Birth ──
    (
        ["birth", "child", "maternity", "newborn"],
        "civil_reg_birth",
        {
            "type": "object",
            "required": ["child_name", "date_of_birth", "mother_id", "county", "phone_number"],
            "properties": {
                "header_1": _s("Child Information"),
                "child_name": _f("Full Name of Child"),
                "date_of_birth": _f("Date of Birth", format="date"),
                "gender": _f("Gender", enum=["Male", "Female"]),
                "hospital_name": _f("Health Facility / Hospital"),
                "header_2": _s("Parental Information"),
                "mother_id": _f("Mother's ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "father_id": _f("Father's ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_3": _s("Location"),
                "county": _f("County"),
                "sub_county": _f("Sub-County"),
                "phone_number": _f("Parent/Guardian Phone Number"),
            },
        },
    ),
    # ── Civil Registration: Death ──
    (
        ["death", "burial", "mortuary", "deceased"],
        "civil_reg_death",
        {
            "type": "object",
            "required": ["deceased_name", "date_of_death", "place_of_death", "informant_id", "informant_phone"],
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
                "relationship": _f("Relationship to Deceased"),
                "header_3": _s("Location"),
                "county": _f("County"),
            },
        },
    ),
    # ── Civil Registration: Marriage / Divorce ──
    (
        ["marriage", "divorce", "wedding", "matrimon"],
        "civil_reg_marriage",
        {
            "type": "object",
            "required": ["groom_id", "bride_id", "date_of_event", "county", "phone_number"],
            "properties": {
                "header_1": _s("Parties"),
                "groom_name": _f("Groom / Party 1 Full Name"),
                "groom_id": _f("Groom / Party 1 ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "bride_name": _f("Bride / Party 2 Full Name"),
                "bride_id": _f("Bride / Party 2 ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_2": _s("Event Details"),
                "date_of_event": _f("Date of Event", format="date"),
                "venue": _f("Venue / Location"),
                "county": _f("County"),
                "marriage_type": _f("Type", enum=["Civil", "Customary", "Christian", "Islamic", "Hindu"]),
                "header_3": _s("Contact"),
                "phone_number": _f("Contact Phone Number"),
                "witness_1_name": _f("Witness 1 Full Name"),
                "witness_2_name": _f("Witness 2 Full Name"),
            },
        },
    ),
    # ── Passport / Travel Document / Visa ──
    (
        ["passport", "travel document", "visa", "work permit"],
        "immigration_passport",
        {
            "type": "object",
            "required": ["full_name", "id_number", "birth_cert_no", "passport_type", "phone_number"],
            "properties": {
                "header_1": _s("Personal Identity", "Information as per National ID"),
                "full_name": _f("Full Name"),
                "id_number": _f("National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "date_of_birth": _f("Date of Birth", format="date"),
                "gender": _f("Gender", enum=["Male", "Female"]),
                "header_2": _s("Citizenship Verification"),
                "birth_cert_no": _f("Birth Certificate Number", lookup_service="CRS", lookup_action="verify_birth"),
                "nationality": _f("Nationality"),
                "county": _f("County of Residence"),
                "header_3": _s("Document Configuration"),
                "passport_type": _f("Document Type", enum=["Ordinary Passport", "East African Passport", "Emergency Travel Document", "Diplomatic Passport"]),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
                "header_4": _s("Digital Uploads"),
                "photo": _f("Passport Size Photo", format="data-url"),
                "id_scan": _f("Scan of National ID", format="data-url"),
            },
        },
    ),
    # ── National ID / Identity Services ──
    (
        ["national id", "identity card", "registration of persons", "maisha namba", "huduma namba"],
        "identity_services",
        {
            "type": "object",
            "required": ["full_name", "date_of_birth", "birth_certificate_number", "county", "phone_number"],
            "properties": {
                "header_1": _s("Personal Details"),
                "full_name": _f("Full Name"),
                "date_of_birth": _f("Date of Birth", format="date"),
                "gender": _f("Gender", enum=["Male", "Female"]),
                "header_2": _s("Citizenship & Parentage"),
                "birth_certificate_number": _f("Birth Certificate Number", lookup_service="CRS", lookup_action="verify_birth"),
                "fathers_name": _f("Father's Full Name"),
                "fathers_id": _f("Father's ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "mothers_name": _f("Mother's Full Name"),
                "mothers_id": _f("Mother's ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_3": _s("Location"),
                "county_of_birth": _f("County of Birth"),
                "county": _f("County of Residence"),
                "sub_county": _f("Sub-County"),
                "phone_number": _f("Phone Number"),
            },
        },
    ),
    # ── Business / Company / Trade ──
    (
        ["business", "company", "incorporat", "trade", "enterprise", "cooperative", "sacco"],
        "business_registration",
        {
            "type": "object",
            "required": ["business_name", "applicant_id", "kra_pin", "nature_of_business", "phone_number", "email"],
            "properties": {
                "header_1": _s("Business Details"),
                "business_name": _f("Proposed Business / Company Name"),
                "business_type": _f("Business Type", enum=["Sole Proprietor", "Partnership", "Private Limited (Ltd)", "Public Limited (PLC)"]),
                "nature_of_business": _f("Nature of Business / Activity"),
                "header_2": _s("Applicant / Director Details"),
                "applicant_name": _f("Applicant / Director Full Name"),
                "applicant_id": _f("National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "kra_pin": _f("KRA PIN", lookup_service="KRA", lookup_action="verify_pin"),
                "header_3": _s("Location & Contact"),
                "business_address": _f("Business Physical Address"),
                "county": _f("County"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
            },
        },
    ),
    # ── Tax / Revenue / KRA ──
    (
        ["tax", "kra", "revenue", "compliance", "itax", "fiscal"],
        "tax_revenue",
        {
            "type": "object",
            "required": ["taxpayer_name", "kra_pin", "phone_number", "email"],
            "properties": {
                "header_1": _s("Taxpayer Information"),
                "taxpayer_name": _f("Taxpayer / Business Name"),
                "kra_pin": _f("KRA PIN", lookup_service="KRA", lookup_action="verify_pin"),
                "id_number": _f("National ID Number (Individuals)", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_2": _s("Tax Details"),
                "tax_types": _f("Tax Types (e.g. Income Tax, VAT)"),
                "tax_period_from": _f("Period From", format="date"),
                "tax_period_to": _f("Period To", format="date"),
                "purpose": _f("Purpose (e.g. Tender, Loan Application)"),
                "header_3": _s("Contact"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
            },
        },
    ),
    # ── Land / Title / Survey / Property ──
    (
        ["land", "title deed", "survey", "property", "ardhisasa", "plot"],
        "land_administration",
        {
            "type": "object",
            "required": ["applicant_name", "applicant_id", "land_reference", "county", "phone_number"],
            "properties": {
                "header_1": _s("Land Details"),
                "title_deed_number": _f("Title Deed Number"),
                "land_reference": _f("Land Reference / LR Number"),
                "county": _f("County"),
                "sub_county": _f("Sub-County"),
                "header_2": _s("Applicant / Owner"),
                "applicant_name": _f("Applicant Full Name"),
                "applicant_id": _f("National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "applicant_kra_pin": _f("KRA PIN", lookup_service="KRA", lookup_action="verify_pin"),
                "header_3": _s("Transaction Details"),
                "transaction_type": _f("Transaction Type", enum=["Transfer", "Subdivision", "Search", "Charge", "Discharge", "New Registration"]),
                "agreed_value": _f("Agreed Value (KES)", field_type="number"),
                "advocate_name": _f("Conveyancing Advocate (if any)"),
                "phone_number": _f("Contact Phone Number"),
            },
        },
    ),
    # ── Education / School / Student / NEMIS ──
    (
        ["education", "school", "student", "nemis", "teacher", "curriculum", "university", "tvet"],
        "education",
        {
            "type": "object",
            "required": ["applicant_name", "id_number", "institution_name", "phone_number"],
            "properties": {
                "header_1": _s("Applicant Information"),
                "applicant_name": _f("Full Name"),
                "id_number": _f("National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_2": _s("Institution Details"),
                "institution_name": _f("Institution Name", lookup_service="KNQA_REGISTRY"),
                "institution_type": _f("Institution Type", enum=["Pre-Primary", "Primary", "Secondary", "TVET", "University"]),
                "admission_number": _f("Admission / Registration Number"),
                "header_3": _s("Location & Contact"),
                "county": _f("County"),
                "sub_county": _f("Sub-County"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
            },
        },
    ),
    # ── Qualification / KNQA ──
    (
        ["qualification", "knqa", "accreditation", "credential"],
        "qualification_knqa",
        {
            "type": "object",
            "required": ["institution_name", "qualification_name", "year_obtained", "id_number"],
            "properties": {
                "header_1": _s("Institution Details"),
                "institution_name": _f("Name of Awarding Institution", lookup_service="KNQA_REGISTRY"),
                "qualification_type": _f("Qualification Type", enum=["Certificate", "Diploma", "Degree", "Masters", "PhD"]),
                "qualification_name": _f("Exact Title of Qualification"),
                "year_obtained": _f("Year Obtained", field_type="number"),
                "header_2": _s("Identity Mapping"),
                "id_number": _f("ID Number as on Certificate", lookup_service="IPRS", lookup_action="get_person_details"),
                "phone_number": _f("Phone Number"),
            },
        },
    ),
    # ── Health / NHIF / Medical / Hospital ──
    (
        ["health", "nhif", "medical", "hospital", "clinical", "pharmacy", "sha "],
        "health_services",
        {
            "type": "object",
            "required": ["full_name", "id_number", "phone_number", "county"],
            "properties": {
                "header_1": _s("Personal Information"),
                "full_name": _f("Full Name"),
                "id_number": _f("National ID / Passport Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "date_of_birth": _f("Date of Birth", format="date"),
                "gender": _f("Gender", enum=["Male", "Female"]),
                "nhif_number": _f("NHIF / SHA Member Number", lookup_service="NHIF"),
                "header_2": _s("Employment & Residence"),
                "employment_type": _f("Employment Type", enum=["Formal Employment", "Self-Employed", "Unemployed", "Student"]),
                "employer_name": _f("Employer Name (if employed)"),
                "county": _f("County of Residence"),
                "header_3": _s("Contact"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
            },
        },
    ),
    # ── Vehicle / Motor / Driving / NTSA ──
    (
        ["vehicle", "motor", "driving", "ntsa", "logbook", "inspection"],
        "transport",
        {
            "type": "object",
            "required": ["owner_name", "owner_id", "phone_number"],
            "properties": {
                "header_1": _s("Owner Details"),
                "owner_name": _f("Vehicle Owner Full Name"),
                "owner_id": _f("Owner National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "owner_kra_pin": _f("Owner KRA PIN", lookup_service="KRA", lookup_action="verify_pin"),
                "header_2": _s("Vehicle Details"),
                "vehicle_make": _f("Vehicle Make (e.g. Toyota)"),
                "vehicle_model": _f("Vehicle Model (e.g. Corolla)"),
                "year_of_manufacture": _f("Year of Manufacture", field_type="number"),
                "engine_number": _f("Engine Number"),
                "chassis_number": _f("Chassis Number"),
                "registration_number": _f("Registration Number (if registered)"),
                "header_3": _s("Contact"),
                "phone_number": _f("Contact Phone Number"),
            },
        },
    ),
    # ── Licence / Permit / Certificate (generic regulatory) ──
    (
        ["licen", "permit", "certificate", "authorization", "clearance"],
        "licensing_permits",
        {
            "type": "object",
            "required": ["applicant_name", "id_number", "license_type", "phone_number"],
            "properties": {
                "header_1": _s("Applicant Information"),
                "applicant_name": _f("Full Name / Business Name"),
                "id_number": _f("National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "kra_pin": _f("KRA PIN (if applicable)", lookup_service="KRA", lookup_action="verify_pin"),
                "header_2": _s("Licence / Permit Details"),
                "license_type": _f("Type of Licence / Permit"),
                "purpose": _f("Purpose / Activity Description"),
                "location": _f("Location / Premises Address"),
                "county": _f("County"),
                "header_3": _s("Supporting Documents"),
                "document_upload": _f("Supporting Document (PDF/JPG)", format="data-url"),
                "header_4": _s("Contact"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
            },
        },
    ),
    # ── Environment / EIA / NEMA / Waste ──
    (
        ["environment", "eia", "nema", "waste", "pollution", "emission", "conservation"],
        "environment",
        {
            "type": "object",
            "required": ["applicant_name", "id_number", "project_name", "location", "phone_number"],
            "properties": {
                "header_1": _s("Applicant / Proponent"),
                "applicant_name": _f("Applicant / Company Name"),
                "id_number": _f("National ID / Registration Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "kra_pin": _f("KRA PIN", lookup_service="KRA", lookup_action="verify_pin"),
                "header_2": _s("Project Details"),
                "project_name": _f("Project Name"),
                "project_type": _f("Project Type", enum=["Residential", "Commercial", "Industrial", "Infrastructure", "Mining"]),
                "location": _f("Project Location"),
                "county": _f("County"),
                "estimated_budget": _f("Estimated Budget (KES)", field_type="number"),
                "header_3": _s("Contact"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
                "header_4": _s("Attachments"),
                "project_brief": _f("Project Brief / EIA Report (PDF)", format="data-url"),
            },
        },
    ),
    # ── Water / Sewerage / Irrigation ──
    (
        ["water", "sewerage", "irrigation", "borehole"],
        "water_services",
        {
            "type": "object",
            "required": ["applicant_name", "id_number", "connection_type", "phone_number"],
            "properties": {
                "header_1": _s("Applicant Information"),
                "applicant_name": _f("Full Name / Business Name"),
                "id_number": _f("National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_2": _s("Connection Details"),
                "connection_type": _f("Connection Type", enum=["New Domestic", "New Commercial", "Reconnection", "Upgrade", "Borehole Permit"]),
                "plot_number": _f("Plot / LR Number"),
                "physical_address": _f("Physical Address"),
                "county": _f("County"),
                "header_3": _s("Contact"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
            },
        },
    ),
    # ── Housing / Building / Construction ──
    (
        ["housing", "building", "construction", "planning approval", "development control"],
        "housing_construction",
        {
            "type": "object",
            "required": ["applicant_name", "id_number", "site_location", "phone_number"],
            "properties": {
                "header_1": _s("Applicant / Developer"),
                "applicant_name": _f("Full Name / Company Name"),
                "id_number": _f("National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "kra_pin": _f("KRA PIN", lookup_service="KRA", lookup_action="verify_pin"),
                "header_2": _s("Site & Building Details"),
                "site_location": _f("Site Location / LR Number"),
                "building_type": _f("Building Type", enum=["Residential", "Commercial", "Industrial", "Mixed Use", "Public Facility"]),
                "architect_name": _f("Architect / Engineer Name"),
                "county": _f("County"),
                "estimated_cost": _f("Estimated Construction Cost (KES)", field_type="number"),
                "header_3": _s("Contact & Uploads"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
                "architectural_plans": _f("Architectural Plans (PDF)", format="data-url"),
            },
        },
    ),
    # ── Pension / Retirement / NSSF ──
    (
        ["pension", "retirement", "nssf", "social security", "provident"],
        "social_protection",
        {
            "type": "object",
            "required": ["full_name", "id_number", "nssf_number", "phone_number"],
            "properties": {
                "header_1": _s("Personal Information"),
                "full_name": _f("Full Name"),
                "id_number": _f("National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "date_of_birth": _f("Date of Birth", format="date"),
                "header_2": _s("Social Security"),
                "nssf_number": _f("NSSF Member Number", lookup_service="NSSF"),
                "employer_name": _f("Current / Last Employer"),
                "employment_status": _f("Employment Status", enum=["Employed", "Retired", "Self-Employed", "Unemployed"]),
                "header_3": _s("Contact"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
            },
        },
    ),
    # ── Immigration (Other) / Alien / Refugee ──
    (
        ["immigra", "alien", "refugee", "asylum", "foreign national"],
        "immigration_other",
        {
            "type": "object",
            "required": ["full_name", "passport_number", "nationality", "phone_number"],
            "properties": {
                "header_1": _s("Personal Information"),
                "full_name": _f("Full Name (as in Passport)"),
                "passport_number": _f("Passport Number"),
                "nationality": _f("Nationality"),
                "date_of_birth": _f("Date of Birth", format="date"),
                "gender": _f("Gender", enum=["Male", "Female"]),
                "header_2": _s("Purpose of Application"),
                "application_type": _f("Application Type", enum=["Work Permit", "Residence Permit", "Student Pass", "Refugee Status", "Re-entry Pass"]),
                "purpose_details": _f("Purpose / Reason for Application"),
                "sponsor_name": _f("Sponsor / Employer Name (if applicable)"),
                "header_3": _s("Contact"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
            },
        },
    ),
    # ── Court / Judicial / Probate / Succession ──
    (
        ["court", "judicial", "probate", "succession", "affidavit", "magistrate"],
        "judicial_services",
        {
            "type": "object",
            "required": ["applicant_name", "id_number", "case_type", "phone_number"],
            "properties": {
                "header_1": _s("Applicant Information"),
                "applicant_name": _f("Full Name"),
                "id_number": _f("National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_2": _s("Case Details"),
                "case_type": _f("Case Type", enum=["Civil", "Criminal", "Probate", "Succession", "Children's Court", "Other"]),
                "court_station": _f("Court Station"),
                "case_number": _f("Case Number (if existing)"),
                "description": _f("Brief Description", format="textarea"),
                "header_3": _s("Contact & Attachments"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
                "supporting_doc": _f("Supporting Document (PDF)", format="data-url"),
            },
        },
    ),
    # ── Procurement / Tender / AGPO ──
    (
        ["procurement", "tender", "agpo", "bid", "supply"],
        "procurement",
        {
            "type": "object",
            "required": ["business_name", "kra_pin", "phone_number"],
            "properties": {
                "header_1": _s("Business Details"),
                "business_name": _f("Registered Business Name"),
                "kra_pin": _f("KRA PIN", lookup_service="KRA", lookup_action="verify_pin"),
                "registration_number": _f("Business Registration Number"),
                "header_2": _s("Procurement Details"),
                "agpo_category": _f("AGPO Category (if applicable)", enum=["Women", "Youth", "Persons with Disability", "N/A"]),
                "tender_reference": _f("Tender / Contract Reference"),
                "goods_services_description": _f("Goods / Services Description"),
                "header_3": _s("Contact"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
            },
        },
    ),
    # ── Energy / Electricity / EPRA ──
    (
        ["energy", "electric", "epra", "power", "petroleum", "solar"],
        "energy",
        {
            "type": "object",
            "required": ["applicant_name", "id_number", "service_type", "phone_number"],
            "properties": {
                "header_1": _s("Applicant Information"),
                "applicant_name": _f("Full Name / Company Name"),
                "id_number": _f("National ID / Registration No", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_2": _s("Service Details"),
                "service_type": _f("Service Type", enum=["New Connection", "Upgrade", "Disconnection", "Licence Application", "Complaint"]),
                "premises_address": _f("Premises Address"),
                "county": _f("County"),
                "meter_number": _f("Meter Number (if existing)"),
                "header_3": _s("Contact"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
            },
        },
    ),
    # ── Agriculture / Livestock / Food ──
    (
        ["agricultur", "livestock", "food", "farmer", "crop", "veterinar", "fisheri"],
        "agriculture",
        {
            "type": "object",
            "required": ["applicant_name", "id_number", "farm_location", "phone_number"],
            "properties": {
                "header_1": _s("Applicant Information"),
                "applicant_name": _f("Full Name"),
                "id_number": _f("National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
                "header_2": _s("Farm / Activity Details"),
                "activity_type": _f("Activity Type", enum=["Crop Farming", "Livestock", "Fisheries", "Agro-processing", "Export"]),
                "farm_location": _f("Farm / Activity Location"),
                "farm_size": _f("Farm Size (Acres)"),
                "county": _f("County"),
                "header_3": _s("Contact"),
                "phone_number": _f("Phone Number"),
                "email": _f("Email Address"),
            },
        },
    ),
]


def _get_generic_fallback_schema(service_name):
    """Returns a standard baseline schema for services with no keyword match."""
    return {
        "type": "object",
        "required": ["full_name", "id_number", "phone_number", "details"],
        "properties": {
            "header_1": _s("Applicant Information"),
            "full_name": _f("Full Legal Name"),
            "id_number": _f("National ID Number", lookup_service="IPRS", lookup_action="get_person_details"),
            "phone_number": _f("Phone Number"),
            "email": _f("Email Address"),
            "header_2": _s("Service Details", f"Information for: {service_name}"),
            "details": _f("Request / Application Details", format="textarea"),
            "supporting_doc": _f("Supporting Document (PDF/JPG)", format="data-url"),
        },
    }


def _match_service(service):
    """
    Returns (category_label, schema_dict) by matching service_name,
    life_event_group, and service_family name against keyword rules.
    Falls back to generic schema if no keyword matches.
    """
    search_text = (service.service_name or "").lower()

    if service.life_event_group:
        search_text += " " + service.life_event_group.lower()
    if service.service_family:
        search_text += " " + service.service_family.name.lower()

    for keywords, category, schema in KEYWORD_SCHEMAS:
        for kw in keywords:
            if kw.lower() in search_text:
                return category, schema

    return "generic", _get_generic_fallback_schema(service.service_name)


def _has_effective_schema(service):
    """Check if the service already has an effective schema via any path."""
    legacy = service.config.get("rules", {}).get("schema") if service.config else None
    if legacy and isinstance(legacy, dict) and legacy.get("properties"):
        return True

    if service.form_schema and isinstance(service.form_schema, dict) and service.form_schema.get("properties"):
        return True

    if service.service_family and service.service_family.shared_form_schema:
        shared = service.service_family.shared_form_schema
        if isinstance(shared, dict) and shared.get("properties"):
            return True

    return False


# ─────────────────────────────────────────────────────────────────────────────
# Management command
# ─────────────────────────────────────────────────────────────────────────────

class Command(BaseCommand):
    help = (
        "Auto-generate and populate form_schema for ServiceConfig records "
        "that are currently missing one. Uses keyword-based inference on "
        "service_name with KeSEL Once-Only lookup_service compliance."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview which services would be updated without saving.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        mode_label = "DRY RUN" if dry_run else "LIVE"

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"\n=== Seed Missing Form Schemas ({mode_label}) ==="
        ))

        services = ServiceConfig.objects.select_related(
            "service_family", "mda"
        ).all()

        total = services.count()
        updated = 0
        skipped = 0
        category_counts = defaultdict(int)

        for idx, svc in enumerate(services, 1):
            if _has_effective_schema(svc):
                skipped += 1
                continue

            category, schema = _match_service(svc)
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
                    f"  [{idx}/{total}] ✅ {svc.service_name} → "
                    f"\"{category}\" schema ({field_count} fields)"
                )
            )

        self.stdout.write(self.style.MIGRATE_HEADING("\n── Summary ──"))
        self.stdout.write(f"  Total services scanned: {total}")
        self.stdout.write(f"  Already had schema (skipped): {skipped}")
        self.stdout.write(
            self.style.SUCCESS(f"  {'Would update' if dry_run else 'Updated'}: {updated}")
        )

        if category_counts:
            self.stdout.write(self.style.MIGRATE_HEADING("\n── By Category ──"))
            for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
                self.stdout.write(f"  {cat}: {count}")

        self.stdout.write(self.style.SUCCESS(
            f"\n✅  {'DRY RUN complete – no changes saved.' if dry_run else 'All missing schemas populated.'}"
        ))
