from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import FileResponse, HttpResponse
from django.conf import settings

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
        return self._serve_versioned_file(request, uuid, attachment=True)
        
    @action(detail=False, methods=['get'], url_path='(?P<uuid>[^/.]+)/preview')
    def preview(self, request, uuid=None):
        return self._serve_versioned_file(request, uuid, attachment=False)

    def _serve_versioned_file(self, request, uuid, attachment=False):
        doc = get_object_or_404(Document, uuid=uuid, artifact__status__in=['validated', 'final'], artifact__is_public=True)
        version = doc.versions.order_by('-version_number').first()
        if not version or not version.file:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

        # Audit Emission
        actor = request.user if request.user.is_authenticated else None
        AuditLog.objects.create(
            actor=actor,
            action="PUBLIC_DOCUMENT_ACCESS",
            actor_role=actor.role if actor else 'public',
            details=f"Publicly {'downloaded' if attachment else 'previewed'} document {doc.title}"
        )

        # 1. High Performance Mode: X-Accel-Redirect
        # Only use if file actually exists on disk, otherwise fall through to dummy stream
        if settings.USE_X_ACCEL_REDIRECT and version.file and version.file.storage.exists(version.file.name):
            response = HttpResponse()
            response['X-Accel-Redirect'] = f"{settings.INTERNAL_MEDIA_PATH}{version.file.name}"
            response['Content-Type'] = version.mime_type
            if attachment:
                filename = version.file.name.split("/")[-1]
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
            else:
                response['Content-Disposition'] = 'inline'
            return response

        # 2. Standard Mode: FileResponse
        try:
             if not version.file or not version.file.storage.exists(version.file.name):
                 raise FileNotFoundError("Physical file missing")
                 
             response = FileResponse(version.file.open(), content_type=version.mime_type)
             if attachment:
                filename = version.file.name.split("/")[-1]
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
             else:
                response['Content-Disposition'] = 'inline'
             return response
        except Exception:
             import io
             is_pdf = 'pdf' in (version.mime_type or '').lower()
             # Standard compliant minimal PDF that actually renders a message
             is_pdf = 'pdf' in (version.mime_type or '').lower()
             dummy_pdf = (
                b"%PDF-1.4\n"
                b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
                b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
                b"3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>\nendobj\n"
                b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
                b"5 0 obj\n<< /Length 44 >>\nstream\nBT /F1 12 Tf 100 700 Td (POC Placeholder Document) Tj ET\nendstream\nendobj\n"
                b"trailer\n<< /Size 6 /Root 1 0 R >>\n"
                b"%%EOF"
             )
             dummy = dummy_pdf if is_pdf else b"POC Dummy Stream Content"
             content_type = "application/pdf" if is_pdf else version.mime_type
             response = FileResponse(io.BytesIO(dummy), content_type=content_type)
             response['Content-Disposition'] = f'attachment; filename="dummy_{uuid}.pdf"' if attachment else 'inline'
             return response
