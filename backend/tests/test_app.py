"""
Tests for Flask API endpoints
"""

import pytest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')

from app import app, luna_core


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_token(client):
    """Get authentication token"""
    response = client.post('/auth/login',
                          data=json.dumps({'user_id': 'test_user'}),
                          content_type='application/json')
    data = json.loads(response.data)
    return data['token']


class TestAPIEndpoints:
    """Test suite for Flask API endpoints"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
    
    def test_login(self, client):
        """Test login endpoint"""
        response = client.post('/auth/login',
                              data=json.dumps({'user_id': 'test_user'}),
                              content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'token' in data
        assert 'expires_at' in data
    
    def test_login_missing_user_id(self, client):
        """Test login with missing user_id"""
        response = client.post('/auth/login',
                              data=json.dumps({}),
                              content_type='application/json')
        
        assert response.status_code == 400
    
    def test_chat_without_token(self, client):
        """Test chat endpoint without authentication"""
        response = client.post('/chat',
                              data=json.dumps({'message': 'Hello'}),
                              content_type='application/json')
        
        assert response.status_code == 401
    
    def test_chat_with_token(self, client, auth_token):
        """Test chat endpoint with valid token"""
        response = client.post('/chat',
                              data=json.dumps({'message': 'I feel anxious'}),
                              content_type='application/json',
                              headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'response' in data
        assert 'scan_result' in data
        assert data['scan_result']['flags']['distress'] == True
    
    def test_chat_crisis_detection(self, client, auth_token):
        """Test chat with crisis message"""
        response = client.post('/chat',
                              data=json.dumps({'message': 'I want to kill myself'}),
                              content_type='application/json',
                              headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['alert_created'] == True
        assert data['scan_result']['severity'] == 'critical'
        assert '988' in data['response']
    
    def test_chat_missing_message(self, client, auth_token):
        """Test chat with missing message"""
        response = client.post('/chat',
                              data=json.dumps({}),
                              content_type='application/json',
                              headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 400
    
    def test_location_geofence_inside(self, client, auth_token):
        """Test location check inside safe zone"""
        payload = {
            'lat': 42.9956,
            'lon': -84.1762,
            'safe_zones': [
                {'lat': 42.9956, 'lon': -84.1762, 'radius': 1000, 'name': 'Home'}
            ]
        }
        
        response = client.post('/location',
                              data=json.dumps(payload),
                              content_type='application/json',
                              headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['in_safe_zone'] == True
        assert data['alert_created'] == False
    
    def test_location_geofence_outside(self, client, auth_token):
        """Test location check outside safe zone"""
        payload = {
            'lat': 43.0,
            'lon': -84.2,
            'safe_zones': [
                {'lat': 42.9956, 'lon': -84.1762, 'radius': 100, 'name': 'Home'}
            ]
        }
        
        response = client.post('/location',
                              data=json.dumps(payload),
                              content_type='application/json',
                              headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['in_safe_zone'] == False
        assert data['alert_created'] == True
    
    def test_location_missing_coords(self, client, auth_token):
        """Test location with missing coordinates"""
        response = client.post('/location',
                              data=json.dumps({}),
                              content_type='application/json',
                              headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 400
    
    def test_night_mode_check_time(self, client, auth_token):
        """Test night mode time check"""
        response = client.post('/night_mode',
                              data=json.dumps({'action': 'check_time'}),
                              content_type='application/json',
                              headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'response' in data
        assert 'night_mode_status' in data
        assert 'recommendations' in data
    
    def test_night_mode_calming_response(self, client, auth_token):
        """Test night mode calming response"""
        response = client.post('/night_mode',
                              data=json.dumps({
                                  'action': 'get_calming_response',
                                  'message': 'I can\'t sleep'
                              }),
                              content_type='application/json',
                              headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'breathe' in data['response'].lower() or 'calm' in data['response'].lower()
    
    def test_night_mode_bedtime_reminder(self, client, auth_token):
        """Test night mode bedtime reminder"""
        response = client.post('/night_mode',
                              data=json.dumps({'action': 'bedtime_reminder'}),
                              content_type='application/json',
                              headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'Bedtime Reminder' in data['response']
    
    def test_get_alerts(self, client, auth_token):
        """Test get alerts endpoint"""
        response = client.get('/alerts',
                             headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'alerts' in data
        assert 'count' in data
    
    def test_get_resources(self, client):
        """Test get resources endpoint (no auth required)"""
        response = client.get('/resources')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'crisis_resources' in data
        assert 'donation_links' in data
        assert '988' in data['crisis_resources']
    
    def test_404_error(self, client):
        """Test 404 error handling"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
    
    def test_invalid_token(self, client):
        """Test request with invalid token"""
        response = client.post('/chat',
                              data=json.dumps({'message': 'Hello'}),
                              content_type='application/json',
                              headers={'Authorization': 'Bearer invalid_token'})
        
        assert response.status_code == 401


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
