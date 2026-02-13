import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig

# Common field templates
COMMON_FIELDS = {
    "applicant_info": [
        {"name": "full_name", "label": "Full Name", "type": "text", "required": True, "validation": {"minLength": 3, "maxLength": 100}},
        {"name": "id_number", "label": "National ID Number", "type": "text", "required": True, "validation": {"pattern": "^[0-9]{8}$"}},
        {"name": "phone", "label": "Phone Number", "type": "tel", "required": True, "validation": {"pattern": "^\\+254[0-9]{9}$"}},
        {"name": "email", "label": "Email Address", "type": "email", "required": True},
        {"name": "postal_address", "label": "Postal Address", "type": "text", "required": False},
    ],
    "business_info": [
        {"name": "business_name", "label": "Business Name", "type": "text", "required": True},
        {"name": "business_registration", "label": "Business Registration Number", "type": "text", "required": True},
        {"name": "kra_pin", "label": "KRA PIN", "type": "text", "required": True, "validation": {"pattern": "^[A-Z][0-9]{9}[A-Z]$"}},
    ],
    "documents": [
        {"name": "id_copy", "label": "Copy of National ID", "type": "file", "required": True, "validation": {"accept": ".pdf,.jpg,.png", "maxSize": 2097152}},
        {"name": "supporting_documents", "label": "Supporting Documents", "type": "file", "required": False, "validation": {"accept": ".pdf,.jpg,.png", "maxSize": 5242880}},
    ],
}

def generate_form_schema(service):
    """Generate appropriate form schema based on service type and category"""
    
    service_name = service.service_name.lower()
    service_type = service.service_type or ""
    category_name = service.category.name.lower() if service.category else ""
    
    # Determine form fields based on service characteristics
    fields = []
    
    # Always start with applicant information for C2G and B2G services
    if service_type in ['C2G', 'G2C']:
        fields.extend(COMMON_FIELDS["applicant_info"])
    elif service_type in ['B2G', 'G2B']:
        fields.extend(COMMON_FIELDS["applicant_info"][:4])  # Name, ID, Phone, Email
        fields.extend(COMMON_FIELDS["business_info"])
    else:
        # For G2G and Internal, just basic contact info
        fields.extend(COMMON_FIELDS["applicant_info"][:4])
    
    # Add service-specific fields based on keywords
    
    # Registration/License services
    if any(word in service_name for word in ['register', 'registration', 'license', 'permit', 'certificate']):
        if 'business' in service_name or 'company' in service_name:
            fields.append({"name": "business_type", "label": "Business Type", "type": "select", "required": True,
                          "options": [{"value": "sole", "label": "Sole Proprietorship"}, 
                                    {"value": "partnership", "label": "Partnership"},
                                    {"value": "limited", "label": "Limited Company"}]})
        
        fields.append({"name": "application_type", "label": "Application Type", "type": "select", "required": True,
                      "options": [{"value": "new", "label": "New Application"}, 
                                {"value": "renewal", "label": "Renewal"}]})
    
    # Payment/Tax services
    if any(word in service_name for word in ['payment', 'tax', 'fee', 'levy', 'revenue']):
        fields.append({"name": "payment_period", "label": "Payment Period", "type": "select", "required": True,
                      "options": [{"value": "monthly", "label": "Monthly"}, 
                                {"value": "quarterly", "label": "Quarterly"},
                                {"value": "annual", "label": "Annual"}]})
        fields.append({"name": "amount", "label": "Amount (KES)", "type": "number", "required": True, "validation": {"min": 0}})
    
    # Application/Request services
    if any(word in service_name for word in ['application', 'apply', 'request']):
        fields.append({"name": "application_reason", "label": "Reason for Application", "type": "textarea", "required": True,
                      "validation": {"minLength": 20, "maxLength": 500}})
    
    # Clearance/Compliance services
    if any(word in service_name for word in ['clearance', 'compliance', 'verification', 'inspection']):
        fields.append({"name": "clearance_type", "label": "Clearance Type", "type": "text", "required": True})
        fields.append({"name": "purpose", "label": "Purpose", "type": "textarea", "required": True})
    
    # Education services
    if 'education' in category_name or any(word in service_name for word in ['school', 'student', 'education', 'scholarship']):
        fields.append({"name": "institution_name", "label": "Institution Name", "type": "text", "required": True})
        fields.append({"name": "level_of_study", "label": "Level of Study", "type": "select", "required": True,
                      "options": [{"value": "primary", "label": "Primary"}, 
                                {"value": "secondary", "label": "Secondary"},
                                {"value": "tertiary", "label": "Tertiary"}]})
    
    # Health services
    if 'health' in category_name or any(word in service_name for word in ['health', 'medical', 'hospital', 'clinic']):
        fields.append({"name": "facility_name", "label": "Health Facility Name", "type": "text", "required": False})
        fields.append({"name": "patient_id", "label": "Patient ID/NUPI", "type": "text", "required": False})
    
    # Land/Property services
    if any(word in service_name for word in ['land', 'property', 'title', 'plot', 'parcel']):
        fields.append({"name": "parcel_number", "label": "Parcel/Plot Number", "type": "text", "required": True})
        fields.append({"name": "location", "label": "Location/County", "type": "text", "required": True})
        fields.append({"name": "size", "label": "Size (Acres/Hectares)", "type": "number", "required": False})
    
    # Transport services
    if 'transport' in category_name or any(word in service_name for word in ['vehicle', 'driving', 'transport', 'logbook']):
        fields.append({"name": "vehicle_registration", "label": "Vehicle Registration Number", "type": "text", "required": False})
        fields.append({"name": "vehicle_type", "label": "Vehicle Type", "type": "select", "required": False,
                      "options": [{"value": "private", "label": "Private"}, 
                                {"value": "commercial", "label": "Commercial"},
                                {"value": "psv", "label": "Public Service Vehicle"}]})
    
    # Always add document upload fields
    fields.extend(COMMON_FIELDS["documents"])
    
    # Add additional notes field
    fields.append({"name": "additional_notes", "label": "Additional Notes/Comments", "type": "textarea", "required": False,
                  "validation": {"maxLength": 1000}})
    
    # Create the form schema
    form_schema = {
        "title": service.service_name,
        "description": service.description or f"Application form for {service.service_name}",
        "fields": fields
    }
    
    return form_schema

print("=" * 80)
print("GENERATING FORMS FOR ALL SERVICES")
print("=" * 80)

# Get all services without forms
services = ServiceConfig.objects.all()
total = services.count()
updated = 0
skipped = 0

for idx, service in enumerate(services, 1):
    # Skip if already has a form (unless it's empty)
    if service.form_schema and len(service.form_schema.get('fields', [])) > 0:
        skipped += 1
        continue
    
    try:
        # Generate form schema
        form_schema = generate_form_schema(service)
        
        # Save to database
        service.form_schema = form_schema
        service.save()
        
        updated += 1
        
        if updated % 50 == 0:
            print(f"Progress: {updated}/{total - skipped} services updated...")
        
    except Exception as e:
        print(f"\n⚠️  Error with {service.service_code}: {str(e)}")
        skipped += 1

print(f"\n{'=' * 80}")
print(f"SUMMARY:")
print(f"  Total Services: {total}")
print(f"  Forms Created: {updated}")
print(f"  Skipped (already had forms): {skipped}")
print(f"  Success Rate: {(updated/(total-skipped)*100):.1f}%" if (total-skipped) > 0 else "N/A")
print(f"{'=' * 80}")

# Show sample of created forms
print(f"\nSample of created forms:")
sample_services = ServiceConfig.objects.exclude(form_schema={})[:5]
for svc in sample_services:
    field_count = len(svc.form_schema.get('fields', []))
    print(f"  • {svc.service_code}: {svc.service_name} ({field_count} fields)")
