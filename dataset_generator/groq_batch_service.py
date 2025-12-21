
import os
import json
import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_env_vars():
    env_path = "backend/.env.backend"
    if os.path.exists(env_path):
        from dotenv import load_dotenv
        load_dotenv(env_path)

load_env_vars()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class GroqBatchService:
    def __init__(self, api_key=GROQ_API_KEY):
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def prepare_batch_file(self, requests_list: list, output_filename: str):
        """
        Guarda una lista de peticiones en formato JSONL para el Batch API.
        """
        with open(output_filename, "w", encoding="utf-8") as f:
            for i, req in enumerate(requests_list):
                batch_item = {
                    "custom_id": f"req_{i}",
                    "method": "POST",
                    "url": "/v1/chat/completions",
                    "body": req
                }
                f.write(json.dumps(batch_item, ensure_ascii=False) + "\n")
        logger.info(f"✅ Archivo batch preparado: {output_filename}")
        return output_filename

    def upload_file(self, file_path: str):
        """Sube el archivo al almacenamiento de Groq"""
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f, "application/jsonl")}
            data = {"purpose": "batch"}
            r = requests.post(f"{self.base_url}/files", headers=self.headers, files=files, data=data)
            r.raise_for_status()
            file_id = r.json()["id"]
            logger.info(f"✅ Archivo subido. File ID: {file_id}")
            return file_id

    def create_batch_job(self, file_id: str):
        """Inicia el trabajo de batch"""
        payload = {
            "input_file_id": file_id,
            "endpoint": "/v1/chat/completions",
            "completion_window": "24h"
        }
        r = requests.post(f"{self.base_url}/batches", headers=self.headers, json=payload)
        r.raise_for_status()
        batch_id = r.json()["id"]
        logger.info(f"🚀 Job de Batch iniciado. Batch ID: {batch_id}")
        return batch_id

    def get_batch_status(self, batch_id: str):
        """Consulta el estado del job"""
        r = requests.get(f"{self.base_url}/batches/{batch_id}", headers=self.headers)
        r.raise_for_status()
        return r.json()

    def download_file(self, file_id: str, output_path: str):
        """Descarga el contenido de un archivo"""
        r = requests.get(f"{self.base_url}/files/{file_id}/content", headers=self.headers)
        r.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(r.content)
        logger.info(f"✅ Archivo descargado en: {output_path}")
        return output_path

if __name__ == "__main__":
    # Test rápido de preparación
    service = GroqBatchService()
    test_reqs = [
        {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": "Hola"}]},
        {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": "Test 2"}]}
    ]
    service.prepare_batch_file(test_reqs, "dataset_generator/test_batch.jsonl")
