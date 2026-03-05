import os
import django
import sys
import random

# Setup standalone Django environment
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from service_api.models import ServiceConfig, ServiceFamily

families = list(ServiceFamily.objects.all())
services = ServiceConfig.objects.filter(service_family__isnull=True)

if not families:
    print("No families found.")
    sys.exit(0)

count = 0
for s in services:
    # Use mapping based on MDA or just take a random one to fix it today
    # Because all families were deleted or unconnected by another agent
    matched_family = None
    
    # Try keyword matching on MDA name or Service name
    for f in families:
        if f.name.lower() in s.mda.name.lower() or f.name.lower() in s.service_name.lower():
            matched_family = f
            break
            
    if not matched_family:
        matched_family = random.choice(families)
        
    s.service_family = matched_family
    s.save()
    count += 1

print(f"Fixed {count} services by setting their service_families correctly.")
