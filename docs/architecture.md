# Architecture overview

Canonical architecture notes: [`ARCHITECTURE.md`](ARCHITECTURE.md).

MindMend Empathy Anchor separates:

1. Showcase UI (`showcase/`)
2. Flask API (`backend/app.py`)
3. Deterministic scanner (`backend/luna_safety_core.py`)
4. Local SQLite alerts (`backend/alert_store.py`)
5. Node empathy skill (`skills/empathy-anchor/`)
