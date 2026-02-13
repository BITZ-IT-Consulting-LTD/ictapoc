import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, ServiceDomain, ServiceCategory, WorkflowStep

# MDAs from Government_Service_Catalogue.md that might be missing
CATALOGUE_MDAS = [
    # From the document
    {"name": "Cabinet Office", "code": "CO", "description": "Cabinet Business and coordination"},
    {"name": "Public Service Commission", "code": "PSC", "description": "Commission Core and support Services"},
    {"name": "State Department for Correctional Services", "code": "SDCS", "description": "Safe custody & inmate management"},
    {"name": "State Department for Economic Planning", "code": "SDEP", "description": "Monitoring and Evaluation of Government Programmes"},
    {"name": "State Department for Higher Education and Research", "code": "SDHER", "description": "Academic services"},
    {"name": "State Department for Housing and Urban Development", "code": "SDHUD", "description": "Housing services"},
    {"name": "State Department for Immigration and Citizen Services", "code": "SDICS", "description": "Immigration and citizen services"},
    {"name": "State Department for Medical Services", "code": "SDMS", "description": "Medical services and records management"},
    {"name": "State Department for TVET", "code": "SDTVET", "description": "TVET records management"},
    {"name": "State Department for Broadcasting and Telecommunications", "code": "SDBT", "description": "Broadcasting and telecommunications services"},
    {"name": "State Department for Public Service and Human Capital Development", "code": "SDPSHCD", "description": "Public service policy"},
    {"name": "State Department for Public Works", "code": "SDPW", "description": "Pre-Construction of Built environment"},
    {"name": "State Department for Science, Research and Innovation", "code": "SDSRI", "description": "Promote science, research and innovation"},
    {"name": "Directorate of Immigration Services", "code": "DIS-ALT", "description": "Travel Documents (alternative entry)"},
    
    # Water sector MDAs (commonly missing)
    {"name": "Athi Water Works Development Agency", "code": "AWWDA", "description": "Water infrastructure development in Athi region"},
    {"name": "Tana Water Works Development Agency", "code": "TWWDA", "description": "Water infrastructure development in Tana region"},
    {"name": "Lake Victoria North Water Works Development Agency", "code": "LVNWWDA", "description": "Water infrastructure in Lake Victoria North"},
    {"name": "Lake Victoria South Water Works Development Agency", "code": "LVSWWDA", "description": "Water infrastructure in Lake Victoria South"},
    {"name": "Rift Valley Water Works Development Agency", "code": "RVWWDA", "description": "Water infrastructure in Rift Valley"},
    {"name": "Coast Water Works Development Agency", "code": "CWWDA", "description": "Water infrastructure in Coast region"},
    {"name": "Northern Water Works Development Agency", "code": "NWWDA", "description": "Water infrastructure in Northern region"},
    
    # Other commonly referenced MDAs
    {"name": "Kenya Airports Authority", "code": "KAA", "description": "Airport management and operations"},
    {"name": "Kenya Ports Authority", "code": "KPA", "description": "Port management and operations"},
    {"name": "Kenya Railways Corporation", "code": "KRC", "description": "Railway services and operations"},
    {"name": "National Construction Authority", "code": "NCA", "description": "Construction industry regulation"},
    {"name": "National Land Commission", "code": "NLC", "description": "Land administration and management"},
    {"name": "Ethics and Anti-Corruption Commission", "code": "EACC-ALT", "description": "Anti-corruption services"},
]

print("=" * 80)
print("CHECKING FOR MISSING MDAs")
print("=" * 80)

existing_mdas = {mda.name.lower(): mda for mda in MDA.objects.all()}
existing_codes = {mda.code.upper() if mda.code else "": mda for mda in MDA.objects.all() if mda.code}

missing_mdas = []
duplicate_mdas = []

for mda_data in CATALOGUE_MDAS:
    name_lower = mda_data["name"].lower()
    code_upper = mda_data["code"].upper()
    
    # Check if exists by name (partial match)
    name_exists = any(name_lower in existing_name or existing_name in name_lower 
                     for existing_name in existing_mdas.keys())
    
    # Check if exists by code
    code_exists = code_upper in existing_codes
    
    if not name_exists and not code_exists:
        missing_mdas.append(mda_data)
        print(f"✗ MISSING: {mda_data['name']} ({mda_data['code']})")
    elif name_exists or code_exists:
        duplicate_mdas.append(mda_data['name'])

print(f"\n{'=' * 80}")
print(f"SUMMARY:")
print(f"  Total checked: {len(CATALOGUE_MDAS)}")
print(f"  Already exist: {len(duplicate_mdas)}")
print(f"  Missing: {len(missing_mdas)}")
print(f"{'=' * 80}")

if missing_mdas:
    print(f"\n📋 MISSING MDAs TO BE ADDED ({len(missing_mdas)}):")
    for idx, mda in enumerate(missing_mdas, 1):
        print(f"{idx:2d}. {mda['code']:10s} - {mda['name']}")
