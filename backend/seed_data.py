import os
import django
import json
from datetime import timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth import get_user_model
from service_api.models import MDA, ServiceConfig, WorkflowStep, ServiceRequest, Role, ServiceFamily
from service_api.utils.taxonomies import KENYA_COUNTIES, BUSINESS_TYPES, APPLICATION_TYPES_ID

User = get_user_model()

def seed_data():
    print("Seeding core government data...")

    # 0. Create Service Families
    families = {
        'Civil Registration & Identity': {
            'description': 'Services related to citizen lifecycle records and identity issuance.',
            'shared_form_schema': {
                'type': 'object',
                'properties': {
                    'maisha_number': {'type': 'string', 'title': 'National ID / Maisha Number', 'lookup_service': 'IPRS'}
                }
            }
        },
        'Business & Revenue': {
            'description': 'Services for commercial entities, tax registration and business licensing.',
            'shared_form_schema': {
                'type': 'object',
                'properties': {
                    'kra_pin': {'type': 'string', 'title': 'KRA PIN Number', 'lookup_service': 'KRA'}
                }
            }
        },
        'Social Services & Education': {
            'description': 'Citizen support services, education grants and community programs.',
        },
        'Government Administration (G2G)': {
            'description': 'Internal government processes, inter-departmental memos and cabinet submissions.',
        }
    }
    
    for name, data in families.items():
        ServiceFamily.objects.update_or_create(
            name=name,
            defaults={
                'description': data.get('description'),
                'shared_form_schema': data.get('shared_form_schema')
            }
        )
        print(f"Ensured Service Family: {name}")

    # 1. Create Roles with fixed GLOBAL authorizations
    roles = {
        'admin': {
            'description': 'Global System Administrator', 
            'permissions': ['all', 'global_view', 'global_manage', 'reports_view']
        },
        'mda_admin': {
            'description': 'MDA Level Administrator', 
            'permissions': ['mda_view', 'mda_manage_users', 'mda_manage_services', 'reports_view', 'request_action']
        },
        'supervisor': {
            'description': 'Departmental Supervisor / Approver', 
            'permissions': ['mda_view', 'request_action', 'request_approve', 'reports_view']
        },
        'officer': {
            'description': 'Standard Desk Officer', 
            'permissions': ['mda_view', 'request_action']
        },
        'citizen': {
            'description': 'Public User / Citizen', 
            'permissions': ['request_create', 'request_view_own', 'saved_docs_manage']
        },
        'GLOBAL_OFFICER': {
            'description': 'Universal Service Officer (All MDAs)', 
            'permissions': ['global_view', 'request_action']
        },
        'GLOBAL_SUPERVISOR': {
            'description': 'Universal Supervisor (All MDAs)', 
            'permissions': ['global_view', 'request_action', 'request_approve', 'reports_view']
        },
    }
    
    for r_name, r_data in roles.items():
        role_obj, created = Role.objects.get_or_create(name=r_name, defaults=r_data)
        if not created:
             role_obj.permissions = r_data['permissions']
             role_obj.save()
        print(f"Ensured Role: {r_name}")

    # 2. Create Priority MDAs
    mdas_data = [
        {'name': 'Ministry of Interior', 'code': 'MOI', 'is_priority': True},
        {'name': 'Department of Immigration Services', 'code': 'DIS', 'is_priority': True},
        {'name': 'Business Registration Service', 'code': 'BRS', 'is_priority': True},
        {'name': 'National Registration Bureau', 'code': 'NRB', 'is_priority': True},
        {'name': 'Kenya Revenue Authority', 'code': 'KRA', 'is_priority': True},
        {'name': 'ICT Authority', 'code': 'ICTA', 'is_priority': True},
    ]
    
    for m_data in mdas_data:
        MDA.objects.get_or_create(code=m_data['code'], defaults=m_data)
        print(f"Ensured MDA: {m_data['code']}")

    print("Core Seeding complete!")

if __name__ == "__main__":
    seed_data()
