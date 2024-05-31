#!/bin/sh

# Exit if any command fails
set -e

echo "Waiting for PostgresSQL to start... Celery"
/BookStore/entrypoints/wait-for-it.sh db:5432 --timeout=30 -- echo "PostgresSQL started"

# Start the Celery worker
echo "Starting Celery Worker"
exec celery -A BookStore worker -l DEBUG