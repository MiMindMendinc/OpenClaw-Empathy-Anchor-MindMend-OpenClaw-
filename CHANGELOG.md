# Changelog

## [0.2.0-prototype] - 2026-07-16

### Migration note — product rename

Public product name is now **MindMend Empathy Anchor** (Local-First Safety Signal Demonstrator) by Michigan MindMend Inc.

- User-facing “OpenClaw Empathy Anchor” branding removed.
- Node compatibility: the `OpenClaw` class name remains as an internal alias so existing `require('./index')` demos keep working.
- API paths gain `/api/v1/*` while legacy routes (`/chat`, `/health`, …) remain for compatibility.

### Added
- Mobile-first showcase with plain-language safety results and optional Technical JSON
- `/api/v1/ready`, `/api/v1/scan`, alert delete/reset endpoints
- Privacy-preserving alert store (raw message retention off by default, retention purge)
- Detector evaluation harness (`backend/eval/`)
- Docs: PRIVACY, SAFETY, THREAT_MODEL, EVALUATION, DEPLOYMENT
- Rate limiting, payload limits, secure headers, localhost bind default
- CI: lint/format smoke, pip-audit, npm audit, evaluation smoke, ready check

### Changed
- Recommended actions labeled as recommendations (not automatic contacts)
- Docker healthcheck uses `/ready`
- System fonts only in showcase (no third-party font CDN)

### Security / Privacy
- No raw message logging/storage by default
- Alert endpoints authorization-scoped
- Production rejects documented demo JWT secrets

## [0.1.0-showcase] - 2026-07-16
Initial evidence-backed local demo release (prior naming).

## [0.1.0-local-safety-demo] - 2026-07-05
SQLite alerts, demo auth gates, Docker port unification.
