#!/bin/sh

# Exit if any command fails
set -e

echo "Waiting for PostgresSQL to start..."
/BookStore/entrypoints/wait-for-it.sh db:5432 --timeout=30 -- echo "PostgresSQL started"

# Make database migrations
echo "Making database migrations"
python manage.py makemigrations --noinput

# Run database migrations
echo "Running database migrations"
python manage.py migrate --noinput

echo "Running Test on APIs"
python manage.py test

# Collect static files
#echo "Collecting static files"
#python manage.py collectstatic --noinput --clear


# Check if in development environment and seed data
if [ "$FAKEDATA" = "True" ]; then
    echo "Seeding database with fake data"
    python manage.py spawn_fake_data --users=50 --entities_per_user=20
fi


# Start Gunicorn server
echo "Starting Gunicorn server"
exec gunicorn --bind 0.0.0.0:8000 BookStore.asgi -w 4 -k uvicorn.workers.UvicornWorker
