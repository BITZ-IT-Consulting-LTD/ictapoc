import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig, WorkflowStep, ServiceRequest, AuditLog

# Services we want to protect (the Showcase ones)
PROTECTED_CODES = [
    'PASSPORT_APP',
    'BIRTH_REG',
    'NATIONAL_ID',
    'KRA_PIN_REG',
    'BIZ_INCORPORATION',
    'SCHOLARSHIPS',
    'CAB_MEMO',
    'SECURE_CLEARANCE',
    'PROFILE_UPDATE'
]

def cleanup_duplicates():
    print("--- Cleaning up duplicate services ---")
    
    # Names to look for duplicates
    MAPPING = {
        'Passport Application': 'DIS',
        'Birth Registration': 'CRS',
        'National ID Application': 'NRB',
        'PIN Registration': 'KRA',
        'Business Incorporation': 'ROC',
        'Scholarships': 'MOE'
    }
    
    for name, mda_code in MAPPING.items():
        print(f"\nChecking duplicates for '{name}' in MDA '{mda_code}'")
        
        # Find all services for this MDA that contain the name
        svcs = ServiceConfig.objects.filter(mda__code=mda_code, service_name__icontains=name)
        
        if svcs.count() > 1:
            # We have duplicates. Keep the one in PROTECTED_CODES or the one with a form_schema.
            protected = svcs.filter(service_code__in=PROTECTED_CODES).first()
            
            if not protected:
                 # Fallback: pick the one with a form_schema
                 protected = svcs.exclude(form_schema=None).first()
            
            if protected:
                print(f"  Keeping: ID={protected.id}, Name='{protected.service_name}', Code='{protected.service_code}'")
                
                # Delete the others
                to_delete = svcs.exclude(id=protected.id)
                for s in to_delete:
                    print(f"  Deleting: ID={s.id}, Name='{s.service_name}', Code='{s.service_code}'")
                    # Cleanup related objects first due to PROTECT
                    ServiceRequest.objects.filter(service_config=s).delete()
                    WorkflowStep.objects.filter(service_config=s).delete()
                    s.delete()
            else:
                print("  No protected version found, skipping.")
        else:
            print("  No duplicates found.")

if __name__ == "__main__":
    cleanup_duplicates()
