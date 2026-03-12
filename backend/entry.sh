#!/bin/bash
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Seeding platform data..."
python manage.py seed_platform

echo "Seeding Document Repository data..."
python seed_document_repository.py

echo "Seeding additional DRMS architecture..."
python seed_drms.py

echo "Starting server..."
exec "$@"
