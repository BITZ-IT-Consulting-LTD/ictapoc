
import os
import django
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, User, Role, ServiceDomain, ServiceCategory

priority_mdas = [
    {"name": "Department of Immigration (DIS)", "aliases": ["Department of Immigration Services", "DIS"], "type": "State Department", "sector": "Interior", "domain_process": "Passport Application Service", "domain_code": "DIS-PASS-01"},
    {"name": "Athi Water Works", "aliases": ["Athi Water", "AWWDA"], "type": "Agency", "sector": "Water", "domain_process": "Water Connection Request", "domain_code": "AWW-WAT-01"},
    {"name": "Department of Refugee Services (DRS)", "aliases": ["DRS"], "type": "State Department", "sector": "Interior", "domain_process": "Refugee Registration", "domain_code": "DRS-REF-01"},
    {"name": "Department of Civil Registration Services (CRS)", "aliases": ["Civil Registration Services", "CRS"], "type": "State Department", "sector": "Interior", "domain_process": "Birth Registration", "domain_code": "CRS-BIR-01"},
    {"name": "State Department for Micro, Small & Medium Enterprises (MSME)", "aliases": ["MSME"], "type": "State Department", "sector": "Trade", "domain_process": "Business Grant Application", "domain_code": "MSM-GRA-01"},
    {"name": "State Department for Culture, the Arts & Heritage", "aliases": ["Culture and Arts"], "type": "State Department", "sector": "Heritage", "domain_process": "Cultural Grant", "domain_code": "CAH-GRA-01"},
    {"name": "National Environment Management Authority (NEMA)", "aliases": ["NEMA"], "type": "Agency", "sector": "Environment", "domain_process": "Environmental Impact Assessment", "domain_code": "NEMA-EIA-01"},
    {"name": "Public Service Commission (PSC)", "aliases": ["PSC"], "type": "Agency", "sector": "Public Service", "domain_process": "Recruitment & HR Records", "domain_code": "PSC-HR-01"},
    {"name": "State Department for Children Services", "aliases": ["Children Services"], "type": "State Department", "sector": "Social Protection", "domain_process": "Child Protection Case Management", "domain_code": "CHI-CASE-01"},
    {"name": "National Government Coordination / Prime Cabinet Secretary (PrimeCS)", "aliases": ["Prime Cabinet Secretary", "PrimeCS"], "type": "State Department", "sector": "Executive", "domain_process": "Executive Briefing Management", "domain_code": "PCS-BRI-01"},
    {"name": "Department for Sports", "aliases": ["Sports Department"], "type": "State Department", "sector": "Sports", "domain_process": "Sports Club Registration", "domain_code": "SPO-REG-01"},
    {"name": "State Department for Cabinet Affairs", "aliases": ["Cabinet Affairs"], "type": "State Department", "sector": "Executive", "domain_process": "Cabinet Memo Tracking", "domain_code": "CAB-TRK-01"},
    {"name": "State Department for Youth Affairs & Creative Economy", "aliases": ["Youth Affairs"], "type": "State Department", "sector": "Youth", "domain_process": "Youth Fund Application", "domain_code": "YTH-FND-01"},
    {"name": "State Department for Energy", "aliases": ["Energy Department"], "type": "State Department", "sector": "Energy", "domain_process": "Power Plant License", "domain_code": "NRG-LIC-01"},
    {"name": "State Department for Science, Research & Innovation", "aliases": ["Science and Research"], "type": "State Department", "sector": "Education", "domain_process": "Research Permit", "domain_code": "SCI-PER-01"},
    {"name": "State Department of Health Services", "aliases": ["Health Services"], "type": "State Department", "sector": "Health", "domain_process": "Health Facility Licensing", "domain_code": "HLT-LIC-01"},
    {"name": "State Department of Higher Education – Rongo University", "aliases": ["Rongo University"], "type": "Institution", "sector": "Education", "domain_process": "Student Registration", "domain_code": "RON-REG-01"},
    {"name": "State Department of Agriculture – AFA", "aliases": ["AFA", "Agriculture Authority"], "type": "Agency", "sector": "Agriculture", "domain_process": "Export Permit", "domain_code": "AFA-EXP-01"},
]

def seed():
    print("| MDA Name | Status | Processes | Actors |")
    print("|---|---|---|---|")

    # Ensure Roles exist
    roles = {
        'admin': Role.objects.get_or_create(name='admin')[0],
        'mda_admin': Role.objects.get_or_create(name='mda_admin')[0],
        'officer': Role.objects.get_or_create(name='officer')[0],
        'supervisor': Role.objects.get_or_create(name='supervisor')[0],
        'registrar': Role.objects.get_or_create(name='registrar')[0],
    }

    # Common Registry Domain/Category
    registry_domain, _ = ServiceDomain.objects.get_or_create(name="Government Registry")
    registry_cat, _ = ServiceCategory.objects.get_or_create(name="Correspondence & Files", domain=registry_domain)

    all_mdas = list(MDA.objects.all())

    for p_mda in priority_mdas:
        target_name = p_mda['name']
        aliases = p_mda['aliases']
        
        existing = None
        for m in all_mdas:
            if m.name == target_name or any(a.lower() == m.name.lower() for a in aliases):
                existing = m
                break
        
        status = "VERIFIED"
        processes_count = 0
        actors_count = 0

        if not existing:
            status = "SEEDED"
            # Improved MDA Code generation
            if '(' in target_name:
                mda_code = target_name.split('(')[-1].replace(')', '')
            elif 'State Department for ' in target_name:
                part = target_name.split('State Department for ')[-1].split()[0][:5].upper()
                mda_code = f"SD-{part}"
            elif 'State Department of ' in target_name:
                part = target_name.split('State Department of ')[-1].split()[0][:5].upper()
                mda_code = f"SD-{part}"
            else:
                mda_code = target_name.split()[-1][:10].upper()
            
            # Ensure unique
            counter = 1
            original_code = mda_code
            while MDA.objects.filter(code=mda_code).exists():
                mda_code = f"{original_code[:7]}{counter}"
                counter += 1

            flags = {
                "EDRMS": "NOT CONFIGURED",
                "MIS": "UNKNOWN",
                "Integration": "PENDING",
                "Infrastructure": "NOT VALIDATED",
                "type": p_mda['type'],
                "sector": p_mda['sector'],
                "seeded_for": "POC"
            }
            
            existing = MDA.objects.create(
                name=target_name,
                code=mda_code,
                description=json.dumps(flags)
            )
            # STEP 4: Attach Core Process Services
            registry_services = [
                "Incoming Correspondence",
                "Outgoing Correspondence",
                "File / Case Management",
                "Archive & Retention",
                "Registry Search & Retrieval"
            ]
            
            for s_name in registry_services:
                ServiceConfig.objects.get_or_create(
                    service_name=f"{s_name} ({existing.code})",
                    defaults={
                        "service_code": f"{existing.code}-{s_name[:3].upper()}-{processes_count}",
                        "mda": existing,
                        "category": registry_cat,
                        "is_public_facing": False,
                        "service_type": "Internal",
                        "description": f"Standard registry process for {existing.name}",
                        "config": {"steps": []}
                    }
                )
                processes_count += 1
            
            # Priority Domain Process
            domain_cat, _ = ServiceCategory.objects.get_or_create(name=p_mda['sector'], domain=registry_domain)
            ServiceConfig.objects.get_or_create(
                service_name=p_mda['domain_process'],
                defaults={
                    "service_code": p_mda['domain_code'],
                    "mda": existing,
                    "category": domain_cat,
                    "is_public_facing": True,
                    "service_type": "Transactional",
                    "description": f"Primary domain service for {existing.name}",
                    "config": {"steps": []}
                }
            )
            processes_count += 1

            # STEP 5: Seed Governance Actors
            actor_roles = [
                ('Records Manager', 'supervisor'),
                ('ICT Manager', 'mda_admin'),
                ('Product Owner', 'supervisor')
            ]
            
            for actor_name, role_key in actor_roles:
                username = f"{existing.code.lower().replace(' ', '_')}_{actor_name.lower().replace(' ', '_')}"
                if not User.objects.filter(username=username).exists():
                    User.objects.create_user(
                        username=username,
                        email=f"{username}@mail.go.ke",
                        password="Starten1@",
                        mda=existing,
                        role=role_key,
                        user_role=roles[role_key],
                        first_name=actor_name,
                        last_name="(POC-default)"
                    )
                    actors_count += 1
        else:
            # For verified ones, just count
            processes_count = ServiceConfig.objects.filter(mda=existing).count()
            actors_count = User.objects.filter(mda=existing).count()

        print(f"| {target_name} | {status} | {processes_count} | {actors_count} |")

if __name__ == "__main__":
    seed()
