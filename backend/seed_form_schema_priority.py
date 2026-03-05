import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig

print("=== SEEDING DEFAULT INPUT SCHEMAS FOR PRIORITY MDAS ===")

with open("/app/priority_workflows.json", "r", encoding="utf-8") as f:
    data = json.load(f)

updated = 0

for item in data:
    process_name = item["process_name"]
    service = ServiceConfig.objects.filter(service_name__icontains=process_name).first()
    
    if service:
        schema = {
            "type": "object",
            "properties": {
                "applicant_id": {"type": "string", "title": "National ID / Passport Number", "description": "Applicant's identification document"},
                "full_name": {"type": "string", "title": "Full Name", "description": "Applicant's official registered name"},
                "contact_number": {"type": "string", "title": "Contact Phone Number"},
                "email_address": {"type": "string", "title": "Email Address", "format": "email"},
                "request_details": {"type": "string", "title": "Request / Application Details", "widget": "textarea"}
            },
            "required": ["applicant_id", "full_name", "request_details"]
        }
        
        # Add basic config metadata mimicking a digital form payload
        if not service.config:
            service.config = {}
        
        rules = service.config.get('rules', {})
        rules['schema'] = schema
        service.config['rules'] = rules
        
        # Keep schema at root level as well for backup
        service.form_schema = schema
        
        service.save()
        updated += 1
        print(f" ✓ Added Dynamic Form Schema to: {service.service_name}")

print(f"\nSuccessfully seeded schema for {updated} services!")
