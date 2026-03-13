import os
import django
from django.db import transaction
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep, ServiceCategory, ServiceFamily, ServiceGroup, ServiceDomain
from django.contrib.auth import get_user_model

User = get_user_model()

def get_taxonomy(domain_name, category_name, family_name):
    domain, _ = ServiceDomain.objects.get_or_create(name=domain_name)
    category, _ = ServiceCategory.objects.get_or_create(name=category_name, domain=domain)
    family, _ = ServiceFamily.objects.get_or_create(name=family_name)
    return category, family

def seed_family_and_end_batch():
    print("Seeding Cradle to Death: Batch 4 (Family & The End)...")
    
    cradle_group, _ = ServiceGroup.objects.get_or_create(name="Cradle to Death")
    
    # 15. AG Marriage
    ag_mda, _ = MDA.objects.get_or_create(
        code='AG',
        defaults={'name': 'Attorney General', 'description': 'Legal services & public trust.'}
    )
    cat_legal, fam_legal = get_taxonomy('Social Services', 'Family', 'Justice & Legal Services')
    
    marriage_reg, _ = ServiceConfig.objects.update_or_create(
        service_code='AG-MARRIAGE-DIGITAL',
        defaults={
            'mda': ag_mda,
            'service_name': 'Marriage Registration (Digital)',
            'description': 'Joint digital notice and automated marriage license issuance.',
            'category': cat_legal,
            'service_family': fam_legal,
            'priority': 'critical',
            'life_event_group': 'Family',
            'form_schema': {"fields": [{"name": "spouse_id", "type": "string", "label": "Spouse ID", "required": True}]}
        }
    )
    marriage_reg.service_groups.add(cradle_group)
    
    WorkflowStep.objects.filter(service_config=marriage_reg, lifecycle_stage='to_be').delete()
    ag_steps = [
        ('Verify Marital Status (IPRS)', 'api_call', 'service_task', {'url': 'internal://iprs/verify-marital', 'method': 'GET', 'is_mock': True}),
        ('Publish e-Gazette Notice', 'api_call', 'service_task', {'url': 'internal://egazette/publish', 'method': 'POST', 'is_mock': True}),
        ('Officiant Solemnization (QR)', 'manual', 'user_task', {}),
        ('Issue Digital Certificate', 'api_call', 'service_task', {'url': 'internal://maisha/marriage/issue', 'method': 'POST', 'is_mock': True}),
    ]
    for i, (name, stype, btype, config) in enumerate(ag_steps, 1):
        WorkflowStep.objects.create(
            service_config=marriage_reg,
            step_name=name,
            step_type=stype,
            bpmn_element_type=btype,
            lifecycle_stage='to_be',
            sequence=i,
            api_config=config if stype == 'api_call' else None
        )

    # 16. Lands
    lands_mda, _ = MDA.objects.get_or_create(
        code='LANDS',
        defaults={'name': 'Ministry of Lands', 'description': 'Lands management.'}
    )
    cat_land, fam_land = get_taxonomy('Economic Services', 'Property', 'Land, Housing & Property Administration')
    
    property_transfer, _ = ServiceConfig.objects.update_or_create(
        service_code='LANDS-TRANSFER-SMART',
        defaults={
            'mda': lands_mda,
            'service_name': 'Property Transfer (Smart)',
            'description': 'Ardhisasa-based property transfer with biometric consent.',
            'category': cat_land,
            'service_family': fam_land,
            'priority': 'critical',
            'life_event_group': 'Property',
            'form_schema': {"fields": [{"name": "parcel_id", "type": "string", "label": "Parcel ID", "required": True}]}
        }
    )
    property_transfer.service_groups.add(cradle_group)
    
    WorkflowStep.objects.filter(service_config=property_transfer, lifecycle_stage='to_be').delete()
    lands_steps = [
        ('Biometric Consent', 'manual', 'user_task', {}),
        ('Verify Parcel Status', 'api_call', 'service_task', {'url': 'internal://lands/verify-parcel', 'method': 'GET', 'is_mock': True}),
        ('Integrate Stamp Duty (KRA)', 'api_call', 'service_task', {'url': 'internal://kra/pay-stamp', 'method': 'POST', 'is_mock': True}),
        ('Execute transfer via Smart Contract', 'api_call', 'service_task', {'url': 'internal://lands/transfer/execute', 'method': 'POST', 'is_mock': True}),
        ('Issue Verifiable Digital Title', 'api_call', 'service_task', {'url': 'internal://maisha/title/issue', 'method': 'POST', 'is_mock': True}),
    ]
    for i, (name, stype, btype, config) in enumerate(lands_steps, 1):
        WorkflowStep.objects.create(
            service_config=property_transfer,
            step_name=name,
            step_type=stype,
            bpmn_element_type=btype,
            lifecycle_stage='to_be',
            sequence=i,
            api_config=config if stype == 'api_call' else None
        )

    # 17. Judiciary
    judiciary_mda, _ = MDA.objects.get_or_create(
        code='JUDICIARY',
        defaults={'name': 'The Judiciary', 'description': 'Legal justice system.'}
    )
    cat_jud, fam_jud = get_taxonomy('Social Services', 'Justice', 'Justice & Legal Services')
    
    succession_service, _ = ServiceConfig.objects.update_or_create(
        service_code='JUD-SUCCESSION-AUTO',
        defaults={
            'mda': judiciary_mda,
            'service_name': 'Succession & Probate (Automated)',
            'description': 'Proactive succession initiation and asset discovery.',
            'category': cat_jud,
            'service_family': fam_jud,
            'priority': 'critical',
            'life_event_group': 'Death',
            'form_schema': {"fields": [{"name": "deceased_id", "type": "string", "label": "Deceased ID", "required": True}]}
        }
    )
    succession_service.service_groups.add(cradle_group)
    
    WorkflowStep.objects.filter(service_config=succession_service, lifecycle_stage='to_be').delete()
    succession_steps = [
        ('Automated Asset Discovery', 'api_call', 'service_task', {'url': 'internal://xroad/asset-discovery', 'method': 'GET', 'is_mock': True}),
        ('Digital e-Gazette Pub', 'api_call', 'service_task', {'url': 'internal://egazette/publish', 'method': 'POST', 'is_mock': True}),
        ('Probate AI Validation', 'api_call', 'service_task', {'url': 'internal://judiciary/ai/validate', 'method': 'POST', 'is_mock': True}),
        ('Issue Digital Grant', 'api_call', 'service_task', {'url': 'internal://maisha/probate/issue', 'method': 'POST', 'is_mock': True}),
    ]
    for i, (name, stype, btype, config) in enumerate(succession_steps, 1):
        WorkflowStep.objects.create(
            service_config=succession_service,
            step_name=name,
            step_type=stype,
            bpmn_element_type=btype,
            lifecycle_stage='to_be',
            sequence=i,
            api_config=config if stype == 'api_call' else None
        )

    # 18. UFAA
    ufaa_mda, _ = MDA.objects.get_or_create(
        code='UFAA',
        defaults={'name': 'UFAA', 'description': 'Unclaimed assets.'}
    )
    cat_ufaa, fam_ufaa = get_taxonomy('Economic Services', 'Finance', 'Social Protection & Welfare')
    
    ufaa_claim, _ = ServiceConfig.objects.update_or_create(
        service_code='UFAA-CLAIM-PROACTIVE',
        defaults={
            'mda': ufaa_mda,
            'service_name': 'Proactive Asset Reunification',
            'description': 'UFAA claim processing using Judiciary and IPRS API verification.',
            'category': cat_ufaa,
            'service_family': fam_ufaa,
            'priority': 'critical',
            'life_event_group': 'Death',
            'form_schema': {"fields": [{"name": "deceased_id", "type": "string", "label": "Original Owner ID", "required": True}]}
        }
    )
    ufaa_claim.service_groups.add(cradle_group)
    
    WorkflowStep.objects.filter(service_config=ufaa_claim, lifecycle_stage='to_be').delete()
    ufaa_steps = [
        ('Verify Probate (Judiciary)', 'api_call', 'service_task', {'url': 'internal://judiciary/probate/verify', 'method': 'GET', 'is_mock': True}),
        ('Instant Digital Payout', 'api_call', 'service_task', {'url': 'internal://payment/instant', 'method': 'POST', 'is_mock': True}),
    ]
    for i, (name, stype, btype, config) in enumerate(ufaa_steps, 1):
        WorkflowStep.objects.create(
            service_config=ufaa_claim,
            step_name=name,
            step_type=stype,
            bpmn_element_type=btype,
            lifecycle_stage='to_be',
            sequence=i,
            api_config=config if stype == 'api_call' else None
        )

    print("Batch 4 Seeded successfully!")

if __name__ == "__main__":
    seed_family_and_end_batch()
