# Repeatable Government Services Platform (POC)

This is a Production-Centric Proof-of-Concept (POC) for a Repeatable Government Services Platform, built with Django REST Framework for the backend and Vue 3 for the frontend, deployed using Docker.

## Key Features (Implemented)
*   **Dynamic Service Configuration:** Define services and schemas via JSON.
*   **Workflow Engine:** Configurable state machine for workflows (Steps, Roles, Actions).
*   **RBAC (Role-Based Access Control):** Granular permissions and Roles (Citizen, Officer, Supervisor, Admin).
*   **Public Registration:** Citizens can self-register.
*   **Profile Management:** Citizens can manage persistent profile data (ID, Passport) and Document Wallet.
*   **Verification Workflow:** Sensitive profile updates trigger a review workflow (Officer Verify -> Supervisor Approve).
*   **Document Preview:** Integrated document viewer for PDFs and images.
*   **Admin Dashboard:** Tools for managing MDAs, Services, and Roles.

## Project Structure

```
.
├── backend/                  # Django REST Framework Backend
│   ├── project/              # Django Project settings and URLs
│   ├── service_api/          # Django App for services, workflows, models, views, serializers
│   ├── manage.py             # Django management script
│   └── seed_data.py          # Seeding script for Demo Data
├── frontend/                 # Vue 3 Frontend
│   ├── src/                  # Vue source code (components, views, router, store, services)
├── docker/                   # Docker configurations
├── docs/                     # Project Documentation Library
├── data/                     # Seed data and CSV exports
├── .env                      # Environment variables
└── docker-compose.yml        # Docker Compose setup
```

## 📖 Documentation Index

The project documentation is organized into specialized directories for better maintainability:

*   **[Architecture](./docs/architecture/)**: Technical design, RBAC, and Workflow logic.
    *   [System Architecture](./docs/architecture/architecture_three.md)
    *   [RBAC Summary](./docs/architecture/RBAC_IMPLEMENTATION_SUMMARY.md)
    *   [Workflow Engine](./docs/architecture/poc_algorithm_workflow_documentation.md)
*   **[POC Core Documents](./docs/poc/)**: Requirements, Design, and Test plans.
    *   [Project Overview](./docs/poc/poc_project_overview_concept_note.md)
    *   [Functional Requirements](./docs/poc/poc_functional_non_functional_requirements.md)
*   **[Guides](./docs/guides/)**: Deployment and integration instructions.
    *   [Deployment Plan](./docs/guides/poc_deployment_dev_ops_plan.md)
    *   [Huduma Bridge Instructions](./docs/guides/huduma_bridge_instructions.md)
*   **[Style Guide](./docs/style-guide/)**: BEM naming conventions and UI patterns.
    *   [BEM Documentation](./docs/style-guide/BEM-DOCUMENTATION.md)
*   **[Reports](./docs/reports/)**: Progress reports and meeting actions.
    *   [Comprehensive POC Report](./docs/reports/ICTA_POC_Comprehensive_Report.md)
    *   [Consolidated Actions](./docs/reports/ICTA_WB_CONSOLIDATED_ACTIONS.md)
*   **Live Catalogue**: Accessible via the **Admin Dashboard > Operations > Whole-of-Gov Catalogue** tab.

## Getting Started

### Prerequisites
*   Docker and Docker Compose installed.

### Setup and Deployment

1.  **Clone the repository & Configure .env** (Using example provided).

2.  **Build and Run:**
    ```bash
    docker-compose up --build -d
    ```

3.  **Apply Migrations & Seed Data:**
    This script wipes the DB and provisions:
    - Users: `admin`, `citizen1`, `officer1`, `supervisor1`
    - Roles & Permissions
    - Services: Birth Registration, Profile Update, etc.
    
    ```bash
    # Run in backend container
    docker exec -it ictapoc-backend-1 python manage.py migrate
    docker exec -it ictapoc-backend-1 python seed_data.py
    ```
    *(Note: `seed_data.py` sets password `Starten1@` for all demo users)*

### Accessing the Application

*   **Frontend:** `http://localhost:5173` (Dev Mode) or `http://localhost:80` (Nginx).
*   **Backend API:** `http://localhost:80/api/` (Proxied).

**Demo Credentials:**
*   **Citizen:** `citizen1` / `Starten1@`
*   **Officer:** `officer1` / `Starten1@`
*   **Supervisor:** `supervisor1` / `Starten1@`
*   **Admin:** `admin` / `Starten1@`

## Workflow Demo
1.  **Register/Login** as Citizen.
2.  **Apply** for Birth Registration (Auto-fills from profile).
3.  **Logout**, Login as Officer (`officer1`).
4.  **View Request**, Verify Documents, Approve/Next.
5.  Login as Supervisor (`supervisor1`) for final approvals if required.

## Profile Update Demo
1.  Login as Citizen.
2.  Go to **Profile**.
3.  Update Phone/ID and Attach Proof.
4.  Submit.
5.  Login as Officer to Verify.
6.  Login as Supervisor to Approve.
