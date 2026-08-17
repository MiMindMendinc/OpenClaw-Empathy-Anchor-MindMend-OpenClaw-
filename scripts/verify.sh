#!/usr/bin/env bash
# End-to-end check: unit tests, eval harness, then a live local process.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PYTHON="${PYTHON:-python3}"
PORT="${PORT:-8000}"
export BASE="http://127.0.0.1:${PORT}"
SKIP_NODE="${SKIP_NODE:-0}"
SERVER_PID=""

cleanup() {
  if [[ -n "$SERVER_PID" ]] && kill -0 "$SERVER_PID" 2>/dev/null; then
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

echo "==> Node tests"
if [[ "$SKIP_NODE" != "1" ]]; then
  npm test
fi

echo "==> Python tests"
DEMO_AUTH=true "$PYTHON" -m pytest backend/tests

echo "==> Detector evaluation"
"$PYTHON" backend/eval/run_eval.py

echo "==> Live local API"
export DEMO_AUTH=true
export BIND_HOST=127.0.0.1
export OFFLINE_MODE=true
export STORE_RAW_MESSAGES=false
export PORT
"$PYTHON" backend/app.py >/tmp/mindmend-verify.log 2>&1 &
SERVER_PID=$!

ready=0
for _ in $(seq 1 40); do
  if curl -sf "$BASE/ready" >/dev/null; then
    ready=1
    break
  fi
  if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    echo "Server exited before becoming ready:" >&2
    cat /tmp/mindmend-verify.log >&2
    exit 1
  fi
  sleep 0.25
done
if [[ "$ready" -ne 1 ]]; then
  echo "Timed out waiting for /ready" >&2
  cat /tmp/mindmend-verify.log >&2
  exit 1
fi

"$PYTHON" - <<'PY'
import json
import os
import urllib.request

base = os.environ["BASE"]

def get(path, headers=None):
    req = urllib.request.Request(base + path, headers=headers or {})
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.load(resp), resp.read if False else resp.getheader("Content-Type")

def get_text(path):
    with urllib.request.urlopen(base + path) as resp:
        return resp.status, resp.read().decode("utf-8", errors="replace"), resp.getheader("Content-Type")

status, health, _ = get("/api/v1/health")
assert status == 200
assert health["status"] == "healthy"
assert health["service"] == "MindMend Empathy Anchor"
assert health["version"]

status, ready, _ = get("/api/v1/ready")
assert status == 200
assert ready["status"] == "ready"
assert ready["storage"]["ok"] is True

status, resources, _ = get("/api/v1/resources")
assert status == 200
blob = json.dumps(resources)
assert "HOME to 741741" in blob
assert "Call or text 988" in blob
assert "1-844-464-3274" not in blob
assert resources["verified_on"] == "2026-08-17"

status, html, ctype = get_text("/")
assert status == 200
assert "MindMend Empathy Anchor" in html

status, docs, ctype = get_text("/docs/PRIVACY.md")
assert status == 200
assert "<html" in docs.lower()
assert "text/html" in (ctype or "")

req = urllib.request.Request(
    base + "/api/v1/auth/login",
    data=json.dumps({"user_id": "verify"}).encode(),
    headers={"Content-Type": "application/json"},
    method="POST",
)
login = json.load(urllib.request.urlopen(req))
token = login["token"]
req = urllib.request.Request(
    base + "/api/v1/scan",
    data=json.dumps({"message": "I feel anxious and overwhelmed"}).encode(),
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    },
    method="POST",
)
scan = json.load(urllib.request.urlopen(req))
assert scan["ok"] is True
assert scan["data"]["summary"]["severity"] == "high"
assert scan["data"]["alert_created"] is True
print("live API checks passed")
print("scan ok", scan["data"]["summary"]["severity"])
PY

echo
echo "Verify passed. Showcase: $BASE/"
