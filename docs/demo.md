# Demo walkthrough

## 60-second show

```bash
docker compose up --build
```

Open [http://localhost:8000/](http://localhost:8000/)

1. Click **Run the live demo**
2. Leave scenario on **Crisis**
3. Click **Scan with live API**
4. Point at the JSON: `severity: critical`, `alert_created: true`, SQLite alert id present
5. Click **Run all /demo scenarios**
6. Open **Boundaries** — say the honesty lines out loud

## Curl proof

```bash
curl -s http://localhost:8000/health | python -m json.tool
curl -s http://localhost:8000/status | python -m json.tool
curl -s http://localhost:8000/demo | python -m json.tool
```

Expected: `"status": "healthy"`, `"clinical_validation": false`, five scenarios including geofence.

## What to say when people ask “is this production?”

> This is a production-grade **local demo** of privacy-first safety infrastructure: real code, real tests, real SQLite alerts, real Docker healthcheck. It is not clinical software and not an emergency service. The scanner is deterministic and explainable on purpose.
