import os
import django
import json

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import RegistryAdapter, RegistryEndpoint

def seed_registry_adapters():
    print("🚀 SEEDING REGISTRY ADAPTERS (GEA COMPLIANT)")
    
    # 1. CLEAN SLATE (Optional, but good for POC)
    # RegistryAdapter.objects.all().delete()

    adapters = [
        {
            "code": "IPRS",
            "name": "Integrated Population Registration System",
            "base_url": "https://api.iprs.go.ke",
            "endpoints": [
                {"name": "Verify Citizen Identity", "path": "/api/v1/citizens/verify", "method": "GET"},
                {"name": "Get Citizen Details", "path": "/api/v1/citizens/{id}", "method": "GET"},
            ],
            "mock_data": {
                "12345678": {"full_name": "JOHN DOE", "status": "ALIVE", "dob": "1990-01-01", "gender": "MALE", "occupation": "SOFTWARE ENGINEER", "residence": "NAIROBI"},
                "22222222": {"full_name": "JANE DOE", "status": "ALIVE", "dob": "1995-05-05", "gender": "FEMALE", "occupation": "DOCTOR", "residence": "MOMBASA"},
                "33333333": {"full_name": "PETER OMONDI", "status": "ALIVE", "dob": "1988-11-12", "gender": "MALE", "occupation": "TEACHER", "residence": "KISUMU"},
                "44444444": {"full_name": "SARAH CHERONO", "status": "ALIVE", "dob": "1992-03-24", "gender": "FEMALE", "occupation": "ACCOUNTANT", "residence": "ELDORET"},
                "55555555": {"full_name": "MOHAMMED HASSAN", "status": "ALIVE", "dob": "1985-07-07", "gender": "MALE", "occupation": "BUSINESSMAN", "residence": "GARISSA"},
                "ID-MOTHER-001": {"full_name": "MARY MOTHER", "status": "ALIVE", "dob": "1980-05-10", "gender": "FEMALE"},
                "ID-FATHER-001": {"full_name": "JOSEPH FATHER", "status": "ALIVE", "dob": "1978-08-15", "gender": "MALE"},
            }
        },
        {
            "code": "NRB",
            "name": "National Registration Bureau",
            "base_url": "https://api.nrb.go.ke",
            "endpoints": [
                {"name": "Check ID Card Status", "path": "/api/cards/status/{serial_no}", "method": "GET"},
                {"name": "Request ID Replacement", "path": "/api/cards/replace", "method": "POST"},
                {"name": "Mint Maisha Namba", "path": "/api/v1/upi/mint", "method": "POST"},
            ],
            "mock_data": {
                "12345678": {"serial_no": "99887766", "issue_date": "2010-01-01", "station": "NAIROBI CENTRAL", "status": "ISSUED", "card_type": "MAISHA_CARD"},
                "22222222": {"serial_no": "11223344", "issue_date": "2015-05-05", "station": "MOMBASA EAST", "status": "ISSUED", "card_type": "2ND_GEN_ID"},
                "33333333": {"serial_no": "55667788", "issue_date": "2018-09-12", "station": "KISUMU WEST", "status": "ISSUED", "card_type": "MAISHA_CARD"},
                "44444444": {"serial_no": "22334455", "issue_date": "2020-11-20", "station": "ELDORET NORTH", "status": "PENDING_COLLECTION", "card_type": "MAISHA_CARD"},
            }
        },
        {
            "code": "CRS",
            "name": "Civil Registration Services",
            "base_url": "https://api.crs.go.ke",
            "endpoints": [
                {"name": "Notify Birth", "path": "/api/births/notify", "method": "POST"},
                {"name": "Register Birth", "path": "/api/births/register", "method": "POST"},
                {"name": "Get Birth Certificate", "path": "/api/certificates/birth/{id}", "method": "GET"},
                {"name": "Notify Death", "path": "/api/deaths/notify", "method": "POST"},
                {"name": "Issue Death Certificate", "path": "/api/certificates/death/issue", "method": "POST"},
            ],
            "mock_data": {
                "BC-111": {"full_name": "JAMES DOE JNR", "event": "BIRTH", "date": "2006-05-15", "mother": "MARY MOTHER", "place": "PUMWANI HOSPITAL"},
                "BC-112": {"full_name": "ALICE WANJIKU", "event": "BIRTH", "date": "2023-10-01", "mother": "JANE DOE", "place": "KNH"},
                "BC-113": {"full_name": "BRIAN KIPROTICH", "event": "BIRTH", "date": "2024-02-14", "mother": "SARAH CHERONO", "place": "MEDIHEAL ELDORET"},
                "DC-999": {"full_name": "SARAH LATE", "event": "DEATH", "date": "2024-01-01", "cert_no": "D-1234", "cause": "NATURAL_CAUSES"},
                "NOTIF-123456": {"full_name": "BABY DOE", "event": "BIRTH_NOTIFICATION", "date": "2024-03-01", "mother": "JANE DOE", "place": "KNH", "status": "PENDING_CERTIFICATE"}
            }
        },
        {
            "code": "IMMIGRATION",
            "name": "Department of Immigration Services",
            "base_url": "https://api.immigration.go.ke",
            "endpoints": [
                {"name": "Check Passport Status", "path": "/api/passports/status", "method": "GET"},
                {"name": "Apply for Passport", "path": "/api/passports/apply", "method": "POST"},
                {"name": "Verify Visa", "path": "/api/visas/verify", "method": "POST"},
            ],
            "mock_data": {
                "AK001": {"name": "JOHN DOE", "type": "PASSPORT", "number": "AK001", "expiry": "2030-01-01", "status": "ACTIVE"},
                "AK002": {"name": "JANE DOE", "type": "PASSPORT", "number": "AK002", "expiry": "2032-05-05", "status": "EXPIRED"},
                "AK003": {"name": "PETER OMONDI", "type": "PASSPORT", "number": "AK003", "expiry": "2031-11-12", "status": "ACTIVE"},
                "V-888": {"name": "ALICE SMITH", "type": "VISA", "expiry": "2024-12-31", "status": "VALID"}
            }
        },
        {
            "code": "BRS",
            "name": "Business Registration Service",
            "base_url": "https://api.brs.go.ke",
            "endpoints": [
                {"name": "Search Business Name", "path": "/api/businesses/search", "method": "GET"},
                {"name": "Reserve Business Name", "path": "/api/businesses/reserve", "method": "POST"},
                {"name": "Register Company", "path": "/api/companies/register", "method": "POST"},
            ],
            "mock_data": {
                "PVT-123": {"name": "TECH SOLUTIONS LTD", "type": "COMPANY", "inc_date": "2020-01-01", "status": "ACTIVE", "directors": ["JOHN DOE", "JANE DOE"]},
                "PVT-456": {"name": "GLOBAL LOGISTICS KE", "type": "COMPANY", "inc_date": "2015-05-10", "status": "ACTIVE", "directors": ["PETER OMONDI"]},
                "BN-987": {"name": "MAMA MBOGA SHOP", "type": "BUSINESS NAME", "owner": "JANE DOE", "status": "ACTIVE"},
                "BN-555": {"name": "JUA KALI AUTO", "type": "BUSINESS NAME", "owner": "MOHAMMED HASSAN", "status": "DISSOLVED"}
            }
        },
        {
            "code": "KRA",
            "name": "Kenya Revenue Authority",
            "base_url": "https://api.kra.go.ke",
            "endpoints": [
                {"name": "Verify PIN", "path": "/api/taxpayers/verify", "method": "GET"},
                {"name": "Check Tax Compliance", "path": "/api/compliance/status", "method": "GET"},
                {"name": "File Returns", "path": "/api/returns/file", "method": "POST"},
            ],
            "mock_data": {
                "A001234567Z": {"name": "JOHN DOE", "pin_type": "INDIVIDUAL", "status": "COMPLIANT", "tax_agent": "TAX_SOLUTIONS"},
                "A009988776B": {"name": "JANE DOE", "pin_type": "INDIVIDUAL", "status": "COMPLIANT"},
                "A005544332C": {"name": "PETER OMONDI", "pin_type": "INDIVIDUAL", "status": "NON_COMPLIANT"},
                "P098765432W": {"name": "TECH SOLUTIONS LTD", "pin_type": "NON_INDIVIDUAL", "status": "COMPLIANT"}
            }
        },
        {
            "code": "NEMIS",
            "name": "National Education Management Information System",
            "base_url": "https://api.nemis.go.ke",
            "endpoints": [
                {"name": "Verify Student UPI", "path": "/api/students/verify", "method": "GET"},
                {"name": "Enroll Student", "path": "/api/enrollment/create", "method": "POST"},
            ],
            "mock_data": {
                "UPI-1122": {"name": "JAMES DOE JNR", "school": "NAIROBI SCHOOL", "status": "ENROLLED", "level": "SECONDARY"},
                "UPI-3344": {"name": "ALICE WANJIKU", "school": "ALLIANCE GIRLS", "status": "ACTIVE", "level": "SECONDARY"},
                "UPI-5566": {"name": "BRIAN KIPROTICH", "school": "STAREHE BOYS", "status": "ENROLLED", "level": "SECONDARY"}
            }
        },
        {
            "code": "SHA",
            "name": "Social Health Authority",
            "base_url": "https://api.sha.go.ke",
            "endpoints": [
                {"name": "Check Membership Status", "path": "/api/members/status", "method": "GET"},
                {"name": "Register Member", "path": "/api/members/register", "method": "POST"},
            ],
            "mock_data": {
                "SHA-12345678": {"name": "JOHN DOE", "id": "12345678", "category": "NATIONAL", "status": "ACTIVE", "cover": "UHC_STANDARD"},
                "SHA-22222222": {"name": "JANE DOE", "id": "22222222", "category": "ENHANCED", "status": "ACTIVE", "cover": "UHC_PREMIUM"},
                "SHA-999": {"name": "ALICE SMITH", "category": "NATIONAL", "status": "ACTIVE"}
            }
        },
        {
            "code": "NSSF",
            "name": "National Social Security Fund",
            "base_url": "https://api.nssf.go.ke",
            "endpoints": [
                {"name": "Check Contributions", "path": "/api/contributions/summary", "method": "GET"},
            ],
            "mock_data": {
                "NSSF-123": {"name": "JOHN DOE", "balance": "150,000", "status": "CONTRIBUTING"},
                "NSSF-999": {"name": "JANE DOE", "balance": "250,000", "status": "ACTIVE"}
            }
        },
        {
            "code": "JUDICIARY",
            "name": "Judiciary Case Tracking System",
            "base_url": "https://api.judiciary.go.ke",
            "endpoints": [
                {"name": "Search Cases", "path": "/api/cases/search", "method": "GET"},
            ],
            "mock_data": {
                "MCC/123/2024": {"title": "REPUBLIC vs CITIZEN", "court": "MILIMANI LAW COURTS", "status": "PENDING", "judge": "HON. JUSTICE MUYA"},
                "DL/456/2023": {"title": "DOE vs BANK", "court": "HIGH COURT NAIROBI", "status": "DISMISSED"}
            }
        },
        {
            "code": "GAZETTE",
            "name": "Kenya Gazette",
            "endpoints": [],
            "mock_data": {
                "GZ-2024-001": {"title": "APPOINTMENT OF ICTA BOARD", "date": "2024-01-05", "status": "PUBLISHED"},
                "GZ-2024-050": {"title": "CHANGE OF NAME - JANE DOE", "date": "2024-02-10", "status": "PUBLISHED"}
            }
        },
        {
            "code": "IEBC",
            "name": "Independent Electoral and Boundaries Commission",
            "endpoints": [],
            "mock_data": {
                "12345678": {"name": "JOHN DOE", "constituency": "STAREHE", "center": "CITY HALL", "status": "REGISTERED"},
                "22222222": {"name": "JANE DOE", "constituency": "MVITA", "center": "MAKADARA", "status": "REGISTERED"}
            }
        },
        {
            "code": "HELB",
            "name": "Higher Education Loans Board",
            "endpoints": [],
            "mock_data": {
                "12345678": {"name": "JOHN DOE", "amount": "140,000", "status": "REPAYING", "compliance": "COMPLIANT"},
                "22222222": {"name": "JANE DOE", "amount": "200,000", "status": "PAID_OFF", "compliance": "COMPLIANT"}
            }
        },
        {
            "code": "KNEC",
            "name": "Kenya National Examinations Council",
            "endpoints": [],
            "mock_data": {
                "12345678/001": {"name": "JOHN DOE", "exam": "KCSE", "year": "2008", "grade": "B+"},
                "22222222/050": {"name": "JANE DOE", "exam": "KCSE", "year": "2013", "grade": "A-"}
            }
        },
        {
            "code": "TSC",
            "name": "Teachers Service Commission",
            "endpoints": [],
            "mock_data": {
                "TSC-33333333": {"name": "PETER OMONDI", "station": "NAIROBI SCHOOL", "status": "ACTIVE", "role": "SENIOR TEACHER"}
            }
        },
        {
            "code": "MAISHA_AUTH",
            "name": "Maisha Digital ID Authentication",
            "endpoints": [],
            "mock_data": {
                "12345678": {"status": "VERIFIED", "credential": "DTC-9988", "last_login": "2024-02-18"}
            }
        },
        {
            "code": "LIVESCAN_KIT",
            "name": "Biometric LiveScan Service",
            "endpoints": [],
            "mock_data": {
                "DEV-001": {"location": "HUDUMA_GPO", "status": "ONLINE", "last_sync": "2024-02-19"}
            }
        },
        {
            "code": "ECITIZEN_APP",
            "name": "eCitizen Portal Registry",
            "endpoints": [],
            "mock_data": {
                "12345678": {"name": "JOHN DOE", "email": "john.doe@example.com", "phone": "0711122233", "verified": True},
                "22222222": {"name": "JANE DOE", "email": "jane.doe@example.com", "phone": "0722233344", "verified": True}
            }
        },
        {
            "code": "HOSPITAL",
            "name": "National Health Facility Registry",
            "endpoints": [],
            "mock_data": {
                "HOSP-001": {"name": "Kenyatta National Hospital", "level": "Level 6", "location": "Nairobi"},
                "HOSP-002": {"name": "Coast General Hospital", "level": "Level 5", "location": "Mombasa"},
                "HOSP-003": {"name": "Mbagathi Hospital", "level": "Level 4", "location": "Nairobi"}
            }
        },
        {
            "code": "HOSPITAL_HIS",
            "name": "Hospital HIS Patient Records",
            "endpoints": [],
            "mock_data": {
                "12345678": {"name": "JOHN DOE", "blood_group": "A+", "allergies": ["PENICILLIN"]},
                "22222222": {"name": "JANE DOE", "blood_group": "O-", "allergies": []}
            }
        },
        {
            "code": "ARDHISASA",
            "name": "National Land Information System",
            "base_url": "https://api.ardhisasa.go.ke",
            "endpoints": [
                {"name": "Search Land Title", "path": "/api/titles/search", "method": "GET"},
                {"name": "Verify Ownership", "path": "/api/ownership/verify", "method": "POST"},
            ],
            "mock_data": {
                "NRB/01/123": {"owner": "JOHN DOE", "location": "UPPERHILL", "status": "CLEAN", "acreage": "0.5"},
                "NRB/05/999": {"owner": "JANE DOE", "location": "KAREN", "status": "CLEAN", "acreage": "2.0"},
                "MSA/02/456": {"owner": "PETER OMONDI", "location": "NYALI", "status": "CHARGED", "chargee": "KCB BANK"}
            }
        },
        {
            "code": "SCHOOLS_REGISTRY",
            "name": "National Schools Registry",
            "base_url": "https://api.education.go.ke/schools",
            "endpoints": [
                {"name": "Search Schools", "path": "/api/v1/schools/search", "method": "GET"},
                {"name": "Get School Details", "path": "/api/v1/schools/{code}", "method": "GET"},
                {"name": "Verify School Capacity", "path": "/api/v1/schools/{code}/capacity", "method": "GET"},
            ],
            "mock_data": {
                "SCH-20101": {"name": "NAIROBI SCHOOL", "level": "SECONDARY", "county": "NAIROBI", "capacity": 1200, "enrolled": 1150, "geo_location": "-1.2587, 36.7691"},
                "SCH-30102": {"name": "ALLIANCE GIRLS HIGH SCHOOL", "level": "SECONDARY", "county": "KIAMBU", "capacity": 1500, "enrolled": 1480, "geo_location": "-1.1819, 36.6581"},
                "SCH-40103": {"name": "STAREHE BOYS CENTRE", "level": "SECONDARY", "county": "NAIROBI", "capacity": 1000, "enrolled": 980, "geo_location": "-1.2721, 36.8354"},
                "SCH-10101": {"name": "MANG'U HIGH SCHOOL", "level": "SECONDARY", "county": "KIAMBU", "capacity": 1300, "enrolled": 1250, "geo_location": "-1.0964, 37.0131"}
            }
        }
    ]

    for adapter_data in adapters:
        adapter, created = RegistryAdapter.objects.update_or_create(
            code=adapter_data["code"],
            defaults={
                "name": adapter_data["name"],
                "base_url": adapter_data.get("base_url"),
                "mock_data": adapter_data["mock_data"],
                "is_mock": True
            }
        )
        status = "Created" if created else "Updated"
        print(f"  ✅ {status} Adapter: {adapter.code}")

        # Seed Endpoints
        endpoints = adapter_data.get("endpoints", [])
        RegistryEndpoint.objects.filter(adapter=adapter).delete()
        for ep in endpoints:
            RegistryEndpoint.objects.create(
                adapter=adapter,
                name=ep["name"],
                path=ep["path"],
                method=ep["method"]
            )

    print("\n✨ REGISTRY ADAPTER SEEDING COMPLETE.")

if __name__ == "__main__":
    seed_registry_adapters()
