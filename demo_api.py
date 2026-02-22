#!/usr/bin/env python3
"""
MindMend Super AI - API Demo Script

This script demonstrates how to use the MindMend Super AI API endpoints.
Run the backend server first: python backend/app.py
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
USER_ID = "demo_user"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")

def pretty_print(data):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=2))

def demo_health_check():
    """Demo: Health check endpoint"""
    print_section("1. Health Check")
    
    response = requests.get(f"{BASE_URL}/health")
    data = response.json()
    
    print(f"Status: {response.status_code}")
    pretty_print(data)
    
    return response.status_code == 200

def demo_authentication():
    """Demo: Authentication / Login"""
    print_section("2. Authentication")
    
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"user_id": USER_ID}
    )
    data = response.json()
    
    print(f"Status: {response.status_code}")
    pretty_print(data)
    
    return data.get("token")

def demo_chat(token, message):
    """Demo: Chat with empathy and safety scanning"""
    print_section(f"3. Chat - Message: '{message}'")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": message},
        headers=headers
    )
    data = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"\nEmpathy Response:\n{data['response']}\n")
    print(f"Safety Scan Result:")
    print(f"  - Safe: {data['scan_result']['safe']}")
    print(f"  - Severity: {data['scan_result']['severity']}")
    print(f"  - Flags: {data['scan_result']['flags']}")
    print(f"  - Alert Created: {data['alert_created']}")

def demo_crisis_detection(token):
    """Demo: Crisis detection in chat"""
    print_section("4. Crisis Detection")
    
    crisis_message = "I feel like I want to hurt myself"
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": crisis_message},
        headers=headers
    )
    data = response.json()
    
    print(f"Message: '{crisis_message}'")
    print(f"\nStatus: {response.status_code}")
    print(f"\nCrisis Detected: {data['scan_result']['flags']['crisis']}")
    print(f"Severity: {data['scan_result']['severity']}")
    print(f"Alert Created: {data['alert_created']}")
    print(f"\nEmpathy Response (excerpt):\n{data['response'][:200]}...")

def demo_geofence(token):
    """Demo: Geofence checking"""
    print_section("5. Geofence / Location Check")
    
    # Owosso, Michigan coordinates
    payload = {
        "lat": 42.9956,
        "lon": -84.1762,
        "safe_zones": [
            {
                "lat": 42.9956,
                "lon": -84.1762,
                "radius": 1000,
                "name": "Home (Owosso, MI)"
            }
        ]
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/location",
        json=payload,
        headers=headers
    )
    data = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"\nLocation Check:")
    print(f"  - Current: {data['current_location']}")
    print(f"  - In Safe Zone: {data['in_safe_zone']}")
    print(f"  - Distance to Nearest: {data['distance_to_nearest']:.2f} meters")
    print(f"  - Alert Parent: {data['alert_parent']}")

def demo_night_mode(token):
    """Demo: Night mode / bedtime support"""
    print_section("6. Night Mode")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Check time
    response = requests.post(
        f"{BASE_URL}/night_mode",
        json={"action": "check_time"},
        headers=headers
    )
    data = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"\nNight Mode Status:")
    print(f"  - Is Night Mode: {data['night_mode_status']['is_night_mode']}")
    print(f"  - Is Bedtime Window: {data['night_mode_status']['is_bedtime_window']}")
    print(f"  - Current Hour: {data['night_mode_status']['current_hour']}")
    print(f"\nResponse: {data['response']}")
    
    if data['recommendations']:
        print(f"\nRecommendations:")
        for rec in data['recommendations']:
            print(f"  - {rec}")

def demo_resources():
    """Demo: Get crisis resources"""
    print_section("7. Crisis Resources & Donation Links")
    
    response = requests.get(f"{BASE_URL}/resources")
    data = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"\nCrisis Resources:")
    for key, value in data['crisis_resources'].items():
        print(f"  - {value}")
    
    print(f"\nSupport MindMend:")
    for key, value in data['donation_links'].items():
        print(f"  - {key}: {value}")

def main():
    """Run all demos"""
    print("\n" + "█" * 60)
    print("  MindMend Super AI - API Demo")
    print("  Privacy-First Youth Mental Health & Safety")
    print("█" * 60)
    
    try:
        # 1. Health check
        if not demo_health_check():
            print("\n❌ Backend not available. Start it with: python backend/app.py")
            return
        
        # 2. Authentication
        token = demo_authentication()
        if not token:
            print("\n❌ Authentication failed")
            return
        
        # 3. Normal chat
        demo_chat(token, "I feel anxious about school tomorrow")
        
        # 4. Crisis detection
        demo_crisis_detection(token)
        
        # 5. Geofence
        demo_geofence(token)
        
        # 6. Night mode
        demo_night_mode(token)
        
        # 7. Resources
        demo_resources()
        
        print_section("✅ Demo Complete!")
        print("All API endpoints are working correctly.")
        print("\nNext Steps:")
        print("  1. Review API_REFERENCE.md for detailed docs")
        print("  2. Check INSTALL.md for deployment guide")
        print("  3. Read README_SUPER_AI.md for full features")
        print("\n💙 Remember: You are not alone. Help is available.\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to backend server")
        print("Please start the backend first:")
        print("  cd backend && python app.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
