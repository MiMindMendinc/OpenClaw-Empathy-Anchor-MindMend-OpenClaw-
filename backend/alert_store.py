"""
SQLite alert persistence for local-first, privacy-first alert storage.
All data stays on-device; no cloud dependency required.
"""

import json
import os
import sqlite3
import uuid
from datetime import datetime
from typing import Dict, List, Optional


DEFAULT_DB_PATH = os.environ.get(
    'ALERT_DB_PATH',
    os.path.join(os.path.dirname(__file__), '..', 'data', 'alerts.db'),
)


class AlertStore:
    """Local SQLite store for parent/caregiver safety alerts."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or DEFAULT_DB_PATH
        db_dir = os.path.dirname(os.path.abspath(self.db_path))
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS alerts (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    alert_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    message TEXT NOT NULL,
                    metadata TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                'CREATE INDEX IF NOT EXISTS idx_alerts_user_id ON alerts(user_id)'
            )
            conn.commit()

    def save_alert(self, alert: Dict, user_id: str) -> Dict:
        """Persist an alert and return the stored record."""
        alert_id = alert.get('id') or f"alert_{uuid.uuid4().hex[:12]}"
        created_at = alert.get('timestamp') or datetime.utcnow().isoformat()
        alert_type = alert.get('type') or alert.get('alert_type', 'unknown')
        metadata = json.dumps(alert.get('metadata') or {})

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO alerts
                    (id, user_id, alert_type, severity, message, metadata, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    alert_id,
                    user_id,
                    alert_type,
                    alert.get('severity', 'low'),
                    alert.get('message', ''),
                    metadata,
                    created_at,
                ),
            )
            conn.commit()

        return {
            'id': alert_id,
            'user_id': user_id,
            'alert_type': alert_type,
            'severity': alert.get('severity', 'low'),
            'message': alert.get('message', ''),
            'metadata': alert.get('metadata') or {},
            'created_at': created_at,
        }

    def get_alerts_for_user(self, user_id: str, limit: int = 100) -> List[Dict]:
        """Return alerts for a user, newest first."""
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, user_id, alert_type, severity, message, metadata, created_at
                FROM alerts
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (user_id, limit),
            ).fetchall()

        return [self._row_to_dict(row) for row in rows]

    def _row_to_dict(self, row: sqlite3.Row) -> Dict:
        metadata = row['metadata']
        return {
            'id': row['id'],
            'user_id': row['user_id'],
            'alert_type': row['alert_type'],
            'severity': row['severity'],
            'message': row['message'],
            'metadata': json.loads(metadata) if metadata else {},
            'created_at': row['created_at'],
        }

    def clear_all(self) -> None:
        """Remove all alerts. Intended for tests only."""
        with self._connect() as conn:
            conn.execute('DELETE FROM alerts')
            conn.commit()
