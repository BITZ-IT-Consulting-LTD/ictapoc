import os
import re
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig, MDA, ServiceCategory, ServiceDomain

def enrich_catalogue():
    print("--- ENRICHING WOG CATALOGUE FROM MD FILES ---")
    bpmn_dir = "/Users/mac/ictapoc/as-is-bpmn"
    
    for filename in os.listdir(bpmn_dir):
        if not filename.endswith(".md"):
            continue
            
        path = os.path.join(bpmn_dir, filename)
        with open(path, 'r') as f:
            content = f.read()
            
        # 1. Extract Title/Category
        # Header 1 often contains MDA and Process Area
        h1_match = re.search(r'^#\s*(.*?)\s*-', content, re.MULTILINE)
        mda_name_raw = h1_match.group(1) if h1_match else filename.replace(".md", "")
        
        # Sub-process or Division in parentheses
        category_match = re.search(r'\((.*?)\)', content.split('\n')[0])
        category_name = category_match.group(1) if category_match else "General Services"
        
        # 2. Extract Key Systems & Actors
        systems = []
        actors = []
        
        systems_match = re.search(r'\*\*Key Systems\*\*\s*\|\s*(.*?)\s*\|', content)
        if systems_match:
            systems = [s.strip() for s in systems_match.group(1).split(',')]
            
        actors_match = re.search(r'\*\*Key Actors\*\*\s*\|\s*(.*?)\s*\|', content)
        if actors_match:
            actors = [a.strip() for a in actors_match.group(1).split(',')]
            
        # 3. Handle Domain (Sector)
        # We'll try to guess sector from MDA name or use a default
        sector = "Public Service & Administration"
        if "Education" in mda_name_raw: sector = "Education & Training"
        elif "Immigration" in mda_name_raw or "Interior" in mda_name_raw: sector = "Identity & National Administration"
        elif "Health" in mda_name_raw: sector = "Health & Wellness"
        elif "Energy" in mda_name_raw: sector = "Infrastructure & Energy"
        elif "Youth" in mda_name_raw: sector = "Youth & Creative Economy"
        
        domain_obj, _ = ServiceDomain.objects.get_or_create(name=sector)
        cat_obj, _ = ServiceCategory.objects.get_or_create(name=category_name, domain=domain_obj)
        
        # 4. Update Matching Services
        # We find services that belong to this MDA
        # The MDA might have been seeded with a slightly different name
        mda_objs = MDA.objects.filter(name__icontains=mda_name_raw.strip())
        if not mda_objs:
             # Fallback: check if the filename starts with the MDA name
             simplified_name = mda_name_raw.split('(')[0].strip()
             mda_objs = MDA.objects.filter(name__icontains=simplified_name)

        for mda_obj in mda_objs:
            services = ServiceConfig.objects.filter(mda=mda_obj)
            for svc in services:
                svc.associated_systems = systems
                svc.associated_actors = actors
                svc.category = cat_obj
                # Add some common pain points if not present
                if not svc.pain_points:
                    svc.pain_points = ["Manual Validation", "Physical Queues", "High TAT"]
                
                svc.save()
                print(f"  [Enriched] {svc.service_name} (Category: {category_name})")

    print("--- ENRICHMENT COMPLETE ---")

if __name__ == '__main__':
    enrich_catalogue()
