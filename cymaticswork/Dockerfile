# Start with a Python base image
FROM python:3.11.0

# Set working directory
WORKDIR /app

# Copy requirements first
COPY cymaticswork/requirements.txt /app/

# Install dependencies
RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

# Copy project files
COPY cymaticswork/ /app/

# Collect static files and run migrations
RUN python manage.py collectstatic --noinput && \
    python manage.py migrate --noinput

# Command to run the application
CMD ["gunicorn", "cymaticspro.wsgi", "--log-file", "-"]