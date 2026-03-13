from rest_framework import serializers
from .models import Project, ProjectPhase, Artifact, Document, DocumentVersion, ArtifactType, Registry, NodeType, Node
from service_api.models import MDA, User

class MdaMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MDA
        fields = ['id', 'name', 'code']

class PhaseMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPhase
        fields = ['id', 'name', 'sequence']

class RegistrySerializer(serializers.ModelSerializer):
    mda_owner = MdaMinimalSerializer(read_only=True)
    class Meta:
        model = Registry
        fields = '__all__'

class NodeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeType
        fields = '__all__'

class NodeSerializer(serializers.ModelSerializer):
    node_type_name = serializers.CharField(source='node_type.name', read_only=True)
    inherited_metadata = serializers.SerializerMethodField()
    class Meta:
        model = Node
        fields = '__all__'
        read_only_fields = ['slug', 'full_path']

    def get_inherited_metadata(self, obj):
        return obj.get_inherited_metadata()

class NodeMinimalSerializer(serializers.ModelSerializer):
    node_type_name = serializers.CharField(source='node_type.name', read_only=True)
    class Meta:
        model = Node
        fields = ['id', 'name', 'slug', 'full_path', 'node_type_name']

class ArtifactTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtifactType
        fields = '__all__'

class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class DocumentVersionSerializer(serializers.ModelSerializer):
    uploaded_by = UserMinimalSerializer(read_only=True)
    class Meta:
        model = DocumentVersion
        fields = ['id', 'version_number', 'file_size', 'mime_type', 'checksum', 'uploaded_by', 'created_at', 'change_summary']

class DocumentSerializer(serializers.ModelSerializer):
    owner_mda = MdaMinimalSerializer(read_only=True)
    uploaded_by = UserMinimalSerializer(read_only=True)
    versions = DocumentVersionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Document
        fields = [
            'uuid', 'title', 'document_type', 'classification_level',
            'uploaded_by', 'owner_mda', 'current_version_number', 
            'metadata', 'created_at', 'versions'
        ]

class ArtifactSerializer(serializers.ModelSerializer):
    mda_owner = MdaMinimalSerializer(read_only=True)
    phase = PhaseMinimalSerializer(read_only=True)
    phase_id = serializers.PrimaryKeyRelatedField(
        queryset=ProjectPhase.objects.all(), source='phase', write_only=True, required=False, allow_null=True
    )
    artifact_type = ArtifactTypeSerializer(read_only=True)
    artifact_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ArtifactType.objects.all(), source='artifact_type', write_only=True, required=False, allow_null=True
    )
    node = NodeMinimalSerializer(read_only=True)
    node_id = serializers.PrimaryKeyRelatedField(
        queryset=Node.objects.all(), source='node', write_only=True, required=False, allow_null=True
    )
    latest_version = serializers.SerializerMethodField()
    
    inherited_metadata = serializers.SerializerMethodField()
    
    class Meta:
        model = Artifact
        fields = [
            'id', 'title', 'artifact_type', 'artifact_type_id', 'node', 'node_id', 
            'phase', 'phase_id', 'mda_owner', 'status', 'tags', 'metadata', 
            'is_public', 'submission_deadline', 'created_at', 'updated_at', 
            'latest_version', 'inherited_metadata'
        ]
        
    def get_latest_version(self, obj):
        doc = obj.documents.last()
        if doc:
            return doc.current_version_number
        return None

    def get_inherited_metadata(self, obj):
        if obj.node:
            return obj.node.get_inherited_metadata()
        return {}

class ArtifactDetailSerializer(ArtifactSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta(ArtifactSerializer.Meta):
        fields = ArtifactSerializer.Meta.fields + ['documents']

class ProjectSerializer(serializers.ModelSerializer):
    mda_owner = MdaMinimalSerializer(read_only=True)
    class Meta:
        model = Project
        fields = '__all__'

class ProjectPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPhase
        fields = '__all__'
