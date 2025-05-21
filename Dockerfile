FROM python:3.11-slim

# Set environment vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=LastDjangoProject.settings

# Workdir
WORKDIR /app

# System deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy start script and make executable (as root)
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Copy project files
COPY . /app

# Add STATIC_ROOT to settings.py if not present
RUN grep -qx "STATIC_ROOT" LastDjangoProject/settings.py || \
    echo "STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')" >> LastDjangoProject/settings.py

# Create non-root user and chown everything
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /app

# Switch to non-root
USER appuser

# Expose port
EXPOSE 8000

# Use start.sh to run migrations, collectstatic and start Gunicorn
ENTRYPOINT ["/app/start.sh"]