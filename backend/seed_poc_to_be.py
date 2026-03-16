import os
import django
from django.db import transaction

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep, ServiceFamily, ServiceCategory, ServiceDomain, ServiceGroup

@transaction.atomic
def seed_poc_to_be_processes():
    print("Initiating POC 'To-Be' Process Seeding (Aligned with Final Docs)...")

    # 1. Setup Taxonomy & Groups
    gov_domain, _ = ServiceDomain.objects.get_or_create(name="Public Administration & Governance")
    economic_domain, _ = ServiceDomain.objects.get_or_create(name="Economic & Regulatory")
    social_domain, _ = ServiceDomain.objects.get_or_create(name="Social & Citizen Services")

    cradle_group, _ = ServiceGroup.objects.get_or_create(name="Cradle to Death")
    priority_group, _ = ServiceGroup.objects.get_or_create(name="Priority MDAs")

    # 2. Setup MDAs (Aligned with docs_final codes)
    crs, _ = MDA.objects.update_or_create(
        code='CRS',
        defaults={'name': 'Civil Registration Services', 'description': 'Vital identity lifecycle management.', 'is_priority': True}
    )
    msme, _ = MDA.objects.update_or_create(
        code='MSME',
        defaults={'name': 'Ministry of Co-operatives and MSME Development', 'description': 'Business support and empowerment.', 'is_priority': True}
    )
    icta, _ = MDA.objects.update_or_create(
        code='ICTA',
        defaults={'name': 'Information and Communication Technology Authority', 'description': 'Digital shared services coordinator.', 'is_priority': True}
    )

    # -------------------------------------------------------------------------
    # PROCESS 1: G2C - Birth Registration (Cradle Portfolio)
    # Ref: _CIVIL_REGISTRATION_SERVICES_CRS____Service_Delivery.md
    # -------------------------------------------------------------------------
    birth_sf, _ = ServiceFamily.objects.get_or_create(name="Civil Registration & Identity")
    birth_cat, _ = ServiceCategory.objects.get_or_create(name="Vital Events", domain=social_domain)
    
    birth_svc, _ = ServiceConfig.objects.update_or_create(
        service_code="POC-G2C-BIRTH",
        defaults={
            'service_name': "Seamless Birth Registration (To-Be)",
            'description': "Automated registration of births triggered by health facilities (Afya App) with Maisha Namba linkage.",
            'mda': crs,
            'service_family': birth_sf,
            'category': birth_cat,
            'service_type': 'G2C',
            'is_public_facing': True,
            'life_event_group': 'Birth',
            'form_schema': {
                'fields': [
                    {'name': 'child_name', 'label': 'Child Name', 'type': 'text', 'required': True},
                    {'name': 'mother_id', 'label': 'Mother ID', 'type': 'text', 'required': True},
                    {'name': 'hospital_code', 'label': 'Hospital Code (MOH Afya)', 'type': 'text', 'required': True}
                ]
            }
        }
    )
    birth_svc.service_groups.add(cradle_group, priority_group)

    WorkflowStep.objects.filter(service_config=birth_svc).delete()
    WorkflowStep.objects.bulk_create([
        WorkflowStep(service_config=birth_svc, sequence=10, step_name="Identity Verification (KeSEL/IPRS)", step_type='api_call', bpmn_element_type='service_task', role='system', lifecycle_stage='to_be', 
                     api_config={'outcomes': [{'label': 'success', 'target_sequence': 20}, {'label': 'failure', 'target_sequence': 30}]}),
        WorkflowStep(service_config=birth_svc, sequence=20, step_name="Mint Unique Maisha Namba", step_type='api_call', bpmn_element_type='service_task', role='system', lifecycle_stage='to_be',
                     api_config={'outcomes': [{'label': 'success', 'target_sequence': 40}]}),
        WorkflowStep(service_config=birth_svc, sequence=30, step_name="Officer Review (Complex Cases)", step_type='manual', bpmn_element_type='user_task', role='GLOBAL_OFFICER', lifecycle_stage='to_be'),
        WorkflowStep(service_config=birth_svc, sequence=40, step_name="NPKI Digital Signing (Trust Hub)", step_type='api_call', bpmn_element_type='service_task', role='system', lifecycle_stage='to_be',
                     api_config={'outcomes': [{'label': 'success', 'target_sequence': 50}]}),
        WorkflowStep(service_config=birth_svc, sequence=50, step_name="Issue Verifiable Credential to Wallet", step_type='api_call', bpmn_element_type='service_task', role='system', lifecycle_stage='to_be'),
    ])

    # -------------------------------------------------------------------------
    # PROCESS 2: G2B - MSME Certificate Issuance (Priority Portfolio)
    # Ref: Ministry_of_Co-operatives_and_Micro_Small_and_Medium_Enterprises_MSME_Development...md
    # -------------------------------------------------------------------------
    msme_sf, _ = ServiceFamily.objects.get_or_create(name="Business & Revenue")
    msme_cat, _ = ServiceCategory.objects.get_or_create(name="Business Licensing", domain=economic_domain)
    
    msme_svc, _ = ServiceConfig.objects.update_or_create(
        service_code="POC-G2B-MSME",
        defaults={
            'service_name': "Enterprise Opportunity Registration",
            'description': "Real-time issuance of MSME certificates with BRS and KRA auto-validation.",
            'mda': msme,
            'service_family': msme_sf,
            'category': msme_cat,
            'service_type': 'G2B',
            'is_public_facing': True,
            'form_schema': {
                'fields': [
                    {'name': 'brn_number', 'label': 'Business Registration Number', 'type': 'text', 'required': True},
                    {'name': 'kra_pin', 'label': 'KRA PIN', 'type': 'text', 'required': True}
                ]
            }
        }
    )
    msme_svc.service_groups.add(priority_group)

    WorkflowStep.objects.filter(service_config=msme_svc).delete()
    WorkflowStep.objects.bulk_create([
        WorkflowStep(service_config=msme_svc, sequence=10, step_name="Fetch BRS Details via Service Bus", step_type='api_call', bpmn_element_type='service_task', role='system', lifecycle_stage='to_be',
                     api_config={'outcomes': [{'label': 'success', 'target_sequence': 20}, {'label': 'failure', 'target_sequence': 40}]}),
        WorkflowStep(service_config=msme_svc, sequence=20, step_name="Auto-Validate KRA Compliance", step_type='api_call', bpmn_element_type='service_task', role='system', lifecycle_stage='to_be',
                     api_config={'outcomes': [{'label': 'success', 'target_sequence': 30}, {'label': 'failure', 'target_sequence': 40}]}),
        WorkflowStep(service_config=msme_svc, sequence=30, step_name="Rules Engine Evaluation", step_type='api_call', bpmn_element_type='service_task', role='system', lifecycle_stage='to_be',
                     api_config={'outcomes': [{'label': 'success', 'target_sequence': 60}, {'label': 'manual_review', 'target_sequence': 40}]}),
        WorkflowStep(service_config=msme_svc, sequence=40, step_name="Strategic Portfolio Review", step_type='manual', bpmn_element_type='user_task', role='GLOBAL_OFFICER', lifecycle_stage='to_be'),
        WorkflowStep(service_config=msme_svc, sequence=50, step_name="Final Strategic Authorization", step_type='manual', bpmn_element_type='user_task', role='GLOBAL_SUPERVISOR', lifecycle_stage='to_be'),
        WorkflowStep(service_config=msme_svc, sequence=60, step_name="Generate Verifiable QR Certificate", step_type='api_call', bpmn_element_type='service_task', role='system', lifecycle_stage='to_be'),
    ])

    # -------------------------------------------------------------------------
    # PROCESS 3: G2G - ICT Standards Compliance Review (Tech Hub)
    # Ref: Information_and_Communication_Technology_Authority_ICTA____Service_Delivery.md
    # -------------------------------------------------------------------------
    ict_sf, _ = ServiceFamily.objects.get_or_create(name="Government Administration (G2G)")
    ict_cat, _ = ServiceCategory.objects.get_or_create(name="Digital Coordination", domain=gov_domain)
    
    ict_svc, _ = ServiceConfig.objects.update_or_create(
        service_code="POC-G2G-ICT-STD",
        defaults={
            'service_name': "ICT Standards Compliance Assessment",
            'description': "Authoritative technical review of MDA infrastructure and software standards.",
            'mda': icta,
            'service_family': ict_sf,
            'category': ict_cat,
            'service_type': 'G2G',
            'is_public_facing': False,
            'form_schema': {
                'fields': [
                    {'name': 'mda_requesting', 'label': 'Originating MDA', 'type': 'text', 'required': True},
                    {'name': 'infrastructure_type', 'label': 'System/Infrastructure Type', 'type': 'text', 'required': True}
                ]
            }
        }
    )
    ict_svc.service_groups.add(priority_group)

    WorkflowStep.objects.filter(service_config=ict_svc).delete()
    WorkflowStep.objects.bulk_create([
        WorkflowStep(service_config=ict_svc, sequence=10, step_name="Inventory Registry Check", step_type='api_call', bpmn_element_type='service_task', role='system', lifecycle_stage='to_be',
                     api_config={'outcomes': [{'label': 'success', 'target_sequence': 20}]}),
        WorkflowStep(service_config=ict_svc, sequence=20, step_name="Technical Standards Evaluation", step_type='manual', bpmn_element_type='user_task', role='GLOBAL_OFFICER', lifecycle_stage='to_be'),
        WorkflowStep(service_config=ict_svc, sequence=30, step_name="Directorate-General Authorization", step_type='manual', bpmn_element_type='user_task', role='GLOBAL_SUPERVISOR', lifecycle_stage='to_be'),
        WorkflowStep(service_config=ict_svc, sequence=40, step_name="Official Compliance Dispatch", step_type='api_call', bpmn_element_type='service_task', role='system', lifecycle_stage='to_be'),
    ])

    print("Successfully seeded all POC 'To-Be' processes with Final Doc alignment!")
    print("- G2C: Seamless Birth Registration (CRS)")
    print("- G2B: Enterprise Opportunity Registration (MSME)")
    print("- G2G: ICT Standards Compliance Review (ICTA)")

if __name__ == "__main__":
    seed_poc_to_be_processes()
