# Release checklist

## Verify

- [ ] `npm test` — 38 passing
- [ ] `DEMO_AUTH=true pytest backend/tests/ -q` — 45 passing
- [ ] `docker compose up --build` — healthy on `:8000`
- [ ] Showcase loads at `/`
- [ ] Crisis scan creates SQLite alert visible in `/alerts`
- [ ] Screenshots in `docs/assets/` match the live UI
- [ ] No stale “100% complete / NASA-grade” docs in the active tree

## Ship

- [ ] Tag `v0.1.0-showcase`
- [ ] Release notes from `CHANGELOG.md`
- [ ] Attach or link `docs/assets/` screenshots
