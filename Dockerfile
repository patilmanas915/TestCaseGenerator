# Render-optimized Docker configuration for Python 3.11
FROM python:3.11.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies including build tools for pandas
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install compatible build tools
RUN python -m pip install --upgrade pip==24.0
RUN pip install setuptools==69.5.1 wheel==0.43.0

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with no cache to save space
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories with proper permissions
RUN mkdir -p uploads downloads logs /tmp/uploads /tmp/downloads
RUN chmod 755 uploads downloads logs /tmp/uploads /tmp/downloads

# Set environment variables for Render
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV RENDER=true

# Expose port (Render will provide the PORT env var)
EXPOSE $PORT

# Health check for Render
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# Run the application with Gunicorn (optimized for Render)
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 300 --max-requests 1000 app:app"]
