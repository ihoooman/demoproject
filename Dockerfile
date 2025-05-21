FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=LastDjangoProject.settings
ARG ALLOWED_HOSTS
ENV ALLOWED_HOSTS=$ALLOWED_HOSTS

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user
RUN adduser --disabled-password --gecos "" appuser

# Copy project
COPY . .

# Add STATIC_ROOT setting to Django settings
RUN echo "STATIC_ROOT = '/app/staticfiles'" >> LastDjangoProject/settings.py

# Collect static files
RUN mkdir -p /app/staticfiles && \
    python manage.py collectstatic --noinput

# Change ownership of all files to the non-root user
RUN chown -R appuser:appuser /app
RUN echo $ALLOWED_HOSTS

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run the application using gunicorn instead of the development server
CMD ["gunicorn", "LastDjangoProject.wsgi", "--bind", "0.0.0.0:8000"]