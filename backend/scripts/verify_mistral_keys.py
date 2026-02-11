import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='/home/spas/OPOS_GEMINI_1/backend/.env.backend')

keys = {
    "MISTRAL_OCR_API_KEY": os.getenv("MISTRAL_OCR_API_KEY"),
    "MISTRAL_API_KEY": os.getenv("MISTRAL_API_KEY")
}

print("🔍 Testing Mistral Keys against https://api.mistral.ai/v1/models ...\n")

for name, key in keys.items():
    if not key:
        print(f"❌ {name}: NOT FOUND")
        continue
        
    clean_key = key.strip()
    headers = {"Authorization": f"Bearer {clean_key}"}
    
    try:
        r = requests.get("https://api.mistral.ai/v1/models", headers=headers, timeout=5)
        if r.status_code == 200:
            print(f"✅ {name}: WORKING! ({clean_key[:5]}...)")
        else:
            print(f"❌ {name}: FAILED (Status {r.status_code}) - {r.json().get('message', 'No msg')}")
    except Exception as e:
        print(f"❌ {name}: ERROR ({e})")
