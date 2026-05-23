import os
import re
import json
import time
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from mistralai import Mistral

# ==========================================
# 🔐 CARGA DE VARIABLES DE ENTORNO (.env.backend)
# ==========================================
ENV_PATH = Path(__file__).parent / ".env.backend"
load_dotenv(ENV_PATH)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("agente-escritor")

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "").strip()
OBSIDIAN_API_KEY = os.getenv("OBSIDIAN_REST_API_KEY", "").strip()
OBSIDIAN_REST_URL_ENV = os.getenv("OBSIDIAN_REST_URL", "").strip()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "").strip()
MISTRAL_MODEL = os.getenv("MISTRAL_AGENT_MODEL", "mistral-large-latest")
PROXY_PORT = int(os.getenv("PROXY_PORT", "8000"))
OBSIDIAN_PORT = 27123

if not MISTRAL_API_KEY:
    log.warning("⚠️  MISTRAL_API_KEY no configurada en .env.backend. El proxy no podrá llamar a Mistral.")
if not OBSIDIAN_API_KEY:
    log.warning("⚠️  OBSIDIAN_REST_API_KEY no configurada. Las herramientas de vault fallarán.")

app = FastAPI(title="Agente EscritorAIA Proxy")


def detectar_ip_windows() -> Optional[str]:
    """Detecta la IP del host Windows desde WSL usando `ip route`.
    La IP de WSL2 cambia tras cada reinicio de Windows."""
    try:
        out = subprocess.check_output(["ip", "route"], text=True, timeout=2)
        for line in out.splitlines():
            if line.startswith("default via "):
                return line.split()[2]
    except Exception as e:
        log.warning(f"No pude detectar IP Windows via 'ip route': {e}")
    return None


def get_obsidian_base_url() -> str:
    """Resuelve la URL del REST API de Obsidian.
    Prioridad: 1) OBSIDIAN_REST_URL en .env, 2) detección dinámica IP Windows, 3) localhost."""
    if OBSIDIAN_REST_URL_ENV:
        return OBSIDIAN_REST_URL_ENV
    ip = detectar_ip_windows()
    if ip:
        return f"http://{ip}:{OBSIDIAN_PORT}"
    return f"http://127.0.0.1:{OBSIDIAN_PORT}"


OBSIDIAN_URL = get_obsidian_base_url()
log.info(f"🔗 Obsidian URL: {OBSIDIAN_URL}")
log.info(f"🤖 Mistral model: {MISTRAL_MODEL}")

HEADERS = {
    "Authorization": f"Bearer {OBSIDIAN_API_KEY}",
    "Content-Type": "text/markdown",
}

# ==========================================
# 🛠️ LA MAGIA: DEFINICIÓN DE HERRAMIENTAS
# ==========================================

def read_obsidian_note(filename: str) -> str:
    """Lee el contenido de una nota de Obsidian dada su ruta relativa."""
    filename = filename.replace(" ", "%20")
    if not filename.endswith(".md"): filename += ".md"
    
    url = f"{OBSIDIAN_URL}/vault/{filename}"
    try:
        r = requests.get(url, headers={"Authorization": HEADERS["Authorization"]})
        if r.status_code == 200:
            return r.text
        return f"Error: No se encontró la nota (Código {r.status_code})"
    except Exception as e:
        return f"Error de conexión: {str(e)}"

def create_obsidian_note(filename: str, content: str) -> str:
    """Crea un fichero nuevo Markdown y escribe el contenido dentro del vault."""
    filename = filename.replace(" ", "%20")
    if not filename.endswith(".md"): filename += ".md"
    
    url = f"{OBSIDIAN_URL}/vault/{filename}"
    try:
        r = requests.put(url, headers=HEADERS, data=content.encode('utf-8'))
        if r.status_code in [200, 201, 204]:
            return f"¡Éxito! La nota {filename} fue creda perfectamente."
        return f"Fallo al crear nota. Código {r.status_code}"
    except Exception as e:
        return f"Error de conexión: {str(e)}"

def update_obsidian_note(filename: str, content: str) -> str:
    """Añade (append) contenido al final de una nota Markdown existente."""
    filename = filename.replace(" ", "%20")
    if not filename.endswith(".md"): filename += ".md"
    
    url = f"{OBSIDIAN_URL}/vault/{filename}"
    try:
        # POST para append
        r = requests.post(url, headers=HEADERS, data=content.encode('utf-8'))
        if r.status_code in [200, 201, 204]:
            return f"¡Éxito! Texto añadido a {filename}."
        return f"Fallo al editar nota. Código {r.status_code}"
    except Exception as e:
        return f"Error de conexión: {str(e)}"


_TEMPORAL_KEYWORDS = (
    "hoy", "actual", "actuales", "reciente", "recientes", "esta semana",
    "este mes", "este año", "noticias", "ultim", "últim", "latest",
    "today", "recent", "news", "yesterday", "ayer",
)


def _enrich_query_with_date(query: str) -> str:
    """Anclamos la query al año en curso para evitar que Mistral recupere
    noticias viejas de 2024. Reglas:
    - Si la query contiene años 2022-2024 explícitos, los sustituimos por año actual.
    - Si la query es temporal (palabras 'hoy', 'noticias', etc.) y no tiene año,
      añadimos el año actual al final.
    - Resto de queries, intactas."""
    current_year = datetime.now().year
    q = query

    # 1) Sustituir años 2022/2023/2024 por año actual si aparecen (Mistral los inventa)
    q = re.sub(r"\b(202[234])\b", str(current_year), q)

    # 2) Si no hay año y la query huele a temporal, añadir año actual
    has_year = bool(re.search(r"\b20\d{2}\b", q))
    lower = q.lower()
    is_temporal = any(kw in lower for kw in _TEMPORAL_KEYWORDS)
    if not has_year and is_temporal:
        q = f"{q} {current_year}"

    if q != query:
        log.info(f"🕐 Query reescrita para fecha actual: '{query}' -> '{q}'")
    return q


def _wrap_results_with_date_anchor(resultados_json: str) -> str:
    """Envuelve los resultados de búsqueda con un recordatorio de la fecha real
    para que Mistral NO reporte fechas que aparecen en los snippets antiguos."""
    fecha = _fecha_humana_es()
    año = datetime.now().year
    aviso = (
        f"[FECHA_REAL_DE_HOY: {fecha}. AÑO_EN_CURSO: {año}. "
        f"IMPORTANTE: los snippets pueden referirse a fechas antiguas, "
        f"pero cuando resumas al usuario indica SIEMPRE que es información "
        f"vigente a día de HOY ({año}). NO digas 'octubre 2024' ni 'el futuro', "
        f"estamos en {año}.]\n\nRESULTADOS:\n"
    )
    return aviso + resultados_json


def search_internet(query: str, max_results: int = 5) -> str:
    """Busca en internet con Tavily si hay key, si no DuckDuckGo HTML scraping.
    Reescribe la query para anclar al año actual y envuelve los resultados con
    un aviso de fecha real (anti-alucinación temporal de Mistral)."""
    query = _enrich_query_with_date(query)
    log.info(f"🔍 search_internet: '{query}'")

    # Camino A: Tavily (si hay key) — más fiable, con filtro temporal
    if TAVILY_API_KEY:
        try:
            r = requests.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": TAVILY_API_KEY,
                    "query": query,
                    "max_results": max_results,
                    "search_depth": "basic",
                    "days": 30,  # solo resultados de los últimos 30 días
                },
                timeout=15,
            )
            if r.status_code == 200:
                data = r.json()
                payload = json.dumps(data.get("results", []), ensure_ascii=False, indent=2)
                return _wrap_results_with_date_anchor(payload)
            log.warning(f"Tavily HTTP {r.status_code}, fallback a DuckDuckGo")
        except Exception as e:
            log.warning(f"Tavily falló: {e}, fallback a DuckDuckGo")

    # Camino B: DuckDuckGo HTML scrape (sin API key, gratis)
    try:
        r = requests.get(
            "https://html.duckduckgo.com/html/",
            params={"q": query},
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
            },
            timeout=15,
        )
        if r.status_code != 200:
            return f"[search_internet] DuckDuckGo HTTP {r.status_code}"
        soup = BeautifulSoup(r.text, "html.parser")
        resultados = []
        for div in soup.select("div.result")[:max_results]:
            titulo_a = div.select_one("a.result__a")
            snippet_el = div.select_one(".result__snippet")
            url_el = div.select_one("a.result__url")
            if titulo_a:
                resultados.append({
                    "titulo": titulo_a.get_text(strip=True),
                    "url": (url_el.get_text(strip=True) if url_el else titulo_a.get("href", "")),
                    "snippet": snippet_el.get_text(strip=True) if snippet_el else "",
                })
        if not resultados:
            return f"[search_internet] Sin resultados para: '{query}'"
        payload = json.dumps(resultados, ensure_ascii=False, indent=2)
        return _wrap_results_with_date_anchor(payload)
    except Exception as e:
        log.error(f"search_internet error: {e}")
        return f"[search_internet] Error: {str(e)}"

# Mapeo para ejecución
names_to_functions = {
    "read_obsidian_note": read_obsidian_note,
    "create_obsidian_note": create_obsidian_note,
    "update_obsidian_note": update_obsidian_note,
    "search_internet": search_internet,
}

tools = [
     {
        "type": "function",
        "function": {
            "name": "read_obsidian_note",
            "description": "Lee el contenido exacto de una nota guardada en tu vault de Obsidian.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Nombre del archivo, ej: 'Personajes/Duque_Juan.md'"}
                },
                "required": ["filename"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_obsidian_note",
            "description": "Crea una nota física en el disco duro del vault de Obsidian. Úsalo si el usuario te pide generar una ficha, esquema o capitulo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Ruta y nombre (Personajes/Nuevo.md)"},
                    "content": {"type": "string", "description": "El contenido markdown completo a escribir."}
                },
                "required": ["filename", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_obsidian_note",
            "description": "Añade texto al final de una nota existente.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Ruta y nombre"},
                    "content": {"type": "string", "description": "El texto que añadirás al final."}
                },
                "required": ["filename", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_internet",
            "description": "Usa internet para consultar información histórica o externa que no sabes. No lo uses si solo es corrección de textos locales.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "La consulta de investigación precisa"}
                },
                "required": ["query"],
            },
        },
    }
]


# ==========================================
# 🔀 ENDPOINT PROXY (Engañando a BMO / Copilot)
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_MESES_ES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]
_DIAS_ES = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


def _fecha_humana_es() -> str:
    now = datetime.now()
    return (
        f"{_DIAS_ES[now.weekday()]}, {now.day} de {_MESES_ES[now.month - 1]} "
        f"de {now.year}, {now.strftime('%H:%M')}"
    )


def build_critical_context() -> str:
    """Contexto mínimo que siempre se inyecta: recordatorio de tools disponibles.
    No inyectamos fecha: si el modelo la necesita, que llame a `search_internet`."""
    return (
        "[HERRAMIENTAS DISPONIBLES PARA ESTE CHAT]\n"
        "- `search_internet(query)`: búsqueda web en tiempo real. Úsala SIEMPRE que "
        "necesites información actual (fecha de hoy, noticias, eventos, cotizaciones, "
        "clima, datos posteriores a tu entrenamiento). No inventes, busca.\n"
        "- `create_obsidian_note(filename, content)`: crea una nota .md en el vault "
        "Obsidian del usuario. Úsala solo si el usuario lo pide explícitamente.\n"
        "- `read_obsidian_note(filename)` / `update_obsidian_note(filename, content)`: "
        "lee o añade contenido a una nota existente.\n"
        "Responde en el idioma del usuario (español o búlgaro).\n"
    )


SYSTEM_PROMPT_FALLBACK = (
    "Eres un agente de investigación y redacción con acceso a internet y al vault "
    "Obsidian del usuario. Sé conciso, útil y preciso. Si no sabes algo actual, "
    "busca con `search_internet` antes de responder."
)

@app.get("/v1/models")
async def get_models():
    """Endpoint compatible OpenAI: lista de modelos disponibles."""
    return {
        "object": "list",
        "data": [
            {
                "id": "agente-escritor",
                "object": "model",
                "created": 1686935002,
                "owned_by": "custom",
            }
        ],
    }


@app.get("/health")
async def health():
    """Health check del proxy y de los servicios externos."""
    obsidian_ok = False
    obsidian_err = None
    try:
        r = requests.get(
            f"{OBSIDIAN_URL}/",
            headers={"Authorization": HEADERS["Authorization"]},
            timeout=3,
        )
        obsidian_ok = r.status_code == 200
        if not obsidian_ok:
            obsidian_err = f"HTTP {r.status_code}"
    except Exception as e:
        obsidian_err = str(e)

    return {
        "proxy": "ok",
        "port": PROXY_PORT,
        "mistral_key_present": bool(MISTRAL_API_KEY),
        "obsidian_url": OBSIDIAN_URL,
        "obsidian_reachable": obsidian_ok,
        "obsidian_error": obsidian_err,
        "tavily_present": bool(TAVILY_API_KEY),
        "model": MISTRAL_MODEL,
    }

@app.post("/v1/chat/completions")
async def proxy_chat(request: Request):
    """Endpoint OpenAI-compatible. Acepta messages, opcionalmente tools (las ignora,
    nosotros forzamos las nuestras), retorna SIEMPRE JSON válido aunque haya error
    para evitar el famoso `SyntaxError: Unexpected token 'B', 'Bearer tok...'` en BMO."""
    try:
        data = await request.json()
    except Exception as e:
        log.error(f"Body no es JSON válido: {e}")
        return JSONResponse(
            status_code=400,
            content={"error": {"message": f"Invalid JSON body: {e}", "type": "invalid_request"}},
        )

    incoming_messages = data.get("messages", [])
    if not incoming_messages:
        return JSONResponse(
            status_code=400,
            content={"error": {"message": "messages array missing", "type": "invalid_request"}},
        )

    if not MISTRAL_API_KEY:
        return JSONResponse(
            status_code=500,
            content={"error": {"message": "MISTRAL_API_KEY no configurada en .env.backend", "type": "server_misconfigured"}},
        )

    # SIEMPRE inyectamos el contexto crítico (fecha real + recordatorio de tools).
    # Si el cliente (BMO plugin) ya mandó un system, lo combinamos: contexto crítico
    # primero, luego su system. Así respetamos sus instrucciones pero garantizamos que
    # Mistral conozca la fecha y sepa que puede usar tools.
    critical = build_critical_context()
    if incoming_messages and incoming_messages[0].get("role") == "system":
        client_system = incoming_messages[0].get("content", "") or ""
        merged_system = (
            critical
            + "\n\n[INSTRUCCIONES DEL CLIENTE]\n"
            + client_system
        )
        messages = [{"role": "system", "content": merged_system}] + list(incoming_messages[1:])
    else:
        messages = [
            {"role": "system", "content": critical + "\n\n" + SYSTEM_PROMPT_FALLBACK}
        ] + list(incoming_messages)

    log.info(f"🚀 Petición interceptada ({len(messages)} mensajes). Iniciando agencia Mistral…")

    client = Mistral(api_key=MISTRAL_API_KEY)

    try:
        response = client.chat.complete(
            model=MISTRAL_MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
    except Exception as e:
        log.error(f"[Mistral inicial] {e}")
        return JSONResponse(
            status_code=502,
            content={"error": {"message": f"Mistral error: {e}", "type": "upstream_error"}},
        )

    messages.append(response.choices[0].message)

    # --- BUCLE DE AGENTE AUTÓNOMO ---
    max_steps = 6
    step = 0
    while response.choices[0].message.tool_calls and step < max_steps:
        step += 1
        n_tools = len(response.choices[0].message.tool_calls)
        log.info(f"[AGENTE paso {step}] ejecutando {n_tools} tool(s)…")

        for tool_call in response.choices[0].message.tool_calls:
            f_name = tool_call.function.name
            try:
                f_args = json.loads(tool_call.function.arguments)
            except Exception:
                f_args = {}
            log.info(f"  └─ {f_name}({list(f_args.keys())})")
            f_func = names_to_functions.get(f_name)
            try:
                f_res = f_func(**f_args) if f_func else f"Función '{f_name}' no mapeada."
            except Exception as e:
                f_res = f"Error ejecutando {f_name}: {e}"
                log.error(f_res)

            messages.append({
                "role": "tool",
                "name": f_name,
                "content": str(f_res),
                "tool_call_id": tool_call.id,
            })

        try:
            response = client.chat.complete(
                model=MISTRAL_MODEL,
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )
        except Exception as e:
            log.error(f"[Mistral paso {step}] {e}")
            return JSONResponse(
                status_code=502,
                content={"error": {"message": f"Mistral error en bucle: {e}", "type": "upstream_error"}},
            )
        messages.append(response.choices[0].message)

    final_text = response.choices[0].message.content or "Tarea finalizada exitosamente."
    log.info("✅ Respuesta final generada.")

    return {
        "id": f"chatcmpl-{int(time.time())}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "agente-escritor",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": final_text},
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        },
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PROXY_PORT)
