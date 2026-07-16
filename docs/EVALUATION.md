# Evaluation

Detector performance is measured with a **synthetic labeled set**, separate from unit tests.

## Reproduce

```bash
python backend/eval/run_eval.py
```

Outputs:

- `docs/evidence/evaluation.json`
- `docs/evidence/evaluation.md`

## Important

- Unit-test counts are **not** accuracy claims.
- Metrics come only from the labeled evaluation harness.
- The set is small and synthetic; results are for engineering transparency, not clinical validation.
- Do not advertise “accuracy” without citing this harness and its limitations.

See also: [`docs/SAFETY.md`](SAFETY.md) and [`docs/evidence/evaluation.md`](evidence/evaluation.md).
