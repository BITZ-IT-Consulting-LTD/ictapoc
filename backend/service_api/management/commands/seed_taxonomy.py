from django.core.management.base import BaseCommand
from service_api.models import ServiceDomain, ServiceCategory, ServiceFamily, ServiceConfig, MDA
import json

class Command(BaseCommand):
    help = "Seeds the new National Cluster and Service Family Taxonomy"

    def handle(self, *args, **options):
        # 1. New Taxonomy Structure
        taxonomy = {
            "Economic & Regulatory": [
                "Business Registration & Trade",
                "Regulatory Licensing & Compliance",
                "Agriculture, Land & Natural Resources",
                "Revenue & Financial Administration"
            ],
            "Social & Citizen Services": [
                "Education & Qualifications",
                "Health & Social Protection",
                "Citizen Identity & Civil Status",
                "Grants & Beneficiary Management"
            ],
            "Policy & Governance": [
                "Executive & Policy Coordination",
                "Public Service & HR Management",
                "Public Information & Heritage"
            ],
            "Security & Infrastructure": [
                "Justice & Case Management",
                "Public Safety & Emergency Services",
                "Infrastructure & Transport Services",
                "Procurement & Asset Management"
            ]
        }

        self.stdout.write(self.style.SUCCESS("Starting taxonomy seeding..."))

        for domain_name, families in taxonomy.items():
            # Create/Get Cluster (Domain)
            domain, d_created = ServiceDomain.objects.get_or_create(name=domain_name)
            if d_created:
                self.stdout.write(f"Created Cluster: {domain_name}")
            else:
                self.stdout.write(f"Found Cluster: {domain_name}")

            for family_name in families:
                # Create/Get Service Family (as Category) under Cluster
                # This ensures the matrix UI (Cluster -> Family -> Service) works
                category, c_created = ServiceCategory.objects.get_or_create(
                    name=family_name,
                    domain=domain
                )
                if c_created:
                    self.stdout.write(f"  Created Service Family (Category): {family_name}")

                # Also create as ServiceFamily model entry for orchestration logic compatibility
                fam, f_created = ServiceFamily.objects.get_or_create(name=family_name)
                if f_created:
                    self.stdout.write(f"  Created ServiceFamily Model: {family_name}")

        # 2. Cleanup Legacy Domains that don't match the new clusters (Optional, depends on business rules)
        # We probably want to move existing services to the new structure rather than just deleting.
        # Mapping for common services to the new taxonomy (best-effort)
        mapping = {
            "Birth Notification (B1)": "Citizen Identity & Civil Status",
            "Business Name Reservation": "Business Registration & Trade",
            "Business Incorporation": "Business Registration & Trade",
            "Personal Taxation (e-TIMS)": "Revenue & Financial Administration",
            "Company Taxation": "Revenue & Financial Administration",
            "Land Transfer (Ardhisasa)": "Agriculture, Land & Natural Resources",
            "Student Enrollment (NEMIS)": "Education & Qualifications",
            "Athlete Registration And Eligibility Management": "Public Information & Heritage",
            "Food Relief Distribution Coordination": "Health & Social Protection",
            "Infrastructure Development Lifecycle": "Infrastructure & Transport Services",
            "Case Filing & Allocation": "Justice & Case Management",
            "Identity Verification (IPRS)": "Public Safety & Emergency Services", # Or Platform Capability?
        }

        for service_name, new_family in mapping.items():
            service = ServiceConfig.objects.filter(service_name__iexact=service_name).first()
            if service:
                # Get the new Category (Family) instance
                new_cat = ServiceCategory.objects.filter(name=new_family).first()
                new_fam = ServiceFamily.objects.filter(name=new_family).first()
                if new_cat:
                    service.category = new_cat
                    service.service_family = new_fam
                    service.save()
                    self.stdout.write(self.style.NOTICE(f"Re-mapped Service: {service_name} to {new_family}"))

        self.stdout.write(self.style.SUCCESS("Taxonomy seeding completed successfully."))
