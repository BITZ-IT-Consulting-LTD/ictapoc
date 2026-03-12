from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from service_api.models import MDA, ServiceConfig, WorkflowStep, ServiceRequest, Role, ServiceFamily
# Import the seed_data logic or just copy it. 
# Since it's huge, I'll just call the function from the existing script if possible, 
# but it's easier to just make it a command.

class Command(BaseCommand):
    help = 'Seeds initial departmental and service data'

    def handle(self, *args, **options):
        from seed_data import seed_data
        seed_data()
        self.stdout.write(self.style.SUCCESS("✅ Initial data seeded successfully."))
