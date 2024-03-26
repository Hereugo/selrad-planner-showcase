#!/bin/sh

until cd /app
do
    echo "Waiting for server volume..."
done

python3 manage.py migrate --no-input

gunicorn config.wsgi:application --bind 0.0:8000 --workers 4 --threads 4 --timeout 600 --log-level=debug --capture-output
