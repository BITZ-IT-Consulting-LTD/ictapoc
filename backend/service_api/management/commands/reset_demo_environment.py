from django.core.management.base import BaseCommand
from django.db import connection, transaction
from service_api.models import ServiceRequest, AuditLog, WorkflowStepExecution, PaymentTransaction, RevenueSplit

class Command(BaseCommand):
    help = 'Wipes application data but preserves configuration and users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force reset without confirmation',
        )

    def handle(self, *args, **options):
        if not options['force']:
            self.stdout.write("CAUTION: This will delete ALL service requests, audit logs, and transactions.")
            confirm = input("Are you sure? (y/N): ")
            if confirm.lower() != 'y':
                self.stdout.write("Reset cancelled.")
                return

        with transaction.atomic():
            self.stdout.write("🗑 Wiping dynamic data...")
            RevenueSplit.objects.all().delete()
            PaymentTransaction.objects.all().delete()
            WorkflowStepExecution.objects.all().delete()
            AuditLog.objects.all().delete()
            ServiceRequest.objects.all().delete()
            
            self.stdout.write(self.style.SUCCESS("✅ Environment reset complete. Configuration and accounts preserved."))
