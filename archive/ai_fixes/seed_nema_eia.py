import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep, ServiceCategory, ServiceDomain, ServiceFamily, ServiceGroup, User
from django.db import transaction

@transaction.atomic
def seed_nema_eia():
    # 1. Setup MDA
    mda_name = "National Environment Management Authority"
    mda_code = "NEMA"
    mda, _ = MDA.objects.update_or_create(
        code=mda_code,
        defaults={
            'name': mda_name,
            'description': "Responsible for the supervision and coordination of environmental management across Kenya.",
            'is_priority': True
        }
    )

    # 2. Setup Taxonomy
    domain, _ = ServiceDomain.objects.get_or_create(name="Economic & Regulatory")
    category, _ = ServiceCategory.objects.get_or_create(
        name="Environmental Licensing",
        domain=domain
    )
    family, _ = ServiceFamily.objects.get_or_create(
        name="Environmental Services",
        defaults={'description': "Services related to environmental impact and compliance."}
    )
    group, _ = ServiceGroup.objects.get_or_create(name="Employment & Business")

    # 3. Service Config
    service_code = "NEMA-EIA-001"
    service_name = "Environmental Impact Assessment (EIA) Licensing"
    
    form_schema = {
        "fields": [
            {"name": "proponent_name", "label": "Proponent Name", "type": "text", "required": True},
            {"name": "business_registration_number", "label": "Business Registration Number", "type": "text", "required": True},
            {"name": "project_title", "label": "Project Title", "type": "text", "required": True},
            {"name": "project_location_coordinates", "label": "Project Location (GPS)", "type": "text", "required": True},
            {"name": "parcel_number", "label": "Land Parcel Number", "type": "text", "required": True},
            {"name": "project_report", "label": "EIA Project Report (PDF)", "type": "file", "required": True}
        ]
    }

    service, _ = ServiceConfig.objects.update_or_create(
        service_code=service_code,
        defaults={
            'service_name': service_name,
            'description': "Issuance of Environmental Impact Assessment (EIA) licenses for development projects.",
            'mda': mda,
            'category': category,
            'service_family': family,
            'service_type': 'G2B',
            'is_public_facing': True,
            'form_schema': form_schema,
            'life_event_group': 'Business',
        }
    )
    service.service_groups.add(group)

    # 4. Workflow Steps (TO-BE)
    # Sequence Table:
    # 10: Verify Business (API -> 11 fallback, 20 success)
    # 11: Manual Business Verify (User) -> 20
    # 20: Fetch Land Data (API -> 21 fallback, 30 success)
    # 21: Manual Land Verify (User) -> 30
    # 30: Screen Environmental Risk (API -> 40 success)
    # 40: Route for Digital Review (API -> 50)
    # 50: Lead Agency Digital Review (User/Role) -> 60
    # 60: Mobile GIS Inspection (User/Role) -> 70
    # 70: Technical Committee Decision (User/Role) -> 80
    # 80: Issue Digital License (API) -> END

    WorkflowStep.objects.filter(service_config=service).delete()

    steps = [
        # 1. Verify BRS
        {
            'step_name': "Verify Business Registration (BRS)",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 10,
            'api_config': {
                'url': 'HUDUMA_BRIDGE/BRS/verify',
                'outcomes': [
                    {'label': 'success', 'target_sequence': 20},
                    {'label': 'failure', 'target_sequence': 11}
                ]
            }
        },
        {
            'step_name': "[Fallback] Manual Business Verification",
            'step_type': 'manual',
            'bpmn_element_type': 'user_task',
            'role': 'NEMA_REGISTRY_OFFICER',
            'sequence': 11,
            'api_config': {
                'outcomes': [
                    {'label': 'verified', 'target_sequence': 20},
                    {'label': 'reject', 'target_sequence': None}
                ]
            }
        },
        # 2. Fetch Land Data
        {
            'step_name': "Fetch Land Data (Ardhisasa)",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 20,
            'api_config': {
                'url': 'HUDUMA_BRIDGE/ARDHISASA/parcel_details',
                'outcomes': [
                    {'label': 'success', 'target_sequence': 30},
                    {'label': 'failure', 'target_sequence': 21}
                ]
            }
        },
        {
            'step_name': "[Fallback] Manual Land Data Verification",
            'step_type': 'manual',
            'bpmn_element_type': 'user_task',
            'role': 'ENVIRONMENTAL_OFFICER',
            'sequence': 21,
            'api_config': {
                'outcomes': [
                    {'label': 'verified', 'target_sequence': 30},
                    {'label': 'reject', 'target_sequence': None}
                ]
            }
        },
        # 3. Screen Risk
        {
            'step_name': "Automated Environmental Risk Screening",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 30,
            'api_config': {
                'url': 'internal://nema/screen_risk',
                'outcomes': [
                    {'label': 'low_risk', 'target_sequence': 40},
                    {'label': 'high_risk', 'target_sequence': 40} # Both go to review in this simplified model
                ]
            }
        },
        # 4. Route for Review
        {
            'step_name': "Route Project for Digital Review",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 40,
            'api_config': {
                'url': 'internal://nema/route_review',
                'outcomes': [
                    {'label': 'routed', 'target_sequence': 50}
                ]
            }
        },
        # 5. Lead Agency Review
        {
            'step_name': "Lead Agency Digital Review",
            'step_type': 'manual',
            'bpmn_element_type': 'user_task',
            'role': 'LEAD_AGENCY_OFFICER',
            'sequence': 50,
            'api_config': {
                'outcomes': [
                    {'label': 'comments_provided', 'target_sequence': 60}
                ]
            }
        },
        # 6. GIS Inspection
        {
            'step_name': "Mobile GIS Site Inspection",
            'step_type': 'manual',
            'bpmn_element_type': 'user_task',
            'role': 'ENVIRONMENTAL_OFFICER',
            'sequence': 60,
            'api_config': {
                'outcomes': [
                    {'label': 'inspection_complete', 'target_sequence': 70}
                ]
            }
        },
        # 7. Committee Decision
        {
            'step_name': "Technical Committee Review & Decision",
            'step_type': 'manual',
            'bpmn_element_type': 'user_task',
            'role': 'TECHNICAL_COMMITTEE',
            'sequence': 70,
            'api_config': {
                'outcomes': [
                    {'label': 'approve', 'target_sequence': 80},
                    {'label': 'reject', 'target_sequence': None}
                ]
            }
        },
        # 8. Issue License
        {
            'step_name': "Auto-generate Digital EIA License",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 80,
            'api_config': {
                'url': 'internal://output/generate_license',
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

    print(f"Successfully seeded NEMA service: {service_name}")

if __name__ == "__main__":
    seed_nema_eia()
