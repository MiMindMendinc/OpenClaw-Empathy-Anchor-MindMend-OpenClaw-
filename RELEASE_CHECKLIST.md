# Release checklist — v0.2.0-prototype

- [ ] Product named MindMend Empathy Anchor everywhere user-facing
- [ ] `npm test` and `DEMO_AUTH=true pytest backend/tests/ -v` pass
- [ ] `python backend/eval/run_eval.py` regenerates evidence
- [ ] `docker compose up --build` and `/ready` succeed
- [ ] Mobile widths 320–430 show stacked layout, no page-wide horizontal scroll
- [ ] Raw message retention remains off by default
- [ ] No secrets/databases committed
- [ ] Status label remains “Technical demonstration”
- [ ] Tag `v0.2.0-prototype`
