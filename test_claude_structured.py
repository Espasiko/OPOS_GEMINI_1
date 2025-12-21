
import os
import requests
import json

def load_env_vars():
    env_path = "backend/.env.backend"
    if os.path.exists(env_path):
        from dotenv import load_dotenv
        load_dotenv(env_path)

load_env_vars()
API_KEY = os.getenv("CLAUDE_API_KEY")

url = "https://api.anthropic.com/v1/messages"
headers = {
    "x-api-key": API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json",
    "anthropic-beta": "structured-outputs-2025-11-13"
}

schema = {
    "type": "object",
    "properties": {
        "topic": {"type": "string"},
        "scenario": {"type": "string"},
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "question": {"type": "string"},
                    "options": {
                        "type": "array", 
                        "items": {
                            "type": "object", 
                            "properties": {
                                "id": {"type": "string"}, 
                                "text": {"type": "string"}
                            }, 
                            "required": ["id", "text"],
                            "additionalProperties": False
                        }
                    },
                    "correct_option_id": {"type": "string"},
                    "explanation": {"type": "string"}
                },
                "required": ["id", "question", "options", "correct_option_id", "explanation"],
                "additionalProperties": False
            }
        }
    },
    "required": ["topic", "scenario", "questions"],
    "additionalProperties": False
}

payload = {
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 1000,
    "tools": [
        {
            "name": "generate_case",
            "description": "Generates a legal case study.",
            "input_schema": schema,
             # Note: 'strict': True might be required inside input_schema OR at tool level depending on API.
             # Based on search, strict tool use typically involves passed 'strict': True at tool definition level? No, usually distinct. 
             # OpenAI uses strict: true. Anthropic's new beta might use strict: true inside JSON schema or separate.
             # Search result said: "Strict Tool Use Mode: This adds strict: true to tool definitions"
        }
    ],
    "tool_choice": {"type": "tool", "name": "generate_case"},
    "messages": [{"role": "user", "content": "Genera un caso de prueba muy breve sobre Jubilación."}]
}

# Adjusting 'strict' location based on latest common patterns (OpenAI style adopted by many)
# But Anthropic docs said "adds strict: true to tool definitions".
payload["tools"][0]["strict"] = True

print("🔍 Testing Structured Outputs Beta...")
try:
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print("Response keys:", data.keys())
        if "content" in data:
            for block in data["content"]:
                if block["type"] == "tool_use":
                    print("✅ Tool Use received!")
                    print(json.dumps(block["input"], indent=2, ensure_ascii=False))
                    break
    else:
        print("❌ Error:", r.text)
except Exception as e:
    print(f"❌ Exception: {e}")
