"""Guardrails for published support-resource copy."""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')

from luna_safety_core import LunaSafetyCore
from support_resources import (
    ADDITIONAL,
    CRISIS_RESOURCES,
    FORBIDDEN_CONTACT_FRAGMENTS,
    IMMEDIATE_24_7,
    VERIFIED_ON,
    public_payload,
)


ROOT = Path(__file__).resolve().parents[2]


SKIP_FILES = {
    'backend/support_resources.py',
    'backend/tests/test_resources.py',
    'backend/tests/test_app.py',
    'scripts/verify.sh',
}


def _repo_text_files():
    skip_dirs = {
        '.git', 'archive', 'node_modules', '.venv', 'venv',
        'docs/evidence', 'docs/assets',
    }
    for path in ROOT.rglob('*'):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel in SKIP_FILES:
            continue
        if any(rel == d or rel.startswith(d + '/') for d in skip_dirs):
            continue
        if path.suffix.lower() not in {'.py', '.js', '.md', '.json', '.yml', '.html', '.css', '.sh', '.mjs'}:
            continue
        yield path, rel


def test_verified_on_is_iso_date():
    assert VERIFIED_ON == '2026-08-17'


def test_immediate_resources_include_official_24_7_contacts():
    blob = json.dumps(IMMEDIATE_24_7)
    assert 'Call or text 988' in blob or 'call or text 988' in blob.lower()
    assert 'HOME to 741741' in CRISIS_RESOURCES['crisis_text']
    assert '911' in CRISIS_RESOURCES['emergency']
    assert 'MiCAL' in CRISIS_RESOURCES['michigan_crisis']
    assert '988' in CRISIS_RESOURCES['michigan_crisis']


def test_additional_resources_do_not_claim_24_7():
    blob = json.dumps(ADDITIONAL).lower()
    assert '24/7' not in blob
    assert 'teen' in ADDITIONAL['teen_line'].lower()
    assert '6–10 p.m. PT' in ADDITIONAL['teen_line'] or '6-10 p.m. PT' in ADDITIONAL['teen_line']
    assert 'namimi.org' in ADDITIONAL['nami_michigan']


def test_forbidden_transposed_mical_number_absent_from_shipped_copy():
    core = LunaSafetyCore()
    payload = json.dumps(public_payload())
    response = core.generate_empathy_response('I want to kill myself')
    haystack = payload + response + json.dumps(core.CRISIS_RESOURCES)
    for fragment in FORBIDDEN_CONTACT_FRAGMENTS:
        assert fragment not in haystack


def test_forbidden_number_not_in_active_repo_files():
    offenders = []
    for path, rel in _repo_text_files():
        text = path.read_text(encoding='utf-8', errors='ignore')
        for fragment in FORBIDDEN_CONTACT_FRAGMENTS:
            if fragment in text:
                offenders.append(f'{rel}: {fragment}')
    assert offenders == []


def test_crisis_scan_attaches_immediate_resources_only():
    result = LunaSafetyCore().scan_message('I want to kill myself')
    assert result['flags']['crisis'] is True
    assert set(result['resources']) == set(CRISIS_RESOURCES)
    assert 'nami_michigan' not in result['resources']
    assert 'HOME to 741741' in result['resources']['crisis_text']
