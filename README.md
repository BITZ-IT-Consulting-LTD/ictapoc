# Repeatable Government Services Platform (POC)

This is a **Proof-of-Concept (POC)** for a Repeatable Government Services Platform, built with Django REST Framework (Backend) and Vue 3 (Frontend).

> **⚠️ ARCHITECTURE NOTICE:**
> This codebase represents the **Functional Prototype** of the platform.
> For the **Target Production Architecture** (GEA Compliant), please refer to [System Architecture](./docs/architecture/architecture_three.md).
>
> **Current Compliance Status:**
> - **Service Configuration:** ✅ GEA Compliant (JSON-driven)
> - **RBAC:** ✅ GEA Compliant (Granular Roles)
> - **Interoperability:** ⚠️ **Mocked** (Requires X-Road Integration)
> - **Payments:** 🔴 **Missing** (Requires Govt Payment Aggregator)
> - **Identity:** ⚠️ **Local Auth** (Requires Maisha Namba SSO)

---

## Key Features (Implemented)
*   **Dynamic Service Engine:** Define services, forms, and workflows via JSON configuration.
*   **Workflow Automation:** Configurable state machine for multi-step approvals (Citizen -> Officer -> Supervisor).
*   **Role-Based Access Control (RBAC):** Granular permissions for Citizens, Officers, Supervisors, and Admins.
*   **Service Catalogue:** Centralized registry of government services with metadata.
*   **G2G Communication:** Digital memos and official correspondence between MDAs.
*   **Audit Trail:** Comprehensive logging of all actions for accountability.

## Project Structure

```
.
├── backend/                  # Django REST Framework (Monolithic Prototype)
│   ├── project/              # Settings & Configuration
│   ├── service_api/          # Core App (Services, Workflows, Models)
│   ├── manage.py             # Management Script
│   └── seed_data.py          # Data Seeding Scripts
├── frontend/                 # Vue 3 Frontend
│   ├── src/                  # Components, Views, Router
├── docker/                   # Docker Configuration
├── docs/                     # 📚 Architecture & Design Documentation
├── data/                     # Seed Data (CSVs, JSONs)
└── docker-compose.yml        # Container Orchestration
```

## 📚 Documentation Library

The project documentation is the **Single Source of Truth** for the target state architecture:

*   **[Architecture Design](./docs/architecture/)**
    *   [Target System Architecture (GEA Compliant)](./docs/architecture/architecture_three.md)
    *   [Workflow Logic & BPMN](./docs/architecture/poc_algorithm_workflow_documentation.md)
*   **[Technical Specifications](./docs/poc/)**
    *   [System Design Documents](./docs/poc/poc_system_design_documents.md)
    *   [Functional Requirements](./docs/poc/poc_functional_non_functional_requirements.md)
*   **[Reports & Analysis](./docs/reports/)**
    *   [Comprehensive POC Report](./docs/reports/ICTA_POC_Comprehensive_Report.md)

---

## Production Roadmap (GEA Compliance)

To transition this POC to a **Live National Platform**, the following modules must be integrated:

1.  **Government Payment Aggregator (GPA):**
    *   Integrate with M-Pesa/Banks for real-time payments.
    *   Implement **Revenue Splitting** logic (County/National Treasury).
2.  **Interoperability Layer (KeSEL / X-Road):**
    *   Replace mock registries with **X-Road Security Server** adapters.
    *   Connect to **IPRS (Identity)**, **BRS (Business)**, and **NLIMS (Land)**.
3.  **Data Protection & Consent:**
    *   Implement a **Consent Manager** to capture citizen authorization for data sharing.
4.  **Identity Federation:**
    *   Replace local JWT auth with **Maisha Namba (OIDC)** Single Sign-On.

---

## Getting Started

### Prerequisites
*   Docker & Docker Compose installed.

### Quick Start

1.  **Clone & Build:**
    ```bash
    git clone <repo_url>
    cd ictapoc
    docker-compose up --build -d
    ```

2.  **Seed Data:**
    ```bash
    docker exec -it ictapoc-backend-1 python manage.py migrate
    docker exec -it ictapoc-backend-1 python seed_data.py
    ```
    *(Creates demo users: `admin`, `citizen1`, `officer1` with password `Starten1@`)*

3.  **Access the App:**
    *   **Frontend:** [http://localhost:5173](http://localhost:5173)
    *   **API:** [http://localhost:80/api/](http://localhost:80/api/)
    *   **Admin Panel:** [http://localhost:80/admin/](http://localhost:80/admin/)

---

## Demo Scenarios

### 1. Citizen Application
*   Login as **citizen1**.
*   Select **"Business Permit"** from the Catalogue.
*   Fill the form (Auto-fills from Profile).
*   Submit Application.

### 2. Officer Review
*   Login as **officer1**.
*   Go to **"My Tasks"**.
*   Review the application and documents.
*   Click **"Approve"** to forward to Supervisor.

### 3. G2G Memo
*   Login as **admin** (MDA Admin).
*   Go to **"Office Automation"** > **"New Memo"**.
*   Draft a memo to another department and send for internal review.
