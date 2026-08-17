#!/bin/sh
# Ensure the alert database directory is writable. Host bind-mounts are often
# owned by a different uid than the container user; fall back to /tmp so the
# demo still becomes ready instead of 503-ing.
set -e
DB_PATH="${ALERT_DB_PATH:-/app/data/alerts.db}"
DB_DIR="$(dirname "$DB_PATH")"
mkdir -p "$DB_DIR" 2>/dev/null || true
if ! touch "$DB_DIR/.write_test" 2>/dev/null; then
  echo "WARN: $DB_DIR is not writable; using /tmp/mindmend-alerts.db" >&2
  export ALERT_DB_PATH=/tmp/mindmend-alerts.db
else
  rm -f "$DB_DIR/.write_test"
fi
exec python backend/app.py
