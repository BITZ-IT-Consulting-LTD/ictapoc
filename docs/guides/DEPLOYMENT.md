# Production Deployment Guide

This runbook deploys the GoK Repeatable Services Platform POC at:

**https://gokservices.bitz-itc.com/**

It assumes one Linux host running Docker Compose and host-level Nginx. Host Nginx terminates TLS and proxies to the container gateway on `127.0.0.1:8087`. PostgreSQL, Redis, Django, Celery, and the frontend remain isolated on the Docker network.

## 1. Production topology

```text
Internet
   |
   | HTTPS :443
   v
Host Nginx
   |
   | HTTP 127.0.0.1:8087
   v
Docker Nginx
   |-- /api, /admin, /health, /ready --> Django + Gunicorn
   |-- /static                         --> collected Django assets
   |-- protected documents             --> EDRMS media volume
   `-- all other routes                 --> Vue frontend

Django --> PostgreSQL
Django/Celery --> authenticated Redis
```

Only ports 80 and 443 should be publicly reachable. The Docker gateway is deliberately bound to loopback.

## 2. Server and DNS prerequisites

Minimum recommended POC host:

- Ubuntu 22.04 or 24.04 LTS
- 2 vCPU, 4 GB RAM, and 30 GB persistent disk
- Docker Engine with the Compose plugin
- Nginx and Certbot installed on the host
- DNS `A` record for `gokservices.bitz-itc.com` pointing to the host IPv4 address
- Optional DNS `AAAA` record only when IPv6 is configured on the host
- Inbound TCP 80 and 443 allowed by the cloud firewall and host firewall

Verify DNS before requesting a certificate:

```bash
dig +short gokservices.bitz-itc.com A
```

## 3. Install runtime dependencies

Install Docker from Docker's official repository, then install host Nginx and Certbot:

```bash
sudo apt update
sudo apt install -y nginx certbot
sudo systemctl enable --now nginx
docker --version
docker compose version
```

Add the deployment user to the Docker group if required, then start a new shell session:

```bash
sudo usermod -aG docker "$USER"
```

## 4. Clone and configure the application

```bash
sudo mkdir -p /opt/gokservices
sudo chown "$USER":"$USER" /opt/gokservices
git clone https://github.com/BITZ-IT-Consulting-LTD/ictapoc.git /opt/gokservices/app
cd /opt/gokservices/app
```

Create the untracked production environment file from the committed template:

```bash
cp .env.production.example .env
chmod 600 .env
```

Generate independent random values for the database, Redis, Django, and JWT secrets:

```bash
openssl rand -hex 32
openssl rand -hex 50
```

Edit `.env` and replace every `REPLACE_WITH_...` value. The production host values must include:

```dotenv
DEBUG=False
ALLOWED_HOSTS=gokservices.bitz-itc.com,localhost,127.0.0.1,backend
POSTGRES_HOST=db
POSTGRES_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
USE_X_ACCEL_REDIRECT=True
```

Never commit `.env` or paste its contents into tickets, chat, or deployment logs.

## 5. Issue the TLS certificate

The committed final Nginx configuration references the Let's Encrypt certificate, so issue it before enabling that configuration. On a new single-purpose host:

```bash
sudo systemctl stop nginx
sudo certbot certonly --standalone \
  --domain gokservices.bitz-itc.com \
  --agree-tos \
  --no-eff-email \
  --email YOUR_OPERATIONS_EMAIL
sudo systemctl start nginx
```

If the host already serves other sites, use Certbot's webroot or Nginx workflow instead of stopping Nginx.

Confirm the certificate exists:

```bash
sudo test -f /etc/letsencrypt/live/gokservices.bitz-itc.com/fullchain.pem
sudo test -f /etc/letsencrypt/live/gokservices.bitz-itc.com/privkey.pem
```

## 6. Install the host Nginx configuration

The production host configuration is committed at:

`docker/prod/nginx/host-gokservices.bitz-itc.com.conf`

Install and enable it:

```bash
sudo mkdir -p /var/www/certbot
sudo cp docker/prod/nginx/host-gokservices.bitz-itc.com.conf \
  /etc/nginx/sites-available/gokservices.bitz-itc.com.conf
sudo ln -sfn /etc/nginx/sites-available/gokservices.bitz-itc.com.conf \
  /etc/nginx/sites-enabled/gokservices.bitz-itc.com.conf
sudo nginx -t
sudo systemctl reload nginx
```

The configuration provides:

- HTTP-to-HTTPS redirection
- TLS 1.2 and TLS 1.3
- HSTS and baseline response security headers
- Forwarded host, client IP, and HTTPS scheme headers for Django
- 100 MB request bodies for EDRMS document uploads
- Five-minute upstream timeouts for large document operations
- A persistent ACME challenge path for certificate renewal

## 7. Build and start the production stack

Validate the resolved Compose configuration without printing it into shared logs because it contains secret environment values:

```bash
docker compose -f docker-compose.prod.yml config --quiet
```

Build and start:

```bash
docker compose -f docker-compose.prod.yml build --pull
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml ps
```

The backend entrypoint automatically runs database migrations, collects Django static files, and seeds the POC platform and EDRMS data. The seeding commands are designed for this demonstration environment.

Review startup logs:

```bash
docker compose -f docker-compose.prod.yml logs --tail=200 backend
docker compose -f docker-compose.prod.yml logs --tail=100 celery
docker compose -f docker-compose.prod.yml logs --tail=100 nginx
```

## 8. Verification

Run these checks from the host:

```bash
curl -I http://gokservices.bitz-itc.com/
curl -fsS https://gokservices.bitz-itc.com/health
curl -fsS https://gokservices.bitz-itc.com/ready
curl -I https://gokservices.bitz-itc.com/login
```

Expected results:

- HTTP redirects to HTTPS.
- `/health` returns a successful liveness response.
- `/ready` confirms application dependencies are ready.
- `/login` returns the Vue application.
- `/admin/` loads with Django Admin styling.
- EDRMS previews and downloads work through Nginx protected-media delivery.

Inspect the certificate and public TLS path:

```bash
openssl s_client -connect gokservices.bitz-itc.com:443 \
  -servername gokservices.bitz-itc.com </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates
```

## 9. POC exposure warning

This repository intentionally seeds demonstration accounts and displays quick-access login buttons. Before exposing the site beyond an approved POC audience:

- Change all seeded account passwords.
- Restrict access at the firewall, VPN, or host Nginx when possible.
- Do not use real citizen records, credentials, payment information, or classified documents.
- Replace mocked registry, identity, payment, and KeSEL connections before treating the platform as production infrastructure.
- Configure a real email provider and operational alerting.

## 10. Routine deployment update

Back up the database before every application update:

```bash
cd /opt/gokservices/app
mkdir -p backups
set -a
. ./.env
set +a
docker compose -f docker-compose.prod.yml exec -T db \
  pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc \
  > "backups/gokservices-$(date +%Y%m%d-%H%M%S).dump"
```

Deploy the update:

```bash
git fetch origin
git pull --ff-only
docker compose -f docker-compose.prod.yml build --pull
docker compose -f docker-compose.prod.yml up -d --remove-orphans
docker compose -f docker-compose.prod.yml ps
curl -fsS https://gokservices.bitz-itc.com/ready
```

## 11. Backup and restore

Database backup:

```bash
docker compose -f docker-compose.prod.yml exec -T db \
  pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc > backup.dump
```

EDRMS media-volume backup:

```bash
docker compose -f docker-compose.prod.yml exec -T backend \
  tar -czf - -C /app/media . \
  > "backups/edrms-media-$(date +%Y%m%d-%H%M%S).tar.gz"
```

Store backups off-host and test restoration periodically. A database restore should be rehearsed on a separate environment before it is needed in an incident.

## 12. Rollback

Application rollback:

```bash
git log --oneline -10
git checkout SAFE_COMMIT_OR_TAG
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d
curl -fsS https://gokservices.bitz-itc.com/ready
```

Do not reverse a database migration without reviewing that migration's data effects. Restore the matching database backup when code and schema are no longer compatible.

## 13. Operations

Useful commands:

```bash
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f --tail=200
docker compose -f docker-compose.prod.yml restart nginx
docker compose -f docker-compose.prod.yml exec backend python manage.py check
sudo nginx -t
sudo journalctl -u nginx --since "30 minutes ago"
```

Verify automatic certificate renewal:

```bash
sudo certbot renew --dry-run
systemctl list-timers | grep certbot
```

The production database, Redis data, collected static files, and EDRMS media are stored in named Docker volumes. Never run `docker compose down -v` on the production host unless permanent data deletion is explicitly intended.
