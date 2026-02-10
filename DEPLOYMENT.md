# Deployment Guide: GOK Repeatable Services Platform

This document provides step-by-step instructions for deploying the GOK Repeatable Services Platform in both local development and production environments.

---

## 1. Local Development Setup (Docker)

The fastest way to get the platform running is using **Docker Compose**. This spins up the Backend (Django), Frontend (Vue), Database (PostgreSQL), and Cache (Redis).

### **Prerequisites**
- Docker & Docker Compose installed.
- Access to the repository.

### **Steps**
1. **Clone & Enter Directory:**
   ```bash
   git clone <repository_url>
   cd ictapoc
   ```

2. **Environment Configuration:**
   Create a `.env` file in the root:
   ```bash
   POSTGRES_DB=icta_db
   POSTGRES_USER=icta_user
   POSTGRES_PASSWORD=icta_pass
   SECRET_KEY=dev_secret_key
   DEBUG=True
   ```

3. **Build & Start Containers:**
   ```bash
   docker-compose build
   docker-compose up -d
   ```

4. **Initialize Database:**
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

5. **Seed Demo Data:**
   Load the Ministries (MDAs) and sample Service Configurations:
   ```bash
   docker-compose exec backend python manage.py loaddata mda_seed_data.json
   docker-compose exec backend python manage.py loaddata service_config_seed_data.json
   ```

6. **Access the App:**
   - **Frontend:** [http://localhost](http://localhost) (via Nginx proxy)
   - **Backend API:** [http://localhost:8001/api](http://localhost:8001/api)

---

## 2. Production Deployment

For a GOK-ready production environment, follow these architectural best practices.

### **A. Infrastructure Requirements**
- **Compute:** AWS EC2, Azure VM, or Local Data Center.
- **Database:** Managed PostgreSQL (e.g., RDS) for reliability.
- **Reverse Proxy:** The included `nginx` container should be updated to handle **SSL (HTTPS)** via Certbot/Let's Encrypt.

### **B. Production Configuration**
1. **Security:**
   - Change `DEBUG=False` in `.env`.
   - Generate a strong `SECRET_KEY`.
   - Restrict `ALLOWED_HOSTS` to your domain.

2. **Application Server:**
   - Use `gunicorn` to serve the Django application (already in `requirements.txt`).
   - Run gunicorn via the backend container command.

3. **Asset Serving:**
   - Use `nginx` to serve the static Vue.js build files.
   - Run `npm run build` in the frontend and map the `dist/` folder to Nginx.

4. **Background Tasks:**
   - Ensure the **Celery Worker** is running to handle SLA escalations and notifications.
   - Command: `celery -A project worker -l info`.

---

## 3. Post-Deployment Verification
Run these checks to ensure the system is functional:
- [ ] **Login:** Can a user log in via the Frontend?
- [ ] **Submission:** Can a Citizen submit a "Birth Registration" request?
- [ ] **Workflow:** Does an Officer see the pending task in their dashboard?
- [ ] **Audit:** Does the Admin view show the step-by-step audit logs?

---
*Created by Loshie (AI Assistant)*
