"""
SQLite alert persistence for local-first, privacy-first alert storage.

Defaults:
- No raw message text retained unless STORE_RAW_MESSAGES=true
- UTC timestamps
- Schema version tracked for migrations
"""

from __future__ import annotations

import json
import os
import sqlite3
import threading
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional


DEFAULT_DB_PATH = os.environ.get(
    'ALERT_DB_PATH',
    os.path.join(os.path.dirname(__file__), '..', 'data', 'alerts.db'),
)

SCHEMA_VERSION = 2


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class AlertStore:
    """Thread-aware local SQLite store for caregiver safety alerts."""

    def __init__(
        self,
        db_path: Optional[str] = None,
        store_raw_messages: bool = False,
        retention_days: Optional[int] = None,
    ):
        self.db_path = db_path or DEFAULT_DB_PATH
        self.store_raw_messages = store_raw_messages
        self.retention_days = retention_days
        self._lock = threading.RLock()
        db_dir = os.path.dirname(os.path.abspath(self.db_path))
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=5.0, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON')
        conn.execute('PRAGMA busy_timeout = 5000')
        return conn

    def _init_db(self) -> None:
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS schema_meta (
                        key TEXT PRIMARY KEY,
                        value TEXT NOT NULL
                    )
                    """
                )
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
                conn.execute(
                    'CREATE INDEX IF NOT EXISTS idx_alerts_created_at ON alerts(created_at)'
                )
                row = conn.execute(
                    "SELECT value FROM schema_meta WHERE key = 'schema_version'"
                ).fetchone()
                current = int(row['value']) if row else 1
                if current < SCHEMA_VERSION:
                    # Future migrations go here. v1->v2 is additive indexes only.
                    conn.execute(
                        """
                        INSERT INTO schema_meta(key, value) VALUES('schema_version', ?)
                        ON CONFLICT(key) DO UPDATE SET value = excluded.value
                        """,
                        (str(SCHEMA_VERSION),),
                    )
                elif not row:
                    conn.execute(
                        "INSERT INTO schema_meta(key, value) VALUES('schema_version', ?)",
                        (str(SCHEMA_VERSION),),
                    )
                conn.commit()

    def ready(self) -> Dict[str, Any]:
        """Return storage readiness without exposing paths by default."""
        try:
            with self._lock:
                with self._connect() as conn:
                    conn.execute('SELECT 1 FROM alerts LIMIT 1')
            return {'ok': True, 'engine': 'sqlite', 'schema_version': SCHEMA_VERSION}
        except sqlite3.Error as exc:
            return {'ok': False, 'engine': 'sqlite', 'error': 'database_unavailable', 'detail': str(exc)}

    def _sanitize_metadata(self, metadata: Optional[Dict]) -> Dict:
        meta = dict(metadata or {})
        if not self.store_raw_messages:
            meta.pop('original_message', None)
            if 'scan_result' in meta and isinstance(meta['scan_result'], dict):
                # Keep flags/severity/actions/matches; drop echoed raw text if present.
                scan = dict(meta['scan_result'])
                scan.pop('raw_message', None)
                meta['scan_result'] = scan
        return meta

    def save_alert(self, alert: Dict, user_id: str) -> Dict:
        """Persist an alert and return the stored record."""
        alert_id = alert.get('id') or f'alert_{uuid.uuid4().hex}'
        created_at = alert.get('timestamp') or utc_now_iso()
        if created_at.endswith('+00:00'):
            pass
        elif 'T' in created_at and not created_at.endswith('Z') and '+' not in created_at:
            created_at = f'{created_at}+00:00' if not created_at.endswith('Z') else created_at

        alert_type = alert.get('type') or alert.get('alert_type', 'unknown')
        metadata = self._sanitize_metadata(alert.get('metadata'))
        message = alert.get('message', '')
        if not self.store_raw_messages and 'original_message' in (alert.get('metadata') or {}):
            # Ensure summary message never embeds raw user text by accident.
            message = f"Safety concern detected ({alert.get('severity', 'unknown')})"

        with self._lock:
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
                        message,
                        json.dumps(metadata),
                        created_at,
                    ),
                )
                conn.commit()

        return {
            'id': alert_id,
            'user_id': user_id,
            'alert_type': alert_type,
            'severity': alert.get('severity', 'low'),
            'message': message,
            'metadata': metadata,
            'created_at': created_at,
            'storage_mode': 'sqlite_local',
            'raw_message_retained': self.store_raw_messages,
        }

    def get_alerts_for_user(self, user_id: str, limit: int = 100) -> List[Dict]:
        limit = max(1, min(int(limit), 500))
        with self._lock:
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

    def get_alert(self, alert_id: str, user_id: str) -> Optional[Dict]:
        with self._lock:
            with self._connect() as conn:
                row = conn.execute(
                    """
                    SELECT id, user_id, alert_type, severity, message, metadata, created_at
                    FROM alerts
                    WHERE id = ? AND user_id = ?
                    """,
                    (alert_id, user_id),
                ).fetchone()
        return self._row_to_dict(row) if row else None

    def delete_alert(self, alert_id: str, user_id: str) -> bool:
        with self._lock:
            with self._connect() as conn:
                cur = conn.execute(
                    'DELETE FROM alerts WHERE id = ? AND user_id = ?',
                    (alert_id, user_id),
                )
                conn.commit()
                return cur.rowcount > 0

    def delete_alerts_for_user(self, user_id: str) -> int:
        with self._lock:
            with self._connect() as conn:
                cur = conn.execute('DELETE FROM alerts WHERE user_id = ?', (user_id,))
                conn.commit()
                return cur.rowcount

    def purge_expired(self, retention_days: Optional[int] = None) -> int:
        days = retention_days if retention_days is not None else self.retention_days
        if not days or days <= 0:
            return 0
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        with self._lock:
            with self._connect() as conn:
                cur = conn.execute(
                    'DELETE FROM alerts WHERE created_at < ?',
                    (cutoff,),
                )
                conn.commit()
                return cur.rowcount

    def reset_all(self) -> None:
        """Delete all alerts. Local admin / test use only."""
        with self._lock:
            with self._connect() as conn:
                conn.execute('DELETE FROM alerts')
                conn.commit()

    def clear_all(self) -> None:
        """Alias for tests."""
        self.reset_all()

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
            'storage_mode': 'sqlite_local',
        }
