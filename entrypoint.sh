#!/bin/bash
set -e

echo "🔁 Running migrations..."
django-admin migrate --settings=$DJANGO_SETTINGS_MODULE --noinput

echo "📦 Collecting static files..."
django-admin collectstatic --settings=$DJANGO_SETTINGS_MODULE --noinput

#echo "🌍 Compiling translation messages..."
#django-admin compilemessages --settings=$DJANGO_SETTINGS_MODULE

echo "🚀 Starting Gunicorn..."
python -m gunicorn --bind=0.0.0.0 --timeout 600 portauthority.wsgi
