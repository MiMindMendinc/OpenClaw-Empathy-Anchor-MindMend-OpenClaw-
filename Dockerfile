# Multi-stage Dockerfile for OpenClaw Empathy Anchor
# Supports arm64 for Raspberry Pi, non-root user, minimal image

# Python dependencies builder
FROM python:3.11-slim AS python-builder
WORKDIR /build
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --target=/python-deps -r requirements.txt

# Runtime image (Flask backend only — Node empathy layer runs outside Docker)
FROM python:3.11-slim AS runtime
# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN useradd -m -u 1001 appuser && chown -R appuser:appuser /home/appuser

# Set working directory
WORKDIR /app

# Copy Python dependencies
COPY --from=python-builder /python-deps /usr/local/lib/python3.11/site-packages

# Copy application code
COPY . .

# Ensure models and data directories exist
RUN mkdir -p models data/journals data

# Change ownership to appuser
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Flask listens on PORT (default 8000 in container)
ENV PORT=8000
ENV OFFLINE_MODE=true
ENV DEMO_AUTH=true
ENV ALERT_DB_PATH=/app/data/alerts.db
# Override JWT_SECRET_KEY at runtime for real deployments (required when FLASK_ENV=production)
ENV JWT_SECRET_KEY=demo-jwt-secret-change-for-real-deployments

# Expose port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the Flask backend
CMD ["python", "backend/app.py"]
