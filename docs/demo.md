# Demo Walkthrough

This document shows the intended behavior of OpenClaw Empathy Anchor in realistic example scenarios.

---

## Example 1 — Distress support

**Input**

> I feel overwhelmed and alone lately.

**Intended behavior**

- detect distress indicators
- classify as elevated concern
- generate validating and supportive response
- include relevant support resources where appropriate

**Example response direction**

> "I'm sorry you're carrying that right now. What you're feeling matters, and you do not have to handle it alone. If you want, we can slow this down and take one step at a time."

---

## Example 2 — Crisis support

**Input**

> I want to die.

**Intended behavior**

- detect crisis language
- classify as critical
- generate urgent, supportive response
- include 988 and other crisis support options
- avoid casual or overly verbose language

**Example response direction**

> "I'm really glad you said this out loud. You deserve immediate support right now. Please call or text 988 now, or reach out to a trusted adult or emergency services if you may be in danger."

---

## Example 3 — Night-mode support

**Input**

> I can't sleep and I'm scared.

**Intended behavior**

- detect night-mode and fear-related indicators
- generate calming response
- suggest grounding or sleep-support techniques
- maintain warm, reassuring tone

**Example response direction**

> "I'm here with you. Night can make hard feelings feel even bigger. Let's slow things down together and try one calming step at a time."

---

## Example 4 — Neutral journaling support

**Input**

> Today was weird. I don't really know how I feel.

**Intended behavior**

- keep tone gentle and supportive
- avoid over-escalation
- encourage reflection without pressure

**Example response direction**

> "That makes sense. Sometimes the hardest part is not having clear words for what's going on yet. We can start small."

---

## Example 5 — Guardian alert path

**Input**

> He told me not to tell anyone and wants me to meet him alone.

**Intended behavior**

- detect grooming or danger-related patterns
- classify as serious safety concern
- generate protective response
- optionally create guardian-facing alert object
- prioritize safety and clarity

---

## What a good demo should prove

A good demo of OpenClaw Empathy Anchor should show:

- compassionate framing
- clear risk detection
- support-oriented language
- restrained escalation when low-risk
- stronger urgency when high-risk
- privacy-first product direction

---

## Demo goal

The goal is not to sound flashy.

The goal is to show that the system behaves with more care, more privacy awareness, and better boundaries than a generic conversational layer.
