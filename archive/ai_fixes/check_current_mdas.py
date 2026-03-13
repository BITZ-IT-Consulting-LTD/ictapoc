import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig

print("=== CURRENT MDAs IN DATABASE ===")
mdas = MDA.objects.all().order_by('name')
for mda in mdas:
    service_count = ServiceConfig.objects.filter(mda=mda).count()
    print(f"{mda.id:3d}. {mda.name} ({mda.code or 'NO CODE'}) - {service_count} services")

print(f"\nTotal MDAs: {mdas.count()}")
print(f"Total Services: {ServiceConfig.objects.count()}")
