"""
Chandra — Router OpenAI-compatible con 7 tools (BMO Obsidian + clientes externos)
=================================================================================
Endpoint: POST /opos/v1/chat/completions

Formato: OpenAI Chat Completions (compatible con BMO de Obsidian, Open WebUI, etc.)

Modelo principal: Mistral (mistral-medium-latest) con function calling iterativo.

Flujo:
  1. Recibe messages OpenAI-style (system + user + assistant + tool roles).
  2. Llama a Mistral con CHANDRA_TOOLS_SCHEMA.
  3. Si Mistral devuelve tool_calls, ejecuta las 7 manos en paralelo.
  4. Inyecta resultados como mensajes 'tool' y vuelve a llamar a Mistral.
  5. Repite hasta que Mistral devuelve respuesta final (sin tool_calls) o max_iterations=10.

Author: Cascade + Spas (29/04/2026 · actualizado 03/05/2026 con 7ª mano escribir_vault)
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import time
import uuid
from typing import Any, AsyncGenerator, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# Imports relativos al patrón del proyecto (backend/main.py añade backend/ al path)
try:
    from agents.chandra_tools import CHANDRA_TOOLS_SCHEMA, execute_tool
except ImportError:
    from backend.agents.chandra_tools import CHANDRA_TOOLS_SCHEMA, execute_tool

# ============================================================================
# Configuración
# ============================================================================

router = APIRouter(prefix="/opos", tags=["chandra"])

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")

# IMPORTANTE: forzamos la URL oficial de Mistral.
# La variable MISTRAL_URL del .env apunta a un proxy VPS personal del usuario
# (electroyhogarpelotazo.tienda) que ya no está activo. BMO y Copilot de Obsidian
# usan directamente api.mistral.ai con su propia config, así que aquí también.
_MISTRAL_OFFICIAL = "https://api.mistral.ai/v1"
_env_url = os.getenv("MISTRAL_URL", "").strip()
MISTRAL_URL = _env_url if (_env_url and "mistral.ai" in _env_url) else _MISTRAL_OFFICIAL

MISTRAL_MODEL = os.getenv("MISTRAL_AGENT_MODEL", "mistral-medium-latest")

MAX_TOOL_ITERATIONS = 10  # límite de loop tool calls
MIN_TEMPERATURE_TOOLS = 0.0  # determinismo durante razonamiento
TEMPERATURE_FINAL = 0.3  # algo más cálido en respuesta final

CHANDRA_SYSTEM_PROMPT = """Eres **Chandra**, un agente jurídico especialista en oposiciones de la Seguridad Social española (corte legal: 04/03/2026).

Tienes **7 herramientas** disponibles (úsalas sin pedir permiso al usuario):
- **tavily_search**: web search para jurisprudencia/doctrina actual.
- **search_boe**: BOE legislación consolidada (devuelve IDs BOE-A-YYYY-NNNN).
- **get_law_text_block**: texto exacto de un artículo BOE (USA SIEMPRE as_of_date='20260304' para examen 2026).
- **consultar_neo4j**: grafo legal Neo4j (relaciones, modificaciones, jerarquía).
- **calcular_ss**: calculadora SS verificada (jubilación, IT, IPA, desempleo, brecha género, PNC, etc.).
- **buscar_vault**: LEE notas del vault Obsidian del opositor (trampas verificadas, esquemas, casos, apuntes). Úsala siempre que necesites contexto ya curado o consultar algo que escribiste antes.
- **escribir_vault**: CREA o AÑADE notas en el vault Obsidian del opositor. Úsala cuando quieras guardar una respuesta de caso práctico, un esquema, un resumen o cualquier contenido que el usuario deba conservar. Parámetros: `path` (ruta tipo `casos_practicos/caso_01.md`), `content` (markdown), `mode` (`overwrite` o `append`).

REGLAS:
1. **Cita siempre el artículo y la URL BOE oficial** (https://www.boe.es/buscar/act.php?id=BOE-A-...).
2. Si el usuario pide un cálculo, **usa calcular_ss** (NO calcules a ojo).
3. Si dudas de una cita, **verifica con get_law_text_block** antes de afirmar.
4. **Fecha de corte = 04/03/2026**: ignora normas posteriores salvo que el usuario pida explícitamente normativa más reciente.
5. **Idioma: español de España**. Tono directo y profesional. Si hay trampa típica de examen, márcala explícitamente.
6. Si una tool devuelve `{"error": ...}`, intenta otra estrategia o pídele al usuario los datos faltantes.
7. **Cuando el usuario te pida guardar/escribir/crear una nota en el vault, usa `escribir_vault` sin preguntar**. Nunca digas "no puedo escribir en el vault": SÍ puedes, tienes la herramienta.
8. **Cuando el usuario te pida leer/buscar/ver una nota del vault, usa `buscar_vault`**. Nunca digas "no tengo acceso al vault": SÍ lo tienes.
9. **CONCISIÓN OBLIGATORIA**: respuestas directas, sin relleno, sin paráfrasis innecesarias ni introducciones tipo "¡Buena pregunta!" o "Con mucho gusto...". Solo los campos del FORMATO. Máximo 400 palabras salvo que el usuario pida desarrollo explícito. Si la respuesta es corta, el texto también.
10. **NO CONFIES EN TU CONOCIMIENTO PREVIO**: toda afirmación jurídica (artículo, cuantía, plazo, fecha, URL BOE, existencia de norma, nombre de ley) DEBE verificarse con tools antes de escribirse. Si no puedes verificar, responde "DATO NO VERIFICABLE, consulta manual BOE" en vez de inventar.
11. **EXCEPCIONES ANTES QUE REGLAS**: la legislación SS tiene muchas excepciones. Antes de dar una regla general, pregúntate qué excepciones existen y verifica cuál aplica al caso.

FORMATO RESPUESTA FINAL (todos los campos obligatorios, en este orden):
- **Respuesta**: solución directa (1-3 líneas).
- **Fundamento legal**: Art. X [nombre norma] — BOE-A-AAAA-NNNN.
- **URL BOE**: https://www.boe.es/buscar/act.php?id=BOE-A-... (verificada con tool, no inventada).
- **Cálculo** (si aplica): pasos verificados con calcular_ss.
- **Verificaciones realizadas**: listado escueto de tools usadas y resultado (ej. "get_law_text_block(BOE-A-2015-11724, a170) → texto vigente confirmado").
- **Trampa de examen** (si la detectas): aviso explícito, 1 línea.
- **Confianza**: ALTA / MEDIA / BAJA — baja si alguna verificación falló.
"""


# ============================================================================
# Modelos Pydantic (formato OpenAI)
# ============================================================================

class ChatMessage(BaseModel):
    role: str  # 'system' | 'user' | 'assistant' | 'tool'
    content: Optional[str] = None
    name: Optional[str] = None
    tool_call_id: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None


class ChatCompletionRequest(BaseModel):
    model: Optional[str] = None  # ignorado, usamos MISTRAL_MODEL
    messages: List[ChatMessage]
    temperature: Optional[float] = None
    max_tokens: Optional[int] = 2000
    stream: Optional[bool] = False
    tools: Optional[List[Dict[str, Any]]] = None  # ignorado, usamos los nuestros


# ============================================================================
# Cliente Mistral con function calling
# ============================================================================

async def call_mistral(
    messages: List[Dict[str, Any]],
    tools: Optional[List[Dict[str, Any]]] = None,
    temperature: float = 0.0,
    max_tokens: int = 2000,
) -> Dict[str, Any]:
    """Llamada única a Mistral chat completions con tools."""
    if not MISTRAL_API_KEY:
        raise HTTPException(status_code=500, detail="MISTRAL_API_KEY no configurada")

    import httpx

    payload = {
        "model": MISTRAL_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{MISTRAL_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {MISTRAL_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        if response.status_code != 200:
            logger.error(f"Mistral error {response.status_code}: {response.text[:500]}")
            raise HTTPException(status_code=502, detail=f"Mistral error: {response.text[:200]}")
        return response.json()


# ============================================================================
# Loop de tool calls iterativo
# ============================================================================

async def chandra_loop(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Loop hasta que Mistral devuelva respuesta sin tool_calls o se agoten iteraciones."""
    # Inyectar system prompt si no existe
    import datetime
    today_str = datetime.datetime.now().strftime('%Y-%m-%d')
    date_context = f"\n[SISTEMA - IMPORTANTE: LA FECHA ACTUAL DE HOY ES {today_str}. Basa todas tus búsquedas temporales (ej. 'hoy', 'este año') estrictamente en esta fecha real.]\n"
    
    # Inyectar system prompt si no existe, o añadir contexto de fecha al existente
    has_system = False
    for m in messages:
        if m.get("role") == "system":
            m["content"] = str(m.get("content", "")) + date_context
            has_system = True
            
    if not has_system:
        messages = [{"role": "system", "content": CHANDRA_SYSTEM_PROMPT + date_context}] + messages

    iteration = 0
    while iteration < MAX_TOOL_ITERATIONS:
        iteration += 1
        is_final = iteration == MAX_TOOL_ITERATIONS
        temperature = TEMPERATURE_FINAL if is_final else MIN_TEMPERATURE_TOOLS

        logger.info(f"Chandra iteration {iteration}/{MAX_TOOL_ITERATIONS}")

        response = await call_mistral(
            messages=messages,
            tools=CHANDRA_TOOLS_SCHEMA if not is_final else None,
            temperature=temperature,
        )

        choice = response["choices"][0]
        message = choice["message"]
        tool_calls = message.get("tool_calls") or []

        # Caso 1: respuesta final sin tools
        if not tool_calls:
            logger.info(f"Chandra completó en {iteration} iteraciones")
            return {
                "id": response.get("id", f"chandra-{uuid.uuid4()}"),
                "object": "chat.completion",
                "created": int(time.time()),
                "model": MISTRAL_MODEL,
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": message.get("content", ""),
                        },
                        "finish_reason": choice.get("finish_reason", "stop"),
                    }
                ],
                "usage": response.get("usage", {}),
                "chandra_iterations": iteration,
            }

        # Caso 2: hay tool_calls — ejecutar y continuar loop
        # Añadir el mensaje del assistant (con tool_calls)
        messages.append({
            "role": "assistant",
            "content": message.get("content", ""),
            "tool_calls": tool_calls,
        })

        # Ejecutar todas las tools en paralelo
        async def run_tool(tc: Dict[str, Any]) -> Dict[str, Any]:
            tool_id = tc.get("id", f"call_{uuid.uuid4()}")
            fn = tc.get("function", {})
            name = fn.get("name", "")
            args_raw = fn.get("arguments", "{}")
            try:
                args = json.loads(args_raw) if isinstance(args_raw, str) else args_raw
            except json.JSONDecodeError as e:
                return {
                    "tool_call_id": tool_id,
                    "name": name,
                    "result": {"error": f"JSON inválido en arguments: {e}"},
                }
            logger.info(f"  → Tool {name}({list(args.keys())})")
            result = await execute_tool(name, args)
            return {"tool_call_id": tool_id, "name": name, "result": result}

        tool_results = await asyncio.gather(*[run_tool(tc) for tc in tool_calls])

        for tr in tool_results:
            messages.append({
                "role": "tool",
                "tool_call_id": tr["tool_call_id"],
                "name": tr["name"],
                "content": json.dumps(tr["result"], ensure_ascii=False, default=str)[:8000],
            })

    # Si se agotan las iteraciones sin respuesta final
    logger.warning("Chandra alcanzó MAX_TOOL_ITERATIONS sin respuesta final")
    return {
        "id": f"chandra-timeout-{uuid.uuid4()}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": MISTRAL_MODEL,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": (
                        "Lo siento, he agotado mis iteraciones de razonamiento sin llegar a una respuesta "
                        "definitiva. ¿Puedes reformular la pregunta o darme más contexto?"
                    ),
                },
                "finish_reason": "length",
            }
        ],
        "chandra_iterations": MAX_TOOL_ITERATIONS,
    }


# ============================================================================
# Endpoints
# ============================================================================

@router.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """Endpoint OpenAI-compatible. BMO Obsidian apunta aquí."""
    try:
        messages = [m.dict(exclude_none=True) for m in request.messages]

        if request.stream:
            # Streaming simple: devolvemos como single chunk al final
            # (BMO acepta tanto stream como non-stream)
            async def stream_gen() -> AsyncGenerator[bytes, None]:
                result = await chandra_loop(messages)
                content = result["choices"][0]["message"]["content"]
                # Format SSE OpenAI-compatible
                chunk = {
                    "id": result["id"],
                    "object": "chat.completion.chunk",
                    "created": result["created"],
                    "model": result["model"],
                    "choices": [
                        {
                            "index": 0,
                            "delta": {"role": "assistant", "content": content},
                            "finish_reason": None,
                        }
                    ],
                }
                yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n".encode("utf-8")
                # Final chunk
                final = {
                    "id": result["id"],
                    "object": "chat.completion.chunk",
                    "created": result["created"],
                    "model": result["model"],
                    "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
                }
                yield f"data: {json.dumps(final, ensure_ascii=False)}\n\n".encode("utf-8")
                yield b"data: [DONE]\n\n"

            return StreamingResponse(stream_gen(), media_type="text/event-stream")

        # No-stream
        result = await chandra_loop(messages)
        return JSONResponse(content=result)

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("chat_completions error")
        raise HTTPException(status_code=500, detail=f"Chandra fallo: {e}")


@router.get("/v1/models")
async def list_models():
    """Modelo único expuesto: chandra (alias de Mistral con 6 tools)."""
    return {
        "object": "list",
        "data": [
            {
                "id": "chandra",
                "object": "model",
                "created": 1714339200,
                "owned_by": "opositaia",
                "description": (
                    "Chandra: agente jurídico especialista oposiciones SS 2026. "
                    "Mistral + 6 tools (Tavily, BOE, Neo4j, Calculadoras SS, Vault Obsidian)."
                ),
            }
        ],
    }


@router.get("/health")
async def chandra_health():
    """Health check con verificación de credenciales."""
    return {
        "status": "healthy",
        "model": MISTRAL_MODEL,
        "mistral_url": MISTRAL_URL,
        "mistral_url_env_raw": os.getenv("MISTRAL_URL", "(unset)"),
        "tools_loaded": len(CHANDRA_TOOLS_SCHEMA),
        "tool_names": [t["function"]["name"] for t in CHANDRA_TOOLS_SCHEMA],
        "credentials": {
            "mistral": bool(MISTRAL_API_KEY),
            "tavily": bool(os.getenv("TAVILY_API_KEY")),
            "neo4j": bool(os.getenv("NEO4J_URI")),
            "obsidian": bool(os.getenv("OBSIDIAN_REST_URL")),
        },
        "max_iterations": MAX_TOOL_ITERATIONS,
        "fecha_corte_legal": "2026-03-04",
    }


@router.post("/v1/tools/test/{tool_name}")
async def test_tool(tool_name: str, args: Dict[str, Any]):
    """Endpoint debug: ejecutar una tool directamente sin pasar por LLM."""
    result = await execute_tool(tool_name, args)
    return {"tool": tool_name, "args": args, "result": result}
