from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import FileResponse

from .models import ProjectPhase, Artifact, Document, ArtifactType, Registry, NodeType, Node
from .serializers import (
    ArtifactSerializer, ArtifactDetailSerializer, 
    DocumentSerializer, ProjectPhaseSerializer, ArtifactTypeSerializer,
    RegistrySerializer, NodeTypeSerializer, NodeSerializer
)
from service_api.models import AuditLog

class PublicRegistryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Registry.objects.all()
    serializer_class = RegistrySerializer
    permission_classes = [permissions.AllowAny]

class PublicNodeTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NodeType.objects.all()
    serializer_class = NodeTypeSerializer
    permission_classes = [permissions.AllowAny]

class PublicNodeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [permissions.AllowAny]

class PublicArtifactTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArtifactType.objects.all().order_by('name')
    serializer_class = ArtifactTypeSerializer
    permission_classes = [permissions.AllowAny]

class PublicProjectPhaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectPhase.objects.all().order_by('sequence')
    serializer_class = ProjectPhaseSerializer
    permission_classes = [permissions.AllowAny]

class PublicArtifactViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Artifact.objects.select_related('phase', 'mda_owner').filter(status__in=['validated', 'final'], is_public=True).order_by('-updated_at')
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArtifactDetailSerializer
        return ArtifactSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()

        # Hierarchy Filtering
        registry_id = self.request.query_params.get('registry')
        node_id = self.request.query_params.get('node')

        if registry_id:
            qs = qs.filter(node__registry_id=registry_id)
        if node_id:
            qs = qs.filter(node_id=node_id)

        # Legacy & Common Filtering
        phase_id = self.request.query_params.get('phase')
        artifact_type_id = self.request.query_params.get('artifact_type')
        search = self.request.query_params.get('search')
        
        if phase_id:
            qs = qs.filter(phase_id=phase_id)
        if artifact_type_id:
            qs = qs.filter(artifact_type_id=artifact_type_id)
        if search:
            qs = qs.filter(Q(title__icontains=search))
            
        return qs

class PublicDocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Document.objects.select_related('uploaded_by', 'owner_mda', 'artifact').filter(artifact__status__in=['validated', 'final'], artifact__is_public=True).order_by('-created_at')
    serializer_class = DocumentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        artifact_id = self.request.query_params.get('artifact_id')
        if artifact_id:
            qs = qs.filter(artifact_id=artifact_id)
        return qs

    @action(detail=False, methods=['get'], url_path='(?P<uuid>[^/.]+)/download')
    def download(self, request, uuid=None):
        doc = get_object_or_404(Document, uuid=uuid, artifact__status__in=['validated', 'final'], artifact__is_public=True)
        version = doc.versions.order_by('-version_number').first()
        if not version or not version.file:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
            
        try:
             response = FileResponse(version.file.open(), content_type=version.mime_type)
             response['Content-Disposition'] = f'attachment; filename="{version.file.name.split("/")[-1]}"'
             return response
        except Exception:
             # POC Fallback for Seed Scripts which write string definitions instead of real files
             import io
             dummy = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\ntrailer\n<< /Size 4 /Root 1 0 R >>\n%%EOF" if 'pdf' in version.mime_type else b"POC Dummy Stream"
             response = FileResponse(io.BytesIO(dummy), content_type=version.mime_type)
             response['Content-Disposition'] = f'attachment; filename="dummy_{uuid}.pdf"'
             
             # Audit Emission on success (fallback)
             actor = request.user if request.user.is_authenticated else None
             AuditLog.objects.create(
                actor=actor,
                action="PUBLIC_DOCUMENT_DOWNLOAD",
                actor_role=actor.role if actor else 'public',
                details=f"Publicly downloaded document {doc.title}"
             )
             return response
        
    @action(detail=False, methods=['get'], url_path='(?P<uuid>[^/.]+)/preview')
    def preview(self, request, uuid=None):
        doc = get_object_or_404(Document, uuid=uuid, artifact__status__in=['validated', 'final'], artifact__is_public=True)
        version = doc.versions.order_by('-version_number').first()
        if not version or not version.file:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
            
        try:
             response = FileResponse(version.file.open(), content_type=version.mime_type)
             response['Content-Disposition'] = 'inline'
             return response
        except Exception:
             import io
             dummy = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\ntrailer\n<< /Size 4 /Root 1 0 R >>\n%%EOF" if 'pdf' in version.mime_type else b"POC Dummy Stream"
             response = FileResponse(io.BytesIO(dummy), content_type=version.mime_type)
             response['Content-Disposition'] = 'inline'
             return response
