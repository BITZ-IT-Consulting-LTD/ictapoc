from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.indexes import GinIndex
from django.utils import timezone
import uuid

User = settings.AUTH_USER_MODEL
MDA = 'service_api.MDA'

class Registry(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    mda_owner = models.ForeignKey(MDA, on_delete=models.CASCADE, related_name='registries', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class NodeType(models.Model):
    name = models.CharField(max_length=100) # e.g. Project, Phase, County, Plot
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Node(models.Model):
    registry = models.ForeignKey(Registry, on_delete=models.CASCADE, related_name='nodes')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    node_type = models.ForeignKey(NodeType, on_delete=models.PROTECT)
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    full_path = models.CharField(max_length=1000, db_index=True, unique=True)
    
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_inherited_metadata(self):
        """Recursively merge metadata from parents."""
        data = {}
        if self.parent:
            data.update(self.parent.get_inherited_metadata())
        data.update(self.metadata)
        return data

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
            
        if self.parent:
            self.full_path = f"{self.parent.full_path}/{self.slug}"
        else:
            self.full_path = f"/{self.registry.slug}/{self.slug}"
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_path

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    mda_owner = models.ForeignKey(MDA, on_delete=models.CASCADE, related_name='projects')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ArtifactType(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    metadata_schema = models.JSONField(default=dict, blank=True, help_text="JSON schema definition for required metadata")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProjectPhase(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='phases')
    name = models.CharField(max_length=255)
    sequence = models.IntegerField(default=1)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return f"{self.project.name} - {self.name}"

class Artifact(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('reviewed', 'Reviewed'),
        ('validated', 'Validated'),
        ('final', 'Final Official'),
        ('archived', 'Archived')
    )
    title = models.CharField(max_length=255)
    artifact_type = models.ForeignKey(ArtifactType, on_delete=models.PROTECT, related_name='artifacts', null=True)
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='artifacts', null=True, blank=True)
    phase = models.ForeignKey(ProjectPhase, on_delete=models.SET_NULL, null=True, blank=True, related_name='artifacts')
    mda_owner = models.ForeignKey(MDA, on_delete=models.CASCADE, related_name='artifacts', null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    tags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Document(models.Model):
    CLASSIFICATION_CHOICES = (
        ('public', 'Public'),
        ('internal', 'Internal'),
        ('restricted', 'Restricted'),
        ('confidential', 'Confidential'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    document_type = models.CharField(max_length=100)
    classification_level = models.CharField(max_length=20, choices=CLASSIFICATION_CHOICES, default='internal')
    
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_documents')
    owner_mda = models.ForeignKey(MDA, on_delete=models.CASCADE, related_name='owned_documents', null=True, blank=True)
    
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.CharField(max_length=255, null=True, blank=True)
    linked_entity = GenericForeignKey('content_type', 'object_id')

    current_version_number = models.IntegerField(default=1)
    
    metadata = models.JSONField(default=dict, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['owner_mda', 'classification_level']),
            models.Index(fields=['content_type', 'object_id']),
            GinIndex(fields=['metadata'])
        ]

    def __str__(self):
        return self.title

def get_s3_path(instance, filename):
    mda_code = instance.document.owner_mda.code if instance.document.owner_mda else 'public'
    clss = instance.document.classification_level
    year = instance.created_at.strftime('%Y') if instance.created_at else timezone.now().strftime('%Y')
    return f"repository/{mda_code}/{clss}/{year}/{instance.document.uuid}/v{instance.version_number}_{filename}"

class DocumentVersion(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='versions')
    version_number = models.IntegerField()
    
    file = models.FileField(upload_to=get_s3_path, max_length=500)
    file_size = models.BigIntegerField(help_text="Size in bytes")
    mime_type = models.CharField(max_length=100)
    checksum = models.CharField(max_length=256, help_text="SHA-256 Hash of the file")
    
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    change_summary = models.TextField(blank=True, help_text="What changed in this version")

    class Meta:
        unique_together = ('document', 'version_number')

    def __str__(self):
        return f"{self.document.title} - v{self.version_number}"
