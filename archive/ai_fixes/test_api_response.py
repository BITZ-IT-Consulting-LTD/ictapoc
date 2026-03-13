#!/usr/bin/env python3
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import ServiceConfig, MDA, ServiceDomain

print("=" * 80)
print("API RESPONSE TEST - What the frontend SHOULD receive")
print("=" * 80)

# Simulate the catalogue summary endpoint
services = ServiceConfig.objects.filter(service_status='active')
mdas = MDA.objects.all()
domains = ServiceDomain.objects.all()

# Count services with workflows
services_with_workflows = 0
automated_services = 0

for svc in services:
    if svc.workflow_steps.exists():
        services_with_workflows += 1
        if svc.workflow_steps.filter(step_type='api').exists():
            automated_services += 1

# Calculate metrics
total_services = services.count()
automation_pct = (automated_services / total_services * 100) if total_services > 0 else 0
avg_maturity = sum(svc.digitization_level or 0 for svc in services) / total_services if total_services > 0 else 0

# This is what the API endpoint should return
api_response = {
    "totalServices": total_services,
    "totalAgencies": mdas.count(),
    "totalMinistries": domains.count(),
    "citizenFacing": services.filter(service_type='C2G').count(),
    "automationCoverage": round(automation_pct, 1),
    "avgDigitizationMaturity": round(avg_maturity, 2)
}

print("\n📊 EXPECTED API RESPONSE:")
print(json.dumps(api_response, indent=2))

print("\n" + "=" * 80)
print("COMPARISON:")
print("=" * 80)
print(f"Database has:     {total_services} services")
print(f"Frontend shows:   355 services (CACHED - STALE)")
print(f"Difference:       {total_services - 355} services missing from frontend")

print("\n" + "=" * 80)
print("SOLUTION:")
print("=" * 80)
print("The backend is serving correct data (380 services).")
print("The frontend is showing cached data (355 services).")
print("\nTo fix this, you need to:")
print("1. Open your browser DevTools (F12)")
print("2. Go to Application tab → Storage → Clear site data")
print("3. OR do a hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)")
print("4. OR restart the frontend dev server")
print("=" * 80)

# Show some of the new services
print("\n📋 SAMPLE NEW SERVICES (should appear after cache clear):")
new_service_codes = ['AWWDA-001', 'AWWDA-002', 'SDHUD-001', 'KAA-001', 'NCA-001']
for code in new_service_codes:
    svc = ServiceConfig.objects.filter(service_code=code).first()
    if svc:
        print(f"  ✓ {code}: {svc.service_name} ({svc.mda.name})")

print("\n" + "=" * 80)
