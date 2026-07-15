# GoK Repeatable Government Services Platform

A proof-of-concept platform for configuring and delivering repeatable government services across ministries, departments, and agencies (MDAs). It combines configurable forms and workflows, role-based service processing, digital public infrastructure (DPI) integration patterns, consent, payments, authoritative registries, auditability, and an Electronic Document and Records Management System (EDRMS).

The application uses Django REST Framework, PostgreSQL, Redis/Celery, Vue 3, and Nginx. The assumed production POC URL is **https://gokservices.bitz-itc.com/**.

> [!IMPORTANT]
> This is a functional POC, not a completed national production platform. KeSEL/X-Road, Maisha Namba, National PKI, banking, Treasury, and authoritative registry connections are represented through POC adapters or simulated integrations. Do not use real citizen, payment, credential, or classified data.

## Start here

| Need | Authoritative file |
|---|---|
| Understand the product | [Project overview and concept note](./docs/poc/poc_project_overview_concept_note.md) |
| Understand the requirements | [Functional and non-functional requirements](./docs/poc/poc_functional_non_functional_requirements.md) |
| Understand the solution design | [System design](./docs/poc/poc_system_design_documents.md) |
| Understand the target architecture | [GEA-aligned system architecture](./docs/architecture/architecture_three.md) |
| Understand workflow execution | [Workflow engine and algorithm](./docs/architecture/poc_algorithm_workflow_documentation.md) |
| Review validation expectations | [Test and validation plan](./docs/poc/poc_test_validation_plan.md) |
| Run locally | [Local development](#local-development) |
| Deploy the production POC | [Production deployment guide](./docs/guides/DEPLOYMENT.md) |
| Install host Nginx | [Domain-specific host configuration](./docker/prod/nginx/host-gokservices.bitz-itc.com.conf) |

## Current implementation status

| Capability | POC status | Production gap |
|---|---|---|
| Configurable services, forms, and workflows | Implemented | Production governance and change control |
| Role-based access | Implemented | Enterprise identity lifecycle and formal access reviews |
| Citizen, officer, supervisor, MDA admin, and platform admin journeys | Implemented | User acceptance and accessibility validation |
| Whole-of-government service catalogue | Implemented and seeded | Authoritative catalogue ownership process |
| Registry adapters | Implemented with seeded/mock data | Live KeSEL/X-Road security servers and MDA integrations |
| Consent manager | POC implemented | Production privacy policy, identity binding, and legal approval |
| Government payments and reconciliation | POC implemented | Live GPA, banks, mobile money, and Treasury integration |
| Identity federation and NPKI | Represented in the trust architecture | Live Maisha Namba/OIDC and certificate infrastructure |
| EDRMS | Implemented | Retention policy, classification, archival, and records authority approval |
| Audit and platform health | Implemented | Central SIEM, alerting, incident response, and retention |

## Architecture at a glance

```text
Digital frontend channels
        |
API gateway + core orchestration
        |
Huduma Bridge / interoperability adapters
        |
Authoritative registries + payments + EDRMS

Cross-cutting: identity, NPKI, consent, RBAC, audit, observability
```

The detailed target model is in [architecture_three.md](./docs/architecture/architecture_three.md). The system-architect view is also rendered in the admin dashboard under **Technical Evidence**.

## Repository structure

```text
.
├── backend/
│   ├── project/                         # Django settings, URLs, Celery and WSGI
│   ├── service_api/                     # Services, workflows, users, DPI and APIs
│   ├── apps/document_repository/        # EDRMS backend
│   └── manage.py
├── frontend/
│   ├── src/                             # Vue application
│   ├── src/modules/repository/          # EDRMS frontend module
│   └── public/docs/                     # Documentation rendered inside the POC
├── docker/
│   ├── dev/                             # Development images and proxy
│   └── prod/                            # Production images and Nginx configs
├── docs/                                # Architecture, specifications and reports
├── mdas/                                # Source MDA documentation and process material
├── docker-compose.yml                   # Local development stack
├── docker-compose.prod.yml              # Production stack
└── .env.production.example              # Safe environment-variable template
```

## Local development

### Prerequisites

- Git
- Docker Engine or Docker Desktop
- Docker Compose plugin (`docker compose`)
- At least 4 GB of memory available to Docker

### 1. Clone the repository

```bash
git clone https://github.com/BITZ-IT-Consulting-LTD/ictapoc.git
cd ictapoc
```

### 2. Create the local environment file

```bash
cp .env.production.example .env
```

Replace all placeholder secrets. For local development, set:

```dotenv
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,backend,gokservices.bitz-itc.com
POSTGRES_HOST=db
POSTGRES_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
USE_X_ACCEL_REDIRECT=False
```

Generate development secrets with `openssl rand -hex 32`. Never commit `.env`.

### 3. Start the stack

```bash
docker compose up -d --build
docker compose ps
```

The backend entrypoint automatically:

1. Applies database migrations.
2. Collects Django static files.
3. Runs the complete platform seed.
4. Seeds the EDRMS structures and sample data.

### 4. Open the application

| Service | URL |
|---|---|
| Vue application | http://localhost:5173 |
| Unified Nginx entry point | http://localhost |
| Django API | http://localhost:8010/api/ |
| Django Admin | http://localhost:8010/admin/ |
| Swagger API documentation | http://localhost:8010/swagger/ |
| Liveness | http://localhost:8010/health |
| Readiness | http://localhost:8010/ready |
| PostgreSQL from host tools | localhost:5436 |
| Redis from host tools | localhost:6382 |

The home page permanently exposes one direct-access button per high-level actor category. The login page retains the complete seeded account matrix for detailed role testing. Seeded accounts use the demonstration password `Starten1@`; never retain this password on an unrestricted deployment.

## Common developer commands

```bash
# Follow all service logs
docker compose logs -f --tail=200

# Follow one service
docker compose logs -f backend

# Open a Django shell
docker compose exec backend python manage.py shell

# Create and apply a migration
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate

# Run Django checks
docker compose exec backend python manage.py check

# Run backend tests
docker compose exec backend python manage.py test

# Validate configured workflows
docker compose exec backend python manage.py validate_workflows

# Rebuild only the frontend
docker compose build frontend
docker compose up -d frontend

# Build the frontend outside Docker
cd frontend
npm ci
npm run build
```

## Data seeding and reset

The aggregate seed command is [seed_platform.py](./backend/service_api/management/commands/seed_platform.py). It loads RBAC, base data, MDAs, priority and cradle-to-death services, registry adapters, schemas, workflows, and demo users in the required order.

```bash
# Rerun the complete idempotent POC seed
docker compose exec backend python manage.py seed_platform

# Seed only roles
docker compose exec backend python manage.py seed_rbac_roles

# Seed only demo users
docker compose exec backend python manage.py seed_demo_users

# Seed registry adapters
docker compose exec backend python manage.py seed_registry_adapters

# Add missing schemas
docker compose exec backend python manage.py seed_missing_schemas
```

The seeded role and user definitions are maintained in:

- [RBAC role seed](./backend/service_api/management/commands/seed_rbac_roles.py)
- [Demo user seed](./backend/service_api/management/commands/seed_demo_users.py)

To clear service requests, workflow executions, payments, and audit activity while preserving configuration and users:

```bash
docker compose exec backend python manage.py reset_demo_environment --force
```

> [!CAUTION]
> The reset command deletes dynamic POC transaction data. Never run it against an environment whose data must be retained.

## Developer code map

### Backend

| Area | File or directory |
|---|---|
| Django settings and security | [backend/project/settings.py](./backend/project/settings.py) |
| Root routes and health endpoints | [backend/project/urls.py](./backend/project/urls.py) |
| Celery configuration | [backend/project/celery.py](./backend/project/celery.py) |
| Core data model | [backend/service_api/models.py](./backend/service_api/models.py) |
| API viewsets and endpoints | [backend/service_api/views.py](./backend/service_api/views.py) |
| API routes | [backend/service_api/urls.py](./backend/service_api/urls.py) |
| Workflow execution engine | [backend/service_api/workflow.py](./backend/service_api/workflow.py) |
| Registry, payment and consent services | [backend/service_api/services.py](./backend/service_api/services.py) |
| Permission policies | [backend/service_api/permissions.py](./backend/service_api/permissions.py) |
| Background tasks | [backend/service_api/tasks.py](./backend/service_api/tasks.py) |
| EDRMS application | [backend/apps/document_repository](./backend/apps/document_repository/) |
| Backend tests | [backend/service_api/tests](./backend/service_api/tests/) |
| Python dependencies | [backend/requirements.txt](./backend/requirements.txt) |

### Frontend

| Area | File or directory |
|---|---|
| Application shell and global navigation | [frontend/src/App.vue](./frontend/src/App.vue) |
| Routes and access guards | [frontend/src/router/index.js](./frontend/src/router/index.js) |
| Authentication state | [frontend/src/store/auth.js](./frontend/src/store/auth.js) |
| Login and POC role access | [frontend/src/views/LoginView.vue](./frontend/src/views/LoginView.vue) |
| Role dashboards and architecture navigation | [frontend/src/views/DashboardView.vue](./frontend/src/views/DashboardView.vue) |
| Workflow and dynamic-form administration | [ServiceConfigManager.vue](./frontend/src/components/Admin/ServiceConfigManager.vue) |
| DPI gateway, payments and shared rails | [ApiRegistry.vue](./frontend/src/components/Admin/ApiRegistry.vue) |
| Consent, identity and trust controls | [SecurityTrustView.vue](./frontend/src/components/Admin/SecurityTrustView.vue) |
| Registry and adapter monitoring | [RegistriesMonitor.vue](./frontend/src/components/Admin/RegistriesMonitor.vue) |
| EDRMS user interface | [frontend/src/modules/repository](./frontend/src/modules/repository/) |
| Frontend dependencies and scripts | [frontend/package.json](./frontend/package.json) |

### Infrastructure

| Area | File |
|---|---|
| Local Docker Compose | [docker-compose.yml](./docker-compose.yml) |
| Production Docker Compose | [docker-compose.prod.yml](./docker-compose.prod.yml) |
| Environment template | [.env.production.example](./.env.production.example) |
| Development backend image | [docker/dev/backend/Dockerfile](./docker/dev/backend/Dockerfile) |
| Development frontend image | [docker/dev/frontend/Dockerfile](./docker/dev/frontend/Dockerfile) |
| Development Nginx proxy | [docker/dev/nginx/default.conf](./docker/dev/nginx/default.conf) |
| Production backend image | [docker/prod/backend/Dockerfile](./docker/prod/backend/Dockerfile) |
| Production frontend image | [docker/prod/frontend/Dockerfile](./docker/prod/frontend/Dockerfile) |
| Production Docker gateway | [docker/prod/nginx/default.conf](./docker/prod/nginx/default.conf) |
| Internal frontend Nginx | [docker/prod/nginx/frontend.conf](./docker/prod/nginx/frontend.conf) |
| Host HTTPS configuration | [docker/prod/nginx/host-gokservices.bitz-itc.com.conf](./docker/prod/nginx/host-gokservices.bitz-itc.com.conf) |

## Documentation library

### Product and technical specification

- [Project overview and concept note](./docs/poc/poc_project_overview_concept_note.md)
- [Functional and non-functional requirements](./docs/poc/poc_functional_non_functional_requirements.md)
- [System design](./docs/poc/poc_system_design_documents.md)
- [Test and validation plan](./docs/poc/poc_test_validation_plan.md)

### Architecture and implementation

- [GEA-aligned target architecture](./docs/architecture/architecture_three.md)
- [Workflow engine and algorithm](./docs/architecture/poc_algorithm_workflow_documentation.md)
- [Configurable workflows](./docs/architecture/CONFIGURABLE_WORKFLOWS_COMPLETE.md)
- [BPMN workflow enhancements](./docs/architecture/BPMN_WORKFLOW_ENHANCEMENT.md)
- [RBAC implementation](./docs/architecture/RBAC_IMPLEMENTATION_SUMMARY.md)
- [All service forms and schemas](./docs/exports/ALL_SERVICES_FORMS_COMPLETE.md)
- [Catalogue verification export](./docs/exports/verify_catalogue_data.html)

### Deployment and integration

- [Production deployment runbook](./docs/guides/DEPLOYMENT.md)
- [POC deployment and DevOps plan](./docs/guides/poc_deployment_dev_ops_plan.md)
- [Huduma Bridge instructions](./docs/guides/huduma_bridge_instructions.md)
- [Frontend cache troubleshooting](./docs/guides/FRONTEND_CACHE_ISSUE.md)

### Reports and handover evidence

- [Comprehensive POC report](./docs/reports/ICTA_POC_Comprehensive_Report.md)
- [World Bank consolidated actions](./docs/reports/ICTA_WB_CONSOLIDATED_ACTIONS.md)
- [Meeting actions](./docs/reports/ICTA_MEETING_ACTIONS.md)
- [POC report outline](./docs/reports/POC_Report_Outline.md)

### UI standards

- [BEM UI documentation](./docs/style-guide/BEM-DOCUMENTATION.md)
- [BEM quick reference](./docs/style-guide/BEM-QUICK-REFERENCE.md)
- [BEM transformation comparison](./docs/style-guide/BEM-TRANSFORMATION-COMPARISON.md)
- [Style-guide overview](./docs/style-guide/README-BEM.md)

When an authoritative document under `docs/` changes, update its corresponding copy under `frontend/public/docs/` when that document is rendered in the Technical Evidence screen.

## Production deployment

Use the full [production deployment guide](./docs/guides/DEPLOYMENT.md). The production path is:

```bash
cp .env.production.example .env
# Replace every placeholder and keep .env private.

docker compose -f docker-compose.prod.yml config --quiet
docker compose -f docker-compose.prod.yml build --pull
docker compose -f docker-compose.prod.yml up -d
```

Install [host-gokservices.bitz-itc.com.conf](./docker/prod/nginx/host-gokservices.bitz-itc.com.conf) on the server after issuing the TLS certificate. Host Nginx proxies HTTPS traffic to the loopback-only Docker gateway at `127.0.0.1:8087`.

Production verification:

```bash
curl -I http://gokservices.bitz-itc.com/
curl -fsS https://gokservices.bitz-itc.com/health
curl -fsS https://gokservices.bitz-itc.com/ready
```

The production guide also covers TLS issuance, secrets, backups, routine updates, rollback, monitoring, and POC exposure controls.

## Quality and security checks

Before handing over a change:

```bash
docker compose exec backend python manage.py check
docker compose exec backend python manage.py test
docker compose exec backend python manage.py validate_workflows

cd frontend
npm ci
npm run build
npm audit --omit=dev

cd ..
docker compose -f docker-compose.prod.yml config --quiet
docker compose -f docker-compose.prod.yml build
git diff --check
```

At the time of the latest production review, the images build successfully, Django checks pass, and the supplied host Nginx file passes syntax validation. The frontend dependency audit still reports high-severity advisories in the current lockfile; resolve and regression-test those upgrades before treating the POC as security-cleared for unrestricted public access.

## Troubleshooting

```bash
# Service state
docker compose ps

# Backend startup, migration or seeding failures
docker compose logs --tail=250 backend

# Frontend build or Vite failures
docker compose logs --tail=250 frontend

# Celery and Redis connectivity
docker compose logs --tail=250 celery_worker redis

# Validate resolved development configuration
docker compose config --quiet

# Restart without deleting data
docker compose restart
```

Do not use `docker compose down -v` unless permanent deletion of the database and other persisted volumes is explicitly intended.

## Suggested developer handover sequence

1. Read the product overview, requirements, system design, and target architecture from the **Start here** table.
2. Start the local stack and confirm `/health`, `/ready`, login, one citizen journey, one officer action, and one admin configuration change.
3. Review the backend and frontend code maps before changing a capability.
4. Update the canonical seed command whenever a new required role, service, workflow, registry, or demo user is introduced.
5. Add or update backend tests and run the quality checks above.
6. Keep canonical docs and their rendered `frontend/public/docs/` copies aligned.
7. Follow the production runbook for deployment; do not improvise ports, secrets, TLS, or Nginx configuration.
