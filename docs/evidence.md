# Evidence

This page exists so reviewers do not have to trust marketing copy.

## Verified commands

```bash
# Node empathy layer
npm install
npm test

# Python backend
pip install -r backend/requirements.txt
DEMO_AUTH=true pytest backend/tests/ -v

# One-command stack
docker compose up --build
curl -s http://localhost:8000/health | python -m json.tool
curl -s http://localhost:8000/demo | python -m json.tool
curl -s http://localhost:8000/status | python -m json.tool
```

## What the tests prove

| Suite | Proves |
|-------|--------|
| Node `npm test` | Emotion validation, crisis detection, offline mode, Michigan resources, response metadata |
| Python API tests | `/health`, demo auth gate, crisis/distress chat alerts, geofence alerts, SQLite `/alerts`, production JWT requirements, `/demo` scenarios |
| Docker smoke (CI) | Image builds and `/health` returns healthy on port 8000 |

## Honesty table

| Claim | Evidence |
|-------|----------|
| Offline-first | No required paid APIs; scanner and empathy layer run locally |
| Crisis-aware framing | Keyword/pattern flags + resource text in responses |
| Parent alerts | SQLite rows created by `/chat` and `/location`, returned by `/alerts` |
| Demo auth labeled | Response includes `"demo_auth": true` and a notice string |
| Not clinical | `/status` and `/demo` both state no clinical validation |
| Screenshots | Captured from live `http://localhost:8000/` showcase — see `docs/assets/` |

## Screenshots

| Asset | What it shows |
|-------|----------------|
| `docs/assets/01-showcase-hero.png` | Brand-first landing viewport |
| `docs/assets/02-live-demo-crisis.png` | Live crisis scan against real API |
| `docs/assets/03-demo-all-scenarios.png` | Full `/demo` JSON scenarios |
| `docs/assets/04-status-json.png` | Runtime `/status` evidence |
| `docs/assets/05-boundaries-placards.png` | Safety boundaries placards |

## Known limits (on purpose)

- Scanner is deterministic keyword/pattern matching — explainable, not “advanced AI”
- Demo JWT login is for local demos only
- No push notifications, no cloud alert sync, no clinical study attached
