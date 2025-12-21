
import os
import requests

def load_env_vars():
    env_path = "backend/.env.backend"
    if os.path.exists(env_path):
        from dotenv import load_dotenv
        load_dotenv(env_path)

load_env_vars()
API_KEY = os.getenv("CLAUDE_API_KEY")

models_to_test = [
    "claude-sonnet-4-5-20250929",
    "claude-sonnet-4-5",
    "claude-4-5-sonnet-20250929",
    "claude-4-5-sonnet",
    "claude-3-7-sonnet-20250219",
    "claude-3-7-sonnet-latest"
]

url = "https://api.anthropic.com/v1/messages"
headers = {
    "x-api-key": API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}

for model in models_to_test:
    print(f"🔍 Testing model: {model}")
    payload = {
        "model": model,
        "max_tokens": 10,
        "messages": [{"role": "user", "content": "Hi"}]
    }
    r = requests.post(url, headers=headers, json=payload)
    if r.status_code == 200:
        print(f"✅ SUCCESS: {model}")
        break
    else:
        print(f"❌ FAILED: {model} - {r.status_code} - {r.text}")
