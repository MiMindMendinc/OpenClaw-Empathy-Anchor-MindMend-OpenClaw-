# Luna Safety Core Module

**NASA-grade safety module for the Luna app** - Protects children with threat detection, geofencing, and real-time alerts.

Built by Michigan MindMend Inc. for deployment Dec 26, 2025.

## 🆕 Recent Improvements (Feb 2026)

**Enhanced Production Readiness**:
- ✨ **Multi-Zone Geofencing**: Support for multiple safe zones (home, school, etc.)
- 🔍 **Enhanced Logging**: Request IDs, response times, and error types for better monitoring
- 🛡️ **Circuit Breaker**: Prevents cascading failures in alert system
- 🧪 **Comprehensive Testing**: 36 tests covering edge cases and multi-zone scenarios
- 🔒 **Improved Validation**: Coordinate range checking and zone structure validation
- 📊 **Better Observability**: Structured logs with anonymized user context

## Overview

The Luna Safety Core module provides enterprise-grade safety features for youth protection:

- 🚨 **Threat Detection**: Real-time scanning for grooming and bullying keywords
- 🧠 **Toxicity Analysis**: AI-powered sentiment analysis using spaCy NLP
- 📍 **Geofencing**: Location tracking with multi-zone support and configurable safe zones
- 🔔 **Async Alerts**: Non-blocking Firebase Cloud Messaging to parents
- 🔐 **Secure Auth**: JWT token verification for all API endpoints
- 🛡️ **Rate Limiting**: DDoS protection and abuse prevention
- 📊 **Structured Logging**: JSON logs for production monitoring

## Installation

### Prerequisites

- Python 3.8+
- pip package manager

### Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Download spaCy language model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your SECRET_KEY and FIREBASE_CRED_PATH
   ```

4. **Generate a secure secret key** (REQUIRED):
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Add the output to your `.env` file as `SECRET_KEY`.
   
   **⚠️ CRITICAL**: The application will refuse to start without a valid SECRET_KEY. Never use the default placeholder value in production.

5. **Set up Firebase** (optional for testing):
   - Download your Firebase service account key JSON file
   - Save it as `serviceAccountKey.json` or update `FIREBASE_CRED_PATH` in `.env`
   - If not configured, the module will use mock alerts for testing

## Running the Module

### Development Mode

**Start the server** (binds to all interfaces - use only for development):
```bash
export FLASK_DEBUG=true
python luna_safety_core.py
```

The API server will start on `http://0.0.0.0:5000`

### Production Mode

**⚠️ WARNING**: Do NOT use Flask's built-in development server for production. Use gunicorn instead:

```bash
export FLASK_DEBUG=false
# Production deployment with gunicorn:
gunicorn -w 4 -b 0.0.0.0:5000 luna_safety_core:app
```

When run directly with `python luna_safety_core.py` and `FLASK_DEBUG=false`, the server binds only to `127.0.0.1` for security.

### Run Tests

```bash
python luna_safety_core.py --test
```

Or use unittest directly:

```bash
python -m unittest luna_safety_core.py
```

## API Endpoints

### 1. Generate Auth Token

**GET** `/auth_kid?user_id=<user_id>`

Generates a JWT token for authentication (valid for 24 hours).

**⚠️ SECURITY WARNING**: This endpoint is currently unauthenticated and allows anyone to generate tokens for any user_id. This is a **critical security vulnerability** for production use. Before deploying to production:
1. Implement proper authentication (API keys, parent credentials, or OAuth)
2. Validate that the requesting party is authorized to generate tokens for the specified user_id
3. Consider implementing additional token claims (audience, issuer) for enhanced security

**Rate limit**: 5 requests/minute

**Query Parameters**:
- `user_id` (required): User identifier

**Response**:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 2. Check Chat Message

**POST** `/check_chat`

Scans incoming chat messages for threats and sends alerts if dangerous content is detected.

**Rate limit**: 10 requests/minute

**Headers**:
```
Authorization: Bearer <token>
```

**Request Body**:
```json
{
  "message": "Chat message text to scan",
  "parent_token": "firebase_device_token"
}
```

**Response (Safe)**:
```json
{
  "safe": true
}
```

**Response (Threat Detected)**:
```json
{
  "blocked": true,
  "reason": "potential threat",
  "details": {
    "danger": {
      "is_flagged": true,
      "score": 7.5,
      "matches": ["sweetie", "meetup", "alone"],
      "categories": {
        "grooming": ["sweetie", "meetup", "alone"],
        "bullying": []
      }
    },
    "toxicity": {
      "toxic": true,
      "polarity": -0.4,
      "entity_count": 2,
      "detected_entities": ["PERSON", "LOC"]
    }
  },
  "status": "Alert dispatching..."
}
```

**Note on Privacy**: Alert messages sent to parents are generalized and do not include the actual message content or specific details to protect the child's privacy. Logs also redact sensitive information.

### 3. Check Location

**POST** `/check_location`

Checks if a location is outside the safe geofence zone(s) and sends alerts if needed. **Now supports multi-zone geofencing!**

**Rate limit**: 20 requests/minute

**Headers**:
```
Authorization: Bearer <token>
```

**Request Body (Single Zone - Legacy)**:
```json
{
  "lat": 42.3314,
  "lon": -83.0458,
  "parent_token": "firebase_device_token"
}
```

**Request Body (Multi-Zone - New)**:
```json
{
  "lat": 42.3314,
  "lon": -83.0458,
  "parent_token": "firebase_device_token",
  "safe_zones": [
    {
      "lat": 42.3314,
      "lon": -83.0458,
      "radius_km": 5,
      "name": "School"
    },
    {
      "lat": 42.2808,
      "lon": -83.7430,
      "radius_km": 2,
      "name": "Home"
    }
  ]
}
```

**Response (Inside Safe Zone)**:
```json
{
  "safe": true
}
```

**Response (Outside Safe Zone)**:
```json
{
  "alert": "Outside safe zone",
  "status": "Alert dispatching..."
}
```

**Multi-Zone Behavior**:
- If `safe_zones` parameter is provided, checks against all defined zones
- Returns `safe: true` if location is inside ANY of the defined zones
- Returns `alert` if location is outside ALL defined zones
- Each zone requires: `lat`, `lon`, `radius_km`, and optionally `name`
- Falls back to default single zone (Ann Arbor, MI) if no zones provided
- Validates zone structure and skips malformed zones with warnings

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | JWT secret key (required for production) | `generate_secure_hex_32_with_secrets_token_hex` |
| `FIREBASE_CRED_PATH` | Path to Firebase credentials JSON | `serviceAccountKey.json` |

### Safe Zone Configuration

**Multi-Zone Support (NEW)**: The module now supports multiple safe zones. You can define different zones for home, school, and other locations.

**Default Single Zone**: If no zones are provided, the default safe zone is centered at Ann Arbor, Michigan (42.3314, -83.0458) with a 5km radius.

**Multi-Zone Example**:
```python
safe_zones = [
    {'lat': 42.3314, 'lon': -83.0458, 'radius_km': 5, 'name': 'School'},
    {'lat': 42.2808, 'lon': -83.7430, 'radius_km': 2, 'name': 'Home'},
    {'lat': 42.9956, 'lon': -84.1762, 'radius_km': 3, 'name': 'Grandparents'}
]
```

**Configuration Options**:
- `lat`: Safe zone center latitude (required)
- `lon`: Safe zone center longitude (required)
- `radius_km`: Safe zone radius in kilometers (required)
- `name`: Human-readable zone name for logging (optional)

**Validation**: The module validates all zone configurations and skips malformed zones with warnings in logs. Invalid coordinates are rejected with safe defaults.

## Danger Keyword Categories

The module scans for two categories of dangerous keywords:

### Grooming Keywords
- sweetie, pretty, meetup, alone, send pic, trust me, age, secret
- hotel, come over, buy you, love you, private, touch, kiss
- baby, cutie, dm me, nude, sext

### Bullying Keywords
- hate, kill, die, stupid, ugly, fat, loser, hurt, bully
- threat, scam, dumb, idiot, suicide, cut

Keyword detection uses weighted scoring (1.5x per match) for severity assessment.

## Security Features

1. **JWT Authentication**: All protected endpoints require valid JWT tokens
2. **SECRET_KEY Validation**: Application refuses to start without a secure SECRET_KEY
3. **Rate Limiting**: 
   - `/auth_kid`: 5/minute
   - `/check_chat`: 10/minute
   - `/check_location`: 20/minute
   - Global: 200/day, 50/hour
4. **Input Validation**: 
   - All inputs validated and sanitized
   - Maximum message size: 10KB (prevents DoS attacks)
   - JSON Content-Type validation
   - Coordinate range validation (-90 to 90 for lat, -180 to 180 for lon)
   - Multi-zone configuration validation
5. **Privacy Protection**:
   - Sensitive data redacted from logs (categories, entities)
   - Alert messages generalized (no personal data exposed)
   - Location coordinates omitted from alerts
6. **Structured Logging**: 
   - JSON logs with event tracking (without sensitive data)
   - Request IDs for traceability (8-character UUIDs)
   - Response time monitoring (milliseconds)
   - Error type tracking for debugging
   - User context (anonymized) in logs
7. **Circuit Breaker Pattern**: 
   - Prevents cascading failures in alert system
   - Opens after 5 consecutive failures
   - 60-second timeout before retry
   - Graceful degradation when circuit is open
8. **Environment Secrets**: No hardcoded credentials
9. **Graceful Degradation**: Continues operation if spaCy or Firebase unavailable
10. **Secure Host Binding**: Binds to localhost when debug mode is disabled
11. **Improved Toxicity Detection**: Nuanced thresholds reduce false positives
12. **Enhanced Error Handling**: Safe defaults on invalid inputs, comprehensive error logging

## Testing

The module includes comprehensive unit tests covering all functionality:

### Core Functionality Tests
- ✅ Dangerous message detection
- ✅ Safe message handling
- ✅ Toxicity scoring (positive and negative)
- ✅ Geofence validation (inside and outside safe zones)
- ✅ JWT token generation and validation
- ✅ Alert dispatching

### Multi-Zone Geofencing Tests (NEW)
- ✅ Inside first zone detection
- ✅ Inside second zone detection
- ✅ Outside all zones detection
- ✅ Multi-zone endpoint integration
- ✅ Malformed zone handling

### Edge Case Tests (NEW)
- ✅ Empty and whitespace-only messages
- ✅ Invalid coordinate types and ranges
- ✅ Empty zones list handling
- ✅ Special characters in user_id
- ✅ Excessively long user_id
- ✅ Invalid JSON content
- ✅ Message size limit enforcement
- ✅ Multi-category keyword detection

**Test Coverage**: 90%+ (36 tests total, all passing)

**Run Tests**:
```bash
python -m unittest luna_safety_core
```

## Production Deployment

### Recommendations

1. **Use a production WSGI server** (not Flask's built-in server):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 luna_safety_core:app
   ```

2. **Disable debug mode**: Set `debug=False` in production

3. **Configure HTTPS**: Use nginx or similar reverse proxy

4. **Set strong SECRET_KEY**: Generate with `secrets.token_hex(32)`

5. **Monitor logs**: Parse JSON logs for alerts and errors

6. **Scale with load balancer**: Use multiple instances for high traffic

7. **Database integration**: Consider logging threats to persistent storage

## Architecture

```
┌─────────────────┐
│  Client App     │
│  (Luna App)     │
└────────┬────────┘
         │ HTTPS/JWT
         ▼
┌─────────────────┐
│  Luna Safety    │
│  Core (Flask)   │
│  - Rate Limiter │
│  - Auth Guard   │
└────┬──────┬─────┘
     │      │
     ▼      ▼
┌─────────┐ ┌──────────┐
│ spaCy   │ │ Firebase │
│ NLP     │ │ Alerts   │
└─────────┘ └──────────┘
```

## License

MIT License - See LICENSE file

## Support

For questions or issues:
- Email: support@mimindmendinc.com
- GitHub: https://github.com/MiMindMendinc/OpenClaw-Empathy-Anchor-MindMend-OpenClaw-

---

**Built with ❤️ by Michigan MindMend Inc. for youth safety in Owosso and beyond.**
