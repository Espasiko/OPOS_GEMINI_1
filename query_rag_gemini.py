import requests
import json

url = "http://127.0.0.1:8000/api/rag/search"
payload = {
    "query": "compatibilidad pension incapacidad permanente total con trabajo y jubilacion requisitos cuantia",
    "top_k": 5
}

try:
    response = requests.post(url, json=payload, timeout=30)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
