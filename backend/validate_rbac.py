import os
import django
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import User, Role, MDA, ServiceConfig, ServiceRequest, AuditLog
from service_api.permissions import RBACScopeManager

def run_rbac_validation():
    print("=" * 80)
    print("🚀 RBAC POC VALIDATION SCENARIOS")
    print("=" * 80)

    # 1. Setup Test Data
    print("Setting up test environment...")
    mda_a, _ = MDA.objects.get_or_create(name="Health (RBAC Test)", code="T-MOH")
    mda_b, _ = MDA.objects.get_or_create(name="Education (RBAC Test)", code="T-MOE")
    
    svc_a, _ = ServiceConfig.objects.get_or_create(
        service_code="MOH-SVC-01", 
        defaults={"service_name": "Health Permit", "mda": mda_a}
    )
    svc_b, _ = ServiceConfig.objects.get_or_create(
        service_code="MOE-SVC-01", 
        defaults={"service_name": "School License", "mda": mda_b}
    )

    citizen, _ = User.objects.get_or_create(username="citizen_test", defaults={"role": "citizen"})
    
    req_a = ServiceRequest.objects.create(
        request_id=f"REQ-{uuid.uuid4().hex[:8]}",
        citizen=citizen,
        service_config=svc_a,
        payload={}
    )
    req_b = ServiceRequest.objects.create(
        request_id=f"REQ-{uuid.uuid4().hex[:8]}",
        citizen=citizen,
        service_config=svc_b,
        payload={}
    )

    # Roles
    global_off_role = Role.objects.get(name="GLOBAL_OFFICER")
    mda_off_role = Role.objects.get(name="MDA_OFFICER")

    # 2. Test Cases
    scenarios = [
        {
            "name": "Global Officer claiming MOH task",
            "user": "global_officer_user",
            "role": global_off_role,
            "mdas": [],
            "request": req_a,
            "expected": "ALLOW"
        },
        {
            "name": "MOH Officer claiming MOH task",
            "user": "moh_officer_user",
            "role": mda_off_role,
            "mdas": [mda_a],
            "request": req_a,
            "expected": "ALLOW"
        },
        {
            "name": "MOE Officer claiming MOH task (MDA VIOLATION)",
            "user": "moe_officer_user",
            "role": mda_off_role,
            "mdas": [mda_b],
            "request": req_a,
            "expected": "DENY"
        },
        {
            "name": "Unassigned Officer claiming MOE task",
            "user": "unassigned_officer_user",
            "role": mda_off_role,
            "mdas": [],
            "request": req_b,
            "expected": "DENY"
        }
    ]

    for s in scenarios:
        # Create/Get user
        user, _ = User.objects.get_or_create(username=s["user"], defaults={"user_role": s["role"], "role": s["role"].name})
        user.assigned_mdas.set(s["mdas"])
        user.user_role = s["role"]
        user.role = s["role"].name
        user.save()

        print(f"\nScenario: {s['name']}")
        print(f"  User: {user.username} ({user.role})")
        print(f"  Target: {s['request'].service_config.service_name} (Owned by {s['request'].service_config.mda.code})")
        
        allowed, reason = RBACScopeManager.evaluate_claim(user, s["request"])
        result = "ALLOW" if allowed else "DENY"
        
        status_mark = "✅ PASSED" if result == s["expected"] else "❌ FAILED"
        print(f"  Result: {result} - {reason}")
        print(f"  Status: {status_mark}")

    # 3. Check Audit Logs
    print("\n" + "-" * 40)
    print("📋 AUDIT LOG VERIFICATION (Recent Attempts)")
    logs = AuditLog.objects.filter(action="CLAIM_PROCESS_ATTEMPT").order_by('-timestamp')[:5]
    for log in logs:
        print(f"[{log.timestamp}] {log.actor_role} | {log.action} | {log.decision} | {log.details}")

if __name__ == "__main__":
    run_rbac_validation()
