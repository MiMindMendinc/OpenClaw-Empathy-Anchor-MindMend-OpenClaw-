# Known issues

## Node version

Standard: **Node.js 20 LTS** (`>=20.0.0`).

CI and docs target Node 20. Newer Node (including 22) usually works for the built-in-module empathy layer.

## Demo authentication

`/auth/login` issues a JWT for any `user_id` only when `DEMO_AUTH=true`.

That is intentional for local demos. It is not identity verification.

## Alert storage

Alerts persist in local SQLite (`data/alerts.db` by default). There is no cloud sync in v0.1.

## Scanner scope

Luna Safety Core uses deterministic keyword/pattern matching. It is explainable and offline-friendly. It is not a trained clinical model.
