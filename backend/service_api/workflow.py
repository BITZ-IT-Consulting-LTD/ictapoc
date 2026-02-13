import uuid
import json
import urllib.request
from django.db import transaction
from .models import ServiceRequest, ServiceConfig, WorkflowStep, AuditLog, User
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

def send_notification(user, message, request=None):
    """
    Sends email and simulates in-app notifications.
    In a production system, this would trigger a Celery task.
    """
    subject = f"GOK Platform: Request {request.request_id}" if request else "Government Services Platform Notification"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    try:
        # Note: In the POC, email settings might not be configured, so we log as well.
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)
        print(f"NOTIFICATION [To: {user.username}]: {message}")
    except Exception as e:
        print(f"FAILED NOTIFICATION [To: {user.username}]: {e}")

class WorkflowEngine:
    """
    The Brain of the Repeatable Government Services Platform.
    Handles transitions between automated and manual steps based on configuration.
    """
    def __init__(self, request_id=None):
        self.request_id = request_id
        self.service_request = None
        if request_id:
            try:
                self.service_request = ServiceRequest.objects.get(request_id=request_id)
            except ServiceRequest.DoesNotExist:
                pass

    @transaction.atomic
    def create_service_request(self, citizen: User, service_config: ServiceConfig, payload: dict):
        """
        Initializes a new service request and starts the workflow.
        """
        self.service_request = ServiceRequest.objects.create(
            request_id=str(uuid.uuid4())[:8].upper(), # Use a short prefix for POC readability
            citizen=citizen,
            service_config=service_config,
            payload=payload,
            status='received'
        )
        
        AuditLog.objects.create(
            service_request=self.service_request,
            actor=citizen,
            action='REQUEST_SUBMITTED',
            details=f"Service request for '{service_config.service_name}' submitted by citizen."
        )
        
        # Start processing the first step
        self.process_workflow_step()

        # POC AUTO-HEALING: If the first step is just a 'submit' placeholder for the citizen,
        # skip it immediately so the request lands on an Officer's desk.
        if self.service_request.current_step and \
           self.service_request.current_step.role == 'citizen' and \
           self.service_request.current_step.action == 'submit':
            self.process_workflow_step()

        return self.service_request

    @transaction.atomic
    def process_workflow_step(self, force_refresh=False):
        """
        Moves the request to the next step in the sequence.
        Supports automated 'api_call' and 'manual' officer review.
        """
        if not self.service_request:
            return

        service_config = self.service_request.service_config
        
        # Determine current sequence. 
        # If current_step is None but status is 'in_progress', we assume it's an orphan and start from 0.
        current_seq = 0
        if self.service_request.current_step:
            current_seq = self.service_request.current_step.sequence
        elif self.service_request.status == 'received':
            current_seq = 0
        else:
            # It's an orphan (status in_progress/escalated but no step)
            current_seq = 0 
        
        # Find the next step in the sequence - STRICTLY 'to_be' for client-facing demo
        next_step = WorkflowStep.objects.filter(
            service_config=service_config, 
            lifecycle_stage='to_be',
            sequence__gt=current_seq
        ).order_by('sequence').first()

        if next_step:
            self.service_request.current_step = next_step
            self.service_request.status = 'in_progress'
            self.service_request.save()

            AuditLog.objects.create(
                service_request=self.service_request,
                action='STEP_TRANSITION',
                details=f"Workflow advanced to Step {next_step.sequence}: {next_step.step_name}"
            )

            if next_step.step_type == 'api_call':
                self._execute_api_call(next_step)
            else:
                self._notify_manual_review(next_step)
        else:
            # Workflow complete
            self._finalize_request('approved')

    def _execute_api_call(self, step: WorkflowStep):
        """
        Executes an automated check via the Huduma Bridge (KeSEL).
        """
        print(f"WORKFLOW [Orchestration]: Initiating secure exchange for step '{step.step_name}'")
        
        # 1. Determine Target Registry from step config or hardcoded fallback
        target_registry = None
        
        api_config = step.api_config or {}
        api_url = api_config.get('url', '')
        
        if api_url:
            # Parse registry from URL like "KESEL_BRIDGE/EDRMS/archive"
            parts = api_url.split('/')
            if len(parts) > 1 and parts[0] in ['KESEL_BRIDGE', 'HUB_BRIDGE', 'HUDUMA_BRIDGE']:
                target_registry = parts[1]
        
        if not target_registry:
            target_registry = "IPRS" # Default fallback
            if "Passport" in self.service_request.service_config.service_name:
                 target_registry = "IPRS"
            elif "Business" in self.service_request.service_config.service_name:
                 target_registry = "BRS"
            elif "Birth" in self.service_request.service_config.service_name:
                 target_registry = "CRS"

        # 2. Prepare Payload (Merge local form data with Step Config)
        payload = self.service_request.payload.copy()
        if step.action:
            payload['action'] = step.action
        
        # 3. Support Internal Logic vs. External Bridge
        if api_url.startswith('internal://'):
            self._execute_internal_action(step, payload)
            return

        # 4. Call KeSEL (Huduma Bridge) with Mock NPKI Signature
        from .kesel import KeSEL
        security_context = {"signed": True, "cert_id": "GOV-CA-12345"}
        
        try:
            response = KeSEL.exchange(target_registry, payload, security_context)
            
            if response.get("status") in ["SUCCESS"]:
                AuditLog.objects.create(
                    service_request=self.service_request,
                    action='KESEL_EXCHANGE_SUCCESS',
                    details=f"Verified with {target_registry}: {response.get('message', 'OK')}"
                )
                
                # Digital Signature Verification Logic for POC
                if step.action == 'verify_signature':
                    AuditLog.objects.create(
                        service_request=self.service_request,
                        action='DIGITAL_SIGNATURE_VERIFIED',
                        details="NPKI X.509 Digital Signature verified against GOK Root CA."
                    )
                
                self.process_workflow_step()
            else:
                 # Auto-reject or Flag for manual review if external check fails
                AuditLog.objects.create(
                    service_request=self.service_request,
                    action='KESEL_VALIDATION_FAILED',
                    details=f"{target_registry} returned: {response.get('message')}"
                )
                # For this POC, let's behave like a strict system: Validation Failure stops the flow
                self.service_request.status = 'validation_failed'
                self.service_request.save()
                send_notification(self.service_request.citizen, f"Your request failed automated validation: {response.get('message')}. Please contact support.", self.service_request)

        except Exception as e:
            print(f"KeSEL connection error: {e}")
            AuditLog.objects.create(
                service_request=self.service_request,
                action='KESEL_ERROR',
                details=f"Transport error: {str(e)}"
            )

    def _execute_internal_action(self, step: WorkflowStep, payload: dict):
        """
        Handles system-internal automated steps (e.g. updating a user profile).
        """
        print(f"WORKFLOW [Internal]: Executing local system action '{step.action}'")
        
        if step.action == 'update_user_profile':
            citizen = self.service_request.citizen
            # Update profile from payload
            if 'phone_number' in payload:
                citizen.phone_number = payload['phone_number']
            if 'passport_number' in payload:
                citizen.passport_number = payload['passport_number']
            citizen.save()
            
            AuditLog.objects.create(
                service_request=self.service_request,
                action='INTERNAL_PROFILE_UPDATE',
                details="Authoritative citizen profile updated from verified request."
            )
            self.process_workflow_step()
        else:
             # Default success for other internal tasks in POC
             self.process_workflow_step()

    def _notify_manual_review(self, step: WorkflowStep):
        """
        Notifies officers assigned to the current role.
        """
        # Support both legacy role strings and new RBAC role names
        from django.db.models import Q
        officers = User.objects.filter(
            Q(role__icontains=step.role) | 
            Q(user_role__name__icontains=step.role)
        )
        for officer in officers:
            send_notification(officer, f"Pending Task: Request {self.service_request.request_id} requires {step.action}.", self.service_request)
            
        AuditLog.objects.create(
            service_request=self.service_request,
            action='MANUAL_STEP_ASSIGNED',
            details=f"Task assigned to role: {step.role}"
        )

    @transaction.atomic
    def complete_manual_step(self, user: User, action: str, details: str = None):
        """
        Handles the outcome of an officer's manual review.
        """
        if not self.service_request or not self.service_request.current_step:
            return

        # Ensure user has the right role
        # Ensure user has the right role or is specifically assigned
        resolved_role = user.user_role.name if user.user_role else user.role
        is_privileged = resolved_role in ['admin', 'system_admin', 'GLOBAL_SUPERVISOR']
        
        if self.service_request.assigned_to != user and not is_privileged:
             raise PermissionError("You must claim this task before you can complete it (only site admins/global supervisors can bypass).")

        AuditLog.objects.create(
            service_request=self.service_request,
            actor=user,
            action=f'OFFICER_ACTION_{action.upper()}',
            details=details or f"Action '{action}' performed by {user.username}."
        )

        if action.lower() == 'reject':
            self._finalize_request('rejected')
        else:
            self.process_workflow_step()

    def _finalize_request(self, outcome: str):
        """
        Closes the request and notifies the citizen.
        """
        self.service_request.status = outcome
        self.service_request.current_step = None
        self.service_request.save()

        AuditLog.objects.create(
            service_request=self.service_request,
            action=f'WORKFLOW_{outcome.upper()}',
            details=f"Service request has been {outcome}."
        )

        # POC Addition: If Approved, Trigger Authoritative Output Automation
        if outcome == 'approved':
            try:
                from .utils.document_generator import DocumentGenerator
                from .registries import get_registry
                
                # 1. Generate the Digital Output (Barcoded & Digitally Signed)
                digital_doc = DocumentGenerator.generate_output(self.service_request)
                
                # 2. Issue to User's Digital Wallet (Saved Documents)
                citizen = self.service_request.citizen
                if not isinstance(citizen.saved_documents, list):
                    citizen.saved_documents = []
                
                citizen.saved_documents.append(digital_doc)
                citizen.save()
                
                # 3. Archive to EDRMS
                DocumentGenerator.archive_to_edrms(digital_doc)
                
                # 4. POC DYNAMIC REGISTRY UPDATE (Vital for End-to-End Demo)
                # This simulates the "Backend Write-Back" where a finished workflow updates the master list.
                svc_code = self.service_request.service_config.service_code
                payload = self.service_request.payload
                auth_id = digital_doc['authoritative_id']
                
                if svc_code == 'BIRTH_REG':
                    # Add to CRS Registry
                    crs = get_registry('CRS')
                    new_record = {
                        "full_name": payload.get('child_full_name'),
                        "date_of_birth": payload.get('date_of_birth'),
                        "gender": payload.get('sex'),
                        "county": payload.get('county'),
                        "mother_name": payload.get('mother_name'),
                        "mother_id": payload.get('mother_id'),
                        "father_name": payload.get('father_name'),
                        "father_id": payload.get('father_id'),
                         # In Demo mode, we might just copy the DOB year - 18 if user requested, 
                         # but here we just store what was applied for.
                    }
                    if crs:
                        crs.BIRTH_RECORDS[auth_id] = new_record
                        print(f"REGISTRY UPDATE [CRS]: Added {auth_id} for {new_record['full_name']}")

                elif svc_code == 'NATIONAL_ID':
                    # Add to IPRS Registry (Mock)
                    iprs = get_registry('IPRS')
                    new_record = {
                        "full_name": payload.get('full_name'),
                        "status": "ALIVE",
                        "date_of_birth": payload.get('date_of_birth'),
                        "gender": payload.get('gender')
                    }
                    if iprs:
                        # auth_id here is the ID Number
                        iprs.CITIZENS[auth_id] = new_record
                        
                        # Also update local User profile if it matches
                        if citizen.id_number != auth_id:
                            citizen.id_number = auth_id
                            citizen.save()
                            
                        print(f"REGISTRY UPDATE [IPRS]: Added ID {auth_id} for {new_record['full_name']}")

                elif svc_code == 'KRA_PIN_REG':
                     kra = get_registry('KRA')
                     # No explicit store in mock registry needed for verify action as it checks length,
                     # but good to have if we expand verification logic.
                     # For now, just logging.
                     print(f"REGISTRY UPDATE [KRA]: Issued PIN {auth_id}")
                     
                     # Update profile
                     citizen.kra_pin = auth_id # Assuming we add this field or store in profile logic
                     citizen.save()

                elif svc_code == 'BIZ_INCORPORATION':
                    brs = get_registry('BRS')
                    if brs:
                        brs.EXISTING_BUSINESSES.append(payload.get('proposed_name_1'))
                        print(f"REGISTRY UPDATE [BRS]: Reserved {payload.get('proposed_name_1')}")
                
                elif svc_code == 'NEMIS_REG':
                    nemis = get_registry('NEMIS')
                    if nemis: 
                         # Store the issued UPI
                         # In a real system, we'd store full student details.
                         # Here we just log it as a success for the demo flow.
                         print(f"REGISTRY UPDATE [NEMIS]: Issued UPI {auth_id} to student.")
                
                AuditLog.objects.create(
                    service_request=self.service_request,
                    action='EDRMS_ARCHIVED',
                    details=f"Authoritative Document {auth_id} generated and archived in EDRMS."
                )
                
                send_notification(
                    self.service_request.citizen, 
                    f"Congratulations! Your {self.service_request.service_config.service_name} has been issued. Check your Digital Wallet.", 
                    self.service_request
                )
                
            except Exception as e:
                print(f"FAILED OUTPUT AUTOMATION: {e}")

        send_notification(self.service_request.citizen, f"Final Update: Your request {self.service_request.request_id} is {outcome}.", self.service_request)
