import os
import django
import json
import random

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig, MDA, ServiceCategory, ServiceDomain, WorkflowStep, RegistryAdapter, RegistryEndpoint

def get_registry_ids(adapter_code, endpoint_name):
    try:
        adapter = RegistryAdapter.objects.filter(code=adapter_code).first()
        if not adapter: return None, None
        endpoint = RegistryEndpoint.objects.filter(adapter=adapter, name=endpoint_name).first()
        return (adapter.id, endpoint.id) if endpoint else (adapter.id, None)
    except:
        return None, None

def run_lifecycle_seed_v3():
    print("=" * 80)
    print("🚀 CRADLE-TO-DEATH LIFECYCLE SEEDER v3.4 (Registry Registry IDs Fix)")
    print("=" * 80)

    iprs_adapter_id, person_lookup_id = get_registry_ids("IPRS", "Verify Citizen Identity")

    # Path to the v3.0 Lifecycle Definition
    json_path = os.path.join(os.path.dirname(__file__), 'citizen_lifecycle.json')
    if not os.path.exists(json_path):
        print(f"❌ V3 Lifecycle file not found at {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        lifecycle_data = json.load(f)

    # 1. Base Domain
    domain, _ = ServiceDomain.objects.get_or_create(
        name="Citizen Lifecycle",
        defaults={"description": "End-to-End Government Service Delivery"}
    )

    # 2. DEFINITIONS
    LIFECYCLE_MAP = {
        "WF-STEP-01": {
            "mda": "MINISTRY OF HEALTH (HOSPITAL)",
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
                {
                    "name": "Capture Details", 
                    "role": "Hospital_Staff", 
                    "type": "manual",
                    "bpmn_element": "user_task"
                },
                {
                    "name": "Validate Parent", 
                    "role": "System", 
                    "type": "system_task",
                    "bpmn_element": "service_task",
                    "action": "IPRS_CHECK"
                },
                {
                    "name": "Generate B1 Number", 
                    "role": "System", 
                    "type": "api_call",
                    "bpmn_element": "service_task",
                    "api_config": {
                        "endpoint": "CRS: Create Notification",
                        "mappings": {
                            "output": {"notification_number": "b1_number"}
                        }
                    }
                },
                {
                    "name": "Notify Parent", 
                    "role": "System", 
                    "type": "system_task",
                    "bpmn_element": "service_task",
                    "action": "SEND_SMS"
                }
            ]
        },
        "WF-STEP-01b": { 
            "mda": "CIVIL REGISTRATION SERVICES (CRS)",
            "service": "Birth Certificate Issuance",
            "code": "CRS-CERT-001",
            "schema": {
                "type": "object",
                "required": ["notification_number"],
                "properties": {
                    "notification_number": {"type": "string", "title": "Notification Number (B1)", "readOnly": True, "description": "Auto-fetched from Hospital"},
                    "child_name": {"type": "string", "title": "Child's Full Name"},
                    "parent_consent": {"type": "boolean", "title": "Confirm Details"}
                }
            }
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
                    "biometric_face": {"type": "string", "format": "data-url", "title": "Face ID"}
                }
            }
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
                    "school_code": {"type": "string", "title": "School Code", "widget": "search"}
                }
            }
        },
        "WF-STEP-04": {
            "mda": "NATIONAL REGISTRATION BUREAU (NRB)",
            "service": "Maisha Namba Upgrade (ID)",
            "code": "NRB-ID-001",
            "schema": {
                "type": "object",
                "required": ["upi", "fingerprints"],
                "properties": {
                    "upi": {"type": "string", "title": "Existing UPI", "readOnly": True},
                    "fingerprints": {"type": "string", "format": "binary", "title": "Biometric Template (WSQ)"},
                    "photo_icao": {"type": "string", "format": "data-url", "title": "Current Photo"}
                }
            }
        },
        "WF-STEP-05": {
            "mda": "KENYA REVENUE AUTHORITY (KRA)",
            "service": "Tax Compliance (Invisible Tax)",
            "code": "KRA-TAX-001",
            "schema": {
                "type": "object",
                "required": ["virtual_id"],
                "properties": {
                    "virtual_id": {"type": "string", "title": "Digital ID", "readOnly": True},
                    "tax_statement": {"type": "string", "widget": "html_view", "title": "Annual Statement"},
                    "action": {"type": "string", "enum": ["Accept", "Dispute"], "title": "Confirm Accuracy", "widget": "select"}
                }
            }
        },
        "WF-STEP-06": {
            "mda": "STATE DEPARTMENT FOR IMMIGRATION",
            "service": "Passport Issuance",
            "code": "IMM-PASS-001",
            "schema": {
                "type": "object",
                "required": ["virtual_id"],
                "properties": {
                    "virtual_id": {"type": "string", "title": "Digital ID", "readOnly": True},
                    "photo_selfie": {"type": "string", "format": "data-url", "title": "Live Selfie (ICAO Check)"},
                    "passport_type": {"type": "string", "enum": ["32 Pages", "50 Pages", "66 Pages"], "title": "Passport Type", "widget": "select"}
                }
            }
        },
        "WF-STEP-07": {
            "mda": "BUSINESS REGISTRATION SERVICE (BRS)",
            "service": "Business Incorporation",
            "code": "BRS-INC-001",
            "schema": {
                "type": "object",
                "required": ["business_name"],
                "properties": {
                    "virtual_id": {"type": "string", "title": "Director Digital ID", "readOnly": True},
                    "entity_type": {"type": "string", "enum": ["Business Name", "Private Limited Company"], "title": "Entity Type", "widget": "select"},
                    "business_name": {"type": "string", "title": "Proposed Name", "validation": "ai_check"},
                    "directors": {"type": "array", "title": "Director IDs", "items": {"type": "string"}}
                }
            }
        },
        "WF-STEP-08": {
            "mda": "STATE LAW OFFICE (AG)",
            "service": "Marriage Registration",
            "code": "AG-MAR-001",
            "schema": {
                "type": "object",
                "required": ["groom_id", "bride_id"],
                "properties": {
                    "groom_id": {"type": "string", "title": "Groom ID", "lookup_service": "IPRS"},
                    "bride_id": {"type": "string", "title": "Bride ID", "lookup_service": "IPRS"},
                    "marriage_type": {"type": "string", "enum": ["Civil", "Christian", "Customary"], "title": "Marriage Type", "widget": "select"},
                    "officiant_qr": {"type": "string", "title": "License QR Code"}
                }
            }
        },
        "WF-STEP-09": {
            "mda": "MINISTRY OF LANDS",
            "service": "Land Transfer (Ardhisasa)",
            "code": "LND-TRF-001",
            "schema": {
                "type": "object",
                "required": ["parcel_no", "consent_bio"],
                "properties": {
                    "parcel_no": {"type": "string", "title": "Parcel Number"},
                    "transfer_type": {"type": "string", "enum": ["Sale", "Gift", "Succession"], "title": "Transfer Type", "widget": "select"},
                    "sale_price": {"type": "number", "title": "Consideration"},
                    "consent_bio": {"type": "boolean", "title": "Biometric Consent (Seller)"}
                }
            }
        },
        "WF-STEP-10": {
            "mda": "THE JUDICIARY",
            "service": "Succession & Probate",
            "code": "JUD-SUCC-001",
            "schema": {
                "type": "object",
                "required": ["death_cert_no"],
                "properties": {
                    "death_cert_no": {"type": "string", "title": "Death Certificate No", "lookup_service": "CRS"},
                    "cause_type": {"type": "string", "enum": ["Intestate (No Will)", "Testate (Will)"], "title": "Cause Type", "widget": "select"},
                    "asset_inventory": {"type": "object", "title": "Declared Assets"},
                    "beneficiaries": {"type": "array", "title": "Heirs (IDs)", "items": {"type": "string"}}
                }
            }
        }
    }

    # Helper to enrich schemas
    form_definitions = {f['field_name']: f for f in lifecycle_data.get('input_form', [])}
    
    for step_id, config in LIFECYCLE_MAP.items():
        if 'schema' in config and 'properties' in config['schema']:
            for field_name, prop in config['schema']['properties'].items():
                if field_name in form_definitions:
                    f_def = form_definitions[field_name]
                    if 'label' in f_def: prop['title'] = f_def['label']
                    if 'validation' in f_def: prop['description'] = f"Validation: {f_def['validation']}"
                    if 'source' in f_def: prop['x-source'] = f_def['source']

    # 3. Seeding Loop
    for step_id, config in LIFECYCLE_MAP.items():
        json_step = next((s for s in lifecycle_data.get('workflow', {}).get('steps', []) if s['step_id'] == step_id), {})
        
        mda_code = config['code'].split('-')[0]
        mda, _ = MDA.objects.get_or_create(code=mda_code, defaults={"name": config['mda']})
        category, _ = ServiceCategory.objects.get_or_create(name=config['service'], domain=domain)

        # ----------------------------------------------------
        # DEDUPLICATION LOGIC
        # 1. Find ANY generic service with same name/MDA but different code
        # ----------------------------------------------------
        generic_duplicates = ServiceConfig.objects.filter(
            service_name__iexact=config['service'], 
            mda=mda
        ).exclude(service_code=config['code'])
        
        if generic_duplicates.exists():
            print(f"  🧹 Removing {generic_duplicates.count()} generic duplicate(s) for {config['service']}...")
            generic_duplicates.delete()

        # 2. Update or Create the Lifecycle Service
        service, created = ServiceConfig.objects.update_or_create(
            service_code=config['code'],
            defaults={
                "service_name": config['service'],
                "mda": mda,
                "category": category,
                "catalogue_tags": ["Lifecycle", "Cradle-to-Death"],
                "description": json_step.get('description', config['service']),
                "service_type": "G2C",
                "digitization_level": 5,
                "service_status": "active",
                "catalogue_visible": True,
                "form_schema": config['schema'],
                "config": {"rules": {"schema": config['schema']}}
            }
        )
        
        status = "Created" if created else "Updated"
        print(f"  ✅ {status}: {config['service']} ({config['code']})")

        # Workflow Steps
        WorkflowStep.objects.filter(service_config=service).delete()
        
        # Use custom workflow if defined (e.g., for Hospital Notification), else default
        workflow_def = config.get('custom_workflow')
        
        if workflow_def:
            for i, step in enumerate(workflow_def):
                WorkflowStep.objects.create(
                    service_config=service,
                    step_name=step['name'],
                    step_type=step['type'] if step['type'] != 'system_task' else 'manual', # Map system_task to manual if model choice is limited, or handle accordingly
                    bpmn_element_type=step.get('bpmn_element', 'user_task'),
                    role=step['role'],
                    action=step.get('action'),
                    api_config=step.get('api_config'),
                    sequence=i+1,
                    lifecycle_stage="to_be"
                )
        else:
            # Standard 3-Step Automated Flow
            actor = json_step.get('actor', 'System')
            WorkflowStep.objects.create(service_config=service, step_name="Trigger Event", step_type="event", role=actor, sequence=1, lifecycle_stage="to_be")
            WorkflowStep.objects.create(service_config=service, step_name="Processing & Validation", step_type="system_task", role="System", sequence=2, lifecycle_stage="to_be")
            WorkflowStep.objects.create(service_config=service, step_name="Registry Update", step_type="api_call", role="System", sequence=3, lifecycle_stage="to_be")

    print("\n✅ Cradle-to-Death Seeding Complete (v3.3 - Cleaned).")

if __name__ == "__main__":
    run_lifecycle_seed_v3()
