# Framework0 Enhanced Context Server Docker Image
# 
# This Dockerfile creates a production-ready container for the Framework0 
# Enhanced Context Server with all dependencies and optimizations.

FROM python:3.11-slim

# Metadata labels for the image
LABEL maintainer="Framework0 Team"
LABEL description="Framework0 Enhanced Context Server - Multi-protocol data sharing"
LABEL version="1.0.0"

# Environment variables for container configuration
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Context server specific environment variables
ENV CONTEXT_SERVER_HOST=0.0.0.0 \
    CONTEXT_SERVER_PORT=8080 \
    CONTEXT_LOG_LEVEL=INFO \
    CONTEXT_DASHBOARD_ENABLED=true \
    CONTEXT_WEBSOCKET_ENABLED=true

# Create non-root user for security
RUN groupadd --gid 1000 framework0 && \
    useradd --uid 1000 --gid framework0 --shell /bin/bash --create-home framework0

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        jq \
        && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=framework0:framework0 . .

# Create necessary directories with proper permissions
RUN mkdir -p /app/logs /app/data /app/configs && \
    chown -R framework0:framework0 /app

# Switch to non-root user
USER framework0

# Create default configuration if it doesn't exist
RUN python3 configs/server_config.py config create configs/default.json

# Expose the server port
EXPOSE 8080

# Health check to ensure server is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Default command to start the server
CMD ["python3", "server/enhanced_context_server.py", "--host", "0.0.0.0", "--port", "8080"]