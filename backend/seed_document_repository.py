import os
import django
import uuid
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, User
from apps.document_repository.models import Project, ProjectPhase, Artifact, ArtifactType, Document, DocumentVersion

def get_or_create_icta():
    icta, created = MDA.objects.get_or_create(
        code="ICTA",
        defaults={
            "name": "ICT Authority",
            "description": "ICT Authority of Kenya",
            "is_priority": True
        }
    )
    return icta

def get_system_admin():
    admin = User.objects.filter(role='system_admin').first()
    if not admin:
         admin = User.objects.first()
    return admin

def seed_database():
    print("Starting Document Repository Seed...")
    
    icta = get_or_create_icta()
    admin_user = get_system_admin()
    
    # 1. Create Project
    now = timezone.now()
    project, created = Project.objects.get_or_create(
        name="ICTA \u2013 Assessment Study for E-Service Delivery, Manual Records, and Governance Requirements",
        defaults={
            "description": "A national assessment of government MDAs to evaluate manual records, digital service maturity, infrastructure readiness, and governance frameworks to support digitization and automation.",
            "mda_owner": icta,
            "start_date": (now - timedelta(days=180)).date(), # Started 6 months ago
            "status": "active"
        }
    )
    print(f"Created Project: {project.name}")

    # 2. Project Phases
    phases_data = [
        {"name": "Phase 1 - Mobilisation & Inception", "sequence": 1, "duration_weeks": 2},
        {"name": "Phase 2 - Inventory & Assessment", "sequence": 2, "duration_weeks": 5},
        {"name": "Phase 3 - Process Mapping & Prioritisation", "sequence": 3, "duration_weeks": 4},
        {"name": "Phase 4 - Frameworks & Governance", "sequence": 4, "duration_weeks": 3},
        {"name": "Phase 5 - Roadmaps & RFPs", "sequence": 5, "duration_weeks": 2},
        {"name": "Phase 6 - Validation & Finalisation", "sequence": 6, "duration_weeks": 2},
    ]

    phase_objects = {}
    for pd in phases_data:
        phase, _ = ProjectPhase.objects.get_or_create(
            project=project,
            sequence=pd["sequence"],
            defaults={"name": pd["name"], "description": f"Duration: {pd['duration_weeks']} weeks"}
        )
        phase_objects[pd["sequence"]] = phase
        print(f"  Created Phase: {phase.name}")

    # Helper for Artifact creation
    def create_artifact(title, category, phase_seq, status="validated"):
        artifact_type, _ = ArtifactType.objects.get_or_create(
            code=category,
            defaults={"name": category.replace("_", " ").title()}
        )
        artifact, created = Artifact.objects.get_or_create(
            title=title,
            phase=phase_objects[phase_seq],
            mda_owner=icta,
            defaults={
                "artifact_type": artifact_type,
                "status": status,
            }
        )
        # Randomize creation date slightly for variety
        artifact.created_at = now - timedelta(days=random.randint(10, 150))
        artifact.save()
        return artifact

    # Helper for Document & Version creation
    def create_document_with_versions(artifact, title, doc_type, class_level, file_names, versions=1):
        doc, _ = Document.objects.get_or_create(
            title=title,
            artifact=artifact,
            defaults={
                "document_type": doc_type,
                "classification_level": class_level,
                "uploaded_by": admin_user,
                "owner_mda": icta,
                "current_version_number": versions
            }
        )
        
        for v in range(1, versions + 1):
            file_name = file_names[v-1] if v-1 < len(file_names) else f"{title.replace(' ', '_').lower()}_v{v}.pdf"
            
            DocumentVersion.objects.get_or_create(
                document=doc,
                version_number=v,
                defaults={
                    "file": f"repository/ICTA/{class_level}/{now.year}/{doc.uuid}/v{v}_{file_name}",
                    "file_size": random.randint(102400, 5242880), # 100KB to 5MB
                    "mime_type": "application/pdf" if file_name.endswith('.pdf') else "application/octet-stream",
                    "checksum": "dummy_hash_" + str(uuid.uuid4()),
                    "uploaded_by": admin_user,
                    "change_summary": f"Version {v} uploaded."
                }
            )
        return doc

    print("\nSeeding Artifacts and Documents...")

    # Phase 1
    art1_1 = create_artifact("Inception Report", "inception_report", 1, "final")
    create_document_with_versions(art1_1, "Final Inception Report", "report", "public", ["inception_report_v1.docx", "inception_report_reviewed.docx", "inception_report_final.pdf"], 3)
    create_artifact("Sampling Framework for 100 MDAs", "framework", 1, "final")
    create_artifact("Standardized Survey & Mapping Tools", "other", 1, "final")
    create_artifact("Enumerator Training Materials", "other", 1, "validated")
    create_artifact("Governance Structure Documentation", "other", 1, "final")

    # Phase 2
    art2_1 = create_artifact("Records Inventory Dataset for 100 MDAs", "other", 2, "validated")
    create_artifact("E-Service Maturity Assessment Results", "other", 2, "validated")
    create_artifact("Infrastructure Assessment Summary", "other", 2, "reviewed")
    create_artifact("Data Quality Dashboards", "other", 2, "draft")
    create_artifact("Field Assessment Consolidated Report", "other", 2, "draft")

    # Phase 3
    art3_1 = create_artifact("Process Maps (As-Is)", "process_map", 3, "draft")
    create_document_with_versions(art3_1, "Immigration Processing Documentation", "report", "internal", ["immigration_process_as_is.bpmn", "immigration_process_to_be.bpmn"], 2)
    create_artifact("Process Maps (To-Be)", "process_map", 3, "draft")
    create_artifact("Prioritisation Framework", "framework", 3, "draft")
    create_artifact("Ranked List of Digitization Opportunities", "other", 3, "draft")
    create_artifact("Proof of Concept Automation Designs", "other", 3, "draft")

    # Phase 4
    art4_1 = create_artifact("Digitization Framework", "framework", 4, "validated")
    create_document_with_versions(art4_1, "Master Digitization Framework", "report", "internal", ["digitization_framework_draft.docx", "digitization_framework_reviewed.docx", "digitization_framework_final.pdf"], 3)
    create_artifact("Automation Framework", "framework", 4, "draft")
    create_artifact("Data Governance Policy Recommendations", "policy", 4, "draft")
    create_artifact("Institutional Governance Model", "other", 4, "draft")
    create_artifact("Metadata Standards for Records Management", "other", 4, "draft")

    # Phase 5
    art5_1 = create_artifact("National Digitization Roadmap", "roadmap", 5, "reviewed")
    create_document_with_versions(art5_1, "Digitization Rollout Strategy", "report", "public", ["national_digitization_roadmap.xlsx", "roadmap_summary.pdf"], 2)
    create_artifact("E-Service Rollout Strategy", "roadmap", 5, "draft")
    create_artifact("KPI Monitoring Framework", "framework", 5, "draft")
    create_artifact("Cost and Investment Model", "other", 5, "restricted")
    create_artifact("Draft RFP Templates", "rfp", 5, "draft")

    # Phase 6
    create_artifact("Validation Workshop Reports", "workshop_output", 6, "draft")
    create_artifact("Final Consolidated Project Report", "other", 6, "draft")
    create_artifact("Lessons Learned Documentation", "other", 6, "draft")
    create_artifact("Project Closure Report", "other", 6, "draft")

    print("Seed Complete!")

if __name__ == "__main__":
    seed_database()
