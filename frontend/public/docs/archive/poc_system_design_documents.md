# System Design Documents

## Project: Repeatable Government Services Platform (Production-Centric POC)

---

## 1. High-Level Architecture Diagram

```mermaid
graph TD
    subgraph "Frontend Layer (Reactive UI)"
        CUI[Citizen UI]
        OWB[Officer Workbench]
        ADM[Admin Dashboard]
    end

    subgraph "API & Logic Layer (Service Orchestrator)"
        RA[RESTful API Gateway]
        WE[Workflow Engine]
        VAL[Validation Module]
    end

    subgraph "Infrastructure & Persistence"
        DB[(Relational Database)]
        RED[In-Memory Cache]
        CEL[Asynchronous Workers]
    end

    CUI & OWB & ADM <--> RA
    RA <--> WE
    WE <--> VAL
    RA <--> DB
    WE <--> CEL
    CEL <--> RED
```

**Components:**
- Citizen UI: Service request submission and tracking
- Frontend Layer: Dynamic forms, dashboards, notifications
- API Gateway: Handles request routing, authentication, and workflow orchestration
- Relational Database: Persistent storage for requests, users, audit logs, and MDA metadata
- Asynchronous Workers: Handles long-running background tasks (workflow automation, notifications)
- Service Config Store: Manages JSON/YAML service definitions and MDA configurations

---

## 2. Detailed Component Design

### 2.1 Backend Components (Service Orchestrator)
- **API Gatekeeper:** Managed endpoints for ServiceRequest, ServiceConfig, User, WorkflowStep, and MDA entities
- **Workflow Engine:** Reads service configuration templates, executes defined steps, and triggers automated tasks
- **Validation Module:** Enforces data integrity and business rules defined in the service configuration
- **Audit Module:** Immutable logging of all platform actions and state transitions
- **Notification Module:** Asynchronous delivery of emails and in-app alerts
- **Authentication Module:** Token-based security supporting hierarchical role-based access control
- **Service Configuration Module:** Enables dynamic addition/editing of services via a metadata-driven approach
- **MDA Registration Module:** Provisioning of Ministries, Departments, and Agencies (MDAs) with administrative role mapping

### 2.2 Frontend Components
- **Dynamic Form Generator:** Reads service config and builds forms for citizens and officers
- **Citizen Dashboard:** Submit and track requests
- **Officer Dashboard:** Review, approve/reject, escalate
- **Supervisor Dashboard:** Monitor workflows, approve escalations, generate reports
- **MDA Management Dashboard:** Register or modify MDAs, assign officers and roles
- **Notifications Module:** Real-time notifications and alerts

---

## 3. Data Model / Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    MDA ||--o{ ServiceConfig : "manages"
    MDA ||--o{ User : "has officers"
    ServiceConfig ||--o{ WorkflowStep : "defines"
    ServiceConfig ||--o{ ServiceRequest : "has"
    User ||--o{ ServiceRequest : "submits"
    ServiceRequest ||--o{ AuditLog : "tracks"
    User ||--o{ AuditLog : "performs"

    ServiceConfig {
        string service_code PK
        string service_name
        json config
    }
    WorkflowStep {
        string step_name
        string role
        int sequence
        json api_config
    }
    ServiceRequest {
        string request_id PK
        string status
        json payload
        datetime created_at
    }
    User {
        string username PK
        string email
        string role
    }
    MDA {
        int id PK
        string name
        string description
    }
    AuditLog {
        string action
        datetime timestamp
        string details
    }
```
**Notes:**
- `ServiceConfig` drives dynamic workflows.
- `WorkflowStep` defines each stage with assigned roles.
- `ServiceRequest` captures user submissions.
- `User` contains roles for RBAC.
- `MDA` stores all registered Ministries, Departments, and Agencies.
- `AuditLog` captures all activities for traceability.

---

## 4. Service and MDA Configuration
- **Service Registration:** JSON/YAML structure with service code, workflow, validation rules, SLA, and output.
- **MDA Registration:** Add new MDAs with name, description, and role assignments.
- Dynamic assignment of officers to workflow steps.
- Admin interface to modify service configurations and MDA details without code changes.

---

## 5. Assumptions
- AI agent can read JSON/YAML service configurations.
- Dockerized backend mirrors production configuration.
- Sample services and MDAs are sufficient to demonstrate workflows.
- External integrations will be mocked during POC.

---

## 6. Acceptance Criteria
- High-level architecture supports production-centric scalability.
- Backend and frontend modules are defined and mapped.
- Data model supports dynamic workflows, service requests, and MDA management.
- Workflow execution can be simulated using sample service configurations.
- Admins can register MDAs and configure services without code changes.
- Audit logging and notifications are fully functional.

