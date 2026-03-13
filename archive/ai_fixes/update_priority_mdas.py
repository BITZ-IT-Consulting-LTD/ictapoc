import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep

# 17 Priority MDAs with their details
PRIORITY_MDAS = [
    {
        "name": "Department of Immigration Services",
        "code": "DIS",
        "head": "Director of Immigration Services",
        "email": "info@immigration.go.ke",
        "phone": "+254-20-2222022",
        "website": "https://www.immigration.go.ke",
        "address": "Nyayo House, Kenyatta Avenue, Nairobi"
    },
    {
        "name": "National Registration Bureau",
        "code": "NRB",
        "head": "Principal Registrar of Persons",
        "email": "info@nrb.go.ke",
        "phone": "+254-20-2227411",
        "website": "https://www.nrb.go.ke",
        "address": "Huduma Centre, GPO, Nairobi"
    },
    {
        "name": "Kenya Revenue Authority",
        "code": "KRA",
        "head": "Commissioner General",
        "email": "callcentre@kra.go.ke",
        "phone": "+254-20-4999999",
        "website": "https://www.kra.go.ke",
        "address": "Times Tower, Haile Selassie Avenue, Nairobi"
    },
    {
        "name": "National Transport and Safety Authority",
        "code": "NTSA",
        "head": "Director General",
        "email": "info@ntsa.go.ke",
        "phone": "+254-20-2211111",
        "website": "https://www.ntsa.go.ke",
        "address": "Upper Hill, Nairobi"
    },
    {
        "name": "Teachers Service Commission",
        "code": "TSC",
        "head": "Secretary/CEO",
        "email": "info@tsc.go.ke",
        "phone": "+254-20-2721620",
        "website": "https://www.tsc.go.ke",
        "address": "Kilimanjaro Road, Upper Hill, Nairobi"
    },
    {
        "name": "Higher Education Loans Board",
        "code": "HELB",
        "head": "Chief Executive Officer",
        "email": "info@helb.co.ke",
        "phone": "+254-20-2211120",
        "website": "https://www.helb.co.ke",
        "address": "HELB Towers, Harambee Avenue, Nairobi"
    },
    {
        "name": "Commission for University Education",
        "code": "CUE",
        "head": "Secretary/CEO",
        "email": "info@cue.or.ke",
        "phone": "+254-20-2211120",
        "website": "https://www.cue.or.ke",
        "address": "Red Hill Road, Nairobi"
    },
    {
        "name": "Kenya National Examinations Council",
        "code": "KNEC",
        "head": "Chief Executive Officer",
        "email": "info@knec.ac.ke",
        "phone": "+254-20-3317870",
        "website": "https://www.knec.ac.ke",
        "address": "Mitihani House, South C, Nairobi"
    },
    {
        "name": "National Health Insurance Fund",
        "code": "NHIF",
        "head": "Chief Executive Officer",
        "email": "customercare@nhif.or.ke",
        "phone": "+254-20-2717171",
        "website": "https://www.nhif.or.ke",
        "address": "Ragati Road, Upper Hill, Nairobi"
    },
    {
        "name": "National Social Security Fund",
        "code": "NSSF",
        "head": "Managing Trustee",
        "email": "info@nssfkenya.co.ke",
        "phone": "+254-20-2729000",
        "website": "https://www.nssfkenya.co.ke",
        "address": "NSSF Building, Eastern Wing, Block A, Nairobi"
    },
    {
        "name": "National Employment Authority",
        "code": "NEA",
        "head": "Director General",
        "email": "info@nea.go.ke",
        "phone": "+254-20-2211120",
        "website": "https://www.nea.go.ke",
        "address": "Social Security House, Nairobi"
    },
    {
        "name": "Registrar of Companies",
        "code": "ROC",
        "head": "Registrar of Companies",
        "email": "info@businessregistration.go.ke",
        "phone": "+254-20-2211120",
        "website": "https://www.businessregistration.go.ke",
        "address": "Sheria House, Harambee Avenue, Nairobi"
    },
    {
        "name": "Communications Authority of Kenya",
        "code": "CA",
        "head": "Director General",
        "email": "info@ca.go.ke",
        "phone": "+254-20-4242000",
        "website": "https://www.ca.go.ke",
        "address": "Waiyaki Way, Nairobi"
    },
    {
        "name": "Office of the Data Protection Commissioner",
        "code": "ODPC",
        "head": "Data Protection Commissioner",
        "email": "info@odpc.go.ke",
        "phone": "+254-20-2211120",
        "website": "https://www.odpc.go.ke",
        "address": "Nairobi"
    },
    {
        "name": "State Department for ICT",
        "code": "ICT",
        "head": "Principal Secretary",
        "email": "ps@ict.go.ke",
        "phone": "+254-20-2211120",
        "website": "https://www.ict.go.ke",
        "address": "Teleposta Towers, Nairobi"
    },
    {
        "name": "Kenya Wildlife Service",
        "code": "KWS",
        "head": "Director General",
        "email": "info@kws.go.ke",
        "phone": "+254-20-6000800",
        "website": "https://www.kws.go.ke",
        "address": "Langata Road, Nairobi"
    },
    {
        "name": "National Environment Management Authority",
        "code": "NEMA",
        "head": "Director General",
        "email": "dgnema@nema.go.ke",
        "phone": "+254-20-2183056",
        "website": "https://www.nema.go.ke",
        "address": "Popo Road, South C, Nairobi"
    }
]

print("=== UPDATING 17 PRIORITY MDAs ===\n")

updated_count = 0
not_found = []

for mda_data in PRIORITY_MDAS:
    try:
        # Try to find existing MDA by name (case-insensitive partial match)
        mda = MDA.objects.filter(name__icontains=mda_data["name"]).first()
        
        if mda:
            # Update existing MDA
            mda.code = mda_data["code"]
            mda.head_of_mda = mda_data["head"]
            mda.contact_email = mda_data["email"]
            mda.contact_phone = mda_data["phone"]
            mda.website = mda_data["website"]
            mda.address = mda_data["address"]
            mda.save()
            
            service_count = ServiceConfig.objects.filter(mda=mda).count()
            print(f"✓ Updated: {mda.name} ({mda.code}) - {service_count} services")
            updated_count += 1
        else:
            not_found.append(mda_data["name"])
            print(f"✗ Not found: {mda_data['name']}")
            
    except Exception as e:
        print(f"✗ Error updating {mda_data['name']}: {str(e)}")

print(f"\n=== SUMMARY ===")
print(f"Updated: {updated_count}/{len(PRIORITY_MDAS)}")
if not_found:
    print(f"\nNot found in database:")
    for name in not_found:
        print(f"  - {name}")
