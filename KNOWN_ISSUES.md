# Known Issues and Resolutions

## Node.js Version Requirements

### Standard
This project targets **Node.js 20 LTS** (`>=20.0.0`).

- `package.json` engines: `>=20.0.0`
- Docker builder image: `node:20-slim`
- CI matrix: Node 20.x

Node 18 is no longer tested in CI. Node 22 may work but is not the documented standard unless OpenClaw CLI dependencies require it in your environment.

### Resolution
Install Node.js 20 LTS from [nodejs.org](https://nodejs.org/) or use your system package manager.

## Security Warnings During Installation

### Issue
`npm install` may show security warnings about vulnerabilities in transitive dependencies when optional OpenClaw CLI packages are present.

### Resolution
**No action required for core empathy-anchor functionality.**

The empathy-anchor skill uses Node.js built-in modules and operates independently of deep OpenClaw dependency chains.

## Demo Authentication

### Issue
`/auth/login` issues a JWT for any `user_id` when `DEMO_AUTH=true`. This is intentional demo behavior, not production authentication.

### Resolution
- For local demos: leave `DEMO_AUTH=true` (default in Docker Compose)
- For production: set `DEMO_AUTH=false`, require `JWT_SECRET_KEY`, and implement proper identity verification

## Alert Storage

Alerts are persisted locally in SQLite (`data/alerts.db` by default). No cloud sync is included in v0.1.

## Summary

**For local demo usage:**
- Node 20 LTS recommended
- `npm install && npm test` for the empathy layer
- `docker compose up --build` for the full backend demo
- Alerts persist locally in SQLite

**For production deployment:**
- Set a strong `JWT_SECRET_KEY`
- Disable `DEMO_AUTH` unless running a controlled demo
- Review [SECURITY.md](SECURITY.md) and [docs/clinical-boundaries.md](docs/clinical-boundaries.md)
