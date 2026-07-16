# Changelog

All notable changes to OpenClaw Empathy Anchor are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.0-showcase] - 2026-07-16

### Added
- Interactive showcase UI at `/` with capability placards and live API demo
- `GET /status` runtime evidence endpoint
- Local screenshots in `docs/assets/` captured from the live server
- Live JSON evidence under `docs/evidence/`
- `docs/evidence.md` honesty table for reviewers
- `archive/legacy/` for stale docs that overclaimed completeness

### Changed
- Docker Compose uses `FLASK_ENV=development` for the local demo (no fake production mode)
- CORS restricted to explicit `CORS_ORIGINS`
- `/resources` returns crisis resources only (donation/demo links removed)
- Demo login requires `DEMO_AUTH=true` in all modes
- Sentiment labeled as `keyword_pattern` (no placeholder NLP claims)
- README rewritten as evidence-first portfolio page
- `SECURITY.md` rewritten to match what CI and the app actually enforce

### Fixed
- Invalid `/night_mode` actions return 400
- Non-numeric `/location` coordinates return 400
- Stale “NASA-grade / 100% complete / production-ready” docs removed from the active tree

## [0.1.0-local-safety-demo] - 2026-07-05

### Added
- SQLite alert persistence (`backend/alert_store.py`)
- `/demo` endpoint for neutral, distress, crisis, night-mode, and geofence scenarios
- Demo authentication guardrails and production JWT requirements
- Python/Node/Docker CI jobs
- `CHANGELOG.md` and `RELEASE_CHECKLIST.md`

### Changed
- Docker port unified on 8000
- Node standard normalized to 20 LTS

[0.1.0-showcase]: https://github.com/MiMindMendinc/OpenClaw-Empathy-Anchor-MindMend-OpenClaw-/releases/tag/v0.1.0-showcase
[0.1.0-local-safety-demo]: https://github.com/MiMindMendinc/OpenClaw-Empathy-Anchor-MindMend-OpenClaw-/releases/tag/v0.1.0-local-safety-demo
