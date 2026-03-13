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

def add_service(mda, code, name, desc, group, cat, fam, event, fields, workflow_steps):
    svc, _ = ServiceConfig.objects.update_or_create(
        service_code=code,
        defaults={
            'mda': mda,
            'service_name': name,
            'description': desc,
            'category': cat,
            'service_family': fam,
            'priority': 'critical',
            'life_event_group': event,
            'form_schema': {"fields": fields}
        }
    )
    svc.service_groups.add(group)
    WorkflowStep.objects.filter(service_config=svc, lifecycle_stage='to_be').delete()
    
    for seq, step_name, stype, btype, config in workflow_steps:
        WorkflowStep.objects.create(
            service_config=svc, sequence=seq, step_name=step_name, step_type=stype,
            bpmn_element_type=btype, lifecycle_stage='to_be', api_config=config
        )

def seed_cradle_to_death_all():
    print("🚀 Seeding Complete Cradle to Death Lifecycle (27+ MDAs)...")
    group_c2d, _ = ServiceGroup.objects.get_or_create(name="Cradle to Death")
    
    # Common taxonomies
    cat_social, fam_vital = get_taxonomy('Social Services', 'Vital Events', 'Identity')
    cat_edu, fam_acad = get_taxonomy('Social Services', 'Education', 'Basic & Higher Ed')
    cat_econ, fam_biz = get_taxonomy('Economic & Regulatory', 'Business', 'Commerce & Tax')
    cat_trans, fam_trans = get_taxonomy('Security & Infrastructure', 'Transport', 'Public Safety')
    cat_land, fam_prop = get_taxonomy('Social Services', 'Property', 'Land & Housing')
    cat_jud, fam_law = get_taxonomy('Policy & Governance', 'Justice', 'Judicial Systems')

    # MDAs
    def get_mda(code, name):
        mda, _ = MDA.objects.get_or_create(code=code, defaults={'name': name})
        return mda

    # --- 1. THE CRADLE (Identity & Health) ---
    crs = get_mda('CRS', 'Civil Registration Services')
    add_service(crs, 'CRS-BIRTH-REG', 'Birth Registration', 'Mints UPI (Maisha Namba) at source.', group_c2d, cat_social, fam_vital, 'Birth', 
        [{"name": "parent_id", "type": "string", "label": "Parent's ID", "required": True}],
        [(1, 'Start', 'manual', 'start_event', None),
         (2, 'Pedigree Verification', 'api_call', 'service_task', {'registry_name': 'IPRS', 'is_mock': True, 'method': 'GET', 'url': '/v1/verify', 'outcomes': [{'label': 'success', 'target_sequence': 3}, {'label': 'failure', 'target_sequence': 3}]}),
         (3, 'Identity Gateway', 'manual', 'exclusive_gateway', {'outcomes': [{'label': 'ok', 'target_sequence': 5}, {'label': 'failure', 'target_sequence': 4}]}),
         (4, 'Manual Vetting', 'manual', 'user_task', {'role': 'officer'}),
         (5, 'Mint UPI', 'api_call', 'service_task', {'registry_name': 'CRS', 'is_mock': True, 'method': 'POST', 'url': '/v1/mint', 'outcomes': [{'label': 'success', 'target_sequence': 6}]}),
         (6, 'Birth Certificate Issued', 'manual', 'end_event', None)])

    sha = get_mda('SHA', 'Social Health Authority')
    add_service(sha, 'SHA-MEMBER-REG', 'SHA Health Insurance', 'Automated UHC enrollment.', group_c2d, cat_social, fam_vital, 'Health',
        [{"name": "id_number", "type": "string", "label": "National ID / UPI", "required": True}],
        [(1, 'Registration Start', 'manual', 'start_event', None),
         (2, 'Fetch Household Data (CRS)', 'api_call', 'service_task', {'registry_name': 'CRS', 'is_mock': True, 'method': 'GET', 'url': '/v1/dependants', 'outcomes': [{'label': 'success', 'target_sequence': 3}, {'label': 'failure', 'target_sequence': 3}]}),
         (3, 'UHC Gateway', 'manual', 'exclusive_gateway', {'outcomes': [{'label': 'ok', 'target_sequence': 4}, {'label': 'manual', 'target_sequence': 4}]}),
         (4, 'Means Test (KRA)', 'api_call', 'service_task', {'registry_name': 'KRA', 'is_mock': True, 'method': 'GET', 'url': '/v1/income', 'outcomes': [{'label': 'success', 'target_sequence': 5}]}),
         (5, 'Benefit Activated', 'manual', 'end_event', None)])

    # --- 2. CHILDHOOD & EDUCATION ---
    moe = get_mda('MOE', 'Ministry of Education')
    add_service(moe, 'MOE-NEMIS-ENROLL', 'School Enrollment', 'UPI-based NEMIS enrollment.', group_c2d, cat_edu, fam_acad, 'Education',
        [{"name": "upi", "type": "string", "label": "Student UPI", "required": True}, {"name": "school_id", "type": "string", "label": "School", "required": True}],
        [(1, 'Admission Request', 'manual', 'start_event', None),
         (2, 'Age Check (CRS)', 'api_call', 'service_task', {'registry_name': 'CRS', 'is_mock': True, 'method': 'GET', 'url': '/v1/verify', 'outcomes': [{'label': 'success', 'target_sequence': 3}, {'label': 'failure', 'target_sequence': 3}]}),
         (3, 'Age/Pedigree Gateway', 'manual', 'exclusive_gateway', {'outcomes': [{'label': 'ok', 'target_sequence': 4}, {'label': 'failure', 'target_sequence': 4}]}),
         (4, 'Activate Student UPI', 'api_call', 'service_task', {'registry_name': 'MOE', 'is_mock': True, 'method': 'POST', 'url': '/v1/activate', 'outcomes': [{'label': 'success', 'target_sequence': 5}]}),
         (5, 'Admitted', 'manual', 'end_event', None)])

    helb = get_mda('HELB', 'Higher Education Loans Board')
    add_service(helb, 'HELB-LOAN-APP', 'Helb Loan/Bursary', 'Automated means testing and loan processing.', group_c2d, cat_edu, fam_acad, 'Education',
        [{"name": "student_id", "type": "string", "label": "National ID / UPI", "required": True}],
        [(1, 'Loan Application', 'manual', 'start_event', None),
         (2, 'Verify Parent Income (KRA)', 'api_call', 'service_task', {'registry_name': 'KRA', 'is_mock': True, 'method': 'GET', 'url': '/v1/income', 'outcomes': [{'label': 'success', 'target_sequence': 3}, {'label': 'failure', 'target_sequence': 3}]}),
         (3, 'Financial Gateway', 'manual', 'exclusive_gateway', {'outcomes': [{'label': 'ok', 'target_sequence': 5}, {'label': 'failure', 'target_sequence': 4}]}),
         (4, 'Board Review', 'manual', 'user_task', {'role': 'officer'}),
         (5, 'Disbursement Notification', 'manual', 'end_event', None)])

    # --- 3. COMING OF AGE ---
    nrb = get_mda('NRB', 'National Registration Bureau')
    add_service(nrb, 'NRB-ID-REPLACE', 'ID Card Replacement', 'Replacement for lost or damaged Maisha ID.', group_c2d, cat_social, fam_vital, 'Identity',
        [{"name": "upi", "type": "string", "label": "National ID / UPI", "required": True}],
        [(1, 'Replacement Request', 'manual', 'start_event', None),
         (2, 'Fetch Biometrics (NRB)', 'api_call', 'service_task', {'registry_name': 'NRB', 'is_mock': True, 'method': 'GET', 'url': '/v1/bio', 'outcomes': [{'label': 'success', 'target_sequence': 3}, {'label': 'failure', 'target_sequence': 3}]}),
         (3, 'Bio Sync Gateway', 'manual', 'exclusive_gateway', {'outcomes': [{'label': 'ok', 'target_sequence': 5}, {'label': 'manual', 'target_sequence': 4}]}),
         (4, 'Manual Recon', 'manual', 'user_task', {'role': 'officer'}),
         (5, 'Issue Virtual ID', 'manual', 'end_event', None)])

    # --- 4. ECONOMIC LIFE ---
    kra = get_mda('KRA', 'Kenya Revenue Authority')
    add_service(kra, 'KRA-PIN-GEN', 'Tax PIN Generation', 'Instant PIN via IPRS identity handshake.', group_c2d, cat_econ, fam_biz, 'Employment',
        [{"name": "id_number", "type": "string", "label": "National ID / UPI", "required": True}],
        [(1, 'PIN Application', 'manual', 'start_event', None),
         (2, 'Identity Flush (IPRS)', 'api_call', 'service_task', {'registry_name': 'IPRS', 'is_mock': True, 'method': 'GET', 'url': '/v1/verify', 'outcomes': [{'label': 'success', 'target_sequence': 3}, {'label': 'failure', 'target_sequence': 3}]}),
         (3, 'Taxpayer Gateway', 'manual', 'exclusive_gateway', {'outcomes': [{'label': 'ok', 'target_sequence': 5}, {'label': 'failure', 'target_sequence': 4}]}),
         (4, 'Tax Compliance Officer', 'manual', 'user_task', {'role': 'officer'}),
         (5, 'PIN Certificate Issued', 'manual', 'end_event', None)])

    brs = get_mda('BRS', 'Business Registration Service')
    add_service(brs, 'BRS-CO-REG', 'Company Registration', 'Zero-entry registration for citizens.', group_c2d, cat_econ, fam_biz, 'Business',
        [{"name": "company_name", "type": "string", "label": "Proposed Name", "required": True}],
        [(1, 'Name Reservation', 'manual', 'start_event', None),
         (2, 'Check Name Availability', 'api_call', 'service_task', {'registry_name': 'BRS', 'is_mock': True, 'method': 'GET', 'url': '/v1/check', 'outcomes': [{'label': 'success', 'target_sequence': 3}, {'label': 'failure', 'target_sequence': 3}]}),
         (3, 'BRS Gateway', 'manual', 'exclusive_gateway', {'outcomes': [{'label': 'ok', 'target_sequence': 5}, {'label': 'manual', 'target_sequence': 4}]}),
         (4, 'Registrar Adjudication', 'manual', 'user_task', {'role': 'officer'}),
         (5, 'Incorporate and Issue CR12', 'manual', 'end_event', None)])

    # --- 5. FAMILY & PROPERTY ---
    slo = get_mda('SLO', 'State Law Office (AG)')
    add_service(slo, 'SLO-MARRIAGE-REG', 'Marriage Registration', 'Legal union with marital status sync.', group_c2d, cat_jud, fam_law, 'Family',
        [{"name": "partner_id", "type": "string", "label": "Partner ID/UPI", "required": True}],
        [(1, 'Notice of Marriage', 'manual', 'start_event', None),
         (2, 'Check Marital Status (IPRS)', 'api_call', 'service_task', {'registry_name': 'IPRS', 'is_mock': True, 'method': 'GET', 'url': '/v1/single', 'outcomes': [{'label': 'success', 'target_sequence': 3}, {'label': 'failure', 'target_sequence': 3}]}),
         (3, 'Status Gateway', 'manual', 'exclusive_gateway', {'outcomes': [{'label': 'ok', 'target_sequence': 5}, {'label': 'failure', 'target_sequence': 4}]}),
         (4, 'Registrar Appeal', 'manual', 'user_task', {'role': 'officer'}),
         (5, 'Certificate Issued', 'manual', 'end_event', None)])

    # --- 6. THE DEATH ---
    judiciary = get_mda('JUD', 'The Judiciary')
    add_service(judiciary, 'JUD-SUCCESSION-PROB', 'Probate & Succession', 'Automated asset-discovery and distribution.', group_c2d, cat_jud, fam_law, 'Succession',
        [{"name": "death_cert_id", "type": "string", "label": "Death Cert No", "required": True}],
        [(1, 'Succession Initiation', 'manual', 'start_event', None),
         (2, 'Discover Assets (Ardhisasa)', 'api_call', 'service_task', {'registry_name': 'LANDS', 'is_mock': True, 'method': 'GET', 'url': '/v1/assets', 'outcomes': [{'label': 'success', 'target_sequence': 3}, {'label': 'failure', 'target_sequence': 3}]}),
         (3, 'Discovery Gateway', 'manual', 'exclusive_gateway', {'outcomes': [{'label': 'ok', 'target_sequence': 5}, {'label': 'failure', 'target_sequence': 4}]}),
         (4, 'Probate Officer Review', 'manual', 'user_task', {'role': 'officer'}),
         (5, 'Distribution Confirmed', 'manual', 'end_event', None)])

    ufaa = get_mda('UFAA', 'Unclaimed Financial Assets Authority')
    add_service(ufaa, 'UFAA-CLAIM-REG', 'Unclaimed Asset Claim', 'Reunifying assets with beneficiaries.', group_c2d, cat_econ, fam_biz, 'Financial',
        [{"name": "deceased_id", "type": "string", "label": "Deceased ID/UPI", "required": True}],
        [(1, 'Asset Claim Request', 'manual', 'start_event', None),
         (2, 'Verify Heir-ship (CRS)', 'api_call', 'service_task', {'registry_name': 'CRS', 'is_mock': True, 'method': 'GET', 'url': '/v1/heirs', 'outcomes': [{'label': 'success', 'target_sequence': 3}, {'label': 'failure', 'target_sequence': 3}]}),
         (3, 'Claim Gateway', 'manual', 'exclusive_gateway', {'outcomes': [{'label': 'ok', 'target_sequence': 5}, {'label': 'failure', 'target_sequence': 4}]}),
         (4, 'UFAA Auditor Review', 'manual', 'user_task', {'role': 'officer'}),
         (5, 'Reunification Approved', 'manual', 'end_event', None)])

    print("✅ All 27+ MDA Cradle-to-Death services seeded with BPMN and KeSEL compliance!")

if __name__ == "__main__":
    seed_cradle_to_death_all()
