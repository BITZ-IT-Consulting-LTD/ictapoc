import requests
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .models import (
    RegistryAdapter, PaymentProvider, PaymentTransaction, 
    RevenueSplit, ServiceRequest, ServiceConfig, MDA, User,
    ConsentRecord, ConsentAccessLog, DataPurpose
)

class RegistryService:
    @staticmethod
    def get_adapter(code):
        try:
            return RegistryAdapter.objects.get(code=code)
        except ObjectDoesNotExist:
            return None

    @classmethod
    def query(cls, registry_code, identifier, identifier_field='id', requester_user=None):
        """
        GEA-Compliant Query with Consent checking.
        """
        # In a full GEA implementation, we'd check Consent here
        # if requester_user and not ConsentService.check_consent(requester_user, ...):
        #     return {"status": "ERROR", "message": "Consent required"}
        
        adapter = cls.get_adapter(registry_code)
        if not adapter:
            return {"status": "ERROR", "message": f"Registry adapter {registry_code} not found."}

        if adapter.is_mock:
            return cls._query_mock(adapter, identifier, identifier_field)
        else:
            return cls._query_api(adapter, identifier, identifier_field)

    @staticmethod
    def _query_mock(adapter, identifier, identifier_field):
        """Logic for querying the database-stored JSON mock data."""
        data = adapter.mock_data
        
        # If the mock data is a flat dictionary (ID as key), look it up directly
        if identifier in data:
            record = data[identifier]
            return {"status": "SUCCESS", "source": "DB_MOCK", "data": record}
        
        # Otherwise, search through values if identifier_field is specified
        for key, val in data.items():
            if isinstance(val, dict) and val.get(identifier_field) == identifier:
                return {"status": "SUCCESS", "source": "DB_MOCK", "data": val}
        
        # Or if the record itself is the value in a list
        if isinstance(data, list):
            for item in data:
                if item.get(identifier_field) == identifier:
                    return {"status": "SUCCESS", "source": "DB_MOCK", "data": item}

        return {"status": "NOT_FOUND", "message": f"Record {identifier} not found in {adapter.code} mock data."}

    @staticmethod
    def _query_api(adapter, identifier, identifier_field):
        """Logic for real API calls via requests with auth config plus resilience."""
        import time
        from requests.exceptions import RequestException

        url = f"{adapter.base_url}?{identifier_field}={identifier}"
        headers = adapter.auth_config.get('headers', {})
        
        max_retries = 3
        backoff_factor = 2

        for attempt in range(max_retries):
            try:
                # In a real environment, this would handle National PKI Certs via (cert, key)
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                raw_data = response.json()
                
                # Apply data mapping if defined
                mapped_data = {}
                if adapter.data_mapping:
                    for target_field, source_field in adapter.data_mapping.items():
                        mapped_data[target_field] = raw_data.get(source_field)
                else:
                    mapped_data = raw_data

                return {"status": "SUCCESS", "source": "API", "data": mapped_data}
            except RequestException as e:
                # Check if it's a retryable error (e.g. timeout, 5xx)
                status_code = getattr(e.response, 'status_code', None)
                if status_code and status_code < 500:
                    # Non-retryable (4xx)
                    return {"status": "ERROR", "message": f"Registry Client Error: {str(e)}", "retryable": False}
                
                if attempt < max_retries - 1:
                    time.sleep(backoff_factor ** attempt)
                    continue
                else:
                    return {"status": "ERROR", "message": f"Registry Connection Failed after {max_retries} attempts: {str(e)}", "retryable": True}
            except Exception as e:
                return {"status": "ERROR", "message": f"Unexpected integration error: {str(e)}", "retryable": False}

    @classmethod
    def get_identity(cls, id_number):
        """Helper for IPRS lookup."""
        return cls.query('IPRS', id_number)

    @classmethod
    def get_kra_status(cls, pin):
        """Helper for KRA lookup."""
        return cls.query('KRA', pin)

class PaymentService:
    """
    Business logic for the Government Payment Aggregator (GPA).
    Handles service payments, callbacks, and automated revenue splitting.
    """

    @classmethod
    def initiate_stk_push(cls, request_id, phone_number, amount, provider_code='MPESA'):
        """
        Initiates a payment request via a digital provider.
        """
        try:
            service_request = ServiceRequest.objects.get(request_id=request_id)
            provider = PaymentProvider.objects.get(code=provider_code, is_active=True)
            
            # 1. Create PENDING Transaction record
            transaction = PaymentTransaction.objects.create(
                service_request=service_request,
                amount=amount,
                provider=provider,
                status='PENDING'
            )

            # 2. Call Provider API (Mocked for PoC)
            # In production, this would use Paybill/Keys from provider.config
            provider_ref = f"GPA-{transaction.id}-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            transaction.provider_ref = provider_ref
            transaction.save()

            print(f"PAYMENT_STK: Initiated {amount} for {request_id} via {provider_code}. Ref: {provider_ref}")
            
            return {
                "status": "SUCCESS",
                "transaction_id": transaction.id,
                "provider_ref": provider_ref,
                "message": "STK Push initiated successfully"
            }
        except ObjectDoesNotExist as e:
            return {"status": "ERROR", "message": f"Setup error: {str(e)}"}
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    @classmethod
    def process_callback(cls, provider_ref, status_code, amount=None):
        """
        Handles post-payment notifications from providers.
        """
        try:
            transaction = PaymentTransaction.objects.get(provider_ref=provider_ref)
            
            if status_code == 'SUCCESS':
                transaction.status = 'SUCCESS'
                transaction.save()
                
                # Update the service request status if necessary
                sr = transaction.service_request
                if sr.status == 'received':
                    sr.status = 'in_progress'
                    sr.save()
                
                # 3. Calculate Revenue Splits
                cls.calculate_revenue_splits(transaction)
                
                return {"status": "SUCCESS", "message": "Transaction completed and split."}
            else:
                transaction.status = 'FAILED'
                transaction.save()
                return {"status": "FAILED", "message": f"Transaction failed with code {status_code}"}
                
        except ObjectDoesNotExist:
            return {"status": "ERROR", "message": "Transaction ref not found."}

    @classmethod
    def calculate_revenue_splits(cls, transaction):
        """
        GEA 'Split-at-Source' logic. Automatically distributes funds to beneficiaries.
        """
        service_config = transaction.service_request.service_config
        amount = transaction.amount
        
        # Determine split percentages from ServiceConfig.config
        # Default: 20% Treasury, 80% Owning Agency
        split_config = service_config.config.get('revenue_split', {
            "TREASURY": 20,
            "AGENCY": 80
        })
        
        splits_created = []

        for ben_code, percentage in split_config.items():
            try:
                # Find beneficiary MDA
                if ben_code == 'TREASURY':
                    mda = MDA.objects.get(code='TREASURY')
                else:
                    mda = service_config.mda
                
                split_amount = (amount * Decimal(str(percentage))) / Decimal('100')
                
                split = RevenueSplit.objects.create(
                    transaction=transaction,
                    beneficiary_mda=mda,
                    amount=split_amount,
                    percentage=percentage,
                    account_number=mda.config.get('bank_account', 'GEN-REV-001') if hasattr(mda, 'config') else 'GEN-REV-001'
                )
                splits_created.append(split)
            except Exception as e:
                print(f"REVENUE_SPLIT_ERROR: Failed for {ben_code}: {str(e)}")

        return splits_created

class ConsentService:
    """
    Business logic for the Consent Manager.
    Ensures Data Protection Act (2019) compliance by capturing and verifying citizen consent.
    """

    @classmethod
    def check_consent(cls, user, requester_mda, scope):
        """Verifies if an active, valid consent record exists."""
        now = timezone.now()
        consent = ConsentRecord.objects.filter(
            user=user,
            requester=requester_mda,
            data_scope=scope,
            status='ACTIVE'
        ).filter(
            Q(expires_at__isnull=True) | Q(expires_at__gt=now)
        ).first()

        return consent

    @classmethod
    def grant_consent(cls, user, requester_mda, scope, purpose_code, expires_in_days=30):
        """Explicitly grants data processing permission."""
        try:
            purpose = DataPurpose.objects.get(code=purpose_code)
            expires_at = timezone.now() + timedelta(days=expires_in_days)
            
            consent = ConsentRecord.objects.create(
                user=user,
                requester=requester_mda,
                data_scope=scope,
                purpose=purpose,
                expires_at=expires_at,
                status='ACTIVE'
            )
            return consent
        except DataPurpose.DoesNotExist:
            return None

    @classmethod
    def revoke_consent(cls, consent_id, user):
        """Citizen initiates revocation of their data permission."""
        try:
            consent = ConsentRecord.objects.get(id=consent_id, user=user)
            consent.status = 'REVOKED'
            consent.revoked_at = timezone.now()
            consent.save()
            return True
        except ConsentRecord.DoesNotExist:
            return False

    @classmethod
    def log_access(cls, consent, accessor_user, resource_id=None):
        """Creates an immutable log of data access initiated under a consent record."""
        log = ConsentAccessLog.objects.create(
            consent=consent,
            accessed_by=accessor_user,
            resource_id=resource_id
        )
        return log

class LifecycleService:
    """
    Orchestrates the 'Cradle-to-Grave' (Lifecycle) scenario.
    Demonstrates the power of interoperability and the 'Once-Only Principle'.
    """

    @classmethod
    def get_citizen_journey_summary(cls, user):
        """
        Aggregates data from multiple registries to show the citizen's 
        authoritative life journey status.
        """
        summary = {
            "identity": {"status": "NOT_FOUND", "label": "National ID (IPRS)"},
            "civil": {"status": "NOT_FOUND", "label": "Birth Record (CRS)"},
            "education": {"status": "NOT_FOUND", "label": "Education (NEMIS)"},
            "tax": {"status": "NOT_FOUND", "label": "Taxation (KRA)"},
            "business": {"status": "NOT_FOUND", "label": "Business (BRS)"}
        }

        # 1. Identity (IPRS)
        if user.id_number:
            iprs_res = RegistryService.query('IPRS', user.id_number)
            if iprs_res['status'] == 'SUCCESS':
                summary['identity']['status'] = 'VERIFIED'
                summary['identity']['data'] = iprs_res['data']

        # 2. Civil (CRS) - Using ID to find Birth Cert if linked, or manual provided cert
        # For POC, we'll try to find a record where Mother or Father matches if not explicit
        # But usually, it's a direct BC number.
        bc_no = user.config.get('birth_certificate_no') if hasattr(user, 'config') else None
        if bc_no:
            crs_res = RegistryService.query('CRS', bc_no, 'birth_certificate_number')
            if crs_res['status'] == 'SUCCESS':
                summary['civil']['status'] = 'VERIFIED'
                summary['civil']['data'] = crs_res['data']

        # 3. Education (NEMIS)
        # UPI might be in user config or found by Name + DOB
        upi = user.config.get('upi') if hasattr(user, 'config') else None
        if upi:
            nemis_res = RegistryService.query('NEMIS', upi, 'upi')
            if nemis_res['status'] == 'SUCCESS':
                summary['education']['status'] = 'VERIFIED'
                summary['education']['data'] = nemis_res['data']

        # 4. Tax (KRA)
        kra_pin = user.config.get('kra_pin') if hasattr(user, 'config') else None
        if kra_pin:
            kra_res = RegistryService.query('KRA', kra_pin, 'pin')
            if kra_res['status'] == 'SUCCESS':
                summary['tax']['status'] = 'VERIFIED'
                summary['tax']['data'] = kra_res['data']

        return summary

    @classmethod
    def prefill_service_application(cls, service_code, user, inputs=None):
        """
        The 'Optimized To-Be' core logic.
        Automatically pulls data from 'Registry B' when applying for 'Service A'.
        """
        prefilled_data = {}
        inputs = inputs or {}

        # 👶 BIRTH -> 🆔 ID Application
        if service_code == 'IPRS-ID-001':
            bc_no = inputs.get('birth_certificate_number')
            if bc_no:
                # 🛡️ In a real system, we'd check Consent here
                crs_res = RegistryService.query('CRS', bc_no, 'birth_certificate_number')
                if crs_res['status'] == 'SUCCESS':
                    data = crs_res['data']
                    prefilled_data['full_name'] = data.get('full_name')
                    prefilled_data['date_of_birth'] = data.get('date')
                    prefilled_data['verified_source'] = 'CRS Authority'

        # 🆔 ID -> 💰 KRA PIN Application
        elif service_code == 'KRA-PIN-001':
            id_no = inputs.get('national_id_number')
            if id_no:
                iprs_res = RegistryService.query('IPRS', id_no, 'id_number')
                if iprs_res['status'] == 'SUCCESS':
                    data = iprs_res['data']
                    prefilled_data['full_name'] = data.get('full_name')
                    prefilled_data['status'] = data.get('status')
                    prefilled_data['verified_source'] = 'IPRS Authority'

        # 💰 PIN -> 🏢 BRS Business Registration
        elif service_code == 'BRS-BIZ-001':
            id_no = inputs.get('director_id')
            pin = inputs.get('director_pin')
            if id_no and pin:
                iprs_res = RegistryService.query('IPRS', id_no)
                kra_res = RegistryService.query('KRA', pin)
                if iprs_res['status'] == 'SUCCESS' and kra_res['status'] == 'SUCCESS':
                    prefilled_data['director_verified'] = True
                    prefilled_data['tax_status'] = kra_res['data'].get('status')
                    prefilled_data['source'] = 'IPRS + KRA Federation'

        return prefilled_data
