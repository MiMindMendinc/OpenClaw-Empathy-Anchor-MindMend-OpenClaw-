"""
Tests for Flask API endpoints
"""

import json
import os
import subprocess
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')

from alert_store import AlertStore
import app as app_module
from app import app, luna_core


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Create test client with isolated alert database."""
    db_path = str(tmp_path / 'test_alerts.db')
    monkeypatch.setenv('ALERT_DB_PATH', db_path)
    monkeypatch.setattr(app_module, 'DEMO_AUTH', True)
    app.config['DEMO_AUTH'] = True
    app_module.alert_store = AlertStore(db_path)
    app.config['TESTING'] = True

    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def auth_token(client):
    """Get authentication token."""
    response = client.post(
        '/auth/login',
        data=json.dumps({'user_id': 'test_user'}),
        content_type='application/json',
    )
    data = json.loads(response.data)
    return data['token']


class TestAPIEndpoints:
    """Test suite for Flask API endpoints."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data

    def test_login_demo_mode(self, client):
        """Test demo login issues a token with demo notice."""
        response = client.post(
            '/auth/login',
            data=json.dumps({'user_id': 'test_user'}),
            content_type='application/json',
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'token' in data
        assert 'expires_at' in data
        assert data['demo_auth'] is True
        assert 'notice' in data

    def test_login_missing_user_id(self, client):
        """Test login with missing user_id."""
        response = client.post(
            '/auth/login',
            data=json.dumps({}),
            content_type='application/json',
        )

        assert response.status_code == 400

    def test_chat_without_token(self, client):
        """Test chat endpoint without authentication."""
        response = client.post(
            '/chat',
            data=json.dumps({'message': 'Hello'}),
            content_type='application/json',
        )

        assert response.status_code == 401

    def test_chat_with_token(self, client, auth_token):
        """Test chat endpoint with valid token."""
        response = client.post(
            '/chat',
            data=json.dumps({'message': 'I feel anxious'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'},
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'response' in data
        assert 'scan_result' in data
        assert data['scan_result']['flags']['distress'] is True

    def test_chat_crisis_creates_persisted_alert(self, client, auth_token):
        """Test chat with crisis message creates and persists an alert."""
        response = client.post(
            '/chat',
            data=json.dumps({'message': 'I want to kill myself'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'},
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['alert_created'] is True
        assert data['scan_result']['severity'] == 'critical'
        assert '988' in data['response']
        assert data['alert'] is not None
        assert data['alert']['user_id'] == 'test_user'

        alerts_response = client.get(
            '/alerts',
            headers={'Authorization': f'Bearer {auth_token}'},
        )
        alerts_data = json.loads(alerts_response.data)
        assert alerts_data['count'] >= 1
        assert alerts_data['alerts'][0]['alert_type'] == 'safety_concern'

    def test_chat_distress_creates_alert(self, client, auth_token):
        """Test chat with high-severity distress creates an alert."""
        response = client.post(
            '/chat',
            data=json.dumps({'message': 'I feel hopeless and worthless'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'},
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['alert_created'] is True

    def test_chat_missing_message(self, client, auth_token):
        """Test chat with missing message."""
        response = client.post(
            '/chat',
            data=json.dumps({}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'},
        )

        assert response.status_code == 400

    def test_location_geofence_inside(self, client, auth_token):
        """Test location check inside safe zone."""
        payload = {
            'lat': 42.9956,
            'lon': -84.1762,
            'safe_zones': [
                {'lat': 42.9956, 'lon': -84.1762, 'radius': 1000, 'name': 'Home'},
            ],
        }

        response = client.post(
            '/location',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'},
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['in_safe_zone'] is True
        assert data['alert_created'] is False

    def test_location_geofence_outside_persists_alert(self, client, auth_token):
        """Test location outside safe zone creates persisted alert."""
        payload = {
            'lat': 43.0,
            'lon': -84.2,
            'safe_zones': [
                {'lat': 42.9956, 'lon': -84.1762, 'radius': 100, 'name': 'Home'},
            ],
        }

        response = client.post(
            '/location',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'},
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['in_safe_zone'] is False
        assert data['alert_created'] is True

        alerts_response = client.get(
            '/alerts',
            headers={'Authorization': f'Bearer {auth_token}'},
        )
        alerts_data = json.loads(alerts_response.data)
        assert alerts_data['count'] >= 1
        assert alerts_data['alerts'][0]['alert_type'] == 'geofence_violation'

    def test_location_missing_coords(self, client, auth_token):
        """Test location with missing coordinates."""
        response = client.post(
            '/location',
            data=json.dumps({}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'},
        )

        assert response.status_code == 400

    def test_night_mode_check_time(self, client, auth_token):
        """Test night mode time check."""
        response = client.post(
            '/night_mode',
            data=json.dumps({'action': 'check_time'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'},
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'response' in data
        assert 'night_mode_status' in data
        assert 'recommendations' in data

    def test_night_mode_calming_response(self, client, auth_token):
        """Test night mode calming response."""
        response = client.post(
            '/night_mode',
            data=json.dumps({
                'action': 'get_calming_response',
                'message': "I can't sleep",
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'},
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'breathe' in data['response'].lower() or 'calm' in data['response'].lower()

    def test_night_mode_bedtime_reminder(self, client, auth_token):
        """Test night mode bedtime reminder."""
        response = client.post(
            '/night_mode',
            data=json.dumps({'action': 'bedtime_reminder'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'},
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'Bedtime reminder' in data['response']

    def test_get_alerts_empty(self, client, auth_token):
        """Test get alerts endpoint returns empty list initially."""
        response = client.get(
            '/alerts',
            headers={'Authorization': f'Bearer {auth_token}'},
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'alerts' in data
        assert 'count' in data
        assert data['count'] == 0

    def test_demo_endpoint(self, client):
        """Test demo endpoint returns all scenario types."""
        response = client.get('/demo')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'disclaimer' in data
        assert 'chat_scenarios' in data
        assert 'geofence_scenario' in data

        scenario_names = {s['scenario'] for s in data['chat_scenarios']}
        assert scenario_names == {'neutral', 'distress', 'crisis', 'night_mode'}
        assert data['geofence_scenario']['result']['alert_parent'] is True

    def test_get_resources(self, client):
        """Test get resources endpoint (no auth required)."""
        response = client.get('/resources')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'crisis_resources' in data
        assert 'notice' in data
        assert 'donation_links' not in data
        assert '988' in data['crisis_resources']

    def test_night_mode_invalid_action(self, client, auth_token):
        response = client.post(
            '/night_mode',
            data=json.dumps({'action': 'not_a_real_action'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'},
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        allowed = data.get('allowed_actions') or data.get('error', {}).get('allowed_actions')
        assert allowed

    def test_location_invalid_coords(self, client, auth_token):
        response = client.post(
            '/location',
            data=json.dumps({'lat': 'west', 'lon': -84.2}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'},
        )
        assert response.status_code == 400

    def test_status_endpoint(self, client):
        response = client.get('/status')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['scanner']['clinical_validation'] is False
        assert data['alert_store'] == 'sqlite_local'

    def test_showcase_served(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'MindMend Empathy Anchor' in response.data

    def test_ready_endpoint(self, client):
        response = client.get('/ready')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ready'

    def test_chat_does_not_store_raw_by_default(self, client, auth_token):
        response = client.post(
            '/chat',
            data=json.dumps({'message': 'I want to kill myself'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'},
        )
        data = json.loads(response.data)
        assert data['alert_created'] is True
        assert 'original_message' not in (data['alert'].get('metadata') or {})

    def test_oversized_message_rejected(self, client, auth_token):
        response = client.post(
            '/chat',
            data=json.dumps({'message': 'x' * 5000}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'},
        )
        assert response.status_code == 400

    def test_delete_alert(self, client, auth_token):
        create = client.post(
            '/chat',
            data=json.dumps({'message': 'I feel hopeless and worthless'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'},
        )
        alert_id = json.loads(create.data)['alert']['id']
        deleted = client.delete(
            f'/api/v1/alerts/{alert_id}',
            headers={'Authorization': f'Bearer {auth_token}'},
        )
        assert deleted.status_code == 200
        missing = client.get(
            f'/api/v1/alerts/{alert_id}',
            headers={'Authorization': f'Bearer {auth_token}'},
        )
        assert missing.status_code == 404

    def test_404_error(self, client):
        """Test 404 error handling."""
        response = client.get('/nonexistent')
        assert response.status_code == 404

    def test_invalid_token(self, client):
        """Test request with invalid token."""
        response = client.post(
            '/chat',
            data=json.dumps({'message': 'Hello'}),
            content_type='application/json',
            headers={'Authorization': 'Bearer invalid_token'},
        )

        assert response.status_code == 401


class TestProductionConfig:
    """Tests for production configuration requirements."""

    BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def test_production_requires_jwt_secret(self):
        """Production mode must not start without JWT_SECRET_KEY."""
        env = os.environ.copy()
        env['FLASK_ENV'] = 'production'
        env.pop('JWT_SECRET_KEY', None)

        result = subprocess.run(
            [
                sys.executable,
                '-c',
                'import sys; sys.path.insert(0, sys.argv[1]); from app import app',
                self.BACKEND_DIR,
            ],
            capture_output=True,
            text=True,
            env=env,
        )

        assert result.returncode != 0
        assert 'JWT_SECRET_KEY' in result.stderr

    def test_production_rejects_default_secret(self):
        """Production mode must reject documented demo secret keys."""
        env = os.environ.copy()
        env['FLASK_ENV'] = 'production'
        env['JWT_SECRET_KEY'] = 'mindmend-secret-key-change-in-production'

        result = subprocess.run(
            [
                sys.executable,
                '-c',
                'import sys; sys.path.insert(0, sys.argv[1]); from app import app',
                self.BACKEND_DIR,
            ],
            capture_output=True,
            text=True,
            env=env,
        )

        assert result.returncode != 0
        assert 'demo value' in result.stderr.lower() or 'documented demo' in result.stderr

    def test_production_demo_auth_disabled(self):
        """Demo login is blocked in production when DEMO_AUTH is not set."""
        env = os.environ.copy()
        env['FLASK_ENV'] = 'production'
        env['JWT_SECRET_KEY'] = 'secure-test-secret-key-for-ci-only'
        env['DEMO_AUTH'] = 'false'

        result = subprocess.run(
            [
                sys.executable,
                '-c',
                '''
import sys
sys.path.insert(0, sys.argv[1])
from app import app
client = app.test_client()
resp = client.post("/auth/login", json={"user_id": "test"})
print(resp.status_code)
print(resp.get_json())
''',
                self.BACKEND_DIR,
            ],
            capture_output=True,
            text=True,
            env=env,
        )

        assert result.returncode == 0
        assert '403' in result.stdout


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
