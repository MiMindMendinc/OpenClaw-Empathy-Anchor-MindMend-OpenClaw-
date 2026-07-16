# Safety

## Status

MindMend Empathy Anchor is a **technical demonstration**.

It is not therapy, a medical device, diagnostic software, an emergency service, or a replacement for parents, guardians, clinicians, 988, or 911.

## Detector honesty

| Topic | Reality |
|-------|---------|
| Method | Deterministic keyword/pattern matching (`rules-v1.0.0`) |
| Categories | crisis, distress, toxicity, night_mode (+ optional geofence) |
| Multi-message context | Not considered |
| Language | English keyword lists only |
| Negation | Shallow preceding-window heuristic |
| Quotes / academic text | Often false-positive |
| Sarcasm | Not modeled |
| Misspellings / obfuscation | Often false-negative |
| Clinical validation | **None** |

Severity meanings:

- `critical` — crisis or toxicity flags
- `high` — distress flags
- `moderate` — night-mode flags
- `low` — no safety flags

Recommended actions are **recommendations**, not completed contacts.

## Immediate danger

If someone may be in immediate danger, contact emergency services or call/text **988** (US). Resource lists are informational and do not guarantee availability.

## Must never be used to decide automatically

Do not use this detector alone to:

- Remove access to care
- Trigger law-enforcement response without human review
- Diagnose mental illness
- Discipline a student/child without human judgment
