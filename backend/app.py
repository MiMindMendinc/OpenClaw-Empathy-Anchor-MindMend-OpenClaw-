"""
OpenClaw Empathy Anchor — Flask backend

Privacy-first empathy and safety response layer for youth-support demos.
Supportive software — not therapy, not a medical device, not emergency service.

Endpoints:
  GET  /health
  GET  /           showcase UI
  GET  /demo       deterministic scan scenarios (no auth)
  POST /auth/login demo JWT when DEMO_AUTH=true
  POST /chat
  POST /location
  POST /night_mode
  GET  /alerts
  GET  /resources
  GET  /status     build/runtime evidence
"""

from __future__ import annotations

from datetime import datetime, timezone
from functools import wraps
import logging
import os
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import jwt
from datetime import timedelta

from alert_store import AlertStore
from luna_safety_core import LunaSafetyCore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_SECRET_KEY = 'mindmend-secret-key-change-in-production'
IS_PRODUCTION = os.environ.get('FLASK_ENV', '').lower() == 'production'
DEMO_AUTH = os.environ.get('DEMO_AUTH', 'false').lower() == 'true'
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', '')
VERSION = '0.1.0'
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


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_config() -> str:
    """Validate environment configuration and return the secret key to use."""
    if IS_PRODUCTION:
        if not JWT_SECRET_KEY:
            raise RuntimeError(
                'JWT_SECRET_KEY is required when FLASK_ENV=production. '
                'Generate one with: python -c "import secrets; print(secrets.token_hex(32))"'
            )
        if JWT_SECRET_KEY in {
            DEFAULT_SECRET_KEY,
            'demo-jwt-secret-change-for-real-deployments',
        }:
            raise RuntimeError(
                'JWT_SECRET_KEY must not use a documented demo value in production.'
            )
        return JWT_SECRET_KEY

    return JWT_SECRET_KEY or DEFAULT_SECRET_KEY


app = Flask(__name__, static_folder=None)
CORS(app, resources={r'/*': {'origins': ALLOWED_ORIGINS}})

app.config['SECRET_KEY'] = validate_config()
app.config['OFFLINE_MODE'] = os.environ.get('OFFLINE_MODE', 'true').lower() == 'true'
app.config['DEMO_AUTH'] = DEMO_AUTH
app.config['IS_PRODUCTION'] = IS_PRODUCTION

alert_store = AlertStore()
luna_core = LunaSafetyCore(
    offline_mode=app.config['OFFLINE_MODE'],
    use_spacy=False,
)

logger.info(
    'OpenClaw Empathy Anchor %s — offline=%s demo_auth=%s production=%s',
    VERSION,
    app.config['OFFLINE_MODE'],
    DEMO_AUTH,
    IS_PRODUCTION,
)


def token_required(f):
    """Require a valid JWT."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user_id = data.get('user_id')
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(*args, **kwargs)

    return decorated


def persist_alert(alert: dict, user_id: str) -> dict:
    return alert_store.save_alert(alert, user_id)


@app.route('/')
def showcase():
    """Serve the interactive showcase UI."""
    return send_from_directory(SHOWCASE_DIR, 'index.html')


@app.route('/showcase/<path:filename>')
def showcase_assets(filename: str):
    return send_from_directory(SHOWCASE_DIR, filename)


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'OpenClaw Empathy Anchor',
        'version': VERSION,
        'offline_mode': app.config['OFFLINE_MODE'],
        'demo_auth': DEMO_AUTH,
        'scanner': 'deterministic_keyword_pattern',
        'timestamp': utc_now_iso(),
    })


@app.route('/status', methods=['GET'])
def status():
    """Runtime evidence for demos and recruiters — what is actually running."""
    return jsonify({
        'version': VERSION,
        'release': 'v0.1.0-local-safety-demo',
        'offline_mode': app.config['OFFLINE_MODE'],
        'demo_auth_enabled': DEMO_AUTH,
        'production_mode': IS_PRODUCTION,
        'alert_store': 'sqlite_local',
        'alert_db_path': os.environ.get('ALERT_DB_PATH', 'data/alerts.db'),
        'scanner': {
            'type': 'deterministic_keyword_pattern',
            'spacy': False,
            'clinical_validation': False,
        },
        'cors_origins': ALLOWED_ORIGINS,
        'boundaries': [
            'supportive prototype',
            'not clinical software',
            'not an emergency service',
            'human review required',
        ],
        'timestamp': utc_now_iso(),
    })


@app.route('/auth/login', methods=['POST'])
def login():
    """
    Demo authentication — issues a JWT for any user_id when DEMO_AUTH=true.

    This is not identity verification. Disabled in production unless DEMO_AUTH=true.
    """
    if IS_PRODUCTION and not DEMO_AUTH:
        return jsonify({
            'error': 'Demo authentication is disabled in production.',
            'hint': 'Set DEMO_AUTH=true only for controlled demos, or implement real auth.',
        }), 403

    if not DEMO_AUTH and not IS_PRODUCTION:
        # Local runs still allow login when DEMO_AUTH is unset, but label it clearly.
        pass

    # Require explicit DEMO_AUTH for issuing tokens in all modes.
    if not DEMO_AUTH:
        return jsonify({
            'error': 'Demo authentication is disabled.',
            'hint': 'Set DEMO_AUTH=true to use /auth/login for local demos.',
        }), 403

    data = request.get_json(silent=True) or {}
    if 'user_id' not in data:
        return jsonify({'error': 'user_id is required'}), 400

    user_id = data['user_id']
    expiration = datetime.now(timezone.utc) + timedelta(hours=24)
    token = jwt.encode(
        {'user_id': user_id, 'exp': expiration},
        app.config['SECRET_KEY'],
        algorithm='HS256',
    )

    return jsonify({
        'token': token,
        'expires_at': expiration.isoformat(),
        'offline_mode': app.config['OFFLINE_MODE'],
        'demo_auth': True,
        'notice': 'Demo authentication — not production identity verification.',
    })


@app.route('/chat', methods=['POST'])
@token_required
def chat():
    data = request.get_json(silent=True) or {}
    if 'message' not in data:
        return jsonify({'error': 'message is required'}), 400

    message = data['message']
    context = data.get('context', {})

    scan_result = luna_core.scan_message(message, context)
    empathy_response = luna_core.generate_empathy_response(message, scan_result)

    alert_created = False
    alert = None

    if (not scan_result.get('safe')) or scan_result.get('severity') in ('critical', 'high'):
        alert = luna_core.create_alert(
            alert_type='safety_concern',
            severity=scan_result['severity'],
            message=f"Safety concern detected in chat: {scan_result['flags']}",
            metadata={
                'user_id': request.user_id,
                'original_message': message,
                'scan_result': scan_result,
            },
        )
        alert = persist_alert(alert, request.user_id)
        alert_created = True
        logger.warning('Alert created for user %s: %s', request.user_id, scan_result['severity'])

    return jsonify({
        'response': empathy_response,
        'scan_result': scan_result,
        'alert_created': alert_created,
        'alert': alert,
        'timestamp': utc_now_iso(),
    })


@app.route('/location', methods=['POST'])
@token_required
def check_location():
    data = request.get_json(silent=True) or {}
    if 'lat' not in data or 'lon' not in data:
        return jsonify({'error': 'lat and lon are required'}), 400

    try:
        lat = float(data['lat'])
        lon = float(data['lon'])
    except (TypeError, ValueError):
        return jsonify({'error': 'lat and lon must be numbers'}), 400

    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return jsonify({'error': 'lat/lon out of valid range'}), 400

    safe_zones = data.get('safe_zones', [])
    geofence_result = luna_core.check_geofence(lat, lon, safe_zones)

    alert_created = False
    alert = None

    if geofence_result.get('alert_parent'):
        alert = luna_core.create_alert(
            alert_type='geofence_violation',
            severity='high',
            message='Child is outside safe zone',
            metadata={
                'user_id': request.user_id,
                'location': geofence_result['current_location'],
                'distance_to_nearest': geofence_result['distance_to_nearest'],
            },
        )
        alert = persist_alert(alert, request.user_id)
        alert_created = True
        logger.warning('Geofence alert for user %s', request.user_id)

    return jsonify({
        **geofence_result,
        'alert_created': alert_created,
        'alert': alert,
    })


@app.route('/night_mode', methods=['POST'])
@token_required
def night_mode():
    data = request.get_json(silent=True) or {}
    action = data.get('action', 'check_time')
    message = data.get('message', '')
    allowed = {'check_time', 'get_calming_response', 'bedtime_reminder'}

    if action not in allowed:
        return jsonify({
            'error': 'Invalid action',
            'allowed_actions': sorted(allowed),
        }), 400

    night_status = luna_core.validate_night_mode_time()
    response_text = ''

    if action == 'check_time':
        if night_status['is_bedtime_window']:
            response_text = (
                "It's getting close to bedtime. Let's start winding down for the night."
            )
        elif night_status['is_night_mode']:
            response_text = "It's nighttime. I'm here if you need calming support."
        else:
            response_text = (
                "You're doing great. Remember to take care of yourself throughout the day."
            )
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


@app.route('/alerts', methods=['GET'])
@token_required
def get_alerts():
    alerts = alert_store.get_alerts_for_user(request.user_id)
    return jsonify({'alerts': alerts, 'count': len(alerts)})


@app.route('/demo', methods=['GET'])
def demo():
    """Deterministic safety scan scenarios — no auth, not clinical assessment."""
    chat_scenarios = [
        {'name': 'neutral', 'message': 'I had a good day at school today.'},
        {'name': 'distress', 'message': 'I feel anxious and overwhelmed about everything.'},
        {'name': 'crisis', 'message': 'I want to kill myself.'},
        {'name': 'night_mode', 'message': "I can't sleep and I'm scared."},
    ]

    results = []
    for scenario in chat_scenarios:
        scan_result = luna_core.scan_message(scenario['message'])
        results.append({
            'scenario': scenario['name'],
            'message': scenario['message'],
            'scan_result': scan_result,
            'response_preview': luna_core.generate_empathy_response(
                scenario['message'],
                scan_result,
            )[:240],
        })

    geofence_demo = luna_core.check_geofence(
        lat=43.0,
        lon=-84.2,
        safe_zones=[{
            'lat': 42.9956,
            'lon': -84.1762,
            'radius': 100,
            'name': 'Home (Owosso, MI)',
        }],
    )

    return jsonify({
        'disclaimer': (
            'Supportive safety prototype — not clinical software, not an emergency service. '
            'Deterministic keyword/pattern scanner.'
        ),
        'chat_scenarios': results,
        'geofence_scenario': {
            'name': 'geofence_violation',
            'description': 'Location outside defined safe zone (Owosso, MI demo)',
            'result': geofence_demo,
        },
        'timestamp': utc_now_iso(),
    })


@app.route('/resources', methods=['GET'])
def get_resources():
    """Informational crisis resource routing — not clinical validation."""
    return jsonify({
        'crisis_resources': luna_core.CRISIS_RESOURCES,
        'notice': (
            'Informational routing only. If someone may be in immediate danger, '
            'call or text 988 or contact emergency services.'
        ),
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error('Internal error: %s', error)
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    logger.info('Starting OpenClaw Empathy Anchor on port %s', port)
    app.run(host='0.0.0.0', port=port, debug=debug)
