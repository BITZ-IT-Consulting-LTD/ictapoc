from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.JSONField(default=list) # List of permission strings e.g. ["case.view", "case.create"]

    def __str__(self):
        return self.name

class User(AbstractUser):
    ROLE_CHOICES = (
        ('citizen', 'Citizen'),
        ('officer', 'Officer'),
        ('supervisor', 'Supervisor'),
        ('registrar', 'Registrar'),
        ('mda_admin', 'MDA Admin'),
        ('admin', 'Admin'),
    )
    # Deprecated 'role' string in favor of 'user_role', but kept for legacy checks
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')
    user_role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    mda = models.ForeignKey('MDA', on_delete=models.SET_NULL, null=True, blank=True, related_name='staff')

    # Profile Fields
    id_number = models.CharField(max_length=20, blank=True, null=True)
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    saved_documents = models.JSONField(default=list, blank=True) # e.g. [{"name": "ID", "content": "..."}]

class MDA(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    head_of_mda = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class ServiceConfig(models.Model):
    service_code = models.CharField(max_length=50, unique=True)
    service_name = models.CharField(max_length=255)
    mda = models.ForeignKey(MDA, on_delete=models.CASCADE)
    config = models.JSONField() # Stores rules, sla, output, etc.
    
    def __str__(self):
        return self.service_name

class WorkflowStep(models.Model):
    STEP_TYPE_CHOICES = (
        ('manual', 'Manual'),
        ('api_call', 'API Call'),
    )
    service_config = models.ForeignKey(ServiceConfig, related_name='workflow_steps', on_delete=models.CASCADE)
    step_name = models.CharField(max_length=255)
    step_type = models.CharField(max_length=20, choices=STEP_TYPE_CHOICES, default='manual')
    role = models.CharField(max_length=50, blank=True, null=True) # Role responsible for this step
    target_mda = models.ForeignKey('MDA', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_steps')
    action = models.CharField(max_length=50, blank=True, null=True)
    api_config = models.JSONField(blank=True, null=True) # For API call steps
    sequence = models.IntegerField()

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return f"{self.service_config.service_name} - Step {self.sequence}: {self.step_name}"

class ServiceRequest(models.Model):
    STATUS_CHOICES = (
        ('received', 'Received'),
        ('validation_failed', 'Validation Failed'),
        ('in_progress', 'In Progress'),
        ('escalated', 'Escalated'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('closed', 'Closed'),
    )
    
    request_id = models.CharField(max_length=255, unique=True)
    citizen = models.ForeignKey(User, on_delete=models.PROTECT, related_name='service_requests')
    service_config = models.ForeignKey(ServiceConfig, on_delete=models.PROTECT)
    payload = models.JSONField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    current_step = models.ForeignKey(WorkflowStep, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    is_escalated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.request_id

class AuditLog(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='audit_logs')
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.service_request.request_id} - {self.action}"