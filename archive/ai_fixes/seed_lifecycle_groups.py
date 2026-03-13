
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig, ServiceGroup

def seed_lifecycle_groups():
    # Define groups
    stages_data = [
        {"name": "1. The Cradle (Birth & Identity)", "description": "Establish legal existence and foundational identity."},
        {"name": "2. Childhood & Education", "description": "Learning, development, and academic progression."},
        {"name": "3. Coming of Age (Adulthood)", "description": "Transition to legal adulthood, rights, and privileges."},
        {"name": "4. Economic Life (Business & Tax)", "description": "Participation in the formal economy and social security."},
        {"name": "5. Family & Property", "description": "Formalizing family units and property ownership."},
        {"name": "6. The Death (Succession)", "description": "Closing the lifecycle and administering succession."}
    ]

    # Main group
    main_group, _ = ServiceGroup.objects.get_or_create(
        name="Cradle to Death",
        defaults={"description": "Whole-of-Government Service Delivery Lifecycle."}
    )

    stages = {}
    for g_data in stages_data:
        g, created = ServiceGroup.objects.get_or_create(
            name=g_data["name"],
            defaults={"description": g_data["description"]}
        )
        stages[g_data["name"]] = g
        print(f"Group: {g.name} ({'Created' if created else 'Existing'})")

    # Mapping keywords/names to groups
    mapping = {
        "1. The Cradle (Birth & Identity)": [
            "Birth Notification",
            "Birth and Death Registration",
            "Taxpayer Registration (PIN)",
            "Identity Registration",
            "IPRS",
            "Burial Permit",
            "SHA Registration"
        ],
        "2. Childhood & Education": [
            "Student Enrollment (NEMIS)",
            "Student Admission",
            "Higher Education Loan",
            "Exam Administration",
            "KNEC"
        ],
        "3. Coming of Age (Adulthood)": [
            "National Identity Card Registration",
            "Passport Application",
            "Driving License Renewal"
        ],
        "4. Economic Life (Business & Tax)": [
            "Tax Return Filing",
            "Tax Payment Processing",
            "Business Incorporation",
            "Social Security (NSSF)",
            "Business Name"
        ],
        "5. Family & Property": [
            "Marriage Registration",
            "Land Register",
            "Title Deed",
            "Property Transfer",
            "Ardhisasa",
            "Societies Registration"
        ],
        "6. The Death (Succession)": [
            "Unclaimed Assets",
            "Estate Administration",
            "Succession & Probate",
            "Grant of Probate"
        ]
    }

    for group_name, patterns in mapping.items():
        stage_group = stages[group_name]
        for pattern in patterns:
            matched_services = ServiceConfig.objects.filter(service_name__icontains=pattern)
            for svc in matched_services:
                svc.service_groups.add(stage_group)
                svc.service_groups.add(main_group) # Also add to the main category
                print(f"  - Linked '{svc.service_name}' to '{group_name}' AND 'Cradle to Death'")

if __name__ == "__main__":
    seed_lifecycle_groups()
