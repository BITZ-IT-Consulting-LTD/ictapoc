import os, django, re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig

def generate_schema(service_name):
    sn = service_name.lower()
    schema = {
        "type": "object",
        "title": service_name,
        "properties": {
            "applicant_name": {"type": "string", "title": "Full Name"},
            "national_id": {"type": "string", "title": "National ID / Passport Number"}
        },
        "required": ["applicant_name", "national_id"]
    }
    
    # Customize based on keywords
    if "passport" in sn or "birth" in sn or "death" in sn:
        schema["properties"]["date_of_event"] = {"type": "string", "format": "date", "title": "Date of Birth/Event"}
        schema["properties"]["county_of_residence"] = {"type": "string", "title": "County"}
        schema["required"].append("date_of_event")
        
    elif "company" in sn or "business" in sn or "msme" in sn or "credit" in sn:
        schema["properties"]["business_name"] = {"type": "string", "title": "Registered Business Name"}
        schema["properties"]["kra_pin"] = {"type": "string", "title": "Company KRA PIN"}
        schema["required"].extend(["business_name", "kra_pin"])
        
    elif "land" in sn or "infrastructure" in sn or "environment" in sn or "eia" in sn:
        schema["properties"]["plot_number"] = {"type": "string", "title": "LR/Plot Number"}
        schema["properties"]["location"] = {"type": "string", "title": "Physical Location/Coordinates"}
        schema["properties"]["project_description"] = {"type": "string", "format": "textarea", "title": "Project Overview"}
        schema["required"].extend(["location", "project_description"])
        
    elif "health" in sn or "medical" in sn or "protection" in sn or "refugee" in sn:
        schema["properties"]["medical_history_id"] = {"type": "string", "title": "Health File Reference Number"}
        schema["properties"]["case_narrative"] = {"type": "string", "format": "textarea", "title": "Case Details / Narrative"}
        
    elif "education" in sn or "research" in sn:
        schema["properties"]["institution_name"] = {"type": "string", "title": "Affiliated Institution"}
        schema["properties"]["research_topic"] = {"type": "string", "title": "Research Topic / Qualification Subject"}
        schema["required"].append("research_topic")
        
    elif "agri" in sn or "farmer" in sn:
        schema["properties"]["farm_size"] = {"type": "number", "title": "Farm Size (Acres)"}
        schema["properties"]["crop_type"] = {"type": "string", "title": "Primary Crop / Livestock"}
        schema["required"].extend(["farm_size"])
        
    # Generic
    schema["properties"]["supporting_document"] = {"type": "string", "format": "data-url", "title": "Supporting Document Upload"}
    
    return schema

updated = 0
for s in ServiceConfig.objects.filter(service_code__startswith="PRI-"):
    form_schema = generate_schema(s.service_name)
    # Update config without wiping workflow
    if "rules" not in s.config:
        s.config["rules"] = {}
    s.config["rules"]["schema"] = form_schema
    s.save()
    updated += 1
    
print(f"Injected richly defined Form Schemas for {updated} priority services.")
