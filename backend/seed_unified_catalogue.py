import os
import django
import json
import csv
import random

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig, MDA, ServiceCategory, ServiceDomain, WorkflowStep, ServiceRequest, RegistryAdapter, RegistryEndpoint

def get_registry_ids(adapter_code, endpoint_name):
    try:
        adapter = RegistryAdapter.objects.filter(code=adapter_code).first()
        if not adapter: return None, None
        endpoint = RegistryEndpoint.objects.filter(adapter=adapter, name=endpoint_name).first()
        return (adapter.id, endpoint.id) if endpoint else (adapter.id, None)
    except:
        return None, None

def seed_unified_catalogue():
    print("=" * 80)
    print("🚀 UNIFIED GOVERNMENT SERVICE CATALOGUE SEEDER v4.0")
    print("=" * 80)

    iprs_adapter_id, person_lookup_id = get_registry_ids("IPRS", "Verify Citizen Identity")

    # 1. CLEAN SLATE
    print("🧹 Cleaning database...")
    ServiceRequest.objects.all().delete()
    WorkflowStep.objects.all().delete()
    ServiceConfig.objects.all().delete()
    MDA.objects.all().delete()
    ServiceCategory.objects.all().delete()
    ServiceDomain.objects.all().delete()

    # 2. LOAD DATA SOURCES
    csv_path = os.path.join(os.path.dirname(__file__), 'all_wog_services.csv')
    json_path = os.path.join(os.path.dirname(__file__), 'citizen_lifecycle.json')

    if not os.path.exists(csv_path) or not os.path.exists(json_path):
        print("❌ Data files missing (CSV or JSON).")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        lifecycle_data = json.load(f)

    # 3. OPTIMIZED DEFINITIONS (from Lifecycle v3.3)
    # These override the generic CSV data
    LIFECYCLE_MAP = {
        "WF-STEP-01": {
            "mda": "MINISTRY OF HEALTH",
            "service": "Birth Notification (B1)",
            "code": "MOH-NOTIF-001",
            "schema": {
                "type": "object",
                "required": ["child_name", "mother_id", "child_gender", "date_of_birth", "place_of_birth"],
                "properties": {
                    "child_name": {
                        "type": "string", 
                        "title": "Child's Full Name",
                        "description": "Enter the name as it should appear on the birth certificate"
                    },
                    "mother_id": {
                        "type": "string", 
                        "title": "Mother's ID Number", 
                        "x-registry-config": {
                            "adapter_id": "IPRS",
                            "endpoint_id": "Verify Citizen Identity"
                        },
                        "description": "Validation: Real-time IPRS Identity Check"
                    },
                    "child_gender": {
                        "type": "string", 
                        "enum": ["Male", "Female"], 
                        "title": "Child Gender"
                    },
                    "date_of_birth": {
                        "type": "string", 
                        "format": "date", 
                        "title": "Date of Birth"
                    },
                    "place_of_birth": {
                        "type": "string", 
                        "title": "Place of Birth (Hospital/Clinic)", 
                        "description": "Captured at source by medical personnel"
                    }
                }
            },
            "custom_workflow": [
                {"name": "Source Capture", "role": "Medical Staff", "type": "manual", "description": "Enter birth details directly at point of event"},
                {"name": "Identity Link (IPRS)", "role": "System", "type": "api_call", "action": "IPRS_LINK", "description": "Auto-fetch and validate Mother's details"},
                {"name": "UPI Minting", "role": "System", "type": "api_call", "action": "MINT_UPI", "description": "Generate Maisha Namba (UPI) for the newborn"},
                {"name": "Notification", "role": "System", "type": "api_call", "action": "SEND_SMS", "description": "Send SMS to Parent with UPI and cert link"}
            ]
        },
        "WF-STEP-01b": { 
            "mda": "CIVIL REGISTRATION SERVICES (CRS)",
            "service": "Birth Certificate Issuance",
            "code": "CRS-CERT-001",
            "schema": {
                "type": "object",
                "required": ["notification_number", "child_name", "parent_consent"],
                "properties": {
                    "notification_number": {"type": "string", "title": "Notification Number (B1)", "description": "Inherited from Hospital Notification"},
                    "child_name": {"type": "string", "title": "Child's Full Name"},
                    "parent_consent": {"type": "boolean", "title": "Confirm Accuracy & Consent"}
                }
            },
            "custom_workflow": [
                {"name": "Application Initiation", "role": "Citizen", "type": "manual", "description": "Verify B1 and apply via eCitizen"},
                {"name": "Verification", "role": "CRS Officer", "type": "manual", "description": "Internal record audit"},
                {"name": "Payment Processing", "role": "System", "type": "api_call", "action": "PROCESS_PAYMENT"},
                {"name": "Issuance", "role": "System", "type": "api_call", "action": "GENERATE_E_CERT", "description": "Generate Verifiable Digital Certificate"}
            ]
        },
        "WF-STEP-02": {
            "mda": "SOCIAL HEALTH AUTHORITY (SHA)",
            "service": "Universal Health Coverage (UHC)",
            "code": "SHA-UHC-001",
            "schema": {
                "type": "object",
                "required": ["upi"],
                "properties": {
                    "upi": {"type": "string", "title": "Maisha Namba (UPI)", "readOnly": True},
                    "dependants": {"type": "array", "title": "Dependants (Linked via CRS)", "items": {"type": "string"}},
                    "income_band": {"type": "string", "title": "Contribution Category (Means Tested)"}
                }
            },
            "custom_workflow": [
                {"name": "Profile Creation", "role": "System", "type": "api_call", "action": "SYNC_IPRS", "description": "Fetch bio-data from National Population Registry"},
                {"name": "Dependant Linking", "role": "System", "type": "api_call", "action": "SYNC_CRS", "description": "Auto-link dependents from CRS records"},
                {"name": "Means Assessment", "role": "System", "type": "api_call", "action": "KRA_ASSESS", "description": "Determine contribution via KRA/Mobile Money APIs"},
                {"name": "Coverage Activation", "role": "System", "type": "api_call", "action": "ACTIVATE_SHA", "description": "Instant activation upon payment/assignment"}
            ]
        },
        "WF-STEP-03": {
            "mda": "MINISTRY OF EDUCATION",
            "service": "Student Enrollment (NEMIS)",
            "code": "MOE-NEMIS-001",
            "schema": {
                "type": "object",
                "required": ["child_upi", "school_code"],
                "properties": {
                    "child_upi": {"type": "string", "title": "Child Maisha Namba (UPI)"},
                    "school_code": {
                        "type": "string", 
                        "title": "Select School", 
                        "widget": "registry_search",
                        "x-registry-config": {
                            "adapter_id": "SCHOOLS_REGISTRY",
                            "endpoint_id": "Search Schools"
                        }
                    },
                    "parent_id": {"type": "string", "title": "Parent/Guardian ID"}
                }
            },
            "custom_workflow": [
                {"name": "Enrollment Request", "role": "Citizen", "type": "manual", "description": "Select child and school on eCitizen"},
                {"name": "UPI Validation", "role": "System", "type": "api_call", "action": "VAL_UPI", "description": "Verify child existence via CRS Registry"},
                {"name": "Capacity Check", "role": "System", "type": "api_call", "action": "CHK_CAPACITY", "description": "Real-time check via National Schools Registry"},
                {"name": "Admission Review", "role": "School Head", "type": "manual", "description": "Digital review and one-click approval"},
                {"name": "Enrollment Sync", "role": "System", "type": "api_call", "action": "SYNC_NEMIS", "description": "Finalize record and trigger capitation"}
            ]
        },
        "WF-STEP-04": {
            "mda": "NATIONAL REGISTRATION BUREAU (NRB)",
            "service": "Maisha Namba Upgrade (ID)",
            "code": "NRB-ID-001",
            "schema": {
                "type": "object",
                "required": ["upi", "current_photo", "fingerprints", "physical_address"],
                "properties": {
                    "upi": {"type": "string", "title": "Maisha Namba (UPI)"},
                    "current_photo": {"type": "string", "format": "data-url", "title": "Live Photo (ICAO Standard)"},
                    "fingerprints": {"type": "string", "format": "binary", "title": "Biometric Template (WSQ)"},
                    "physical_address": {"type": "string", "title": "Residential Address", "widget": "geo_address"},
                    "mobile_number": {"type": "string", "title": "Mobile Number"},
                    "signature": {"type": "string", "format": "data-url", "title": "Digital Signature"}
                }
            },
            "custom_workflow": [
                {"name": "Initiation", "role": "Citizen", "type": "manual", "description": "Request upgrade via eCitizen"},
                {"name": "Data Fetch", "role": "System", "type": "api_call", "action": "FETCH_CRS", "description": "Pull child record from CRS"},
                {"name": "Auto-Vetting", "role": "System", "type": "api_call", "action": "VET_CITIZEN", "description": "Verify citizenship status automatically"},
                {"name": "Biometric Capture", "role": "NRB Officer", "type": "manual", "description": "Live scan at Local Hub/Huduma Centre"},
                {"name": "Identity Linkage", "role": "System", "type": "api_call", "action": "LINK_BIO", "description": "Update Maisha Database to Adult status"},
                {"name": "Virtual ID Issuance", "role": "System", "type": "api_call", "action": "ISSUE_ID", "description": "Generate Digital ID in Maisha Wallet"}
            ]
        },
        "WF-STEP-05": {
            "mda": "KENYA REVENUE AUTHORITY (KRA)",
            "service": "Taxpayer Registration (PIN)",
            "code": "KRA-TAX-001",
            "schema": {
                "type": "object",
                "required": ["virtual_id"],
                "properties": {
                    "virtual_id": {"type": "string", "title": "National Digital ID (Maisha)", "readOnly": True},
                    "economic_status": {"type": "string", "enum": ["Employed", "Business", "Student"], "title": "Primary Source of Income"}
                }
            },
            "custom_workflow": [
                {"name": "Identity Sync", "role": "System", "type": "api_call", "action": "SYNC_ID", "description": "Fetch verified identity via Maisha API"},
                {"name": "PIN Allocation", "role": "System", "type": "api_call", "action": "GEN_PIN", "description": "Automatic KRA PIN generation"},
                {"name": "Registry Update", "role": "System", "type": "api_call", "action": "UPD_KRA", "description": "Initialize Taxpayer Ledger"},
                {"name": "Notification", "role": "System", "type": "api_call", "action": "SEND_NOTIF", "description": "Proactive SMS with new PIN details"}
            ]
        },
        "WF-STEP-06": {
            "mda": "STATE DEPARTMENT FOR IMMIGRATION",
            "service": "Passport Issuance",
            "code": "IMM-PASS-001",
            "schema": {
                "type": "object",
                "required": ["virtual_id", "passport_type", "current_photo", "delivery_address"],
                "properties": {
                    "virtual_id": {"type": "string", "title": "Digital ID (Maisha)", "readOnly": True},
                    "passport_type": {"type": "string", "enum": ["32 Pages", "50 Pages", "66 Pages"], "title": "Booklet Size"},
                    "current_photo": {"type": "string", "format": "data-url", "title": "Live Selfie (ICAO AI Check)"},
                    "delivery_address": {"type": "string", "title": "Posta Delivery Address", "widget": "geo_address"}
                }
            },
            "custom_workflow": [
                {"name": "Digital Application", "role": "Citizen", "type": "manual", "description": "ICAO Selfie capture on eCitizen App"},
                {"name": "Biometric Reuse", "role": "System", "type": "api_call", "action": "REUSE_BIO", "description": "Fetch fingerprints from NRB Maisha Database"},
                {"name": "Auto-Approval", "role": "System", "type": "api_call", "action": "AUTO_APP", "description": "Security screening and approval rules"},
                {"name": "Booklet Production", "role": "System", "type": "api_call", "action": "PRINT_PPT", "description": "Trigger booklet printing"},
                {"name": "Secure Delivery", "role": "System", "type": "api_call", "action": "POSTA_DELIVERY", "description": "Dispatch via Posta with tracking"}
            ]
        },
        "WF-STEP-07": {
            "mda": "BUSINESS REGISTRATION SERVICE (BRS)",
            "service": "Business Incorporation",
            "code": "BRS-INC-001",
            "schema": {
                "type": "object",
                "required": ["proposed_name", "entity_type", "nature_of_business", "directors"],
                "properties": {
                    "proposed_name": {"type": "string", "title": "Proposed Business Name", "description": "Subject to AI Phonetic Check"},
                    "entity_type": {"type": "string", "enum": ["Business Name", "Private Limited", "LLP"], "title": "Legal Entity Type"},
                    "nature_of_business": {"type": "string", "title": "Nature of Business (ISIC Codes)"},
                    "directors": {"type": "array", "title": "List of Directors (IDs)", "items": {"type": "string"}}
                }
            },
            "custom_workflow": [
                {"name": "Name Reservation", "role": "System", "type": "api_call", "action": "AI_NAME_CHECK", "description": "Instant algorithmic name clearance"},
                {"name": "Director Verification", "role": "System", "type": "api_call", "action": "VERIFY_ID", "description": "ID validation against IPRS"},
                {"name": "Director Consent", "role": "Director", "type": "manual", "description": "In-app biometric/PIN consent by directors"},
                {"name": "Bundled Payment", "role": "System", "type": "api_call", "action": "GPA_PAY", "description": "Process unified registration & tax fees"},
                {"name": "Digital Minting", "role": "System", "type": "api_call", "action": "ISSUE_CERT", "description": "Instant issuance of Certificate & CR12"}
            ]
        },
        "WF-STEP-08": {
            "mda": "STATE LAW OFFICE",
            "service": "Marriage Registration",
            "code": "AG-MAR-001",
            "schema": {
                "type": "object",
                "required": ["groom_id", "bride_id", "marriage_type", "officiant_id"],
                "properties": {
                    "groom_id": {"type": "string", "title": "Groom ID (Maisha)", "x-registry-config": {"adapter_id": "IPRS", "endpoint_id": "Verify Citizen Identity"}},
                    "bride_id": {"type": "string", "title": "Bride ID (Maisha)", "x-registry-config": {"adapter_id": "IPRS", "endpoint_id": "Verify Citizen Identity"}},
                    "marriage_type": {"type": "string", "enum": ["Civil", "Christian", "Customary", "Hindu"], "title": "Marital Category"},
                    "officiant_id": {"type": "string", "title": "Licensed Officiant ID"}
                }
            },
            "custom_workflow": [
                {"name": "Joint Digital Notice", "role": "Citizen", "type": "manual", "description": "Submit notice via eCitizen; status auto-verified"},
                {"name": "Payment & Publishing", "role": "System", "type": "api_call", "action": "PUB_GAZETTE", "description": "Auto-post on e-Gazette for 21 days"},
                {"name": "License Issuance", "role": "System", "type": "api_call", "action": "ISSUE_LICENSE", "description": "Generate Digital Marriage License (QR)"},
                {"name": "Solemnization", "role": "Registrar", "type": "manual", "description": "Scan QR and sign digitally during ceremony"},
                {"name": "Registry Update", "role": "System", "type": "api_call", "action": "SYNC_MARRIAGE", "description": "Update IPRS status and issue E-Cert"}
            ]
        },
        "WF-STEP-09": {
            "mda": "MINISTRY OF LANDS",
            "service": "Land Transfer (Ardhisasa)",
            "code": "LND-TRF-001",
            "schema": {
                "type": "object",
                "required": ["parcel_no", "buyer_id", "seller_id", "transfer_type", "sale_price", "consent_bio"],
                "properties": {
                    "parcel_no": {"type": "string", "title": "Parcel/Folio Number"},
                    "buyer_id": {"type": "string", "title": "Buyer ID"},
                    "seller_id": {"type": "string", "title": "Seller ID"},
                    "transfer_type": {"type": "string", "enum": ["Sale", "Inheritance", "Court Order"]},
                    "sale_price": {"type": "number", "title": "Valuation (KES)"},
                    "consent_bio": {"type": "boolean", "title": "Biometric Seller/Buyer Consent"}
                }
            },
            "custom_workflow": [
                {"name": "Smart Transfer Initiation", "role": "Citizen", "type": "manual", "description": "Biometric verification of parties via Maisha"},
                {"name": "Property Audit", "role": "System", "type": "api_call", "action": "CHK_LIEN", "description": "Automated check for encumbrances/cautions"},
                {"name": "Digital Consents", "role": "Partner", "type": "manual", "description": "Spousal/Board consent via e-Signatures"},
                {"name": "Tax Settlement", "role": "System", "type": "api_call", "action": "PAY_STAMP", "description": "Integrated Stamp Duty settlement"},
                {"name": "Execution", "role": "System", "type": "api_call", "action": "RUN_CONTRACT", "description": "Smart contract land registry update"},
                {"name": "Digital Title Issuance", "role": "System", "type": "api_call", "action": "ISSUE_TITLE", "description": "New verifiable digital title to wallet"}
            ]
        },
        "WF-STEP-10": {
            "mda": "THE JUDICIARY",
            "service": "Succession & Probate",
            "code": "JUD-SUCC-001",
            "schema": {
                "type": "object",
                "required": ["death_cert_no", "probate_type", "beneficiaries"],
                "properties": {
                    "death_cert_no": {"type": "string", "title": "Death Certificate No", "lookup_service": "CRS"},
                    "probate_type": {"type": "string", "enum": ["Intestate", "Testate"], "title": "Probate Classification"},
                    "beneficiaries": {"type": "array", "title": "Heir Digital IDs", "items": {"type": "string"}},
                    "asset_inventory": {"type": "array", "title": "Discovered Assets", "items": {"type": "string"}, "readOnly": True}
                }
            },
            "custom_workflow": [
                {"name": "Case Initiation", "role": "System", "type": "api_call", "action": "OPEN_CASE", "description": "Auto-creation triggered by digital death certificate"},
                {"name": "Asset Discovery", "role": "System", "type": "api_call", "action": "DISC_ASSETS", "description": "Inter-agency inventory (Lands, NTSA, Banks)"},
                {"name": "Verif & Proposal", "role": "Executor", "type": "manual", "description": "Verify assets and input distribution plan"},
                {"name": "e-Gazettement", "role": "System", "type": "api_call", "action": "PUB_CASE", "description": "Instant 30-day digital notice publication"},
                {"name": "AI Validation", "role": "System", "type": "api_call", "action": "AI_AUDIT", "description": "Compliance check vs Law of Succession"},
                {"name": "Grant Issuance", "role": "System", "type": "api_call", "action": "ISSUE_GRANT", "description": "Verifiable Digital Grant to executor's wallet"}
            ]
        },
        "WF-STEP-11": {
            "mda": "CIVIL REGISTRATION SERVICES (CRS)",
            "service": "Death Registration",
            "code": "CRS-DEATH-001",
            "schema": {
                "type": "object",
                "required": ["deceased_id", "date_of_death", "cause_of_death", "informant_id"],
                "properties": {
                    "deceased_id": {"type": "string", "title": "Deceased's National ID/UPI"},
                    "date_of_death": {"type": "string", "format": "date", "title": "Date of Death"},
                    "cause_of_death": {"type": "string", "title": "Cause of Death (ICD-11)"},
                    "informant_id": {"type": "string", "title": "Informant's National ID"}
                }
            },
            "custom_workflow": [
                {"name": "Source Capture", "role": "Medical Staff", "type": "manual", "description": "Digital notification by hospital/chief"},
                {"name": "IPRS Status Update", "role": "System", "type": "api_call", "action": "IPRS_DEATH", "description": "Instantly freeze ID to prevent fraud"},
                {"name": "Burial Permit", "role": "System", "type": "api_call", "action": "ISSUE_PERMIT", "description": "Auto-generate verifiable QR burial permit"},
                {"name": "Cert Application", "role": "Next of Kin", "type": "manual", "description": "Apply via eCitizen using Digital Permit ID"},
                {"name": "Issuance", "role": "System", "type": "api_call", "action": "GEN_DEATH_CERT", "description": "Generate digital verifiable death certificate"}
            ]
        }
    }


    # Enrich Lifecycle Schema with Field Definitions from JSON
    form_definitions = {f['field_name']: f for f in lifecycle_data.get('input_form', [])}
    for step_id, config in LIFECYCLE_MAP.items():
        if 'schema' in config and 'properties' in config['schema']:
            for field_name, prop in config['schema']['properties'].items():
                if field_name in form_definitions:
                    f_def = form_definitions[field_name]
                    if 'label' in f_def: prop['title'] = f_def['label']
                    if 'validation' in f_def: prop['description'] = f"Validation: {f_def['validation']}"
                    if 'source' in f_def: prop['x-source'] = f_def['source']

    # 4. PREPARE DOMAIN
    domain, _ = ServiceDomain.objects.get_or_create(
        name="Whole of Government",
        defaults={"description": "Unified Citizen and Business Service Catalogue"}
    )

    # 5. MAPPING DICTIONARY FOR FAST MATCHING
    # Match on normalized (Service Name, MDA Name) or Keywords
    MATCH_MAP = {}
    for step_id, config in LIFECYCLE_MAP.items():
        key = (config['service'].lower(), config['mda'].lower())
        MATCH_MAP[key] = config

    # Explicit Aliases (CSV Name -> Step ID)
    ALIASES = {
        "Passport Application": "WF-STEP-06",
        "National ID Application": "WF-STEP-04",
        "Birth Registration": "WF-STEP-01b",
        "Issuance of Birth Certificate": "WF-STEP-01b",
        "Marriage Registration": "WF-STEP-08",
        "Business Registration": "WF-STEP-07",
        "Registration of Business Name": "WF-STEP-07",
        "Company Incorporation": "WF-STEP-07",
        "Business Name Registration": "WF-STEP-07",
        "Land Transfer": "WF-STEP-09",
        "Transfer of Land Ownership": "WF-STEP-09",
        "Death Registration": "WF-STEP-11",
        "NHIF Registration": "WF-STEP-02",
        "Student Enrollment": "WF-STEP-03",
        "Tax Compliance Certificates": "WF-STEP-05",
        "Registration of Basic Education Institutions": "WF-STEP-03"
    }

    seeded_codes = set()
    service_count = 0

    # 6. ITERATE THROUGH CSV
    print(f"📦 Seeding from {csv_path}...")
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 5: continue
            
            orig_code = row[0]
            mda_name = row[3]
            svc_name = row[4]
            svc_type = row[5]
            
            # ----------------------------------------------------
            # MATCHING LOGIC
            # ----------------------------------------------------
            optimized = None
            
            # 1. Direct Name/MDA Match
            key = (svc_name.lower(), mda_name.lower())
            optimized = MATCH_MAP.get(key)
            
            # 2. Alias Match
            if not optimized and svc_name in ALIASES:
                optimized = LIFECYCLE_MAP.get(ALIASES[svc_name])
                
            # 3. Keyword Heuristic
            if not optimized:
                for alias_name, step_id in ALIASES.items():
                    if alias_name.lower() in svc_name.lower():
                        optimized = LIFECYCLE_MAP.get(step_id)
                        break

            if optimized:
                print(f"  ✨ Optimized: {svc_name} -> {optimized['service']} ({optimized['code']})")
                code = optimized['code']
                mda_full_name = optimized['mda']
                schema = optimized['schema']
                workflow = optimized.get('custom_workflow')
                tags = ["Lifecycle", "Cradle-to-Death", "Optimized"]
                description = f"Optimized {svc_name} as part of the Kenya Citizen Lifecycle."
                category_name = optimized['service']
            else:
                code = orig_code
                mda_full_name = mda_name
                schema = {} 
                workflow = None
                tags = ["Generic", svc_type]
                description = f"{svc_name} provided by {mda_name}."
                # Use Department for generic categories
                category_name = row[2] if row[2] else "General"

            # Skip if we already seeded this code (deduplication)
            if code in seeded_codes: continue
            
            # Create/Get MDA
            mda_code = code.split('-')[0]
            mda, _ = MDA.objects.get_or_create(
                code=mda_code,
                defaults={"name": mda_full_name}
            )
            
            # Create/Get Category
            cat, _ = ServiceCategory.objects.get_or_create(
                name=category_name,
                domain=domain
            )
            
            # ----------------------------------------------------
            # LIFE EVENT MAPPING
            # ----------------------------------------------------
            life_event = "Other"
            if optimized:
                for s in lifecycle_data.get('workflow', {}).get('steps', []):
                    if s.get('step_id') in LIFECYCLE_MAP and LIFECYCLE_MAP[s['step_id']]['code'] == code:
                        life_event = s.get('life_event', "Other")
                        break
            else:
                mda_upper = mda_full_name.upper()
                svc_upper = svc_name.upper()
                
                # Broad MDA based mapping
                if any(k in mda_upper for k in ["EDUCATION", "TSC", "KNEC", "UNIVERSITY", "SCHOOL"]): life_event = "Education"
                elif any(k in mda_upper for k in ["HEALTH", "SHA", "HOSPITAL", "MEDICAL", "NHIF"]): life_event = "Health"
                elif any(k in mda_upper for k in ["LAND", "ARDHISASA", "HOUSING", "PLANNING", "SURVEY"]): life_event = "Property"
                elif any(k in mda_upper for k in ["BUSINESS", "BRS", "COMPANIES", "TRADE", "INVESTMENT", "INDUSTRY"]): life_event = "Business"
                elif any(k in mda_upper for k in ["TAX", "KRA", "REVENUE", "TREASURY", "FINANCE", "PFM"]): life_event = "Finance"
                elif any(k in mda_upper for k in ["IMMIGRATION", "PASSPORT", "FOREIGN"]): life_event = "Travel"
                elif any(k in mda_upper or k in svc_upper for k in ["NRB", "REGISTRATION OF PERSONS", "ID "]): life_event = "Adulthood"
                elif any(k in mda_upper or k in svc_upper for k in ["CRS", "CIVIL REGISTRATION", "BIRTH", "DEATH"]): life_event = "Civil Status"
                elif any(k in mda_upper or k in svc_upper for k in ["MARRIAGE", "AG-MAR", "STATE LAW"]): life_event = "Marriage"
                elif any(k in mda_upper for k in ["JUDICIARY", "JUSTICE", "LEGAL"]): life_event = "Legal"
                elif any(k in mda_upper for k in ["TRANSPORT", "NTSA", "ROADS", "AVIATION", "MARITIME"]): life_event = "Transport"
                elif any(k in mda_upper for k in ["SOCIAL", "NSSF", "PROTECTION", "GENDER", "YOUTH", "CULTURE"]): life_event = "Social Welfare"
                elif any(k in mda_upper for k in ["POLICE", "SECURITY", "INTERIOR", "DEFENCE"]): life_event = "Security"
                elif any(k in mda_upper for k in ["AGRICULTURE", "LIVESTOCK", "FISHERIES"]): life_event = "Agriculture"
                elif any(k in mda_upper for k in ["ENERGY", "WATER", "ENVIRONMENT", "WILDLIFE"]): life_event = "Infrastructure"

            # Create Service
            service = ServiceConfig.objects.create(
                service_code=code,
                service_name=svc_name if not optimized else optimized['service'],
                mda=mda,
                category=cat,
                description=description,
                service_type=svc_type if not optimized else "G2C",
                digitization_level=5 if optimized else 3,
                service_status="active",
                catalogue_visible=True,
                catalogue_tags=tags,
                life_event_group=life_event,
                form_schema=schema,
                config={"rules": {"schema": schema}}
            )
            
            seeded_codes.add(code)
            
            # Create Workflow Steps
            if workflow:
                for i, step_def in enumerate(workflow):
                    raw_type = step_def['type']
                    normalized_type = 'manual'
                    if raw_type in ['api_call', 'system_task', 'event', 'auto']:
                        normalized_type = 'api_call'
                    WorkflowStep.objects.create(
                        service_config=service,
                        step_name=step_def['name'],
                        step_type=normalized_type,
                        role=step_def['role'],
                        sequence=i+1,
                        lifecycle_stage="to_be",
                        api_config=step_def.get('api_config', {})
                    )
            elif optimized:
                # Default 3-step for optimized without custom workflow
                WorkflowStep.objects.create(service_config=service, step_name="Trigger Event", step_type="api_call", role="System", sequence=1, lifecycle_stage="to_be")
                WorkflowStep.objects.create(service_config=service, step_name="Processing & Validation", step_type="api_call", role="System", sequence=2, lifecycle_stage="to_be")
                WorkflowStep.objects.create(service_config=service, step_name="Registry Update", step_type="api_call", role="System", sequence=3, lifecycle_stage="to_be")
            else:
                # Default 3-step workflow for generic services
                WorkflowStep.objects.create(service_config=service, step_name="Application Submission", step_type="api_call", role="Citizen", sequence=1, lifecycle_stage="as_is")
                WorkflowStep.objects.create(service_config=service, step_name="MDA Processing", step_type="manual", role="Officer", sequence=2, lifecycle_stage="as_is")
                WorkflowStep.objects.create(service_config=service, step_name="Final Approval", step_type="manual", role="Supervisor", sequence=3, lifecycle_stage="as_is")

            service_count += 1

    # 7. FORCE SEED ANY LIFECYCLE ITEMS THAT DIDN'T MATCH CSV
    print("🛰️ Ensuring all Lifecycle Services are present...")
    for step_id, config in LIFECYCLE_MAP.items():
        if config['code'] in seeded_codes: continue
        
        print(f"  🆕 Adding Missing Lifecycle: {config['service']} ({config['code']})")
        mda_code = config['code'].split('-')[0]
        mda, _ = MDA.objects.get_or_create(code=mda_code, defaults={"name": config['mda']})
        cat, _ = ServiceCategory.objects.get_or_create(name=config['service'], domain=domain)
        
        # Get life event from JSON
        life_event = "Other"
        for s in lifecycle_data.get('workflow', {}).get('steps', []):
            if s.get('step_id') == step_id:
                life_event = s.get('life_event', "Other")
                break

        service = ServiceConfig.objects.create(
            service_code=config['code'],
            service_name=config['service'],
            mda=mda,
            category=cat,
            description=f"Lifecycle Optimized: {config['service']}",
            service_type="G2C",
            digitization_level=5,
            service_status="active",
            catalogue_visible=True,
            catalogue_tags=["Lifecycle", "Cradle-to-Death", "Optimized"],
            life_event_group=life_event,
            form_schema=config['schema'],
            config={"rules": {"schema": config['schema']}}
        )
        
        workflow = config.get('custom_workflow')
        if workflow:
            for i, step in enumerate(workflow):
                # Normalize step type for the engine (Manual or API Call)
                raw_type = step['type']
                normalized_type = 'manual'
                if raw_type in ['api_call', 'system_task', 'event', 'auto']:
                    normalized_type = 'api_call'
                
                WorkflowStep.objects.create(
                    service_config=service, 
                    step_name=step['name'], 
                    step_type=normalized_type, 
                    role=step['role'], 
                    sequence=i+1, 
                    lifecycle_stage="to_be",
                    action=step.get('action'),
                    api_config=step.get('api_config', {})
                )
        else:
            WorkflowStep.objects.create(service_config=service, step_name="Trigger Event", step_type="api_call", role="System", sequence=1, lifecycle_stage="to_be")
            WorkflowStep.objects.create(service_config=service, step_name="Processing", step_type="api_call", role="System", sequence=2, lifecycle_stage="to_be")
            WorkflowStep.objects.create(service_config=service, step_name="Record Finalization", step_type="api_call", role="System", sequence=3, lifecycle_stage="to_be")
            
        seeded_codes.add(config['code'])
        service_count += 1

    print(f"\n✅ UNIFIED SEEDING COMPLETE. Total Services: {service_count}")

if __name__ == "__main__":
    seed_unified_catalogue()
