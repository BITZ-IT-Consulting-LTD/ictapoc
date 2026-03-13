import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep

print("=" * 80)
print("PRIORITY MDAs UPDATE SUMMARY REPORT")
print("=" * 80)

# 17 Priority MDAs
priority_mda_codes = ['DIS', 'NRB', 'KRA', 'NTSA', 'TSC', 'HELB', 'CUE', 'KNEC', 
                      'NHIF', 'NSSF', 'NEA', 'ROC', 'CA', 'ODPC', 'ICT', 'KWS', 'NEMA']

print("\n📊 UPDATED MDAs (17 Priority Agencies)")
print("-" * 80)

total_services = 0
total_workflows = 0

for code in priority_mda_codes:
    mda = MDA.objects.filter(code=code).first()
    if mda:
        services = ServiceConfig.objects.filter(mda=mda)
        service_count = services.count()
        
        # Count services with enhanced workflows (both as-is and to-be)
        enhanced_count = 0
        for svc in services:
            as_is = WorkflowStep.objects.filter(service_config=svc, lifecycle_stage='as_is').count()
            to_be = WorkflowStep.objects.filter(service_config=svc, lifecycle_stage='to_be').count()
            if as_is > 3 and to_be > 3:  # Enhanced workflows have more than basic 3 steps
                enhanced_count += 1
        
        total_services += service_count
        total_workflows += enhanced_count
        
        status = "✓" if enhanced_count > 0 else "○"
        print(f"{status} {code:6s} | {mda.name:45s} | {service_count:2d} services | {enhanced_count:2d} enhanced")

print("\n" + "=" * 80)
print(f"TOTALS: {len(priority_mda_codes)} MDAs | {total_services} Services | {total_workflows} Enhanced Workflows")
print("=" * 80)

print("\n🔧 ENHANCED SERVICES WITH DETAILED WORKFLOWS")
print("-" * 80)

enhanced_services = []
for code in priority_mda_codes:
    mda = MDA.objects.filter(code=code).first()
    if mda:
        for svc in ServiceConfig.objects.filter(mda=mda):
            as_is_count = WorkflowStep.objects.filter(service_config=svc, lifecycle_stage='as_is').count()
            to_be_count = WorkflowStep.objects.filter(service_config=svc, lifecycle_stage='to_be').count()
            if as_is_count > 3 and to_be_count > 3:
                enhanced_services.append({
                    'mda': mda.code,
                    'service': svc.service_name,
                    'as_is': as_is_count,
                    'to_be': to_be_count
                })

for idx, svc in enumerate(enhanced_services, 1):
    print(f"{idx:2d}. [{svc['mda']:6s}] {svc['service']:50s} | As-Is: {svc['as_is']:2d} steps | To-Be: {svc['to_be']:2d} steps")

print("\n" + "=" * 80)
print(f"Total Enhanced Services: {len(enhanced_services)}")
print("=" * 80)

print("\n📋 MDA CONTACT INFORMATION")
print("-" * 80)

for code in priority_mda_codes:
    mda = MDA.objects.filter(code=code).first()
    if mda:
        print(f"\n{mda.code} - {mda.name}")
        print(f"  Head: {mda.head_of_mda or 'Not set'}")
        print(f"  Email: {mda.contact_email or 'Not set'}")
        print(f"  Phone: {mda.contact_phone or 'Not set'}")
        print(f"  Website: {mda.website or 'Not set'}")

print("\n" + "=" * 80)
print("END OF REPORT")
print("=" * 80)
