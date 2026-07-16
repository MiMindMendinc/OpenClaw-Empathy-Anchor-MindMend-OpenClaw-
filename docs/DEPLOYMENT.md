# Deployment

## Local demo (recommended)

```bash
docker compose up --build
curl http://127.0.0.1:8000/ready
open http://127.0.0.1:8000/
```

Container listens on `0.0.0.0:8000` inside Docker so port publishing works. Treat published ports as local-demo exposure unless you add TLS.

## Python local (localhost bind)

```bash
cd backend
pip install -r requirements.txt
export DEMO_AUTH=true
export BIND_HOST=127.0.0.1
python app.py
```

## LAN bind (explicit)

```bash
export BIND_HOST=0.0.0.0
export ALLOW_LAN_BIND=true
# Warning: HTTP on a LAN is not encrypted. Put TLS termination in front for any shared network.
python app.py
```

## Data

- Alerts: `ALERT_DB_PATH` (default `data/alerts.db`)
- Backup: copy the SQLite file while the service is stopped
- Reset: delete the SQLite file
- Rollback: redeploy previous image tag / git tag and restore DB backup

## Production-like notes

This project is a **technical demonstration**. If you expose it beyond localhost:

1. Set a strong `JWT_SECRET_KEY`
2. Set `DEMO_AUTH=false` and replace demo login
3. Set `FLASK_ENV=production`
4. Restrict `CORS_ORIGINS`
5. Terminate TLS at a reverse proxy
6. Keep `STORE_RAW_MESSAGES=false` unless legally/operationally justified
