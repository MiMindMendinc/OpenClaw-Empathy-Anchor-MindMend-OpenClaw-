# OpenClaw Empathy Anchor

## A HumaniCare AI module by Michigan MindMend Inc.

**Offline-first empathy and safety infrastructure for youth-support AI systems.**

OpenClaw Empathy Anchor is the core empathy and safety module inside **HumaniCare AI**: privacy-first, local-first AI infrastructure for healthcare access, mental health support, family safety, and community resilience.

> Helpful AI should protect people without harvesting their data.

---

## Positioning

**Privacy-first. Local-first. Clinician-informed. Built for underserved communities.**

This project is designed for sensitive AI use cases involving youth wellness, journaling, emotional check-ins, safety-aware response generation, and offline-capable support workflows.

It combines:

- compassionate response framing
- crisis-aware safety logic
- youth-appropriate language handling
- privacy-first local deployment patterns
- optional geofence and alert workflows
- rural and low-connectivity deployment direction
- human-in-the-loop escalation boundaries

---

## Why this exists

Most AI support tools for vulnerable users depend on cloud APIs, stored conversations, or third-party infrastructure.

OpenClaw and HumaniCare explore a different model:

- local-first
- privacy-first
- offline-capable
- safety-aware
- human-centered
- transparent about clinical limits

The goal is not to replace human care. The goal is to build a safer, more respectful support layer for sensitive environments.

---

## HumaniCare AI Architecture

```mermaid
flowchart TD
    A[User / Youth / Family / Caregiver] --> B[Local Device or Edge Server]

    B --> C[HumaniCare AI Safety Router]

    C --> D[OpenClaw Empathy Anchor]
    C --> E[MindMend Guardian]
    C --> F[Journal Coach]
    C --> G[Link Sentinel]
    C --> H[Crisis Resource Layer]
    C --> I[Rural Edge Kit]

    D --> D1[Supportive Response Framing]
    E --> E1[Youth and Family Safety Workflows]
    F --> F1[Private Reflection and Grounding]
    G --> G1[Scam / Abuse / Harmful Link Detection]
    H --> H1[Escalation-Safe Resource Routing]
    I --> I1[Offline / Low-Bandwidth Deployment]

    C --> J[Local Audit Log]
    J --> K[Human Review / Caregiver / Clinician / Trusted Helper]

    L[Optional Cloud Services] -. disabled by default / explicit use only .-> C
```

OpenClaw is the empathy and response-framing layer. HumaniCare is the umbrella system that can connect it to Guardian, Journal Coach, Link Sentinel, crisis resource routing, and rural edge deployments.

See [docs/humanicare-blueprint.md](docs/humanicare-blueprint.md).

---

## What this repo contains

This repository currently includes:

- a Node-based empathy anchor layer for compassionate response wrapping
- a Flask backend for safety scanning, geofence checks, night-mode support, and alert generation
- a privacy-first architecture direction designed for sensitive use cases
- localized Michigan crisis resources and youth-support pathways
- HumaniCare umbrella documentation for safety, clinical boundaries, and rural deployment

---

## Product direction

OpenClaw Empathy Anchor is being developed as a foundation for:

- local journaling assistants
- youth-support AI companions
- school and nonprofit pilot tools
- clinician-adjacent internal prototypes
- privacy-first family support systems
- edge and mini-PC deployments
- rural community resilience tools

---

## Architecture at a glance

High-level flow:

```text
User input
→ empathy anchor
→ safety scan
→ supportive response
→ optional resources
→ optional alert event
→ optional human review
```

Core components:

- **Empathy Anchor**: wraps responses in validating, supportive language
- **Luna Safety Core**: evaluates crisis language, distress indicators, toxicity patterns, geofence events, and night-mode needs
- **Backend API**: exposes endpoints for auth, chat, location, alerts, resources, and support workflows
- **HumaniCare Layer**: product umbrella for privacy-first healthcare access, youth wellness, and rural support infrastructure

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
- rural/low-connectivity support environments

See [docs/rural-edge-deployment.md](docs/rural-edge-deployment.md).

---

## Privacy model

OpenClaw Empathy Anchor is designed around a privacy-first direction:

- no required accounts
- no forced cloud inference path
- support for local-first operation
- intended for sensitive, trust-dependent environments
- no hidden telemetry by design direction

Implementation details may evolve over time, but the design goal is consistent: reduce unnecessary data exposure.

---

## Safety and clinical boundaries

This project is supportive software infrastructure, not a replacement for:

- licensed clinicians
- emergency services
- crisis professionals
- parental or guardian judgment

If someone may be in immediate danger, contact emergency services or call/text **988** right away.

Read more:

- [Safety model](docs/safety-model.md)
- [Clinical boundaries](docs/clinical-boundaries.md)
- [HumaniCare blueprint](docs/humanicare-blueprint.md)

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
- healthcare-adjacent boundary awareness
- rural and underserved-community deployment thinking

---

## Current status

Active prototype and portfolio project.

Current focus:

- repository cleanup and consolidation
- stronger demo experience
- clearer packaging and documentation
- offline deployment improvements
- sharper product positioning
- HumaniCare umbrella integration

---

## Roadmap

- unify Node and backend demo flow
- add screenshots and demo assets
- improve test organization
- add Raspberry Pi and edge deployment notes
- add local journaling storage examples
- publish a clean versioned release
- document validation and advisory-review path
- connect Guardian / Journal Coach / Link Sentinel modules under HumaniCare

See [docs/roadmap.md](docs/roadmap.md) for the product-facing roadmap.

---

## Repository structure

```text
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
│   ├── humanicare-blueprint.md
│   ├── clinical-boundaries.md
│   ├── rural-edge-deployment.md
│   └── ...
└── examples/
```

---

## Built by

**Lyle Perrien II**  
**Michigan MindMend Inc.**

Privacy-first AI for families, communities, and youth-support environments.

## License

MIT — Built for the people, not the platforms.
