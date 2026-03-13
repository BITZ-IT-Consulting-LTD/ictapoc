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

def seed_education_batch():
    print("Seeding Cradle to Death: Batch 2 (Education)...")
    
    cradle_group, _ = ServiceGroup.objects.get_or_create(name="Cradle to Death")
    
    # 5. Ministry of Education (MOE)
    moe_mda, _ = MDA.objects.get_or_create(
        code='MOE',
        defaults={'name': 'Ministry of Education', 'description': 'National education management.'}
    )
    cat_edu, fam_edu = get_taxonomy('Social Services', 'Education', 'Education & Skills Development')
    
    nemis_enroll, _ = ServiceConfig.objects.update_or_create(
        service_code='MOE-NEMIS-ENROLL',
        defaults={
            'mda': moe_mda,
            'service_name': 'School Enrollment (NEMIS)',
            'description': 'Parent-led school enrollment via UPI (Maisha Namba).',
            'category': cat_edu,
            'service_family': fam_edu,
            'priority': 'critical',
            'life_event_group': 'Education',
            'form_schema': {
                "fields": [
                    {"name": "child_upi", "type": "string", "label": "Child's Maisha Namba (UPI)", "required": True},
                    {"name": "school_code", "type": "string", "label": "Preferred School Code", "required": True}
                ]
            }
        }
    )
    nemis_enroll.service_groups.add(cradle_group)
    
    WorkflowStep.objects.filter(service_config=nemis_enroll, lifecycle_stage='to_be').delete()
    moe_steps = [
        ('Fetch Child Bio-data (CRS)', 'api_call', 'service_task', {'url': 'internal://crs/fetch-profile', 'method': 'GET', 'is_mock': True}),
        ('Verify School Capacity', 'api_call', 'service_task', {'url': 'internal://moe/school/capacity', 'method': 'GET', 'is_mock': True}),
        ('Head Teacher Approval', 'manual', 'user_task', {}),
        ('Activate Student & Trigger Capitation', 'api_call', 'service_task', {'url': 'internal://moe/nemis/activate', 'method': 'POST', 'is_mock': True}),
    ]
    for i, (name, stype, btype, config) in enumerate(moe_steps, 1):
        WorkflowStep.objects.create(
            service_config=nemis_enroll,
            step_name=name,
            step_type=stype,
            bpmn_element_type=btype,
            lifecycle_stage='to_be',
            sequence=i,
            api_config=config if stype == 'api_call' else None
        )

    # 6. KNEC
    knec_mda, _ = MDA.objects.get_or_create(
        code='KNEC',
        defaults={'name': 'Kenya National Examinations Council', 'description': 'National exam administration.'}
    )
    
    exam_reg, _ = ServiceConfig.objects.update_or_create(
        service_code='KNEC-EXAM-REG',
        defaults={
            'mda': knec_mda,
            'service_name': 'National Exam Registration',
            'description': 'Automated exam registration for eligible NEMIS students.',
            'category': cat_edu,
            'service_family': fam_edu,
            'priority': 'critical',
            'life_event_group': 'Education',
            'form_schema': {
                "fields": [
                    {"name": "student_upi", "type": "string", "label": "Student Maisha Namba (UPI)", "required": True},
                    {"name": "exam_id", "type": "string", "label": "Examination ID (KPSEA/KCSE)", "required": True}
                ]
            }
        }
    )
    exam_reg.service_groups.add(cradle_group)
    
    WorkflowStep.objects.filter(service_config=exam_reg, lifecycle_stage='to_be').delete()
    knec_steps = [
        ('Verify Eligibility via NEMIS', 'api_call', 'service_task', {'url': 'internal://moe/nemis/verify-eligibility', 'method': 'GET', 'is_mock': True}),
        ('Issue Exam Index Number', 'api_call', 'service_task', {'url': 'internal://knec/exam/issue-index', 'method': 'POST', 'is_mock': True}),
        ('Issue Results & Digital Certificate', 'api_call', 'service_task', {'url': 'internal://knec/exam/issue-certificate', 'method': 'POST', 'is_mock': True}),
    ]
    for i, (name, stype, btype, config) in enumerate(knec_steps, 1):
        WorkflowStep.objects.create(
            service_config=exam_reg,
            step_name=name,
            step_type=stype,
            bpmn_element_type=btype,
            lifecycle_stage='to_be',
            sequence=i,
            api_config=config if stype == 'api_call' else None
        )

    # 7. KUCCPS
    kuccps_mda, _ = MDA.objects.get_or_create(
        code='KUCCPS',
        defaults={'name': 'KUCCPS', 'description': 'Tertiary placement coordination.'}
    )
    
    placement_service, _ = ServiceConfig.objects.update_or_create(
        service_code='KUCCPS-PLACEMENT',
        defaults={
            'mda': kuccps_mda,
            'service_name': 'University/TVET Placement',
            'description': 'Algorithmic placement into higher learning institutions.',
            'category': cat_edu,
            'service_family': fam_edu,
            'priority': 'critical',
            'life_event_group': 'Education',
            'form_schema': {
                "fields": [
                    {"name": "student_upi", "type": "string", "label": "Student Maisha Namba (UPI)", "required": True},
                    {"name": "course_preferences", "type": "array", "label": "Course Preferences", "required": True}
                ]
            }
        }
    )
    placement_service.service_groups.add(cradle_group)
    
    WorkflowStep.objects.filter(service_config=placement_service, lifecycle_stage='to_be').delete()
    kuccps_steps = [
        ('Fetch KCSE Results (KNEC)', 'api_call', 'service_task', {'url': 'internal://knec/results/fetch', 'method': 'GET', 'is_mock': True}),
        ('AI Course Recommendation', 'api_call', 'service_task', {'url': 'internal://kuccps/ai/recommend', 'method': 'POST', 'is_mock': True}),
        ('Algorithmic Placement Decision', 'api_call', 'service_task', {'url': 'internal://kuccps/algorithmic/placement', 'method': 'POST', 'is_mock': True}),
        ('Push Results to HELB', 'api_call', 'service_task', {'url': 'internal://helb/loan/initiate', 'method': 'POST', 'is_mock': True}),
    ]
    for i, (name, stype, btype, config) in enumerate(kuccps_steps, 1):
        WorkflowStep.objects.create(
            service_config=placement_service,
            step_name=name,
            step_type=stype,
            bpmn_element_type=btype,
            lifecycle_stage='to_be',
            sequence=i,
            api_config=config if stype == 'api_call' else None
        )

    # 8. HELB
    helb_mda, _ = MDA.objects.get_or_create(
        code='HELB',
        defaults={'name': 'HELB', 'description': 'Education finance provider.'}
    )
    cat_fin, fam_fin = get_taxonomy('Economic Services', 'Finance', 'Education & Skills Development')
    
    loan_service, _ = ServiceConfig.objects.update_or_create(
        service_code='HELB-AUTO-LOAN',
        defaults={
            'mda': helb_mda,
            'service_name': 'Higher Education Loan (Automated)',
            'description': 'API-driven loan assessment and smart-contract disbursement.',
            'category': cat_fin,
            'service_family': fam_fin,
            'priority': 'critical',
            'life_event_group': 'Education',
            'form_schema': {
                "fields": [
                    {"name": "student_upi", "type": "string", "label": "Student Maisha Namba (UPI)", "required": True}
                ]
            }
        }
    )
    loan_service.service_groups.add(cradle_group)
    
    WorkflowStep.objects.filter(service_config=loan_service, lifecycle_stage='to_be').delete()
    helb_steps = [
        ('Fetch Admission details (KUCCPS)', 'api_call', 'service_task', {'url': 'internal://kuccps/admission/fetch', 'method': 'GET', 'is_mock': True}),
        ('Auto-Fetch Parent Income (KRA)', 'api_call', 'service_task', {'url': 'internal://kra/income/fetch-parent', 'method': 'GET', 'is_mock': True}),
        ('AI Loan Assessment', 'api_call', 'service_task', {'url': 'internal://helb/ai/allocate', 'method': 'POST', 'is_mock': True}),
        ('Smart Contract Disbursement', 'api_call', 'service_task', {'url': 'internal://payment/smart-disburse', 'method': 'POST', 'is_mock': True}),
    ]
    for i, (name, stype, btype, config) in enumerate(helb_steps, 1):
        WorkflowStep.objects.create(
            service_config=loan_service,
            step_name=name,
            step_type=stype,
            bpmn_element_type=btype,
            lifecycle_stage='to_be',
            sequence=i,
            api_config=config if stype == 'api_call' else None
        )

    print("Batch 2 Seeded successfully!")

if __name__ == "__main__":
    seed_education_batch()
