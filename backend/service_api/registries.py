import random

class MockRegistry:
    """Base class for authoritative registries."""
    def query(self, params):
        raise NotImplementedError 

class IPRS(MockRegistry):
    """Integrated Population Registration System (Identity)."""
    CITIZENS = {
        "12345678": {"full_name": "JOHN DOE", "status": "ALIVE", "dob": "1990-01-01", "gender": "MALE"},
        "22222222": {"full_name": "JANE DOE", "status": "ALIVE", "dob": "1995-05-05", "gender": "FEMALE"},
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
        "12345678": {"serial_no": "99887766", "issue_date": "2010-01-01", "station": "NAIROBI CENTRAL", "status": "ISSUED"},
        "22222222": {"serial_no": "11223344", "issue_date": "2015-05-05", "station": "MOMBASA EAST", "status": "ISSUED"}
    }
    def query(self, params):
        cid = params.get('id_number') or params.get('identifier')
        if cid in self.CARDS:
            return {"status": "SUCCESS", "source": "NRB", "data": self.CARDS[cid]}
        return {"status": "NOT_FOUND", "message": f"ID {cid} not found in NRB"}

class CRS(MockRegistry):
    """Civil Registration Services (Births/Deaths)."""
    RECORDS = {
        "BC-111": {"full_name": "JAMES DOE JNR", "event": "BIRTH", "date": "2006-05-15", "mother": "MARY MOTHER"},
        "DC-999": {"full_name": "SARAH LATE", "event": "DEATH", "date": "2024-01-01", "cert_no": "D-1234"}
    }
    def query(self, params):
        bid = params.get('birth_certificate_number') or params.get('identifier')
        if bid in self.RECORDS:
            return {"status": "SUCCESS", "source": "CRS", "data": self.RECORDS[bid]}
        return {"status": "NOT_FOUND", "message": f"Record {bid} not found in CRS"}

class Immigration(MockRegistry):
    """Department of Immigration Services."""
    DOCUMENTS = {
        "AK001": {"name": "JOHN DOE", "type": "PASSPORT", "expiry": "2030-01-01", "status": "ACTIVE"},
        "V-888": {"name": "ALICE SMITH", "type": "VISA", "expiry": "2024-12-31", "status": "VALID"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class BRS(MockRegistry):
    """Business Registration Service."""
    ENTITIES = {
        "PVT-123": {"name": "TECH SOLUTIONS LTD", "type": "COMPANY", "inc_date": "2020-01-01", "status": "ACTIVE"},
        "BN-987": {"name": "MAMA MBOGA SHOP", "type": "BUSINESS NAME", "owner": "JANE DOE", "status": "ACTIVE"}
    }
    def query(self, params):
        eid = params.get('entity_id') or params.get('identifier')
        if eid in self.ENTITIES:
            return {"status": "SUCCESS", "source": "BRS", "data": self.ENTITIES[eid]}
        return {"status": "NOT_FOUND", "message": f"Entity {eid} not found in BRS"}

class KRA(MockRegistry):
    """Kenya Revenue Authority."""
    PINS = {
        "A001234567Z": {"name": "JOHN DOE", "pin_type": "INDIVIDUAL", "status": "COMPLIANT"},
        "P098765432W": {"name": "JANE DOE", "pin_type": "INDIVIDUAL", "status": "NON_COMPLIANT"}
    }
    def query(self, params):
        pin = params.get('pin') or params.get('identifier')
        if pin in self.PINS:
            return {"status": "SUCCESS", "source": "KRA", "data": self.PINS[pin]}
        return {"status": "NOT_FOUND", "message": f"PIN {pin} not found in KRA"}

class NGOBoard(MockRegistry):
    """NGO Coordination Board."""
    ENTITIES = {
        "NGO-001": {"name": "SAVE THE PLANET", "sector": "ENVIRONMENT", "status": "REGISTERED"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class Ardhisasa(MockRegistry):
    """National Land Information Management System."""
    TITLES = {
        "NRB/01/123": {"owner": "JOHN DOE", "location": "UPPERHILL", "status": "CLEAN"},
        "MSA/02/456": {"owner": "JANE DOE", "location": "NYALI", "status": "CHARGED"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class CollateralRegistry(MockRegistry):
    """Movable assets registry."""
    ASSETS = {
        "CR-001": {"owner": "JOHN DOE", "asset": "TOYOTA HILUX", "lien": "ABC BANK", "status": "ACTIVE"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class NTSA(MockRegistry):
    """National Transport and Safety Authority."""
    RECORDS = {
        "KAA 001A": {"owner": "JOHN DOE", "type": "VEHICLE_LOGBOOK", "status": "VALID"},
        "DL-9988": {"name": "JANE DOE", "type": "DRIVING_LICENSE", "expiry": "2027-01-01", "status": "VALID"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class KCAA(MockRegistry):
    """Kenya Civil Aviation Authority."""
    AIRCRAFT = {
        "5Y-XYZ": {"owner": "FLY KENYA", "model": "REIMS-CESSNA 172", "status": "AIRWORTHY"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class NEMIS(MockRegistry):
    """National Education Management Information System."""
    LEARNERS = {
        "UPI-1122": {"name": "JAMES DOE JNR", "school": "NAIROBI SCHOOL", "status": "ENROLLED"},
        "UPI-3344": {"name": "LUCY SMITH", "school": "ALLIANCE GIRLS", "status": "ACTIVE"}
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
        "LSK-123": {"name": "ADV. JANE DOE", "board": "LAW SOCIETY", "status": "ACTIVE"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class SocialProtection(MockRegistry):
    """Single Registry (Inua Jamii)."""
    BENEFICIARIES = {
        "12345678": {"name": "JOHN DOE", "program": "OPCT", "stipend": "2,000", "status": "ACTIVE"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class SHA(MockRegistry):
    """Social Health Authority / NHIF."""
    MEMBERS = {
        "SHA-999": {"name": "JOHN DOE", "category": "NATIONAL", "status": "ACTIVE"},
        "NHIF-001": {"name": "JANE DOE", "category": "ENHANCED", "status": "ACTIVE"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class NSSF(MockRegistry):
    """National Social Security Fund."""
    MEMBERS = {
        "NSSF-123": {"name": "JOHN DOE", "balance": "150,000", "status": "CONTRIBUTING"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class Judiciary(MockRegistry):
    """Judiciary Case Tracking System (CTS)."""
    CASES = {
        "MCC/123/2024": {"title": "REPUBLIC vs CITIZEN", "court": "MILIMANI LAW COURTS", "status": "PENDING"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class Gazette(MockRegistry):
    """Kenya Gazette."""
    NOTICES = {
        "GZ-2024-001": {"title": "APPOINTMENT OF ICTA BOARD", "date": "2024-01-05", "status": "PUBLISHED"}
    }
    def query(self, params): return {"status": "SUCCESS"}

class IEBC(MockRegistry):
    """Voter Register."""
    VOTERS = {
        "12345678": {"name": "JOHN DOE", "constituency": "STAREHE", "center": "CITY HALL", "status": "REGISTERED"}
    }
    def query(self, params): return {"status": "SUCCESS"}

REGISTRY_MAP = {
    # 1. Identity & Civil Registration
    "IPRS": IPRS(),
    "NRB": NRB(),
    "CRS": CRS(),
    "IMMIGRATION": Immigration(),
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
    "PROFESSIONAL_BODIES": ProfessionalBodies(),
    # 6. Social Services
    "SOCIAL_PROTECTION": SocialProtection(),
    "SHA": SHA(),
    "NSSF": NSSF(),
    # 7. Other Key Registries
    "JUDICIARY": Judiciary(),
    "GAZETTE": Gazette(),
    "IEBC": IEBC()
}

def get_registry(name):
    return REGISTRY_MAP.get(name)
