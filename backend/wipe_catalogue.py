import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig, WorkflowStep, ServiceCategory, ServiceDomain, MDA

def wipe_data():
    print("--- WIPING ALL CATALOGUE DATA ---")
    
    print("Deleting Workflow Steps...")
    WorkflowStep.objects.all().delete()
    
    print("Deleting Service Configs...")
    ServiceConfig.objects.all().delete()
    
    print("Deleting Service Categories...")
    ServiceCategory.objects.all().delete()
    
    print("Deleting Service Domains...")
    ServiceDomain.objects.all().delete()
    
    # We might want to keep MDAs if they are used elsewhere (like roles), 
    # but for a clean catalogue seed, deleting them ensures no orphans.
    # However, MDAs are often linked to Users. Let's be careful.
    # We'll only delete MDAs that don't have users if possible, or just keep them.
    # For now, let's just delete them and see if it breaks anything. 
    # Actually, let's just clear the catalogue-specific ones.
    print("Deleting MDAs (Catalogue entries)...")
    MDA.objects.all().delete()

    print("--- WIPE COMPLETE: CLEAN SLATE CREATED ---")

if __name__ == '__main__':
    wipe_data()
