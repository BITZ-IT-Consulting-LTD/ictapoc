import os
import django
import sys

# Setup Django environment
sys.path.append('/Users/mac/ictapoc/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import RegistryAdapter
from service_api.registries import (
    IPRS, NRB, CRS, Immigration, BRS, KRA, NGOBoard, Ardhisasa, 
    CollateralRegistry, NTSA, KCAA, NEMIS, ProfessionalBodies, 
    SocialProtection, SHA, NSSF, Judiciary, Gazette, IEBC
)

def seed_registry_adapters():
    """
    Seeds the RegistryAdapter table with data extracted from the legacy hardcoded classes.
    """
    registries_to_seed = [
        ('IPRS', 'Integrated Population Registration System', IPRS, 'CITIZENS'),
        ('NRB', 'National Registration Bureau', NRB, 'CARDS'),
        ('CRS', 'Civil Registration Services', CRS, 'RECORDS'),
        ('IMMIGRATION', 'Department of Immigration Services', Immigration, 'DOCUMENTS'),
        ('BRS', 'Business Registration Service', BRS, 'ENTITIES'),
        ('KRA', 'Kenya Revenue Authority', KRA, 'PINS'),
        ('NGO_BOARD', 'NGO Coordination Board', NGOBoard, 'ENTITIES'),
        ('ARDHISASA', 'National Land Information Management System', Ardhisasa, 'TITLES'),
        ('COLLATERAL', 'Movable Assets Registry', CollateralRegistry, 'ASSETS'),
        ('NTSA', 'National Transport and Safety Authority', NTSA, 'RECORDS'),
        ('KCAA', 'Kenya Civil Aviation Authority', KCAA, 'AIRCRAFT'),
        ('NEMIS', 'National Education Management Information System', NEMIS, 'LEARNERS'),
        ('PROFESSIONAL_BODIES', 'Professional Bodies (EBK, LSK, etc.)', ProfessionalBodies, 'MEMBERS'),
        ('SOCIAL_PROTECTION', 'Social Protection Single Registry', SocialProtection, 'BENEFICIARIES'),
        ('SHA', 'Social Health Authority (NHIF)', SHA, 'MEMBERS'),
        ('NSSF', 'National Social Security Fund', NSSF, 'MEMBERS'),
        ('JUDICIARY', 'Judiciary Case Tracking System', Judiciary, 'CASES'),
        ('GAZETTE', 'Kenya Gazette', Gazette, 'NOTICES'),
        ('IEBC', 'Voter Register', IEBC, 'VOTERS'),
    ]

    print(f"Starting seeding of {len(registries_to_seed)} registry adapters...")

    for code, name, cls, attr in registries_to_seed:
        # Get the hardcoded data dictionary
        mock_dicts = getattr(cls, attr, {})
        
        adapter, created = RegistryAdapter.objects.update_or_create(
            code=code,
            defaults={
                'name': name,
                'is_mock': True,
                'mock_data': mock_dicts,
                'base_url': f"https://api.gov.ke/v1/registries/{code.lower()}", # Placeholder for future
                'data_mapping': {} # To be configured manually later
            }
        )
        
        status = "Created" if created else "Updated"
        print(f"[{status}] {code}: {len(mock_dicts)} records imported.")

    print("Seeding completed successfully!")

if __name__ == "__main__":
    seed_registry_adapters()
