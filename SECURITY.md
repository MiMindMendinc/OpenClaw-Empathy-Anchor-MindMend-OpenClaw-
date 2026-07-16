# Security

OpenClaw Empathy Anchor is a **local-first demo**. Treat it as infrastructure for controlled demos, not a hardened multi-tenant SaaS.

## What is enforced today

| Control | Behavior |
|---------|----------|
| Demo auth gate | `/auth/login` only issues tokens when `DEMO_AUTH=true` |
| Production secrets | `FLASK_ENV=production` refuses missing or demo `JWT_SECRET_KEY` values |
| Local alerts | SQLite on-device (`ALERT_DB_PATH`) — no cloud sync in v0.1 |
| CORS | Explicit allow-list via `CORS_ORIGINS` (defaults to localhost:8000) |
| Offline default | `OFFLINE_MODE=true` — no required cloud inference path |
| Dependencies | `gunicorn>=22.0.0` in `backend/requirements.txt` (HTTP smuggling fixes) |

## What is intentionally demo-scoped

- `/auth/login` is **not** identity verification. It mints a JWT for any `user_id` when demo auth is on.
- Docker Compose uses `FLASK_ENV=development` and a local demo JWT secret.
- Crisis detection is a **deterministic keyword/pattern scanner**, not a clinical model.

## Production checklist (if you deploy beyond local demo)

1. Set a strong `JWT_SECRET_KEY` (`python -c "import secrets; print(secrets.token_hex(32))"`)
2. Set `DEMO_AUTH=false` and replace `/auth/login` with real identity verification
3. Set `FLASK_ENV=production`
4. Restrict `CORS_ORIGINS` to your real frontend origins
5. Terminate TLS at a reverse proxy
6. Keep alert DB on encrypted local storage if the host is shared

## Reporting

If you find a vulnerability, contact Michigan MindMend privately. Do not open a public issue with exploit details.
