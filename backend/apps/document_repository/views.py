from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import FileResponse
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Project, ProjectPhase, Artifact, Document, DocumentVersion, ArtifactType, Registry, NodeType, Node
from .serializers import (
    ArtifactSerializer, ArtifactDetailSerializer, 
    DocumentSerializer, DocumentVersionSerializer,
    ProjectPhaseSerializer, ArtifactTypeSerializer,
    RegistrySerializer, NodeTypeSerializer, NodeSerializer, NodeMinimalSerializer
)
from service_api.models import AuditLog
import uuid

class RegistryViewSet(viewsets.ModelViewSet):
    queryset = Registry.objects.all()
    serializer_class = RegistrySerializer
    permission_classes = [permissions.IsAuthenticated]

class NodeTypeViewSet(viewsets.ModelViewSet):
    queryset = NodeType.objects.all()
    serializer_class = NodeTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [permissions.IsAuthenticated]

class RepositoryViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='explore/(?P<path>.+)')
    def resolve_path(self, request, path=None):
        # Normalize: strip potential trailing slash and ensure leading slash
        path = path.rstrip('/')
        full_path = path if path.startswith('/') else '/' + path

        # 1. Check if the path is actually a Registry slug (Registry Root)
        # Registry slugs are usually the first part of the path (minus slashes)
        registry_slug = path.split('/')[0] if not path.startswith('/') else path.split('/')[1]
        
        registry = Registry.objects.filter(slug=registry_slug).first()
        
        # If the path equals the registry slug root, we're at the top level
        if full_path == f"/{registry_slug}" and registry:
            child_nodes = registry.nodes.filter(parent__isnull=True)
            return Response({
                "path": full_path,
                "node": {
                    "id": 0,
                    "name": registry.name,
                    "full_path": full_path,
                    "node_type_name": "Authoritative Registry",
                    "inherited_metadata": {}
                },
                "nodes": NodeMinimalSerializer(child_nodes, many=True).data,
                "artifacts": [],
                "documents": []
            })

        # 2. Otherwise, resolve via Node's full_path
        node = get_object_or_404(Node, full_path=full_path)
        child_nodes = node.children.all()
        
        # Filtering artifacts within this branch
        artifacts = node.artifacts.all()
        
        artifact_type = request.query_params.get('artifact_type')
        owner_mda = request.query_params.get('owner_mda')
        status_filter = request.query_params.get('status')
        search = request.query_params.get('search')
        
        if artifact_type:
            artifacts = artifacts.filter(artifact_type_id=artifact_type)
        if owner_mda:
            artifacts = artifacts.filter(mda_owner_id=owner_mda)
        if status_filter:
            artifacts = artifacts.filter(status=status_filter)
        if search:
            artifacts = artifacts.filter(title__icontains=search)
            
        return Response({
            "path": node.full_path,
            "node": NodeSerializer(node).data,
            "nodes": NodeMinimalSerializer(child_nodes, many=True).data,
            "artifacts": ArtifactSerializer(artifacts, many=True).data,
            "documents": []
        })

class ArtifactTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArtifactType.objects.all().order_by('name')
    serializer_class = ArtifactTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProjectPhaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectPhase.objects.all().order_by('sequence')
    serializer_class = ProjectPhaseSerializer
    permission_classes = [permissions.IsAuthenticated]

class ArtifactViewSet(viewsets.ModelViewSet):
    queryset = Artifact.objects.select_related('phase', 'mda_owner').all().order_by('-updated_at')
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArtifactDetailSerializer
        return ArtifactSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        
        # --- RBAC Enforcement ---
        # 1. System Admins and Admins see everything
        # 2. Supervisors see all artifacts within their MDA
        # 3. Regular users only see artifacts they created or those in their MDA that are 'validated' or 'final'
        if user.role not in ['system_admin', 'admin', 'GLOBAL_SUPERVISOR']:
            if hasattr(user, 'mda') and user.mda:
                if user.role in ['supervisor', 'mda_admin', 'MDA_SUPERVISOR']:
                    qs = qs.filter(mda_owner=user.mda)
                else:
                    # Officers/Others see their own OR final/validated documents in their MDA
                    qs = qs.filter(
                        Q(mda_owner=user.mda, status__in=['validated', 'final']) |
                        Q(mda_owner=user.mda, documents__uploaded_by=user)
                    ).distinct()
            else:
                # If no MDA, only see what they uploaded
                qs = qs.filter(documents__uploaded_by=user).distinct()

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
        status_filter = self.request.query_params.get('status')
        search = self.request.query_params.get('search')
        
        if phase_id:
            qs = qs.filter(phase_id=phase_id)
        if artifact_type_id:
            qs = qs.filter(artifact_type_id=artifact_type_id)
        if status_filter:
            qs = qs.filter(status=status_filter)
        if search:
            qs = qs.filter(Q(title__icontains=search))
            
        return qs

    @action(detail=True, methods=['patch'])
    def status(self, request, pk=None):
        artifact = self.get_object()
        new_status = request.data.get('status')
        if not new_status or new_status not in dict(Artifact.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Optional: Add RBAC checks (e.g. only supervisor+ can validate)
        # Using simple check here based on our frontend requirement:
        if request.user.role not in ['system_admin', 'supervisor', 'admin', 'mda_admin']:
             return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
             
        artifact.status = new_status
        artifact.save()
        return Response(self.get_serializer(artifact).data)

    def create(self, request, *args, **kwargs):
        # We need to manually handle mda_owner since it's read_only in serializer
        mda = request.user.mda if hasattr(request.user, 'mda') and request.user.mda else None
        
        # In this POC, if user has no MDA, try to just assign the default ICTA for seeding continuity
        if not mda:
             from service_api.models import MDA
             mda = MDA.objects.filter(code='ICTA').first()

        data = request.data.copy()
        
        # Manually create the object so we can bypass read-only fields missing validation
        title = data.get('title')
        artifact_type_id = data.get('artifact_type')
        phase_id = data.get('phase')
        node_id = data.get('node')
        status_val = data.get('status', 'draft')
        
        if not title:
             return Response({"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)
             
        phase = None
        if phase_id:
             phase = ProjectPhase.objects.filter(id=phase_id).first()
             
        artifact_type = None
        if artifact_type_id:
             artifact_type = ArtifactType.objects.filter(id=artifact_type_id).first()

        node = None
        if node_id:
             node = Node.objects.filter(id=node_id).first()
             
        artifact = Artifact.objects.create(
             title=title,
             artifact_type=artifact_type,
             phase=phase,
             node=node,
             mda_owner=mda,
             status=status_val
        )
        
        return Response(self.get_serializer(artifact).data, status=status.HTTP_201_CREATED)

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.select_related('uploaded_by', 'owner_mda', 'artifact').all().order_by('-created_at')
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_queryset(self):
        qs = super().get_queryset()
        artifact_id = self.request.query_params.get('artifact_id')
        if artifact_id:
            qs = qs.filter(artifact_id=artifact_id)
        return qs
        
    def create(self, request, *args, **kwargs):
        # Handle file upload & metadata
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
            
        title = request.data.get('title', file_obj.name)
        classification_level = request.data.get('classification_level', 'internal')
        document_type = request.data.get('document_type', 'report')
        artifact_id = request.data.get('artifact_id')
        
        artifact = get_object_or_404(Artifact, id=artifact_id) if artifact_id else None
        
        # Get logic for version increment vs new doc
        # Here we simplify to creating a new Document wrapper per upload, but in a full implementation
        # you might match by title to bump version. We'll simply create a Document + Version 1 here.
        
        import json
        metadata_str = request.data.get('metadata', '{}')
        try:
            metadata = json.loads(metadata_str)
        except (ValueError, TypeError):
            metadata = {}
            
        doc = Document.objects.create(
            title=title,
            document_type=document_type,
            classification_level=classification_level,
            uploaded_by=request.user,
            owner_mda=request.user.mda if hasattr(request.user, 'mda') and request.user.mda else (artifact.mda_owner if artifact else None),
            artifact=artifact,
            metadata=metadata,
            current_version_number=1
        )
        
        DocumentVersion.objects.create(
            document=doc,
            version_number=1,
            file=file_obj,
            file_size=file_obj.size,
            mime_type=file_obj.content_type,
            checksum="dummy_checksum_" + str(uuid.uuid4()),
            uploaded_by=request.user,
            change_summary="Initial upload"
        )

        # Audit Emission
        AuditLog.objects.create(
            actor=request.user,
            action="DOCUMENT_UPLOAD",
            actor_role=request.user.role,
            owning_mda_id=doc.owner_mda.id if doc.owner_mda else None,
            details=f"Uploaded document {doc.title} to artifact {artifact.title if artifact else 'N/A'}"
        )
        
        serializer = self.get_serializer(doc)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Note using lookup_field = 'uuid' is preferred, but viewset defaults to pk
    @action(detail=False, methods=['get'], url_path='(?P<uuid>[^/.]+)/download')
    def download(self, request, uuid=None):
        doc = get_object_or_404(Document, uuid=uuid)
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
             AuditLog.objects.create(
                actor=request.user,
                action="DOCUMENT_DOWNLOAD",
                actor_role=request.user.role,
                details=f"Downloaded document {doc.title}"
             )
             return response
        
    @action(detail=False, methods=['get'], url_path='(?P<uuid>[^/.]+)/preview')
    def preview(self, request, uuid=None):
        doc = get_object_or_404(Document, uuid=uuid)
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
