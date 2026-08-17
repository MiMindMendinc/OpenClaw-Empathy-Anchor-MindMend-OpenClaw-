# Evidence

Counts and JSON below were produced by `scripts/capture-evidence.sh` on 2026-08-17 against a live local process. Reproduce with `make evidence`.

## Automated tests

- Node: `npm test` → **38 passing**
- Python: `DEMO_AUTH=true python3 -m pytest backend/tests -q` → **57 passed in 0.80s**

Logs: `npm-test.txt`, `pytest.txt` in this folder.

## Detector evaluation (separate from unit tests)

```bash
python3 backend/eval/run_eval.py
```

See `evaluation.md` / `evaluation.json` in this folder. Metrics are from 25 synthetic labeled cases and are **not** clinical validation.

## Live runtime artifacts

- `health.json`, `ready.json`, `status.json`, `resources.json`
- `alerts.json`, `chat-crisis.json`, `demo.json`

## Screenshots

| File | Shows |
|------|-------|
| `docs/assets/01-showcase-hero.png` | Desktop hero with live status pills |
| `docs/assets/02-live-demo-distress.png` | Live distress scan results |
| `docs/assets/03-live-demo-crisis.png` | Live crisis-language scan results |
| `docs/assets/05-boundaries-placards.png` | Safety boundaries |
| `docs/assets/06-mobile-375-hero.png` | Mobile hero (native stack) |
| `docs/assets/07-mobile-390-results.png` | Mobile results stack |
