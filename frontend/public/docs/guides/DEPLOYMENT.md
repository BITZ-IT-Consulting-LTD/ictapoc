# Production Deployment Guide

The production POC is deployed at:

**https://gokservices.bitz-itc.com/**

This rendered guide covers the deployment path. The repository's authoritative, operations-ready runbook is `docs/guides/DEPLOYMENT.md`, and the installable host configuration is `docker/prod/nginx/host-gokservices.bitz-itc.com.conf`.

## Production topology

```text
Internet :443
    |
Host Nginx (TLS termination)
    |
127.0.0.1:8087
    |
Docker Nginx
    |-- Django + Gunicorn
    |-- Vue frontend
    |-- Django static files
    `-- protected EDRMS media

Django --> PostgreSQL
Django/Celery --> authenticated Redis
```

Only host ports 80 and 443 are public. The container gateway is bound to loopback and is not directly accessible from the network.

## Prerequisites

- Ubuntu 22.04 or 24.04 LTS host
- Recommended POC baseline: 2 vCPU, 4 GB RAM, 30 GB disk
- Docker Engine and Docker Compose plugin
- Host Nginx and Certbot
- DNS `A` record for `gokservices.bitz-itc.com`
- Firewall access for TCP 80 and 443

Verify DNS:

```bash
dig +short gokservices.bitz-itc.com A
```

## Application installation

```bash
sudo mkdir -p /opt/gokservices
sudo chown "$USER":"$USER" /opt/gokservices
git clone https://github.com/BITZ-IT-Consulting-LTD/ictapoc.git /opt/gokservices/app
cd /opt/gokservices/app
cp .env.production.example .env
chmod 600 .env
```

Generate separate random values with `openssl rand -hex 32` and replace every placeholder in `.env`. Required host settings include:

```dotenv
DEBUG=False
ALLOWED_HOSTS=gokservices.bitz-itc.com,localhost,127.0.0.1,backend
POSTGRES_HOST=db
POSTGRES_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
USE_X_ACCEL_REDIRECT=True
```

Never commit or share the production `.env` file.

## TLS certificate

On a new single-purpose host, issue the certificate before enabling the final Nginx configuration:

```bash
sudo apt update
sudo apt install -y nginx certbot
sudo systemctl stop nginx
sudo certbot certonly --standalone \
  --domain gokservices.bitz-itc.com \
  --agree-tos \
  --no-eff-email \
  --email YOUR_OPERATIONS_EMAIL
sudo systemctl start nginx
```

Use Certbot's webroot or Nginx workflow if the host already serves other domains.

## Host Nginx

```bash
sudo mkdir -p /var/www/certbot
sudo cp docker/prod/nginx/host-gokservices.bitz-itc.com.conf \
  /etc/nginx/sites-available/gokservices.bitz-itc.com.conf
sudo ln -sfn /etc/nginx/sites-available/gokservices.bitz-itc.com.conf \
  /etc/nginx/sites-enabled/gokservices.bitz-itc.com.conf
sudo nginx -t
sudo systemctl reload nginx
```

The host configuration provides HTTPS redirection, TLS 1.2/1.3, forwarded HTTPS headers, baseline security headers, 100 MB EDRMS uploads, and extended document-operation timeouts.

## Start the stack

```bash
docker compose -f docker-compose.prod.yml config --quiet
docker compose -f docker-compose.prod.yml build --pull
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml ps
```

The backend startup applies migrations, collects Django static files, and seeds POC platform and EDRMS data. Review the logs:

```bash
docker compose -f docker-compose.prod.yml logs --tail=200 backend
docker compose -f docker-compose.prod.yml logs --tail=100 celery
docker compose -f docker-compose.prod.yml logs --tail=100 nginx
```

## Verification

```bash
curl -I http://gokservices.bitz-itc.com/
curl -fsS https://gokservices.bitz-itc.com/health
curl -fsS https://gokservices.bitz-itc.com/ready
curl -I https://gokservices.bitz-itc.com/login
sudo certbot renew --dry-run
```

Confirm that:

- HTTP redirects to HTTPS.
- Health and readiness checks succeed.
- Login and Django Admin load correctly.
- Django Admin static assets are styled.
- EDRMS previews, uploads, and protected downloads work.
- Payment, consent, workflow, and registry POC screens load after login.

## Updating the deployment

Create database and EDRMS backups first, then deploy:

```bash
cd /opt/gokservices/app
set -a
. ./.env
set +a
mkdir -p backups
docker compose -f docker-compose.prod.yml exec -T db \
  pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc \
  > "backups/gokservices-$(date +%Y%m%d-%H%M%S).dump"
docker compose -f docker-compose.prod.yml exec -T backend \
  tar -czf - -C /app/media . \
  > "backups/edrms-media-$(date +%Y%m%d-%H%M%S).tar.gz"
git pull --ff-only
docker compose -f docker-compose.prod.yml build --pull
docker compose -f docker-compose.prod.yml up -d --remove-orphans
curl -fsS https://gokservices.bitz-itc.com/ready
```

Never run `docker compose down -v` on the production host unless permanent deletion of PostgreSQL, Redis, and EDRMS data is explicitly intended.

## POC security warning

This POC intentionally includes seeded accounts and quick-access login buttons. Before exposure beyond an approved demonstration audience:

- Change seeded passwords.
- Restrict the host through a firewall, VPN, or Nginx access control where possible.
- Do not use real citizen, payment, credential, or classified information.
- Replace mocked KeSEL, registry, payment, and identity connections before treating the platform as production infrastructure.
- Configure production email delivery, monitoring, alerting, backup retention, and restore testing.
