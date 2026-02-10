from django.test import TestCase
from django.contrib.auth import get_user_model
from service_api.models import MDA, ServiceConfig, WorkflowStep, ServiceRequest, AuditLog
from service_api.workflow import WorkflowEngine
from unittest.mock import patch

User = get_user_model()

class WorkflowEngineTestCase(TestCase):
    def setUp(self):
        self.citizen_user = User.objects.create_user('citizen', 'citizen@example.com', 'password', role='citizen')
        self.officer_user = User.objects.create_user('officer', 'officer@example.com', 'password', role='officer')
        self.supervisor_user = User.objects.create_user('supervisor', 'supervisor@example.com', 'password', role='supervisor')

        self.mda = MDA.objects.create(name='Ministry of Test', description='Test MDA')
        self.service_config_manual = ServiceConfig.objects.create(
            service_code='MANUAL_SVC',
            service_name='Manual Service',
            mda=self.mda,
            config={'rules': {'schema': {'properties': {'field1': {'type': 'string'}}}}}
        )
        self.step_officer_review = WorkflowStep.objects.create(
            service_config=self.service_config_manual,
            step_name='Officer Review',
            role='officer',
            action='review',
            sequence=1
        )
        self.step_supervisor_approve = WorkflowStep.objects.create(
            service_config=self.service_config_manual,
            step_name='Supervisor Approval',
            role='supervisor',
            action='approve',
            sequence=2
        )
        self.service_config_auto = ServiceConfig.objects.create(
            service_code='AUTO_SVC',
            service_name='Auto Service',
            mda=self.mda,
            config={'rules': {'schema': {'properties': {'field2': {'type': 'number'}}}}}
        )
        self.step_auto_process = WorkflowStep.objects.create(
            service_config=self.service_config_auto,
            step_name='Automated Validation',
            role='system',
            action='auto_validate',
            auto_process=True,
            sequence=1
        )
        self.step_final_check = WorkflowStep.objects.create(
            service_config=self.service_config_auto,
            step_name='Final Check',
            role='officer',
            action='check',
            sequence=2
        )

    @patch('service_api.workflow.send_notification')
    def test_create_service_request_manual_workflow(self, mock_send_notification):
        engine = WorkflowEngine()
        service_request = engine.create_service_request(
            self.citizen_user,
            self.service_config_manual,
            {'field1': 'test_value'}
        )
        self.assertIsNotNone(service_request.id)
        self.assertEqual(service_request.citizen, self.citizen_user)
        self.assertEqual(service_request.service_config, self.service_config_manual)
        self.assertEqual(service_request.status, 'in_progress')
        self.assertEqual(service_request.current_step, self.step_officer_review)
        self.assertEqual(AuditLog.objects.count(), 2) # Request created + Step started
        mock_send_notification.assert_called_once() # Citizen notified for request created

    @patch('service_api.workflow.send_notification')
    def test_create_service_request_auto_workflow(self, mock_send_notification):
        engine = WorkflowEngine()
        service_request = engine.create_service_request(
            self.citizen_user,
            self.service_config_auto,
            {'field2': 123}
        )
        self.assertIsNotNone(service_request.id)
        self.assertEqual(service_request.citizen, self.citizen_user)
        self.assertEqual(service_request.service_config, self.service_config_auto)
        # Auto step should have processed, so it should be at the next step
        self.assertEqual(service_request.current_step, self.step_final_check)
        self.assertEqual(service_request.status, 'in_progress')
        self.assertEqual(AuditLog.objects.count(), 3) # Request created + Auto step started + Auto step completed
        self.assertEqual(AuditLog.objects.filter(action__startswith='AUTO_STEP_COMPLETED').count(), 1)
        mock_send_notification.assert_called_once() # Citizen notified for request created

    @patch('service_api.workflow.send_notification')
    def test_complete_manual_step_success(self, mock_send_notification):
        engine = WorkflowEngine()
        service_request = engine.create_service_request(
            self.citizen_user,
            self.service_config_manual,
            {'field1': 'test_value'}
        )
        self.assertEqual(service_request.current_step, self.step_officer_review)
        
        engine_for_completion = WorkflowEngine(request_id=service_request.request_id)
        engine_for_completion.complete_manual_step(self.officer_user, 'approved', 'Looks good')
        
        service_request.refresh_from_db()
        self.assertEqual(service_request.current_step, self.step_supervisor_approve)
        self.assertEqual(AuditLog.objects.count(), 4) # +1 for manual step completion +1 for next step started
        self.assertEqual(AuditLog.objects.filter(action__startswith='MANUAL_STEP_ACTION').count(), 1)
        self.assertEqual(mock_send_notification.call_count, 3) # Citizen created, Officer notified, Citizen updated

    def test_complete_manual_step_permission_denied(self):
        engine = WorkflowEngine()
        service_request = engine.create_service_request(
            self.citizen_user,
            self.service_config_manual,
            {'field1': 'test_value'}
        )
        
        engine_for_completion = WorkflowEngine(request_id=service_request.request_id)
        with self.assertRaises(PermissionError):
            engine_for_completion.complete_manual_step(self.supervisor_user, 'approved', 'Looks good') # Wrong role

    def test_complete_manual_step_invalid_action(self):
        engine = WorkflowEngine()
        service_request = engine.create_service_request(
            self.citizen_user,
            self.service_config_manual,
            {'field1': 'test_value'}
        )
        
        engine_for_completion = WorkflowEngine(request_id=service_request.request_id)
        with self.assertRaises(ValueError):
            engine_for_completion.complete_manual_step(self.officer_user, 'invalid_action', 'Details')

    @patch('service_api.workflow.send_notification')
    def test_workflow_completion(self, mock_send_notification):
        engine = WorkflowEngine()
        service_request = engine.create_service_request(
            self.citizen_user,
            self.service_config_manual,
            {'field1': 'test_value'}
        )
        
        engine_for_completion1 = WorkflowEngine(request_id=service_request.request_id)
        engine_for_completion1.complete_manual_step(self.officer_user, 'approved', 'Officer done')
        
        service_request.refresh_from_db()
        self.assertEqual(service_request.current_step, self.step_supervisor_approve)

        engine_for_completion2 = WorkflowEngine(request_id=service_request.request_id)
        engine_for_completion2.complete_manual_step(self.supervisor_user, 'approved', 'Supervisor done')

        service_request.refresh_from_db()
        self.assertIsNone(service_request.current_step)
        self.assertEqual(service_request.status, 'closed')
        self.assertEqual(AuditLog.objects.filter(action='WORKFLOW_COMPLETED').count(), 1)
        self.assertEqual(mock_send_notification.call_count, 5) # Citizen created, Officer notified, Citizen updated, Supervisor notified, Citizen completed
