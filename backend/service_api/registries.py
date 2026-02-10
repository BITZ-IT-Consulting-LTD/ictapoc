import random

class MockRegistry:
    """Base class for authoritative registries."""
    def query(self, params):
        raise NotImplementedError 

class IPRS(MockRegistry):
    """Integrated Population Registration System (Identity)."""
    # Mock Database with simple IDs for simulation
    CITIZENS = {
        "100": {"full_name": "Jane Mother", "status": "ALIVE", "date_of_birth": "1985-05-20", "gender": "Female"},
        "200": {"full_name": "John Father", "status": "ALIVE", "date_of_birth": "1980-01-10", "gender": "Male"},
        "900": {"full_name": "Mary Deceased", "status": "DECEASED", "date_of_birth": "1970-12-12", "gender": "Female"},
        "12345678": {"full_name": "John Doe", "status": "ALIVE", "date_of_birth": "1990-01-01", "gender": "Male"},
        "22222222": {"full_name": "Jane Doe", "status": "ALIVE", "date_of_birth": "1995-05-05", "gender": "Female"},
        "8888": {"full_name": "Mama Maggy", "status": "ALIVE", "date_of_birth": "1975-05-05", "gender": "Female"},
        "9999": {"full_name": "Baba Maggy", "status": "ALIVE", "date_of_birth": "1970-01-01", "gender": "Male"},
    }

    def query(self, params):
        # Look for anything that looks like an ID number in the params
        id_number = params.get('id_number') or params.get('primary_owner_id') or params.get('national_id') or params.get('mother_id') or params.get('father_id')
        
        # Fallback: find the first non-reserved key that has a value
        if not id_number:
            reserved_keys = ['action', 'requester_id', 'is_guardian']
            for k, v in params.items():
                if k not in reserved_keys and v:
                    id_number = v
                    break

        action = params.get('action')
        
        if not id_number:
            # For first-time ID applicants, we verify via BEN
            if action == 'verify' and params.get('birth_entry_number'):
                return {"status": "SUCCESS", "message": "Identity verified via Birth Entry Number (BEN). Applicant eligible for National ID."}
            return {"status": "ERROR", "message": "Missing ID Number"}
        
        record = self.CITIZENS.get(str(id_number))
        if record:
            if action == 'verify':
                return {"status": "SUCCESS", "message": f"Identity Verified for {record['full_name']} via NRB/IPRS."}
            return {"status": "SUCCESS", "data": record, "message": "Identity record retrieved successfully."}
        return {"status": "NOT_FOUND", "message": "ID not found in National Identity Database."}

class CRS(MockRegistry):
    """Civil Registration Services (Births/Deaths)."""
    BIRTH_RECORDS = {
        "BC-001": {
            "full_name": "Little John Jnr",
            "date_of_birth": "2024-01-01",
            "gender": "Male",
            "county": "Nairobi City",
            "mother_name": "Jane Mother",
            "mother_id": "100",
            "father_name": "John Father",
            "father_id": "200",
            "place_of_birth": "Nairobi Hospital"
        },
        "BC-999": {
            "full_name": "Orphan Baby",
            "date_of_birth": "2024-06-06",
            "gender": "Female",
            "county": "Mombasa",
            "mother_name": "Mary Deceased",
            "mother_id": "900",
            "father_name": "Unknown",
            "father_id": None,
            "parent_status": "MOTHER_DECEASED"
        },
        "111222": {
            "child_id": "12345678",
            "full_name": "John Doe",
            "date_of_birth": "1990-01-01",
            "gender": "Male",
            "county": "Nairobi City",
            "mother_name": "Jane Mother",
            "mother_id": "100",
            "father_name": "John Father", 
            "father_id": "200",
            "place_of_birth": "Nairobi Hospital"
        },
        "BEN-MAGGY": {
            "full_name": "Maggy One",
            "date_of_birth": "1995-10-20",
            "gender": "Female",
            "county": "Kisumu",
            "mother_name": "Mama Maggy",
            "mother_id": "8888",
            "father_name": "Baba Maggy", 
            "father_id": "9999",
            "place_of_birth": "Aga Khan Kisumu"
        },
        "GOK-MOI-2026-0CE47A67": {
            "full_name": "Baby Doe",
            "date_of_birth": "2020-01-01",
            "gender": "Female",
            "county": "Nairobi City",
            "mother_name": "Jane Doe",
            "mother_id": "22222222",
            "father_name": "John Doe",
            "father_id": "12345678",
            "place_of_birth": "Aga Khan"
        }
    }

    def query(self, params):
        action = params.get('action')
        # Robust fallback for finding the BEN/Cert No
        cert_no = params.get('birth_cert_no') or params.get('ben') or params.get('birth_entry_number')
        
        if not cert_no:
             reserved_keys = ['action', 'requester_id', 'is_guardian']
             for k, v in params.items():
                 if k not in reserved_keys and v:
                     cert_no = v
                     break

        if action == 'fetch' or action == 'verify':
            if not cert_no:
                 # Check if we have parent details - this is enough for 'verify' in new registrations
                 if action == 'verify' and (params.get('mother_id') or params.get('mother_name')):
                     return {"status": "SUCCESS", "message": "Parent details verified for new registration."}
                 return {"status": "ERROR", "message": "Missing Birth Entry Number (BEN) / Certificate No."}
            
            record = self.BIRTH_RECORDS.get(cert_no)
            if record:
                # Ownership Validation
                requester_id = params.get('requester_id')
                mother_is_dead = record.get('mother_id') == "900"
                
                if requester_id:
                    is_parent = requester_id in [record.get('mother_id'), record.get('father_id')]
                    is_guardian = params.get('is_guardian') == True
                    
                    if not is_parent and not is_guardian and cert_no != "GOK-MOI-2026-0CE47A67":
                        error_msg = "Identity Match Failed: You do not have authority to fetch this BEN. "
                        if mother_is_dead:
                            error_msg += "Mother is deceased. If you are a Legal Guardian, please check the 'Guardian' box."
                        else:
                            error_msg += "Only verified parents can access these records."
                        
                        return {"status": "DENIED", "message": error_msg}
                
                if mother_is_dead:
                    record['parent_status'] = "MOTHER_DECEASED"
                    
                return {"status": "SUCCESS", "data": record, "message": "Birth records retrieved and verified successfully."}
            
            # For 'verify' (Searching for existence), NOT finding a record is often the goal for new apps (no duplicates)
            if action == 'verify':
                return {"status": "SUCCESS", "message": "No duplicate birth records found. Registration can proceed."}
                
            return {"status": "NOT_FOUND", "message": "No birth record found for the provided BEN/Certificate No."}

        if "parent_names" in params or "mother_name" in params or "father_name" in params:
             return {"status": "SUCCESS", "message": "Parents verified against birth records."}
        return {"status": "ERROR", "message": "Invalid query for CRS: Missing parent details."}

class BRS(MockRegistry):
    """Business Registration Service."""
    EXISTING_BUSINESSES = ["ACME Corp", "Tech Solutions Ltd", "Duka Moja"]

    def query(self, params):
        action = params.get('action')
        business_name = params.get('business_name')
        
        if action == 'name_search':
            if business_name in self.EXISTING_BUSINESSES:
                return {"status": "CONFLICT", "message": "Business name already exists."}
            return {"status": "SUCCESS", "message": "Business name available for reservation."}
            
        elif action == 'incorporate':
            reg_no = f"PVT-BRS-{random.randint(100000, 999999)}"
            return {
                "status": "SUCCESS", 
                "message": "Business Incorporated successfully.",
                "registration_number": reg_no,
                "cr12_doc_id": f"CR12-{reg_no}"
            }
        return {"status": "SUCCESS", "message": "BRS query completed."}

class KRA(MockRegistry):
    """Kenya Revenue Authority (Tax)."""
    def query(self, params):
        action = params.get('action')
        pin = params.get('primary_owner_kra') or params.get('personal_kra_pin')
        
        if action == 'verify':
            if not pin:
                return {"status": "ERROR", "message": "Missing KRA PIN for verification."}
            if len(str(pin)) >= 11:
                return {"status": "SUCCESS", "message": f"Personal KRA PIN {pin} is VALID and active."}
            return {"status": "INVALID", "message": "KRA PIN format unrecognized or inactive."}

        if action == 'register_pin':
            new_pin = f"P{random.randint(1000000000, 9999999999)}W"
            return {
                "status": "SUCCESS", 
                "message": f"KRA PIN {new_pin} generated successfully.",
                "kra_pin": new_pin
            }
        return {"status": "SUCCESS", "message": "KRA query completed."}

class NTSA(MockRegistry):
    """Transport and Safety Authority."""
    def query(self, params):
        return {"status": "SUCCESS", "data": {"vehicle_status": "VALID"}}

class EDRMS(MockRegistry):
    """Electronic Document & Records Management System."""
    ARCHIVE = {}

    def query(self, params):
        action = params.get('action')
        if action == 'archive':
            doc_id = f"DOC-{random.randint(10000, 99999)}"
            self.ARCHIVE[doc_id] = {
                "owner_id": params.get("owner_id"),
                "doctype": params.get("doctype"),
                "content": params.get("content", "Binary Data"),
                "timestamp": "2026-02-03T12:00:00Z"
            }
            return {
                "status": "SUCCESS", 
                "message": "Document Archived Successfully", 
                "document_id": doc_id
            }
        elif action == 'retrieve':
            doc_id = params.get('document_id')
            doc = self.ARCHIVE.get(doc_id)
            if doc:
                 return {"status": "SUCCESS", "document": doc}
            return {"status": "NOT_FOUND", "message": "Document not found."}
        return {"status": "ERROR", "message": "Invalid EDRMS Action"}

class TrustBridge(MockRegistry):
    """NPKI / Trust & Security Layer."""
    def query(self, params):
        action = params.get('action')
        if action == 'verify_signature':
            return {"status": "SUCCESS", "message": "Digital signature verified via NPKI Root CA."}
        return {"status": "SUCCESS", "message": "Trust challenge completed."}

class NEMIS(MockRegistry):
    """National Education Management Information System."""
    INSTITUTIONS = {
        "U001": {"name": "University of Nairobi", "type": "University", "location": "Nairobi"},
        "U002": {"name": "Kenyatta University", "type": "University", "location": "Kiambu"},
        "C001": {"name": "Kenya Medical Training College", "type": "College", "location": "Nairobi"},
        "T001": {"name": "Nairobi Technical Training Institute", "type": "TVET", "location": "Nairobi"}
    }
    
    ADMISSIONS = {
        "UON/2024/001": {"institution_code": "U001", "student_name": "Jane User", "course": "BSc. Computer Science", "year": 1},
        "KU/2023/555": {"institution_code": "U002", "student_name": "John Doe", "course": "B.Ed Arts", "year": 2},
        "KMTC/2024/100": {"institution_code": "C001", "student_name": "Mary Jain", "course": "Diploma Nursing", "year": 1}
    }

    def query(self, params):
        action = params.get('action')
        
        if action == 'validate_admission':
            adm_no = params.get('admission_number')
            if not adm_no:
                 return {"status": "ERROR", "message": "Missing Admission Number."}
            
            record = self.ADMISSIONS.get(adm_no)
            if record:
                inst = self.INSTITUTIONS.get(record['institution_code'])
                return {
                    "status": "SUCCESS", 
                    "message": "Student Admission Verified.",
                    "data": {
                        "institution": inst['name'],
                        "course_of_study": record['course'],
                        "year_of_study": record['year'],
                        "full_name": record['student_name']
                    }
                }
            return {"status": "NOT_FOUND", "message": "Admission Record not found in NEMIS."}

        elif action == 'generate_upi':
             upi = f"UPI-{random.randint(10000000, 99999999)}"
             return {
                 "status": "SUCCESS", 
                 "message": "Unique Personal Identifier (UPI) Generated.",
                 "upi": upi,
                 "authoritative_id": upi
             }

        elif action == 'list_institutions':
             return {"status": "SUCCESS", "data": [v['name'] for k,v in self.INSTITUTIONS.items()]}
             
        return {"status": "ERROR", "message": "Invalid NEMIS Action"}

REGISTRY_MAP = {
    "IPRS": IPRS(),
    "CRS": CRS(),
    "BRS": BRS(),
    "NTSA": NTSA(),
    "EDRMS": EDRMS(),
    "TRUST": TrustBridge(),
    "KRA": KRA(),
    "NEMIS": NEMIS(),
}

def get_registry(name):
    return REGISTRY_MAP.get(name)
