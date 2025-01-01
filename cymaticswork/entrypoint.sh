#!/bin/bash
set -e

# Install Python and pip
apt-get update
apt-get install -y python3 python3-pip

# Install requirements
cd cymaticswork
pip install -r requirements.txt

# Run Django commands
python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Start gunicorn
gunicorn cymaticspro.wsgi --log-file -