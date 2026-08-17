# API

## HTTP

Canonical HTTP documentation: [`docs/API_REFERENCE.md`](docs/API_REFERENCE.md)

Preferred prefix: `/api/v1` on `http://127.0.0.1:8000`.

## Node library

```javascript
const { MindMendEmpathyAnchor } = require('./index');
const app = new MindMendEmpathyAnchor({ offlineMode: true });
const result = app.chat('I feel overwhelmed.');
```

`OpenClaw` remains a compatibility alias for `MindMendEmpathyAnchor`.

### `chat(message, aiResponse?)`

Returns `{ response, metadata }` where `metadata` includes `emotionsDetected`, `isCrisis`, `intensity`, `inputHash`, and `offlineMode`. Raw input is omitted unless `storeRawText: true`.

### `checkCrisis(message)`

Returns `true` when crisis keyword patterns match.

Interactive CLI: `npm start`  
HTTP showcase: `make demo`
