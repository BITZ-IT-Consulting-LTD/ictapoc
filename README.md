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
├── .env                      # Environment variables
└── docker-compose.yml        # Docker Compose setup
```

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
