from django.test import TestCase, override_settings
from unittest.mock import patch, MagicMock
from service_api.models import MDA, ServiceConfig, WorkflowStep, ServiceRequest, User, WorkflowStepExecution
from service_api.workflow import WorkflowEngine

@override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES=True)
@patch('django.db.transaction.on_commit', lambda f: f())
class WorkflowEngineIntegrationTest(TestCase):
    def setUp(self):
        # Setup Data
        self.mda = MDA.objects.create(code='TEST_MDA', name='Test Authority')
        self.service = ServiceConfig.objects.create(
            service_code='TEST-SVC-001',
            service_name='Test Integrated Service',
            mda=self.mda
        )
        self.citizen = User.objects.create_user(username='test_citizen', password='password1')
        self.officer = User.objects.create_user(username='test_officer', role='officer', mda=self.mda)
        
        # Steps
        self.step1 = WorkflowStep.objects.create(
            service_config=self.service, step_name='Verification', step_type='api_call', 
            bpmn_element_type='service_task', lifecycle_stage='to_be', sequence=1,
            api_config={'outcomes': [{'label': 'verified', 'target_sequence': 2}, {'label': 'failed', 'target_sequence': 3}]}
        )
        self.step2 = WorkflowStep.objects.create(
            service_config=self.service, step_name='Approval', step_type='manual', 
            bpmn_element_type='user_task', lifecycle_stage='to_be', sequence=2, role='officer',
            api_config={'outcomes': [{'label': 'approve', 'target_sequence': None}]}
        )
        self.step3 = WorkflowStep.objects.create(
            service_config=self.service, step_name='Fallback', step_type='manual', 
            bpmn_element_type='exclusive_gateway', lifecycle_stage='to_be', sequence=3, role='officer'
        )

    @patch('service_api.kesel.KeSEL.exchange')
    def test_happy_path(self, mock_exchange):
        """1. Happy Path: KeSEL success -> to manual step -> approve."""
        mock_exchange.return_value = {'status': 'SUCCESS'}
        
        engine = WorkflowEngine()
        request = engine.create_service_request(self.citizen, self.service, {})
        request.refresh_from_db()
        
        self.assertEqual(request.current_step, self.step2, 
            f'[AI_FIX_REQUIRED] Test: "test_happy_path", Error: "State Mismatch", Detail: "Engine expected to land on manual step (sequence 2) after KeSEL success, but landed on sequence {request.current_step.sequence if request.current_step else "None"}."')

        # Claim and Approve
        request.assigned_to = self.officer
        request.save()
        
        engine = WorkflowEngine(request.request_id)
        engine.complete_manual_step(self.officer, 'approve')
        
        request.refresh_from_db()
        self.assertEqual(request.status, 'approved', 
            f'[AI_FIX_REQUIRED] Test: "test_happy_path", Error: "Finalization Failure", Detail: "Request status should be \'approved\' after manual completion, but is \'{request.status}\'."')

    @patch('service_api.kesel.KeSEL.exchange')
    def test_fallback_path(self, mock_exchange):
        """2. Fallback Path: KeSEL failure -> manual fallback step."""
        mock_exchange.return_value = {'status': 'FAILED', 'message': 'API Error'}
        
        engine = WorkflowEngine()
        request = engine.create_service_request(self.citizen, self.service, {})
        request.refresh_from_db()
        
        self.assertEqual(request.current_step, self.step3, 
            f'[AI_FIX_REQUIRED] Test: "test_fallback_path", Error: "State Mismatch", Detail: "Engine expected to land on manual step (sequence 3) after KeSEL failure, but landed on sequence {request.current_step.sequence if request.current_step else "None"}."')

    def test_two_person_rule(self):
        """3. Two-Person Rule: Citizen cannot approve own request."""
        request = ServiceRequest.objects.create(
            request_id='REQ-SEC-001', citizen=self.citizen, service_config=self.service, 
            payload={}, status='in_progress', current_step=self.step2
        )
        WorkflowStepExecution.objects.create(service_request=request, step=self.step2, status='pending')
        
        engine = WorkflowEngine(request.request_id)
        try:
             engine.complete_manual_step(self.citizen, 'approve')
             self.fail(f'[AI_FIX_REQUIRED] Test: "test_two_person_rule", Error: "Security Bypass", Detail: "Citizen was able to approve their own request."')
        except PermissionError:
             pass
        except Exception as e:
             self.fail(f'[AI_FIX_REQUIRED] Test: "test_two_person_rule", Error: "Wrong Exception", Detail: "Caught {type(e).__name__} instead of PermissionError."')
