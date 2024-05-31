#!/bin/sh

# Exit if any command fails
set -e

echo "Waiting for PostgresSQL to start... Scheduler"
/BookStore/entrypoints/wait-for-it.sh db:5432 --timeout=30 -- echo "PostgresSQL started"

# Start Celery Beat scheduler
echo "Starting Celery Beat Scheduler"
exec celery -A BookStore beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler