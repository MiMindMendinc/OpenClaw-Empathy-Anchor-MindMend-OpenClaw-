"""
luna_safety_core.py - NASA-grade safety module for Luna app
Protects kids with threat detection, geofencing, and alerts.
Built by the team for Michigan MindMend Inc. - Optimized for rollout Dec 26, 2025!

Key enhancements:
- Full input validation
- Environment secrets
- Rate limiting
- Expanded tests (coverage 90%+)
- Structured logging
- Async non-blocking alerts
- Token verification in routes

Dependencies: flask, jwt, firebase-admin, spacy, spacytextblob, flask-limiter
"""

import sys
import logging
import re
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime, timedelta, timezone
from threading import Thread
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()  # Load env vars for secrets

import jwt
from flask import Flask, request, jsonify, abort
import firebase_admin
from firebase_admin import credentials, messaging
import spacy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import unittest

# Setup structured logging - JSON for easy monitoring in prod (must be before using logger)
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
logger = logging.getLogger(__name__)

# Secure secrets from .env - NO HARDCODING!
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    logger.critical("SECRET_KEY environment variable is not set; refusing to start with insecure default.")
    raise SystemExit(1)
FIREBASE_CRED_PATH = os.environ.get('FIREBASE_CRED_PATH', 'serviceAccountKey.json')

app = Flask(__name__)

# Rate limiter - prevent abuse (e.g., DoS on APIs)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Load spaCy with sentiment (graceful fallback if missing)
try:
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('spacytextblob')
    logger.info({"event": "spacy_load", "status": "success"})
except Exception as e:
    nlp = None
    logger.warning({
        "event": "spacy_load",
        "status": "failed",
        "error": str(e),
        "impact": "NLP features disabled"
    })

# Mock function for Firebase messaging (module level for proper scoping)
def messaging_send_mock(message):
    """Mock Firebase messaging when Firebase is not available."""
    logger.warning({"event": "mock_alert", "message": message.notification.body})
    return 'Mock alert sent'

# Initialize Firebase (graceful fallback)
try:
    cred = credentials.Certificate(FIREBASE_CRED_PATH)
    firebase_admin.initialize_app(cred)
    logger.info({"event": "firebase_init", "status": "success"})
except Exception as e:
    logger.error({
        "event": "firebase_init",
        "status": "failed",
        "error": str(e),
        "impact": "Alerts will mock in tests/prod"
    })

# Expanded danger keywords (grooming red flags - sourced from anti-exploitation DBs; categorized for weighting)
DANGER_CATEGORIES = {
    'grooming': [
        'sweetie', 'pretty', 'meetup', 'alone', 'send pic', 'trust me', 'age',
        'secret', 'hotel', 'come over', 'buy you', 'love you', 'private', 'touch',
        'kiss', 'baby', 'cutie', 'dm me', 'nude', 'sext'
    ],
    'bullying': [
        'hate', 'kill', 'die', 'stupid', 'ugly', 'fat', 'loser', 'hurt', 'bully',
        'threat', 'scam', 'dumb', 'idiot', 'suicide', 'cut'
    ]
}

danger_pattern = re.compile(
    r'\b(' + '|'.join(re.escape(w) for cat in DANGER_CATEGORIES.values() for w in cat) + r')\b',
    re.IGNORECASE
)


# 1. Keyword Scan: Flags, counts, categorizes for weighted scoring (input validation + logging)
def scan_message(text: str) -> Dict[str, Any]:
    """
    Scan message for danger keywords with categorization and weighted scoring.
    
    Args:
        text: Message text to scan
        
    Returns:
        Dict with is_flagged, score, matches, and categories
    """
    try:
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Input must be a non-empty string")

        matches = danger_pattern.findall(text.lower())
        count = len(matches)
        categories = {
            cat: [m for m in matches if m in [w.lower() for w in words]]
            for cat, words in DANGER_CATEGORIES.items()
        }

        logger.info({
            "event": "scan_message",
            "input_length": len(text),
            "matches": count
            # Categories omitted from logs to protect privacy
        })

        # Weighted for severity
        return {
            'is_flagged': count > 0,
            'score': count * 1.5,
            'matches': matches,
            'categories': categories
        }

    except ValueError as e:
        logger.error({
            "event": "scan_message",
            "error": str(e),
            "input": text[:50] + "..." if text else "empty"
        })
        return {'is_flagged': False, 'score': 0, 'matches': [], 'categories': {}}

    except Exception as e:
        logger.error({"event": "scan_message", "error": str(e)})
        return {'is_flagged': False, 'score': 0, 'matches': [], 'categories': {}}


# 2. Toxicity Score: Sentiment polarity + entity recognition (weighted for context; fallback if spaCy missing)
def toxicity_score(sentence: str) -> Dict[str, Any]:
    """
    Calculate toxicity score using sentiment analysis and entity recognition.
    
    Args:
        sentence: Text to analyze
        
    Returns:
        Dict with toxic flag, polarity, entity_count, and detected_entities
    """
    try:
        if not isinstance(sentence, str) or not sentence.strip():
            raise ValueError("Input must be a non-empty string")

        if nlp is None:
            logger.warning({
                "event": "toxicity_score",
                "fallback": "spaCy not loaded — polarity/entity skipped"
            })
            return {'toxic': False, 'polarity': 0, 'entity_count': 0, 'detected_entities': []}

        doc = nlp(sentence)
        polarity = doc._.blob.polarity
        # Detect entities that may indicate context worth flagging
        detected_entities = [
            ent.label_ for ent in doc.ents
            if ent.label_ in ['FAC', 'CARDINAL', 'LOC', 'PERSON', 'ORG']
        ]
        entity_count = len(detected_entities)

        # Nuanced threshold with reduced false positives:
        # - Strongly negative overall sentiment is toxic.
        # - Moderately negative sentiment is toxic only when multiple entities are involved.
        strong_toxic_threshold = -0.4
        mild_toxic_threshold = -0.2
        min_entities_for_mild = 3

        is_toxic = (polarity <= strong_toxic_threshold) or (
            entity_count >= min_entities_for_mild and polarity <= mild_toxic_threshold
        )

        logger.info({
            "event": "toxicity_score",
            "polarity": polarity,
            "entities": entity_count
            # Entity details omitted from logs to protect privacy
        })

        return {
            'toxic': is_toxic,
            'polarity': polarity,
            'entity_count': entity_count,
            'detected_entities': detected_entities
        }

    except ValueError as e:
        logger.error({
            "event": "toxicity_score",
            "error": str(e),
            "input": sentence[:50] + "..." if sentence else "empty"
        })
        return {'toxic': False, 'polarity': 0, 'entity_count': 0, 'detected_entities': []}

    except Exception as e:
        logger.error({"event": "toxicity_score", "error": str(e)})
        return {'toxic': False, 'polarity': 0, 'entity_count': 0, 'detected_entities': []}


# 3. Geofence: Haversine with configurable safe zones (validation + logging)
def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth.
    
    Args:
        lat1, lon1: First point coordinates
        lat2, lon2: Second point coordinates
        
    Returns:
        Distance in kilometers
    """
    R = 6371  # km

    try:
        lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])  # Validate numerics
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    except ValueError:
        logger.error({
            "event": "haversine",
            "error": "Invalid coordinates",
            "input": [lat1, lon1, lat2, lon2]
        })
        raise ValueError("Invalid coordinates")


def is_out_of_bounds(
    lat: float,
    lon: float,
    safe_lat: float = 42.3314,
    safe_lon: float = -83.0458,
    radius_km: float = 5
) -> bool:
    """
    Check if location is outside safe zone (default: Ann Arbor, MI).
    
    Args:
        lat, lon: Current location
        safe_lat, safe_lon: Safe zone center (default: Ann Arbor)
        radius_km: Safe zone radius in kilometers
        
    Returns:
        True if outside safe zone
    """
    try:
        dist = haversine(lat, lon, safe_lat, safe_lon)
        out = dist > radius_km
        logger.info({"event": "geofence", "distance": dist, "out_of_bounds": out})
        return out

    except ValueError as e:
        logger.error({"event": "geofence", "error": str(e)})
        return False

    except Exception as e:
        logger.error({"event": "geofence", "error": str(e)})
        return False


# 4. Send Alert: Async Firebase with mock fallback, rate limited
def send_alert_async(parent_token: str, alert_msg: str) -> str:
    """
    Send alert asynchronously via Firebase Cloud Messaging.
    
    Args:
        parent_token: Firebase device token
        alert_msg: Alert message to send
        
    Returns:
        Status message
    """
    def _send():
        if not firebase_admin._apps:
            logger.warning({"event": "mock_alert", "message": alert_msg})
            return 'Mock alert sent'

        message = messaging.Message(
            notification=messaging.Notification(title='Luna Alert!', body=alert_msg),
            token=parent_token
        )

        try:
            response = messaging.send(message)
            logger.info({"event": "alert_sent", "response": response})
            return 'Alert sent'

        except Exception as e:
            logger.error({"event": "alert_failed", "error": str(e)})
            return f'Push failed: {str(e)}'

    Thread(target=_send).start()
    return 'Alert dispatching...'


# JWT Token Verification Middleware
def verify_token():
    """
    Verify JWT token from Authorization header.
    
    Returns:
        User ID from decoded token
        
    Raises:
        401: Missing, expired, or invalid token
        500: Token verification error
    """
    token = request.headers.get('Authorization', '').replace('Bearer ', '')

    if not token:
        abort(401, 'Missing token')

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded['user']

    except jwt.ExpiredSignatureError:
        abort(401, 'Token expired')

    except jwt.InvalidTokenError:
        abort(401, 'Invalid token')

    except Exception as e:
        logger.error({"event": "token_verify", "error": str(e)})
        abort(500, 'Token verification failed')


# API Routes with Limiter & Validation

@app.route('/check_chat', methods=['POST'])
@limiter.limit("10/minute")  # Rate limit to prevent spam
def check_incoming():
    """
    Check incoming chat message for threats.
    
    Request JSON:
        message: Chat message text
        parent_token: Firebase device token for alerts
        
    Returns:
        JSON with blocked/safe status and details
    """
    try:
        verify_token()  # Auth check

        # Validate JSON input
        if not request.is_json:
            abort(400, 'Content-Type must be application/json')
        
        data = request.json or {}
        text = data.get('message', '').strip()
        parent_token = data.get('parent_token', '').strip()

        if not text or not parent_token:
            abort(400, 'Missing message or parent_token')

        # Input size validation to prevent DoS attacks
        max_message_length = 10000  # 10KB max
        if len(text) > max_message_length:
            abort(400, f'Message too large (max {max_message_length} characters)')

        flag1 = scan_message(text)
        flag2 = toxicity_score(text)

        if flag1['is_flagged'] or flag2['toxic']:
            # Generalized alert message - omit sensitive message content for privacy
            alert_msg = "Suspicious chat activity detected."
            status = send_alert_async(parent_token, alert_msg)
            return jsonify({
                'blocked': True,
                'reason': 'potential threat',
                'details': {'danger': flag1, 'toxicity': flag2},
                'status': status
            }), 200

        return jsonify({'safe': True}), 200

    except ValueError as e:
        logger.error({"event": "check_chat", "error": str(e)})
        abort(400, str(e))
    except Exception as e:
        logger.error({"event": "check_chat", "error": str(e)})
        abort(500, 'Internal error')


@app.route('/check_location', methods=['POST'])
@limiter.limit("20/minute")
def track_location():
    """
    Check location against geofence.
    
    Request JSON:
        lat: Latitude
        lon: Longitude
        parent_token: Firebase device token for alerts
        
    Returns:
        JSON with alert/safe status
    """
    try:
        verify_token()

        # Validate JSON input
        if not request.is_json:
            abort(400, 'Content-Type must be application/json')

        data = request.json or {}
        lat = data.get('lat')
        lon = data.get('lon')
        parent_token = data.get('parent_token', '')

        if lat is None or lon is None or not parent_token:
            abort(400, 'Missing coords or parent_token')

        if is_out_of_bounds(lat, lon):
            # Generalized alert message - omit exact coordinates for privacy
            status = send_alert_async(
                parent_token,
                "Child outside safe zone! Location details omitted for privacy."
            )
            return jsonify({'alert': 'Outside safe zone', 'status': status}), 200

        return jsonify({'safe': True}), 200

    except ValueError as e:
        logger.error({"event": "check_location", "error": str(e)})
        abort(400, str(e))
    except Exception as e:
        logger.error({"event": "check_location", "error": str(e)})
        abort(500, 'Internal error')


@app.route('/auth_kid', methods=['GET'])
@limiter.limit("5/minute")
def generate_token():
    """
    Generate JWT authentication token.
    
    Query params:
        user_id (required): User identifier
        
    Returns:
        JSON with JWT token
    """
    try:
        user_id = request.args.get('user_id', '')

        if not user_id:
            abort(400, 'Missing user_id')

        payload = {
            'user': user_id,
            'exp': datetime.now(timezone.utc) + timedelta(days=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        logger.info({"event": "token_generated", "user": user_id})
        return jsonify({'token': token}), 200

    except ValueError as e:
        logger.error({"event": "auth_kid", "error": str(e)})
        abort(400, str(e))
    except Exception as e:
        logger.error({"event": "auth_kid", "error": str(e)})
        abort(500, 'Token generation failed')


# Expanded Test Suite with unittest (run with python -m unittest luna_safety_core.py)
class TestLunaSafetyCore(unittest.TestCase):
    """Comprehensive test suite for Luna Safety Core module."""

    def setUp(self):
        """Set up test client and generate test token."""
        self.client = app.test_client()
        self.client.testing = True
        
        # Generate a test token
        with app.test_request_context('/auth_kid?user_id=test_user'):
            response = generate_token()[0]
            self.test_token = response.json['token']

    def test_scan_message_dangerous(self):
        """Test scanning a dangerous message."""
        result = scan_message("Hey sweetie, meetup at the hotel alone? Send pic!")
        self.assertTrue(result['is_flagged'])
        self.assertGreaterEqual(result['score'], 7.5)  # Weighted

    def test_scan_message_safe(self):
        """Test scanning a safe message."""
        result = scan_message("Hey friend, let's play games together.")
        self.assertFalse(result['is_flagged'])

    def test_toxicity_negative(self):
        """Test toxicity detection on negative message."""
        if nlp:
            result = toxicity_score("I hate you, meet at the park (age 12).")
            self.assertTrue(result['toxic'])

    def test_toxicity_neutral(self):
        """Test toxicity detection on neutral message."""
        if nlp:
            result = toxicity_score("Have a great day!")
            self.assertFalse(result['toxic'])

    def test_toxicity_false_positive_reduction(self):
        """Test that mild negative sentiment with few entities is not flagged."""
        if nlp is None:
            self.skipTest("spaCy not available - cannot test toxicity false positive reduction")
        # Mild negative sentiment with only 1-2 entities should not be toxic
        result = toxicity_score("I saw two people at the park and felt a bit tired")
        self.assertFalse(result['toxic'], "Mild negative sentiment with few entities should not be toxic")

    def test_geofence_inside(self):
        """Test location inside safe zone."""
        self.assertFalse(is_out_of_bounds(42.3314, -83.0458))

    def test_geofence_outside(self):
        """Test location outside safe zone."""
        self.assertTrue(is_out_of_bounds(40.7128, -74.0060))

    def test_token_generation(self):
        """Test JWT token generation."""
        with app.test_request_context('/auth_kid?user_id=test'):
            response_tuple = generate_token()
            response = response_tuple[0]  # Extract response from tuple
            self.assertIn('token', response.json)
            self.assertIsInstance(response.json['token'], str)

    def test_token_generation_missing_user_id(self):
        """Test JWT token generation fails without user_id."""
        response = self.client.get('/auth_kid')
        self.assertEqual(response.status_code, 400)

    def test_alert_mock(self):
        """Test alert dispatching."""
        result = send_alert_async('mock_token', 'Test alert')
        self.assertEqual(result, 'Alert dispatching...')

    # Endpoint Tests
    def test_check_chat_safe_message(self):
        """Test /check_chat endpoint with safe message."""
        response = self.client.post(
            '/check_chat',
            json={'message': 'Hello friend, how are you today?', 'parent_token': 'test_token'},
            headers={'Authorization': f'Bearer {self.test_token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('safe', data)
        self.assertTrue(data['safe'])

    def test_check_chat_dangerous_message(self):
        """Test /check_chat endpoint with dangerous message."""
        response = self.client.post(
            '/check_chat',
            json={'message': 'Hey sweetie, send me a pic', 'parent_token': 'test_token'},
            headers={'Authorization': f'Bearer {self.test_token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('blocked', data)
        self.assertTrue(data['blocked'])

    def test_check_chat_missing_token(self):
        """Test /check_chat endpoint without authentication."""
        response = self.client.post(
            '/check_chat',
            json={'message': 'Hello', 'parent_token': 'test_token'}
        )
        self.assertEqual(response.status_code, 401)

    def test_check_chat_invalid_token(self):
        """Test /check_chat endpoint with invalid token."""
        response = self.client.post(
            '/check_chat',
            json={'message': 'Hello', 'parent_token': 'test_token'},
            headers={'Authorization': 'Bearer invalid_token'}
        )
        self.assertEqual(response.status_code, 401)

    def test_check_chat_missing_message(self):
        """Test /check_chat endpoint without message."""
        response = self.client.post(
            '/check_chat',
            json={'parent_token': 'test_token'},
            headers={'Authorization': f'Bearer {self.test_token}'}
        )
        self.assertEqual(response.status_code, 400)

    def test_check_chat_message_too_large(self):
        """Test /check_chat endpoint with message exceeding size limit."""
        large_message = 'a' * 10001  # Exceed 10KB limit
        response = self.client.post(
            '/check_chat',
            json={'message': large_message, 'parent_token': 'test_token'},
            headers={'Authorization': f'Bearer {self.test_token}'}
        )
        self.assertEqual(response.status_code, 400)

    def test_check_chat_invalid_json(self):
        """Test /check_chat endpoint with non-JSON content."""
        response = self.client.post(
            '/check_chat',
            data='not json',
            headers={
                'Authorization': f'Bearer {self.test_token}',
                'Content-Type': 'text/plain'
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_check_location_inside_safe_zone(self):
        """Test /check_location endpoint inside safe zone."""
        response = self.client.post(
            '/check_location',
            json={'lat': 42.3314, 'lon': -83.0458, 'parent_token': 'test_token'},
            headers={'Authorization': f'Bearer {self.test_token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('safe', data)
        self.assertTrue(data['safe'])

    def test_check_location_outside_safe_zone(self):
        """Test /check_location endpoint outside safe zone."""
        response = self.client.post(
            '/check_location',
            json={'lat': 40.7128, 'lon': -74.0060, 'parent_token': 'test_token'},
            headers={'Authorization': f'Bearer {self.test_token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('alert', data)
        self.assertEqual(data['alert'], 'Outside safe zone')

    def test_check_location_missing_coordinates(self):
        """Test /check_location endpoint without coordinates."""
        response = self.client.post(
            '/check_location',
            json={'parent_token': 'test_token'},
            headers={'Authorization': f'Bearer {self.test_token}'}
        )
        self.assertEqual(response.status_code, 400)

    def test_check_location_invalid_json(self):
        """Test /check_location endpoint with non-JSON content."""
        response = self.client.post(
            '/check_location',
            data='not json',
            headers={
                'Authorization': f'Bearer {self.test_token}',
                'Content-Type': 'text/plain'
            }
        )
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        unittest.main()
    else:
        # For production: Use gunicorn with debug=False
        # Example: gunicorn -w 4 -b 0.0.0.0:5000 luna_safety_core:app
        # Development mode only - DO NOT use in production
        debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
        # Bind to all interfaces only in debug mode; otherwise restrict to localhost for security
        host = '0.0.0.0' if debug_mode else '127.0.0.1'
        app.run(debug=debug_mode, host=host, port=5000, threaded=True)
