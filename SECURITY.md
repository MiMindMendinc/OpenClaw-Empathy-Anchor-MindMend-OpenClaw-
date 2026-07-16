# Security

## Reporting

If you find a vulnerability, contact Michigan MindMend privately. Do not open a public issue with exploit details.

## Controls in this technical demonstration

| Control | Behavior |
|---------|----------|
| Demo auth gate | `/auth/login` requires `DEMO_AUTH=true` |
| Production secrets | `FLASK_ENV=production` rejects missing/demo `JWT_SECRET_KEY` |
| CORS | Explicit `CORS_ORIGINS` allow-list |
| Body/message limits | `MAX_CONTENT_LENGTH`, `MAX_MESSAGE_CHARS` |
| Rate limiting | Per-IP sliding window (`RATE_LIMIT_PER_MINUTE`) |
| Bind default | Python binds `127.0.0.1` unless `ALLOW_LAN_BIND=true` |
| Alert authz | Alerts scoped to JWT `user_id` |
| Raw text | Not stored/logged by default |
| Secure headers | nosniff, frame deny, referrer policy, no-store |
| Dependencies | Pinned in `backend/requirements.txt`; CI runs `pip-audit` / `npm audit` |

## Not claimed

- HIPAA compliance
- Formal penetration test
- Internet-facing production readiness

See [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md).
