import csv
from django.core.management.base import BaseCommand
from service_api.models import ServiceConfig, ServiceRequest, MDA, ServiceFamily

class Command(BaseCommand):
    help = 'Migrate existing ServiceRequests to new WoG ServiceConfigs and cleanup duplicates'

    def handle(self, *args, **options):
        # 1. Identify all services that were created today (assumed newWoG)
        # Actually better to use the new codes pattern (3 segments with dashes)
        new_services = ServiceConfig.objects.filter(service_code__regex=r'^[A-Z]{3}-[A-Z]{3,4}-\d{3}$')
        new_svc_map = {s.service_name: s for s in new_services}
        
        self.stdout.write(f"Found {len(new_svc_map)} potential new WoG services for mapping.")

        # 2. Map existing requests
        requests = ServiceRequest.objects.all()
        migrated_count = 0
        for req in requests:
            old_svc = req.service_config
            # Try to find a match in the new catalogue by name
            new_svc = new_svc_map.get(old_svc.service_name)
            
            if new_svc and new_svc.id != old_svc.id:
                req.service_config = new_svc
                req.save()
                migrated_count += 1
        
        self.stdout.write(self.style.SUCCESS(f"Migrated {migrated_count} applications to new WoG services."))

        # 3. Cleanup: Deactivate or Delete old services that have a new counterpart
        old_services = ServiceConfig.objects.exclude(id__in=[s.id for s in new_services])
        deactivated_count = 0
        for old_svc in old_services:
            if old_svc.service_name in new_svc_map:
                # Check if any requests still point to it (should be 0 if migration worked)
                if old_svc.servicerequest_set.count() == 0:
                    old_svc.service_status = 'deprecated'
                    old_svc.catalogue_visible = False
                    old_svc.save()
                    deactivated_count += 1

        self.stdout.write(self.style.SUCCESS(f"Deprecated {deactivated_count} redundant service configurations."))
        
        # 4. Cleanup MDAs: If an MDA has no services and is not in the new list, mark it?
        # Actually let's just leave MDAs for now to avoid breaking historical audit logs.
