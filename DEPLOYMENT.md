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

For a GOK-ready production environment, we use a dedicated `docker-compose.prod.yml` which sets up:
1.  **Backend:** Gunicorn application server with static file collection.
2.  **Frontend/Nginx:** An internal Nginx container that serves the built Vue.js assets and proxies API requests.
3.  **Database & Cache:** PostgreSQL and Redis.

### **Steps**

1.  **Configure Environment:**
    Ensure your `.env` file has production settings. **Critical**: Set hosts to service names.
    ```bash
    POSTGRES_DB=icta_db
    POSTGRES_USER=icta_user
    POSTGRES_PASSWORD=secure_password
    POSTGRES_HOST=db
    
    REDIS_HOST=redis
    REDIS_PORT=6379
    
    SECRET_KEY=long_random_secret_key
    DEBUG=False
    ALLOWED_HOSTS=yourdomain.com,localhost,127.0.0.1
    ```

2.  **Build and Run:**
    Use the production compose file:
    ```bash
    docker-compose -f docker-compose.prod.yml up -d --build
    ```

    *This command will:*
    - Build the Vue frontend (multi-stage build).
    - Build the Django backend and install Gunicorn.
    - Start the Internal Nginx (Port 80).
    - Run `collectstatic` automatically on startup.

3.  **Host Nginx Configuration (External):**
    The user requested an "Internal Nginx" to communicate with the "Host Nginx".
    The container `nginx` exposes Port 80.
    
    Configure your **Host** Nginx to proxy to this container:
    ```nginx
    server {
        listen 80;
        server_name yourdomain.com;
    
        location / {
            proxy_pass http://localhost:80;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
    ```

4.  **Verification:**
    - Access `http://localhost` (or your domain).
    - Check API at `http://localhost/api/`.
    - Check Admin at `http://localhost/admin/`.

---

## 3. Post-Deployment Verification
Run these checks to ensure the system is functional:
- [ ] **Login:** Can a user log in via the Frontend?
- [ ] **Submission:** Can a Citizen submit a "Birth Registration" request?
- [ ] **Workflow:** Does an Officer see the pending task in their dashboard?
- [ ] **Audit:** Does the Admin view show the step-by-step audit logs?

---
*Created by Loshie (AI Assistant)*
