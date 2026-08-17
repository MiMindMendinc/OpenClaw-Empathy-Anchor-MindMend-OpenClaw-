# Using MindMend Empathy Anchor

This repository has two runnable surfaces:

1. **Local Flask showcase + API** — the demonstration you can show in a browser
2. **Node empathy skill** — a library/CLI that wraps messages in supportive language

Neither one is an OpenClaw runtime, a therapist, or an emergency service.

## Browser demonstration

```bash
python3 -m pip install -r backend/requirements.txt
make demo
```

Then open `http://127.0.0.1:8000/`.

Walkthrough: [`demo.md`](demo.md)

## Node CLI

```bash
npm start
```

Type a message, or `exit`. Crisis language should mention 988.

Scripted examples:

```bash
npm run demo
node examples/demo.js
```

## HTTP API

Preferred prefix: `/api/v1`. See [`API_REFERENCE.md`](API_REFERENCE.md).

Demo login exists only when `DEMO_AUTH=true` and is not identity verification.

## Support resources

Shipped contacts and the pages used to check them: [`RESOURCES.md`](RESOURCES.md).
