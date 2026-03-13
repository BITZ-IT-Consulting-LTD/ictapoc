import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig

print("=== SEEDING SCHEMA FOR ALL 26 PROCESSED SERVICES ===")

with open("/app/priority_workflows.json", "r", encoding="utf-8") as f:
    data = json.load(f)

updated = 0

for item in data:
    process_name = item["process_name"]
    # Broadly search the entire list of 26 we just seeded
    services = ServiceConfig.objects.filter(service_name__icontains=process_name)
    
    for service in services:
        properties = {
            "applicant_id": {"type": "string", "title": "National ID / Passport Number", "description": "Applicant's identification document"},
            "full_name": {"type": "string", "title": "Full Name", "description": "Applicant's official registered name"},
            "contact_number": {"type": "string", "title": "Contact Phone Number"},
            "email_address": {"type": "string", "title": "Email Address"},
        }

        if "Passport" in process_name or "Passport" in service.service_name:
             properties["birth_certificate"] = {"type": "string", "title": "Birth Certificate Entry Number"}
             properties["passport_type"] = {"type": "string", "title": "Passport Pages", "enum": ["32 Pages", "50 Pages", "Diplomatic"]}
        elif "Enrollment" in process_name or "Student" in process_name or "Student" in service.service_name:
             properties["upi"] = {"type": "string", "title": "Student UPI / BEN"}
             properties["school_level"] = {"type": "string", "title": "School Level", "enum": ["Primary", "JSS", "Senior"]}
        elif "Correspondence" in process_name or "Correspondence" in service.service_name:
             properties["subject"] = {"type": "string", "title": "Subject"}
             properties["memo_body"] = {"type": "string", "title": "Correspondence Content", "widget": "textarea"}
        else:
             properties["request_details"] = {"type": "string", "title": "Request / Application Details", "widget": "textarea"}
            
        schema = {
            "type": "object",
            "properties": properties,
            "required": ["applicant_id", "full_name"]
        }
        
        # Add basic config metadata mimicking a digital form payload
        if not service.config:
            service.config = {}
        
        rules = service.config.get('rules', {})
        rules['schema'] = schema
        service.config['rules'] = rules
        
        # Keep schema at root level as well for standard lookup
        service.form_schema = schema
        
        service.save()
        updated += 1
        print(f" ✓ Added Schema to: {service.service_name}")

print(f"\nSuccessfully seeded dynamic JSON schema for {updated} services!")
