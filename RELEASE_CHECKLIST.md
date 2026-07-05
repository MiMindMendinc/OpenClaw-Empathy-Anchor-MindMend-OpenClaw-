# Release Checklist — v0.1.0-local-safety-demo

Use this checklist before tagging and publishing a demo release.

## Pre-release verification

- [ ] `npm install && npm test` — all Node tests pass
- [ ] `pip install -r backend/requirements.txt && pytest backend/tests/ -v` — all Python tests pass
- [ ] `docker compose up --build` — container starts and stays healthy
- [ ] `curl http://localhost:8000/health` — returns `"status": "healthy"`
- [ ] `curl http://localhost:8000/demo` — returns all five scenario types
- [ ] Demo auth works: `curl -X POST http://localhost:8000/auth/login -H 'Content-Type: application/json' -d '{"user_id":"demo"}'`
- [ ] Crisis chat creates persisted alert and `/alerts` returns it

## Configuration review

- [ ] `JWT_SECRET_KEY` documented and required for production
- [ ] `DEMO_AUTH=true` only used for controlled demos
- [ ] `PORT=8000` consistent across Docker, Compose, and healthcheck
- [ ] Node 20 LTS documented as standard runtime

## Documentation

- [ ] README "Run the demo" section is accurate
- [ ] Safety boundaries section present (not clinical, not emergency service)
- [ ] Implemented vs roadmap table reflects current state
- [ ] CHANGELOG.md updated for this release

## Safety and scope

- [ ] No paid APIs, cloud dependencies, tracking, or telemetry added
- [ ] No external database — SQLite only for alerts
- [ ] Crisis resources labeled as informational routing, not clinical validation

## GitHub Release

- [ ] Tag: `v0.1.0-local-safety-demo`
- [ ] Title: `v0.1.0 — Local Safety Demo`
- [ ] Release notes copied from CHANGELOG.md
- [ ] Attach demo curl examples or screenshot of `/demo` output (optional)

## Post-release

- [ ] Verify CI passes on main after merge
- [ ] Note any follow-up items in docs/roadmap.md
