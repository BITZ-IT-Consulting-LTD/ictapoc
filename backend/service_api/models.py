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
        ('system_admin', 'System Admin'),
        ('admin', 'Admin'),
    )
    # Deprecated 'role' string in favor of 'user_role', but kept for legacy checks
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')
    user_role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    mda = models.ForeignKey('MDA', on_delete=models.SET_NULL, null=True, blank=True, related_name='staff') # Primary MDA
    assigned_mdas = models.ManyToManyField('MDA', blank=True, related_name='assigned_users') # Multi-MDA assignment

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

class ServiceDomain(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class ServiceCategory(models.Model):
    name = models.CharField(max_length=255)
    domain = models.ForeignKey(ServiceDomain, related_name='categories', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('name', 'domain')

    def __str__(self):
        return f"{self.domain.name} - {self.name}"

class ServiceConfig(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('deprecated', 'Deprecated'),
        ('draft', 'Draft'),
    )

    service_code = models.CharField(max_length=50, unique=True)
    service_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True) # New field
    mda = models.ForeignKey(MDA, on_delete=models.CASCADE)
    
    # Catalogue & Classification
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='services')
    service_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Digitization & Readiness
    digitization_level = models.IntegerField(default=1, help_text="1=Manual, 5=Fully Digital")
    is_public_facing = models.BooleanField(default=True)
    
    # New fields for Catalogue
    service_type = models.CharField(max_length=50, blank=True, null=True) # G2G, G2C, G2B, Internal
    delivery_channels = models.JSONField(default=list, blank=True)
    process_complexity = models.CharField(max_length=50, blank=True, null=True)
    pain_points = models.JSONField(default=list, blank=True)
    
    # Metadata
    legal_basis_summary = models.TextField(blank=True, null=True)
    processing_time_estimate = models.CharField(max_length=100, blank=True, null=True)
    fees_applicable = models.BooleanField(default=False)
    
    # Discovery
    catalogue_visible = models.BooleanField(default=True)
    catalogue_order = models.IntegerField(default=0)
    life_event_group = models.CharField(max_length=100, blank=True, null=True) # e.g. "Birth", "Business"
    catalogue_tags = models.JSONField(default=list, blank=True)
    
    # Analysis & Roadmap
    consolidation_candidate = models.BooleanField(default=False)
    blocking_issues = models.TextField(blank=True, null=True)
    quick_wins = models.TextField(blank=True, null=True)

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('critical', 'Critical'),
    )
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')

    # Technical
    shared_services = models.JSONField(default=list, blank=True) # List of shared enablers used
    associated_systems = models.JSONField(default=list, blank=True) # e.g. ["NIIMS", "IPPD"]
    associated_actors = models.JSONField(default=list, blank=True) # e.g. ["Citizens", "Immigration Officers"]
    dependencies = models.JSONField(default=list, blank=True)
    
    config = models.JSONField(default=dict) # Stores rules, sla, output, etc.
    form_schema = models.JSONField(default=dict, blank=True) # Dynamic form configuration for workflows
    
    def __str__(self):
        return self.service_name

class WorkflowStep(models.Model):
    STEP_TYPE_CHOICES = (
        ('manual', 'Manual'),
        ('api_call', 'API Call'),
    )
    BPMN_ELEMENT_CHOICES = (
        ('start_event', 'Start Event'),
        ('user_task', 'User Task'),
        ('service_task', 'Service Task'),
        ('exclusive_gateway', 'Exclusive Gateway'),
        ('end_event', 'End Event'),
    )
    LIFECYCLE_CHOICES = (
        ('as_is', 'As-Is (Current)'),
        ('to_be', 'To-Be (Optimized)'),
    )
    service_config = models.ForeignKey(ServiceConfig, related_name='workflow_steps', on_delete=models.CASCADE)
    step_name = models.CharField(max_length=255)
    step_type = models.CharField(max_length=20, choices=STEP_TYPE_CHOICES, default='manual')
    bpmn_element_type = models.CharField(max_length=30, choices=BPMN_ELEMENT_CHOICES, default='user_task')
    lifecycle_stage = models.CharField(max_length=10, choices=LIFECYCLE_CHOICES, default='as_is')
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
    priority = models.CharField(max_length=20, choices=(
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ), default='normal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.request_id

class AuditLog(models.Model):
    # Enforced RBAC Audit structure
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='audit_logs', null=True, blank=True)
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # Metadata for RBAC Enforcement
    actor_role = models.CharField(max_length=50, blank=True, null=True)
    actor_mdas = models.JSONField(default=list, blank=True)
    
    action = models.CharField(max_length=255) # e.g. "CLAIM_PROCESS"
    decision = models.CharField(max_length=10, choices=(('ALLOW', 'ALLOW'), ('DENY', 'DENY')), default='ALLOW')
    
    # Context
    process_id = models.CharField(max_length=100, blank=True, null=True)
    service_id = models.CharField(max_length=100, blank=True, null=True)
    owning_mda_id = models.IntegerField(null=True, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.timestamp} - {self.actor} - {self.action} - {self.decision}"

class GovernmentFile(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('pending', 'Pending'),
        ('escalated', 'Escalated'),
        ('closed', 'Closed'),
        ('archived', 'Archived'),
    )
    file_number = models.CharField(max_length=100, unique=True) # Official Registry Ref
    subject = models.CharField(max_length=255)
    owning_mda = models.ForeignKey(MDA, on_delete=models.CASCADE, related_name='registry_files')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.file_number}: {self.subject}"

class InterDepartmentalMemo(models.Model):
    MEMO_TYPES = (
        ('policy', 'Policy Memo'),
        ('operational', 'Operational Request'),
        ('instruction', 'Instruction'),
        ('concurrence', 'Concurrence'),
        ('escalation', 'Escalation'),
        ('information', 'Information'),
    )
    STATUS_CHOICES = (
        ('draft', 'Draft (Initiated)'), 
        ('reviewing', 'In Internal Review'),
        ('approved', 'Internally Approved'),
        ('registered', 'Registry Registered'),
        ('signed', 'Digitally Signed'),
        ('actioning', 'Issued & In Action'),
        ('responded', 'Responded'),
        ('closed', 'Closed'),
    )
    PRIORITY_CHOICES = (
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )

    gov_file = models.ForeignKey(GovernmentFile, on_delete=models.CASCADE, related_name='memos', null=True, blank=True)
    official_ref = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sent_memos')
    sender_mda = models.ForeignKey(MDA, on_delete=models.CASCADE, related_name='outbound_memos')
    recipient_mda = models.ForeignKey(MDA, on_delete=models.CASCADE, related_name='inbound_memos')
    
    memo_type = models.CharField(max_length=30, choices=MEMO_TYPES, default='operational')
    subject = models.CharField(max_length=255)
    content = models.TextField()
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='draft')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    
    is_read = models.BooleanField(default=False)
    digitally_signed = models.BooleanField(default=False)
    signed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='signed_memos', blank=True)
    
    parent_memo = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='responses')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.official_ref or 'DRAFT'}: {self.subject}"

class OfficialLetter(models.Model):
    gov_file = models.ForeignKey(GovernmentFile, on_delete=models.CASCADE, related_name='letters')
    official_ref = models.CharField(max_length=100, unique=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient_name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    signed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CorrespondenceAction(models.Model):
    memo = models.ForeignKey(InterDepartmentalMemo, on_delete=models.CASCADE, related_name='actions')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    instruction = models.TextField()
    deadline = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    progress_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class DesktopReview(models.Model):
    mda = models.ForeignKey(MDA, on_delete=models.CASCADE, related_name='desktop_reviews')
    process_id = models.CharField(max_length=100, blank=True, null=True)
    executive_summary = models.TextField(blank=True, null=True)
    process_overview = models.JSONField(default=dict, blank=True)
    stakeholders = models.JSONField(default=list, blank=True)
    inputs_outputs_dependencies = models.JSONField(default=dict, blank=True)
    process_maturity = models.JSONField(default=dict, blank=True)
    as_is_narrative = models.TextField(blank=True, null=True)
    as_is_steps = models.JSONField(default=list, blank=True)
    pain_points_bottlenecks_risks = models.JSONField(default=list, blank=True)
    to_be_process = models.JSONField(default=dict, blank=True)
    digitization_opportunities = models.JSONField(default=list, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Desktop Review: {self.mda.name}"

class RegistryAdapter(models.Model):
    """
    GEA-Compliant Registry Adapter configuration.
    Allows decoupling of registry logic from hardcoded mocks to DB-driven API integrations.
    """
    code = models.CharField(max_length=50, unique=True, help_text="Unique code (e.g., IPRS, KRA, CRS)")
    name = models.CharField(max_length=255)
    base_url = models.URLField(blank=True, null=True, help_text="Authoritative API Base URL")
    auth_config = models.JSONField(default=dict, blank=True, help_text="Headers, API Keys, or Certificates")
    data_mapping = models.JSONField(default=dict, blank=True, help_text="Field mapping from Registry -> Platform")
    
    is_mock = models.BooleanField(default=True)
    mock_data = models.JSONField(default=dict, blank=True, help_text="JSON dump of original authoritative dictionaries")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class PaymentProvider(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True) # e.g. MPESA, VISA, KCB
    config = models.JSONField(default=dict, blank=True) # API keys, Paybill numbers, etc.
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class PaymentTransaction(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    provider = models.ForeignKey(PaymentProvider, on_delete=models.PROTECT)
    provider_ref = models.CharField(max_length=100, unique=True, null=True, blank=True) # e.g. M-Pesa Code
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"TXN-{self.id}: {self.amount} {self.currency} ({self.status})"

class RevenueSplit(models.Model):
    transaction = models.ForeignKey(PaymentTransaction, on_delete=models.CASCADE, related_name='splits')
    beneficiary_mda = models.ForeignKey(MDA, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    account_number = models.CharField(max_length=100, blank=True, null=True) # Destination Account

    def __str__(self):
        return f"Split: {self.beneficiary_mda.name} - {self.amount}"

class DataPurpose(models.Model):
    """Legal grounds for data processing."""
    code = models.CharField(max_length=50, unique=True) # e.g. SERVICE_DELIVERY, LAW_ENFORCEMENT
    description = models.TextField()

    def __str__(self):
        return self.code

class ConsentRecord(models.Model):
    """
    Tracks explicit citizen consent for data sharing according to the Data Protection Act.
    """
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('REVOKED', 'Revoked'),
        ('EXPIRED', 'Expired'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consents')
    requester = models.ForeignKey(MDA, on_delete=models.CASCADE, related_name='requested_consents')
    data_scope = models.CharField(max_length=255) # e.g. "identity.read", "tax_compliance.verify"
    purpose = models.ForeignKey(DataPurpose, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    
    granted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Consent: {self.user.username} -> {self.requester.name} ({self.data_scope})"

class ConsentAccessLog(models.Model):
    """
    Immutable audit log for every time data is accessed under a consent record.
    """
    consent = models.ForeignKey(ConsentRecord, on_delete=models.CASCADE, related_name='access_logs')
    accessed_at = models.DateTimeField(auto_now_add=True)
    accessed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    resource_id = models.CharField(max_length=100, blank=True, null=True) # e.g. Request ID

    def __str__(self):
        return f"Access: {self.consent.id} at {self.accessed_at}"