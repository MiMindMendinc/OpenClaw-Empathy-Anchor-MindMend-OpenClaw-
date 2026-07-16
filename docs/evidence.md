# Evidence

## Automated tests

- Node: `npm test` → 38 passing
- Python: `DEMO_AUTH=true pytest backend/tests/ -q` → 49 passing

## Detector evaluation (separate from unit tests)

```bash
python backend/eval/run_eval.py
```

See `evaluation.md` / `evaluation.json` in this folder.

## Live runtime artifacts

- `health.json`, `status.json`, `alerts.json`, `chat-crisis.json`, `demo.json`

## Screenshots

| File | Shows |
|------|-------|
| `docs/assets/01-showcase-hero.png` | Desktop hero |
| `docs/assets/02-live-demo-crisis.png` | Live results panel |
| `docs/assets/05-boundaries-placards.png` | Boundaries |
| `docs/assets/06-mobile-375-hero.png` | Mobile hero (native stack) |
| `docs/assets/07-mobile-390-results.png` | Mobile results stack |
