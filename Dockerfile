FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG=False

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user for security
RUN useradd -m -u 1000 webuser
RUN chown -R webuser:webuser /app
USER webuser

# Expose port
EXPOSE 8000

# Start server
CMD ["gunicorn", "job_portal.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]