from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from service_api.models import MDA, ServiceConfig, WorkflowStep, ServiceRequest, AuditLog
import json

User = get_user_model()

class APIViewTestCase(APITestCase):
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

        # Get JWT tokens
        self.admin_token = self.get_token(self.admin_user.username, 'password')
        self.citizen_token = self.get_token(self.citizen_user.username, 'password')
        self.officer_token = self.get_token(self.officer_user.username, 'password')
        self.supervisor_token = self.get_token(self.supervisor_user.username, 'password')

    def get_token(self, username, password):
        response = self.client.post(reverse('token_obtain_pair'), {'username': username, 'password': password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def authenticate_client(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_mda_list_admin_access(self):
        self.authenticate_client(self.admin_token)
        response = self.client.get(reverse('mda-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_mda_list_non_admin_denied(self):
        self.authenticate_client(self.citizen_token)
        response = self.client.get(reverse('mda-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_service_config_list_admin_access(self):
        self.authenticate_client(self.admin_token)
        response = self.client.get(reverse('serviceconfig-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_service_config_list_citizen_access(self):
        self.authenticate_client(self.citizen_token)
        response = self.client.get(reverse('serviceconfig-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) # IsAdminOrReadOnly allows read for all authenticated

    def test_service_request_create_citizen(self):
        self.authenticate_client(self.citizen_token)
        data = {
            'service_code': self.service_config.service_code,
            'payload': {'field1': 'new_value'}
        }
        response = self.client.post(reverse('servicerequest-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ServiceRequest.objects.count(), 2)
        new_request = ServiceRequest.objects.get(id=response.data['id'])
        self.assertEqual(new_request.citizen, self.citizen_user)
        self.assertEqual(new_request.status, 'in_progress') # Should move to first step

    def test_service_request_list_citizen_only_own(self):
        self.authenticate_client(self.citizen_token)
        response = self.client.get(reverse('servicerequest-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) # Only own request

    def test_service_request_list_officer_assigned(self):
        self.authenticate_client(self.officer_token)
        response = self.client.get(reverse('servicerequest-list') + '?assigned_to_me=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) # Request is assigned to officer role

    def test_service_request_complete_step_officer(self):
        self.authenticate_client(self.officer_token)
        data = {'action': 'validated', 'details': 'All good'}
        response = self.client.post(reverse('servicerequest-complete-step', args=[self.service_request.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.service_request.refresh_from_db()
        self.assertEqual(self.service_request.current_step, self.workflow_step2) # Moved to next step
        self.assertEqual(AuditLog.objects.count(), 2) # Original + step completion
