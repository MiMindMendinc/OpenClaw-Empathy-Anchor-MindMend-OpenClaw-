# 🔌 MindMend Super AI - API Reference

Complete API documentation for the MindMend Super AI backend.

## Base URL

```
http://localhost:5000  (Development)
https://your-domain.com  (Production)
```

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

---

## Endpoints

### 1. Health Check

Check if the API is running.

**Endpoint:** `GET /health`

**Authentication:** Not required

**Response:**
```json
{
  "status": "healthy",
  "service": "MindMend Super AI",
  "offline_mode": true,
  "timestamp": "2026-02-01T12:00:00.000Z"
}
```

---

### 2. Login / Authentication

Get a JWT token for authenticated requests.

**Endpoint:** `POST /auth/login`

**Authentication:** Not required

**Request Body:**
```json
{
  "user_id": "string"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2026-02-02T12:00:00.000Z",
  "offline_mode": true
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user"}'
```

---

### 3. Chat (Empathy + Safety Scan)

Send a message for empathetic response with safety scanning.

**Endpoint:** `POST /chat`

**Authentication:** Required

**Request Body:**
```json
{
  "message": "string (required)",
  "context": {
    "location": {"lat": 0.0, "lon": 0.0},
    "time": "timestamp"
  }
}
```

**Response:**
```json
{
  "response": "Empathy response text...",
  "scan_result": {
    "safe": true,
    "severity": "low|moderate|high|critical",
    "flags": {
      "crisis": false,
      "distress": false,
      "toxicity": false,
      "night_mode": false
    },
    "matches": {
      "crisis": [],
      "distress": [],
      "toxicity": [],
      "night_mode": []
    },
    "sentiment": {
      "polarity": 0.0,
      "method": "pattern_matching"
    },
    "actions": ["EMPATHY_RESPONSE_MEDIUM"],
    "resources": { /* Optional, if crisis/distress detected */ },
    "timestamp": "2026-02-01T12:00:00.000Z",
    "offline_mode": true
  },
  "alert_created": false,
  "alert": null,
  "timestamp": "2026-02-01T12:00:00.000Z"
}
```

**Example - Normal Message:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"message": "I feel anxious about tomorrow"}'
```

**Example - Crisis Message:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"message": "I want to hurt myself"}'
```

---

### 4. Location / Geofence Check

Check if a location is within safe geofence zones.

**Endpoint:** `POST /location`

**Authentication:** Required

**Request Body:**
```json
{
  "lat": 42.9956,
  "lon": -84.1762,
  "safe_zones": [
    {
      "lat": 42.9956,
      "lon": -84.1762,
      "radius": 1000,
      "name": "Home"
    }
  ]
}
```

**Response:**
```json
{
  "in_safe_zone": true,
  "nearest_zone": {
    "lat": 42.9956,
    "lon": -84.1762,
    "radius": 1000,
    "name": "Home"
  },
  "distance_to_nearest": 50.5,
  "current_location": {
    "lat": 42.9956,
    "lon": -84.1762
  },
  "timestamp": "2026-02-01T12:00:00.000Z",
  "alert_parent": false,
  "alert_created": false,
  "alert": null
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/location \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "lat": 42.9956,
    "lon": -84.1762,
    "safe_zones": [
      {"lat": 42.9956, "lon": -84.1762, "radius": 1000, "name": "Home"}
    ]
  }'
```

---

### 5. Night Mode

Get bedtime support and calming responses.

**Endpoint:** `POST /night_mode`

**Authentication:** Required

**Request Body:**
```json
{
  "message": "string (optional)",
  "action": "check_time|get_calming_response|bedtime_reminder"
}
```

**Response:**
```json
{
  "response": "Night mode response text...",
  "night_mode_status": {
    "is_night_mode": true,
    "is_bedtime_window": false,
    "current_hour": 21,
    "recommendations": [
      "Start winding down activities",
      "Reduce screen brightness"
    ]
  },
  "recommendations": [],
  "timestamp": "2026-02-01T21:00:00.000Z"
}
```

**Example - Check Time:**
```bash
curl -X POST http://localhost:5000/night_mode \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"action": "check_time"}'
```

**Example - Calming Response:**
```bash
curl -X POST http://localhost:5000/night_mode \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "action": "get_calming_response",
    "message": "I cant sleep"
  }'
```

---

### 6. Get Alerts

Retrieve parent alerts (placeholder - DB not yet implemented).

**Endpoint:** `GET /alerts`

**Authentication:** Required

**Response:**
```json
{
  "alerts": [],
  "count": 0,
  "message": "Alert storage not yet implemented - alerts are created but not persisted in this demo"
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/alerts \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 7. Get Resources

Get crisis resources and donation links.

**Endpoint:** `GET /resources`

**Authentication:** Not required

**Response:**
```json
{
  "crisis_resources": {
    "988": "Suicide & Crisis Lifeline - Call or text 988 (24/7)",
    "nami_michigan": "NAMI Michigan - 1-800-950-NAMI (6264)",
    "crisis_text": "Crisis Text Line - Text HELLO to 741741",
    "michigan_crisis": "Michigan Crisis & Access Line - 1-844-464-3274",
    "emergency": "911 - For immediate life-threatening emergencies"
  },
  "donation_links": {
    "gofundme": "https://gofund.me/42b8334bd",
    "cashapp": "https://cash.app/$MichiganMindMendinc"
  },
  "demo": {
    "eve_ai": "https://kid-helper-ai.replit.app"
  }
}
```

**Example:**
```bash
curl http://localhost:5000/resources
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "message is required"
}
```

### 401 Unauthorized
```json
{
  "error": "Token is missing"
}
```
or
```json
{
  "error": "Invalid token"
}
```

### 404 Not Found
```json
{
  "error": "Endpoint not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Data Models

### Scan Result
```typescript
{
  safe: boolean,
  severity: "low" | "moderate" | "high" | "critical",
  flags: {
    crisis: boolean,
    distress: boolean,
    toxicity: boolean,
    night_mode: boolean
  },
  matches: {
    crisis: string[],
    distress: string[],
    toxicity: string[],
    night_mode: string[]
  },
  sentiment: {
    polarity: number,  // -1 to 1
    method: "pattern_matching" | "spacy"
  },
  actions: string[],
  resources?: object,  // Optional
  timestamp: string,
  offline_mode: boolean
}
```

### Alert
```typescript
{
  id: string,
  type: "crisis" | "toxicity" | "geofence_violation" | "safety_concern",
  severity: "low" | "moderate" | "high" | "critical",
  message: string,
  timestamp: string,
  status: "pending" | "sent" | "acknowledged",
  metadata: object,
  queued_offline?: boolean
}
```

---

## Rate Limiting

Currently not implemented. For production:
- Recommended: 100 requests per minute per user
- Crisis endpoints: No rate limiting

---

## Security Notes

1. **Always use HTTPS in production**
2. **Store JWT_SECRET_KEY securely**
3. **Validate all user inputs**
4. **Enable CORS only for trusted domains**
5. **Monitor for abuse patterns**

---

## Testing the API

### Using Python requests:

```python
import requests

# Login
response = requests.post('http://localhost:5000/auth/login',
                        json={'user_id': 'test_user'})
token = response.json()['token']

# Chat
headers = {'Authorization': f'Bearer {token}'}
response = requests.post('http://localhost:5000/chat',
                        json={'message': 'I feel anxious'},
                        headers=headers)
print(response.json())
```

### Using JavaScript fetch:

```javascript
// Login
const loginRes = await fetch('http://localhost:5000/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({user_id: 'test_user'})
});
const {token} = await loginRes.json();

// Chat
const chatRes = await fetch('http://localhost:5000/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({message: 'I feel anxious'})
});
const data = await chatRes.json();
console.log(data);
```

---

## Changelog

- **v1.0.0** (2026-02-01): Initial release with all core endpoints

---

Built with 💙 by MiMindMendinc
