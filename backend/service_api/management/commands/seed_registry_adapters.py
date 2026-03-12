from django.core.management.base import BaseCommand
from service_api.models import RegistryAdapter, RegistryEndpoint

class Command(BaseCommand):
    help = 'Seeds GEA-compliant registry adapters'

    def handle(self, *args, **options):
        from seed_registry_adapters import seed_registry_adapters
        seed_registry_adapters()
        self.stdout.write(self.style.SUCCESS("✅ Registry adapters seeded successfully."))
