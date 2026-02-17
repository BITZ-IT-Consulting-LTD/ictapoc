# RBAC Implementation Summary: Repeatable Government Services Platform

## 1. Role & Scope Model
A tiered RBAC model has been implemented to support cross-agency oversight and institutional autonomy.

### Global Roles (Full Authority)
- **GLOBAL_OFFICER**: Can view and claim any process across any MDA.
- **GLOBAL_SUPERVISOR**: Can view, claim, and perform supervisory actions across any MDA.

### MDA-Scoped Roles (Restricted Authority)
- **MDA_OFFICER**: Limited to view/claim processes within assigned MDA(s).
- **MDA_SUPERVISOR**: Limited to view/claim/supervise within assigned MDA(s).

## 2. Enforcement Logic (Pseudocode)
The following logic is enforced on every "Claim" and "Action" request:

```python
if user.role in [GLOBAL_OFFICER, GLOBAL_SUPERVISOR]:
    allow_claim()
else if user.role in [MDA_OFFICER, MDA_SUPERVISOR]:
    if process.owning_mda_id in user.assigned_mdas:
        allow_claim()
    else:
        deny("MDA scope violation")
else:
    deny("Unauthorized role")
```

## 3. Integration Points
- **API Guard**: A custom DRF permission class `IsClaimAuthorized` validates every request.
- **Queryset Scoping**: The `ServiceRequestViewSet` automatically filters list views based on the user's scope.
- **Workflow Engine**: Authorization checks are injected into manual step transitions.

## 4. Audit & Compliance
Every claim attempt is logged in an immutable `AuditLog` table with the following structure:
- `user_id`, `actor_role`, `actor_mdas`
- `process_id`, `service_id`, `owning_mda_id`
- `decision` (ALLOW / DENY)
- `details` (Reasoning for the decision)

## 5. POC Validation Results
| Test Scenario | Role | Target MDA | Expected | Result |
| :--- | :--- | :--- | :--- | :--- |
| Global officer claiming any MDA process | GLOBAL_OFFICER | MOH | ALLOW | ✅ PASSED |
| Global supervisor claiming any MDA process | GLOBAL_SUPERVISOR | MOE | ALLOW | ✅ PASSED |
| MDA officer claiming own MDA service | MDA_OFFICER | MOH (Assigned) | ALLOW | ✅ PASSED |
| MDA officer claiming different MDA service | MDA_OFFICER | MOH (Not Assigned) | DENY | ✅ PASSED |
| Missing MDA assignment | MDA_OFFICER | - | DENY | ✅ PASSED |

## 6. UI Behavior Rules
- **Disabled Actions**: The "Claim Task" button is disabled client-side when the MDA ID mismatch is detected.
- **Error Toasts**: API-level scope violations trigger a toast: *"You are not authorized to act on services outside your MDA."*
