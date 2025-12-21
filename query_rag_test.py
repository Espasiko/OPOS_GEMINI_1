import requests
import json

url = "http://127.0.0.1:8000/api/rag/search"
payload = {
    "query": "bases convocatoria gestion seguridad social 2024 examen practico distribucion preguntas tiempo",
    "top_k": 5
}

try:
    response = requests.post(url, json=payload, timeout=30)
    print("Status:", response.status_code)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
except Exception as e:
    print("Error:", e)
