# Privacy

MindMend Empathy Anchor is designed for **local-first** demonstration.

## What is received

- Text submitted to scan/chat endpoints
- Optional location coordinates for geofence checks
- Demo `user_id` values used to mint local JWTs when `DEMO_AUTH=true`

## What is stored

| Item | Default |
|------|---------|
| Alert summary (type, severity, recommended actions, matches) | Yes — local SQLite |
| Raw message text | **No** (`STORE_RAW_MESSAGES=false`) |
| Analytics / telemetry | **None** |
| Third-party cloud sync | **None** |

Storage location defaults to `data/alerts.db` (configurable via `ALERT_DB_PATH`).

## Retention

- `ALERT_RETENTION_DAYS` (default `30`) deletes older alert rows on read paths / purge.
- Authenticated users can delete one alert or all of their alerts via API.
- Full reset: stop the service and delete the SQLite file.

## Logging

- Application logs do **not** include raw message content by default.
- Alert creation logs include user id, severity, and request id only.

## Network

- No outbound network requests are required for scanning or alerts.
- The showcase UI uses **system fonts only** (no Google Fonts / trackers).
- Optional external model API keys in `.env.example` are unused by the default offline path.

## Deletion API

```bash
# delete one alert
curl -X DELETE http://127.0.0.1:8000/api/v1/alerts/<id> -H "Authorization: Bearer $TOKEN"

# delete all alerts for authenticated user
curl -X DELETE http://127.0.0.1:8000/api/v1/alerts -H "Authorization: Bearer $TOKEN"
```

## Full local reset

```bash
docker compose down
rm -f data/alerts/alerts.db data/alerts.db
```
