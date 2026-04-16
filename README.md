# OpenClaw Empathy Anchor

**Offline-first empathy and safety infrastructure for youth-support AI systems**

OpenClaw Empathy Anchor is a privacy-first support layer built by Michigan MindMend Inc. for sensitive AI use cases involving youth wellness, journaling, emotional check-ins, and safety-aware response generation.

It combines:

- compassionate response framing
- crisis-aware safety logic
- optional geofence and alert workflows
- offline-capable deployment paths
- youth-appropriate language handling

---

## Why this exists

Most AI support tools for vulnerable users depend on cloud APIs, stored conversations, or third-party infrastructure.

OpenClaw Empathy Anchor explores a different model:

- local-first
- privacy-first
- offline-capable
- safety-aware
- human-centered

The goal is not to replace human care. The goal is to build a safer, more respectful support layer for sensitive environments.

---

## What this repo contains

This repository currently includes:

- a Node-based empathy anchor layer for compassionate response wrapping
- a Flask backend for safety scanning, geofence checks, night-mode support, and alert generation
- a privacy-first architecture direction designed for sensitive use cases
- localized Michigan crisis resources and youth-support pathways

---

## Product direction

OpenClaw Empathy Anchor is being developed as a foundation for:

- local journaling assistants
- youth-support AI companions
- school and nonprofit pilot tools
- clinician-adjacent internal prototypes
- privacy-first family support systems
- edge and mini-PC deployments

---

## Architecture at a glance

High-level flow:

```
User input
→ empathy anchor
→ safety scan
→ supportive response
→ optional resources
→ optional alert event
```

Core components:

- **Empathy Anchor**: wraps responses in validating, supportive language
- **Luna Safety Core**: evaluates crisis language, distress indicators, toxicity patterns, geofence events, and night-mode needs
- **Backend API**: exposes endpoints for auth, chat, location, alerts, resources, and support workflows

For a fuller breakdown, see [docs/architecture.md](docs/architecture.md).

---

## Quick start

**Option A — Run the empathy layer**

```bash
npm install
npm start
```

**Option B — Run the backend**

```bash
cd backend
pip install -r requirements.txt
python app.py
```

**Docker**

```bash
docker build -t openclaw-empathy-anchor .
docker run -p 8000:8000 openclaw-empathy-anchor
```

The current Docker path is designed around the Flask backend.

---

## Deployment modes

This project can be adapted for:

- local developer testing
- nonprofit pilot deployments
- family device or mini-PC deployments
- school or clinic internal demos
- Raspberry Pi and edge-device experiments

---

## Privacy model

OpenClaw Empathy Anchor is designed around a privacy-first direction:

- no required accounts
- no forced cloud inference path
- support for local-first operation
- intended for sensitive, trust-dependent environments

Implementation details may evolve over time, but the design goal is consistent: reduce unnecessary data exposure.

---

## Safety notice

This project is a supportive software prototype, not a replacement for:

- licensed clinicians
- emergency services
- crisis professionals
- parental or guardian judgment

If someone may be in immediate danger, contact emergency services or call/text **988** right away.

For more on design boundaries, see [docs/safety-model.md](docs/safety-model.md).

---

## For recruiters and collaborators

This repository demonstrates:

- privacy-first product thinking
- modular AI system design
- safety-aware response architecture
- Flask API design
- Node-based response-layer implementation
- offline and local deployment direction
- product framing for sensitive use cases

---

## Current status

Active prototype and portfolio project.

Current focus:

- repository cleanup and consolidation
- stronger demo experience
- clearer packaging and documentation
- offline deployment improvements
- sharper product positioning

---

## Roadmap

- unify Node and backend demo flow
- add screenshots and demo assets
- improve test organization
- add Raspberry Pi and edge deployment notes
- add local journaling storage examples
- publish a clean versioned release

See [docs/roadmap.md](docs/roadmap.md) for the product-facing roadmap.

---

## Repository structure

```
.
├── README.md
├── package.json
├── index.js
├── Dockerfile
├── backend/
│   ├── app.py
│   ├── luna_safety_core.py
│   ├── requirements.txt
│   └── tests/
├── skills/
│   └── empathy-anchor/
├── docs/
└── examples/
```

---

## Built by

Lyle Perrien II
Michigan MindMend Inc.

Privacy-first AI for families, communities, and youth-support environments.

## 📄 License

MIT — Built for the people, not the platforms.
