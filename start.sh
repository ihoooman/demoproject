#!/bin/bash
set -e

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
exec gunicorn LastDjangoProject.wsgi:application --bind 0.0.0.0:${PORT:-8000}