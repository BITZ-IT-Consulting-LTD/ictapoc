from service_api.models import ServiceFamily, ServiceConfig
from django.db.models import Count

def consolidate_families():
    print("Consolidating service families...")
    
    # Define mapping of redundant/short names to canonical names
    mapping = {
        'Civil Registration & Identity': 'Identity & Civil Registration',
        'Immigration': 'Immigration & Border Management',
        'Business & Revenue': 'Taxation & Revenue Administration',
        'Social Services & Education': 'Social Protection & Welfare',
        'Government Administration (G2G)': 'Governance & Intergovernmental Coordination',
    }
    
    for old_name, new_name in mapping.items():
        try:
            old_fam = ServiceFamily.objects.get(name=old_name)
            new_fam, created = ServiceFamily.objects.get_or_create(name=new_name)
            
            # Move services
            svc_count = ServiceConfig.objects.filter(service_family=old_fam).update(service_family=new_fam)
            print(f"  Moved {svc_count} services from '{old_name}' to '{new_name}'")
            
            # Delete old family
            old_fam.delete()
            print(f"  Deleted redundant family '{old_name}'")
        except ServiceFamily.DoesNotExist:
            continue

    # Delete any other empty families
    empty = ServiceFamily.objects.annotate(svc_count=Count('services')).filter(svc_count=0)
    for f in empty:
        print(f"  Deleting empty family '{f.name}'")
        f.delete()

if __name__ == "__main__":
    consolidate_families()
