#!/bin/bash
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Seeding database..."
python seed_data.py
python seed_catalogue_master.py
python seed_rbac_roles.py
python seed_demo_users.py
python seed_test_data.py

echo "Starting server..."
exec "$@"
