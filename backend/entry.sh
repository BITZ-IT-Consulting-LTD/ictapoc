#!/bin/bash
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Seeding database..."
python seed_data.py

echo "🚀 Seeding optimized Cradle to Death Citizen Lifecycle journey..."
python seed_unified_catalogue.py

python seed_rbac_roles.py
python seed_demo_users.py
python seed_registry_adapters.py
python seed_registry_operations.py
python seed_test_data.py

echo "Starting server..."
exec "$@"
