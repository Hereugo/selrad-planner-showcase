#!/bin/sh

until cd /app
do
    echo "Waiting for server volume..."
done

python3 manage.py migrate --no-input

python3 manage.py collectstatic --no-input

# Check if DJANGO_DEBUG is set to "True"
if [ "$DJANGO_DEBUG" = "True" ]; then
    GUNICORN_LOG_LEVEL="debug"
else
    GUNICORN_LOG_LEVEL="info"
fi
GUNICORN_LOG_CLASS="rich.logging.RichHandler"

gunicorn config.wsgi:application \
         --bind 0.0:8000 \
         --workers 1 --threads 4 --timeout 600 \
         --log-level $GUNICORN_LOG_LEVEL \
         --access-logfile - \
         --error-logfile - \
         --capture-output
