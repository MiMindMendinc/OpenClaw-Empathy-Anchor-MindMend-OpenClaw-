"""
MindMend Super AI - Flask Backend API
Privacy-first unified app for youth mental health and safety

API Endpoints:
- /chat - Empathy chat with safety scanning
- /location - Geofence checking
- /night_mode - Bedtime routine and calming support
- /auth - JWT authentication
- /alerts - Parent alert management
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
from functools import wraps
import os
import logging

from luna_safety_core import LunaSafetyCore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Configuration
app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'mindmend-secret-key-change-in-production')
app.config['OFFLINE_MODE'] = os.environ.get('OFFLINE_MODE', 'true').lower() == 'true'

# Initialize Luna Safety Core
luna_core = LunaSafetyCore(
    offline_mode=app.config['OFFLINE_MODE'],
    use_spacy=False  # Start with pattern matching, can enable spaCy later
)

logger.info(f"MindMend Super AI Backend Started - Offline Mode: {app.config['OFFLINE_MODE']}")


# JWT Authentication Decorator
def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
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


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'MindMend Super AI',
        'offline_mode': app.config['OFFLINE_MODE'],
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/auth/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT token
    
    Request body:
        {
            "user_id": "string",
            "password": "string" (or other auth method)
        }
    
    Returns:
        {
            "token": "jwt_token",
            "expires_at": "timestamp"
        }
    """
    data = request.get_json()
    
    if not data or 'user_id' not in data:
        return jsonify({'error': 'user_id is required'}), 400
    
    user_id = data['user_id']
    # In production, validate credentials properly
    # For now, generate token for any user_id (offline mode)
    
    # Generate JWT token (valid for 24 hours)
    expiration = datetime.utcnow() + timedelta(hours=24)
    token = jwt.encode({
        'user_id': user_id,
        'exp': expiration
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'token': token,
        'expires_at': expiration.isoformat(),
        'offline_mode': app.config['OFFLINE_MODE']
    })


@app.route('/chat', methods=['POST'])
@token_required
def chat():
    """
    Chat endpoint with empathy support and safety scanning
    
    Request body:
        {
            "message": "user message",
            "context": {  // optional
                "location": {"lat": float, "lon": float},
                "time": "timestamp"
            }
        }
    
    Returns:
        {
            "response": "empathy response",
            "scan_result": { ... },
            "alert_created": bool
        }
    """
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({'error': 'message is required'}), 400
    
    message = data['message']
    context = data.get('context', {})
    
    # Scan message for safety concerns
    scan_result = luna_core.scan_message(message, context)
    
    # Generate empathy response
    empathy_response = luna_core.generate_empathy_response(message, scan_result)
    
    # Create alert if needed
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
                'scan_result': scan_result
            }
        )
        alert_created = True
        logger.warning(f"Alert created for user {request.user_id}: {scan_result['severity']}")
    
    return jsonify({
        'response': empathy_response,
        'scan_result': scan_result,
        'alert_created': alert_created,
        'alert': alert,
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/location', methods=['POST'])
@token_required
def check_location():
    """
    Check geofence location
    
    Request body:
        {
            "lat": float,
            "lon": float,
            "safe_zones": [
                {
                    "lat": float,
                    "lon": float,
                    "radius": int (meters),
                    "name": "string"
                }
            ]
        }
    
    Returns:
        {
            "in_safe_zone": bool,
            "alert_created": bool,
            ...
        }
    """
    data = request.get_json()
    
    if not data or 'lat' not in data or 'lon' not in data:
        return jsonify({'error': 'lat and lon are required'}), 400
    
    lat = float(data['lat'])
    lon = float(data['lon'])
    safe_zones = data.get('safe_zones', [])
    
    # Check geofence
    geofence_result = luna_core.check_geofence(lat, lon, safe_zones)
    
    # Create alert if outside safe zone
    alert_created = False
    alert = None
    
    if geofence_result['alert_parent']:
        alert = luna_core.create_alert(
            alert_type='geofence_violation',
            severity='high',
            message=f"Child is outside safe zone",
            metadata={
                'user_id': request.user_id,
                'location': geofence_result['current_location'],
                'distance_to_nearest': geofence_result['distance_to_nearest']
            }
        )
        alert_created = True
        logger.warning(f"Geofence alert for user {request.user_id}")
    
    return jsonify({
        **geofence_result,
        'alert_created': alert_created,
        'alert': alert
    })


@app.route('/night_mode', methods=['POST'])
@token_required
def night_mode():
    """
    Night mode endpoint for bedtime support
    
    Request body:
        {
            "message": "optional user message",
            "action": "check_time" | "get_calming_response" | "bedtime_reminder"
        }
    
    Returns:
        {
            "response": "calming response",
            "night_mode_status": { ... },
            "recommendations": [ ... ]
        }
    """
    data = request.get_json() or {}
    
    action = data.get('action', 'check_time')
    message = data.get('message', '')
    
    # Check if it's night mode time
    night_status = luna_core.validate_night_mode_time()
    
    response_text = ""
    
    if action == 'check_time':
        if night_status['is_bedtime_window']:
            response_text = "It's getting close to bedtime. Let's start winding down for the night. 🌙"
        elif night_status['is_night_mode']:
            response_text = "It's nighttime. I'm here if you need calming support. 💙"
        else:
            response_text = "You're doing great! Remember to take care of yourself throughout the day."
    
    elif action == 'get_calming_response':
        # If user provided a message, scan it
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
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/alerts', methods=['GET'])
@token_required
def get_alerts():
    """
    Get alerts for user (parent view)
    
    In production, this would query a database
    For offline mode, this is a placeholder
    
    Returns:
        {
            "alerts": [ ... ],
            "count": int
        }
    """
    # Placeholder - in production, query database
    return jsonify({
        'alerts': [],
        'count': 0,
        'message': 'Alert storage not yet implemented - alerts are created but not persisted in this demo'
    })


@app.route('/resources', methods=['GET'])
def get_resources():
    """
    Get crisis and support resources
    
    Returns:
        {
            "crisis_resources": { ... },
            "donation_links": { ... }
        }
    """
    return jsonify({
        'crisis_resources': luna_core.CRISIS_RESOURCES,
        'donation_links': {
            'gofundme': 'https://gofund.me/42b8334bd',
            'cashapp': 'https://cash.app/$MichiganMindMendinc'
        },
        'demo': {
            'eve_ai': 'https://kid-helper-ai.replit.app'
        }
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    logger.info(f"Starting MindMend Super AI Backend on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
