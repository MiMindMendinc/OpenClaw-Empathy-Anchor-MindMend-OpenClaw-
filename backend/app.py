"""
MindMend Empathy Anchor — Flask backend

Local-first safety signal demonstrator.
Technical demonstration — not clinical software, not an emergency service.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from functools import wraps
import logging
import os
import secrets
import time
import uuid
from collections import defaultdict, deque
from pathlib import Path

from flask import Flask, g, jsonify, request, send_from_directory
from flask_cors import CORS
import jwt

from alert_store import AlertStore
from luna_safety_core import LunaSafetyCore
from version import (
    API_VERSION,
    ORGANIZATION,
    PRODUCT_NAME,
    PRODUCT_SUBTITLE,
    PRODUCT_TAGLINE,
    PROJECT_STATUS,
    RELEASE,
    SCANNER_VERSION,
    SCHEMA_VERSION,
    STATUS_STATEMENT,
    VERSION,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_SECRET_KEY = 'mindmend-secret-key-change-in-production'
DEMO_SECRETS = {
    DEFAULT_SECRET_KEY,
    'demo-jwt-secret-change-for-real-deployments',
    'local-demo-only-not-for-production',
}
IS_PRODUCTION = os.environ.get('FLASK_ENV', '').lower() == 'production'
DEMO_AUTH = os.environ.get('DEMO_AUTH', 'false').lower() == 'true'
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', '')
STORE_RAW_MESSAGES = os.environ.get('STORE_RAW_MESSAGES', 'false').lower() == 'true'
RETENTION_DAYS = int(os.environ.get('ALERT_RETENTION_DAYS', '30') or '30')
MAX_MESSAGE_CHARS = int(os.environ.get('MAX_MESSAGE_CHARS', '4000'))
MAX_BODY_BYTES = int(os.environ.get('MAX_BODY_BYTES', '65536'))
RATE_LIMIT_PER_MINUTE = int(os.environ.get('RATE_LIMIT_PER_MINUTE', '60'))
BIND_HOST = os.environ.get('BIND_HOST', '127.0.0.1')
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        'CORS_ORIGINS',
        'http://localhost:8000,http://127.0.0.1:8000',
    ).split(',')
    if origin.strip()
]

ROOT_DIR = Path(__file__).resolve().parent.parent
SHOWCASE_DIR = ROOT_DIR / 'showcase'
DOCS_DIR = ROOT_DIR / 'docs'


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def utc_now_iso() -> str:
    return utc_now().isoformat()


def validate_config() -> str:
    if IS_PRODUCTION:
        if not JWT_SECRET_KEY:
            raise RuntimeError(
                'JWT_SECRET_KEY is required when FLASK_ENV=production. '
                'Generate one with: python -c "import secrets; print(secrets.token_hex(32))"'
            )
        if JWT_SECRET_KEY in DEMO_SECRETS:
            raise RuntimeError(
                'JWT_SECRET_KEY must not use a documented demo value in production.'
            )
        return JWT_SECRET_KEY
    return JWT_SECRET_KEY or DEFAULT_SECRET_KEY


def redact(text: str, keep: int = 24) -> str:
    if not text:
        return ''
    if len(text) <= keep:
        return '[redacted]'
    return text[:8] + '…[redacted]'


app = Flask(__name__, static_folder=None)
app.config['MAX_CONTENT_LENGTH'] = MAX_BODY_BYTES
CORS(app, resources={r'/*': {'origins': ALLOWED_ORIGINS}})

app.config['SECRET_KEY'] = validate_config()
app.config['OFFLINE_MODE'] = os.environ.get('OFFLINE_MODE', 'true').lower() == 'true'
app.config['DEMO_AUTH'] = DEMO_AUTH
app.config['IS_PRODUCTION'] = IS_PRODUCTION

alert_store = AlertStore(
    store_raw_messages=STORE_RAW_MESSAGES,
    retention_days=RETENTION_DAYS,
)
luna_core = LunaSafetyCore(
    offline_mode=app.config['OFFLINE_MODE'],
    use_spacy=False,
)

_rate_buckets: dict[str, deque] = defaultdict(deque)


logger.info(
    '%s %s — offline=%s demo_auth=%s production=%s bind_default=%s',
    PRODUCT_NAME,
    VERSION,
    app.config['OFFLINE_MODE'],
    DEMO_AUTH,
    IS_PRODUCTION,
    BIND_HOST,
)


@app.before_request
def before_request():
    g.request_id = request.headers.get('X-Request-ID') or uuid.uuid4().hex
    g.start = time.time()

    # Simple IP rate limit for API routes
    if request.path.startswith('/api/') or request.path in {
        '/chat', '/auth/login', '/alerts', '/location', '/night_mode', '/demo', '/scan',
    }:
        ip = request.headers.get('X-Forwarded-For', request.remote_addr or 'local').split(',')[0].strip()
        bucket = _rate_buckets[ip]
        now = time.time()
        while bucket and now - bucket[0] > 60:
            bucket.popleft()
        if len(bucket) >= RATE_LIMIT_PER_MINUTE:
            return api_error('rate_limit_exceeded', 'Too many requests. Try again shortly.', 429)
        bucket.append(now)


@app.after_request
def after_request(response):
    response.headers['X-Request-ID'] = getattr(g, 'request_id', '')
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    response.headers['Cache-Control'] = 'no-store'
    if request.path.startswith('/api/') or request.path.endswith('.json'):
        response.headers['Content-Security-Policy'] = "default-src 'none'; frame-ancestors 'none'"
    return response


def api_ok(data: dict, status: int = 200):
    payload = {
        'ok': True,
        'request_id': getattr(g, 'request_id', None),
        'api_version': API_VERSION,
        'product': PRODUCT_NAME,
        'version': VERSION,
        'data': data,
    }
    return jsonify(payload), status


def api_error(code: str, message: str, status: int = 400, **extra):
    payload = {
        'ok': False,
        'request_id': getattr(g, 'request_id', None),
        'api_version': API_VERSION,
        'error': {
            'code': code,
            'message': message,
            **extra,
        },
    }
    return jsonify(payload), status


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return api_error('unauthorized', 'Token is missing', 401)
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user_id = data.get('user_id')
            if not request.user_id:
                return api_error('unauthorized', 'Invalid token subject', 401)
        except jwt.ExpiredSignatureError:
            return api_error('unauthorized', 'Token has expired', 401)
        except jwt.InvalidTokenError:
            return api_error('unauthorized', 'Invalid token', 401)
        return f(*args, **kwargs)

    return decorated


def validate_message(data: dict):
    if not isinstance(data, dict) or 'message' not in data:
        return None, api_error('validation_error', 'message is required', 400)
    message = data.get('message')
    if not isinstance(message, str):
        return None, api_error('validation_error', 'message must be a string', 400)
    if len(message) > MAX_MESSAGE_CHARS:
        return None, api_error(
            'validation_error',
            f'message exceeds max length of {MAX_MESSAGE_CHARS} characters',
            400,
        )
    return message, None


def human_result(scan_result: dict, alert: dict | None = None, alert_created: bool = False) -> dict:
    flags = scan_result.get('flags') or {}
    categories = [name for name, on in flags.items() if on]
    matches = {
        k: v for k, v in (scan_result.get('matches') or {}).items() if v
    }
    return {
        'severity': scan_result.get('severity', 'low'),
        'detected_categories': categories,
        'matched_indicators': matches,
        'recommended_actions': scan_result.get('recommended_actions') or scan_result.get('actions') or [],
        'alert_persisted': alert_created,
        'alert_id': alert.get('id') if alert else None,
        'created_at': alert.get('created_at') if alert else scan_result.get('timestamp'),
        'storage_mode': 'sqlite_local' if alert_created else 'none',
        'scanner_version': scan_result.get('scanner_version', SCANNER_VERSION),
        'scanner_method': scan_result.get('scanner_method', 'deterministic_keyword_pattern'),
        'quoted_context_suspected': scan_result.get('quoted_context_suspected', False),
        'resources': scan_result.get('resources'),
        'note': (
            'Recommended actions are guidance only. No parent, clinician, or emergency '
            'service was contacted automatically.'
        ),
    }


# --------------- Static / pages ---------------

@app.route('/')
def showcase():
    return send_from_directory(SHOWCASE_DIR, 'index.html')


@app.route('/showcase/<path:filename>')
def showcase_assets(filename: str):
    return send_from_directory(SHOWCASE_DIR, filename)


@app.route('/docs/<path:filename>')
def docs_assets(filename: str):
    return send_from_directory(DOCS_DIR, filename)


# --------------- Health / meta ---------------

@app.route('/health', methods=['GET'])
@app.route('/api/v1/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': PRODUCT_NAME,
        'version': VERSION,
        'timestamp': utc_now_iso(),
    })


@app.route('/ready', methods=['GET'])
@app.route('/api/v1/ready', methods=['GET'])
def ready_check():
    storage = alert_store.ready()
    ready = bool(storage.get('ok'))
    body = {
        'status': 'ready' if ready else 'not_ready',
        'storage': storage,
        'scanner_version': SCANNER_VERSION,
        'schema_version': SCHEMA_VERSION,
        'demo_auth': DEMO_AUTH,
        'offline_mode': app.config['OFFLINE_MODE'],
        'timestamp': utc_now_iso(),
    }
    return jsonify(body), (200 if ready else 503)


@app.route('/version', methods=['GET'])
@app.route('/api/v1/version', methods=['GET'])
@app.route('/status', methods=['GET'])
@app.route('/api/v1/status', methods=['GET'])
def status():
    return jsonify({
        'product': PRODUCT_NAME,
        'subtitle': PRODUCT_SUBTITLE,
        'organization': ORGANIZATION,
        'tagline': PRODUCT_TAGLINE,
        'version': VERSION,
        'release': RELEASE,
        'project_status': PROJECT_STATUS,
        'status_statement': STATUS_STATEMENT,
        'api_version': API_VERSION,
        'offline_mode': app.config['OFFLINE_MODE'],
        'demo_auth_enabled': DEMO_AUTH,
        'production_mode': IS_PRODUCTION,
        'store_raw_messages': STORE_RAW_MESSAGES,
        'alert_retention_days': RETENTION_DAYS,
        'alert_store': 'sqlite_local',
        'scanner': {
            'type': 'deterministic_keyword_pattern',
            'version': SCANNER_VERSION,
            'spacy': False,
            'clinical_validation': False,
            'language': 'en',
            'multi_message_context': False,
        },
        'cors_origins': ALLOWED_ORIGINS,
        'bind_host_default': BIND_HOST,
        'boundaries': [
            'supportive technical demonstration',
            'not clinical software',
            'not an emergency service',
            'human review required',
        ],
        'timestamp': utc_now_iso(),
    })


# --------------- Auth ---------------

@app.route('/auth/login', methods=['POST'])
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    if not DEMO_AUTH:
        return api_error(
            'demo_auth_disabled',
            'Demo authentication is disabled. Set DEMO_AUTH=true for local demos only.',
            403,
        )

    data = request.get_json(silent=True) or {}
    user_id = data.get('user_id')
    if not user_id or not isinstance(user_id, str) or len(user_id) > 128:
        return api_error('validation_error', 'user_id is required (string, max 128)', 400)

    expiration = utc_now() + timedelta(hours=24)
    token = jwt.encode(
        {'user_id': user_id, 'exp': expiration},
        app.config['SECRET_KEY'],
        algorithm='HS256',
    )
    # Dual shape: legacy top-level fields + versioned envelope fields.
    body = {
        'ok': True,
        'request_id': getattr(g, 'request_id', None),
        'api_version': API_VERSION,
        'token': token,
        'expires_at': expiration.isoformat(),
        'offline_mode': app.config['OFFLINE_MODE'],
        'demo_auth': True,
        'notice': 'Demo authentication — not production identity verification.',
        'data': {
            'token': token,
            'expires_at': expiration.isoformat(),
            'demo_auth': True,
        },
    }
    return jsonify(body)


# --------------- Scan / chat ---------------

@app.route('/api/v1/scan', methods=['POST'])
@app.route('/scan', methods=['POST'])
@token_required
def scan():
    data = request.get_json(silent=True) or {}
    message, err = validate_message(data)
    if err:
        return err

    persist = bool(data.get('persist_alert', True))
    scan_result = luna_core.scan_message(message, data.get('context') or {})
    empathy = luna_core.generate_empathy_response(message, scan_result)

    alert = None
    alert_created = False
    if persist and ((not scan_result.get('safe')) or scan_result.get('severity') in ('critical', 'high')):
        metadata = {
            'user_id': request.user_id,
            'scan_result': {
                'severity': scan_result.get('severity'),
                'flags': scan_result.get('flags'),
                'matches': scan_result.get('matches'),
                'recommended_actions': scan_result.get('recommended_actions'),
                'scanner_version': scan_result.get('scanner_version'),
            },
        }
        if STORE_RAW_MESSAGES:
            metadata['original_message'] = message
        alert = luna_core.create_alert(
            alert_type='safety_concern',
            severity=scan_result['severity'],
            message=f"Safety concern detected ({scan_result['severity']})",
            metadata=metadata,
        )
        alert = alert_store.save_alert(alert, request.user_id)
        alert_created = True
        logger.warning(
            'Alert created user=%s severity=%s request_id=%s',
            request.user_id,
            scan_result.get('severity'),
            g.request_id,
        )

    return api_ok({
        'summary': human_result(scan_result, alert, alert_created),
        'response': empathy,
        'scan_result': scan_result,
        'alert_created': alert_created,
        'alert': alert,
        'timestamp': utc_now_iso(),
    })


@app.route('/chat', methods=['POST'])
@app.route('/api/v1/chat', methods=['POST'])
@token_required
def chat():
    # Compatibility wrapper around /scan
    data = request.get_json(silent=True) or {}
    data['persist_alert'] = True
    request_json = data
    # Reuse scan logic by calling internals
    message, err = validate_message(request_json)
    if err:
        return err
    scan_result = luna_core.scan_message(message, request_json.get('context') or {})
    empathy = luna_core.generate_empathy_response(message, scan_result)
    alert = None
    alert_created = False
    if (not scan_result.get('safe')) or scan_result.get('severity') in ('critical', 'high'):
        metadata = {
            'user_id': request.user_id,
            'scan_result': {
                'severity': scan_result.get('severity'),
                'flags': scan_result.get('flags'),
                'matches': scan_result.get('matches'),
                'recommended_actions': scan_result.get('recommended_actions'),
                'scanner_version': scan_result.get('scanner_version'),
            },
        }
        if STORE_RAW_MESSAGES:
            metadata['original_message'] = message
        alert = luna_core.create_alert(
            alert_type='safety_concern',
            severity=scan_result['severity'],
            message=f"Safety concern detected ({scan_result['severity']})",
            metadata=metadata,
        )
        alert = alert_store.save_alert(alert, request.user_id)
        alert_created = True
        logger.warning(
            'Alert created user=%s severity=%s request_id=%s',
            request.user_id,
            scan_result.get('severity'),
            g.request_id,
        )

    # Preserve legacy response shape for existing tests + envelope for new clients
    legacy = {
        'response': empathy,
        'scan_result': scan_result,
        'alert_created': alert_created,
        'alert': alert,
        'summary': human_result(scan_result, alert, alert_created),
        'timestamp': utc_now_iso(),
    }
    return jsonify(legacy)


@app.route('/location', methods=['POST'])
@app.route('/api/v1/location', methods=['POST'])
@token_required
def check_location():
    data = request.get_json(silent=True) or {}
    if 'lat' not in data or 'lon' not in data:
        return api_error('validation_error', 'lat and lon are required', 400)
    try:
        lat = float(data['lat'])
        lon = float(data['lon'])
    except (TypeError, ValueError):
        return api_error('validation_error', 'lat and lon must be numbers', 400)
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return api_error('validation_error', 'lat/lon out of valid range', 400)

    safe_zones = data.get('safe_zones', [])
    if not isinstance(safe_zones, list) or len(safe_zones) > 50:
        return api_error('validation_error', 'safe_zones must be a list of up to 50 zones', 400)

    geofence_result = luna_core.check_geofence(lat, lon, safe_zones)
    alert = None
    alert_created = False
    if geofence_result.get('alert_parent'):
        alert = luna_core.create_alert(
            alert_type='geofence_violation',
            severity='high',
            message='Location outside configured safe zone',
            metadata={
                'user_id': request.user_id,
                'location': geofence_result.get('current_location'),
                'distance_to_nearest': geofence_result.get('distance_to_nearest'),
            },
        )
        alert = alert_store.save_alert(alert, request.user_id)
        alert_created = True
        logger.warning('Geofence alert user=%s request_id=%s', request.user_id, g.request_id)

    return jsonify({
        **geofence_result,
        'alert_created': alert_created,
        'alert': alert,
        'note': 'Geofence alerts are local recommendations, not automatic emergency contact.',
    })


@app.route('/night_mode', methods=['POST'])
@app.route('/api/v1/night_mode', methods=['POST'])
@token_required
def night_mode():
    data = request.get_json(silent=True) or {}
    action = data.get('action', 'check_time')
    message = data.get('message', '')
    allowed = {'check_time', 'get_calming_response', 'bedtime_reminder'}
    if action not in allowed:
        return api_error('validation_error', 'Invalid action', 400, allowed_actions=sorted(allowed))
    if message and len(message) > MAX_MESSAGE_CHARS:
        return api_error('validation_error', f'message exceeds max length of {MAX_MESSAGE_CHARS}', 400)

    night_status = luna_core.validate_night_mode_time()
    response_text = ''
    if action == 'check_time':
        if night_status['is_bedtime_window']:
            response_text = "It's getting close to bedtime. Let's start winding down for the night."
        elif night_status['is_night_mode']:
            response_text = "It's nighttime. I'm here if you need calming support."
        else:
            response_text = "You're doing great. Remember to take care of yourself throughout the day."
    elif action == 'get_calming_response':
        if message:
            scan_result = luna_core.scan_message(message)
            response_text = luna_core.generate_empathy_response(message, scan_result)
        else:
            response_text = luna_core._generate_night_mode_response("can't sleep", {})
    elif action == 'bedtime_reminder':
        response_text = (
            'Bedtime reminder:\n'
            '• Finish any activities\n'
            '• Get ready for bed\n'
            '• Take some deep breaths\n'
            '• Think of something peaceful\n\n'
            'Sleep well. Tomorrow is a new day.'
        )

    return jsonify({
        'response': response_text,
        'night_mode_status': night_status,
        'recommendations': night_status['recommendations'],
        'timestamp': utc_now_iso(),
    })


# --------------- Alerts ---------------

@app.route('/alerts', methods=['GET'])
@app.route('/api/v1/alerts', methods=['GET'])
@token_required
def get_alerts():
    alert_store.purge_expired()
    alerts = alert_store.get_alerts_for_user(request.user_id)
    return jsonify({'alerts': alerts, 'count': len(alerts)})


@app.route('/api/v1/alerts/<alert_id>', methods=['GET'])
@token_required
def get_alert(alert_id: str):
    alert = alert_store.get_alert(alert_id, request.user_id)
    if not alert:
        return api_error('not_found', 'Alert not found', 404)
    return api_ok({'alert': alert})


@app.route('/api/v1/alerts/<alert_id>', methods=['DELETE'])
@token_required
def delete_alert(alert_id: str):
    deleted = alert_store.delete_alert(alert_id, request.user_id)
    if not deleted:
        return api_error('not_found', 'Alert not found', 404)
    return api_ok({'deleted': True, 'id': alert_id})


@app.route('/api/v1/alerts', methods=['DELETE'])
@token_required
def delete_user_alerts():
    count = alert_store.delete_alerts_for_user(request.user_id)
    return api_ok({'deleted_count': count})


@app.route('/api/v1/admin/reset', methods=['POST'])
@token_required
def admin_reset():
    """Local demo reset for the authenticated user only."""
    count = alert_store.delete_alerts_for_user(request.user_id)
    return api_ok({
        'reset': True,
        'deleted_count': count,
        'scope': 'authenticated_user_alerts_only',
        'notice': 'Full local DB wipe: stop the service and delete the SQLite file documented in PRIVACY.md.',
    })


# --------------- Demo / resources ---------------

@app.route('/demo', methods=['GET'])
@app.route('/api/v1/demo', methods=['GET'])
def demo():
    chat_scenarios = [
        {'name': 'neutral', 'message': 'I had a good day at school today.'},
        {'name': 'distress', 'message': 'I feel anxious and overwhelmed about everything.'},
        {'name': 'night_mode', 'message': "I can't sleep and I'm scared."},
        # Crisis example intentionally last and not promotional.
        {'name': 'crisis', 'message': 'I want to kill myself.'},
    ]
    results = []
    for scenario in chat_scenarios:
        scan_result = luna_core.scan_message(scenario['message'])
        results.append({
            'scenario': scenario['name'],
            'message': scenario['message'] if scenario['name'] != 'crisis' else '[sensitive example withheld in listing — select crisis scenario in UI]',
            'scan_result': scan_result,
            'summary': human_result(scan_result),
            'response_preview': luna_core.generate_empathy_response(
                scenario['message'], scan_result
            )[:240],
        })
        # Keep technical demo usable: still include scan from real message above.

    # Restore accurate crisis scan for machine consumers while UI can hide phrase
    crisis_msg = 'I want to kill myself.'
    crisis_scan = luna_core.scan_message(crisis_msg)
    for item in results:
        if item['scenario'] == 'crisis':
            item['scan_result'] = crisis_scan
            item['summary'] = human_result(crisis_scan)
            item['response_preview'] = luna_core.generate_empathy_response(crisis_msg, crisis_scan)[:240]
            item['sensitive_example'] = True

    geofence_demo = luna_core.check_geofence(
        lat=43.0,
        lon=-84.2,
        safe_zones=[{
            'lat': 42.0,
            'lon': -84.0,
            'radius': 100,
            'name': 'Home (demo)',
        }],
    )

    return jsonify({
        'disclaimer': STATUS_STATEMENT,
        'content_notice': (
            'Some scenarios involve sensitive safety language for verification only. '
            'This is not clinical assessment.'
        ),
        'chat_scenarios': results,
        'geofence_scenario': {
            'name': 'geofence_violation',
            'description': 'Location outside defined safe zone (demo)',
            'result': geofence_demo,
        },
        'scanner_version': SCANNER_VERSION,
        'timestamp': utc_now_iso(),
    })


@app.route('/resources', methods=['GET'])
@app.route('/api/v1/resources', methods=['GET'])
def get_resources():
    region = (request.args.get('region') or 'us-mi').lower()
    return jsonify({
        'region': region,
        'crisis_resources': luna_core.CRISIS_RESOURCES,
        'notice': (
            'Informational routing only. Availability is not guaranteed. '
            'If someone may be in immediate danger, call or text 988 (US) '
            'or contact local emergency services.'
        ),
    })


@app.errorhandler(404)
def not_found(error):
    return api_error('not_found', 'Endpoint not found', 404)


@app.errorhandler(413)
def too_large(error):
    return api_error('payload_too_large', 'Request body too large', 413)


@app.errorhandler(500)
def internal_error(error):
    logger.error('Internal error request_id=%s', getattr(g, 'request_id', None))
    return api_error('internal_error', 'Internal server error', 500)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    host = os.environ.get('BIND_HOST', BIND_HOST)
    if host not in ('127.0.0.1', 'localhost') and os.environ.get('ALLOW_LAN_BIND', '').lower() != 'true':
        logger.warning(
            'BIND_HOST=%s requested without ALLOW_LAN_BIND=true; falling back to 127.0.0.1. '
            'LAN HTTP is not encrypted.',
            host,
        )
        host = '127.0.0.1'
    if host in ('0.0.0.0', '::'):
        logger.warning('Listening on all interfaces. Use TLS via a reverse proxy for any non-local access.')
    logger.info('Starting %s on %s:%s', PRODUCT_NAME, host, port)
    app.run(host=host, port=port, debug=debug)
