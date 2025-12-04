#!/usr/bin/env python3
import requests

# Probar diferentes keys
keys = [
    "Dn11EQcZl36z7BghhcM3mfa8mrjI5Ko2",  # Del .env
]

for i, key in enumerate(keys, 1):
    print(f"\n🔑 Probando key {i}: {key[:20]}...")
    
    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistral-medium-latest",
            "messages": [{"role": "user", "content": "Hola"}]
        }
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
