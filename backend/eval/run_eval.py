#!/usr/bin/env python3
"""Reproducible detector evaluation for MindMend Empathy Anchor."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from luna_safety_core import LunaSafetyCore  # noqa: E402
from version import PRODUCT_NAME, SCANNER_VERSION, VERSION  # noqa: E402

CATEGORIES = ['crisis', 'distress', 'toxicity', 'night_mode']


def f1(precision: float, recall: float) -> float:
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def main() -> int:
    cases_path = Path(__file__).with_name('cases.json')
    data = json.loads(cases_path.read_text(encoding='utf-8'))
    cases = data['cases']
    core = LunaSafetyCore(offline_mode=True, use_spacy=False)

    per_cat = {
        cat: {'tp': 0, 'fp': 0, 'tn': 0, 'fn': 0}
        for cat in CATEGORIES
    }
    rows = []

    for case in cases:
        result = core.scan_message(case.get('text') or '')
        flags = result.get('flags') or {}
        predicted = {cat for cat in CATEGORIES if flags.get(cat)}
        labels = set(case.get('labels') or [])
        rows.append({
            'id': case['id'],
            'category': case.get('category'),
            'labels': sorted(labels),
            'predicted': sorted(predicted),
            'severity': result.get('severity'),
        })
        for cat in CATEGORIES:
            truth = cat in labels
            pred = cat in predicted
            if truth and pred:
                per_cat[cat]['tp'] += 1
            elif not truth and pred:
                per_cat[cat]['fp'] += 1
            elif not truth and not pred:
                per_cat[cat]['tn'] += 1
            else:
                per_cat[cat]['fn'] += 1

    metrics = {}
    for cat, c in per_cat.items():
        prec = c['tp'] / (c['tp'] + c['fp']) if (c['tp'] + c['fp']) else 0.0
        rec = c['tp'] / (c['tp'] + c['fn']) if (c['tp'] + c['fn']) else 0.0
        metrics[cat] = {
            'precision': round(prec, 4),
            'recall': round(rec, 4),
            'f1': round(f1(prec, rec), 4),
            'confusion': c,
            'support_positive': c['tp'] + c['fn'],
        }

    report = {
        'product': PRODUCT_NAME,
        'version': VERSION,
        'scanner_version': SCANNER_VERSION,
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'dataset': data['dataset'],
        'n_cases': len(cases),
        'metrics': metrics,
        'disclaimer': (
            'These metrics are from a small synthetic labeled set for a deterministic '
            'rule scanner. They are not clinical validation and must not be advertised '
            'as accuracy guarantees.'
        ),
        'cases': rows,
    }

    out_dir = Path(__file__).resolve().parents[2] / 'docs' / 'evidence'
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / 'evaluation.json'
    md_path = out_dir / 'evaluation.md'
    json_path.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')

    lines = [
        f'# Detector evaluation — {PRODUCT_NAME}',
        '',
        f'- Scanner: `{SCANNER_VERSION}` (deterministic keyword/pattern)',
        f'- Cases: **{len(cases)}** synthetic labeled examples',
        f'- Generated: {report["generated_at"]}',
        '',
        report['disclaimer'],
        '',
        '| Category | Precision | Recall | F1 | Support (+) |',
        '|----------|----------:|-------:|---:|------------:|',
    ]
    for cat in CATEGORIES:
        m = metrics[cat]
        lines.append(
            f"| {cat} | {m['precision']:.3f} | {m['recall']:.3f} | {m['f1']:.3f} | {m['support_positive']} |"
        )
    lines.extend([
        '',
        '## Known limitations highlighted by this set',
        '',
        '- Negation handling is shallow and may still false-positive on complex phrasing.',
        '- Quoted/academic mentions of crisis words are often flagged (documented false-positive class).',
        '- Misspellings and obfuscation are largely undetected (documented false-negative class).',
        '- Sarcasm and multi-turn context are not modeled.',
        '',
        'Reproduce:',
        '',
        '```bash',
        'python backend/eval/run_eval.py',
        '```',
        '',
    ])
    md_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Wrote {json_path}')
    print(f'Wrote {md_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
