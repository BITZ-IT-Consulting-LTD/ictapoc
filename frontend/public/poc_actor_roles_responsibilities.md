# User Roles & Responsibilities Matrix

This document outlines the specific actors within the Kenya Digital Service Automation Platform (POC), detailing their scope, capabilities, and interaction with the system workflows.

## 1. The Citizen (Service Consumer)
**Persona in POC**: `citizen1`  
**Role Scope**: The primary beneficiary of the platform. Accesses government services through self-service channels.

### Key Responsibilities
*   **Service Discovery**: browsing the catalog of available government services (e.g., Birth Registration, Business Permits).
*   **Application Submission**: Filling out dynamic forms and uploading required attributes/documents.
*   **Status Tracking**: Monitoring the realtime progress of their requests (Received -> In Progress -> Approved).
*   **Feedback**: Receiving notifications on approval, rejection, or requests for more information.

### Workflow Interaction
*   **Initiator**: Triggers the `create_service_request` event.
*   **Viewer**: Can only view requests where they are the `owner`.

---

## 2. The Officer (Technical Execution)
**Persona in POC**: `officer1`  
**Role Scope**: Government staff responsible for the initial processing, verification, and drafting of technical documents.

### Key Responsibilities
*   **Task Management**: access the "My Tasks" or "Officer Workbench" to see applications assigned to their role.
*   **Verification**: Reviewing submitted data against requirements (e.g., verifying a Business Permit application).
*   **Drafting (Internal Services)**: For internal G2G workflows (like Cabinet Memos), the Officer acts as the **Drafter** or Technical Initiator.
*   **Implementation**: executing post-approval tasks (e.g., "Post-Cabinet Implementation Tracking").

### Workflow Interaction
*   **Processor**: completes `manual` workflow steps (e.g., Sequence 1 & 2).
*   **Actions**: `Verify`, `Submit`, `Review`.

---

## 3. The Supervisor (Authority & Oversight)
**Persona in POC**: `supervisor1`  
**Role Scope**: Senior management (e.g., Principal Secretaries, Cabinet Secretaries) responsible for approvals and exception handling.

### Key Responsibilities
*   **Approval Authority**: providing the "green light" for sensitive stages (e.g., PS Clearance, Granting a Passport).
*   **Escalation Handling**: resolving requests that have been "flagged" or "escalated" by junior officers.
*   **Performance Monitoring**: viewing team reports and service level agreement (SLA) adherence.

### Workflow Interaction
*   **Approver**: completes higher-sequence `manual` steps (e.g., Sequence 3 & 4).
*   **Actions**: `Approve`, `Reject`, `Escalate`.

---

## 4. The Administrator (Configuration & Governance)
**Persona in POC**: `admin`  
**Role Scope**: Responsible for system health, service definition, and high-level compliance checks (e.g., Cabinet Office Secretariat).

### Key Responsibilities
*   **Service Definition**: Creating new services, linking them to MDAs, and building form schemas via the schema builder.
*   **Workflow Design**: Defining the linear sequence of approval steps and assigning them to roles.
*   **Compliance Checks**: For high-level workflows (Cabinet Memos), the Admin acts as the **Secretariat** to verify format and policy compliance.
*   **Audit**: viewing the global audit log for security and traceability.

### Workflow Interaction
*   **Architect**: defines `ServiceConfig` and `WorkflowStep`.
*   **Gatekeeper**: completes the final governance steps (e.g., "Cabinet Consideration").

---

## 5. System Actors (Automation & Interoperability)
**Persona in POC**: `KeSEL` (Kenya Secure Exchange Layer) / `WorkflowEngine`  
**Role Scope**: Non-human actors that execute logic, ensure security, and validate data.

### Key Responsibilities
*   **Orchestration**: The `WorkflowEngine` automatically moves a request from Step 1 to Step 2 upon completion.
*   **Interoperability**: The `KeSEL` bridge performs secure Peer-to-Peer (P2P) exchanges with authoritative registries (IPRS, BRS).
*   **Validation**: Automatically checking data rules (e.g., "Does this ID number exist?") without human intervention.
*   **Notification**: Sending emails/alerts to users upon status changes.

### Workflow Interaction
*   **Automator**: executes `api_call` steps.
*   **Enforcer**: blocks requests that fail automated validation.
