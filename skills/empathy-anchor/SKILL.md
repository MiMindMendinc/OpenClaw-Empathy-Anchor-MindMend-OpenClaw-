---
name: empathy-anchor
description: Youth-focused empathy skill that validates emotions and provides checked US and Michigan mental health resources. Not clinical software.
license: MIT
allowed-tools:
  - node
metadata:
  language: JavaScript
  ecosystem: Node.js
  target-audience: Youth
  focus: Mental Health, Empathy, Privacy
  region: Michigan
---

# Empathy Anchor Skill

Supportive response framing for youth-support demos. This skill is **not** therapy, a medical device, or an emergency service.

Resource contacts and hours were checked against official public pages on **2026-08-17**. See [`docs/RESOURCES.md`](../../docs/RESOURCES.md).

## What it does

- Analyzes a message for emotion and crisis keyword patterns
- Wraps a response in validating language
- Adds informational resources when distress or crisis language is present
- Can run fully offline

## Immediate resources (24/7, United States)

- **988 Suicide & Crisis Lifeline** — Call or text 988 — https://988lifeline.org
- **Crisis Text Line** — Text HOME to 741741 — https://www.crisistextline.org
- **Michigan / MiCAL** — Call or text 988 (MiCAL is Michigan’s statewide 988 call center)
- **911** — immediate life-threatening emergencies

## Additional resources (not 24/7)

- **NAMI HelpLine** — 1-800-950-NAMI (6264), Monday–Friday 10 a.m.–10 p.m. ET — https://www.nami.org/support
- **NAMI Michigan** — https://namimi.org
- **Teen Line** — Call 800-852-8336 (6–10 p.m. PT) or text TEEN to 839863 (6–9 p.m. PT). Outside those hours, use 988. — https://www.teenline.org

## Boundaries

- Do not claim clinical effectiveness
- Do not invent phone numbers or hours
- Do not describe NAMI HelpLine or Teen Line as 24/7 crisis lines
- If someone may be in immediate danger, call or text 988 or contact emergency services
