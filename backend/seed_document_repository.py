import os
import django
import json
import uuid
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.document_repository.models import Artifact, ArtifactType, Document, DocumentVersion, Registry, Node, NodeType, Project, ProjectPhase
from service_api.models import MDA

User = get_user_model()

def create_artifact(title, type_code, phase_obj=None, status='final'):
    """
    Idempotent helper to create an artifact.
    Fixes the 'category' field name error previously encountered.
    """
    try:
        art_type = ArtifactType.objects.get(code=type_code)
    except ArtifactType.DoesNotExist:
        art_type = ArtifactType.objects.create(
            name=type_code.replace('_', ' ').title(),
            code=type_code
        )
        print(f"Created missing ArtifactType: {type_code}")

    artifact, created = Artifact.objects.get_or_create(
        title=title,
        artifact_type=art_type,
        phase=phase_obj,
        defaults={
            'status': status
        }
    )
    if not created and artifact.status != status:
        artifact.status = status
        artifact.save()
    
    return artifact

def seed_database():
    print("Seeding Artifacts and Documents...")
    
    # 1. Ensure a default User and MDA for ownership
    user = User.objects.filter(is_superuser=True).first() or User.objects.first()
    mda = MDA.objects.get_or_create(code='ICTA', defaults={'name': 'ICT Authority'})[0]
    
    # 2. Create Artifact Types
    types = [
        ("Inception Report", "inception_report"),
        ("Technical Specification", "tech_spec"),
        ("Project Plan", "project_plan"),
        ("Standard Operating Procedure", "sop"),
        ("Citizen Wallet Document", "CITIZEN_WALLET_DOC")
    ]
    for name, code in types:
        ArtifactType.objects.get_or_create(code=code, defaults={'name': name})
    
    # 3. Create a Dummy Project and Phase
    project, _ = Project.objects.get_or_create(
        name="Digital Infrastructure Rollout",
        defaults={
            'mda_owner': mda,
            'start_date': timezone.now().date()
        }
    )
    phase, _ = ProjectPhase.objects.get_or_create(
        project=project,
        name="Phase 1: Planning",
        defaults={'sequence': 1}
    )

    # 4. Create Artifacts
    # Fixed: Use 'artifact_type' instead of 'category'
    art1 = create_artifact("Project Inception Memo", "inception_report", phase, "final")
    art2 = create_artifact("Architecture Blueprint", "tech_spec", phase, "final")
    art3 = create_artifact("Citizen ID Copy", "CITIZEN_WALLET_DOC", None, "final")
    
    print(f"Ensured Artifacts: {art1.title}, {art2.title}, {art3.title}")

    # 5. Create Documents and Versions (Simulated)
    def create_doc_with_version(title, artifact_obj):
        doc, created = Document.objects.get_or_create(
            title=title,
            artifact=artifact_obj,
            defaults={
                'document_type': artifact_obj.artifact_type.name,
                'owner_mda': mda,
                'uploaded_by': user,
                'classification_level': 'internal'
            }
        )
        
        if created:
            # Create an initial version (empty file for seeding)
            DocumentVersion.objects.create(
                document=doc,
                version_number=1,
                file_size=0,
                mime_type="application/pdf",
                checksum="dummy_checksum_" + str(uuid.uuid4()),
                uploaded_by=user,
                change_summary="Initial seed version"
            )
            print(f"Created Document: {title} v1")
        return doc

    create_doc_with_version("Inception_Report_v1.pdf", art1)
    create_doc_with_version("System_Architecture_2024.pdf", art2)

    print("Seeding complete!")

if __name__ == "__main__":
    seed_database()
