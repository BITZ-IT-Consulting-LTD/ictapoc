import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep, ServiceCategory, ServiceDomain, ServiceFamily, ServiceGroup, User
from django.db import transaction

@transaction.atomic
def seed_children_services_case_management():
    # 1. Setup MDA
    mda_name = "State Department for Children Services"
    mda_code = "CHILDREN"
    mda, _ = MDA.objects.update_or_create(
        code=mda_code,
        defaults={
            'name': mda_name,
            'description': "Responsible for the protection and well-being of children in Kenya.",
            'is_priority': True
        }
    )

    # 2. Setup Taxonomy
    domain, _ = ServiceDomain.objects.get_or_create(name="Social & Citizen Services")
    category, _ = ServiceCategory.objects.get_or_create(
        name="Child Protection",
        domain=domain
    )
    family, _ = ServiceFamily.objects.get_or_create(
        name="Protection & Welfare",
        defaults={'description': "Services related to the safety and welfare of vulnerable groups."}
    )
    group, _ = ServiceGroup.objects.get_or_create(name="Social Protection & Justice")

    # 3. Service Config
    service_code = "CHILD-CASE-001"
    service_name = "Child Protection Case Management (Digital)"
    
    form_schema = {
        "fields": [
            {"name": "reporter_name", "label": "Reporter Name", "type": "text", "required": True},
            {"name": "child_upi", "label": "Child's Maisha Namba (if known)", "type": "text", "required": False},
            {"name": "child_name", "label": "Child's Name", "type": "text", "required": True},
            {"name": "incident_description", "label": "Incident Description", "type": "textarea", "required": True},
            {"name": "location", "label": "Location of Incident", "type": "text", "required": True},
            {"name": "danger_level", "label": "Self-Assessed Danger Level", "type": "select", "options": ["Low", "Medium", "High", "Critical"], "required": True}
        ]
    }

    service, _ = ServiceConfig.objects.update_or_create(
        service_code=service_code,
        defaults={
            'service_name': service_name,
            'description': "Digital end-to-end case management for children in need of care and protection.",
            'mda': mda,
            'category': category,
            'service_family': family,
            'service_type': 'G2C',
            'is_public_facing': True,
            'form_schema': form_schema,
            'life_event_group': 'Childhood',
        }
    )
    service.service_groups.add(group)

    # 4. Workflow Steps (TO-BE)
    WorkflowStep.objects.filter(service_config=service).delete()

    steps = [
        # 1. Identity Verification
        {
            'step_name': "Identity Verification Integration (IPRS)",
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
            'role': 'CHILDREN_OFFICER',
            'sequence': 11,
            'api_config': {
                'outcomes': [
                    {'label': 'verified', 'target_sequence': 20},
                    {'label': 'reject', 'target_sequence': None}
                ]
            }
        },
        # 2. Risk Scoring
        {
            'step_name': "AI Risk Scoring Support",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 20,
            'api_config': {
                'url': 'internal://children/risk_score',
                'outcomes': [
                    {'label': 'emergency', 'target_sequence': 30},
                    {'label': 'standard', 'target_sequence': 30}
                ]
            }
        },
        # 3. Investigation
        {
            'step_name': "Investigation & Human Casework Action",
            'step_type': 'manual',
            'bpmn_element_type': 'user_task',
            'role': 'CHILDREN_OFFICER',
            'sequence': 30,
            'api_config': {
                'outcomes': [
                    {'label': 'court_order_needed', 'target_sequence': 40},
                    {'label': 'care_placement_needed', 'target_sequence': 50},
                    {'label': 'resolved_at_investigation', 'target_sequence': 70}
                ]
            }
        },
        # 4. Court Filing
        {
            'step_name': "Automated Court Filing (Judiciary API)",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 40,
            'api_config': {
                'url': 'HUDUMA_BRIDGE/JUDICIARY/file_protection_order',
                'outcomes': [
                    {'label': 'filed', 'target_sequence': 41},
                    {'label': 'failure', 'target_sequence': 42}
                ]
            }
        },
        {
            'step_name': "[Manual] Process Protection Order (Judiciary)",
            'step_type': 'manual',
            'bpmn_element_type': 'user_task',
            'role': 'JUDICIAL_OFFICER',
            'sequence': 41,
            'api_config': {
                'outcomes': [
                    {'label': 'order_issued', 'target_sequence': 50},
                    {'label': 'order_denied', 'target_sequence': 30}
                ]
            }
        },
        {
            'step_name': "[Fallback] Manual Court Filing Liaison",
            'step_type': 'manual',
            'bpmn_element_type': 'user_task',
            'role': 'CHILDREN_OFFICER',
            'sequence': 42,
            'api_config': {
                'outcomes': [
                    {'label': 'order_obtained', 'target_sequence': 50},
                    {'label': 'retry_api', 'target_sequence': 40}
                ]
            }
        },
        # 5. Care Institution
        {
            'step_name': "Provide Intervention Care (Care Institution)",
            'step_type': 'manual',
            'bpmn_element_type': 'user_task',
            'role': 'CARE_INSTITUTION_OFFICER',
            'sequence': 50,
            'api_config': {
                'outcomes': [
                    {'label': 'care_initiated', 'target_sequence': 60}
                ]
            }
        },
        # 6. Monitoring
        {
            'step_name': "Monitoring Visits & Case Updates",
            'step_type': 'manual',
            'bpmn_element_type': 'user_task',
            'role': 'CHILDREN_OFFICER',
            'sequence': 60,
            'api_config': {
                'outcomes': [
                    {'label': 'not_ready_for_closure', 'target_sequence': 60}, # Loop for monitoring
                    {'label': 'ready_for_closure', 'target_sequence': 70}
                ]
            }
        },
        # 7. Secure Archival
        {
            'step_name': "Secure Case Archival (National CPIMS)",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 70,
            'api_config': {
                'url': 'internal://cpims/secure_archival',
                'outcomes': [
                    {'label': 'archived', 'target_sequence': 80}
                ]
            }
        },
        # 8. Closure
        {
            'step_name': "Case Closure Finalization",
            'step_type': 'manual',
            'bpmn_element_type': 'user_task',
            'role': 'CHILDREN_OFFICER',
            'sequence': 80,
            'api_config': {
                'outcomes': [
                    {'label': 'closed', 'target_sequence': None}
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

    print(f"Successfully seeded Children Services: {service_name}")

if __name__ == "__main__":
    seed_children_services_case_management()
