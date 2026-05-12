"""
Lanzador ligero de Chandra — Solo el router opos_chat con 6 tools.
Evita importar torch/sentence_transformers que bloquean el arranque.

Endpoints (AMBOS funcionan, para compatibilidad BMO + Copilot):
  POST /v1/chat/completions         ← Copilot apunta aquí
  POST /opos/v1/chat/completions    ← BMO apunta aquí (también vale)
  GET  /v1/models                   ← Copilot lista modelos
  GET  /opos/v1/models              ← BMO lista modelos
  GET  /opos/health                 ← Health check detallado
  GET  /health                      ← Health check simple
"""

import os
import sys
import time
import logging
from pathlib import Path

# Cargar .env.backend ANTES de importar nada que lea os.getenv
from dotenv import load_dotenv
env_path = Path(__file__).parent / ".env.backend"
load_dotenv(dotenv_path=env_path, override=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("chandra")

# Verificar credenciales
api_key = os.getenv("MISTRAL_API_KEY", "")
model = os.getenv("MISTRAL_AGENT_MODEL", "mistral-medium-latest")
obsidian = os.getenv("OBSIDIAN_REST_URL", "")
log.info(f"🔑 MISTRAL_API_KEY: {'✅ ' + api_key[:8] + '...' if api_key else '❌ MISSING'}")
log.info(f"🤖 Modelo: {model}")
log.info(f"📦 Obsidian URL: {obsidian or '❌ MISSING'}")
log.info(f"🔍 TAVILY_API_KEY: {'✅' if os.getenv('TAVILY_API_KEY') else '❌ MISSING'}")
log.info(f"🗄️  NEO4J_URI: {os.getenv('NEO4J_URI', '❌ MISSING')}")

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

# Importar SOLO el router de Chandra
sys.path.insert(0, str(Path(__file__).parent))
from routers.opos_chat import router as chandra_router

app = FastAPI(title="Chandra — Agente Jurídico OPOS SS")

# ============================================================================
# MIDDLEWARE: Log TODA petición entrante (para debugging)
# ============================================================================
class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        # Log de entrada
        client = request.client.host if request.client else "?"
        log.info(f"📥 {request.method} {request.url.path} ← {client}")
        if request.url.query:
            log.info(f"   query: {request.url.query}")
        # Headers relevantes (sin volcar todo)
        auth = request.headers.get("authorization", "")
        if auth:
            log.info(f"   auth: {auth[:30]}...")
        content_type = request.headers.get("content-type", "")
        if content_type:
            log.info(f"   content-type: {content_type}")

        response = await call_next(request)
        elapsed = time.time() - start
        log.info(f"📤 {response.status_code} ({elapsed:.2f}s) → {request.method} {request.url.path}")
        return response

app.add_middleware(RequestLoggerMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Router Chandra montado en DOS prefijos para máxima compatibilidad
# ============================================================================
# /opos/v1/chat/completions  ← BMO con REST API URL
app.include_router(chandra_router)
# /v1/chat/completions        ← Copilot con openAIProxyBaseUrl
# Copilot construye: {openAIProxyBaseUrl}/chat/completions
# Si openAIProxyBaseUrl = "http://127.0.0.1:8000/v1"
# entonces llama a: http://127.0.0.1:8000/v1/chat/completions
#
# Pero nuestro router tiene prefix="/opos" y el endpoint es /v1/chat/completions
# → Copilot necesita /v1/chat/completions en la raíz
from routers.opos_chat import router as chandra_router_root

# Crear un segundo montaje sin el prefijo /opos
from fastapi import APIRouter
root_router = APIRouter(tags=["chandra-root"])

# Re-exportar los endpoints críticos en /v1/...
from routers.opos_chat import chat_completions, list_models, chandra_health, test_tool
from typing import Dict, Any

@root_router.post("/v1/chat/completions")
async def root_chat_completions(request: Request):
    """Proxy directo al endpoint Chandra para Copilot."""
    from routers.opos_chat import ChatCompletionRequest
    import json
    body = await request.body()
    data = json.loads(body)
    req = ChatCompletionRequest(**data)
    return await chat_completions(req)

@root_router.get("/v1/models")
async def root_list_models():
    return await list_models()

app.include_router(root_router)


@app.get("/")
async def root():
    return {
        "service": "Chandra",
        "status": "running",
        "model": model,
        "endpoints": [
            "POST /v1/chat/completions (Copilot)",
            "POST /opos/v1/chat/completions (BMO)",
            "GET /v1/models",
            "GET /opos/v1/models",
            "GET /opos/health",
        ],
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "chandra-standalone",
        "model": model,
        "mistral_key": bool(api_key),
        "obsidian_url": obsidian,
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PROXY_PORT", "8000"))
    log.info(f"🚀 Arrancando Chandra en 0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
