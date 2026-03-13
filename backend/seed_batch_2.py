import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep, ServiceCategory, ServiceDomain, ServiceFamily, ServiceGroup, User
from django.db import transaction

@transaction.atomic
def seed_batch_2():
    def get_taxonomy(domain_name, category_name, family_name, group_name):
        domain, _ = ServiceDomain.objects.get_or_create(name=domain_name)
        category, _ = ServiceCategory.objects.get_or_create(name=category_name, domain=domain)
        family, _ = ServiceFamily.objects.get_or_create(name=family_name)
        group, _ = ServiceGroup.objects.get_or_create(name=group_name)
        return category, family, group

    # 1. Energy
    mda_energy, _ = MDA.objects.update_or_create(
        code="ENERGY",
        defaults={'name': "Ministry of Energy and Petroleum", 'is_priority': True}
    )
    cat, fam, grp = get_taxonomy("Economic & Regulatory", "Energy Licensing", "Energy & Resources", "Employment & Business")
    service_energy, _ = ServiceConfig.objects.update_or_create(
        service_code="ENG-LIC-001",
        defaults={
            'service_name': "Energy Licensing & Records Management",
            'description': "Digital EDRMS and automated licensing for the energy sector.",
            'mda': mda_energy,
            'category': cat,
            'service_family': fam,
            'service_type': 'G2B',
            'is_public_facing': True,
            'form_schema': {
                "fields": [
                    {"name": "company_reg", "label": "Company Registration Number", "type": "text", "required": True},
                    {"name": "permit_type", "label": "Permit Type", "type": "select", "options": ["Generation", "Transmission", "Distribution"], "required": True},
                    {"name": "application_doc", "label": "Technical Proposal (PDF)", "type": "file", "required": True}
                ]
            }
        }
    )
    service_energy.service_groups.add(grp)
    WorkflowStep.objects.filter(service_config=service_energy).delete()
    energy_steps = [
        {'sequence': 10, 'step_name': "Digital Intake & NPKI Verification", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'internal://trust/verify_npki'}},
        {'sequence': 20, 'step_name': "Cross-verify with EPRA / BRS / KRA", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/ENERGY/verify_all', 'outcomes': [{'label': 'verified', 'target_sequence': 30}, {'label': 'fail', 'target_sequence': 21}]}},
        {'sequence': 21, 'step_name': "[Fallback] Manual Compliance Review", 'step_type': 'manual', 'bpmn_element_type': 'user_task', 'role': 'ENERGY_RECORDS_OFFICER', 'api_config': {'outcomes': [{'label': 'cleared', 'target_sequence': 30}]}},
        {'sequence': 30, 'step_name': "Parallel Inter-departmental Review", 'step_type': 'manual', 'bpmn_element_type': 'user_task', 'role': 'ENERGY_TECHNICAL_UNIT'},
        {'sequence': 40, 'step_name': "Digital Approval & Cloud Archival", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'internal://edrms/archive'}},
    ]
    for s in energy_steps: WorkflowStep.objects.create(service_config=service_energy, lifecycle_stage='to_be', **s)

    # 2. Government Spokesperson
    mda_spox, _ = MDA.objects.update_or_create(
        code="SPOKESPERSON",
        defaults={'name': "Office of the Government Spokesperson", 'is_priority': True}
    )
    cat, fam, grp = get_taxonomy("Policy & Governance", "Public Communication", "Governance & Policy", "Social Protection & Justice")
    service_spox, _ = ServiceConfig.objects.update_or_create(
        service_code="SPX-MSG-001",
        defaults={
            'service_name': "Public Communication & Archiving",
            'description': "Immutable government messaging and AI archiving.",
            'mda': mda_spox,
            'category': cat,
            'service_family': fam,
            'service_type': 'G2G',
            'is_public_facing': False,
            'form_schema': {
                "fields": [
                    {"name": "mda_source", "label": "Source MDA", "type": "text", "required": True},
                    {"name": "message_title", "label": "Press Release Title", "type": "text", "required": True},
                    {"name": "content", "label": "Content", "type": "textarea", "required": True}
                ]
            }
        }
    )
    service_spox.service_groups.add(grp)
    WorkflowStep.objects.filter(service_config=service_spox).delete()
    spox_steps = [
        {'sequence': 10, 'step_name': "NPKI Digital Signature Application", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'internal://trust/apply_stamp'}},
        {'sequence': 20, 'step_name': "Multi-Channel Dissemination (KBC/SMS)", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/PUSH/all'}},
        {'sequence': 30, 'step_name': "AI-based Metadata Tagging & Archiving", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'internal://ai/archive_msg'}},
    ]
    for s in spox_steps: WorkflowStep.objects.create(service_config=service_spox, lifecycle_stage='to_be', **s)

    # 3. ICT Authority
    mda_icta, _ = MDA.objects.update_or_create(
        code="ICTA",
        defaults={'name': "ICT Authority", 'is_priority': True}
    )
    cat, fam, grp = get_taxonomy("Policy & Governance", "Digital Infrastructure", "Technology & Innovation", "Social Protection & Justice")
    service_icta, _ = ServiceConfig.objects.update_or_create(
        service_code="ICTA-GOV-001",
        defaults={
            'service_name': "Government ICT Project Implementation",
            'description': "Shared platforms and infrastructure management via GEA.",
            'mda': mda_icta,
            'category': cat,
            'service_family': fam,
            'service_type': 'G2G',
            'is_public_facing': False,
            'form_schema': {
                "fields": [
                    {"name": "project_name", "label": "Project Name", "type": "text", "required": True},
                    {"name": "target_mda", "label": "Implementing MDA", "type": "text", "required": True},
                    {"name": "architecture_blueprint", "label": "Architecture Blueprint (PDF)", "type": "file", "required": True}
                ]
            }
        }
    )
    service_icta.service_groups.add(grp)
    WorkflowStep.objects.filter(service_config=service_icta).delete()
    icta_steps = [
        {'sequence': 10, 'step_name': "Validate Against GEA Standards", 'step_type': 'manual', 'bpmn_element_type': 'user_task', 'role': 'ICTA_ARCHITECT'},
        {'sequence': 20, 'step_name': "Integrate via KeSEL (X-Road)", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/KESEL/register'}},
        {'sequence': 30, 'step_name': "Deploy on National Government Cloud", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'internal://cloud/deploy'}},
        {'sequence': 40, 'step_name': "Apply National PKI & Security Layer", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'internal://trust/secure'}},
    ]
    for s in icta_steps: WorkflowStep.objects.create(service_config=service_icta, lifecycle_stage='to_be', **s)

    # 4. KBC
    mda_kbc, _ = MDA.objects.update_or_create(
        code="KBC",
        defaults={'name': "Kenya Broadcasting Corporation", 'is_priority': True}
    )
    cat, fam, grp = get_taxonomy("Social & Citizen Services", "Content Licensing", "Media & Communication", "Employment & Business")
    service_kbc, _ = ServiceConfig.objects.update_or_create(
        service_code="KBC-ARC-001",
        defaults={
            'service_name': "Archival Content Licensing",
            'description': "Access to historical archives with digital licensing via GPA.",
            'mda': mda_kbc,
            'category': cat,
            'service_family': fam,
            'service_type': 'G2C',
            'is_public_facing': True,
            'form_schema': {
                "fields": [
                    {"name": "archive_id", "label": "Archive Asset ID", "type": "text", "required": True},
                    {"name": "license_use", "label": "Purpose of Use", "type": "select", "options": ["Academic", "Commercial", "Personal"], "required": True}
                ]
            }
        }
    )
    service_kbc.service_groups.add(grp)
    WorkflowStep.objects.filter(service_config=service_kbc).delete()
    kbc_steps = [
        {'sequence': 10, 'step_name': "AI-Powered Metadata Search", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'internal://kbc/search'}},
        {'sequence': 20, 'step_name': "Auto-verify Copyright & Fees", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'internal://kbc/verify_rights'}},
        {'sequence': 30, 'step_name': "Payment via GPA & Token Generation", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/GPA/pay_and_issue'}},
    ]
    for s in kbc_steps: WorkflowStep.objects.create(service_config=service_kbc, lifecycle_stage='to_be', **s)

    # 5. MSME Development
    mda_msme, _ = MDA.objects.update_or_create(
        code="MSME",
        defaults={'name': "Ministry of Co-operatives and MSMEs", 'is_priority': True}
    )
    cat, fam, grp = get_taxonomy("Social & Citizen Services", "MSME Support", "Finance & Credit", "Employment & Business")
    service_msme, _ = ServiceConfig.objects.update_or_create(
        service_code="MSM-CRD-001",
        defaults={
            'service_name': "MSME Credit & Fund Management",
            'description': "Unified credit portal with digital group wallets and AI scoring.",
            'mda': mda_msme,
            'category': cat,
            'service_family': fam,
            'service_type': 'G2B',
            'is_public_facing': True,
            'form_schema': {
                "fields": [
                    {"name": "id_no", "label": "National ID Number", "type": "text", "required": True},
                    {"name": "fund_type", "label": "Fund Type", "type": "select", "options": ["Hustler", "Uwezo", "WEF"], "required": True},
                    {"name": "loan_amount", "label": "Requested Amount", "type": "number", "required": True}
                ]
            }
        }
    )
    service_msme.service_groups.add(grp)
    WorkflowStep.objects.filter(service_config=service_msme).delete()
    msme_steps = [
        {'sequence': 10, 'step_name': "Validate Identity & BRS (X-Road)", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/MSME/verify', 'outcomes': [{'label': 'success', 'target_sequence': 20}, {'label': 'fail', 'target_sequence': 11}]}},
        {'sequence': 11, 'step_name': "[Fallback] Manual Identity Review", 'step_type': 'manual', 'bpmn_element_type': 'user_task', 'role': 'MSME_OFFICER', 'api_config': {'outcomes': [{'label': 'verified', 'target_sequence': 20}]}},
        {'sequence': 20, 'step_name': "AI Credit Scoring (GPA/BRS Data)", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'internal://msme/credit_score'}},
        {'sequence': 30, 'step_name': "Digital Group Wallet Creation (GPA)", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/GPA/create_wallet'}},
        {'sequence': 40, 'step_name': "Instant Disbursement via Aggregator", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/GPA/disburse'}},
    ]
    for s in msme_steps: WorkflowStep.objects.create(service_config=service_msme, lifecycle_stage='to_be', **s)

    # 6. Ministry of Health (MOH) - Detailed Workflow
    mda_moh, _ = MDA.objects.update_or_create(
        code="MOH",
        defaults={'name': "Ministry of Health", 'is_priority': True}
    )
    cat, fam, grp = get_taxonomy("Social & Citizen Services", "Health Care", "Social Protection", "Cradle to Death")
    service_moh, _ = ServiceConfig.objects.update_or_create(
        service_code="MOH-KHIE-001",
        defaults={
            'service_name': "Kenya Health Information Exchange (Unified Identity)",
            'description': "Unified patient mapping via Maisha Namba and Shared Health Record.",
            'mda': mda_moh,
            'category': cat,
            'service_family': fam,
            'service_type': 'G2C',
            'is_public_facing': True,
            'form_schema': {
                "fields": [
                    {"name": "maisha_namba", "label": "Maisha Namba / National ID", "type": "text", "required": True},
                    {"name": "fingerprint_data", "label": "Biometric Hash", "type": "text", "required": False}
                ]
            }
        }
    )
    service_moh.service_groups.add(grp)
    WorkflowStep.objects.filter(service_config=service_moh).delete()
    moh_steps = [
        {'sequence': 10, 'step_name': "Query Master Patient Index (MPI)", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/MPI/query', 'outcomes': [{'label': 'found', 'target_sequence': 20}, {'label': 'not_found', 'target_sequence': 11}]}},
        {'sequence': 11, 'step_name': "[Fallback] Hospital ID Verification", 'step_type': 'manual', 'bpmn_element_type': 'user_task', 'role': 'HEALTH_WORKER', 'api_config': {'outcomes': [{'label': 'verified', 'target_sequence': 20}]}},
        {'sequence': 20, 'step_name': "Retrieve Shared Health Record (SHR)", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/SHR/retrieve'}},
        {'sequence': 30, 'step_name': "Push Encounter to KHIE Platform", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'internal://khie/push_encounter'}},
        {'sequence': 40, 'step_name': "Trigger SHA Claims Processing", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/SHA/trigger_claim'}},
    ]
    for s in moh_steps: WorkflowStep.objects.create(service_config=service_moh, lifecycle_stage='to_be', **s)

    print("Successfully seeded Batch 2 (6 MDAs)")

if __name__ == "__main__":
    seed_batch_2()
