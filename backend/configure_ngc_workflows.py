
import os
import django
import json
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import MDA, ServiceConfig, WorkflowStep, ServiceDomain, ServiceCategory, ServiceRequest, User, Role

def configure_ngc_workflow():
    mda = MDA.objects.get(id=53)
    print(f"Configuring National Government Coordination Workflows for {mda.name}")

    domain, _ = ServiceDomain.objects.get_or_create(name="Interior & National Administration")
    category, _ = ServiceCategory.objects.get_or_create(name="Monitoring & Projects", domain=domain)

    # 1. National Projects Field Monitoring & Reporting
    wf_config = {
        "service_name": "National Projects Field Monitoring & Reporting",
        "service_code": "NGC-FIELD-001",
        "category": category,
        "mda": mda,
        "description": "Digitized field data collection for site visits to support the National Projects Dashboard.",
        "config": {
            "environment": "POC",
            "lifecycle": "active",
            "mobile_ready": True,
            "offline_support": "Enabled",
            "geo_enforcement": True,
            "alerts": ["Delay", "Stalled", "Cost Overrun"]
        }
    }
    svc, _ = ServiceConfig.objects.get_or_create(service_code=wf_config["service_code"], defaults=wf_config)
    
    # Remove existing steps to ensure fresh sequence
    svc.workflow_steps.all().delete()

    steps = [
        (1, "Plan & Prioritise Visits", "manual", "supervisor", "plan_visits"),
        (2, "Schedule & Prepare", "manual", "supervisor", "schedule"),
        (3, "Conduct Site Visit", "manual", "officer", "inspect"),
        (4, "Enter & Sync Field Data", "manual", "officer", "sync_data"),
        (5, "Review & Verify Submission", "manual", "supervisor", "verify"),
        (6, "Quality Assurance & Audit", "manual", "supervisor", "audit"),
        (7, "Dashboard Integration", "api_call", "system_admin", "update_dashboard"),
        (8, "Reporting & Feedback", "manual", "mda_admin", "generate_report"),
    ]
    for seq, name, stype, role, act in steps:
        WorkflowStep.objects.create(
            service_config=svc, sequence=seq,
            step_name=name, step_type=stype, role=role, action=act
        )

    print(f"Workflow configured: {svc.id}")

    # Generate test data
    citizen = User.objects.filter(role='citizen').first()
    if not citizen:
        citizen_role = Role.objects.get(name='citizen')
        citizen = User.objects.create_user(username='ngc_tester', password='Starten1@', email='ngc@test.com', role='citizen', user_role=citizen_role)

    projects = [
        "Nairobi Expressway Extension", "Galana-Kulalu Irrigation Project", "LAPSSET Pipeline Segment A",
        "Konza Technopolis Phase 2", "National Data Center Expansion", "Last Mile Connectivity Phase IV",
        "Standard Gauge Railway Extension", "Mombasa Port Berth 22", "Lake Victoria Water Cluster", "Northern Collector Tunnel"
    ]

    # Generate 10 Projects / 20 Site Visits
    for i in range(20):
        project_name = projects[i % len(projects)]
        ServiceRequest.objects.create(
            request_id=f"NGC-SITE-{202600+i}",
            service_config=svc,
            citizen=citizen,
            status='received' if i % 2 == 0 else 'in_progress',
            current_step=svc.workflow_steps.first() if i % 2 == 0 else svc.workflow_steps.get(sequence=3),
            payload={
                "project_name": project_name,
                "visit_type": "Progress Inspection",
                "priority": "High" if random.random() > 0.7 else "Normal",
                "county": random.choice(["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Uasin Gishu"]),
                "geotag": f"{random.uniform(-1.5, 1.5)}, {random.uniform(34.0, 40.0)}",
                "budget_utilisation": f"{random.randint(10, 95)}%",
                "status_color": random.choice(["Green", "Yellow", "Red"])
            }
        )
    
    print("Sample test data (10 projects, 20 site visits) generated.")

if __name__ == "__main__":
    configure_ngc_workflow()
