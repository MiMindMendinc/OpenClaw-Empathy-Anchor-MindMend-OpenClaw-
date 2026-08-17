#!/usr/bin/env bash
# Capture live runtime JSON and test logs into docs/evidence/.
# Requires a running server on PORT (default 8000) OR starts one.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PYTHON="${PYTHON:-python3}"
PORT="${PORT:-8000}"
BASE="http://127.0.0.1:${PORT}"
OUT="$ROOT/docs/evidence"
STARTED=0
SERVER_PID=""

cleanup() {
  if [[ "$STARTED" = "1" && -n "$SERVER_PID" ]]; then
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

mkdir -p "$OUT"

if ! curl -sf "$BASE/ready" >/dev/null; then
  echo "Starting local server to capture evidence…"
  DEMO_AUTH=true BIND_HOST=127.0.0.1 OFFLINE_MODE=true PORT="$PORT" \
    "$PYTHON" backend/app.py >/tmp/mindmend-evidence.log 2>&1 &
  SERVER_PID=$!
  STARTED=1
  for _ in $(seq 1 40); do
    curl -sf "$BASE/ready" >/dev/null && break
    sleep 0.25
  done
  curl -sf "$BASE/ready" >/dev/null
fi

curl -sf "$BASE/api/v1/health" | "$PYTHON" -m json.tool > "$OUT/health.json"
curl -sf "$BASE/api/v1/ready" | "$PYTHON" -m json.tool > "$OUT/ready.json"
curl -sf "$BASE/api/v1/status" | "$PYTHON" -m json.tool > "$OUT/status.json"
curl -sf "$BASE/api/v1/demo" | "$PYTHON" -m json.tool > "$OUT/demo.json"
curl -sf "$BASE/api/v1/resources" | "$PYTHON" -m json.tool > "$OUT/resources.json"

TOKEN="$("$PYTHON" - <<PY
import json, urllib.request
req = urllib.request.Request(
    "$BASE/api/v1/auth/login",
    data=json.dumps({"user_id": "evidence"}).encode(),
    headers={"Content-Type": "application/json"},
    method="POST",
)
print(json.load(urllib.request.urlopen(req))["token"])
PY
)"

"$PYTHON" - <<PY
import json, urllib.request
token = """$TOKEN"""
base = "$BASE"
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
req = urllib.request.Request(
    base + "/api/v1/scan",
    data=json.dumps({"message": "I want to kill myself"}).encode(),
    headers=headers,
    method="POST",
)
scan = json.load(urllib.request.urlopen(req))
open("$OUT/chat-crisis.json", "w", encoding="utf-8").write(json.dumps(scan, indent=2) + "\n")
req = urllib.request.Request(base + "/api/v1/alerts", headers={"Authorization": f"Bearer {token}"})
alerts = json.load(urllib.request.urlopen(req))
open("$OUT/alerts.json", "w", encoding="utf-8").write(json.dumps(alerts, indent=2) + "\n")
PY

"$PYTHON" backend/eval/run_eval.py
npm test > "$OUT/npm-test.txt" 2>&1 || { cat "$OUT/npm-test.txt"; exit 1; }
DEMO_AUTH=true "$PYTHON" -m pytest backend/tests -q --tb=no > "$OUT/pytest.txt" 2>&1 || { cat "$OUT/pytest.txt"; exit 1; }

echo "Wrote evidence under $OUT"
