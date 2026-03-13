import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep, ServiceCategory, ServiceDomain, ServiceFamily, ServiceGroup, User
from django.db import transaction

@transaction.atomic
def seed_batch_1():
    # Helper to get/create common taxonomy
    def get_taxonomy(domain_name, category_name, family_name, group_name):
        domain, _ = ServiceDomain.objects.get_or_create(name=domain_name)
        category, _ = ServiceCategory.objects.get_or_create(name=category_name, domain=domain)
        family, _ = ServiceFamily.objects.get_or_create(name=family_name)
        group, _ = ServiceGroup.objects.get_or_create(name=group_name)
        return category, family, group

    # 1. Agriculture and Food Authority (AFA)
    mda_afa, _ = MDA.objects.update_or_create(
        code="AFA",
        defaults={'name': "Agriculture and Food Authority", 'is_priority': True}
    )
    cat, fam, grp = get_taxonomy("Economic & Regulatory", "Agricultural Licensing", "Trade & Commerce", "Employment & Business")
    service_afa, _ = ServiceConfig.objects.update_or_create(
        service_code="AFA-LIC-001",
        defaults={
            'service_name': "Farmer Registration & Licensing",
            'description': "Automated licensing for farmers and traders via KIAMIS and Huduma Bridge.",
            'mda': mda_afa,
            'category': cat,
            'service_family': fam,
            'service_type': 'G2B',
            'is_public_facing': True,
            'form_schema': {
                "fields": [
                    {"name": "license_type", "label": "License Type", "type": "select", "options": ["Trading", "Export", "Import"], "required": True},
                    {"name": "business_reg_no", "label": "BRS Registration Number", "type": "text", "required": True},
                    {"name": "kra_pin", "label": "KRA PIN", "type": "text", "required": True},
                    {"name": "kiamis_id", "label": "KIAMIS Farmer ID", "type": "text", "required": False}
                ]
            }
        }
    )
    service_afa.service_groups.add(grp)
    WorkflowStep.objects.filter(service_config=service_afa).delete()
    afa_steps = [
        {'sequence': 10, 'step_name': "Validate BRS Registration", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/BRS/validate', 'outcomes': [{'label': 'success', 'target_sequence': 20}, {'label': 'failure', 'target_sequence': 11}]}},
        {'sequence': 11, 'step_name': "[Fallback] Physical BRS Verification", 'step_type': 'manual', 'bpmn_element_type': 'user_task', 'role': 'AFA_OFFICER', 'api_config': {'outcomes': [{'label': 'verified', 'target_sequence': 20}]}},
        {'sequence': 20, 'step_name': "Validate KRA Tax Compliance", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/KRA/validate', 'outcomes': [{'label': 'compliant', 'target_sequence': 30}, {'label': 'non_compliant', 'target_sequence': 21}]}},
        {'sequence': 21, 'step_name': "[Fallback] Manual Compliance Review", 'step_type': 'manual', 'bpmn_element_type': 'user_task', 'role': 'AFA_OFFICER', 'api_config': {'outcomes': [{'label': 'cleared', 'target_sequence': 30}]}},
        {'sequence': 30, 'step_name': "Retrieve KIAMIS Farmer Data", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/KIAMIS/fetch', 'outcomes': [{'label': 'exists', 'target_sequence': 40}, {'label': 'not_found', 'target_sequence': 31}]}},
        {'sequence': 31, 'step_name': "[Fallback] Manual Farmer Onboarding", 'step_type': 'manual', 'bpmn_element_type': 'user_task', 'role': 'AFA_OFFICER', 'api_config': {'outcomes': [{'label': 'onboarded', 'target_sequence': 40}]}},
        {'sequence': 40, 'step_name': "Run Risk Assessment", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'internal://afa/risk_engine', 'outcomes': [{'label': 'low_risk', 'target_sequence': 70}, {'label': 'medium_risk', 'target_sequence': 50}, {'label': 'high_risk', 'target_sequence': 60}]}},
        {'sequence': 50, 'step_name': "Officer Technical Review", 'step_type': 'manual', 'bpmn_element_type': 'user_task', 'role': 'AFA_OFFICER', 'api_config': {'outcomes': [{'label': 'approve', 'target_sequence': 70}, {'label': 'needs_insp', 'target_sequence': 60}]}},
        {'sequence': 60, 'step_name': "Schedule & Conduct Physical Inspection", 'step_type': 'manual', 'bpmn_element_type': 'user_task', 'role': 'AFA_INSPECTOR', 'api_config': {'outcomes': [{'label': 'pass', 'target_sequence': 70}, {'label': 'fail', 'target_sequence': None}]}},
        {'sequence': 70, 'step_name': "Generate Digital License", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'internal://output/gen_license', 'outcomes': [{'label': 'generated', 'target_sequence': 80}]}},
        {'sequence': 80, 'step_name': "Sync with Kentrade Single Window", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/KENTRADE/sync', 'outcomes': [{'label': 'synced', 'target_sequence': None}]}},
    ]
    for s in afa_steps: WorkflowStep.objects.create(service_config=service_afa, lifecycle_stage='to_be', **s)

    # 2. Assets Recovery Agency (ARA)
    mda_ara, _ = MDA.objects.update_or_create(
        code="ARA",
        defaults={'name': "Assets Recovery Agency", 'is_priority': True}
    )
    cat, fam, grp = get_taxonomy("Policy & Governance", "Asset Recovery", "Justice & Security", "Social Protection & Justice")
    service_ara, _ = ServiceConfig.objects.update_or_create(
        service_code="ARA-REC-001",
        defaults={
            'service_name': "Asset Identification & Preservation",
            'description': "Real-time asset tracing and digital preservation via Huduma Bridge.",
            'mda': mda_ara,
            'category': cat,
            'service_family': fam,
            'service_type': 'G2G',
            'is_public_facing': False,
            'form_schema': {
                "fields": [
                    {"name": "suspect_id", "label": "Suspect Maisha Namba / PIN", "type": "text", "required": True},
                    {"name": "case_reference", "label": "Case Reference Number", "type": "text", "required": True},
                    {"name": "referring_agency", "label": "Referring Agency (DCI/EACC)", "type": "text", "required": True}
                ]
            }
        }
    )
    service_ara.service_groups.add(grp)
    WorkflowStep.objects.filter(service_config=service_ara).delete()
    ara_steps = [
        {'sequence': 10, 'step_name': "Parallel Asset Discovery (Lands/NTSA/BRS)", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/TRACE/all', 'outcomes': [{'label': 'found', 'target_sequence': 20}, {'label': 'not_found', 'target_sequence': 11}]}},
        {'sequence': 11, 'step_name': "[Fallback] Manual Field Verification", 'step_type': 'manual', 'bpmn_element_type': 'user_task', 'role': 'ARA_INVESTIGATOR', 'api_config': {'outcomes': [{'label': 'found', 'target_sequence': 20}]}},
        {'sequence': 20, 'step_name': "Generate Unified Asset Map (AI)", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'internal://ara/asset_map'}},
        {'sequence': 30, 'step_name': "Compile NPKI-Signed Evidence Packet", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'internal://trust/sign_packet'}},
        {'sequence': 40, 'step_name': "Auto-file Preservation Motion (Judiciary)", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/JUDICIARY/file', 'outcomes': [{'label': 'filed', 'target_sequence': 50}, {'label': 'fail', 'target_sequence': 41}]}},
        {'sequence': 41, 'step_name': "[Fallback] Manual Court Filing Liaison", 'step_type': 'manual', 'bpmn_element_type': 'user_task', 'role': 'ARA_LEGAL_OFFICER', 'api_config': {'outcomes': [{'label': 'filed', 'target_sequence': 50}]}},
        {'sequence': 50, 'step_name': "Place Digital 'Caution' on Registries", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/FREEZE/all'}},
    ]
    for s in ara_steps: WorkflowStep.objects.create(service_config=service_ara, lifecycle_stage='to_be', **s)

    # 3. Athi Water Works (AWWDA)
    mda_awwda, _ = MDA.objects.update_or_create(
        code="AWWDA",
        defaults={'name': "Athi Water Works Development Agency", 'is_priority': True}
    )
    cat, fam, grp = get_taxonomy("Social & Citizen Services", "Water Infrastructure", "Infrastructure & Energy", "Retirement & Legacy")
    service_awwda, _ = ServiceConfig.objects.update_or_create(
        service_code="AWWDA-INF-001",
        defaults={
            'service_name': "Infrastructure Project Lifecycle",
            'description': "End-to-end management from GIS planning to IoT commissioning.",
            'mda': mda_awwda,
            'category': cat,
            'service_family': fam,
            'service_type': 'G2C',
            'is_public_facing': False,
            'form_schema': {
                "fields": [
                    {"name": "project_name", "label": "Project Name", "type": "text", "required": True},
                    {"name": "gis_location", "label": "GIS Coordinates", "type": "text", "required": True},
                    {"name": "budget_code", "label": "IFMIS Budget Code", "type": "text", "required": True}
                ]
            }
        }
    )
    service_awwda.service_groups.add(grp)
    WorkflowStep.objects.filter(service_config=service_awwda).delete()
    awwda_steps = [
        {'sequence': 10, 'step_name': "GIS Master Plan Alignment Check", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'internal://gis/check_alignment'}},
        {'sequence': 20, 'step_name': "Auto-Task ESIA (NEMA) & Technical Review", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/NEMA/esia_request'}},
        {'sequence': 30, 'step_name': "Integrated e-Tendering (IFMIS)", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/IFMIS/tender'}},
        {'sequence': 40, 'step_name': "Resident Engineer Mobile Logging", 'step_type': 'manual', 'bpmn_element_type': 'user_task', 'role': 'RESIDENT_ENGINEER'},
        {'sequence': 50, 'step_name': "IoT Sensor Flow/Pressure Verification", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'internal://iot/verify'}},
        {'sequence': 60, 'step_name': "Auto-Generate Interim Payment Certificate", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'internal://pms/gen_ipc'}},
    ]
    for s in awwda_steps: WorkflowStep.objects.create(service_config=service_awwda, lifecycle_stage='to_be', **s)

    # 4. Cabinet Office
    # (Using the Presidency MDA created earlier if exists, or presidency code)
    mda_cab, _ = MDA.objects.update_or_create(
        code="CABINET",
        defaults={'name': "State Department for Cabinet Affairs", 'is_priority': True}
    )
    cat, fam, grp = get_taxonomy("Policy & Governance", "Executive Decisions", "Governance & Policy", "Social Protection & Justice")
    service_cab, _ = ServiceConfig.objects.update_or_create(
        service_code="CAB-MEMO-001",
        defaults={
            'service_name': "Cabinet Memorandum Processing",
            'description': "Secure digital drafting and parallel inter-ministerial review.",
            'mda': mda_cab,
            'category': cat,
            'service_family': fam,
            'service_type': 'G2G',
            'is_public_facing': False,
            'form_schema': {
                "fields": [
                    {"name": "memo_title", "label": "Memorandum Title", "type": "text", "required": True},
                    {"name": "fiscal_impact", "label": "National Treasury Fiscal Impact", "type": "textarea", "required": True},
                    {"name": "legal_implications", "label": "Attorney General Legal Opinion", "type": "textarea", "required": True}
                ]
            }
        }
    )
    service_cab.service_groups.add(grp)
    WorkflowStep.objects.filter(service_config=service_cab).delete()
    cab_steps = [
        {'sequence': 10, 'step_name': "Digitally Sign via CS NPKI", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'internal://trust/sign_memo'}},
        {'sequence': 20, 'step_name': "Parallel Routing to AG & Treasury", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/CABINET/route', 'outcomes': [{'label': 'routed', 'target_sequence': 30}]}},
        {'sequence': 30, 'step_name': "Mandatory Legal Review (AG)", 'step_type': 'manual', 'bpmn_element_type': 'user_task', 'role': 'AG_OFFICER'},
        {'sequence': 40, 'step_name': "Mandatory Fiscal Review (Treasury)", 'step_type': 'manual', 'bpmn_element_type': 'user_task', 'role': 'TREASURY_OFFICER'},
        {'sequence': 50, 'step_name': "AI-Assisted Feedback Consolidation", 'step_type': 'manual', 'bpmn_element_type': 'user_task', 'role': 'CABINET_AFFAIRS_OFFICER'},
        {'sequence': 60, 'step_name': "Auto-Sync to GDMIS for Tracking", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/GDMIS/sync'}},
    ]
    for s in cab_steps: WorkflowStep.objects.create(service_config=service_cab, lifecycle_stage='to_be', **s)

    # 5. Culture & Heritage (Ushanga)
    mda_cult, _ = MDA.objects.update_or_create(
        code="CULTURE",
        defaults={'name': "State Department for Culture, Arts and Heritage", 'is_priority': True}
    )
    cat, fam, grp = get_taxonomy("Social & Citizen Services", "Creative Economy", "Arts & Culture", "Employment & Business")
    service_ushanga, _ = ServiceConfig.objects.update_or_create(
        service_code="USH-KEN-001",
        defaults={
            'service_name': "Ushanga Kenya Digital Value Chain",
            'description': "Traceable beadwork inventory and automated artisan payments.",
            'mda': mda_cult,
            'category': cat,
            'service_family': fam,
            'service_type': 'G2B',
            'is_public_facing': True,
            'form_schema': {
                "fields": [
                    {"name": "coop_reg_no", "label": "Cooperative Registration (BRS)", "type": "text", "required": True},
                    {"name": "product_category", "label": "Product Type", "type": "select", "options": ["Necklace", "Bracelet", "Belt", "Bag"], "required": True},
                    {"name": "artisan_id", "label": "Artisan Maisha Namba", "type": "text", "required": True}
                ]
            }
        }
    )
    service_ushanga.service_groups.add(grp)
    WorkflowStep.objects.filter(service_config=service_ushanga).delete()
    ushanga_steps = [
        {'sequence': 10, 'step_name': "Digital Product Intake & Coop Check", 'step_type': 'manual', 'bpmn_element_type': 'user_task', 'role': 'USHANGA_CENTER_OFFICER'},
        {'sequence': 20, 'step_name': "AI-Assisted Grading & Human QA", 'step_type': 'manual', 'bpmn_element_type': 'user_task', 'role': 'USHANGA_QA_OFFICER'},
        {'sequence': 30, 'step_name': "Generate Unique QR Product Identity", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'internal://inventory/gen_qr'}},
        {'sequence': 40, 'step_name': "Automated Payment Split (GPA)", 'step_type': 'api_call', 'bpmn_element_type': 'service_task', 'role': 'system', 'api_config': {'url': 'HUDUMA_BRIDGE/GPA/split_payment'}},
    ]
    for s in ushanga_steps: WorkflowStep.objects.create(service_config=service_ushanga, lifecycle_stage='to_be', **s)

    print("Successfully seeded Batch 1 (5 MDAs)")

if __name__ == "__main__":
    seed_batch_1()
