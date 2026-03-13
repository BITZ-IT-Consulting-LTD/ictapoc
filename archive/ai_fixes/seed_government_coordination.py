import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep, ServiceCategory, ServiceDomain, ServiceFamily, ServiceGroup, User
from django.db import transaction

@transaction.atomic
def seed_interior_coordination():
    # 1. Setup MDA
    mda_name = "Executive Office of the President"
    mda_code = "PRESIDENCY"
    mda, _ = MDA.objects.update_or_create(
        code=mda_code,
        defaults={
            'name': mda_name,
            'description': "National Government Coordination & Information Tasking.",
            'is_priority': True
        }
    )

    # 2. Setup Taxonomy
    domain, _ = ServiceDomain.objects.get_or_create(name="Policy & Governance")
    category, _ = ServiceCategory.objects.get_or_create(
        name="Inter-Agency Coordination",
        domain=domain
    )
    family, _ = ServiceFamily.objects.get_or_create(
        name="Government Efficiency",
        defaults={'description': "Services aimed at enhancing government operations and alignment."}
    )
    group, _ = ServiceGroup.objects.get_or_create(name="Social Protection & Justice") # As per life-cycle group 5

    # 3. Service Config
    service_code = "PRES-COORD-001"
    service_name = "Zero-Friction Inter-Agency Tasking"
    
    form_schema = {
        "fields": [
            {"name": "priority_title", "label": "National Priority Title", "type": "text", "required": True},
            {"name": "description", "label": "Scope & Objectives", "type": "textarea", "required": True},
            {"name": "target_mdas", "label": "Stakeholder MDAs", "type": "text", "required": True},
            {"name": "kpis", "label": "Target KPIs", "type": "text", "required": True},
            {"name": "deadline", "label": "Completion Deadline", "type": "date", "required": True}
        ]
    }

    service, _ = ServiceConfig.objects.update_or_create(
        service_code=service_code,
        defaults={
            'service_name': service_name,
            'description': "Automated coordination hub leveraging real-time status tracking via service bus.",
            'mda': mda,
            'category': category,
            'service_family': family,
            'service_type': 'G2G',
            'is_public_facing': False, # G2G
            'form_schema': form_schema,
            'life_event_group': 'Governance',
        }
    )
    service.service_groups.add(group)

    # 4. Workflow Steps (TO-BE)
    WorkflowStep.objects.filter(service_config=service).delete()

    steps = [
        # 1. Auto-dispatch
        {
            'step_name': "Workflow Engine: Auto-dispatch Tasks to MDAs",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 10,
            'api_config': {
                'url': 'internal://workflow/auto_dispatch',
                'outcomes': [
                    {'label': 'dispatched', 'target_sequence': 20}
                ]
            }
        },
        # 2. Real-time Data Pull
        {
            'step_name': "X-Road: Real-time Data Pull (MDA Registries)",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 20,
            'api_config': {
                'url': 'HUDUMA_BRIDGE/MDAS/pull_kpi_data',
                'outcomes': [
                    {'label': 'data_pulled', 'target_sequence': 30},
                    {'label': 'api_failure', 'target_sequence': 21}
                ]
            }
        },
        {
            'step_name': "[Fallback] AI-based Nudge System for Deadlines",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 21,
            'api_config': {
                'url': 'internal://ai/nudge_mdas',
                'outcomes': [
                    {'label': 'nudged', 'target_sequence': 20} # Retry pull
                ]
            }
        },
        # 3. Auto-verify
        {
            'step_name': "X-Road: Auto-verify against IFMIS/BRS/IPRS",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 30,
            'api_config': {
                'url': 'HUDUMA_BRIDGE/REGISTRIES/verify_cross_reference',
                'outcomes': [
                    {'label': 'verified', 'target_sequence': 40}
                ]
            }
        },
        # 4. Data Consolidation
        {
            'step_name': "System: Real-time Data Consolidation",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 40,
            'api_config': {
                'url': 'internal://bi/consolidate_data',
                'outcomes': [
                    {'label': 'consolidated', 'target_sequence': 50}
                ]
            }
        },
        # 5. Dashboarding
        {
            'step_name': "Generate Live Executive Heatmap & Dashboard",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 50,
            'api_config': {
                'url': 'internal://bi/generate_heatmap',
                'outcomes': [
                    {'label': 'rendered', 'target_sequence': 60}
                ]
            }
        },
        # 6. Trend Detection & Escalation
        {
            'step_name': "AI Trend Detection (Escalation Trigger)",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 60,
            'api_config': {
                'url': 'internal://ai/detect_negative_trends',
                'outcomes': [
                    {'label': 'negative_trend', 'target_sequence': 61},
                    {'label': 'trend_positive', 'target_sequence': 70}
                ]
            }
        },
        {
            'step_name': "Auto-Trigger Escalation (HPS/CS)",
            'step_type': 'api_call',
            'bpmn_element_type': 'service_task',
            'role': 'system',
            'sequence': 61,
            'api_config': {
                'url': 'internal://workflow/escalate_critical',
                'outcomes': [
                    {'label': 'escalated', 'target_sequence': 70}
                ]
            }
        },
        # 7. Final SitRep
        {
            'step_name': "Routine Dashboard Monitoring & Archival",
            'step_type': 'manual',
            'bpmn_element_type': 'user_task',
            'role': 'COORDINATION_OFFICER',
            'sequence': 70,
            'api_config': {
                'outcomes': [
                    {'label': 'archived', 'target_sequence': None}
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

    print(f"Successfully seeded Coordination Service: {service_name}")

if __name__ == "__main__":
    seed_interior_coordination()
