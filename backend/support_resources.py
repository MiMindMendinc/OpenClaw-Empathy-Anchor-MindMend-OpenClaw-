"""
Verified support-resource copy for MindMend Empathy Anchor.

Numbers and hours below were checked against the organizations' public pages
on 2026-08-17. This module is the Python source of truth. Do not invent
contacts, hours, or “24/7” claims here.

Informational routing only. Availability is not guaranteed.
"""

from __future__ import annotations

from typing import Dict

VERIFIED_ON = '2026-08-17'

# Immediate, 24/7 US crisis routing. Shown when crisis language is detected.
IMMEDIATE_24_7: Dict[str, str] = {
    '988': (
        '988 Suicide & Crisis Lifeline — Call or text 988 (24/7, United States). '
        'https://988lifeline.org'
    ),
    'crisis_text': (
        'Crisis Text Line — Text HOME to 741741 (24/7, United States). '
        'https://www.crisistextline.org'
    ),
    'michigan_crisis': (
        'Michigan Crisis & Access Line (MiCAL) — Call or text 988. '
        'MiCAL is Michigan’s statewide 988 call center. '
        'https://www.michigan.gov/mdhhs/keep-mi-healthy/mentalhealth/crisis-and-access-line'
    ),
    'emergency': '911 — For immediate life-threatening emergencies',
}

# Additional routing. Hours are not 24/7; never describe these as always-on crisis lines.
ADDITIONAL: Dict[str, str] = {
    'nami_helpline': (
        'NAMI HelpLine — 1-800-950-NAMI (6264), Monday–Friday 10 a.m.–10 p.m. ET. '
        'https://www.nami.org/support'
    ),
    'nami_michigan': (
        'NAMI Michigan — education, advocacy, and support groups. '
        'https://namimi.org'
    ),
    'teen_line': (
        'Teen Line — Call 800-852-8336 (6–10 p.m. PT) or text TEEN to 839863 '
        '(6–9 p.m. PT). Outside those hours, call or text 988. '
        'https://www.teenline.org'
    ),
}

# Compatibility alias used by /api/v1/resources and scan_result["resources"].
CRISIS_RESOURCES: Dict[str, str] = dict(IMMEDIATE_24_7)

SOURCES = {
    '988': 'https://988lifeline.org',
    'crisis_text_line': 'https://www.crisistextline.org',
    'michigan_988_mical': (
        'https://www.michigan.gov/mdhhs/keep-mi-healthy/mentalhealth/crisis-and-access-line'
    ),
    'nami_helpline': 'https://www.nami.org/support',
    'nami_michigan': 'https://namimi.org',
    'teen_line': 'https://www.teenline.org',
}

# Strings that must never appear: a previously shipped transposition of the
# historical MiCAL number (1-844-44MICAL / 1-844-446-4225). MDHHS now directs
# the public to 988, which is what this repo ships.
FORBIDDEN_CONTACT_FRAGMENTS = (
    '1-844-464-3274',
    '18444643274',
    '844-464-3274',
)


def public_payload(region: str = 'us-mi') -> dict:
    return {
        'region': region,
        'verified_on': VERIFIED_ON,
        'immediate_24_7': IMMEDIATE_24_7,
        'additional': ADDITIONAL,
        'crisis_resources': CRISIS_RESOURCES,
        'sources': SOURCES,
        'notice': (
            'Informational routing only. Hours and availability are not guaranteed. '
            'If someone may be in immediate danger, call or text 988 (US) '
            'or contact local emergency services.'
        ),
    }
