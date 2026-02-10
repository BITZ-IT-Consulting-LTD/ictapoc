#!/bin/bash
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Seeding database..."
python seed_data.py

echo "Starting server..."
exec "$@"
