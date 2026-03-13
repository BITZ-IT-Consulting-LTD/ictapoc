import uuid
import json
import urllib.request
from django.db import transaction
from .models import ServiceRequest, ServiceConfig, WorkflowStep, AuditLog, User, WorkflowStepExecution
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

def send_notification(user, message, request=None):
    """
    Sends email and simulates in-app notifications.
    Now triggers a Celery task for non-blocking execution.
    """
    from .tasks import send_notification_task
    subject = f"GOK Platform: Request {request.request_id}" if request else "Government Services Platform Notification"
    
    # Trigger background task
    send_notification_task.delay(user.email, subject, message)
    
    # Internal log for visibility
    print(f"NOTIFICATION_QUEUED [To: {user.username}]: {message}")

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
                # Use select_for_update to lock the row for the duration of the transaction
                self.service_request = ServiceRequest.objects.select_for_update().get(request_id=request_id)
            except ServiceRequest.DoesNotExist:
                pass
    @transaction.atomic
    def create_service_request(self, citizen: User, service_config: ServiceConfig, payload: dict):
        """
        Initializes a new service request and starts the workflow.
        """
        # DRMS Integration: If the payload contains a base64 supporting document, store it in DRMS
        if isinstance(payload, dict) and 'supporting_document' in payload:
            doc_data = payload['supporting_document']
            if isinstance(doc_data, dict) and 'content' in doc_data and str(doc_data['content']).startswith('data:'):
                try:
                    from apps.document_repository.utils import create_document_from_base64
                    drms_doc = create_document_from_base64(
                        user=citizen,
                        title=doc_data.get('name', f"Supporting Proof - {service_config.service_name}"),
                        base64_content=doc_data['content'],
                        document_type='supporting_proof',
                        metadata={'service_code': service_config.service_code, 'context': 'request_submission'}
                    )
                    if drms_doc:
                        payload['supporting_document_drms_uuid'] = str(drms_doc.uuid)
                        # Remove base64 to keep payload lean if desired, or keep it for the first step
                except ImportError:
                    pass

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
    def process_workflow_step(self, force_refresh=False, target_sequence=None):
        """
        Moves the request to the next step. 
        If target_sequence is provided, jumps to that specific step.
        """
        if not self.service_request:
            print("ERROR: process_workflow_step called with no service_request.")
            return

        print(f"DEBUG: Entering process_workflow_step. Current: {self.service_request.current_step.step_name if self.service_request.current_step else 'START'}")

        # 1. Complete the current step execution if it exists
        if self.service_request.current_step:
            execution = WorkflowStepExecution.objects.filter(
                service_request=self.service_request,
                step=self.service_request.current_step,
                completed_at__isnull=True
            ).last()
            if execution:
                execution.status = 'completed'
                execution.completed_at = timezone.now()
                delta = execution.completed_at - execution.started_at
                execution.duration_seconds = int(delta.total_seconds())
                execution.save()

        service_config = self.service_request.service_config
        current_seq = self.service_request.current_step.sequence if self.service_request.current_step else 0

        next_step_data = None

        if target_sequence:
            next_step_data = WorkflowStep.objects.filter(
                service_config=service_config,
                sequence=target_sequence
            ).first()
        
        if not next_step_data:
            # Fallback to standard sequence logic
            target_stage = 'to_be'
            if self.service_request.current_step:
                target_stage = self.service_request.current_step.lifecycle_stage
            elif not WorkflowStep.objects.filter(service_config=service_config, lifecycle_stage='to_be').exists():
                target_stage = 'as_is'

            next_step_data = WorkflowStep.objects.filter(
                service_config=service_config, 
                lifecycle_stage=target_stage,
                sequence__gt=current_seq
            ).order_by('sequence').first()

        if next_step_data:
            self.service_request.current_step = next_step_data
            self.service_request.status = 'in_progress'
            self.service_request.save()

            # 2. Create the Start signal for the next workflow item
            exec_status = 'scheduled' if next_step_data.step_type == 'api_call' else 'pending'
            WorkflowStepExecution.objects.create(
                service_request=self.service_request,
                step=next_step_data,
                status=exec_status
            )

            AuditLog.objects.create(
                service_request=self.service_request,
                action='STEP_TRANSITION',
                details=f"Workflow advanced to Step {next_step_data.sequence}: {next_step_data.step_name}"
            )

            if next_step_data.step_type == 'api_call':
                from .tasks import execute_system_step_task
                transaction.on_commit(
                    lambda: execute_system_step_task.delay(self.service_request.request_id, next_step_data.id)
                )
            else:
                self._notify_manual_review(next_step_data)
        else:
            # Workflow complete
            self._finalize_request('approved')

        
    @transaction.atomic
    def process_async_api_call(self, step_id):
        """
        Executes an automated check via the Huduma Bridge (KeSEL) in a background task.
        Supports outcome-based branching for both success and failure states.
        """
        step = WorkflowStep.objects.get(id=step_id)
        # Re-fetch with lock for safety
        self.service_request = ServiceRequest.objects.select_for_update().get(request_id=self.request_id)
        
        print(f"WORKFLOW [Orchestration]: Initiating background exchange for step '{step.step_name}'")
        
        # Re-verify lock and status
        if not self.service_request:
             print("ERROR: Service request missing from engine context.")
             return
        
        # Update execution record to signal it's being processed immediately
        execution = WorkflowStepExecution.objects.filter(
            service_request=self.service_request,
            step=step,
            completed_at__isnull=True
        ).last()
        if execution:
            execution.status = 'in_progress'
            execution.details = f"System scheduled process triggered for {step.step_name}..."
            execution.save()
        
        # 1. Determine Target Registry
        target_registry = None
        api_config = step.api_config or {}
        api_url = api_config.get('url', '')
        
        if api_url:
            parts = api_url.split('/')
            if len(parts) > 1 and parts[0] in ['KESEL_BRIDGE', 'HUB_BRIDGE', 'HUDUMA_BRIDGE']:
                target_registry = parts[1]
        
        if not target_registry:
            target_registry = "IPRS" 
            if "Passport" in self.service_request.service_config.service_name: target_registry = "IPRS"
            elif "Business" in self.service_request.service_config.service_name: target_registry = "BRS"
            elif "Birth" in self.service_request.service_config.service_name: target_registry = "CRS"

        payload = self.service_request.payload.copy()
        if step.action: payload['action'] = step.action
        
        if api_url.startswith('internal://'):
            print(f"DEBUG: Found internal URL: {api_url}")
            self._execute_internal_action(step, payload)
            return

        from .kesel import KeSEL
        try:
            # Execute the secure exchange via Huduma Bridge
            response = KeSEL.exchange(target_registry, payload, {"signed": True, "cert_id": "GOV-CA-12345"})
            
            # Map labels to branching logic
            outcomes = api_config.get('outcomes', [])
            target_seq = None

            if response.get("status") in ["SUCCESS"]:
                AuditLog.objects.create(
                    service_request=self.service_request,
                    action='KESEL_EXCHANGE_SUCCESS',
                    details=f"Verified with {target_registry}: {response.get('message', 'OK')}"
                )
                
                # Check for Success-based branching
                for outcome in outcomes:
                    if outcome.get('label', '').lower() in ['verified', 'success', 'approved', 'yes']:
                        target_seq = outcome.get('target_sequence')
                        break
                
                self.process_workflow_step(target_sequence=target_seq)
            else:
                # Handle failure branching if defined, otherwise use standard failure logic
                AuditLog.objects.create(
                    service_request=self.service_request,
                    action='KESEL_VALIDATION_FAILED',
                    details=f"{target_registry} returned: {response.get('message')}"
                )

                for outcome in outcomes:
                    if outcome.get('label', '').lower() in ['failure', 'failed', 'rejected', 'no', 'non_compliant']:
                        target_seq = outcome.get('target_sequence')
                        break
                
                if target_seq:
                    # Move to manual fallback or gateway as defined in outcomes
                    self.process_workflow_step(target_sequence=target_seq)
                else:
                    self._handle_validation_failure(target_registry, response)

        except Exception as e:
            print(f"EXCEPTION in process_async_api_call: {str(e)}")
            import traceback
            traceback.print_exc()
            self._handle_transport_error(target_registry, e)

    def _handle_validation_failure(self, registry, response):
        """Standard handler for business-level validation failures when no fallback is defined."""
        self.service_request.status = 'validation_failed'
        self.service_request.save()
        send_notification(self.service_request.citizen, f"Your request failed automated validation: {response.get('message')}. Please contact Huduma Support.", self.service_request)

    def _handle_transport_error(self, registry, error):
        """Standard handler for technical connection errors."""
        print(f"KeSEL connection error: {error}")
        AuditLog.objects.create(
            service_request=self.service_request,
            action='KESEL_ERROR',
            details=f"Transport error communicating with {registry}: {str(error)}"
        )
        self.service_request.status = 'validation_failed'
        self.service_request.save()
        send_notification(self.service_request.citizen, f"A system communication error occurred. Ref: {self.service_request.request_id}", self.service_request)

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
        Notifies officers assigned to the current role and performs load-balanced auto-assignment.
        """
        from django.db.models import Q, Count
        
        target_role = step.role
        target_mda = step.target_mda or self.service_request.service_config.mda
        
        eligible_query = Q(role__icontains=target_role) | Q(user_role__name__icontains=target_role) | Q(role__icontains=f"GLOBAL_{target_role}") | Q(user_role__name__icontains=f"GLOBAL_{target_role}")
        
        if target_mda:
            # Match users who belong to this MDA or are multi-assigned to it
            # OR anyone who is a GLOBAL officer/supervisor
            global_perms = Q(role__in=['GLOBAL_OFFICER', 'GLOBAL_SUPERVISOR', 'admin', 'system_admin']) | \
                          Q(user_role__name__in=['GLOBAL_OFFICER', 'GLOBAL_SUPERVISOR'])
            
            mda_query = Q(mda=target_mda) | Q(assigned_mdas=target_mda)
            
            eligible_query &= (mda_query | global_perms)
        
        # 2. Load-Balancing: Find the officer with the least current tasks
        eligible_officers = User.objects.filter(eligible_query).annotate(
            task_load=Count('assigned_tasks', filter=Q(assigned_tasks__status='in_progress'))
        ).order_by('task_load')

        assigned_user = None
        if eligible_officers.exists():
            assigned_user = eligible_officers.first()
            self.service_request.assigned_to = assigned_user
            self.service_request.save()
            
            print(f"WORKFLOW [Assignment]: Auto-assigned {self.service_request.request_id} to {assigned_user.username} (Load: {assigned_user.task_load})")
            
            send_notification(
                assigned_user, 
                f"New Task Assigned: Request {self.service_request.request_id} for {self.service_request.service_config.service_name}.", 
                self.service_request
            )
        
        # 3. Fallback: Notify all eligible if no one was explicitly assigned or in addition to assignment
        if not assigned_user:
            for officer in User.objects.filter(eligible_query):
                send_notification(officer, f"Unassigned Task: Request {self.service_request.request_id} requires {step.step_name}.", self.service_request)
            
        AuditLog.objects.create(
            service_request=self.service_request,
            action='MANUAL_STEP_ASSIGNED',
            details=f"Task assigned to role '{target_role}' (Auto-assigned to: {assigned_user.username if assigned_user else 'None'})"
        )

    @transaction.atomic
    def complete_manual_step(self, user: User, action: str, details: str = None, payload: dict = None):
        """
        Handles the outcome of an officer's manual review.
        """
        if not self.service_request or not self.service_request.current_step:
            return

        # Update payload if provided (Incremental data capture)
        if payload:
            if not self.service_request.payload:
                self.service_request.payload = {}
            self.service_request.payload.update(payload)
            self.service_request.save()

        # Ensure user has the right role
        # Ensure user has the right role or is specifically assigned
        resolved_role = user.user_role.name if user.user_role else user.role
        is_privileged = resolved_role in ['admin', 'system_admin', 'GLOBAL_SUPERVISOR']
        
        if self.service_request.assigned_to != user and not is_privileged:
             raise PermissionError("You must claim this task before you can complete it (only site admins/global supervisors can bypass).")

        # 1.5 Two-Person Rule Enforcement
        # Prevent the citizen who created the request from approving it
        if self.service_request.citizen == user and action.lower() in ['approve', 'complete', 'verify']:
            raise PermissionError("Access Denied: The two-person rule prevents you from approving your own request.")

        # Update execution record with manual disposition
        execution = WorkflowStepExecution.objects.filter(
            service_request=self.service_request,
            step=self.service_request.current_step,
            completed_at__isnull=True
        ).last()
        if execution:
            execution.actor = user
            execution.action_taken = action
            execution.details = details
            execution.status = 'in_progress'
            execution.save()

        # 2. Dynamic Hierarchy Check: Ensure current step index matches user's role capability
        # In a fully dynamic system, we just check if they are authorized for THIS specific step.
        # We removed the hardcoded 'if officer then supervisor' logic.
        current_step = self.service_request.current_step
        
        # Logging context for the dynamic transition
        AuditLog.objects.create(
            service_request=self.service_request,
            actor=user,
            action=f'ACTION_{action.upper()}',
            details=details or f"Disposition '{action}' finalized for step {current_step.sequence} by {user.username}."
        )

        if action.lower() == 'reject':
            # Close the current execution before finalizing
            execution = WorkflowStepExecution.objects.filter(
                service_request=self.service_request,
                step=current_step,
                completed_at__isnull=True
            ).last()
            if execution:
                execution.status = 'failed'
                execution.completed_at = timezone.now()
                execution.save()
                
            self._finalize_request('rejected')
            return

        # Check for branching outcomes in manual steps
        target_seq = None
        api_config = current_step.api_config or {}
        outcomes = api_config.get('outcomes', [])
        
        for outcome in outcomes:
            if outcome.get('label', '').lower() == action.lower():
                target_seq = outcome.get('target_sequence')
                break
        
        # If an outcome was matched but has no target, it's a completion
        if outcomes and target_seq is None and any(o.get('label', '').lower() == action.lower() for o in outcomes):
             self._finalize_request('approved')
        else:
             self.process_workflow_step(target_sequence=target_seq)

    def _finalize_request(self, outcome: str):
        """
        Closes the request and notifies the citizen.
        """
        self.service_request.status = outcome
        self.service_request.current_step = None
        self.service_request.completed_at = timezone.now()
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
                
                if svc_code in ['BIRTH_REG', 'CRS-CERT-001', 'MOH-NOTIF-001']:
                    # Add to CRS Registry
                    crs = get_registry('CRS')
                    
                    # For Hospital Notifications, status is PENDING_CERTIFICATE
                    # For Certificates, status is ISSUED
                    record_status = 'ISSUED' if svc_code != 'MOH-NOTIF-001' else 'PENDING_CERTIFICATE'
                    
                    new_record = {
                        "full_name": payload.get('child_full_name', payload.get('child_name', 'N/A')),
                        "date_of_birth": payload.get('date_of_birth'),
                        "gender": payload.get('sex', payload.get('child_gender')),
                        "county": payload.get('county'),
                        "mother_name": payload.get('mother_name'),
                        "mother_id": payload.get('mother_id'),
                        "father_name": payload.get('father_name'),
                        "father_id": payload.get('father_id'),
                        "status": record_status
                    }
                    if crs:
                        crs.RECORDS[auth_id] = new_record
                        print(f"REGISTRY UPDATE [CRS]: Added {auth_id} for {new_record['full_name']}")
                    
                    # Also update DB-driven RegistryAdapter for KeSEL visibility
                    try:
                        from .models import RegistryAdapter
                        crs_adapter = RegistryAdapter.objects.get(code='CRS')
                        if crs_adapter.is_mock:
                            crs_adapter.mock_data[auth_id] = new_record
                            crs_adapter.save()
                    except Exception as e:
                        print(f"REGISTRY ADAPTER UPDATE FAILED: {e}")

                elif svc_code in ['NATIONAL_ID', 'NRB-ID-001']:
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

                elif svc_code in ['KRA_PIN_REG', 'KRA-TAX-001']:
                     kra = get_registry('KRA')
                     # No explicit store in mock registry needed for verify action as it checks length,
                     # but good to have if we expand verification logic.
                     # For now, just logging.
                     print(f"REGISTRY UPDATE [KRA]: Issued PIN {auth_id}")
                     
                     # Update profile
                     citizen.kra_pin = auth_id # Assuming we add this field or store in profile logic
                     citizen.save()

                elif svc_code in ['BIZ_INCORPORATION', 'BRS-INC-001']:
                    brs = get_registry('BRS')
                    if brs:
                        brs.EXISTING_BUSINESSES.append(payload.get('proposed_name_1'))
                        print(f"REGISTRY UPDATE [BRS]: Reserved {payload.get('proposed_name_1')}")
                
                elif svc_code in ['NEMIS_REG', 'MOE-NEMIS-001']:
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
                
                # 5. DYNAMIC LIFECYCLE TRIGGERING (The Bridge)
                # When one life event finishes, automatically trigger the next in the chain
                LIFECYCLE_CHAIN = {
                    'MOH-NOTIF-001': 'CRS-CERT-001',   # Birth Notification -> Birth Certificate
                    'CRS-CERT-001': 'MOE-NEMIS-001',  # Birth Certificate -> School Enrollment
                    'MOE-NEMIS-001': 'NRB-ID-001',    # NEMIS -> National ID
                    'NRB-ID-001': 'KRA-TAX-001',      # National ID -> KRA PIN
                    'KRA-TAX-001': 'IMM-PASS-001'     # KRA PIN -> Passport Eligibility
                }
                
                next_svc_code = LIFECYCLE_CHAIN.get(svc_code)
                if next_svc_code:
                    try:
                        next_svc_config = ServiceConfig.objects.get(service_code=next_svc_code)
                        
                        # Prepare payload for the next step (carrying over the authoritative ID/UPI)
                        next_payload = self.service_request.payload.copy()
                        
                        # Correctly map the authoritative ID to the expected field for the next service
                        if svc_code == 'MOH-NOTIF-001':
                            next_payload['notification_number'] = auth_id
                        elif 'upi' not in next_payload and auth_id:
                            next_payload['upi'] = auth_id
                        
                        # Trigger the next service automatically
                        new_engine = WorkflowEngine()
                        new_request = new_engine.create_service_request(
                            citizen=self.service_request.citizen,
                            service_config=next_svc_config,
                            payload=next_payload
                        )
                        
                        AuditLog.objects.create(
                            service_request=self.service_request,
                            action='LIFECYCLE_CASCADE_TRIGGER',
                            details=f"Automated Cascade: Triggered '{next_svc_config.service_name}' based on completion of current stage."
                        )
                        
                        print(f"LIFECYCLE [Cascade]: Successfully triggered {next_svc_code} for user {citizen.username}")
                        
                    except ServiceConfig.DoesNotExist:
                        print(f"LIFECYCLE [Warning]: Target service {next_svc_code} not found in registry.")
                
                send_notification(
                    self.service_request.citizen, 
                    f"Congratulations! Your {self.service_request.service_config.service_name} has been issued. Check your Digital Wallet.", 
                    self.service_request
                )
                
            except Exception as e:
                print(f"FAILED OUTPUT AUTOMATION: {e}")

        send_notification(self.service_request.citizen, f"Final Update: Your request {self.service_request.request_id} is {outcome}.", self.service_request)
