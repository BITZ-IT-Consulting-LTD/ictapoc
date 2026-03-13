import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep, ServiceCategory, ServiceDomain, ServiceFamily, ServiceGroup, User
from django.db import transaction

@transaction.atomic
def seed_crs_birth_registration():
    # 1. Setup MDA
    mda_name = "Ministry of Interior and National Administration"
    mda_code = "INTERIOR"
    mda, _ = MDA.objects.update_or_create(
        code=mda_code,
        defaults={
            'name': mda_name,
            'description': "Department of Civil Registration Services (CRS)",
            'is_priority': True
        }
    )

    # 2. Setup Taxonomy
    domain, _ = ServiceDomain.objects.get_or_create(name="Social & Citizen Services")
    category, _ = ServiceCategory.objects.get_or_create(
        name="Vital Event Registration",
        domain=domain
    )
    family, _ = ServiceFamily.objects.get_or_create(
        name="Civil Registration",
        defaults={'description': "Registration of births, deaths, and marriages."}
    )
    group, _ = ServiceGroup.objects.get_or_create(name="Cradle to Death")

    # 3. Service Config
    service_code = "CRS-BIRTH-001"
    service_name = "Birth Registration (Seamless)"
    
    form_schema = {
        "fields": [
            {"name": "child_name", "label": "Child's Full Name", "type": "text", "required": True},
            {"name": "date_of_birth", "label": "Date of Birth", "type": "date", "required": True},
            {"name": "mother_id", "label": "Mother's ID Number", "type": "text", "required": True},
            {"name": "father_id", "label": "Father's ID Number", "type": "text", "required": False},
            {"name": "hospital_name", "label": "Hospital/Point of Occurrence", "type": "text", "required": True},
            {"name": "notification_number", "label": "Notification Number", "type": "text", "required": True}
        ]
    }

    service, _ = ServiceConfig.objects.update_or_create(
        service_code=service_code,
        defaults={
            'service_name': service_name,
            'description': "Seamless registration of births triggered by hospital notifications.",
            'mda': mda,
            'category': category,
            'service_family': family,
            'service_type': 'G2C',
            'is_public_facing': True,
            'form_schema': form_schema,
            'life_event_group': 'Birth',
        }
    )
    service.service_groups.add(group)

    # 4. Workflow Steps (TO-BE)
    WorkflowStep.objects.filter(service_config=service).delete()

    steps = [
        # 1. Verify Parent IDs
        {
            'step_name': "Verify Parents Identity (IPRS/KeSEL)",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 10,
            'api_config': {
                'url': 'HUDUMA_BRIDGE/IPRS/verify',
                'outcomes': [
                    {'label': 'verified', 'target_sequence': 20},
                    {'label': 'failure', 'target_sequence': 11}
                ]
            }
        },
        {
            'step_name': "[Fallback] Manual Identity Verification",
            'step_type': 'manual',
            'bpmn_element_type': 'user_task',
            'role': 'CRS_OFFICER',
            'sequence': 11,
            'api_config': {
                'outcomes': [
                    {'label': 'verified', 'target_sequence': 20},
                    {'label': 'reject', 'target_sequence': None}
                ]
            }
        },
        # 2. Mint Maisha Namba
        {
            'step_name': "Mint Maisha Namba (UPI)",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 20,
            'api_config': {
                'url': 'internal://crs/mint_upi',
                'outcomes': [
                    {'label': 'minted', 'target_sequence': 30}
                ]
            }
        },
        # 3. Store in Vault
        {
            'step_name': "Archive to Vital Events Vault",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 30,
            'api_config': {
                'url': 'internal://crs/archive_vault',
                'outcomes': [
                    {'label': 'archived', 'target_sequence': 40}
                ]
            }
        },
        # 4. Notify Parents
        {
            'step_name': "Notify Parents via SMS/eCitizen",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 40,
            'api_config': {
                'url': 'internal://notification/notify_issuance',
                'outcomes': [
                    {'label': 'notified', 'target_sequence': 50}
                ]
            }
        },
        # 5. Issue Digital Certificate
        {
            'step_name': "Issue Verifiable Digital Certificate to Wallet",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 50,
            'api_config': {
                'url': 'internal://output/generate_certificate',
                'outcomes': [
                    {'label': 'issued', 'target_sequence': None}
                ]
            }
        }
    ]

    for step_data in steps:
        WorkflowStep.objects.create(
            service_config=service,
            lifecycle_stage='to_be',
            **step_data
        )

    print(f"Successfully seeded CRS service: {service_name}")

if __name__ == "__main__":
    seed_crs_birth_registration()
