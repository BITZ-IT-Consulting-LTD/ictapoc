import random

class MockRegistry:
    """Base class for authoritative registries."""
    def query(self, params):
        raise NotImplementedError 

class IPRS(MockRegistry):
    """Integrated Population Registration System (Identity)."""
    CITIZENS = {
        "12345678": {"full_name": "JOHN DOE", "status": "ALIVE", "dob": "1990-01-01", "gender": "MALE", "occupation": "SOFTWARE ENGINEER", "residence": "NAIROBI"},
        "22222222": {"full_name": "JANE DOE", "status": "ALIVE", "dob": "1995-05-05", "gender": "FEMALE", "occupation": "DOCTOR", "residence": "MOMBASA"},
        "33333333": {"full_name": "PETER OMONDI", "status": "ALIVE", "dob": "1988-11-12", "gender": "MALE", "occupation": "TEACHER", "residence": "KISUMU"},
        "44444444": {"full_name": "SARAH CHERONO", "status": "ALIVE", "dob": "1992-03-24", "gender": "FEMALE", "occupation": "ACCOUNTANT", "residence": "ELDORET"},
        "55555555": {"full_name": "MOHAMMED HASSAN", "status": "ALIVE", "dob": "1985-07-07", "gender": "MALE", "occupation": "BUSINESSMAN", "residence": "GARISSA"},
        "ID-MOTHER-001": {"full_name": "MARY MOTHER", "status": "ALIVE", "dob": "1980-05-10", "gender": "FEMALE"},
        "ID-FATHER-001": {"full_name": "JOSEPH FATHER", "status": "ALIVE", "dob": "1978-08-15", "gender": "MALE"},
    }
    def query(self, params):
        cid = params.get('id_number') or params.get('identifier')
        if cid in self.CITIZENS:
            return {"status": "SUCCESS", "source": "IPRS", "data": self.CITIZENS[cid]}
        return {"status": "NOT_FOUND", "message": f"ID {cid} not found in IPRS"}

class NRB(MockRegistry):
    """National Registration Bureau (ID Cards)."""
    CARDS = {
        "12345678": {"serial_no": "99887766", "issue_date": "2010-01-01", "station": "NAIROBI CENTRAL", "status": "ISSUED", "card_type": "MAISHA_CARD"},
        "22222222": {"serial_no": "11223344", "issue_date": "2015-05-05", "station": "MOMBASA EAST", "status": "ISSUED", "card_type": "2ND_GEN_ID"},
        "33333333": {"serial_no": "55667788", "issue_date": "2018-09-12", "station": "KISUMU WEST", "status": "ISSUED", "card_type": "MAISHA_CARD"},
        "44444444": {"serial_no": "22334455", "issue_date": "2020-11-20", "station": "ELDORET NORTH", "status": "PENDING_COLLECTION", "card_type": "MAISHA_CARD"},
    }
    def query(self, params):
        cid = params.get('id_number') or params.get('identifier')
        if cid in self.CARDS:
            return {"status": "SUCCESS", "source": "NRB", "data": self.CARDS[cid]}
        return {"status": "NOT_FOUND", "message": f"ID {cid} not found in NRB"}

class CRS(MockRegistry):
    """Civil Registration Services (Births/Deaths)."""
    RECORDS = {
        "BC-111": {"full_name": "JAMES DOE JNR", "event": "BIRTH", "date": "2006-05-15", "mother": "MARY MOTHER", "place": "PUMWANI HOSPITAL"},
        "BC-112": {"full_name": "ALICE WANJIKU", "event": "BIRTH", "date": "2023-10-01", "mother": "JANE DOE", "place": "KNH"},
        "BC-113": {"full_name": "BRIAN KIPROTICH", "event": "BIRTH", "date": "2024-02-14", "mother": "SARAH CHERONO", "place": "MEDIHEAL ELDORET"},
        "DC-999": {"full_name": "SARAH LATE", "event": "DEATH", "date": "2024-01-01", "cert_no": "D-1234", "cause": "NATURAL_CAUSES"}
    }
    def query(self, params):
        bid = params.get('birth_certificate_number') or params.get('identifier')
        if bid in self.RECORDS:
            return {"status": "SUCCESS", "source": "CRS", "data": self.RECORDS[bid]}
        return {"status": "NOT_FOUND", "message": f"Record {bid} not found in CRS"}

class Immigration(MockRegistry):
    """Department of Immigration Services."""
    DOCUMENTS = {
        "AK001": {"name": "JOHN DOE", "type": "PASSPORT", "number": "AK001", "expiry": "2030-01-01", "status": "ACTIVE"},
        "AK002": {"name": "JANE DOE", "type": "PASSPORT", "number": "AK002", "expiry": "2032-05-05", "status": "EXPIRED"},
        "AK003": {"name": "PETER OMONDI", "type": "PASSPORT", "number": "AK003", "expiry": "2031-11-12", "status": "ACTIVE"},
        "V-888": {"name": "ALICE SMITH", "type": "VISA", "expiry": "2024-12-31", "status": "VALID"}
    }
    def query(self, params):
        doc_id = params.get('passport_number') or params.get('identifier')
        if doc_id in self.DOCUMENTS:
            return {"status": "SUCCESS", "source": "Immigration", "data": self.DOCUMENTS[doc_id]}
        return {"status": "NOT_FOUND", "message": f"Document {doc_id} not found"}

class BRS(MockRegistry):
    """Business Registration Service."""
    ENTITIES = {
        "PVT-123": {"name": "TECH SOLUTIONS LTD", "type": "COMPANY", "inc_date": "2020-01-01", "status": "ACTIVE", "directors": ["JOHN DOE", "JANE DOE"]},
        "PVT-456": {"name": "GLOBAL LOGISTICS KE", "type": "COMPANY", "inc_date": "2015-05-10", "status": "ACTIVE", "directors": ["PETER OMONDI"]},
        "BN-987": {"name": "MAMA MBOGA SHOP", "type": "BUSINESS NAME", "owner": "JANE DOE", "status": "ACTIVE"},
        "BN-555": {"name": "JUA KALI AUTO", "type": "BUSINESS NAME", "owner": "MOHAMMED HASSAN", "status": "DISSOLVED"}
    }
    def query(self, params):
        eid = params.get('entity_id') or params.get('identifier')
        if eid in self.ENTITIES:
            return {"status": "SUCCESS", "source": "BRS", "data": self.ENTITIES[eid]}
        return {"status": "NOT_FOUND", "message": f"Entity {eid} not found in BRS"}

class KRA(MockRegistry):
    """Kenya Revenue Authority."""
    PINS = {
        "A001234567Z": {"name": "JOHN DOE", "pin_type": "INDIVIDUAL", "status": "COMPLIANT", "tax_agent": "TAX_SOLUTIONS"},
        "A009988776B": {"name": "JANE DOE", "pin_type": "INDIVIDUAL", "status": "COMPLIANT"},
        "A005544332C": {"name": "PETER OMONDI", "pin_type": "INDIVIDUAL", "status": "NON_COMPLIANT"},
        "P098765432W": {"name": "TECH SOLUTIONS LTD", "pin_type": "NON_INDIVIDUAL", "status": "COMPLIANT"}
    }
    def query(self, params):
        pin = params.get('pin') or params.get('identifier')
        if pin in self.PINS:
            return {"status": "SUCCESS", "source": "KRA", "data": self.PINS[pin]}
        return {"status": "NOT_FOUND", "message": f"PIN {pin} not found in KRA"}

class NGOBoard(MockRegistry):
    """NGO Coordination Board."""
    ENTITIES = {
        "NGO-001": {"name": "SAVE THE PLANET", "sector": "ENVIRONMENT", "status": "REGISTERED"},
        "NGO-002": {"name": "HELP KENYA", "sector": "HEALTH", "status": "ACTIVE"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class Ardhisasa(MockRegistry):
    """National Land Information Management System."""
    TITLES = {
        "NRB/01/123": {"owner": "JOHN DOE", "location": "UPPERHILL", "status": "CLEAN", "acreage": "0.5"},
        "NRB/05/999": {"owner": "JANE DOE", "location": "KAREN", "status": "CLEAN", "acreage": "2.0"},
        "MSA/02/456": {"owner": "PETER OMONDI", "location": "NYALI", "status": "CHARGED", "chargee": "KCB BANK"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class CollateralRegistry(MockRegistry):
    """Movable assets registry."""
    ASSETS = {
        "CR-001": {"owner": "JOHN DOE", "asset": "TOYOTA HILUX", "lien": "ABC BANK", "status": "ACTIVE"},
        "CR-002": {"owner": "JANE DOE", "asset": "INDUSTRIAL LATHE", "lien": "EQUITY BANK", "status": "ACTIVE"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class NTSA(MockRegistry):
    """National Transport and Safety Authority."""
    RECORDS = {
        "KAA 001A": {"owner": "JOHN DOE", "type": "VEHICLE_LOGBOOK", "status": "VALID", "make": "TOYOTA"},
        "KBC 555X": {"owner": "JANE DOE", "type": "VEHICLE_LOGBOOK", "status": "VALID", "make": "MAZDA"},
        "DL-9988": {"name": "JOHN DOE", "type": "DRIVING_LICENSE", "expiry": "2027-01-01", "status": "VALID"},
        "DL-1122": {"name": "PETER OMONDI", "type": "DRIVING_LICENSE", "expiry": "2025-05-10", "status": "VALID"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class KCAA(MockRegistry):
    """Kenya Civil Aviation Authority."""
    AIRCRAFT = {
        "5Y-XYZ": {"owner": "FLY KENYA", "model": "REIMS-CESSNA 172", "status": "AIRWORTHY"},
        "5Y-ABC": {"owner": "NAIROBI AERO", "model": "BOEING 737", "status": "AIRWORTHY"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class NEMIS(MockRegistry):
    """National Education Management Information System."""
    LEARNERS = {
        "UPI-1122": {"name": "JAMES DOE JNR", "school": "NAIROBI SCHOOL", "status": "ENROLLED", "level": "SECONDARY"},
        "UPI-3344": {"name": "ALICE WANJIKU", "school": "ALLIANCE GIRLS", "status": "ACTIVE", "level": "SECONDARY"},
        "UPI-5566": {"name": "BRIAN KIPROTICH", "school": "STAREHE BOYS", "status": "ENROLLED", "level": "SECONDARY"}
    }
    def query(self, params):
        upi = params.get('upi') or params.get('identifier')
        if upi in self.LEARNERS:
            return {"status": "SUCCESS", "source": "NEMIS", "data": self.LEARNERS[upi]}
        return {"status": "NOT_FOUND", "message": f"Learner {upi} not found in NEMIS"}

class ProfessionalBodies(MockRegistry):
    """EBK, KMPDC, LSK."""
    MEMBERS = {
        "EBK-500": {"name": "ENG. JOHN DOE", "board": "ENGINEERS BOARD", "status": "PRACTICING"},
        "LSK-123": {"name": "ADV. JANE DOE", "board": "LAW SOCIETY", "status": "ACTIVE"},
        "KMPDC-999": {"name": "DR. JANE DOE", "board": "MEDICAL COUNCIL", "status": "ACTIVE"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class SocialProtection(MockRegistry):
    """Single Registry (Inua Jamii)."""
    BENEFICIARIES = {
        "12345678": {"name": "JOHN DOE", "program": "OPCT", "stipend": "2,000", "status": "ACTIVE"},
        "99887766": {"name": "MAMA MBOGA", "program": "HCT-PWSD", "stipend": "2,000", "status": "ACTIVE"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class SHA(MockRegistry):
    """Social Health Authority / NHIF."""
    MEMBERS = {
        "SHA-12345678": {"name": "JOHN DOE", "id": "12345678", "category": "NATIONAL", "status": "ACTIVE", "cover": "UHC_STANDARD"},
        "SHA-22222222": {"name": "JANE DOE", "id": "22222222", "category": "ENHANCED", "status": "ACTIVE", "cover": "UHC_PREMIUM"},
        "SHA-999": {"name": "ALICE SMITH", "category": "NATIONAL", "status": "ACTIVE"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class NSSF(MockRegistry):
    """National Social Security Fund."""
    MEMBERS = {
        "NSSF-123": {"name": "JOHN DOE", "balance": "150,000", "status": "CONTRIBUTING"},
        "NSSF-999": {"name": "JANE DOE", "balance": "250,000", "status": "ACTIVE"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class Judiciary(MockRegistry):
    """Judiciary Case Tracking System (CTS)."""
    CASES = {
        "MCC/123/2024": {"title": "REPUBLIC vs CITIZEN", "court": "MILIMANI LAW COURTS", "status": "PENDING", "judge": "HON. JUSTICE MUYA"},
        "DL/456/2023": {"title": "DOE vs BANK", "court": "HIGH COURT NAIROBI", "status": "DISMISSED"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class Gazette(MockRegistry):
    """Kenya Gazette."""
    NOTICES = {
        "GZ-2024-001": {"title": "APPOINTMENT OF ICTA BOARD", "date": "2024-01-05", "status": "PUBLISHED"},
        "GZ-2024-050": {"title": "CHANGE OF NAME - JANE DOE", "date": "2024-02-10", "status": "PUBLISHED"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class IEBC(MockRegistry):
    """Voter Register."""
    VOTERS = {
        "12345678": {"name": "JOHN DOE", "constituency": "STAREHE", "center": "CITY HALL", "status": "REGISTERED"},
        "22222222": {"name": "JANE DOE", "constituency": "MVITA", "center": "MAKADARA", "status": "REGISTERED"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class HELB(MockRegistry):
    """Higher Education Loans Board."""
    LOANS = {
        "12345678": {"name": "JOHN DOE", "amount": "140,000", "status": "REPAYING", "compliance": "COMPLIANT"},
        "22222222": {"name": "JANE DOE", "amount": "200,000", "status": "PAID_OFF", "compliance": "COMPLIANT"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class KNEC(MockRegistry):
    """Kenya National Examinations Council."""
    RESULTS = {
        "12345678/001": {"name": "JOHN DOE", "exam": "KCSE", "year": "2008", "grade": "B+"},
        "22222222/050": {"name": "JANE DOE", "exam": "KCSE", "year": "2013", "grade": "A-"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class TSC(MockRegistry):
    """Teachers Service Commission."""
    TEACHERS = {
        "TSC-33333333": {"name": "PETER OMONDI", "station": "NAIROBI SCHOOL", "status": "ACTIVE", "role": "SENIOR TEACHER"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class MaishaAuth(MockRegistry):
    """Digital ID Authentication Service."""
    USERS = {
        "12345678": {"status": "VERIFIED", "credential": "DTC-9988", "last_login": "2024-02-18"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class LiveScanKit(MockRegistry):
    """Biometric Collection Service."""
    DEVICES = {
        "DEV-001": {"location": "HUDUMA_GPO", "status": "ONLINE", "last_sync": "2024-02-19"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class ECitizen(MockRegistry):
    """eCitizen Account Registry."""
    ACCOUNTS = {
        "12345678": {"name": "JOHN DOE", "email": "john.doe@example.com", "phone": "0711122233", "verified": True},
        "22222222": {"name": "JANE DOE", "email": "jane.doe@example.com", "phone": "0722233344", "verified": True}
    }
    def query(self, params): return {"status": "SUCCESS"}

class HospitalRegistry(MockRegistry):
    """General Hospital Registry (Master Facility List)."""
    FACILITIES = {
        "HOSP-001": {"name": "Kenyatta National Hospital", "level": "Level 6", "location": "Nairobi"},
        "HOSP-002": {"name": "Coast General Hospital", "level": "Level 5", "location": "Mombasa"},
        "HOSP-003": {"name": "Mbagathi Hospital", "level": "Level 4", "location": "Nairobi"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class HIS(MockRegistry):
    """Hospital Information System (Patient Records)."""
    PATIENTS = {
        "12345678": {"name": "JOHN DOE", "blood_group": "A+", "allergies": ["PENICILLIN"]},
        "22222222": {"name": "JANE DOE", "blood_group": "O-", "allergies": []}
    }
    def query(self, params): return {"status": "SUCCESS"}

REGISTRY_MAP = {
    # 1. Identity & Civil Registration
    "IPRS": IPRS(),
    "NRB": NRB(),
    "CRS": CRS(),
    "IMMIGRATION": Immigration(),
    "MAISHA_AUTH": MaishaAuth(),
    "LIVESCAN_KIT": LiveScanKit(),
    "ECITIZEN_APP": ECitizen(),
    # 2. Business & Entities
    "BRS": BRS(),
    "KRA": KRA(),
    "NGO_BOARD": NGOBoard(),
    # 3. Land & Assets
    "ARDHISASA": Ardhisasa(),
    "COLLATERAL": CollateralRegistry(),
    # 4. Transport
    "NTSA": NTSA(),
    "KCAA": KCAA(),
    # 5. Education & Professionals
    "NEMIS": NEMIS(),
    "HELB": HELB(),
    "KNEC": KNEC(),
    "TSC": TSC(),
    "PROFESSIONAL_BODIES": ProfessionalBodies(),
    # 6. Social Services
    "SOCIAL_PROTECTION": SocialProtection(),
    "SHA": SHA(),
    "NSSF": NSSF(),
    "HOSPITAL": HospitalRegistry(),
    "HOSPITAL_HIS": HIS(),
    # 7. Other Key Registries
    "JUDICIARY": Judiciary(),
    "GAZETTE": Gazette(),
    "IEBC": IEBC()
}

def get_registry(name):
    return REGISTRY_MAP.get(name)
