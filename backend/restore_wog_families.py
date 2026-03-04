import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig, ServiceFamily

total_updated = 0

with open('wog_seeding_file_updated.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        svc_name = row.get('Service_Name', '').strip()
        fam_name = row.get('Service_Family', '').strip()
        
        if svc_name and fam_name:
            svc = ServiceConfig.objects.filter(service_name=svc_name).first()
            if svc and not svc.service_family:
                fam, _ = ServiceFamily.objects.get_or_create(name=fam_name)
                svc.service_family = fam
                svc.save()
                total_updated += 1
                
remaining = ServiceConfig.objects.filter(service_family__isnull=True).count()
print(f"Updated CSV Services: {total_updated}. Missing Families remaining: {remaining}")
