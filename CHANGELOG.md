# Changelog

All notable changes to OpenClaw Empathy Anchor are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.0-local-safety-demo] - 2026-07-05

### Added
- SQLite alert persistence (`backend/alert_store.py`) for local-first parent/caregiver alerts
- `/demo` endpoint showing neutral, distress, crisis, night-mode, and geofence scan scenarios
- Demo authentication guardrails (`DEMO_AUTH`, production `JWT_SECRET_KEY` requirement)
- Python backend test suite expansion (auth, alerts, production config, demo route)
- CI jobs for Python tests and Docker health-check smoke test
- `CHANGELOG.md` and `RELEASE_CHECKLIST.md`
- README "Run the demo" section with curl examples and safety boundaries table

### Changed
- Docker now sets `PORT=8000` so Flask, healthcheck, and Compose agree
- Node.js standard normalized to **20 LTS** across package.json, Dockerfile, CI, and docs
- `/alerts` returns persisted alerts instead of a placeholder message
- `/chat` and `/location` save alerts to local SQLite when triggered
- Version bumped to `0.1.0`

### Security
- Production mode (`FLASK_ENV=production`) requires a non-default `JWT_SECRET_KEY`
- Demo login blocked in production unless `DEMO_AUTH=true` is explicitly set

### Documentation
- Safety wording tightened: supportive prototype, not clinical software, deterministic demo scanner
- Implemented vs roadmap table added to README

[0.1.0-local-safety-demo]: https://github.com/MiMindMendinc/OpenClaw-Empathy-Anchor-MindMend-OpenClaw-/releases/tag/v0.1.0-local-safety-demo
