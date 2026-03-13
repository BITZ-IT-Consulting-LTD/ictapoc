import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, DesktopReview
import random

def seed_desktop_reviews():
    print("Seeding Desktop Reviews...")
    
    mdas = MDA.objects.all()
    if not mdas.exists():
        print("No MDAs found. Please seed MDAs first.")
        return

    # Sample sectors
    sectors = ["Public Safety", "Economy & Finance", "Education", "Health", "Infrastructure", "Trade & Industry", "Natural Resources"]
    
    reviews_count = 0
    for mda in mdas:
        # Create a review for each MDA to ensure the list is populated
        sector = random.choice(sectors)
        maturity_score = random.randint(1, 5)
        
        # Example BPA data
        process_overview = {
            "process_objective": f"To modernize and digitize {mda.name} services for improved citizen experience.",
            "policy_legal_context": [f"Standard operational procedure under {mda.name} mandate."]
        }
        
        inputs_outputs = {
            "inputs": ["Physical Application Form", "Copy of National ID", "Proof of Payment"],
            "outputs": ["Official Certificate / License", "Registry Entry", "Digital Confirmation"]
        }
        
        maturity_data = {
            "score": maturity_score,
            "documentation": random.randint(1, 4),
            "data_std": random.randint(1, 4),
            "automation": random.randint(1, 3),
            "strategic": random.randint(2, 5)
        }
        
        as_is_steps = [
            {"description": "Applicant visits physical office", "actor": "Citizen"},
            {"description": "Manual verification of documents", "actor": "Officer"},
            {"description": "Submission to supervisor for approval", "actor": "Supervisor"},
            {"description": "Physical registry update", "actor": "Registrar"}
        ]
        
        to_be_process = {
            "steps": [
                {"description": "Online application submission", "actor": "Citizen", "system": True},
                {"description": "Automated document verification (IPRS/KRA)", "actor": "System", "system": True},
                {"description": "Digital approval queue", "actor": "Officer", "system": True},
                {"description": "Instant digital issuance", "actor": "System", "system": True}
            ]
        }
        
        DesktopReview.objects.get_or_create(
            mda=mda,
            process_id=f"BPA-{mda.code}-{random.randint(100, 999)}",
            defaults={
                "executive_summary": f"A comprehensive audit of the {mda.name} business processes reveals significant opportunities for digitization and inter-agency integration.",
                "process_overview": process_overview,
                "stakeholders": ["Citizens", "Internal Staff", "External Regulators"],
                "inputs_outputs_dependencies": inputs_outputs,
                "process_maturity": maturity_data,
                "as_is_narrative": "Currently heavily dependent on physical files and manual courier movements between departments.",
                "as_is_steps": as_is_steps,
                "pain_points_bottlenecks_risks": ["High administrative friction", "Risk of document loss", "Long turnaround times"],
                "to_be_process": to_be_process,
                "digitization_opportunities": ["Unified API integration", "Mobile-first delivery", "Blockchain for record integrity"],
                "metadata": {"sector": sector, "study_year": 2024}
            }
        )
        reviews_count += 1

    print(f"Successfully seeded {reviews_count} Desktop Reviews.")

if __name__ == "__main__":
    seed_desktop_reviews()
