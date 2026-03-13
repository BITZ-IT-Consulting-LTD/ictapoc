import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep, ServiceCategory, ServiceDomain, ServiceFamily, ServiceGroup, User
from django.db import transaction

@transaction.atomic
def seed_knqa_validation():
    # 1. Setup MDA
    mda_name = "Kenya National Qualifications Authority"
    mda_code = "KNQA"
    mda, _ = MDA.objects.update_or_create(
        code=mda_code,
        defaults={
            'name': mda_name,
            'description': "Coordinates and harmonizes education, training, and assessment in Kenya.",
            'is_priority': True
        }
    )

    # 2. Setup Taxonomy
    domain, _ = ServiceDomain.objects.get_or_create(name="Social & Citizen Services")
    category, _ = ServiceCategory.objects.get_or_create(
        name="Education & Employment",
        domain=domain
    )
    family, _ = ServiceFamily.objects.get_or_create(
        name="Skills & Qualifications",
        defaults={'description': "Services related to the recognition and validation of learning achievements."}
    )
    group, _ = ServiceGroup.objects.get_or_create(name="Childhood & Education")

    # 3. Service Config
    service_code = "KNQA-VAL-001"
    service_name = "Qualification Validation (TO-BE)"
    
    form_schema = {
        "fields": [
            {"name": "applicant_full_name", "label": "Full Name", "type": "text", "required": True},
            {"name": "id_number", "label": "ID Number", "type": "text", "required": True},
            {"name": "institution_name", "label": "Issuing Institution", "type": "text", "required": True},
            {"name": "certificate_number", "label": "Certificate/Diploma Number", "type": "text", "required": True},
            {"name": "year_of_graduation", "label": "Year of Graduation", "type": "number", "required": True},
            {"name": "specialization", "label": "Field of Study", "type": "text", "required": True}
        ]
    }

    service, _ = ServiceConfig.objects.update_or_create(
        service_code=service_code,
        defaults={
            'service_name': service_name,
            'description': "Validation of local and foreign qualifications and recognition of prior learning.",
            'mda': mda,
            'category': category,
            'service_family': family,
            'service_type': 'G2C',
            'is_public_facing': True,
            'form_schema': form_schema,
            'life_event_group': 'Education',
        }
    )
    service.service_groups.add(group)

    # 4. Workflow Steps (TO-BE)
    WorkflowStep.objects.filter(service_config=service).delete()

    steps = [
        # 1. Retrieve Credentials
        {
            'step_name': "Retrieve Credentials from Registries (X-Road)",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 10,
            'api_config': {
                'url': 'HUDUMA_BRIDGE/KNEC/verify_credential',
                'outcomes': [
                    {'label': 'found', 'target_sequence': 20},
                    {'label': 'not_found', 'target_sequence': 11}
                ]
            }
        },
        {
            'step_name': "[Fallback] Manual Credential Retrieval/Vetting",
            'step_type': 'manual',
            'bpmn_element_type': 'user_task',
            'role': 'KNQA_TECHNICAL_OFFICER',
            'sequence': 11,
            'api_config': {
                'outcomes': [
                    {'label': 'verified', 'target_sequence': 20},
                    {'label': 'reject', 'target_sequence': None}
                ]
            }
        },
        # 2. Verify Authenticity
        {
            'step_name': "Automated Authenticity Verification",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 20,
            'api_config': {
                'url': 'internal://knqa/verify_authenticity',
                'outcomes': [
                    {'label': 'authentic', 'target_sequence': 30},
                    {'label': 'suspicious', 'target_sequence': 21}
                ]
            }
        },
        {
            'step_name': "[Fallback] In-depth Authenticity Review",
            'step_type': 'manual',
            'bpmn_element_type': 'user_task',
            'role': 'KNQA_TECHNICAL_OFFICER',
            'sequence': 21,
            'api_config': {
                'outcomes': [
                    {'label': 'authentic', 'target_sequence': 30},
                    {'label': 'reject', 'target_sequence': None}
                ]
            }
        },
        # 3. Map to KNQF
        {
            'step_name': "Map to KNQF Standard",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 30,
            'api_config': {
                'url': 'internal://knqa/map_knqf',
                'outcomes': [
                    {'label': 'mapped', 'target_sequence': 40}
                ]
            }
        },
        # 4. Risk Assessment
        {
            'step_name': "Risk-Based Routing Assessment",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 40,
            'api_config': {
                'url': 'internal://knqa/risk_assessment',
                'outcomes': [
                    {'label': 'low_risk', 'target_sequence': 60},
                    {'label': 'medium_risk', 'target_sequence': 41},
                    {'label': 'high_risk', 'target_sequence': 51}
                ]
            }
        },
        # 5. Review (Role-based)
        {
            'step_name': "Officer Review (Medium Risk)",
            'step_type': 'manual',
            'bpmn_element_type': 'user_task',
            'role': 'KNQA_TECHNICAL_OFFICER',
            'sequence': 41,
            'api_config': {
                'outcomes': [
                    {'label': 'approve', 'target_sequence': 60},
                    {'label': 'reject', 'target_sequence': None}
                ]
            }
        },
        {
            'step_name': "Committee Review (High Risk)",
            'step_type': 'manual',
            'bpmn_element_type': 'user_task',
            'role': 'TECHNICAL_COMMITTEE',
            'sequence': 51,
            'api_config': {
                'outcomes': [
                    {'label': 'approve', 'target_sequence': 60},
                    {'label': 'reject', 'target_sequence': None}
                ]
            }
        },
        # 6. Generate Letter
        {
            'step_name': "Generate Verifiable Validation Letter",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 60,
            'api_config': {
                'url': 'internal://output/generate_validation_letter',
                'outcomes': [
                    {'label': 'generated', 'target_sequence': 70}
                ]
            }
        },
        # 7. Update Registry
        {
            'step_name': "Update National Qualification Registry",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 70,
            'api_config': {
                'url': 'internal://knqa/update_registry',
                'outcomes': [
                    {'label': 'updated', 'target_sequence': None}
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

    print(f"Successfully seeded KNQA service: {service_name}")

if __name__ == "__main__":
    seed_knqa_validation()
