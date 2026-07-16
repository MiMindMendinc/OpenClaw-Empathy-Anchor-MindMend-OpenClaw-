# MindMend Empathy Anchor — local technical demonstration image
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
COPY backend ./backend
COPY showcase ./showcase
COPY docs ./docs
COPY package.json LICENSE ./

RUN mkdir -p models data/journals data \
    && chown -R appuser:appuser /app

USER appuser

ENV PORT=8000 \
    BIND_HOST=0.0.0.0 \
    ALLOW_LAN_BIND=true \
    OFFLINE_MODE=true \
    DEMO_AUTH=true \
    FLASK_ENV=development \
    STORE_RAW_MESSAGES=false \
    ALERT_RETENTION_DAYS=30 \
    ALERT_DB_PATH=/app/data/alerts.db \
    JWT_SECRET_KEY=local-demo-only-not-for-production \
    CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://127.0.0.1:8000/ready || exit 1

CMD ["python", "backend/app.py"]
