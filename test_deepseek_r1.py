
import os
import requests
import json
from pathlib import Path

# Load env
env_path = Path("backend/.env.backend")
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)

API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/v1/chat/completions"

payload = {
    "model": "deepseek-reasoner",
    "messages": [{"role": "user", "content": "Hola, respondeme con un JSON: {'test': 'ok'}"}],
    "max_tokens": 100
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print(f"Sending request to {URL}...")
try:
    r = requests.post(URL, headers=headers, json=payload, timeout=30)
    print(f"Status: {r.status_code}")
    print("Raw Response Body:")
    print(r.text) # PRINT EVERYTHING
except Exception as e:
    print(f"Error: {e}")
