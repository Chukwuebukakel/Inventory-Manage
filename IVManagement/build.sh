#!/bin/bash

echo "🚀 Starting Deployment..."

# Exit on error
set -e

# Activate virtual environment (if applicable)
if [ -d "venv" ]; then
    echo "🔹 Activating virtual environment..."
    source venv/bin/activate
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Apply database migrations
echo "🔄 Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "🖼️ Collecting static files..."
python manage.py collectstatic --noinput

# Restart Gunicorn server
echo "🚀 Restarting Gunicorn server..."
pkill gunicorn || true  # Stop existing Gunicorn processes
gunicorn -k uvicorn.workers.UvicornWorker myapp.asgi:application --bind 0.0.0.0:8000 --daemon

echo "✅ Deployment Completed Successfully!"
