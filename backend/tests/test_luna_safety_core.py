"""
Tests for Luna Safety Core
"""

import pytest
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')

from luna_safety_core import LunaSafetyCore, scan_text


class TestLunaSafetyCore:
    """Test suite for Luna Safety Core"""
    
    def setup_method(self):
        """Setup test instance"""
        self.core = LunaSafetyCore(offline_mode=True, use_spacy=False)
    
    def test_initialization(self):
        """Test core initialization"""
        assert self.core.offline_mode == True
        assert self.core.use_spacy == False
        assert self.core.nlp is None
    
    def test_crisis_detection(self):
        """Test crisis keyword detection"""
        crisis_message = "I want to kill myself"
        result = self.core.scan_message(crisis_message)
        
        assert result['safe'] == False
        assert result['flags']['crisis'] == True
        assert result['severity'] == 'critical'
        assert 'IMMEDIATE_ALERT_PARENT' in result['actions']
        assert 'resources' in result
    
    def test_distress_detection(self):
        """Test distress keyword detection"""
        distress_message = "I feel so anxious and overwhelmed"
        result = self.core.scan_message(distress_message)
        
        assert result['flags']['distress'] == True
        assert result['severity'] == 'high'
        assert 'EMPATHY_RESPONSE_MEDIUM' in result['actions']
    
    def test_night_mode_detection(self):
        """Test night mode keyword detection"""
        night_message = "I can't sleep and having nightmares"
        result = self.core.scan_message(night_message)
        
        assert result['flags']['night_mode'] == True
        assert result['severity'] == 'moderate'
        assert 'NIGHT_MODE_RESPONSE' in result['actions']
    
    def test_toxicity_detection(self):
        """Test toxicity keyword detection"""
        toxic_message = "I hate you and want to hurt you"
        result = self.core.scan_message(toxic_message)
        
        assert result['safe'] == False
        assert result['flags']['toxicity'] == True
        assert result['severity'] == 'critical'
    
    def test_neutral_message(self):
        """Test neutral message processing"""
        neutral_message = "How are you today?"
        result = self.core.scan_message(neutral_message)
        
        assert result['safe'] == True
        assert result['severity'] == 'low'
        assert result['flags']['crisis'] == False
    
    def test_empathy_response_crisis(self):
        """Test empathy response for crisis"""
        message = "I want to die"
        response = self.core.generate_empathy_response(message)
        
        assert "difficult" in response.lower()
        assert "988" in response or "crisis" in response.lower()
        assert "Privacy Mode" in response  # Offline mode notice
    
    def test_empathy_response_distress(self):
        """Test empathy response for distress"""
        message = "I feel so anxious"
        response = self.core.generate_empathy_response(message)
        
        assert "valid" in response.lower() or "courage" in response.lower()
        assert "NAMI" in response or "support" in response.lower()
    
    def test_empathy_response_night_mode(self):
        """Test empathy response for night mode"""
        message = "I can't sleep"
        response = self.core.generate_empathy_response(message)
        
        assert "calming" in response.lower() or "breathe" in response.lower()
        assert "💙" in response  # Empathy emoji
    
    def test_geofence_inside_safe_zone(self):
        """Test geofence when inside safe zone"""
        safe_zones = [
            {'lat': 42.9956, 'lon': -84.1762, 'radius': 1000, 'name': 'Home'}  # Owosso, MI
        ]
        
        result = self.core.check_geofence(42.9956, -84.1762, safe_zones)
        
        assert result['in_safe_zone'] == True
        assert result['alert_parent'] == False
    
    def test_geofence_outside_safe_zone(self):
        """Test geofence when outside safe zone"""
        safe_zones = [
            {'lat': 42.9956, 'lon': -84.1762, 'radius': 100, 'name': 'Home'}
        ]
        
        # Different location
        result = self.core.check_geofence(43.0, -84.2, safe_zones)
        
        assert result['in_safe_zone'] == False
        assert result['alert_parent'] == True
        assert result['distance_to_nearest'] > 100
    
    def test_create_alert(self):
        """Test alert creation"""
        alert = self.core.create_alert(
            alert_type='crisis',
            severity='critical',
            message='Test alert',
            metadata={'user_id': 'test123'}
        )
        
        assert alert['type'] == 'crisis'
        assert alert['severity'] == 'critical'
        assert alert['status'] == 'pending'
        assert 'id' in alert
        assert 'timestamp' in alert
        assert alert['queued_offline'] == True  # Offline mode
    
    def test_night_mode_time_validation_bedtime(self):
        """Test night mode time validation for bedtime window"""
        result = self.core.validate_night_mode_time(hour=21)  # 9 PM
        
        assert result['is_night_mode'] == True
        assert result['is_bedtime_window'] == True
        assert len(result['recommendations']) > 0
    
    def test_night_mode_time_validation_late_night(self):
        """Test night mode time validation for late night"""
        result = self.core.validate_night_mode_time(hour=23)  # 11 PM
        
        assert result['is_night_mode'] == True
        assert result['is_bedtime_window'] == False
        assert 'getting late' in ' '.join(result['recommendations']).lower()
    
    def test_night_mode_time_validation_daytime(self):
        """Test night mode time validation for daytime"""
        result = self.core.validate_night_mode_time(hour=14)  # 2 PM
        
        assert result['is_night_mode'] == False
        assert result['is_bedtime_window'] == False
        assert len(result['recommendations']) == 0
    
    def test_empty_message(self):
        """Test handling of empty messages"""
        result = self.core.scan_message("")
        
        assert 'error' in result
        assert result['safe'] == True
    
    def test_sentiment_analysis_positive(self):
        """Test sentiment analysis for positive message"""
        result = self.core.scan_message("I'm feeling happy and great today!")
        
        assert result['sentiment']['polarity'] > 0
    
    def test_sentiment_analysis_negative(self):
        """Test sentiment analysis for negative message"""
        result = self.core.scan_message("I feel terrible and sad")
        
        assert result['sentiment']['polarity'] < 0
    
    def test_scan_text_convenience_function(self):
        """Test convenience scan_text function"""
        result = scan_text("Test message")
        
        assert 'safe' in result
        assert 'severity' in result
        assert result['offline_mode'] == True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
