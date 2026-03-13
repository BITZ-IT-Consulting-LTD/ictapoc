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

def seed_cradle_batch():
    print("Seeding Cradle to Death: Batch 1 (The Cradle)...")
    
    cradle_group, _ = ServiceGroup.objects.get_or_create(name="Cradle to Death")
    
    # 1. Civil Registration Services (CRS)
    crs_mda, _ = MDA.objects.get_or_create(
        code='CRS',
        defaults={'name': 'Civil Registration Services', 'description': 'Custodian of vital life events.'}
    )
    
    cat, fam = get_taxonomy('Social Services', 'Vital Events', 'Identity & Civil Registration')
    
    # Birth Registration
    birth_reg, _ = ServiceConfig.objects.update_or_create(
        service_code='CRS-BIRTH-REG',
        defaults={
            'mda': crs_mda,
            'service_name': 'Birth Registration',
            'description': 'Event-driven birth registration and UPI (Maisha Namba) minting.',
            'category': cat,
            'service_family': fam,
            'priority': 'critical',
            'life_event_group': 'Birth',
            'form_schema': {
                "fields": [
                    {"name": "child_name", "type": "string", "label": "Full Name of Child", "required": True},
                    {"name": "birth_date", "type": "date", "label": "Date of Birth", "required": True},
                    {"name": "hospital_name", "type": "string", "label": "Hospital/Facility Name", "required": True},
                    {"name": "parent1_id", "type": "string", "label": "Mother's National ID / Maisha Namba", "required": True},
                    {"name": "parent2_id", "type": "string", "label": "Father's National ID / Maisha Namba", "required": False}
                ]
            }
        }
    )
    birth_reg.service_groups.add(cradle_group)
    
    WorkflowStep.objects.filter(service_config=birth_reg, lifecycle_stage='to_be').delete()
    
    steps = [
        ('Verify Parents Identity', 'api_call', 'service_task', {
            'url': 'internal://iprs/verify-identity',
            'method': 'POST',
            'is_mock': True
        }),
        ('Identity Verification Check', 'manual', 'exclusive_gateway', {}),
        ('[TBD: Manual Review Required] - Parent Verification Failed', 'manual', 'user_task', {}),
        ('Mint Maisha Namba (UPI)', 'api_call', 'service_task', {
            'url': 'internal://crs/mint-upi',
            'method': 'POST',
            'is_mock': True
        }),
        ('Auto-Enroll in SHA (Social Health Authority)', 'api_call', 'service_task', {
            'url': 'internal://sha/auto-enroll',
            'method': 'POST',
            'is_mock': True
        }),
        ('Issue Digital Birth Certificate', 'api_call', 'service_task', {
            'url': 'internal://notification/send-certificate',
            'method': 'POST',
            'is_mock': True
        }),
    ]
    
    for i, (name, stype, btype, config) in enumerate(steps, 1):
        WorkflowStep.objects.create(
            service_config=birth_reg,
            step_name=name,
            step_type=stype,
            bpmn_element_type=btype,
            lifecycle_stage='to_be',
            sequence=i,
            api_config=config if stype == 'api_call' else None
        )

    # 2. MOH
    moh_mda, _ = MDA.objects.get_or_create(
        code='MOH',
        defaults={'name': 'Ministry of Health', 'description': 'Health management.'}
    )
    cat_health, fam_health = get_taxonomy('Social Services', 'Health', 'Health & Public Health Regulation')
    
    hie_service, _ = ServiceConfig.objects.update_or_create(
        service_code='MOH-KHIE-SYNC',
        defaults={
            'mda': moh_mda,
            'service_name': 'Health Information Exchange (KHIE)',
            'description': 'Unified patient identity and Shared Health Record (SHR) management.',
            'category': cat_health,
            'service_family': fam_health,
            'priority': 'critical',
            'life_event_group': 'Health',
            'form_schema': {
                "fields": [
                    {"name": "patient_id", "type": "string", "label": "Maisha Namba / National ID", "required": True},
                    {"name": "facility_id", "type": "string", "label": "Health Facility Code", "required": True}
                ]
            }
        }
    )
    hie_service.service_groups.add(cradle_group)
    
    WorkflowStep.objects.filter(service_config=hie_service, lifecycle_stage='to_be').delete()
    moh_steps = [
        ('Identify Patient (MPI)', 'api_call', 'service_task', {'url': 'internal://khie/mpi/search', 'method': 'GET', 'is_mock': True}),
        ('Retrieve Shared Health Record', 'api_call', 'service_task', {'url': 'internal://khie/shr/retrieve', 'method': 'GET', 'is_mock': True}),
        ('Record Clinical Encounter', 'manual', 'user_task', {}),
        ('Update National SHR', 'api_call', 'service_task', {'url': 'internal://khie/shr/update', 'method': 'POST', 'is_mock': True}),
    ]
    for i, (name, stype, btype, config) in enumerate(moh_steps, 1):
        WorkflowStep.objects.create(
            service_config=hie_service,
            step_name=name,
            step_type=stype,
            bpmn_element_type=btype,
            lifecycle_stage='to_be',
            sequence=i,
            api_config=config if stype == 'api_call' else None
        )

    # 4. SHA
    sha_mda, _ = MDA.objects.get_or_create(
        code='SHA',
        defaults={'name': 'Social Health Authority', 'description': 'Universal Health Coverage.'}
    )
    cat_sha, fam_sha = get_taxonomy('Social Services', 'Insurance', 'Social Protection & Welfare')
    
    sha_reg, _ = ServiceConfig.objects.update_or_create(
        service_code='SHA-AUTO-ENROLL',
        defaults={
            'mda': sha_mda,
            'service_name': 'Automated Health Insurance Enrollment',
            'description': 'Proactive enrollment and means testing for UHC.',
            'category': cat_sha,
            'service_family': fam_sha,
            'priority': 'critical',
            'life_event_group': 'Health',
            'form_schema': {
                "fields": [
                    {"name": "id_number", "type": "string", "label": "National ID / Maisha Namba", "required": True}
                ]
            }
        }
    )
    sha_reg.service_groups.add(cradle_group)
    
    WorkflowStep.objects.filter(service_config=sha_reg, lifecycle_stage='to_be').delete()
    sha_steps = [
        ('Fetch Bio-data from IPRS', 'api_call', 'service_task', {'url': 'internal://iprs/fetch-profile', 'method': 'GET', 'is_mock': True}),
        ('Auto-Link Dependants (CRS)', 'api_call', 'service_task', {'url': 'internal://crs/fetch-dependants', 'method': 'GET', 'is_mock': True}),
        ('Means Testing Assessment (KRA)', 'api_call', 'service_task', {'url': 'internal://kra/fetch-income', 'method': 'GET', 'is_mock': True}),
        ('Activate SHA Coverage', 'api_call', 'service_task', {'url': 'internal://sha/activate-coverage', 'method': 'POST', 'is_mock': True}),
    ]
    for i, (name, stype, btype, config) in enumerate(sha_steps, 1):
        WorkflowStep.objects.create(
            service_config=sha_reg,
            step_name=name,
            step_type=stype,
            bpmn_element_type=btype,
            lifecycle_stage='to_be',
            sequence=i,
            api_config=config if stype == 'api_call' else None
        )

    print("Batch 1 Seeded successfully!")

if __name__ == "__main__":
    seed_cradle_batch()
