# API reference — MindMend Empathy Anchor

Base URL (local): `http://127.0.0.1:8000`

Preferred prefix: `/api/v1`  
Legacy aliases remain for `/health`, `/chat`, `/alerts`, `/demo`, etc.

## GET /api/v1/health

Process alive.

## GET /api/v1/ready

Storage and configuration usable. Returns 503 if storage is not ready.

## GET /api/v1/status

Runtime honesty JSON (scanner method, privacy flags, boundaries).

## POST /api/v1/auth/login

Demo JWT minting when `DEMO_AUTH=true`. Body: `{"user_id":"demo"}`.

## POST /api/v1/scan

Authenticated scan. Body: `{"message":"...","persist_alert":true}`.

Response `data.summary` includes severity, categories, matches, recommended actions, alert persistence fields.

## POST /api/v1/chat

Compatibility chat endpoint (legacy response shape).

## GET /api/v1/alerts

List alerts for JWT user.

## DELETE /api/v1/alerts/{id}

Delete one alert for JWT user.

## DELETE /api/v1/alerts

Delete all alerts for JWT user.

## GET /api/v1/demo

Deterministic scenarios for verification.

## GET /api/v1/resources

Informational crisis resources.
