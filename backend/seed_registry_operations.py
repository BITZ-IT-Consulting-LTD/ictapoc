import os
import django
import random
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import User, MDA, GovernmentFile, InterDepartmentalMemo, ServiceRequest

def seed_registry_operations():
    """
    Seeds Government Files and Inter-Departmental Memos for the MDA Registry.
    """
    print("🚀 Seeding Government Files and Registry Operations...")

    mdas = list(MDA.objects.all())
    staff_users = list(User.objects.filter(role__in=['officer', 'supervisor', 'admin']))

    if not mdas or not staff_users:
        print("❌ MDAs or Staff Users missing. Run seed_demo_users.py first.")
        return

    subjects = [
        "Digitization of Records Phase 1",
        "Quarterly Performance Review",
        "Inter-Agency Collaborative Framework",
        "Budget Estimates for FY 2024/25",
        "Public Participation Report: Digital ID",
        "Audit Findings - Revenue Collection",
        "Staff Training on GEA Standards",
        "Procurement of Specialized Equipment",
        "Legal Opinion on Data Sharing Agreement",
        "Request for Concurrence on Policy Update"
    ]

    # 1. Create Government Files
    files = []
    for mda in mdas:
        for i in range(3):
            file_num = f"{mda.code}/REG/{random.randint(100, 999)}/{datetime.now().year}"
            gov_file, created = GovernmentFile.objects.update_or_create(
                file_number=file_num,
                defaults={
                    "subject": random.choice(subjects),
                    "owning_mda": mda,
                    "status": random.choice(['open', 'pending', 'closed'])
                }
            )
            files.append(gov_file)
            if created:
                print(f"  [File] Created {file_num}")

    # 2. Create Inter-Departmental Memos
    memo_types = ['policy', 'operational', 'instruction', 'concurrence', 'escalation', 'information']
    memo_statuses = ['actioning', 'approved', 'registered', 'signed', 'responded', 'closed']

    for i in range(20):
        sender_mda = random.choice(mdas)
        recipient_mda = random.choice([m for m in mdas if m != sender_mda])
        sender = random.choice([u for u in staff_users if u.mda == sender_mda]) if any(u.mda == sender_mda for u in staff_users) else random.choice(staff_users)
        
        gov_file = random.choice([f for f in files if f.owning_mda == sender_mda])
        
        ref = f"MEMO/{sender_mda.code}/{recipient_mda.code}/{random.randint(1000, 9999)}"
        
        memo, created = InterDepartmentalMemo.objects.update_or_create(
            official_ref=ref,
            defaults={
                "gov_file": gov_file,
                "sender": sender,
                "sender_mda": sender_mda,
                "recipient_mda": recipient_mda,
                "memo_type": random.choice(memo_types),
                "subject": f"RE: {gov_file.subject} - Follow up {i}",
                "content": f"Formal communication regarding the ongoing collaboration on {gov_file.subject}. Please review the attached documents and provide feedback by end of week.",
                "status": random.choice(memo_statuses),
                "priority": random.choice(['normal', 'high', 'urgent']),
                "digitally_signed": random.choice([True, False])
            }
        )
        if created:
            print(f"  [Memo] Created {ref} ({sender_mda.code} -> {recipient_mda.code})")

    print("✅ Registry Seeding Completed!")

if __name__ == "__main__":
    seed_registry_operations()
