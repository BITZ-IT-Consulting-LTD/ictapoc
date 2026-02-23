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
            "service": "Birth Notification",
            "code": "MOH-NOTIF-001",
            "schema": {
                "type": "object",
                "required": ["mother_id", "child_gender", "date_of_birth"],
                "properties": {
                    "mother_id": {
                        "type": "string", 
                        "title": "Mother's ID Number", 
                        "widget": "text",
                        "x-registry-config": {
                            "adapter_id": iprs_adapter_id or "IPRS",
                            "endpoint_id": person_lookup_id or "Verify Citizen Identity"
                        },
                        "description": "Validation: IPRS Identity Check"
                    },
                    "child_gender": {
                        "type": "string", 
                        "enum": ["Male", "Female"], 
                        "title": "Child Gender", 
                        "widget": "select"
                    },
                    "date_of_birth": {
                        "type": "string", 
                        "format": "date", 
                        "title": "Date of Birth",
                        "default": "2026-02-19"
                    },
                    "place_of_birth": {
                        "type": "string", 
                        "title": "Place of Birth (Hospital)", 
                        "readOnly": True, 
                        "default": "Kenyatta National Hospital"
                    }
                }
            },
            "custom_workflow": [
                {"name": "Capture Details", "role": "Hospital_Staff", "type": "manual"},
                {"name": "Validate Parent", "role": "System", "type": "api_call", "api_config": {"url": "KESEL_BRIDGE/IPRS/api/v1/citizens/verify"}, "action": "IPRS_CHECK"},
                {"name": "Generate B1 Number", "role": "System", "type": "api_call", "api_config": {"endpoint": "CRS: Create Notification", "mappings": {"output": {"notification_number": "b1_number"}}}},
                {"name": "Notify Parent", "role": "System", "type": "api_call", "action": "SEND_SMS"}
            ]
        },
        "WF-STEP-01b": { 
            "mda": "CIVIL REGISTRATION SERVICES (CRS)",
            "service": "Birth Certificate Issuance",
            "code": "CRS-CERT-001",
            "schema": {
                "type": "object",
                "required": ["notification_number", "child_name"],
                "properties": {
                    "notification_number": {"type": "string", "title": "Notification Number (B1)", "readOnly": True, "description": "Inherited from Hospital Notification"},
                    "child_name": {"type": "string", "title": "Child's Full Name"},
                    "parent_consent": {"type": "boolean", "title": "Confirm Institutional Accuracy"}
                }
            },
            "custom_workflow": [
                {"name": "Initialize Birth Record", "role": "Citizen", "type": "manual"},
                {"name": "Verify B1 Notification", "role": "CRS Officer", "type": "manual"},
                {"name": "MINT MAISHA NAMBA (UPI)", "role": "System", "type": "api_call", "api_config": {"url": "KESEL_BRIDGE/NRB/mint_upi"}},
                {"name": "Final Registrar Approval", "role": "CRS Registrar", "type": "manual"}
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
                    "biometric_face": {"type": "string", "format": "data-url", "title": "Face ID (Newborn Capture)"}
                }
            },
            "custom_workflow": [
                {"name": "Retrieve Maisha Record", "role": "System", "type": "api_call", "api_config": {"url": "KESEL_BRIDGE/IPRS/lookup"}},
                {"name": "Activate Linda Mama Cover", "role": "SHA Officer", "type": "manual"},
                {"name": "Enrollment Confirmation", "role": "System", "type": "api_call", "api_config": {"url": "KESEL_BRIDGE/SHA/register"}}
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
                    "child_upi": {"type": "string", "title": "Child UPI", "lookup_service": "CRS"},
                    "school_code": {"type": "string", "title": "Selection: Institutional Code", "widget": "select", "enum": ["SCH-001 (Kenyatta Primary)", "SCH-002 (Moi Primary)"]}
                }
            },
            "custom_workflow": [
                {"name": "Parental Enrollment Request", "role": "Citizen", "type": "manual"},
                {"name": "Validate UPI Registry", "role": "System", "type": "api_call", "api_config": {"url": "KESEL_BRIDGE/CRS/verify_upi"}},
                {"name": "Head Teacher Admission", "role": "School Head", "type": "manual"},
                {"name": "NEMIS Record Finalization", "role": "System", "type": "api_call", "api_config": {"url": "KESEL_BRIDGE/NEMIS/enroll"}}
            ]
        },
        "WF-STEP-04": {
            "mda": "NATIONAL REGISTRATION BUREAU (NRB)",
            "service": "Maisha Namba Upgrade (ID)",
            "code": "NRB-ID-001",
            "schema": {
                "type": "object",
                "required": ["upi", "fingerprints", "photo_icao"],
                "properties": {
                    "upi": {"type": "string", "title": "Existing UPI (Maisha Namba)", "readOnly": True},
                    "fingerprints": {"type": "string", "format": "binary", "title": "Biometric Template (WSQ)"},
                    "photo_icao": {"type": "string", "format": "data-url", "title": "Current Photo (ICAO Standard)"}
                }
            },
            "custom_workflow": [
                {"name": "Biometric Data Harvest", "role": "NRB Officer", "type": "manual"},
                {"name": "Automated AFIS Deduplication", "role": "System", "type": "api_call", "api_config": {"url": "KESEL_BRIDGE/IPRS/dedup"}},
                {"name": "Identity Authentication", "role": "NRB Supervisor", "type": "manual"},
                {"name": "Secure ID Production", "role": "System", "type": "api_call", "api_config": {"url": "KESEL_BRIDGE/NRB/issue_id"}}
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
                    "virtual_id": {"type": "string", "title": "National Digital ID", "readOnly": True},
                    "occupational_status": {"type": "string", "enum": ["Employed", "Self-Employed", "Student"], "title": "Economic Status"}
                }
            },
            "custom_workflow": [
                {"name": "Identity Sync (NRB)", "role": "System", "type": "api_call", "api_config": {"url": "KESEL_BRIDGE/IPRS/lookup"}},
                {"name": "Generate KRA PIN", "role": "System", "type": "api_call", "api_config": {"url": "KESEL_BRIDGE/KRA/generate_pin"}},
                {"name": "Ledger Initialization", "role": "KRA Officer", "type": "manual"}
            ]
        },
        "WF-STEP-06": {
            "mda": "STATE DEPARTMENT FOR IMMIGRATION",
            "service": "Passport Issuance",
            "code": "IMM-PASS-001",
            "schema": {
                "type": "object",
                "required": ["virtual_id", "photo_selfie"],
                "properties": {
                    "virtual_id": {"type": "string", "title": "Digital ID (Maisha)", "readOnly": True},
                    "photo_selfie": {"type": "string", "format": "data-url", "title": "Live Selfie (Security Audit)"},
                    "passport_type": {"type": "string", "enum": ["32 Pages", "50 Pages", "66 Pages"], "title": "Booklet Size", "widget": "select"}
                }
            },
            "custom_workflow": [
                {"name": "DTC Application Submission", "role": "Citizen", "type": "manual"},
                {"name": "National Security Screening", "role": "Interpol/Police", "type": "api_call"},
                {"name": "Immigration Adjudication", "role": "Immigration Officer", "type": "manual"},
                {"name": "Passport Booklet Production", "role": "System", "type": "api_call"}
            ]
        },
        "WF-STEP-07": {
            "mda": "BUSINESS REGISTRATION SERVICE (BRS)",
            "service": "Business Incorporation",
            "code": "BRS-INC-001",
            "schema": {
                "type": "object",
                "required": ["business_name", "entity_type"],
                "properties": {
                    "virtual_id": {"type": "string", "title": "Director Digital ID", "readOnly": True},
                    "entity_type": {"type": "string", "enum": ["Business Name", "Private Limited", "LLP"], "title": "Institutional Category"},
                    "business_name": {"type": "string", "title": "Proposed Designation", "validation": "ai_check"},
                    "directors": {"type": "array", "title": "Co-Director IDs", "items": {"type": "string"}}
                }
            },
            "custom_workflow": [
                {"name": "AI Name Reservation", "role": "System", "type": "system_task"},
                {"name": "Memorandum Verification", "role": "BRS Legal", "type": "manual"},
                {"name": "Certificate Digital Minting", "role": "System", "type": "api_call"}
            ]
        },
        "WF-STEP-08": {
            "mda": "STATE LAW OFFICE",
            "service": "Marriage Registration",
            "code": "AG-MAR-001",
            "schema": {
                "type": "object",
                "required": ["groom_id", "bride_id", "marriage_type"],
                "properties": {
                    "groom_id": {"type": "string", "title": "Groom ID", "lookup_service": "IPRS"},
                    "bride_id": {"type": "string", "title": "Bride ID", "lookup_service": "IPRS"},
                    "marriage_type": {"type": "string", "enum": ["Civil", "Christian", "Customary", "Hindu"], "title": "Union Category"},
                    "officiant_qr": {"type": "string", "title": "Licensed Officiant ID"}
                }
            },
            "custom_workflow": [
                {"name": "Institutional Notice Filing", "role": "Citizen", "type": "manual"},
                {"name": "Legal Impediment Search", "role": "System", "type": "api_call"},
                {"name": "Marriage Solemnization", "role": "Registrar", "type": "manual"},
                {"name": "Spousal Linkage (IPRS)", "role": "System", "type": "api_call"}
            ]
        },
        "WF-STEP-09": {
            "mda": "MINISTRY OF LANDS",
            "service": "Land Transfer (Ardhisasa)",
            "code": "LND-TRF-001",
            "schema": {
                "type": "object",
                "required": ["parcel_no", "consent_bio"],
                "properties": {
                    "parcel_no": {"type": "string", "title": "Parcel/Folio Number"},
                    "transfer_type": {"type": "string", "enum": ["Sale", "Inheritance", "Court Order"], "title": "Transfer Mechanism"},
                    "sale_price": {"type": "number", "title": "Valuation (KES)"},
                    "consent_bio": {"type": "boolean", "title": "Biometric Seller Consent"}
                }
            },
            "custom_workflow": [
                {"name": "Parcel Search Initiation", "role": "Citizen", "type": "manual"},
                {"name": "Valuation Audit", "role": "Gov Valuer", "type": "manual"},
                {"name": "title Deed Tokenization", "role": "System", "type": "api_call"},
                {"name": "Registry Record Sync", "role": "Land Registrar", "type": "manual"}
            ]
        },
        "WF-STEP-10": {
            "mda": "THE JUDICIARY",
            "service": "Succession & Probate",
            "code": "JUD-SUCC-001",
            "schema": {
                "type": "object",
                "required": ["death_cert_no", "cause_type"],
                "properties": {
                    "death_cert_no": {"type": "string", "title": "Death Certificate No", "lookup_service": "CRS"},
                    "cause_type": {"type": "string", "enum": ["Intestate", "Testate"], "title": "Probate Classification"},
                    "beneficiaries": {"type": "array", "title": "Heir Digital IDs", "items": {"type": "string"}}
                }
            },
            "custom_workflow": [
                {"name": "Cause Filing", "role": "Executor", "type": "manual"},
                {"name": "Estate Inventory Audit", "role": "System", "type": "api_call"},
                {"name": "Judicial Confirmation", "role": "Judge", "type": "manual"},
                {"name": "Asset Distribution Bridge", "role": "System", "type": "api_call"}
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
        "Succession": "WF-STEP-10",
        "Death Registration": "WF-STEP-10",
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
