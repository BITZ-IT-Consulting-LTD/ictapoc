import os
import django
import csv
import json
import re

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig, MDA, ServiceCategory, ServiceDomain, WorkflowStep, Role, User, ServiceRequest, AuditLog

def convert_fields_to_schema(fields_array):
    """Converts a simplified fields array to JSON Schema format for the UI"""
    schema = {
        "type": "object",
        "properties": {},
        "required": []
    }
    for field in fields_array:
        name = field['name']
        prop = {
            "type": "string" if field['type'] != 'number' else "number",
            "title": field['label'],
        }
        if 'options' in field:
            prop['enum'] = [opt['value'] for opt in field['options']]
        if 'validation' in field:
            if 'pattern' in field['validation']: prop['pattern'] = field['validation']['pattern']
            if 'minLength' in field['validation']: prop['minLength'] = field['validation']['minLength']
        
        if field['type'] == 'date': prop['format'] = 'date'
        if field['type'] == 'textarea': prop['format'] = 'textarea'
        if field['type'] == 'file': prop['format'] = 'data-url'
        if field['type'] == 'select': prop['widget'] = 'select'
        if field['type'] == 'tel': prop['format'] = 'tel'
        
        # Meta and Lookups
        if 'description' in field: prop['description'] = field['description']
        if 'lookup_service' in field: prop['lookup_service'] = field['lookup_service']
        if 'lookup_action' in field: prop['lookup_action'] = field['lookup_action']
        if field.get('read_only'): prop['readOnly'] = True
        
        schema['properties'][name] = prop
        if field.get('required'):
            schema['required'].append(name)
            
    return schema

def run_master_seed():
    print("=" * 80)
    print("🚀 MASTER CATALOGUE SYNCHRONIZER & SEEDER v8 (380+ Services)")
    print("=" * 80)

    # 1. CLEAN SLATE
    print("\n🧹 Cleaning existing data...")
    # We keep Roles and Users
    AuditLog.objects.all().delete()
    ServiceRequest.objects.all().delete()
    WorkflowStep.objects.all().delete()
    ServiceConfig.objects.all().delete()

    # 2. SEED FROM CSV
    print("\n📄 Seeding from all_wog_services.csv...")
    csv_path = "all_wog_services.csv"
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 5: continue
            
            code = row[0].strip()
            ministry_name = row[1].strip()
            category_name = row[2].strip()
            department_name = row[3].strip() # This is the specific MDA
            service_name = row[4].strip()
            type_val = row[5].strip()
            complexity = row[6].strip()
            channel = row[7].strip()
            
            # Use Department Name if available, fallback to Ministry
            final_mda_name = department_name if department_name else ministry_name
            
            mda_obj, _ = MDA.objects.get_or_create(
                name=final_mda_name,
                defaults={'code': code.split('-')[0] if '-' in code else code[:5]}
            )
            
            sector = "Public Service & Administration"
            if any(x in final_mda_name for x in ["Interior", "Immigration", "Police"]): sector = "Identity & Security"
            elif any(x in final_mda_name for x in ["Education", "Teachers", "University"]): sector = "Education & Training"
            elif any(x in final_mda_name for x in ["Health", "Hospital"]): sector = "Health & Wellness"
            
            domain_obj, _ = ServiceDomain.objects.get_or_create(name=sector)
            cat_obj, _ = ServiceCategory.objects.get_or_create(name=category_name, domain=domain_obj)
            
            ServiceConfig.objects.create(
                service_code=code,
                service_name=service_name,
                mda=mda_obj,
                category=cat_obj,
                service_type=type_val,
                description=f"Official {service_name} service by {final_mda_name}.",
                digitization_level=1 if "Physical" in channel else 3,
                delivery_channels=[channel],
                process_complexity=complexity,
                service_status='active',
                catalogue_visible=True,
                config={"rules": {"workflow": [], "schema": {"type": "object", "properties": {}, "required": []}}}
            )

    print(f"✓ Base CSV Seeded: {ServiceConfig.objects.count()} services.")

    # 2b. SEED MISSING SERVICES
    print("\n➕ Adding Missing Services from Python Definitions...")
    try:
        from add_missing_mdas_services import NEW_MDAS_WITH_SERVICES
        for entry in NEW_MDAS_WITH_SERVICES:
            mda_data = entry["mda"]
            mda, _ = MDA.objects.get_or_create(
                code=mda_data["code"],
                defaults={
                    "name": mda_data["name"],
                    "description": mda_data["description"],
                    "head_of_mda": mda_data.get("head", ""),
                    "contact_email": mda_data.get("email", ""),
                    "contact_phone": mda_data.get("phone", ""),
                    "website": mda_data.get("website", "")
                }
            )
            
            for svc_data in entry["services"]:
                domain, _ = ServiceDomain.objects.get_or_create(name=svc_data["domain"])
                category, _ = ServiceCategory.objects.get_or_create(name=svc_data["category"], domain=domain)
                
                if not ServiceConfig.objects.filter(service_code=svc_data["code"]).exists():
                    ServiceConfig.objects.create(
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
                        catalogue_visible=True,
                        config={"rules": {"workflow": [], "schema": {"type": "object", "properties": {}, "required": []}}}
                    )
        print(f"✓ Total Services after increment: {ServiceConfig.objects.count()}")
    except Exception as e:
        print(f"⚠️ Could not add missing services: {e}")

    # 3. APPLY ENHANCED WORKFLOWS
    print("\n⚙️  Applying enhanced workflows...")
    from enhance_priority_workflows import ENHANCED_WORKFLOWS
    rename_map = {
        "Passport Application": "Passport Application",
        "National ID Application": "National ID Application",
        "KRA PIN Registration": "PIN Registration",
        "Driving License Application": "Driving Licence Application",
        "TSC Number Application": "Teacher Registration",
        "NEMIS Registration": "Capitation Disbursement"
    }

    for svc_key, wf_data in ENHANCED_WORKFLOWS.items():
        search_name = rename_map.get(svc_key, svc_key)
        svc = ServiceConfig.objects.filter(service_name__icontains=search_name).first()
        if svc:
            WorkflowStep.objects.filter(service_config=svc).delete()
            for step in wf_data['as_is']:
                WorkflowStep.objects.create(service_config=svc, step_name=step['name'], role=step['role'], step_type=step['type'], bpmn_element_type=step['bpmn'], lifecycle_stage="as_is", sequence=step['seq'])
            for step in wf_data['to_be']:
                WorkflowStep.objects.create(service_config=svc, step_name=step['name'], role=step['role'], step_type=step['type'], bpmn_element_type=step['bpmn'], lifecycle_stage="to_be", sequence=step['seq'])
            print(f"  ✓ Workflow Enhanced: {svc.service_name}")

    # 4. APPLY FORM SCHEMAS
    print("\n📝 Mapping form fields (JSON Schema format)...")
    from add_form_schemas import FORM_SCHEMAS
    for mda_alias, schema_data in FORM_SCHEMAS.items():
        # Smart matching for MDAs
        mda_objs = MDA.objects.filter(name__icontains=mda_alias) | \
                   MDA.objects.filter(code=mda_alias) | \
                   MDA.objects.filter(name__icontains=mda_alias.replace("State Department for ", ""))
        
        # Special case for CRS (Civil Registration Services)
        if mda_alias == "CRS":
            mda_objs = mda_objs | MDA.objects.filter(name__icontains="Civil Registration")
        if mda_alias == "NEMIS":
            mda_objs = mda_objs | MDA.objects.filter(code="MOE") | MDA.objects.filter(name__icontains="Basic Education")
            
        for mda in mda_objs.distinct():
            for svc in ServiceConfig.objects.filter(mda=mda):
                json_schema = convert_fields_to_schema(schema_data['fields'])
                if not svc.config: svc.config = {}
                if 'rules' not in svc.config: svc.config['rules'] = {}
                svc.config['rules']['schema'] = json_schema
                svc.form_schema = schema_data
                svc.save()
                print(f"  ✓ Schema Linked: {svc.service_name} ({mda.name})")

    # 5. GENERIC GENERATOR
    print("\n🔮 Generating generic schemas for the remaining...")
    def generate_json_schema(svc):
        name = svc.service_name.lower()
        props = {
            "full_name": {"type": "string", "title": "Full Name", "description": "As per National ID"},
            "id_number": {"type": "string", "title": "ID Number", "lookup_service": "IPRS"},
            "phone": {"type": "string", "title": "Phone Number", "format": "tel"},
            "attachment": {"type": "string", "title": "Supporting Document", "format": "data-url"}
        }
        required = ["full_name", "id_number", "phone", "attachment"]
        if "business" in name or "company" in name:
            props["kra_pin"] = {"type": "string", "title": "Business KRA PIN", "lookup_service": "KRA"}
            required.append("kra_pin")
        return {"type": "object", "properties": props, "required": required}

    for svc in ServiceConfig.objects.all():
        schema_props = svc.config.get('rules', {}).get('schema', {}).get('properties', {})
        if not schema_props:
            if not svc.config: svc.config = {}
            if 'rules' not in svc.config: svc.config['rules'] = {}
            svc.config['rules']['schema'] = generate_json_schema(svc)
            svc.save()

    # 6. BASIC WORKFLOW FALLBACK
    for svc in ServiceConfig.objects.all():
        if not svc.workflow_steps.exists():
            for i, name in enumerate(["Submission", "Review", "Approval"]):
                WorkflowStep.objects.create(service_config=svc, step_name=name, lifecycle_stage="as_is", sequence=i+1, role="officer")
                WorkflowStep.objects.create(service_config=svc, step_name=f"Digital {name}", lifecycle_stage="to_be", sequence=i+1, role="citizen" if i==0 else "system")

    print("\n" + "=" * 80)
    print("🎬 MASTER SEED COMPLETE")
    print(f"Total Services: {ServiceConfig.objects.count()}")
    print("=" * 80)

if __name__ == "__main__":
    run_master_seed()
