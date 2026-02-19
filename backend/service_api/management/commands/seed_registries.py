from django.core.management.base import BaseCommand
from service_api.models import RegistryAdapter

class Command(BaseCommand):
    help = 'Seeds the RegistryAdapter table with GEA-compliant authoritative government registries'

    def handle(self, *args, **options):
        registries = [
            {
                "code": "IPRS",
                "name": "Integrated Population Registration System (Identity)",
                "base_url": "https://api.gov.ke/ke-sel/registries/iprs",
                "data_mapping": {
                    "full_name": "full_name",
                    "dob": "date_of_birth",
                    "gender": "sex",
                    "status": "record_status"
                }
            },
            {
                "code": "NIIMS",
                "name": "Maisha Namba / NIIMS (Digital ID)",
                "base_url": "https://api.gov.ke/ke-sel/registries/niims",
                "data_mapping": {
                    "maisha_namba": "person_id",
                    "id_number": "national_id"
                }
            },
            {
                "code": "BRS",
                "name": "Business Registration Service",
                "base_url": "https://api.gov.ke/ke-sel/registries/brs",
                "data_mapping": {
                    "name": "legal_name",
                    "status": "business_status",
                    "inc_date": "registration_date"
                }
            },
            {
                "code": "ARDHISASA",
                "name": "National Land Information Management System (Ardhisasa)",
                "base_url": "https://api.gov.ke/ke-sel/registries/nlims",
                "data_mapping": {
                    "parcel_no": "block_number",
                    "owner": "title_holder",
                    "status": "encumbrance_status"
                }
            },
            {
                "code": "NTSA",
                "name": "National Transport & Safety Authority",
                "base_url": "https://api.gov.ke/ke-sel/registries/ntsa",
                "data_mapping": {
                    "plate": "registration_number",
                    "owner": "registered_owner",
                    "expiry": "license_expiry"
                }
            },
            {
                "code": "KRA",
                "name": "Kenya Revenue Authority (iTax)",
                "base_url": "https://api.gov.ke/ke-sel/registries/kra",
                "data_mapping": {
                    "pin": "taxpayer_pin",
                    "status": "compliance_status"
                }
            },
            {
                "code": "NEMIS",
                "name": "National Education Management Information System",
                "base_url": "https://api.gov.ke/ke-sel/registries/nemis",
                "data_mapping": {
                    "upi": "learner_unique_identifier",
                    "school": "institution_name"
                }
            },
            {
                "code": "HRMIS",
                "name": "Human Resource Management Information System",
                "base_url": "https://api.gov.ke/ke-sel/registries/hrmis",
                "data_mapping": {
                    "staff_id": "personal_number",
                    "ministry": "department_name"
                }
            },
            {
                "code": "IFMIS",
                "name": "Integrated Financial Management Information System",
                "base_url": "https://api.gov.ke/ke-sel/registries/ifmis",
                "data_mapping": {
                    "supplier_id": "ifmis_code",
                    "status": "payment_status"
                }
            },
            {
                "code": "JUDICIARY",
                "name": "Judiciary Case Management System (CMS)",
                "base_url": "https://api.gov.ke/ke-sel/registries/judiciary",
                "data_mapping": {
                    "case_no": "case_reference",
                    "status": "litigation_status"
                }
            },
            {
                "code": "IMMIGRATION",
                "name": "Department of Immigration Services (eFNS)",
                "base_url": "https://api.gov.ke/ke-sel/registries/immigration",
                "data_mapping": {
                    "passport_no": "document_number",
                    "status": "permit_status"
                }
            },
            {
                "code": "CRS",
                "name": "Civil Registration Services (Births/Deaths)",
                "base_url": "https://api.gov.ke/ke-sel/registries/crs",
                "data_mapping": {
                    "ben": "entry_number",
                    "status": "vital_status"
                }
            },
            {
                "code": "SOCIAL_PROTECTION",
                "name": "Social Protection Single Registry (Inua Jamii)",
                "base_url": "https://api.gov.ke/ke-sel/registries/social",
                "data_mapping": {
                    "ben_id": "beneficiary_id",
                    "program": "scheme_name"
                }
            },
            {
                "code": "HEALTH",
                "name": "Social Health Authority (SHA/NHIF)",
                "base_url": "https://api.gov.ke/ke-sel/registries/health",
                "data_mapping": {
                    "member_id": "sha_id",
                    "status": "insurance_status"
                }
            }
        ]

        self.stdout.write(self.style.SUCCESS(f'Starting seeding of {len(registries)} authoritative registries...'))

        for reg_data in registries:
            adapter, created = RegistryAdapter.objects.update_or_create(
                code=reg_data["code"],
                defaults={
                    "name": reg_data["name"],
                    "base_url": reg_data["base_url"],
                    "data_mapping": reg_data["data_mapping"],
                    "is_mock": True, # Default to mock for POC
                    "auth_config": {
                        "pki_required": True,
                        "auth_pattern": "KeSEL/X-Road",
                        "security_server": "https://security-server.gov.ke/query"
                    }
                }
            )
            
            if created:
                self.stdout.write(f'  - Created: {adapter.code}')
            else:
                self.stdout.write(f'  - Updated: {adapter.code}')

        self.stdout.write(self.style.SUCCESS('Seeding complete!'))
