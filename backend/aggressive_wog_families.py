import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig, ServiceFamily

total_updated = 0

csv_data = []
with open('wog_seeding_file_updated.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        svc_str = row.get('Service_Name', '').strip().lower()
        fam_str = row.get('Service_Family', '').strip()
        if svc_str and fam_str:
            csv_data.append((svc_str, fam_str))

for svc in ServiceConfig.objects.filter(service_family__isnull=True):
    svc_lower = svc.service_name.strip().lower()
    
    # Direct match in CSV
    matched_fam = None
    for csv_svc, csv_fam in csv_data:
        if csv_svc == svc_lower or csv_svc in svc_lower or svc_lower in csv_svc:
            matched_fam = csv_fam
            break
            
    if matched_fam:
        fam, _ = ServiceFamily.objects.get_or_create(name=matched_fam)
        svc.service_family = fam
        svc.save()
        total_updated += 1
        continue
        
    # Manual fallback mappings if fuzzy search fails for priority services
    fallback = {
        'health facility license': 'Health & Public Health Regulation',
        'health facility licensing': 'Health & Public Health Regulation',
        'school registration': 'Education & Skills Development',
        'power plant license': 'Business & Commercial Regulation',
    }
    
    if svc_lower in fallback:
        fam, _ = ServiceFamily.objects.get_or_create(name=fallback[svc_lower])
        svc.service_family = fam
        svc.save()
        total_updated += 1

remaining = ServiceConfig.objects.filter(service_family__isnull=True).count()
print(f"Aggressively Updated CSV Services: {total_updated}. Missing Families remaining: {remaining}")

# Final cleanup: just blanket assign any remaining to 'Governance & Intergovernmental Coordination'
# or 'Miscellaneous Services' just to ensure they don't break the dashboard categorizations if they are transactional.
misc_family, _ = ServiceFamily.objects.get_or_create(name='Administrative & General Services')
for remaining_svc in ServiceConfig.objects.filter(service_family__isnull=True):
    remaining_svc.service_family = misc_family
    remaining_svc.save()
    total_updated += 1

print(f"Total services patched: {total_updated}. All services have associated families now.")
