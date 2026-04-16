# Safety Model

## Purpose

This document describes the intended safety posture of OpenClaw Empathy Anchor.

The project is designed as a supportive software layer for sensitive AI use cases. It is not intended to replace human care, crisis professionals, or clinical judgment.

---

## What the system is designed to do

OpenClaw Empathy Anchor is designed to help with:

- detecting crisis-related language
- detecting distress indicators
- detecting selected harmful or threatening patterns
- generating supportive, empathy-anchored responses
- attaching relevant support resources
- optionally creating alert objects for guardian-facing systems
- supporting night-mode and calming workflows
- supporting privacy-first and offline-capable deployment paths

---

## What the system is not designed to do

This project is not designed to:

- diagnose mental illness
- assess legal liability
- replace a therapist, counselor, or psychiatrist
- replace emergency response
- guarantee prevention of harm
- make clinical decisions on behalf of professionals
- act as a substitute for guardians, caregivers, or clinicians

---

## Safety posture

The intended posture is:

- supportive
- conservative in high-risk situations
- respectful of user sensitivity
- explicit about limitations
- designed to escalate to human help when needed

The system should help surface concern, not create false certainty.

---

## Escalation model

The intended escalation flow is:

1. detect concerning language or signals
2. classify severity level
3. generate empathy-anchored response
4. attach relevant crisis or support resources
5. optionally create alert event for guardian-facing systems
6. encourage human follow-up when risk is elevated

---

## Severity concept

A practical severity model may include:

- **low** — neutral or routine supportive interaction
- **moderate** — signs of stress, overwhelm, fear, or sleep difficulty
- **high** — significant distress or elevated concern
- **critical** — crisis-related or clearly dangerous language

The exact implementation may evolve, but the design goal is to keep severity understandable and actionable.

---

## Resource behavior

When elevated risk is detected, the system should prefer:

- clear supportive language
- concise crisis resources
- nonjudgmental wording
- encouragement to contact a trusted adult, guardian, clinician, or crisis line

In urgent cases, the system should favor clarity over cleverness.

---

## Privacy and safety relationship

Privacy is part of the safety model.

For sensitive youth-support use cases, unnecessary exposure of emotional content to external systems can create trust and risk problems of its own.

That is why the project emphasizes:

- local-first thinking
- minimal unnecessary data exposure
- explicit support boundaries
- support for offline-capable deployment paths

---

## Human override principle

Human care takes priority over software output.

Whenever there is serious concern:

- human review matters more than model tone
- crisis services matter more than system continuity
- guardian or clinician intervention matters more than automation

---

## Summary

OpenClaw Empathy Anchor is a safety-aware support layer, not a clinical authority.

Its role is to help supportive systems behave with more care, more privacy awareness, and better escalation boundaries.
