# OpenClaw Empathy Anchor — Flask backend image
# Local-first demo. Not a clinical product.

FROM python:3.11-slim AS python-builder
WORKDIR /build
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --target=/python-deps -r requirements.txt

FROM python:3.11-slim AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

RUN useradd -m -u 1001 appuser && chown -R appuser:appuser /home/appuser

WORKDIR /app

COPY --from=python-builder /python-deps /usr/local/lib/python3.11/site-packages
COPY . .

RUN mkdir -p models data/journals data \
    && chown -R appuser:appuser /app

USER appuser

ENV PORT=8000
ENV OFFLINE_MODE=true
ENV DEMO_AUTH=true
ENV FLASK_ENV=development
ENV ALERT_DB_PATH=/app/data/alerts.db
ENV JWT_SECRET_KEY=local-demo-only-not-for-production
ENV CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "backend/app.py"]
