#!/usr/bin/env python3
"""
Test AI Functions Endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🏥 Testing AI Functions Health...")
    response = requests.get(f"{BASE_URL}/ai/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_practical_case():
    """Test practical case generation"""
    print("📝 Testing Practical Case Generation...")
    response = requests.post(
        f"{BASE_URL}/ai/practical-case",
        json={
            "topic": "Incapacidad temporal",
            "difficulty": "medium",
            "provider": "groq-70b"
        },
        timeout=60
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Scenario length: {len(data.get('scenario', ''))} chars")
        print(f"✅ Questions: {len(data.get('questions', []))}")
    else:
        print(f"❌ Error: {response.text}")
    print()

def test_mind_map():
    """Test mind map generation"""
    print("🗺️  Testing Mind Map Generation...")
    response = requests.post(
        f"{BASE_URL}/ai/mind-map",
        json={
            "topic": "Jubilación",
            "provider": "groq-70b"
        },
        timeout=60
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Root label: {data.get('label', 'N/A')}")
        print(f"✅ Children: {len(data.get('children', []))}")
    else:
        print(f"❌ Error: {response.text}")
    print()

def test_flashcards():
    """Test flashcards generation"""
    print("🎴 Testing Flashcards Generation...")
    response = requests.post(
        f"{BASE_URL}/ai/flashcards",
        json={
            "topic": "Cotización",
            "num_cards": 5,
            "provider": "groq-8b"
        },
        timeout=60
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Cards generated: {len(data.get('cards', []))}")
    else:
        print(f"❌ Error: {response.text}")
    print()

if __name__ == "__main__":
    print("🚀 Testing AI Functions Endpoints\n")
    
    test_health()
    test_practical_case()
    test_mind_map()
    test_flashcards()
    
    print("✅ Tests completed!")
