# Threat model

Scope: local technical demonstration on a developer machine or controlled demo host.

## Assets

- Local SQLite alert database
- Demo JWT signing secret
- Submitted message content (transient; optionally retained)
- Availability of the local service

## Threats and mitigations

| Threat | Mitigation |
|--------|------------|
| Local attacker reads DB | OS file permissions; optional encrypted disk; no cloud sync |
| LAN eavesdropping | Bind `127.0.0.1` by default; require `ALLOW_LAN_BIND=true` for non-local bind; document TLS reverse proxy |
| Stolen demo JWT secret | Reject known demo secrets when `FLASK_ENV=production`; require strong `JWT_SECRET_KEY` |
| Malicious oversized input | `MAX_CONTENT_LENGTH`, `MAX_MESSAGE_CHARS` |
| Alert enumeration | Alerts scoped to authenticated `user_id` |
| Dependency compromise | Pinned requirements; CI dependency audit |
| DoS via request floods | Basic per-IP rate limit |
| Log exposure of sensitive text | Raw messages not logged by default |
| Admin wipe abuse | Reset scoped to authenticated user's alerts |

## Out of scope (for this prototype)

- Multi-tenant SaaS isolation
- Formal penetration test
- HIPAA / clinical compliance programs
