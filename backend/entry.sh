#!/bin/bash
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Seeding platform data..."
python manage.py seed_platform

echo "Starting server..."
exec "$@"
