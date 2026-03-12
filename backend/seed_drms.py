import os
import django
import uuid
import random
from datetime import timedelta
from django.utils import timezone
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, User
from apps.document_repository.models import (
    Project, ArtifactType, Artifact, Document, DocumentVersion,
    Registry, NodeType, Node
)

def get_or_create_mdas():
    icta, _ = MDA.objects.get_or_create(code="ICTA", defaults={"name": "ICT Authority", "is_priority": True})
    lands, _ = MDA.objects.get_or_create(code="MOLP", defaults={"name": "Ministry of Lands and Physical Planning", "is_priority": True})
    return icta, lands

def get_system_admin():
    admin = User.objects.filter(role='system_admin').first()
    if not admin:
         admin = User.objects.first()
    return admin

def seed_database():
    print("🚀 Starting DRMS Authoritative Registry & Hierarchy Seed...")
    
    icta, lands = get_or_create_mdas()
    admin_user = get_system_admin()
    now = timezone.now()

    # 1. Artifact Types Definition (System Classifications)
    artifact_types_def = [
        {
            "name": "Project Documentation",
            "code": "PROJECT_DOC",
            "description": "Used to manage project deliverables such as reports, frameworks, roadmaps.",
            "metadata_schema": {
                "type": "object",
                "properties": {
                    "project_name": {"type": "string"},
                    "phase": {"type": "string"},
                    "category": {"type": "string"},
                    "version": {"type": "string"},
                    "approval_status": {"type": "string", "enum": ["Draft", "Reviewed", "Approved"]},
                },
                "required": ["project_name", "category", "approval_status"]
            }
        },
        {
            "name": "Building Plans",
            "code": "BUILDING_PLAN",
            "description": "Used by planning departments to store architectural drawings and approvals.",
            "metadata_schema": {
                "type": "object",
                "properties": {
                    "building_owner": {"type": "string"},
                    "plot_number": {"type": "string"},
                    "county": {"type": "string"},
                    "architect_name": {"type": "string"},
                    "approval_status": {"type": "string"},
                    "submission_date": {"type": "string", "format": "date"}
                },
                "required": ["plot_number", "building_owner"]
            }
        },
        {
            "name": "Land Registry Records",
            "code": "LAND_RECORD",
            "description": "Used to store land ownership documentation.",
            "metadata_schema": {
                "type": "object",
                "properties": {
                    "parcel_number": {"type": "string"},
                    "owner_name": {"type": "string"},
                    "registry_office": {"type": "string"},
                    "survey_reference": {"type": "string"},
                    "registration_date": {"type": "string", "format": "date"}
                }
            }
        }
    ]

    types = {}
    for t_def in artifact_types_def:
        obj, _ = ArtifactType.objects.get_or_create(
            code=t_def["code"],
            defaults={
                "name": t_def["name"],
                "description": t_def["description"],
                "metadata_schema": t_def["metadata_schema"]
            }
        )
        types[t_def["code"]] = obj
        print(f"✅ Verified Artifact Type: {obj.name}")

    # 2. Registries & Node Types
    print("\n📂 Seeding Hierarchical Structures...")
    
    # Node Types
    nt_project, _ = NodeType.objects.get_or_create(code='PROJECT', defaults={'name': 'Project'})
    nt_phase, _ = NodeType.objects.get_or_create(code='PHASE', defaults={'name': 'Phase'})
    nt_county, _ = NodeType.objects.get_or_create(code='COUNTY', defaults={'name': 'County'})
    nt_plot, _ = NodeType.objects.get_or_create(code='PLOT', defaults={'name': 'Plot'})
    nt_parcel, _ = NodeType.objects.get_or_create(code='PARCEL', defaults={'name': 'Parcel'})

    # Registries
    project_reg, _ = Registry.objects.get_or_create(
        slug='project-registry',
        defaults={'name': 'National Project Repository', 'mda_owner': icta}
    )
    building_reg, _ = Registry.objects.get_or_create(
        slug='building-registry',
        defaults={'name': 'Building Approvals Registry', 'mda_owner': lands}
    )
    land_reg, _ = Registry.objects.get_or_create(
        slug='land-registry',
        defaults={'name': 'National Land Registry', 'mda_owner': lands}
    )

    # 3. Build Nodes with Paths
    # Project Branch
    icta_assessment, _ = Node.objects.get_or_create(
        registry=project_reg,
        slug='icta-assessment',
        defaults={'name': 'ICTA Assessment Study', 'node_type': nt_project}
    )
    
    phase1, _ = Node.objects.get_or_create(
        registry=project_reg,
        parent=icta_assessment,
        slug='phase-1',
        defaults={
            'name': 'Phase 1: Inception', 
            'node_type': nt_phase,
            'metadata': {'lifecycle': 'Inception', 'priority': 'High'}
        }
    )
    
    # Building Branch
    nairobi_county, _ = Node.objects.get_or_create(
        registry=building_reg,
        slug='nairobi',
        defaults={'name': 'Nairobi City County', 'node_type': nt_county}
    )
    
    plot_10234, _ = Node.objects.get_or_create(
        registry=building_reg,
        parent=nairobi_county,
        slug='plot-10234',
        defaults={'name': 'Plot 10234 - Upper Hill', 'node_type': nt_plot}
    )

    # Land Branch
    kilifi_county, _ = Node.objects.get_or_create(
        registry=land_reg,
        slug='kilifi',
        defaults={'name': 'Kilifi County', 'node_type': nt_county}
    )
    
    parcel_A1, _ = Node.objects.get_or_create(
        registry=land_reg,
        parent=kilifi_county,
        slug='parcel-A1',
        defaults={'name': 'Parcel A1 - Mariakani', 'node_type': nt_parcel}
    )

    print("✅ Verified Repository Traversal Nodes")

    # 4. Artifact & Document Helper with Node linkage
    def create_artifact_with_docs(artifact_type_code, title, node, mda, status, doc_specs, artifact_meta=None):
        art_type = types[artifact_type_code]
        artifact, _ = Artifact.objects.get_or_create(
            title=title,
            node=node,
            artifact_type=art_type,
            mda_owner=mda,
            defaults={
                "status": status,
                "metadata": artifact_meta or {}
            }
        )
        
        for d in doc_specs:
            doc, _ = Document.objects.get_or_create(
                title=d["title"],
                artifact=artifact,
                defaults={
                    "document_type": d["type"],
                    "classification_level": d.get("classification", "internal"),
                    "uploaded_by": admin_user,
                    "owner_mda": mda,
                    "metadata": d.get("metadata", {}),
                    "current_version_number": 1
                }
            )
            
            DocumentVersion.objects.get_or_create(
                document=doc,
                version_number=1,
                defaults={
                    "file": f"repository/{mda.code}/{doc.classification_level}/{now.year}/{doc.uuid}/v1_{d['filename']}",
                    "file_size": random.randint(500000, 15000000),
                    "mime_type": "application/pdf" if d["filename"].endswith(".pdf") else "application/octet-stream",
                    "checksum": "dummy_chk_" + str(uuid.uuid4())[:8],
                    "uploaded_by": admin_user,
                    "change_summary": "Initial Seeding"
                }
            )
        return artifact

    print("\n📜 Seeding Authoritative Records...")

    # Data Point 1: Project Docs under Phase 1 Node
    create_artifact_with_docs(
        "PROJECT_DOC", "Inception Report - ICTA POC", phase1, icta, "final",
        doc_specs=[
            {"title": "Inception Strategy v1.1", "filename": "inception_strategy.pdf", "type": "report", "classification": "public", "metadata": {
                "project_name": "ICTA Assessment", "phase": "Inception", "category": "Strategy", "version": "1.1", "approval_status": "Approved"
            }}
        ]
    )

    # Data Point 2: Building Plans under Plot Node
    create_artifact_with_docs(
        "BUILDING_PLAN", "Structural Approvals - Plot 10234", plot_10234, lands, "reviewed",
        doc_specs=[
            {"title": "Upper Hill Tower A Plans", "filename": "tower_a_blueprint.pdf", "type": "drawing", "metadata": {
                "building_owner": "Joseph Kimani", "plot_number": "10234", "county": "Nairobi", "architect_name": "Afritech Designs", "approval_status": "Pending"
            }}
        ]
    )

    # Data Point 3: Land Records under Parcel Node
    create_artifact_with_docs(
        "LAND_RECORD", "Title Deed - Mariakani Parcel A1", parcel_A1, lands, "final",
        doc_specs=[
            {"title": "Title Deed Scan", "filename": "deed_mariakani_01.pdf", "type": "deed", "classification": "restricted", "metadata": {
                "parcel_number": "A1/MARIAKANI", "owner_name": "Coast Development Authority", "registry_office": "Kilifi Central"
            }}
        ]
    )

    print("\n✨ DRMS Authoritative Registry Seed Complete!")
    print(f"Total Registries: {Registry.objects.count()}")
    print(f"Total Nodes: {Node.objects.count()}")
    print(f"Total Artifacts: {Artifact.objects.count()}")

if __name__ == "__main__":
    seed_database()
