from django.test import TestCase
from django.contrib.auth import get_user_model
from service_api.models import MDA, ServiceConfig, WorkflowStep, ServiceRequest, AuditLog

User = get_user_model()

class ModelTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.citizen_user = User.objects.create_user('citizen', 'citizen@example.com', 'password', role='citizen')
        self.officer_user = User.objects.create_user('officer', 'officer@example.com', 'password', role='officer')
        self.supervisor_user = User.objects.create_user('supervisor', 'supervisor@example.com', 'password', role='supervisor')

        self.mda = MDA.objects.create(name='Ministry of Test', description='Test MDA')
        self.service_config = ServiceConfig.objects.create(
            service_code='TEST_SVC',
            service_name='Test Service',
            mda=self.mda,
            config={'rules': {'schema': {'properties': {'field1': {'type': 'string'}}}}}
        )
        self.workflow_step1 = WorkflowStep.objects.create(
            service_config=self.service_config,
            step_name='Initial Review',
            role='officer',
            action='review',
            sequence=1
        )
        self.workflow_step2 = WorkflowStep.objects.create(
            service_config=self.service_config,
            step_name='Approval',
            role='supervisor',
            action='approve',
            sequence=2
        )
        self.service_request = ServiceRequest.objects.create(
            request_id='req-123',
            citizen=self.citizen_user,
            service_config=self.service_config,
            payload={'field1': 'value1'},
            current_step=self.workflow_step1
        )
        self.audit_log = AuditLog.objects.create(
            service_request=self.service_request,
            actor=self.citizen_user,
            action='REQUEST_CREATED',
            details='Service request created'
        )

    def test_user_creation(self):
        self.assertEqual(self.admin_user.username, 'admin')
        self.assertTrue(self.admin_user.is_staff)
        self.assertTrue(self.admin_user.is_superuser)
        self.assertEqual(self.citizen_user.role, 'citizen')
        self.assertEqual(self.officer_user.role, 'officer')
        self.assertEqual(self.supervisor_user.role, 'supervisor')

    def test_mda_creation(self):
        self.assertEqual(self.mda.name, 'Ministry of Test')
        self.assertEqual(self.mda.description, 'Test MDA')

    def test_service_config_creation(self):
        self.assertEqual(self.service_config.service_code, 'TEST_SVC')
        self.assertEqual(self.service_config.service_name, 'Test Service')
        self.assertEqual(self.service_config.mda, self.mda)
        self.assertIn('rules', self.service_config.config)

    def test_workflow_step_creation(self):
        self.assertEqual(self.workflow_step1.step_name, 'Initial Review')
        self.assertEqual(self.workflow_step1.role, 'officer')
        self.assertEqual(self.workflow_step1.sequence, 1)
        self.assertEqual(self.workflow_step1.service_config, self.service_config)

    def test_service_request_creation(self):
        self.assertEqual(self.service_request.request_id, 'req-123')
        self.assertEqual(self.service_request.citizen, self.citizen_user)
        self.assertEqual(self.service_request.service_config, self.service_config)
        self.assertEqual(self.service_request.payload, {'field1': 'value1'})
        self.assertEqual(self.service_request.status, 'received')
        self.assertEqual(self.service_request.current_step, self.workflow_step1)

    def test_audit_log_creation(self):
        self.assertEqual(self.audit_log.service_request, self.service_request)
        self.assertEqual(self.audit_log.actor, self.citizen_user)
        self.assertEqual(self.audit_log.action, 'REQUEST_CREATED')
        self.assertEqual(self.audit_log.details, 'Service request created')
