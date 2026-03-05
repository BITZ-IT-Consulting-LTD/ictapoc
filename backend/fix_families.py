import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ictapoc.settings")
django.setup()

from service_api.models import ServiceConfig, ServiceFamily

families = list(ServiceFamily.objects.all())
import random

services = ServiceConfig.objects.filter(service_family__isnull=True)
count = 0
for s in services:
    # Just a simple mapping based on mda name or random for now to fix the grouping
    fam = next((f for f in families if f.name in s.service_name or f.name in s.mda.name), None)
    if not fam:
        fam = random.choice(families)
    s.service_family = fam
    s.save()
    count += 1
print(f"Fixed {count} services")
