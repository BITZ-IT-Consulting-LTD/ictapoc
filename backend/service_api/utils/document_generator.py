import json
import uuid
import datetime
from django.utils import timezone

class DocumentGenerator:
    """
    Utility to generate authoritative digital documents for government services.
    This simulates PDF generation with digital signatures and barcodes.
    """
    
    @staticmethod
    def generate_output(service_request):
        """
        Creates a digital certificate/permit payload for the approved request.
        """
        service_config = service_request.service_config
        citizen = service_request.citizen
        mda = service_config.mda
        
        import random
        svc_code = service_config.service_code
        
        # 1. Generate a Unique Authoritative ID (The "Barcode" content) based on Service Type
        if svc_code in ['BIRTH_REG', 'CRS-CERT-001', 'MOH-NOTIF-001']:
            prefix = "BEN" if svc_code != 'MOH-NOTIF-001' else "NOTIF"
            auth_id = f"{prefix}-{random.randint(100000, 999999)}"
        elif svc_code in ['NATIONAL_ID', 'NRB-ID-001']:
            auth_id = str(random.randint(10000000, 99999999))
        elif svc_code in ['KRA_PIN_REG', 'KRA-TAX-001']:
            auth_id = f"A{random.randint(100000000, 999999999)}W"
        elif svc_code in ['BIZ_INCORPORATION', 'BRS-INC-001']:
            auth_id = f"PVT-{random.randint(1000,9999)}"
        elif svc_code in ['NEMIS_REG', 'MOE-NEMIS-001']:
            auth_id = f"UPI-{random.randint(10000000, 99999999)}"
        else:
            auth_id = f"GOK-{mda.code}-{datetime.datetime.now().year}-{str(uuid.uuid4())[:8].upper()}"
        
        # 2. Extract specific data points based on service type
        payload = service_request.payload
        subject_name = (
            payload.get('child_full_name') or 
            payload.get('child_name') or 
            payload.get('business_name') or 
            payload.get('mda_requesting') or
            citizen.get_full_name() or 
            citizen.username
        )
        
        # 3. Construct the "Digital Document" Structure
        document = {
            "id": str(uuid.uuid4()),
            "type": "AUTHORITATIVE_OUTPUT",
            "name": f"{service_config.service_name} - {subject_name}",
            "issued_by": f"{mda.name} ({mda.code})",
            "issued_to": citizen.username,
            "issue_date": timezone.now().isoformat(),
            "authoritative_id": auth_id,
            "status": "VALID",
            "verification_url": f"https://trust.example.go.ke/verify/{auth_id}",
            "metadata": {
                "service_request_id": service_request.request_id,
                "workflow_finalized_at": timezone.now().isoformat(),
                "barcode_data": auth_id,
                "digital_signature": f"SIG_{str(uuid.uuid4())[:16].upper()}_NPKI_GOK"
            },
            # Mock PDF content (representing the visual appearance)
            "content": f"data:application/pdf;base64,JVBERi0xLjQKJ...(MOCK_BASE64_CERTIFICATE_FOR_{auth_id})..."
        }
        
        return document

    @staticmethod
    def archive_to_edrms(document):
        """
        Sends the document to the internal Document repository for authoritative record keeping.
        """
        print(f"EDRMS [ARCHIVE]: Archiving document {document.get('authoritative_id')} to DRMS...")
        try:
            from apps.document_repository.utils import create_document_from_base64
            from service_api.models import User
            
            # Identify the citizen owner
            user = User.objects.filter(username=document.get('issued_to')).first()
            if not user:
                 return False

            # Persist to DRMS using our existing high-performance utility
            drms_doc = create_document_from_base64(
                user=user,
                title=document.get('name', 'Authoritative Document'),
                base64_content=document.get('content'),
                document_type='authoritative_output',
                classification='internal',
                metadata=document.get('metadata', {})
            )
            return bool(drms_doc)
        except Exception as e:
            print(f"EDRMS [ERROR]: Failed to archive to repository: {str(e)}")
            return False
