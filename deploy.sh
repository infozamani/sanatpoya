#!/bin/bash

# Exit on any error
set -e

# Variables
PROJECT_DIR="/root/zamani/project_sanatpoya-"       # Update this to your project's path
REPO_BRANCH="main"                       # Update this to your repository branch if different
STATIC_TARGET_DIR="/var/www/sanatpoya/staticfiles/"
MEDIA_TARGET_DIR="/var/www/sanatpoya/media/"
NGINX_SERVICE="nginx"
GUNICORN_SERVICE="gunicorn"

echo "Starting deployment script..."

# Step 1: Navigate to the project directory
cd "$PROJECT_DIR"
echo "Changed directory to $PROJECT_DIR"

# Step 2: Pull the latest changes from the repository
echo "Pulling latest changes from branch $REPO_BRANCH..."
git fetch origin
git pull origin "$REPO_BRANCH"

# Step 3: Install or update dependencies (optional, if needed)
echo "Installing dependencies..."
source venv/bin/activate    # Activate your virtual environment
pip install -r sanatpoya/requirements.txt

# Step 4: Migrate and Collect static files
echo "Migrating and Collecting static files..."
DJANGO_ENV=production python sanatpoya/manage.py makemigrations --noinput
DJANGO_ENV=production python sanatpoya/manage.py migrate --noinput
DJANGO_ENV=production python sanatpoya/manage.py collectstatic --noinput

# Step 7: Restart Gunicorn and Nginx services
echo "Restarting Gunicorn and Nginx services..."
sudo systemctl restart "$GUNICORN_SERVICE"
sudo systemctl restart "$NGINX_SERVICE"

echo "Deployment completed successfully!"