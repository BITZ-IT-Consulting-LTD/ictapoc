# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Proof-of-Concept for Kenya's Repeatable Government Services Platform. Django REST Framework backend (monolithic) + Vue 3 SPA frontend, orchestrated via Docker Compose. Demonstrates dynamic service configuration, multi-step approval workflows, RBAC, G2G communication, and mock registry integrations.

## Development Commands

### Start/Stop Development Environment
```bash
docker-compose up --build -d       # Build and start all services
docker-compose down                # Stop all services
docker-compose down -v             # Stop and remove volumes (destroys DB)
```

### Services & Ports (Development)
- **Frontend (Vue):** http://localhost:5173 (Vite dev server with HMR)
- **Backend (Django):** http://localhost:8010 (direct) or http://localhost/api/ (via nginx)
- **Nginx proxy:** http://localhost:80 (routes /api/* to backend, /* to frontend)
- **PostgreSQL:** localhost:5436
- **Redis:** localhost:6382
- **Admin panel:** http://localhost/admin/

### Backend Commands (run inside container)
```bash
docker exec -it ictapoc-backend-1 python manage.py migrate
docker exec -it ictapoc-backend-1 python manage.py seed_platform          # Main seed command
docker exec -it ictapoc-backend-1 python manage.py seed_demo_users
docker exec -it ictapoc-backend-1 python manage.py seed_mdas_from_docs
docker exec -it ictapoc-backend-1 python manage.py seed_missing_schemas
docker exec -it ictapoc-backend-1 python manage.py test service_api       # Run backend tests
docker exec -it ictapoc-backend-1 python manage.py test service_api.tests.TestClassName  # Single test class
```

Note: `entry.sh` automatically runs migrations, collectstatic, `seed_platform`, `seed_document_repository.py`, and `seed_drms.py` on container start.

### Frontend Commands (run inside container or locally in /frontend)
```bash
npm run dev          # Vite dev server
npm run build        # Production build
npm run preview      # Preview production build
npx vitest           # Run unit tests
npx vitest run       # Run tests once (no watch)
npx playwright test  # Run E2E tests
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up --build -d   # Port 8087
```

## Architecture

### Backend (`/backend`)
Two Django apps within a Django project (`project/`):

**`service_api/`** - Core services app (mounted at `/api/`):
- **`models.py`** - 30+ models: `User`, `Role`, `MDA`, `ServiceConfig`, `ServiceRequest`, `WorkflowStep`, `WorkflowStepExecution`, `AuditLog`, `ConsentRecord`, `InterDepartmentalMemo`, `PaymentTransaction`, etc.
- **`views.py`** - 20+ DRF ViewSets registered via router
- **`serializers.py`** - DRF serializers
- **`workflow.py`** - `WorkflowEngine` class: state machine handling transitions (received -> processing -> payment -> approved -> issued)
- **`permissions.py`** - RBAC permission classes
- **`registries.py`** - Mock adapters for external registries (IPRS, BRS, CRS, NTSA, KRA)
- **`services.py`** - Business logic (payments, consent)
- **`tasks.py`** - Celery async tasks
- **`management/commands/`** - Seed commands (`seed_platform`, `seed_demo_users`, `seed_mdas_from_docs`, `seed_missing_schemas`)

**`apps/document_repository/`** - Document & Records Management (mounted at `/api/v1/`):
- **`models.py`** - `Registry`, `Node` (tree structure), `Project`, `Artifact`, `ArtifactType`, `Document`, `DocumentVersion` (versioned file storage with classification levels)
- **`views.py`** - ViewSets for artifacts, documents (upload/download/versioning), registries, nodes
- **`urls.py`** - DRF router: `types/`, `artifacts/`, `documents/`, `registries/`, `nodes/`, `repos/`
- Seeded via `seed_document_repository.py` and `seed_drms.py` (run automatically on container start)

**Key patterns:**
- Services are JSON-driven: `ServiceConfig` stores form schemas and workflow definitions as JSON fields
- RBAC roles: `citizen`, `officer`, `supervisor`, `mda_admin`, `system_admin`
- User model extends Django's AbstractUser with `role`, `mda`, `id_number` fields
- JWT auth via `djangorestframework-simplejwt` with custom email/username login backend

### Frontend (`/frontend/src`)
- **`views/`** - Page components (DashboardView, ServiceApplicationView, LoginView, etc.)
- **`components/`** - Organized by role: `Admin/`, `Citizen/`, `Supervisor/`, `Common/`
- **`store/`** - Pinia stores: `auth.js`, `citizen.js`, `staff.js`, `serviceConfig.js`, `admin.js`, `mda.js`
- **`services/`** - Axios-based API client modules
- **`modules/repository/`** - Document Repository module (pages, components, Pinia store, API service)
- **`composables/`** - Vue 3 composition functions
- **`router/index.js`** - Vue Router with role-based route guards

**Stack:** Vue 3 + Vite + Tailwind CSS 3 + Pinia + Vue Router + Axios

### Infrastructure
- **Docker Compose** orchestrates: backend, frontend, PostgreSQL 15, Redis 7, Celery worker, Nginx
- **Nginx** reverse proxy: `/api/*` -> backend:8000, `/*` -> frontend:5173
- **Celery + Redis** for background task processing

## Demo Credentials
- Users: `admin`, `citizen1`, `officer1` - Password: `Starten1@`

## API Documentation
- Swagger UI available at `/api/swagger/` when running
- ReDoc at `/api/redoc/`

## Key Integration Points (Currently Mocked)
- Registry integrations (IPRS, BRS, CRS, NTSA, KRA) return mock data via `registries.py`
- Payments use mock provider in `services.py`
- Auth is local JWT (target: Maisha Namba OIDC SSO)
- Interoperability layer planned for X-Road/KeSEL (`kesel.py` stub exists)
