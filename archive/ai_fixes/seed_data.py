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
    print("Seeding data...")

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
        },
        'System Operations': {
            'description': 'Platform management and base infrastructure services.',
        }
    }
    
    created_families = {}
    for name, data in families.items():
        fam, created = ServiceFamily.objects.update_or_create(
            name=name,
            defaults={
                'description': data.get('description'),
                'shared_form_schema': data.get('shared_form_schema')
            }
        )
        created_families[name] = fam
        print(f"Ensured Service Family: {name}")

    # 1. Create Roles
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
        'registrar': {
            'description': 'Civil Registrar', 
            'permissions': ['mda_view', 'request_action', 'request_approve']
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
    
    role_objects = {}
    for r_name, r_data in roles.items():
        role_obj, created = Role.objects.get_or_create(name=r_name, defaults=r_data)
        if not created:
             role_obj.permissions = r_data['permissions']
             role_obj.save()
        role_objects[r_name] = role_obj
        print(f"Ensured Role: {r_name}")

    # 1. Create MDAs
    mdas_data = [
        {
            'name': 'Ministry of Interior', 
            'code': 'MOI',
            'description': 'Responsible for state security and correctional services.',
            'head_of_mda': 'Hon. John Doe',
            'contact_email': 'contact@interior.go.ke',
            'contact_phone': '+254700000001',
            'website': 'https://www.interior.go.ke',
            'address': 'Harambee House, Nairobi'
        },
        {
            'name': 'Department of Immigration Services', 
            'code': 'DIS',
            'description': 'Passports, Visas, and Citizenship.',
            'head_of_mda': 'Director Jane Smith',
            'contact_email': 'help@immigration.go.ke',
            'contact_phone': '+254700000002',
            'website': 'https://www.immigration.go.ke',
            'address': 'Nyayo House, Nairobi'
        },
        {
            'name': 'Business Registration Service', 
            'code': 'BRS',
            'description': 'Registration of companies and businesses.',
            'head_of_mda': 'Registrar Robert Brown',
            'contact_email': 'info@brs.go.ke',
            'contact_phone': '+254700000003',
            'website': 'https://www.brs.go.ke',
            'address': 'Sheria House, Nairobi'
        },
        {
            'name': 'National Registration Bureau', 
            'code': 'NRB',
            'description': 'Issuance of National Identity Cards and identity management.',
            'head_of_mda': 'Director of Registration',
            'contact_email': 'nrb@interior.go.ke',
            'address': 'NSSF Building, Nairobi'
        },
        {
            'name': 'Kenya Revenue Authority', 
            'code': 'KRA',
            'description': 'Assessment and collection of taxes and border control.',
            'head_of_mda': 'Commissioner General',
            'contact_email': 'itax@kra.go.ke',
            'contact_phone': '+254700000005',
            'website': 'https://itax.kra.go.ke',
            'address': 'Times Tower, Nairobi'
        },
        {
            'name': 'Ministry of Education', 
            'code': 'MOE',
            'description': 'Responsible for national education policy and leadership.',
            'head_of_mda': 'Cabinet Secretary',
            'contact_email': 'info@education.go.ke',
            'website': 'https://www.education.go.ke',
            'address': 'Jogoo House, Nairobi'
        },
    ]
    
    # Priority MDAs extracted from the blueprints
    mdas_data.extend([
        {
            'name': 'Ministry of Youth Affairs, Creative Economy and Sports',
            'code': 'MOYACES',
            'description': 'Empowering youth and promoting sports and creative economy.',
            'head_of_mda': 'Cabinet Secretary',
        },
        {
            'name': 'Ministry of Information, Communications and the Digital Economy',
            'code': 'MICDE',
            'description': 'Responsible for ICT policy, implementation, and digital economy.',
            'head_of_mda': 'Cabinet Secretary',
        },
        {
            'name': 'Executive Office of the President',
            'code': 'EOP',
            'description': 'Top executive management, national coordination.',
            'head_of_mda': 'Chief of Staff',
        },
        {
            'name': 'Ministry of Environment, Climate Change and Forestry',
            'code': 'MOECCF',
            'description': 'Protection, conservation and management of environment.',
            'head_of_mda': 'Cabinet Secretary',
        },
        {
            'name': 'STATE DEPARTMENT FOR IMMIGRATION AND CITIZEN SERVICES',
            'code': 'SDICS',
            'description': 'Immigration, passports, visas, and citizen services.',
            'head_of_mda': 'Principal Secretary',
        },
        {
            'name': 'Ministry of Public Service, Gender and Affirmative Action',
            'code': 'MPSGA',
            'description': 'Public service management, gender equality, and affirmative action.',
            'head_of_mda': 'Cabinet Secretary',
        },
        {
            'name': 'Agriculture and Food Authority',
            'code': 'AFA',
            'description': 'Regulation and promotion of agricultural products.',
            'head_of_mda': 'Director General',
        },
        {
            'name': 'Office of the Attorney General',
            'code': 'OAG',
            'description': 'Principal legal adviser to the Government.',
            'head_of_mda': 'Attorney General',
        },
        {
            'name': 'Ministry of Water, Sanitation and Irrigation',
            'code': 'MOWSI',
            'description': 'Water resources management, sanitation and irrigation.',
            'head_of_mda': 'Cabinet Secretary',
        },
        {
            'name': 'Ministry of Energy and Petroleum',
            'code': 'MOEP',
            'description': 'Energy policy formulation and sector regulation.',
            'head_of_mda': 'Cabinet Secretary',
        },
        {
            'name': 'Ministry of Labour and Social Protection',
            'code': 'MOLSP',
            'description': 'Labor relations, social security and protection.',
            'head_of_mda': 'Cabinet Secretary',
        },
        {
            'name': 'Ministry of Co-operatives and MSMEs',
            'code': 'MOCM',
            'description': 'Cooperatives development and MSME promotion.',
            'head_of_mda': 'Cabinet Secretary',
        },
        {
            'name': 'Ministry of Interior and National Administration',
            'code': 'MINA',
            'description': 'Internal security, state functions, and national administration.',
            'head_of_mda': 'Cabinet Secretary',
        },
        {
            'name': 'MINISTRY OF HEALTH',
            'code': 'MOH',
            'description': 'Health policy, national hospitals, and public health.',
            'head_of_mda': 'Cabinet Secretary',
        }
    ])


    created_mdas = {}
    for m_data in mdas_data:
        mda, created = MDA.objects.update_or_create(
            code=m_data['code'], 
            defaults={
                'name': m_data['name'], 
                'description': m_data.get('description'),
                'head_of_mda': m_data.get('head_of_mda'),
                'contact_email': m_data.get('contact_email'),
                'contact_phone': m_data.get('contact_phone'),
                'website': m_data.get('website'),
                'address': m_data.get('address'),
            }
        )
        created_mdas[mda.name] = mda
        print(f"Ensured MDA: {mda.name}")

    # 2. Create Users
    users = [
        {
            'username': 'admin', 
            'email': 'admin@example.com', 
            'first_name': 'System',
            'last_name': 'Administrator',
            'role': 'admin', 
            'rbac': 'admin', 
            'is_staff': True, 
            'is_superuser': True
        },
        {
            'username': 'citizen1', 
            'email': 'citizen1@example.com', 
            'first_name': 'James',
            'last_name': 'Bond',
            'role': 'citizen', 
            'rbac': 'citizen',
            'id_number': '12345678',

            'saved_documents': [
                {
                    "name": "Birth Certificate",
                    "type": "AUTHORITATIVE_OUTPUT",
                    "doctype": "BIRTH_CERTIFICATE",
                    "authoritative_id": "BEN-TEST-2026",
                    "issued_by": "Civil Registration Services",
                    "issued_to": "James Bond Standard",
                    "issue_date": "2026-02-01",
                    "metadata": {
                        "ben": "BEN-TEST-2026",
                        "full_name": "James Bond Standard",
                        "mother_name": "Molly Mother",
                        "mother_id": "ID-MOTHER-001",
                        "father_name": "Frank Father",
                        "father_id": "ID-FATHER-001",
                        "date_of_birth": "2000-01-01",
                        "county": "Nairobi City",
                        "place_of_birth": "Nairobi Hospital",
                        "digital_signature": "SIG-CRS-998877665544"
                    }
                },
                {
                    "name": "NEMIS Card",
                    "type": "AUTHORITATIVE_OUTPUT",
                    "doctype": "NEMIS_CARD",
                    "authoritative_id": "UPI-88877766",
                    "issued_by": "Ministry of Education",
                    "issued_to": "James Bond Standard",
                    "issue_date": "2026-02-05",
                    "metadata": {
                        "upi": "UPI-88877766",
                        "institution": "University of Nairobi",
                        "digital_signature": "SIG-MOE-1122334455"
                    }
                }
            ]
        },
        {
            'username': 'maggy1', 
            'email': 'maggy1@example.com', 
            'first_name': 'Maggy',
            'last_name': 'One',
            'role': 'citizen', 
            'rbac': 'citizen',
            'id_number': '555555',
            'saved_documents': [
                {
                    "name": "Birth Certificate",
                    "type": "AUTHORITATIVE_OUTPUT",
                    "doctype": "BIRTH_CERTIFICATE",
                    "authoritative_id": "BEN-MAGGY",
                    "issued_by": "Civil Registration Services",
                    "issued_to": "Maggy One",
                    "issue_date": "2026-01-15",
                    "metadata": {
                        "ben": "BEN-MAGGY",
                        "full_name": "Maggy One",
                        "mother_name": "Mama Maggy",
                        "mother_id": "8888",
                        "father_name": "Baba Maggy",
                        "father_id": "9999",
                        "date_of_birth": "1995-10-20",
                        "county": "Kisumu",
                        "place_of_birth": "Kisumu General Hospital",
                        "digital_signature": "SIG-CRS-MAGGY-123"
                    }
                }
            ]
        },
        {
            'username': 'mary',
            'email': 'mary@example.com',
            'first_name': 'Mary',
            'last_name': 'Mother',
            'role': 'citizen',
            'rbac': 'citizen',
            'id_number': 'ID-MOTHER-001'
        },
        {
            'username': 'joseph',
            'email': 'joseph@example.com',
            'first_name': 'Joseph',
            'last_name': 'Father',
            'role': 'citizen',
            'rbac': 'citizen',
            'id_number': 'ID-FATHER-001'
        },

        {
            'username': 'officer1', 
            'email': 'officer1@example.com', 
            'first_name': 'Officer',
            'last_name': 'One',
            'role': 'officer', 
            'rbac': 'officer',
            'mda_name': 'Ministry of Interior'
        },
        {
            'username': 'officer2', 
            'email': 'officer2@example.com', 
            'first_name': 'Officer',
            'last_name': 'Two',
            'role': 'officer', 
            'rbac': 'registrar',
            'mda_name': 'Ministry of Interior'
        },
        {
            'username': 'supervisor1', 
            'email': 'supervisor1@example.com', 
            'first_name': 'Supervisor',
            'last_name': 'One',
            'role': 'supervisor', 
            'rbac': 'supervisor',
            'mda_name': 'Ministry of Interior'
        },

    ]

    for u_data in users:
        defaults = {
            'email': u_data['email'], 
            'first_name': u_data.get('first_name', ''),
            'last_name': u_data.get('last_name', ''),
            'role': u_data['role'],
            'id_number': u_data.get('id_number'),
        }

        if u_data.get('is_staff'):
            defaults['is_staff'] = True
        if u_data.get('is_superuser'):
            defaults['is_superuser'] = True
        
        # Link MDA
        if u_data.get('mda_name'):
            defaults['mda'] = created_mdas.get(u_data['mda_name'])

        # Link RBAC Role
        rbac_role = role_objects.get(u_data.get('rbac', 'citizen'))
        defaults['user_role'] = rbac_role

        user, created = User.objects.get_or_create(username=u_data['username'], defaults=defaults)
        
        if created:
            user.set_password('Starten1@')
            user.save()
            print(f"Created user: {user.username}")
        else:
            user.user_role = rbac_role
            user.first_name = u_data.get('first_name', user.first_name)
            user.last_name = u_data.get('last_name', user.last_name)
            if u_data.get('id_number'):
                user.id_number = u_data['id_number']
            if u_data.get('mda_name'):
                user.mda = created_mdas.get(u_data['mda_name'])
            if u_data.get('saved_documents'):
                user.saved_documents = u_data['saved_documents']
            user.save()

            if u_data.get('is_superuser') and not user.is_superuser:
                user.is_staff = True
                user.is_superuser = True
                user.save()
            print(f"User {user.username} exists, updated role/mda.")

    # 3. Create Service Configs
    services = [
        {
            'service_code': 'ONBOARD',
            'service_name': 'Platform Onboarding',
            'mda': 'Ministry of Interior',
            'family': 'System Operations',
            'config': {
                'description': 'Onboard from legacy systems to the Digital Maisha Platform.',
            }
        },
        {
            'service_code': 'BIRTH_REG',
            'service_name': 'Birth Registration & Issuance',
            'mda': 'Ministry of Interior',
            'family': 'Civil Registration & Identity',
            'config': {
                "rules": {
                    "schema": {
                        "type": "object",
                        "title": "Application for Registration of Birth",
                        "properties": {
                            "header_0": {"type": "section_header", "title": "0. Registration Type"},
                            "reg_type": {
                                "type": "string",
                                "title": "Registration Scenario",
                                "enum": ["Hospital Birth (Standard)", "Home Birth (Requires Chief Letter)", "Late Registration (>6 months)"],
                                "widget": "select"
                            },
                            
                            "header_1": {"type": "section_header", "title": "1. Child's Details"},
                            "child_full_name": {"type": "string", "title": "Child's Full Name"},
                            "date_of_birth": {"type": "string", "format": "date", "title": "Date of Birth"},
                            "sex": {"type": "string", "title": "Sex", "enum": ["Male", "Female"], "widget": "radio"},
                            "birth_notification_no": {"type": "string", "title": "Birth Notification Number (from Hospital)"},
                            
                            "header_2": {"type": "section_header", "title": "2. Parents' Identity"},
                            "mother_id": {
                                "type": "string", 
                                "title": "Mother's National ID",
                                "description": "Mandatory. Enter ID to fetch details.",
                                "lookup_service": "IPRS",
                                "lookup_action": "fetch"
                            },
                            "mother_name": {"type": "string", "title": "Mother's Full Name (Auto-filled)"},
                            "father_id": {
                                "type": "string", 
                                "title": "Father's National ID (Optional)",
                                "description": "Enter ID to fetch details if available.",
                                "lookup_service": "IPRS",
                                "lookup_action": "fetch"
                            },
                            "father_name": {"type": "string", "title": "Father's Full Name (Auto-filled)"},
                            
                            "header_3": {"type": "section_header", "title": "3. Location & Verification"},
                            "place_of_birth": {"type": "string", "title": "Facility / Village Name"},
                            "county": {"type": "string", "title": "County", "enum": KENYA_COUNTIES, "widget": "select"},
                            
                            "header_4": {"type": "section_header", "title": "4. Evidence Uploads"},
                            "birth_notification_scan": {"type": "string", "title": "Birth Notification (Hospital)", "format": "data-url"},
                            "chief_letter_scan": {"type": "string", "title": "Chief's Letter (For Home Births)", "format": "data-url"},
                            "parents_id_scans": {"type": "string", "title": "Parents' IDs (Combined Scan)", "format": "data-url"},
                            "clinic_card_scan": {"type": "string", "title": "Clinic/Immunization Card (For Late Reg)", "format": "data-url"}
                        },
                        "required": ["reg_type", "child_full_name", "date_of_birth", "mother_id", "county"]
                    },
                    "workflow": [
                        {"sequence": 1, "step_name": "Submission", "step_type": "manual", "role": "citizen", "action": "submit"},
                        {"sequence": 2, "step_name": "Identity Verification (IPRS)", "step_type": "api_call", "action": "verify", "api_config": {"url": "HUDUMA_BRIDGE/IPRS/verify"}},
                        {"sequence": 3, "step_name": "Birth Records Search (CRS)", "step_type": "api_call", "action": "verify", "api_config": {"url": "HUDUMA_BRIDGE/CRS/verify"}},
                        {"sequence": 4, "step_name": "Officer Review & Vetting", "step_type": "manual", "role": "officer", "action": "verify"},
                        {"sequence": 5, "step_name": "Civil Registrar Approval", "step_type": "manual", "role": "supervisor", "action": "approve"},
                        {"sequence": 6, "step_name": "BEN Generation (Registry Entry)", "step_type": "api_call", "action": "archive", "api_config": {"url": "KESEL_BRIDGE/EDRMS/archive"}},
                        {"sequence": 7, "step_name": "Certificate Printing", "step_type": "manual", "role": "officer", "action": "print"},
                        {"sequence": 8, "step_name": "Digital Issuance (Wallet)", "step_type": "manual", "role": "registrar", "action": "issue"}
                    ]
                },
                "output": "Authoritative Birth Certificate"
            }
        },
        {
            'service_code': 'PASSPORT_APP',
            'service_name': 'Passport Application',
            'mda': 'Department of Immigration Services',
            'family': 'Civil Registration & Identity',
            'config': {
                "rules": {
                    "schema": {
                        "type": "object",
                        "title": "Passport Application Form",
                        "properties": {
                            "id_number": {"type": "string", "title": "National ID Number"},
                            "full_name": {"type": "string", "title": "Full Name"},
                            "travel_reason": {"type": "string", "title": "Reason for Travel"},
                            "passport_type": {
                                "type": "string", 
                                "title": "Passport Type", 
                                "enum": ["Ordinary", "Diplomatic", "East African"]
                            }
                        },
                        "required": ["id_number", "full_name", "passport_type"]
                    }
                },
                "sla": 10,
                "output": "Passport"
            }
        },
        {
            'service_code': 'BIZ_INCORPORATION',
            'service_name': 'Business Incorporation (Ltd/BN)',
            'mda': 'Business Registration Service',
            'family': 'Business & Revenue',
            'config': {
                "rules": {
                    "schema": {
                        "type": "object",
                        "title": "Application for Business Incorporation",
                        "properties": {
                            "header_1": {"type": "section_header", "title": "1. Business Type & Names"},
                            "business_type": {
                                "type": "string",
                                "title": "Legal Structure",
                                "enum": ["Business Name (Sole Prop)", "Private Limited Company (Ltd)", "Public Limited Company (PLC)", "LLP"],
                                "widget": "select"
                            },
                            "proposed_name_1": {"type": "string", "title": "Proposed Name (Option 1)"},
                            "proposed_name_2": {"type": "string", "title": "Proposed Name (Option 2)"},
                            "proposed_name_3": {"type": "string", "title": "Proposed Name (Option 3)"},
                            
                            "header_2": {"type": "section_header", "title": "2. Owners & Directors Details"},
                            "primary_owner_name": {"type": "string", "title": "Primary Director/Owner Full Name"},
                            "primary_owner_id": {"type": "string", "title": "ID/Maisha Number"},
                            "primary_owner_kra": {"type": "string", "title": "Personal KRA PIN"},
                            
                            "header_3": {"type": "section_header", "title": "3. Business Operations"},
                            "business_activity": {"type": "string", "title": "Nature of Business / Activity", "format": "textarea"},
                            "physical_address": {"type": "string", "title": "Physical Address (Building, Street, Town)"},
                            "estimated_capital": {"type": "number", "title": "Nominal Share Capital (KES)"},
                            
                            "header_4": {"type": "section_header", "title": "4. Tax & Compliance"},
                            "register_for_vat": {"type": "boolean", "title": "Register for VAT? (If turnover > 5M)"},
                            "employer_registration": {"type": "boolean", "title": "Register as Employer (NSSF/NHIF)?"}
                        },
                        "required": ["business_type", "proposed_name_1", "primary_owner_name", "primary_owner_id", "business_activity", "physical_address"]
                    },
                    "workflow": [
                        {"sequence": 1, "step_name": "Applicant Submission", "step_type": "manual", "role": "citizen", "action": "submit"},
                        {"sequence": 2, "step_name": "Identity Verification (IPRS)", "step_type": "api_call", "action": "verify", "api_config": {"url": "HUDUMA_BRIDGE/IPRS/verify"}},
                        {"sequence": 3, "step_name": "Owner KRA PIN Verification", "step_type": "api_call", "action": "verify", "api_config": {"url": "HUDUMA_BRIDGE/KRA/verify"}},
                        {"sequence": 4, "step_name": "BRS Name Search & Reservation", "step_type": "api_call", "action": "name_search", "api_config": {"url": "HUDUMA_BRIDGE/BRS/name_search"}},
                        {"sequence": 5, "step_name": "Document Verification (BRS)", "step_type": "manual", "role": "officer", "action": "verify"},
                        {"sequence": 6, "step_name": "Business KRA PIN Generation", "step_type": "api_call", "action": "register_pin", "api_config": {"url": "HUDUMA_BRIDGE/KRA/register_pin"}},
                        {"sequence": 7, "step_name": "Final Approval & Seal", "step_type": "manual", "role": "supervisor", "action": "approve"},
                        {"sequence": 8, "step_name": "E-Registry Archival", "step_type": "api_call", "action": "archive", "api_config": {"url": "KESEL_BRIDGE/EDRMS/archive"}}
                    ]
                },
                "output": "Certificate of Incorporation & CR12"
            }
        },
        {
            'service_code': 'PROFILE_UPDATE',
            'service_name': 'Profile Update Verification',
            'mda': 'Ministry of Interior',
            'family': 'Civil Registration & Identity',
            'config': {
                'description': 'Request to update authoritative profile information.',
                'rules': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                             'id_number': {'type': 'string', 'title': 'National ID Number'},
                             'passport_number': {'type': 'string', 'title': 'Passport Number'},
                             'phone_number': {'type': 'string', 'title': 'Phone Number', 'format': 'tel'},
                             'supporting_document': {'type': 'string', 'format': 'data-url', 'title': 'Supporting Document (ID/Passport Scan)'}
                        },
                        'required': ['supporting_document']
                    },
                    'workflow': [
                        {
                            'sequence': 1,
                            'step_name': 'Update Request Submission',
                            'step_type': 'manual',
                            'role': 'citizen',
                            'action': 'submit'
                        },
                        {
                            'sequence': 2,
                            'step_name': 'Document Verification',
                            'step_type': 'manual',
                            'role': 'officer',
                            'action': 'verify'
                        },
                         {
                            'sequence': 3,
                            'step_name': 'Supervisor Approval',
                            'step_type': 'manual',
                            'role': 'supervisor',
                            'action': 'approve'
                        },
                        {
                            'sequence': 4,
                            'step_name': 'System Update',
                            'step_type': 'api_call',
                            'role': 'system',
                            'action': 'update_user_profile', # Special action
                            'api_config': {'url': 'internal://update_profile'} 
                        }
                    ]
                }
            }
        },
        {
            'service_code': 'CAB_MEMO',
            'service_name': 'Cabinet Memorandum Submission',
            'mda': 'Ministry of Interior',
            'family': 'Government Administration (G2G)',
            'config': {
                "rules": {
                    "schema": {
                        "type": "object",
                        "title": "Cabinet Memorandum Submission",
                        "properties": {
                            "memo_title": {"type": "string", "title": "Memo Title"},
                            "header_1": {
                                "type": "section_header",
                                "title": "1. Basic Details",
                                "description": "General information about the memorandum."
                            },
                            "originating_mda": {"type": "string", "title": "Originating MDA"},
                            "policy_summary": {"type": "string", "title": "Policy / Issue Summary", "format": "textarea"},
                            "problem_statement": {"type": "string", "title": "Problem Statement", "format": "textarea"},
                            
                            "header_2": {
                                "type": "section_header",
                                "title": "2. Impact Analysis",
                                "description": "Assess the implications of this policy."
                            },
                             "memo_priority": {
                                "type": "string",
                                "title": "Priority Level",
                                "enum": ["Normal", "High", "Critical"],
                                "widget": "radio"
                            },
                            "agencies_consulted": {
                                "type": "string",
                                "title": "Ministries/Agencies Consulted",
                                "enum": ["Treasury", "Attorney General", "Interior", "ICT Authority", "Other"],
                                "widget": "checkbox-group"
                            },
                            "financial_implications": {"type": "string", "title": "Financial Implications (Text)"},
                            "estimated_cost": {
                                "type": "number",
                                "title": "Estimated Implementation Cost (KES)",
                                "format": "currency"
                            },
                            
                            "header_3": {
                                "type": "section_header",
                                "title": "3. Authorization"
                            },
                            "confidentiality_agreement": {
                                "type": "boolean",
                                "title": "Confidentiality Agreement",
                                "description": "I actchnowledge this document contains Sensitive Information."
                            },
                             "contact_email": {
                                "type": "string",
                                "title": "Drafter Email",
                                "format": "email"
                            },
                            "recommendations": {"type": "string", "title": "Proposed Recommendations", "format": "textarea"},
                            "legal_implications": {"type": "string", "title": "Legal Implications"},
                            "annex_document": {
                                "type": "string", 
                                "title": "Annex (PDF Upload)", 
                                "format": "data-url",
                                "description": "Upload supporting policy document."
                            },
                            "inter_ministerial_impact": {
                                "type": "string",
                                "title": "Inter-Ministerial Impact",
                                "enum": ["Yes", "No", "N/A"]
                            }
                        },
                        "required": ["memo_title", "originating_mda", "recommendations"]
                    }
                },
                "sla": 14,
                "output": "Cabinet Decision"
            }
        },
        {
            'service_code': 'NATIONAL_ID',
            'service_name': 'National ID Application (Maisha)',
            'mda': 'National Registration Bureau',
            'family': 'Civil Registration & Identity',
            'config': {
                'rules': {
                    'schema': {
                        'type': 'object',
                        'title': 'Application for National Identity Card',
                        'properties': {
                            'header_1': {'type': 'section_header', 'title': '1. Identity Source'},
                            'birth_entry_number': {
                                'type': 'string', 
                                'title': 'Birth Entry Number (BEN) / Cert No.', 
                                'description': 'Enter your BEN from your Birth Certificate to fetch record.',
                                'lookup_service': 'CRS',
                                'lookup_action': 'fetch'
                            },
                            'is_guardian_app': {
                                'type': 'boolean', 
                                'title': 'Guardian / Orphan Application?',
                                'description': 'Check this if applying as a Legal Guardian (e.g. if parents are deceased).'
                            },
                            'death_cert_no': {
                                'type': 'string', 
                                'title': 'Mother/Father Death Certificate No.',
                                'description': 'Required for orphan applications.'
                            },
                            'application_type': {
                                'type': 'string',
                                'title': 'Type of Application',
                                'enum': ['First Time ID', 'Replacement (Lost)', 'Replacement (Damaged)', 'Change of Particulars'],
                                'widget': 'select'
                            },
                            
                            'header_2': {'type': 'section_header', 'title': '2. Personal Details (Pre-filled)'},
                            'full_name': {'type': 'string', 'title': 'Full Name (as per Birth Certificate)'},
                            'date_of_birth': {'type': 'string', 'format': 'date', 'title': 'Date of Birth'},
                            'gender': {'type': 'string', 'title': 'Gender', 'enum': ['Male', 'Female'], 'widget': 'radio'},
                            
                            'header_3': {'type': 'section_header', 'title': '3. Parents Details'},
                            'mother_name': {'type': 'string', 'title': "Mother's Full Name"},
                            'mother_id': {'type': 'string', 'title': "Mother's ID Number"},
                            'father_name': {'type': 'string', 'title': "Father's Full Name"},
                            'father_id': {'type': 'string', 'title': "Father's ID Number"},
                            
                            'header_4': {'type': 'section_header', 'title': '4. Residence & Location'},
                            'county': {
                                'type': 'string', 
                                'title': 'County of Birth/Origin',
                                'enum': KENYA_COUNTIES,
                                'widget': 'select'
                            },
                            'sub_county': {'type': 'string', 'title': 'Sub-County'},
                            'location': {'type': 'string', 'title': 'Location'},
                            'village': {'type': 'string', 'title': 'Village / Estate'},
                            
                            'header_5': {'type': 'section_header', 'title': '5. Supporting Documents'},
                            'birth_cert_upload': {'type': 'string', 'format': 'data-url', 'title': 'Copy of Birth Certificate'},
                            'parent_id_upload': {'type': 'string', 'format': 'data-url', 'title': "Copy of Mother's/Father's ID"},
                            'police_abstract': {'type': 'string', 'format': 'data-url', 'title': 'Police Abstract (Required for Replacement)'}
                        },
                        'required': ['birth_entry_number', 'application_type', 'full_name', 'date_of_birth', 'gender', 'county']
                    },
                    'workflow': [
                        {'sequence': 1, 'step_name': 'Application Submission', 'step_type': 'manual', 'role': 'citizen', 'action': 'submit'},
                        {'sequence': 2, 'step_name': 'IPRS Verification', 'step_type': 'api_call', 'action': 'verify', 'api_config': {'url': 'HUDUMA_BRIDGE/IPRS/verify'}},
                        {'sequence': 3, 'step_name': 'Local Vetting (Chief/Committee)', 'step_type': 'manual', 'role': 'officer', 'action': 'verify'},
                        {'sequence': 4, 'step_name': 'Biometric Capture & Enrollment', 'step_type': 'manual', 'role': 'officer', 'action': 'capture_biometrics'},
                        {'sequence': 5, 'step_name': 'Central Registry Review', 'step_type': 'manual', 'role': 'registrar', 'action': 'approve'},
                        {'sequence': 6, 'step_name': 'ID Production (Printing)', 'step_type': 'manual', 'role': 'officer', 'action': 'print'},
                        {'sequence': 7, 'step_name': 'Final Issuance (Collection)', 'step_type': 'manual', 'role': 'registrar', 'action': 'issue'}
                    ]
                },
                'output': 'National Identity Card (Maisha Card)'
            }
        },
        {
            'service_code': 'SECURE_CLEARANCE',
            'service_name': 'Secure Inter-Agency Clearance',
            'mda': 'Ministry of Interior',
            'family': 'Government Administration (G2G)',
            'config': {
                "rules": {
                    "schema": {
                        "type": "object",
                        "title": "Secure Clearance Request",
                        "properties": {
                            "document_title": {"type": "string", "title": "Document Title"},
                            "security_level": {
                                "type": "string",
                                "title": "Security Level",
                                "enum": ["Public", "Internal", "Secret"]
                            },
                            "signed_content": {"type": "string", "format": "textarea", "title": "Digital Signature Hash (NPKI)"}
                        },
                        "required": ["document_title", "signed_content"]
                    },
                    "workflow": [
                        {"sequence": 1, "step_name": "Submission", "step_type": "manual", "role": "citizen", "action": "submit"},
                        {"sequence": 2, "step_name": "NPKI Signature Validation", "step_type": "api_call", "action": "verify_signature", "api_config": {"url": "HUDUMA_BRIDGE/TRUST/verify"}},
                        {"sequence": 3, "step_name": "MOI Internal Review", "step_type": "manual", "role": "officer", "action": "verify"},
                        {"sequence": 4, "step_name": "BRS Cross-Agency Approval", "step_type": "manual", "role": "supervisor", "target_mda_code": "BRS", "action": "approve"},
                        {"sequence": 5, "step_name": "Final Archive", "step_type": "api_call", "api_config": {"url": "KESEL_BRIDGE/EDRMS/archive"}, "action": "archive"}
                    ]
                }
            }
        },
        {
            'service_code': 'KRA_PIN_REG',
            'service_name': 'Individual KRA PIN Registration',
            'mda': 'Kenya Revenue Authority',
            'family': 'Business & Revenue',
            'config': {
                'rules': {
                    'schema': {
                        'type': 'object',
                        'title': 'Individual Taxpayer Registration',
                        'properties': {
                            'header_1': {'type': 'section_header', 'title': '1. Identity Authentication'},
                            'national_id': {
                                'type': 'string', 
                                'title': 'National ID Number', 
                                'description': 'Enter your ID to pull verified details from NRB.',
                                'lookup_service': 'IPRS',
                                'lookup_action': 'fetch'
                            },
                            
                            'header_2': {'type': 'section_header', 'title': '2. Personal Details (Auto-filled)'},
                            'full_name': {'type': 'string', 'title': 'Full Name'},
                            'date_of_birth': {'type': 'string', 'format': 'date', 'title': 'Date of Birth'},
                            'gender': {'type': 'string', 'title': 'Gender', 'enum': ['Male', 'Female'], 'widget': 'radio'},
                            
                            'header_3': {'type': 'section_header', 'title': '3. Taxpayer Classification'},
                            'resident_type': {
                                'type': 'string',
                                'title': 'Resident Type',
                                'enum': ['Resident', 'Non-Resident', 'Non-Resident with Permanent Establishment'],
                                'widget': 'select'
                            },
                            'income_sources': {
                                'type': 'array',
                                'title': 'Income Sources',
                                'items': {
                                    'type': 'string',
                                    'enum': ['Employment', 'Business', 'Rental', 'Professional', 'Agriculture', 'None (Student/Unemployed)']
                                },
                                'widget': 'checkbox-group'
                            },
                            
                            'header_4': {'type': 'section_header', 'title': '4. Contact Information'},
                            'phone_number': {'type': 'string', 'title': 'Personal Phone Number'},
                            'email': {'type': 'string', 'format': 'email', 'title': 'Personal Email Address'}
                        },
                        'required': ['national_id', 'full_name', 'date_of_birth', 'resident_type', 'income_sources', 'email']
                    },
                    'workflow': [
                        {'sequence': 1, 'step_name': 'Application Submission', 'step_type': 'manual', 'role': 'citizen', 'action': 'submit'},
                        {'sequence': 2, 'step_name': 'NRB Identity Validation', 'step_type': 'api_call', 'action': 'verify', 'api_config': {'url': 'HUDUMA_BRIDGE/IPRS/verify'}},
                        {'sequence': 3, 'step_name': 'Tax Obligation Mapping', 'step_type': 'api_call', 'action': 'map_taxes', 'api_config': {'url': 'KRA_ITAX/obligations/map'}},
                        {'sequence': 4, 'step_name': 'PIN Generation', 'step_type': 'api_call', 'action': 'register_pin', 'api_config': {'url': 'HUDUMA_BRIDGE/KRA/register_pin'}},
                        {'sequence': 5, 'step_name': 'Digital PIN Certificate Issuance', 'step_type': 'manual', 'role': 'officer', 'action': 'issue'}
                    ]
                },
                'output': 'Instant KRA PIN Certificate'
            }
        },
        {
            'service_code': 'SCHOLARSHIPS',
            'service_name': 'Scholarships & Bursaries Coordination',
            'mda': 'Ministry of Education',
            'family': 'Social Services & Education',
            'config': {
                "rules": {
                    "schema": {
                        "type": "object",
                        "title": "Scholarship & Bursary Application",
                        "properties": {
                             "header_1": {"type": "section_header", "title": "1. Personal Details"},
                             "full_name": {"type": "string", "title": "Applicant Full Name"},
                             "id_number": {"type": "string", "title": "ID Number / Birth Cert No"},
                             "date_of_birth": {"type": "string", "format": "date", "title": "Date of Birth"},
                             "gender": {"type": "string", "title": "Gender", "enum": ["Male", "Female"], "widget": "radio"},
                             
                             "header_2": {"type": "section_header", "title": "2. Education Details"},
                             "institution": {"type": "string", "title": "Institution Name"},
                             "admission_number": {"type": "string", "title": "Admission Number"},
                             "course_of_study": {"type": "string", "title": "Course of Study"},
                             "year_of_study": {"type": "number", "title": "Year of Study"},
                             
                             "header_3": {"type": "section_header", "title": "3. Financial Need Assessment"},
                             "maternal_status": {"type": "string", "enum": ["Alive", "Deceased", "Unknown"], "title": "Mother's Status", "widget": "radio"},
                             "paternal_status": {"type": "string", "enum": ["Alive", "Deceased", "Unknown"], "title": "Father's Status", "widget": "radio"},
                             "financial_need_desc": {"type": "string", "format": "textarea", "title": "Explain Financial Need"},
                             
                             "header_4": {"type": "section_header", "title": "4. Supporting Documents"},
                             "admission_letter": {"type": "string", "format": "data-url", "title": "Admission Letter"},
                             "fees_structure": {"type": "string", "format": "data-url", "title": "Fee Structure"},
                             "id_copy": {"type": "string", "format": "data-url", "title": "ID/Birth Cert Copy"}
                        },
                        "required": ["full_name", "id_number", "institution", "financial_need_desc", "admission_letter"]
                    },
                    "workflow": [
                        {"sequence": 1, "step_name": "Application Submission", "step_type": "manual", "role": "citizen", "action": "submit"},
                        {"sequence": 2, "step_name": "Preliminary Screening", "step_type": "manual", "role": "officer", "action": "screen"},
                        {"sequence": 3, "step_name": "Verification & Due Diligence", "step_type": "manual", "role": "officer", "action": "verify"},
                        {"sequence": 4, "step_name": "Evaluation & Scoring", "step_type": "manual", "role": "supervisor", "action": "score"},
                        {"sequence": 5, "step_name": "Approval & Award Decision", "step_type": "manual", "role": "supervisor", "action": "approve"},
                        {"sequence": 6, "step_name": "Funds Disbursement", "step_type": "manual", "role": "officer", "action": "disburse"},
                        {"sequence": 7, "step_name": "Utilization Monitoring", "step_type": "manual", "role": "officer", "action": "monitor"}
                    ]
                },
                "output": "Scholarship Award Letter"
            }
        }
    ]

    # The mdas loop and created_mdas are now at the top of the function.
    pass

    try:
        import os, json
        pw_path = os.path.join(os.getcwd(), 'priority_workflows.json')
        if os.path.exists(pw_path):
            with open(pw_path, 'r') as f:
                p_data = json.load(f)
                for idx, item in enumerate(p_data):
                    mda_name = item.get('mda_name', '').strip()
                    raw_process_name = item.get('process_name')
                    if not raw_process_name or not mda_name: continue
                    process_name = str(raw_process_name).replace('\n', ' ').strip()
                    
                    # Match MDA logic loosely
                    matched_mda_code = None
                    for m_name, m_obj in created_mdas.items():
                        if m_name.lower() == mda_name.lower() or mda_name.lower() in m_name.lower() or m_name.lower() in mda_name.lower():
                            matched_mda_code = m_name
                            break
                    if not matched_mda_code:
                        matched_mda_code = mda_name
                    
                    # Construct workflows
                    to_be = item.get('to_be', [])
                    wf = []
                    seq_counter = 1
                    for row in to_be:
                        if len(row) >= 3:
                            role_val = str(row[1]).replace('\n', ' ').strip()[:50]
                            step_name = str(row[2]).replace('\n', ' ').strip()[:100]
                            desc_val = str(row[3]).replace('\n', ' ').strip().lower() if len(row) > 3 else ''
                            stype = 'api_call' if ('api' in desc_val or 'system' in desc_val or 'portal' in desc_val or 'bridge' in desc_val or 'x-road' in desc_val or role_val.lower() == 'system') else 'manual'
                            wf.append({
                                'sequence': seq_counter,
                                'step_name': step_name,
                                'step_type': stype,
                                'role': role_val,
                                'action': 'execute'
                            })
                            seq_counter += 1
                    
                    services.append({
                        'service_code': f"PRI-{idx+1000}",
                        'service_name': process_name[:255],
                        'mda': matched_mda_code,
                        'family': 'Government Administration (G2G)',
                        'config': {
                            'rules': {
                                'schema': {
                                    'type': 'object',
                                    'title': process_name[:100],
                                    'properties': {
                                        'virtual_id': {'type': 'string', 'title': 'Digital ID (Maisha)', 'readOnly': True}
                                    },
                                    'required': ['virtual_id']
                                },
                                'workflow': wf
                            }
                        }
                    })
    except Exception as e:
        print(f"Error loading priority_workflows.json: {e}")

    for svc_data in services:
        mda = created_mdas.get(svc_data['mda'])
        if not mda:
            print(f"Skipping {svc_data['service_name']} - MDA not found")
            continue
        
        family_name = svc_data.get('family')
        family = created_families.get(family_name) if family_name else None
        
        svc, created = ServiceConfig.objects.update_or_create(
            service_code=svc_data['service_code'],
            defaults={
                'service_name': svc_data['service_name'],
                'mda': mda,
                'service_family': family,
                'config': svc_data['config']
            }
        )
        print(f"Ensured Service: {svc.service_name}")

        # 4. Create Lifecycle/Workflow Steps
        # Clear existing steps via cascade or manual delete
        try:
             WorkflowStep.objects.filter(service_config=svc).delete()
        except:
             pass

        workflow_rules = svc.config.get('rules', {}).get('workflow', [])
        
        if workflow_rules:
            print(f"Creating {len(workflow_rules)} workflow steps for {svc.service_name} from config...")
            for step_data in workflow_rules:
                # Handle optional fields safely
                api_conf = step_data.get('api_config')
                # Handle target_mda if specified by code
                target_mda = None
                mda_code = step_data.get('target_mda_code')
                if mda_code:
                    target_mda = MDA.objects.filter(code=mda_code).first()

                WorkflowStep.objects.create(
                    service_config=svc,
                    sequence=step_data['sequence'],
                    step_name=step_data['step_name'],
                    role=step_data.get('role', 'system'),
                    step_type=step_data['step_type'],
                    target_mda=target_mda,
                    action=step_data.get('action', 'execute'),
                    api_config=api_conf
                )
        else:
            # Fallback for generic services if no workflow defined in config
            pass

    # 5. Seed one active request
    # SKIPPED: User requested clean slate without sample applications.

    print("Seeding complete!")

if __name__ == '__main__':
    seed_data()
