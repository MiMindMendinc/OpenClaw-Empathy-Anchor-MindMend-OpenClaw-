# Detector evaluation — MindMend Empathy Anchor

- Scanner: `rules-v1.0.0` (deterministic keyword/pattern)
- Cases: **25** synthetic labeled examples
- Generated: 2026-07-16T21:38:49.682096+00:00

These metrics are from a small synthetic labeled set for a deterministic rule scanner. They are not clinical validation and must not be advertised as accuracy guarantees.

| Category | Precision | Recall | F1 | Support (+) |
|----------|----------:|-------:|---:|------------:|
| crisis | 1.000 | 0.875 | 0.933 | 8 |
| distress | 0.833 | 1.000 | 0.909 | 5 |
| toxicity | 1.000 | 0.500 | 0.667 | 2 |
| night_mode | 1.000 | 1.000 | 1.000 | 1 |

## Known limitations highlighted by this set

- Negation handling is shallow and may still false-positive on complex phrasing.
- Quoted/academic mentions of crisis words are often flagged (documented false-positive class).
- Misspellings and obfuscation are largely undetected (documented false-negative class).
- Sarcasm and multi-turn context are not modeled.

Reproduce:

```bash
python backend/eval/run_eval.py
```
