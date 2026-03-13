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

def seed_economic_batch():
    print("Seeding Cradle to Death: Batch 3 (Economic Life)...")
    
    cradle_group, _ = ServiceGroup.objects.get_or_create(name="Cradle to Death")
    
    # 9. NRB
    nrb_mda, _ = MDA.objects.get_or_create(
        code='NRB',
        defaults={'name': 'National Registration Bureau', 'description': 'Adult identity management.'}
    )
    cat_id, fam_id = get_taxonomy('Social Services', 'Identity', 'Identity & Civil Registration')
    
    id_upgrade, _ = ServiceConfig.objects.update_or_create(
        service_code='NRB-ID-UPGRADE',
        defaults={
            'mda': nrb_mda,
            'service_name': 'Adult ID Upgrade (Biometric)',
            'description': 'Transition from Child UPI to Adult ID with biometric capture.',
            'category': cat_id,
            'service_family': fam_id,
            'priority': 'critical',
            'life_event_group': 'Identity',
            'form_schema': {
                "fields": [
                    {"name": "child_upi", "type": "string", "label": "Child's Maisha Namba (UPI)", "required": True},
                    {"name": "photo", "type": "file", "label": "Recent Photo", "required": True}
                ]
            }
        }
    )
    id_upgrade.service_groups.add(cradle_group)
    
    WorkflowStep.objects.filter(service_config=id_upgrade, lifecycle_stage='to_be').delete()
    nrb_steps = [
        ('Verify UPI Data (CRS)', 'api_call', 'service_task', {'url': 'internal://crs/verify-upi', 'method': 'GET', 'is_mock': True}),
        ('Auto-Vet Citizenship', 'api_call', 'service_task', {'url': 'internal://nrb/auto-vet', 'method': 'POST', 'is_mock': True}),
        ('Capture Biometrics at Hub', 'manual', 'user_task', {}),
        ('Issue Virtual Adult ID', 'api_call', 'service_task', {'url': 'internal://maisha/issue-virtual-id', 'method': 'POST', 'is_mock': True}),
    ]
    for i, (name, stype, btype, config) in enumerate(nrb_steps, 1):
        WorkflowStep.objects.create(
            service_config=id_upgrade,
            step_name=name,
            step_type=stype,
            bpmn_element_type=btype,
            lifecycle_stage='to_be',
            sequence=i,
            api_config=config if stype == 'api_call' else None
        )

    # 10. Immigration
    imm_mda, _ = MDA.objects.get_or_create(
        code='IMM',
        defaults={'name': 'Immigration', 'description': 'Travel document issuance.'}
    )
    cat_travel, fam_travel = get_taxonomy('Social Services', 'Identity', 'Identity & Travel')
    
    passport_service, _ = ServiceConfig.objects.update_or_create(
        service_code='IMM-PASSPORT-SMART',
        defaults={
            'mda': imm_mda,
            'service_name': 'E-Passport Application (Optimized)',
            'description': 'Smart passport application using existing NRB biometrics.',
            'category': cat_travel,
            'service_family': fam_travel,
            'priority': 'critical',
            'life_event_group': 'Identity',
            'form_schema': {
                "fields": [
                    {"name": "id_number", "type": "string", "label": "National ID / Maisha Namba", "required": True}
                ]
            }
        }
    )
    passport_service.service_groups.add(cradle_group)
    
    WorkflowStep.objects.filter(service_config=passport_service, lifecycle_stage='to_be').delete()
    imm_steps = [
        ('Verify Identity (IPRS)', 'api_call', 'service_task', {'url': 'internal://iprs/verify', 'method': 'GET', 'is_mock': True}),
        ('Fetch Biometrics (NRB)', 'api_call', 'service_task', {'url': 'internal://nrb/biometrics/fetch', 'method': 'GET', 'is_mock': True}),
        ('Automated Production Queue', 'api_call', 'service_task', {'url': 'internal://imm/production/queue', 'method': 'POST', 'is_mock': True}),
    ]
    for i, (name, stype, btype, config) in enumerate(imm_steps, 1):
        WorkflowStep.objects.create(
            service_config=passport_service,
            step_name=name,
            step_type=stype,
            bpmn_element_type=btype,
            lifecycle_stage='to_be',
            sequence=i,
            api_config=config if stype == 'api_call' else None
        )

    # 11. NTSA
    ntsa_mda, _ = MDA.objects.get_or_create(
        code='NTSA',
        defaults={'name': 'NTSA', 'description': 'Transport management.'}
    )
    cat_trans, fam_trans = get_taxonomy('Service Management', 'Licensing', 'Transport & Mobility')
    
    dl_renewal, _ = ServiceConfig.objects.update_or_create(
        service_code='NTSA-DL-RENEW-1CLICK',
        defaults={
            'mda': ntsa_mda,
            'service_name': '1-Click DL Renewal',
            'description': 'Proactive Driving License renewal via eCitizen SSO.',
            'category': cat_trans,
            'service_family': fam_trans,
            'priority': 'critical',
            'life_event_group': 'Travel',
            'form_schema': {
                "fields": [
                    {"name": "license_number", "type": "string", "label": "License Number", "required": True}
                ]
            }
        }
    )
    dl_renewal.service_groups.add(cradle_group)
    
    WorkflowStep.objects.filter(service_config=dl_renewal, lifecycle_stage='to_be').delete()
    ntsa_steps = [
        ('Proactive Expiry Alert', 'api_call', 'service_task', {'url': 'internal://notify/dl-expiry', 'method': 'POST', 'is_mock': True}),
        ('Compliance Check (Judiciary)', 'api_call', 'service_task', {'url': 'internal://compliance/check-fines', 'method': 'GET', 'is_mock': True}),
        ('Update DL Registry', 'api_call', 'service_task', {'url': 'internal://ntsa/dl/renew', 'method': 'POST', 'is_mock': True}),
        ('Issue Digital DL to Wallet', 'api_call', 'service_task', {'url': 'internal://maisha/dl/issue', 'method': 'POST', 'is_mock': True}),
    ]
    for i, (name, stype, btype, config) in enumerate(ntsa_steps, 1):
        WorkflowStep.objects.create(
            service_config=dl_renewal,
            step_name=name,
            step_type=stype,
            bpmn_element_type=btype,
            lifecycle_stage='to_be',
            sequence=i,
            api_config=config if stype == 'api_call' else None
        )

    # 12. KRA
    kra_mda, _ = MDA.objects.get_or_create(
        code='KRA',
        defaults={'name': 'KRA', 'description': 'Revenue collection.'}
    )
    cat_tax, fam_tax = get_taxonomy('Economic Services', 'Taxation', 'Taxation & Revenue Administration')
    
    pin_reg, _ = ServiceConfig.objects.update_or_create(
        service_code='KRA-PIN-AUTO',
        defaults={
            'mda': kra_mda,
            'service_name': 'Zero-Touch PIN Registration',
            'description': 'Automated KRA PIN generation upon identity event.',
            'category': cat_tax,
            'service_family': fam_tax,
            'priority': 'critical',
            'life_event_group': 'Identity',
            'form_schema': {"fields": [{"name": "id_number", "type": "string", "label": "ID Number", "required": True}]}
        }
    )
    pin_reg.service_groups.add(cradle_group)
    
    WorkflowStep.objects.filter(service_config=pin_reg, lifecycle_stage='to_be').delete()
    WorkflowStep.objects.create(
        service_config=pin_reg,
        step_name='Generate PIN via X-Road',
        step_type='api_call',
        bpmn_element_type='service_task',
        lifecycle_stage='to_be',
        sequence=1,
        api_config={'url': 'internal://kra/pin/generate', 'method': 'POST', 'is_mock': True}
    )

    # 13. BRS
    brs_mda, _ = MDA.objects.get_or_create(
        code='BRS',
        defaults={'name': 'BRS', 'description': 'Business registration.'}
    )
    cat_bus, fam_bus = get_taxonomy('Economic Services', 'Business', 'Business & Commercial Regulation')
    
    company_reg, _ = ServiceConfig.objects.update_or_create(
        service_code='BRS-CO-REG-AI',
        defaults={
            'mda': brs_mda,
            'service_name': 'Algorithmic Company Registration',
            'description': 'AI-assisted instant company incorporation.',
            'category': cat_bus,
            'service_family': fam_bus,
            'priority': 'critical',
            'life_event_group': 'Business',
            'form_schema': {"fields": [{"name": "proposed_name", "type": "string", "label": "Company Name", "required": True}]}
        }
    )
    company_reg.service_groups.add(cradle_group)
    
    WorkflowStep.objects.filter(service_config=company_reg, lifecycle_stage='to_be').delete()
    brs_steps = [
        ('AI Name Search', 'api_call', 'service_task', {'url': 'internal://brs/ai/name-search', 'method': 'POST', 'is_mock': True}),
        ('Verify Director (IPRS)', 'api_call', 'service_task', {'url': 'internal://iprs/verify', 'method': 'GET', 'is_mock': True}),
        ('Director Consent (App)', 'manual', 'user_task', {}),
        ('Issue Bundled Certificates', 'api_call', 'service_task', {'url': 'internal://brs/bundle/issue', 'method': 'POST', 'is_mock': True}),
    ]
    for i, (name, stype, btype, config) in enumerate(brs_steps, 1):
        WorkflowStep.objects.create(
            service_config=company_reg,
            step_name=name,
            step_type=stype,
            bpmn_element_type=btype,
            lifecycle_stage='to_be',
            sequence=i,
            api_config=config if stype == 'api_call' else None
        )

    # 14. NSSF
    nssf_mda, _ = MDA.objects.get_or_create(
        code='NSSF',
        defaults={'name': 'NSSF', 'description': 'Social security.'}
    )
    cat_social, fam_social = get_taxonomy('Social Services', 'Welfare', 'Social Protection')
    
    nssf_reg, _ = ServiceConfig.objects.update_or_create(
        service_code='NSSF-AUTO-REG',
        defaults={
            'mda': nssf_mda,
            'service_name': 'Automated NSSF Registration',
            'description': 'Event-driven pension fund enrollment.',
            'category': cat_social,
            'service_family': fam_social,
            'priority': 'critical',
            'life_event_group': 'Employment',
            'form_schema': {"fields": [{"name": "id_number", "type": "string", "label": "ID Number", "required": True}]}
        }
    )
    nssf_reg.service_groups.add(cradle_group)
    
    WorkflowStep.objects.filter(service_config=nssf_reg, lifecycle_stage='to_be').delete()
    WorkflowStep.objects.create(
        service_config=nssf_reg,
        step_name='Generate NSSF Number',
        step_type='api_call',
        bpmn_element_type='service_task',
        lifecycle_stage='to_be',
        sequence=1,
        api_config={'url': 'internal://nssf/number/generate', 'method': 'POST', 'is_mock': True}
    )

    print("Batch 3 Seeded successfully!")

if __name__ == "__main__":
    seed_economic_batch()
