# Demonstration walkthrough

## 60 seconds

```bash
docker compose up --build
open http://127.0.0.1:8000/
```

1. Confirm status pills show API/storage ready
2. Keep **Neutral** selected and scan
3. Switch to **Distress** and scan — read severity, categories, recommended actions
4. Expand **Technical JSON** only if needed
5. Open **Boundaries** and state the honesty lines

Crisis language examples stay behind an explicit selector with a content notice.

## Verify persistence

```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H 'Content-Type: application/json' -d '{"user_id":"demo"}' | python -c "import sys,json; print(json.load(sys.stdin)['token'])")
curl -s -X POST http://127.0.0.1:8000/api/v1/scan \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"message":"I feel anxious and overwhelmed"}'
# restart container/process, then:
curl -s http://127.0.0.1:8000/api/v1/alerts -H "Authorization: Bearer $TOKEN"
```
