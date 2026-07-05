"""
MindMend Super AI - Flask Backend API
Privacy-first unified app for youth mental health and safety

API Endpoints:
- /chat - Empathy chat with safety scanning
- /location - Geofence checking
- /night_mode - Bedtime routine and calming support
- /auth - JWT authentication (demo mode when DEMO_AUTH=true)
- /alerts - Parent alert management (SQLite persistence)
- /demo - Safety scan demonstrations
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
from functools import wraps
import os
import logging

from luna_safety_core import LunaSafetyCore
from alert_store import AlertStore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_SECRET_KEY = 'mindmend-secret-key-change-in-production'
IS_PRODUCTION = os.environ.get('FLASK_ENV', '').lower() == 'production'
DEMO_AUTH = os.environ.get('DEMO_AUTH', 'false').lower() == 'true'
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', '')


def validate_config() -> str:
    """Validate environment configuration and return the secret key to use."""
    if IS_PRODUCTION:
        if not JWT_SECRET_KEY:
            raise RuntimeError(
                'JWT_SECRET_KEY is required when FLASK_ENV=production. '
                'Generate one with: python -c "import secrets; print(secrets.token_hex(32))"'
            )
        if JWT_SECRET_KEY == DEFAULT_SECRET_KEY:
            raise RuntimeError(
                'JWT_SECRET_KEY must not use the default demo value in production.'
            )
        return JWT_SECRET_KEY

    return JWT_SECRET_KEY or DEFAULT_SECRET_KEY


# Initialize Flask app
app = Flask(__name__)
CORS(app)

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
    'MindMend Super AI Backend Started - Offline Mode: %s, Demo Auth: %s, Production: %s',
    app.config['OFFLINE_MODE'],
    DEMO_AUTH,
    IS_PRODUCTION,
)


def token_required(f):
    """Decorator to require valid JWT token."""
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


def _persist_alert(alert: dict, user_id: str) -> dict:
    """Save alert to local SQLite store."""
    return alert_store.save_alert(alert, user_id)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'MindMend Super AI',
        'offline_mode': app.config['OFFLINE_MODE'],
        'demo_auth': DEMO_AUTH,
        'timestamp': datetime.utcnow().isoformat(),
    })


@app.route('/auth/login', methods=['POST'])
def login():
    """
    Demo authentication — issues a JWT for any user_id when DEMO_AUTH=true.

    In production without DEMO_AUTH, this endpoint is disabled.
    This is not real authentication; use proper identity verification for production.
    """
    if IS_PRODUCTION and not DEMO_AUTH:
        return jsonify({
            'error': 'Demo authentication is disabled in production.',
            'hint': 'Set DEMO_AUTH=true only for controlled demo deployments, '
                    'or implement proper authentication.',
        }), 403

    data = request.get_json()

    if not data or 'user_id' not in data:
        return jsonify({'error': 'user_id is required'}), 400

    user_id = data['user_id']
    expiration = datetime.utcnow() + timedelta(hours=24)
    token = jwt.encode({
        'user_id': user_id,
        'exp': expiration,
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({
        'token': token,
        'expires_at': expiration.isoformat(),
        'offline_mode': app.config['OFFLINE_MODE'],
        'demo_auth': True,
        'notice': 'Demo authentication — not for production use without proper auth.',
    })


@app.route('/chat', methods=['POST'])
@token_required
def chat():
    """
    Chat endpoint with empathy support and safety scanning.

    Creates and persists alerts when crisis or high-severity distress is detected.
    """
    data = request.get_json()

    if not data or 'message' not in data:
        return jsonify({'error': 'message is required'}), 400

    message = data['message']
    context = data.get('context', {})

    scan_result = luna_core.scan_message(message, context)
    empathy_response = luna_core.generate_empathy_response(message, scan_result)

    alert_created = False
    alert = None

    if not scan_result['safe'] or scan_result['severity'] in ['critical', 'high']:
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
        alert = _persist_alert(alert, request.user_id)
        alert_created = True
        logger.warning(
            'Alert created for user %s: %s',
            request.user_id,
            scan_result['severity'],
        )

    return jsonify({
        'response': empathy_response,
        'scan_result': scan_result,
        'alert_created': alert_created,
        'alert': alert,
        'timestamp': datetime.utcnow().isoformat(),
    })


@app.route('/location', methods=['POST'])
@token_required
def check_location():
    """Check geofence location and persist alerts when outside safe zones."""
    data = request.get_json()

    if not data or 'lat' not in data or 'lon' not in data:
        return jsonify({'error': 'lat and lon are required'}), 400

    lat = float(data['lat'])
    lon = float(data['lon'])
    safe_zones = data.get('safe_zones', [])

    geofence_result = luna_core.check_geofence(lat, lon, safe_zones)

    alert_created = False
    alert = None

    if geofence_result['alert_parent']:
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
        alert = _persist_alert(alert, request.user_id)
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
    """Night mode endpoint for bedtime support."""
    data = request.get_json() or {}

    action = data.get('action', 'check_time')
    message = data.get('message', '')

    night_status = luna_core.validate_night_mode_time()
    response_text = ''

    if action == 'check_time':
        if night_status['is_bedtime_window']:
            response_text = (
                "It's getting close to bedtime. Let's start winding down for the night. 🌙"
            )
        elif night_status['is_night_mode']:
            response_text = "It's nighttime. I'm here if you need calming support. 💙"
        else:
            response_text = (
                "You're doing great! Remember to take care of yourself throughout the day."
            )

    elif action == 'get_calming_response':
        if message:
            scan_result = luna_core.scan_message(message)
            response_text = luna_core.generate_empathy_response(message, scan_result)
        else:
            response_text = luna_core._generate_night_mode_response("can't sleep", {})

    elif action == 'bedtime_reminder':
        response_text = "🌙 Bedtime Reminder:\n\n"
        response_text += "• Finish any activities\n"
        response_text += "• Get ready for bed\n"
        response_text += "• Take some deep breaths\n"
        response_text += "• Think of something peaceful\n\n"
        response_text += "Sleep well! Tomorrow is a new day. 💙"

    return jsonify({
        'response': response_text,
        'night_mode_status': night_status,
        'recommendations': night_status['recommendations'],
        'timestamp': datetime.utcnow().isoformat(),
    })


@app.route('/alerts', methods=['GET'])
@token_required
def get_alerts():
    """Return persisted alerts for the authenticated user."""
    alerts = alert_store.get_alerts_for_user(request.user_id)
    return jsonify({
        'alerts': alerts,
        'count': len(alerts),
    })


@app.route('/demo', methods=['GET'])
def demo():
    """
    Demonstrate deterministic safety scanning for common scenarios.

    No authentication required. Returns scan results only — not clinical assessment.
    """
    chat_scenarios = [
        {
            'name': 'neutral',
            'message': 'I had a good day at school today.',
        },
        {
            'name': 'distress',
            'message': 'I feel anxious and overwhelmed about everything.',
        },
        {
            'name': 'crisis',
            'message': 'I want to kill myself.',
        },
        {
            'name': 'night_mode',
            'message': "I can't sleep and I'm scared.",
        },
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
            )[:200],
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
            'Deterministic keyword/pattern scanner for demo purposes.'
        ),
        'chat_scenarios': results,
        'geofence_scenario': {
            'name': 'geofence_violation',
            'description': 'Location outside defined safe zone (Owosso, MI demo)',
            'result': geofence_demo,
        },
        'timestamp': datetime.utcnow().isoformat(),
    })


@app.route('/resources', methods=['GET'])
def get_resources():
    """Get crisis and support resources."""
    return jsonify({
        'crisis_resources': luna_core.CRISIS_RESOURCES,
        'donation_links': {
            'gofundme': 'https://gofund.me/42b8334bd',
            'cashapp': 'https://cash.app/$MichiganMindMendinc',
        },
        'demo': {
            'eve_ai': 'https://kid-helper-ai.replit.app',
        },
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error('Internal error: %s', error)
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'

    logger.info('Starting MindMend Super AI Backend on port %s', port)
    app.run(host='0.0.0.0', port=port, debug=debug)
