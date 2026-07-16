# Architecture

MindMend Empathy Anchor separates:

1. **Showcase UI** (`showcase/`) — local static frontend served by Flask
2. **API** (`backend/app.py`) — auth, scan, alerts, health/ready
3. **Deterministic scanner** (`backend/luna_safety_core.py`) — keyword/pattern rules
4. **Alert store** (`backend/alert_store.py`) — SQLite, privacy-preserving defaults
5. **Node empathy skill** (`skills/empathy-anchor/`) — supportive response framing for CLI/demos

```text
Browser/CLI
   → Flask /api/v1
   → LunaSafetyCore.scan_message
   → optional AlertStore.save_alert
   → supportive response + informational resources
   → human review
```

No required cloud dependency. Optional model API keys are not used by the default offline path.
