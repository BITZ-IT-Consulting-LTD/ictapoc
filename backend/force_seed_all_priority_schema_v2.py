import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig

print("=== SEEDING GLOBAL SCHEMA FOR EXACTLY 26 PROCESSES ===")

with open("/app/priority_workflows.json", "r", encoding="utf-8") as f:
    data = json.load(f)

updated = 0

for item in data:
    process_name = item["process_name"]
    # Look for the exact service we seeded earlier based on ProcessName
    service = ServiceConfig.objects.filter(service_name__iexact=process_name).first()
    if not service:
         service = ServiceConfig.objects.filter(service_name__icontains=process_name).first()
         
    if not service:
         # Some strings were mapped shorter during extraction. Let's do a word overlap logic
         words = process_name.split()
         if len(words) > 2:
             q = words[0] + " " + words[1]
             service = ServiceConfig.objects.filter(service_name__icontains=q).first()

    if service:
        properties = {
            "applicant_id": {"type": "string", "title": "National ID / Passport Number", "description": "Applicant's identification document"},
            "full_name": {"type": "string", "title": "Full Name", "description": "Applicant's official registered name"},
            "contact_number": {"type": "string", "title": "Contact Phone Number"},
            "email_address": {"type": "string", "title": "Email Address"},
        }
        
        svc_str = service.service_name.lower()
        if "passport" in svc_str:
             properties["birth_certificate"] = {"type": "string", "title": "Birth Certificate Entry Number"}
             properties["passport_type"] = {"type": "string", "title": "Passport Pages", "enum": ["32 Pages", "50 Pages", "Diplomatic"]}
        elif "enrollment" in svc_str or "student" in svc_str:
             properties["upi"] = {"type": "string", "title": "Student UPI / BEN"}
             properties["school_level"] = {"type": "string", "title": "School Level", "enum": ["Primary", "JSS", "Senior"]}
        elif "correspondence" in svc_str or "memo" in svc_str or "advisory" in svc_str:
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
        print(f" ✓ Mapped JSON Schema for: {service.service_name}")
    else:
        print(f" ✗ Could not find Service: {process_name}")

print(f"\nSuccessfully attached Dynamic form schemas to {updated} exact Priority services!")
