# Algorithm & Workflow Documentation

## Project: Repeatable Government Services Platform (Production-Centric POC)

---

## 1. Pseudo-Code: Service Processing Algorithm
```python
def process_service_request(service_code, citizen_id, payload):
    # Load service configuration
    service_config = load_service_config(service_code)

    # Validate input according to service rules
    if not validate_request(payload, service_config['rules']):
        log_audit(citizen_id, service_code, 'VALIDATION_FAILED')
        return {'status': 'VALIDATION_FAILED', 'message': 'Input validation failed.'}

    # Create service request record
    request = create_service_request(citizen_id, service_code, payload)

    # Execute workflow steps
    for step in service_config['workflow']:
        assigned_role = step['role']
        action_required = step['action']

        # Automatic step (optional AI validation)
        if step.get('auto_process'):
            perform_auto_action(request, step)
            log_audit(citizen_id, service_code, f'AUTO_{action_required}')
            continue

        # Manual review step
        notify_role(assigned_role, request, action_required)
        wait_for_action(request, assigned_role)
        log_audit(citizen_id, service_code, f'MANUAL_{action_required}')

        # Check SLA and escalate if needed
        if step.get('sla') and check_sla(request, step['sla']):
            escalate_request(request, step)
            log_audit(citizen_id, service_code, 'ESCALATED')

    # Close request after workflow completion
    update_request_status(request, 'CLOSED')
    log_audit(citizen_id, service_code, 'CLOSED')
    return {'status': 'CLOSED', 'request_id': request.id}
```

---

## 2. Activity Diagram

```mermaid
stateDiagram-v2
    [*] --> Submitted: Citizen Submits Request
    Submitted --> Validating
    Validating --> ValidationFailed: Validation Fails
    ValidationFailed --> NotifyCitizen
    NotifyCitizen --> [*]
    
    Validating --> InProgress: Validation Passes
    state InProgress {
        [*] --> StepExecution
        StepExecution --> AutoAction: auto_process == true
        AutoAction --> NextStep
        StepExecution --> ManualAction: auto_process == false
        ManualAction --> WaitForOfficer: Notify Assigned Role
        WaitForOfficer --> Decision: Action Logged
        Decision --> NextStep: Approved
        Decision --> Rejected: Rejected
        NextStep --> WorkflowComplete: All Steps Done
        NextStep --> StepExecution: Remaining Steps
    }
    
    WorkflowComplete --> Closed
    Rejected --> Closed
    Closed --> NotifyCitizenOutcome: Notify Citizen
    NotifyCitizenOutcome --> [*]
    
    InProgress --> Escalated: SLA Breach
    Escalated --> InProgress: Supervisor Review
```

---

## 3. Sequence Diagram

```mermaid
sequenceDiagram
    participant C as Citizen
    participant F as Frontend (Vue)
    participant A as API (DRF)
    participant E as Workflow Engine
    participant R as Authoritative Registry

    C->>F: Submit Request
    F->>A: POST /service-requests/
    A->>A: Validate Schema
    A->>E: Initialize Workflow
    E->>A: Create Audit Log (RECEIVED)
    
    alt is Step Type: api_call
        E->>R: Execute API Request
        R-->>E: Return Result
        E->>A: Update Request Status
    else is Step Type: manual
        E->>F: Notify Assigned Role
        F->>A: Submit Action (Approve/Reject)
        A->>E: Advance Workflow
    end
    
    E->>A: Finalize (APPROVED/REJECTED)
    A->>F: Push Notification
    F->>C: Display Result
```

---

## 4. Class Diagram

```mermaid
classDiagram
    class ServiceConfig {
        +string service_code
        +string service_name
        +json config
    }
    class WorkflowStep {
        +string step_name
        +string step_type
        +string role
        +int sequence
        +json api_config
    }
    class ServiceRequest {
        +string request_id
        +json payload
        +string status
        +bool is_escalated
    }
    class User {
        +string username
        +string email
        +string role
    }
    class MDA {
        +string name
        +string description
    }
    class AuditLog {
        +string action
        +datetime timestamp
        +text details
    }

    ServiceConfig "1" -- "*" WorkflowStep : "has"
    ServiceConfig "1" -- "*" ServiceRequest : "instantiates"
    MDA "1" -- "*" ServiceConfig : "governs"
    ServiceRequest "*" -- "1" User : "submitted by"
    ServiceRequest "1" -- "*" AuditLog : "logs"
    User "1" -- "*" AuditLog : "acts in"
```
---

## 5. Service Configuration Example (JSON)
```json
{
  "service_code": "BIRTH_REG",
  "workflow": [
    {"step_name": "Initial Validation", "role": "Officer", "action": "validate", "auto_process": true},
    {"step_name": "Approval", "role": "Supervisor", "action": "approve"}
  ],
  "rules": {"required_fields": ["full_name", "dob", "parent_ids"]},
  "sla": 3,
  "output": "Birth Certificate"
}
```

---

## 6. Notes
- Algorithm supports **dynamic services** configured via JSON/YAML.
- Workflow engine handles **manual and automatic steps** with SLA monitoring.
- Audit logging ensures **traceability** of all actions.
- Sequence and activity diagrams provide **full view of request processing**.
- Class diagram captures core entities for **database and API design**.

