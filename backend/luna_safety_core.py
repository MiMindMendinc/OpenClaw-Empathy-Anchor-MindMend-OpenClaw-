"""
Luna Safety Core — deterministic safety-signal scanner for MindMend Empathy Anchor.

This is keyword/pattern matching, not clinical AI, not a trained NLP model, and not
an emergency service. Rules are versioned via SCANNER_VERSION.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
import logging
import re

from version import SCANNER_VERSION

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NEGATION_WINDOW = re.compile(
    r"\b(not|no|never|don't|dont|didn't|didnt|isn't|isnt|wasn't|wasnt|won't|wont|"
    r"without|stop|stopped)\b[\w\s']{0,24}$",
    re.IGNORECASE,
)


class LunaSafetyCore:
    """Deterministic local safety-signal scanner."""

    SCANNER_VERSION = SCANNER_VERSION
    SCANNER_METHOD = 'deterministic_keyword_pattern'
    
    # Crisis keywords for immediate intervention
    CRISIS_KEYWORDS = [
        'suicide', 'kill myself', 'end my life', 'want to die', 'self harm',
        'cut myself', 'hurt myself', 'no reason to live', 'better off dead',
        'overdose', 'jump off', 'hang myself'
    ]
    
    # Distress keywords for mental health support
    DISTRESS_KEYWORDS = [
        'depressed', 'anxious', 'anxiety', 'panic', 'overwhelmed', 'scared',
        'lonely', 'hopeless', 'worthless', 'tired of life', 'can\'t cope',
        'stressed', 'worried', 'afraid', 'terrified', 'desperate'
    ]
    
    # Toxicity/threat keywords for safety monitoring
    TOXICITY_KEYWORDS = [
        'hate you', 'kill you', 'hurt you', 'threatening', 'bully',
        'harass', 'abuse', 'violence', 'weapon', 'fight'
    ]
    
    # Night mode keywords for bedtime monitoring
    NIGHT_MODE_KEYWORDS = [
        'can\'t sleep', 'insomnia', 'nightmare', 'scared of dark',
        'bedtime', 'tired', 'exhausted', 'sleep problems', 'wide awake'
    ]
    
    # Michigan crisis resources
    CRISIS_RESOURCES = {
        '988': 'Suicide & Crisis Lifeline - Call or text 988 (24/7)',
        'nami_michigan': 'NAMI Michigan - 1-800-950-NAMI (6264)',
        'crisis_text': 'Crisis Text Line - Text HELLO to 741741',
        'michigan_crisis': 'Michigan Crisis & Access Line - 1-844-464-3274',
        'emergency': '911 - For immediate life-threatening emergencies'
    }
    
    def __init__(self, offline_mode: bool = True, use_spacy: bool = False):
        """
        Initialize Luna Safety Core
        
        Args:
            offline_mode: Enable offline mode for privacy (default: True)
            use_spacy: Enable spaCy NLP if available (default: False, uses pattern matching)
        """
        self.offline_mode = offline_mode
        self.use_spacy = use_spacy
        self.nlp = None
        
        # Try to load spaCy if requested and available
        if use_spacy:
            try:
                import spacy
                self.nlp = spacy.load('en_core_web_sm')
                logger.info("spaCy NLP loaded successfully")
            except (ImportError, OSError) as e:
                logger.warning(f"spaCy not available, using pattern matching: {e}")
                self.use_spacy = False
        
        logger.info(f"Luna Safety Core initialized - Offline: {offline_mode}, NLP: {self.use_spacy}")
    
    def scan_message(self, message: str, context: Optional[Dict] = None) -> Dict:
        """
        Scan a message for safety concerns, mental health indicators, and sentiment
        
        Args:
            message: User message to scan
            context: Optional context (user_id, timestamp, location, etc.)
        
        Returns:
            Dict with scan results including flags, severity, and recommended actions
        """
        if not message or not message.strip():
            return {
                'error': 'Empty message',
                'safe': True,
                'severity': 'low',
                'flags': {
                    'crisis': False,
                    'distress': False,
                    'toxicity': False,
                    'night_mode': False,
                },
                'matches': {
                    'crisis': [],
                    'distress': [],
                    'toxicity': [],
                    'night_mode': [],
                },
                'recommended_actions': [],
                'scanner_version': self.SCANNER_VERSION,
                'scanner_method': self.SCANNER_METHOD,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'offline_mode': self.offline_mode,
            }

        message_lower = message.lower()
        quoted_context = bool(re.search(r'["“”\'].+["“”\']', message))

        crisis_detected, crisis_matches = self._check_keywords(message_lower, self.CRISIS_KEYWORDS)
        distress_detected, distress_matches = self._check_keywords(message_lower, self.DISTRESS_KEYWORDS)
        toxicity_detected, toxicity_matches = self._check_keywords(message_lower, self.TOXICITY_KEYWORDS)
        night_mode_detected, night_matches = self._check_keywords(message_lower, self.NIGHT_MODE_KEYWORDS)

        severity = self._calculate_severity(
            crisis_detected, distress_detected, toxicity_detected, night_mode_detected
        )
        sentiment = self._analyze_sentiment(message)

        result = {
            'safe': not (crisis_detected or toxicity_detected),
            'severity': severity,
            'flags': {
                'crisis': crisis_detected,
                'distress': distress_detected,
                'toxicity': toxicity_detected,
                'night_mode': night_mode_detected,
            },
            'matches': {
                'crisis': crisis_matches,
                'distress': distress_matches,
                'toxicity': toxicity_matches,
                'night_mode': night_matches,
            },
            'sentiment': sentiment,
            'quoted_context_suspected': quoted_context,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'offline_mode': self.offline_mode,
            'scanner_version': self.SCANNER_VERSION,
            'scanner_method': self.SCANNER_METHOD,
        }

        result['recommended_actions'] = self._get_recommended_actions(result)
        # Compatibility alias for older clients/tests
        result['actions'] = result['recommended_actions']

        if crisis_detected or distress_detected:
            result['resources'] = self.CRISIS_RESOURCES

        return result

    def _check_keywords(self, message: str, keywords: List[str]) -> Tuple[bool, List[str]]:
        """Match keywords unless clearly negated in a short preceding window."""
        matches = []
        for keyword in keywords:
            start = 0
            while True:
                idx = message.find(keyword, start)
                if idx < 0:
                    break
                prefix = message[max(0, idx - 32):idx]
                if NEGATION_WINDOW.search(prefix):
                    start = idx + len(keyword)
                    continue
                matches.append(keyword)
                break
        return len(matches) > 0, matches
    
    def _calculate_severity(self, crisis: bool, distress: bool, 
                           toxicity: bool, night_mode: bool) -> str:
        """Calculate severity level based on detected flags"""
        if crisis or toxicity:
            return 'critical'
        elif distress:
            return 'high'
        elif night_mode:
            return 'moderate'
        else:
            return 'low'
    
    def _analyze_sentiment(self, message: str) -> Dict:
        """
        Lightweight polarity hint using keyword counts.

        This is not a trained NLP model. It exists so demos can show an
        explainable local signal alongside crisis/distress flags.
        """
        positive_words = ('happy', 'good', 'great', 'better', 'love', 'excited', 'joy')
        negative_words = ('bad', 'sad', 'terrible', 'awful', 'hate', 'angry', 'upset')

        message_lower = message.lower()
        pos_count = sum(1 for word in positive_words if word in message_lower)
        neg_count = sum(1 for word in negative_words if word in message_lower)

        if pos_count > neg_count:
            polarity = 0.5
        elif neg_count > pos_count:
            polarity = -0.5
        else:
            polarity = 0.0

        return {
            'polarity': polarity,
            'method': 'keyword_pattern',
            'positive_hits': pos_count,
            'negative_hits': neg_count,
        }
    
    def _get_recommended_actions(self, scan_result: Dict) -> List[str]:
        """Return recommended local actions — not completed automated contacts."""
        actions = []

        if scan_result['flags']['crisis']:
            actions.extend([
                'RECOMMEND_ALERT_TRUSTED_ADULT',
                'SHOW_CRISIS_RESOURCES',
                'SUPPORTIVE_RESPONSE_HIGH',
            ])

        if scan_result['flags']['toxicity']:
            actions.extend([
                'RECOMMEND_REVIEW_BY_CAREGIVER',
                'LOG_LOCAL_INCIDENT',
            ])

        if scan_result['flags']['distress']:
            actions.extend([
                'SUPPORTIVE_RESPONSE_MEDIUM',
                'SUGGEST_SUPPORT_RESOURCES',
            ])

        if scan_result['flags']['night_mode']:
            actions.extend([
                'NIGHT_MODE_SUPPORT',
                'SUGGEST_CALMING_TECHNIQUES',
            ])

        return actions

    def generate_empathy_response(self, message: str, scan_result: Optional[Dict] = None) -> str:
        """Generate supportive response framing from scan results."""
        if scan_result is None:
            scan_result = self.scan_message(message)
        
        # Build empathetic response based on severity
        if scan_result['flags']['crisis']:
            response = self._generate_crisis_response(message, scan_result)
        elif scan_result['flags']['distress']:
            response = self._generate_distress_response(message, scan_result)
        elif scan_result['flags']['night_mode']:
            response = self._generate_night_mode_response(message, scan_result)
        else:
            response = self._generate_neutral_response(message, scan_result)
        
        # Add privacy notice if offline
        if self.offline_mode:
            response += "\n\n🔒 Privacy Mode: Your conversation is staying private on this device."
        
        return response
    
    def _generate_crisis_response(self, message: str, scan_result: Dict) -> str:
        """Generate response for crisis situations"""
        response = "I hear that you're going through something really difficult right now, and I want you to know that your feelings are valid. "
        response += "However, I'm concerned about your safety and wellbeing.\n\n"
        response += "**Please reach out to someone who can help right away:**\n\n"
        
        for key, resource in self.CRISIS_RESOURCES.items():
            response += f"• {resource}\n"
        
        response += "\nYou don't have to face this alone. These resources are available 24/7, and the people there truly care and want to help."
        
        return response
    
    def _generate_distress_response(self, message: str, scan_result: Dict) -> str:
        """Generate response for distress/mental health concerns"""
        response = "Thank you for sharing what you're feeling. It takes courage to talk about difficult emotions, and I want you to know that what you're experiencing is valid.\n\n"
        response += "Many young people go through similar feelings, and there are people who understand and want to support you. "
        
        if 'anxious' in message.lower() or 'anxiety' in message.lower():
            response += "Anxiety can feel overwhelming, but there are ways to work through it.\n\n"
        elif 'sad' in message.lower() or 'depressed' in message.lower():
            response += "These feelings of sadness are real, and you deserve support.\n\n"
        
        response += "**Support resources:**\n"
        response += f"• {self.CRISIS_RESOURCES['nami_michigan']}\n"
        response += f"• {self.CRISIS_RESOURCES['crisis_text']}\n"
        
        return response
    
    def _generate_night_mode_response(self, message: str, scan_result: Dict) -> str:
        """Generate calming response for night mode / bedtime concerns"""
        response = "I understand that nighttime can sometimes feel challenging. Let's work on this together.\n\n"
        
        if 'can\'t sleep' in message.lower() or 'insomnia' in message.lower():
            response += "**Here are some calming techniques that might help:**\n\n"
            response += "• Take slow, deep breaths - breathe in for 4 counts, hold for 4, out for 4\n"
            response += "• Try a simple body scan - relax each part of your body starting from your toes\n"
            response += "• Think of a peaceful place - imagine all the details that make you feel calm\n"
            response += "• Listen to gentle sounds or calming music\n\n"
        
        if 'nightmare' in message.lower() or 'scared' in message.lower():
            response += "Remember that you're safe right now. Dreams can feel scary, but they can't hurt you. "
            response += "If you're feeling afraid, it's okay to turn on a light or talk to a parent or guardian.\n\n"
        
        response += "It's okay to have trouble sleeping sometimes. Be patient with yourself. 💙"
        
        return response
    
    def _generate_neutral_response(self, message: str, scan_result: Dict) -> str:
        """Generate supportive response for neutral messages"""
        response = "Thank you for sharing with me. I'm here to listen and support you. "
        response += "How are you feeling today?"
        
        return response
    
    def check_geofence(self, lat: float, lon: float, safe_zones: List[Dict]) -> Dict:
        """
        Check if location is within safe geofence zones
        
        Args:
            lat: Latitude
            lon: Longitude
            safe_zones: List of safe zone dicts with 'lat', 'lon', 'radius' (in meters)
        
        Returns:
            Dict with geofence status
        """
        from math import radians, cos, sin, asin, sqrt
        
        def haversine(lat1, lon1, lat2, lon2):
            """Calculate distance between two points on Earth in meters"""
            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            r = 6371000  # Radius of Earth in meters
            return c * r
        
        in_safe_zone = False
        nearest_zone = None
        min_distance = float('inf')
        
        for zone in safe_zones:
            distance = haversine(lat, lon, zone['lat'], zone['lon'])
            
            if distance < min_distance:
                min_distance = distance
                nearest_zone = zone
            
            if distance <= zone['radius']:
                in_safe_zone = True
                break
        
        return {
            'in_safe_zone': in_safe_zone,
            'nearest_zone': nearest_zone,
            'distance_to_nearest': min_distance,
            'current_location': {'lat': lat, 'lon': lon},
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'alert_parent': not in_safe_zone
        }
    
    def create_alert(self, alert_type: str, severity: str, 
                    message: str, metadata: Optional[Dict] = None) -> Dict:
        """
        Create parent alert for safety concerns
        
        Args:
            alert_type: Type of alert (crisis, toxicity, geofence, etc.)
            severity: Severity level (critical, high, moderate, low)
            message: Alert message
            metadata: Optional additional context
        
        Returns:
            Alert dict ready to send via Firebase or other notification system
        """
        alert = {
            'id': f"alert_{datetime.now(timezone.utc).timestamp()}",
            'type': alert_type,
            'severity': severity,
            'message': message,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'status': 'pending',
            'metadata': metadata or {}
        }
        
        # In offline mode, queue for later delivery
        if self.offline_mode:
            alert['queued_offline'] = True
        
        return alert
    
    def validate_night_mode_time(self, hour: int = None) -> Dict:
        """
        Check if current time is within night mode hours
        
        Args:
            hour: Optional hour to check (0-23), defaults to current hour
        
        Returns:
            Dict with night mode status and recommendations
        """
        if hour is None:
            hour = datetime.now().hour
        
        # Night mode: 8 PM (20:00) to 7 AM (07:00)
        is_night_mode = hour >= 20 or hour < 7
        
        bedtime_window = 20 <= hour <= 22  # 8-10 PM is bedtime window
        
        response = {
            'is_night_mode': is_night_mode,
            'is_bedtime_window': bedtime_window,
            'current_hour': hour,
            'recommendations': []
        }
        
        if bedtime_window:
            response['recommendations'].extend([
                'Start winding down activities',
                'Reduce screen brightness',
                'Consider calming activities',
                'Prepare for bedtime routine'
            ])
        elif is_night_mode and hour >= 23:
            response['recommendations'].extend([
                'It\'s getting late - consider getting rest',
                'Tomorrow is a new day',
                'Your body needs sleep to stay healthy'
            ])
        
        return response


# Convenience function for quick scanning
def scan_text(text: str, offline: bool = True) -> Dict:
    """Quick scan of text for safety concerns"""
    core = LunaSafetyCore(offline_mode=offline)
    return core.scan_message(text)
