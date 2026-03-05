import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig

print("=== SEEDING GLOBAL SCHEMA FOR ALL PRIORITY SERVICES ===")

with open("/app/priority_workflows.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract all process names explicitly
process_names = [item["process_name"] for item in data]

print(f"Scanning for {len(process_names)} processes...")

updated = 0

# Grab EVERY service in the DB to check against our process list
for service in ServiceConfig.objects.all():
    match = False
    for pn in process_names:
        if pn.lower() in service.service_name.lower():
             match = True
             break
             
    if match:
        properties = {
            "applicant_id": {"type": "string", "title": "National ID / Passport Number", "description": "Applicant's identification document"},
            "full_name": {"type": "string", "title": "Full Name", "description": "Applicant's official registered name"},
            "contact_number": {"type": "string", "title": "Contact Phone Number"},
            "email_address": {"type": "string", "title": "Email Address"},
        }
        
        svc_name_lower = service.service_name.lower()
        if "passport" in svc_name_lower:
             properties["birth_certificate"] = {"type": "string", "title": "Birth Certificate Entry Number"}
             properties["passport_type"] = {"type": "string", "title": "Passport Pages", "enum": ["32 Pages", "50 Pages", "Diplomatic"]}
        elif "enrollment" in svc_name_lower or "student" in svc_name_lower:
             properties["upi"] = {"type": "string", "title": "Student UPI / BEN"}
             properties["school_level"] = {"type": "string", "title": "School Level", "enum": ["Primary", "JSS", "Senior"]}
        elif "correspondence" in svc_name_lower or "memo" in svc_name_lower or "advisory" in svc_name_lower:
             properties["subject"] = {"type": "string", "title": "Subject"}
             properties["memo_body"] = {"type": "string", "title": "Correspondence Content", "widget": "textarea"}
        else:
             properties["request_details"] = {"type": "string", "title": "Request / Application Details", "widget": "textarea"}
            
        schema = {
            "type": "object",
            "properties": properties,
            "required": ["applicant_id", "full_name"]
        }
        
        if not service.config:
            service.config = {}
        
        rules = service.config.get('rules', {})
        rules['schema'] = schema
        service.config['rules'] = rules
        
        service.form_schema = schema
        service.save()
        updated += 1
        print(f" ✓ Integrated Schema mapping for: {service.service_name}")

print(f"\nSuccessfully attached Dynamic form schemas to {updated} Priority services!")
