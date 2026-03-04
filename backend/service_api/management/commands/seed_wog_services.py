import csv
import os
from django.core.management.base import BaseCommand
from service_api.models import ServiceConfig, ServiceFamily, MDA, ServiceCategory, ServiceDomain

class Command(BaseCommand):
    help = 'Seed WoG Services from normalized CSV'

    def handle(self, *args, **options):
        csv_path = '/app/wog_seeding_file_updated.csv'  # Works in Docker (mapped to backend/)
        official_codes = set()
        
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'CSV file not found at {csv_path}'))
            return

        self.stdout.write(f'Loading data from {csv_path}...')
        
        count = 0
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 1. Get/Create MDA
                mda_name = row['Department_Agency']
                ministry = row['Ministry']
                mda = MDA.objects.filter(name=mda_name).first()
                if not mda:
                    mda = MDA.objects.create(
                        name=mda_name,
                        description=f'Agency under {ministry}'
                    )
                
                if not mda.code:
                    base_code = mda_name.split(' ')[0][:5].upper()
                    mda.code = f"MDA-{base_code}-{mda.id}"
                    mda.save()

                # 2. Get/Create Service Family
                family_name = row['Service_Family']
                family = ServiceFamily.objects.filter(name=family_name).first()
                if not family:
                    family = ServiceFamily.objects.create(
                        name=family_name,
                        description=f'Family of services grouped under {family_name}'
                    )

                # 3. Get/Create Service Domain & Category
                domain = ServiceDomain.objects.filter(name=family_name).first()
                if not domain:
                    domain = ServiceDomain.objects.create(name=family_name)
                
                category_name = row['Service_Category']
                category = ServiceCategory.objects.filter(name=category_name, domain=domain).first()
                if not category:
                    category = ServiceCategory.objects.create(
                        name=category_name,
                        domain=domain
                    )

                # 4. Map Priority
                priority_map = {'Tier 1': 'high', 'Tier 2': 'normal', 'Tier 3': 'low'}
                priority = priority_map.get(row['Priority_Tier'], 'normal')

                # 5. Shared Caps & Systems
                caps_raw = row.get('Shared_Capabilities_Required', 'None')
                caps = [] if caps_raw == 'None' else [c.strip() for c in caps_raw.split(',')]
                
                platform = row.get('Digital_Platform', 'Manual')
                systems = [platform] if platform and platform != 'N/A' else []

                # 6. Lifecycle / Life Event
                lifecycle = row.get('Lifecycle_Tag', 'General Civil')
                
                # 7. Create/Update ServiceConfig
                ServiceConfig.objects.update_or_create(
                    service_code=row['Service_Code'],
                    defaults={
                        'service_name': row['Service_Name'],
                        'mda': mda,
                        'service_family': family,
                        'category': category,
                        'service_type': row['Service_Nature'],
                        'delivery_channels': [row['Delivery_Mode']],
                        'legal_basis_summary': row['Legal_Basis'],
                        'shared_services': caps,
                        'associated_systems': systems,
                        'life_event_group': lifecycle,
                        'priority': priority,
                        'is_public_facing': True,
                        'catalogue_visible': True,
                        'service_status': 'active'
                    }
                )
                count += 1
                official_codes.add(row['Service_Code'])

        # 8. Deactivate legacy services not in the new catalogue
        deactivated = ServiceConfig.objects.exclude(service_code__in=official_codes).update(
            service_status='deprecated',
            catalogue_visible=False
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully re-seeded {count} WoG services with enriched metadata'))
        self.stdout.write(self.style.WARNING(f'Deprecated {deactivated} legacy services not in the WoG catalogue.'))
