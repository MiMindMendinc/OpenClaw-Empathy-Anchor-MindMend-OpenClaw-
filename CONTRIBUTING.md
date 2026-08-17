# Contributing to MindMend Empathy Anchor

Thank you for your interest. This project is a **technical demonstration** of local-first safety-signal tooling by Michigan MindMend Inc. It is not clinical software and must not be described as therapy, a medical device, or an emergency service.

## How to contribute

1. Check existing issues before opening a new one.
2. For security issues, use GitHub’s private vulnerability reporting or contact maintainers privately. Do not file a public issue with exploit details.
3. Prefer small, tested changes. Safety-copy and crisis-resource edits need extra care.

## Development setup

```bash
python3 -m pip install -r backend/requirements.txt
npm test
DEMO_AUTH=true python3 -m pytest backend/tests
make demo
```

Or: `docker compose up --build` then open `http://127.0.0.1:8000/`.

Full check: `make verify`.

## Safety-copy rules

- Do not invent phone numbers, hours, or “24/7” claims.
- Crisis contacts live in `backend/support_resources.py`. Update [`docs/RESOURCES.md`](docs/RESOURCES.md) with the public page you checked and the date.
- Unit tests fail if the previously shipped transposed MiCAL number reappears.
- Keep the product status label as a technical demonstration.

## Pull requests

- Branch names should describe the change.
- Include how you tested (`make test` / `make verify`).
- Do not add analytics, telemetry, or third-party font/trackers to the showcase.

## Code of conduct

This repository discusses crisis language for verification. Be respectful, do not share real people’s private conversations, and do not make medical claims.

By contributing, you agree that your contributions are licensed under the MIT License.
