import os
import re
from pathlib import Path

# This script is designed to run via `python manage.py shell`
# Usage: python manage.py shell < seed_priority_forms.py
from service_api.models import ServiceConfig

def create_property_from_field(field_name, field_type):
    """
    Infers the JSON Schema property type and format from the parsed field type string.
    """
    prop_def = {"title": field_name.strip()}
    ft_lower = field_type.lower()
    
    if any(t in ft_lower for t in ['image', 'document', 'file', 'attachment', 'upload', 'cert']):
        prop_def["type"] = "string"
        prop_def["format"] = "data-url"
    elif any(t in ft_lower for t in ['enum', 'select', 'choice', 'dropdown', 'type']):
        prop_def["type"] = "string"
        prop_def["enum"] = ["Option 1", "Option 2"]
    elif any(t in ft_lower for t in ['int', 'number', 'amount']):
        prop_def["type"] = "number"
    elif 'date' in ft_lower:
        prop_def["type"] = "string"
        prop_def["format"] = "date"
    else:
        prop_def["type"] = "string"

    fn_lower = field_name.lower()
    
    # KeSEL lookups
    if any(x in fn_lower for x in ['id', 'national id', 'maisha', 'id number', 'identification', 'parent id', 'deceased id']):
        prop_def["lookup_service"] = "IPRS"
    if any(x in fn_lower for x in ['birth cert', 'upi', 'birth certificate']):
        prop_def["lookup_service"] = "CRS"
        
    return prop_def

def parse_markdown_for_schema(md_content):
    """
    Parses a markdown string to extract data inputs from tables, returning properties and required lists.
    """
    lines = md_content.split('\n')
    properties = {}
    required = []
    
    in_table = False
    
    for line in lines:
        if '|' in line and '---' not in line:
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if not in_table:
                lower_parts = [p.lower() for p in parts]
                # Look for header row that mentions field/input/name
                if len(lower_parts) >= 2 and any(h in p for h in ['field', 'input', 'parameter', 'name', 'document'] for p in lower_parts):
                    in_table = True
            else:
                if not parts:
                    continue
                
                field_name = parts[0]
                if field_name.lower() in ['field name', 'input', 'document', 'name']:
                    continue
                    
                field_type = parts[1] if len(parts) > 1 else 'string'
                fn_lower = field_name.lower()
                
                # Exclude basic bio-data (KeSEL 'Once-Only' Principle)
                bio_terms = ['name', 'dob', 'date of birth', 'age', 'gender', 'sex', 'first name', 'last name', 'email', 'phone']
                if any(bio == fn_lower or fn_lower.startswith(bio + ' ') or fn_lower.endswith(' ' + bio) for bio in bio_terms):
                    # Exclude typical bio-data, but don't accidentally drop 'business name'
                    if 'business' not in fn_lower and 'company' not in fn_lower:
                        continue
                    
                prop_key = re.sub(r'[^a-z0-9_]', '_', fn_lower.replace(' ', '_'))
                prop_key = re.sub(r'_+', '_', prop_key).strip('_')
                if not prop_key:
                    continue
                    
                prop_def = create_property_from_field(field_name, field_type)
                
                properties[prop_key] = prop_def
                # Make KRA PIN and IDs required by default
                if 'kra' in fn_lower or 'id' in fn_lower or 'cert' in fn_lower:
                    required.append(prop_key)
                elif len(required) < 3: # default to making first few required
                    required.append(prop_key)
                
        elif in_table and not line.strip():
            break
            
    return properties, required

def main():
    print("Starting Form Schema Seeding for Priority & Critical Services...")
    
    # 1. Target Query
    services = ServiceConfig.objects.filter(priority__in=['high', 'critical'])
    count = services.count()
    print(f"Found {count} priority services to update.")
    
    # 2. Source of Truth
    # Docs are located in /Users/mac/ictapoc/mdas/docs_final/
    docs_dir = Path('/Users/mac/ictapoc/mdas/docs_final/')
    md_files = list(docs_dir.rglob('*.md'))
    
    updated_count = 0
    
    for service in services:
        best_match = None
        best_score = 0
        
        service_name_lower = service.service_name.lower()
        mda_name_lower = service.mda.name.lower() if service.mda else ""
        
        # Heuristically match the service to the right markdown documentation file
        for md_file in md_files:
            if md_file.name in ['README.md', 'Cradle_to_Death_MDAs.md', 'Priority_MDAs_Justification_Matrix.md']:
                continue
                
            score = 0
            file_name_lower = md_file.name.lower()
            
            service_words = [w for w in re.findall(r'\w+', service_name_lower) if len(w) > 3]
            mda_words = [w for w in re.findall(r'\w+', mda_name_lower) if len(w) > 3]
            
            for word in service_words:
                if word in file_name_lower:
                    score += 3
            for word in mda_words:
                if word in file_name_lower:
                    score += 1
                    
            if score > best_score:
                best_score = score
                best_match = md_file
                
        properties = {}
        required = []
        
        # 3. Form Schema Structure Generation
        if best_match and best_score > 0:
            try:
                content = best_match.read_text(encoding='utf-8')
                properties, required = parse_markdown_for_schema(content)
            except Exception as e:
                pass
            
        # 4. Fallbacks implementing the KeSEL Once-Only Principle if strict MD parsing yields empty
        if not properties:
            if 'passport' in service_name_lower:
                properties = {
                    "national_id": {"type": "string", "title": "National ID / Maisha Namba", "lookup_service": "IPRS"},
                    "passport_type": {"type": "string", "title": "Passport Type", "enum": ["32 Pages", "50 Pages", "66 Pages"]},
                    "current_photo": {"type": "string", "title": "Current Photo", "format": "data-url"},
                    "recommender_id": {"type": "string", "title": "Recommender ID", "lookup_service": "IPRS"}
                }
                required = ["national_id", "passport_type", "current_photo"]
            elif 'birth' in service_name_lower:
                properties = {
                    "parent_national_id": {"type": "string", "title": "Parent National ID", "lookup_service": "IPRS"},
                    "hospital_notification": {"type": "string", "title": "Hospital Notification", "format": "data-url"}
                }
                required = ["parent_national_id", "hospital_notification"]
            elif 'death' in service_name_lower:
                properties = {
                    "deceased_national_id": {"type": "string", "title": "Deceased National ID", "lookup_service": "IPRS"},
                    "medical_certificate": {"type": "string", "title": "Medical Certificate", "format": "data-url"},
                    "informant_id": {"type": "string", "title": "Informant ID", "lookup_service": "IPRS"}
                }
                required = ["medical_certificate", "informant_id"]
            elif 'driving' in service_name_lower or 'license' in service_name_lower:
                properties = {
                    "national_id": {"type": "string", "title": "National ID", "lookup_service": "IPRS"},
                    "medical_fitness_cert": {"type": "string", "title": "Medical Fitness Certificate", "format": "data-url"},
                    "kra_pin": {"type": "string", "title": "KRA PIN"}
                }
                required = ["national_id"]
            elif 'marriage' in service_name_lower:
                properties = {
                    "groom_id": {"type": "string", "title": "Groom National ID", "lookup_service": "IPRS"},
                    "bride_id": {"type": "string", "title": "Bride National ID", "lookup_service": "IPRS"},
                    "marriage_type": {"type": "string", "title": "Marriage Type", "enum": ["Civil", "Christian", "Customary", "Hindu", "Islamic"]}
                }
                required = ["groom_id", "bride_id", "marriage_type"]
            elif 'business' in service_name_lower or 'company' in service_name_lower:
                properties = {
                    "applicant_id": {"type": "string", "title": "Applicant National ID", "lookup_service": "IPRS"},
                    "kra_pin": {"type": "string", "title": "KRA PIN"},
                    "proposed_name": {"type": "string", "title": "Proposed Business Name"}
                }
                required = ["applicant_id", "kra_pin", "proposed_name"]
            elif 'kra' in service_name_lower or 'tax' in service_name_lower:
                properties = {
                    "national_id": {"type": "string", "title": "National ID", "lookup_service": "IPRS"},
                    "kra_pin": {"type": "string", "title": "KRA PIN"}
                }
                required = ["national_id", "kra_pin"]
            elif 'education' in service_name_lower or 'admission' in service_name_lower:
                properties = {
                    "student_id": {"type": "string", "title": "Student National ID / UPI", "lookup_service": "CRS"},
                    "kcse_index": {"type": "string", "title": "KCSE Index Number"}
                }
                required = ["student_id", "kcse_index"]
            elif 'health' in service_name_lower or 'hospital' in service_name_lower or 'patient' in service_name_lower:
                properties = {
                    "patient_id": {"type": "string", "title": "Patient National ID", "lookup_service": "IPRS"},
                    "referral_document": {"type": "string", "title": "Referral Document", "format": "data-url"}
                }
                required = ["patient_id"]
            else:
                properties = {
                    "applicant_id": {"type": "string", "title": "Applicant National ID", "lookup_service": "IPRS"},
                    "supporting_document": {"type": "string", "title": "Supporting Document", "format": "data-url"}
                }
                required = ["applicant_id"]

        # Build final JSON schema
        schema = {
            "title": f"{service.service_name} Application Form",
            "type": "object",
            "properties": properties,
            "required": list(set(required))
        }
        
        # Update Service Config
        service.form_schema = schema
        service.save()
        updated_count += 1
        
        match_info = best_match.name if (best_match and best_score > 0) else "Fallback/Heuristic"
        print(f"[{updated_count}/{count}] Seeded form_schema for: {service.service_name} (Source: {match_info})")

    print(f"\nSuccessfully generated and seeded {updated_count} priority forms based on process documentation.")

if __name__ == '__main__':
    main()
