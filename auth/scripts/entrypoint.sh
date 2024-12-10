#!/bin/bash
set -e

# Wait for database to be ready
echo "Waiting for MySQL to be ready..."
while ! nc -z auth-db 3306; do
  sleep 1
done
echo "MySQL is ready!"

# Initialize database
echo "Creating database tables..."
python init_db.py

# Start the FastAPI application
echo "Starting FastAPI application..."
uvicorn main:app --host 0.0.0.0 --port 8000 