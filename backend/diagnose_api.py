#!/usr/bin/env python3
"""
Diagnostic script to verify all 380 services are accessible via API
"""
import requests
import json

API_URL = "http://localhost:8000/api/catalog/services/process_matrix/"

print("=" * 80)
print("WOG CATALOGUE API DIAGNOSTIC")
print("=" * 80)

try:
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    # Count services
    total_services = 0
    services_by_domain = {}
    new_mdas = {}
    
    new_mda_codes = ['AWWDA', 'TWWDA', 'SDHUD', 'SDCS', 'SDMS', 'SDBT', 'SDPW', 
                     'SDSRI', 'KAA', 'KPA', 'KRC', 'NCA', 'NLC']
    
    for domain in data:
        domain_name = domain['domain_name']
        domain_service_count = 0
        
        for process in domain.get('processes', []):
            for service in process.get('services', []):
                total_services += 1
                domain_service_count += 1
                
                mda_code = service.get('mda_code', '')
                if mda_code in new_mda_codes:
                    if mda_code not in new_mdas:
                        new_mdas[mda_code] = []
                    new_mdas[mda_code].append({
                        'code': service.get('service_code'),
                        'name': service.get('service_name'),
                        'mda': service.get('mda')
                    })
        
        services_by_domain[domain_name] = domain_service_count
    
    print(f"\n✅ API RESPONSE SUCCESSFUL")
    print(f"\n📊 OVERALL STATISTICS:")
    print(f"  Total Domains: {len(data)}")
    print(f"  Total Services: {total_services}")
    print(f"  New MDAs Found: {len(new_mdas)}")
    print(f"  New Services Found: {sum(len(svcs) for svcs in new_mdas.values())}")
    
    print(f"\n📋 SERVICES BY DOMAIN (Top 10):")
    for domain, count in sorted(services_by_domain.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {domain:50s}: {count:3d} services")
    
    print(f"\n🆕 NEWLY ADDED MDAs AND SERVICES:")
    for mda_code in sorted(new_mdas.keys()):
        services = new_mdas[mda_code]
        print(f"\n  {mda_code} - {services[0]['mda']} ({len(services)} services):")
        for svc in services:
            print(f"    • {svc['code']}: {svc['name']}")
    
    print(f"\n{'=' * 80}")
    print(f"RESULT: API is serving {total_services} services correctly")
    print(f"{'=' * 80}")
    
    if total_services == 380:
        print("\n✅ SUCCESS: All 380 services are accessible via API")
        print("\nIf frontend still shows 355:")
        print("1. Clear browser cache (Cmd+Shift+Delete)")
        print("2. Hard refresh (Cmd+Shift+R)")
        print("3. Check browser console for errors (F12)")
        print("4. Verify frontend is calling the correct API endpoint")
    else:
        print(f"\n⚠️  WARNING: Expected 380 services, got {total_services}")
    
except requests.exceptions.ConnectionError:
    print("\n❌ ERROR: Cannot connect to backend server")
    print("   Make sure Django server is running on http://localhost:8000")
except requests.exceptions.Timeout:
    print("\n❌ ERROR: Request timed out")
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")

print()
