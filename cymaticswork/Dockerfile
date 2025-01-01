FROM python:3.9

WORKDIR /app

# Copy requirements first for better caching
COPY cymaticswork/requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy project files
COPY cymaticswork/ .

# Collect static files and run migrations
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate --noinput

# Command to run the application
CMD ["gunicorn", "cymaticspro.wsgi", "--log-file", "-"]