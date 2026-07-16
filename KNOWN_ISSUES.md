# Known issues

## Detector limits

- Deterministic English keyword/pattern rules only
- Quoted/academic mentions often false-positive
- Misspellings/obfuscation often false-negative
- Sarcasm and multi-turn context not modeled
- Negation handling is shallow

## Demo authentication

`/auth/login` requires `DEMO_AUTH=true` and is not identity verification.

## Compatibility alias

Node module still exports `OpenClaw` as an alias for `MindMendEmpathyAnchor`.

## Repository name

The GitHub repository URL may still contain historical “OpenClaw” naming; the public product name is MindMend Empathy Anchor.
