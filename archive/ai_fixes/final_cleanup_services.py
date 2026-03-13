import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig, MDA, WorkflowStep, ServiceRequest, AuditLog

def final_cleanup():
    print("--- Finalizing service consolidation ---")
    
    # 1. Consolidate Birth Registration
    crs = MDA.objects.filter(code='CRS').first()
    birth_showcase = ServiceConfig.objects.filter(service_code='BIRTH_REG').first()
    
    if crs and birth_showcase:
        print(f"Moving '{birth_showcase.service_name}' to MDA '{crs.name}'")
        birth_showcase.mda = crs
        birth_showcase.save()
        
        # Delete the legacy ones in CRS that might conflict
        legacy = ServiceConfig.objects.filter(mda=crs).exclude(service_code='BIRTH_REG').filter(service_name__icontains='Birth Registration')
        for s in legacy:
            print(f"  Removing legacy birth service: {s.service_name} ({s.service_code})")
            ServiceRequest.objects.filter(service_config=s).delete()
            WorkflowStep.objects.filter(service_config=s).delete()
            AuditLog.objects.filter(service_request__service_config=s).delete()
            s.delete()

    # 2. Check for other duplicates that might have been missed
    # (Especially those that differ by minor name variations)
    
    MAPPINGS = [
        ('Passport Application', 'DIS', 'PASSPORT_APP'),
        ('National ID', 'NRB', 'NATIONAL_ID'),
        ('KRA PIN', 'KRA', 'KRA_PIN_REG'),
        ('Business Incorporation', 'ROC', 'BIZ_INCORPORATION')
    ]
    
    for name_part, mda_code, protected_code in MAPPINGS:
        mda = MDA.objects.filter(code=mda_code).first()
        if not mda: continue
        
        svcs = ServiceConfig.objects.filter(mda=mda, service_name__icontains=name_part)
        if svcs.count() > 1:
            protected = svcs.filter(service_code=protected_code).first()
            if protected:
                to_delete = svcs.exclude(id=protected.id)
                for s in to_delete:
                    print(f"Removing duplicate for {name_part}: {s.service_name} ({s.service_code})")
                    ServiceRequest.objects.filter(service_config=s).delete()
                    WorkflowStep.objects.filter(service_config=s).delete()
                    AuditLog.objects.filter(service_request__service_config=s).delete()
                    s.delete()

if __name__ == "__main__":
    final_cleanup()
