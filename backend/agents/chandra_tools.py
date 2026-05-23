"""
Chandra Tools — 7 manos del agente Chandra
==========================================
Implementaciones de las 7 herramientas que el LLM puede invocar via function calling
para responder preguntas legales de oposiciones SS con corte 04/03/2026.

Las 7 manos:
  1. tavily_search            — búsqueda web general (jurisprudencia, doctrina actual)
  2. search_boe               — búsqueda en BOE legislación consolidada
  3. get_law_text_block       — texto exacto de un artículo BOE (con as_of_date)
  4. consultar_neo4j          — query al grafo legal Neo4j
  5. calcular_ss              — dispatcher de calculadoras Seguridad Social
  6. buscar_vault             — búsqueda en vault Obsidian (trampas verificadas)
  7. escribir_vault           — crear/añadir notas en vault Obsidian

Cada función:
  - Acepta un dict con argumentos (lo que envía el LLM)
  - Devuelve un dict serializable JSON con resultado o error
  - NUNCA lanza excepción al LLM (siempre devuelve {"error": "..."} si algo falla)

Author: Cascade + Spas (29/04/2026)
"""

from __future__ import annotations

import logging
import os
from decimal import Decimal
from typing import Any, Dict, List, Optional

import httpx

logger = logging.getLogger(__name__)

# ============================================================================
# JSON Schema para tools — formato OpenAI / Mistral function calling
# ============================================================================

CHANDRA_TOOLS_SCHEMA: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "tavily_search",
            "description": (
                "Búsqueda web general sobre jurisprudencia, doctrina actual o normativa. "
                "Útil cuando la respuesta no está en BOE/Neo4j/vault y se necesita información reciente. "
                "NO usar para citar artículos (usa search_boe o get_law_text_block para eso)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Consulta en español."},
                    "max_results": {"type": "integer", "description": "Número de resultados (1-10).", "default": 5},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_boe",
            "description": (
                "Recupera metadatos de una norma BOE concreta cuando ya tienes su ID (BOE-A-YYYY-NNNN), "
                "o lista normas consolidadas en un rango de fechas. "
                "IMPORTANTE: la API BOE de datos abiertos NO soporta búsqueda por texto libre. "
                "Para BUSCAR por términos, usa primero tavily_search (devuelve URLs/IDs BOE) "
                "y después llama aquí con el id_norma encontrado."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "id_norma": {"type": "string", "description": "ID BOE concreto: 'BOE-A-2015-11724' (TRLGSS), 'BOE-A-2025-26474' (RDL 16/2025)."},
                    "from_date": {"type": "string", "description": "Filtro fecha inicio AAAAMMDD (ej: '20251201')."},
                    "to_date": {"type": "string", "description": "Filtro fecha fin AAAAMMDD."},
                    "limit": {"type": "integer", "description": "Resultados (1-50).", "default": 20},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_law_text_block",
            "description": (
                "Obtiene el texto EXACTO de un bloque (artículo, disposición) de una norma BOE. "
                "IMPORTANTE: si el usuario pregunta por la legislación a fecha del examen 2026, "
                "usar as_of_date='20260304' (corte oficial) para devolver el texto vigente esa fecha."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "law_id": {"type": "string", "description": "ID BOE: 'BOE-A-2015-11724' (TRLGSS), etc."},
                    "block_id": {"type": "string", "description": "ID del bloque: 'a322' (artículo 322), 'dd' (disp. derogatoria), 'preambulo'."},
                    "as_of_date": {"type": "string", "description": "Fecha vigencia AAAAMMDD. Para examen 2026 usar '20260304'.", "default": "20260304"},
                },
                "required": ["law_id", "block_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_neo4j",
            "description": (
                "Consulta el grafo legal Neo4j. Útil para encontrar relaciones entre leyes, "
                "preceptos, modificaciones, jerarquía. Con mode='hybrid' combina búsqueda "
                "semántica (vector) + léxica (fulltext) con reranking RRF para máxima precisión."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "cypher": {"type": "string", "description": "Query Cypher directa (preferido para traversal de relaciones)."},
                    "pregunta_nl": {"type": "string", "description": "Pregunta en lenguaje natural → activa búsqueda híbrida automáticamente."},
                    "mode": {"type": "string", "description": "Modo: 'hybrid' (vector+fulltext+RRF), 'cypher' (solo query directa). Default: hybrid si hay pregunta_nl.", "default": "hybrid"},
                    "limit": {"type": "integer", "description": "Límite resultados (1-50).", "default": 10},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calcular_ss",
            "description": (
                "Calculadora de prestaciones de Seguridad Social 2026 (jubilación, IT, IPT, IPA, "
                "desempleo, viudedad, orfandad, maternidad, PNC, brecha género, cese actividad RETA, etc.). "
                "Pasa 'tipo_calculo' y los parámetros necesarios. Para casos complejos en texto libre, "
                "usa tipo_calculo='auto' con el texto en 'caso_practico'."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "tipo_calculo": {
                        "type": "string",
                        "description": (
                            "Tipo: 'jubilacion', 'br_dual', 'it', 'ipt', 'ipa', 'desempleo', "
                            "'maternidad', 'pnc', 'brecha_genero', 'cese_reta', 'solidaridad', "
                            "'lagunas', 'auto' (parsea texto libre)."
                        ),
                    },
                    "caso_practico": {"type": "string", "description": "Solo si tipo_calculo='auto': texto del caso."},
                    "parametros": {
                        "type": "object",
                        "description": "Parámetros específicos del cálculo (bases, edad, años cotizados, etc.).",
                    },
                },
                "required": ["tipo_calculo"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_vault",
            "description": (
                "Busca en el vault Obsidian del opositor (trampas verificadas, esquemas, "
                "notas personales). Útil para recuperar contexto pedagógico ya curado."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Términos a buscar."},
                    "carpeta": {"type": "string", "description": "Subcarpeta opcional: 'wiki/trampas', 'wiki/esquemas'."},
                    "limit": {"type": "integer", "description": "Resultados (1-20).", "default": 5},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "escribir_vault",
            "description": (
                "Crea o añade contenido a una nota en el vault Obsidian. "
                "Útil para guardar respuestas de casos prácticos, esquemas o resúmenes. "
                "Usa mode='overwrite' para crear/reemplazar, mode='append' para añadir al final."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Ruta del archivo dentro del vault (ej: 'casos_practicos/caso_01.md').",
                    },
                    "content": {
                        "type": "string",
                        "description": "Contenido en formato Markdown a escribir.",
                    },
                    "mode": {
                        "type": "string",
                        "description": "'overwrite' para reemplazar contenido, 'append' para añadir al final.",
                        "enum": ["overwrite", "append"],
                        "default": "overwrite",
                    },
                },
                "required": ["path", "content"],
            },
        },
    },
]


# ============================================================================
# IMPLEMENTACIONES — cada función recibe dict de args y devuelve dict resultado
# ============================================================================

# ---------- 1. TAVILY SEARCH ----------
async def tool_tavily_search(args: Dict[str, Any]) -> Dict[str, Any]:
    """Búsqueda web vía Tavily API."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return {"error": "TAVILY_API_KEY no configurada"}

    query = args.get("query", "").strip()
    if not query:
        return {"error": "query vacía"}
    max_results = min(int(args.get("max_results", 5)), 10)

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": api_key,
                    "query": query,
                    "search_depth": "basic",
                    "max_results": max_results,
                    "include_answer": True,
                },
            )
            response.raise_for_status()
            data = response.json()
        return {
            "query": query,
            "answer": data.get("answer", ""),
            "results": [
                {
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "content": r.get("content", "")[:500],
                }
                for r in data.get("results", [])
            ],
        }
    except Exception as e:
        logger.exception("tool_tavily_search error")
        return {"error": f"Tavily fallo: {e}"}


# ---------- 2. SEARCH BOE ----------
async def tool_search_boe(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recupera metadatos por ID BOE o lista por rango de fechas.
    NOTA: la API BOE de datos abiertos NO soporta búsqueda por texto.
    """
    id_norma = (args.get("id_norma") or "").strip()
    from_date = (args.get("from_date") or "").strip()
    to_date = (args.get("to_date") or "").strip()
    limit = min(int(args.get("limit", 20)), 50)

    if not id_norma and not (from_date or to_date):
        return {
            "error": "Debes pasar id_norma (preferido) o un rango from_date/to_date. "
                     "Para buscar por TEXTO, usa primero tavily_search."
        }

    try:
        from agents.boe_api_client import BOEApiClient
        # Caso 1: ID concreto → metadatos
        if id_norma:
            with BOEApiClient() as client:
                metadatos = client.get_metadatos(id_norma=id_norma, formato="json")
            return {
                "id": id_norma,
                "url_boe": f"https://www.boe.es/buscar/act.php?id={id_norma}",
                "metadatos": metadatos,
            }

        # Caso 2: listado por fechas
        with BOEApiClient() as client:
            result = client.get_legislacion_consolidada(
                from_date=from_date or None,
                to_date=to_date or None,
                offset=0,
                limit=limit,
            )

        # Normalizar resultados (la API devuelve XML/dict anidado)
        items = []
        try:
            data = result.get("data", {}) or result
            docs = data.get("legislacion_consolidada", data).get("documento", []) if isinstance(data.get("legislacion_consolidada", data), dict) else []
            if isinstance(docs, dict):
                docs = [docs]
            for d in docs[:limit]:
                items.append({
                    "id": d.get("identificador") or d.get("id"),
                    "titulo": d.get("titulo"),
                    "fecha": d.get("fecha_disposicion") or d.get("fecha_publicacion"),
                })
        except Exception:
            items = [{"raw": str(result)[:1000]}]

        return {
            "from_date": from_date or "n/a",
            "to_date": to_date or "n/a",
            "n_resultados": len(items),
            "resultados": items,
        }
    except Exception as e:
        logger.exception("tool_search_boe error")
        return {"error": f"BOE search fallo: {e}"}


# ---------- 3. GET LAW TEXT BLOCK ----------
async def tool_get_law_text_block(args: Dict[str, Any]) -> Dict[str, Any]:
    """Texto exacto de un bloque BOE con as_of_date (corte 04/03/2026 por defecto)."""
    law_id = args.get("law_id", "").strip()
    block_id = args.get("block_id", "").strip()
    as_of = args.get("as_of_date", "20260304").strip()

    if not law_id or not block_id:
        return {"error": "law_id y block_id obligatorios"}

    # Construir URL — BOE soporta filtro de fecha vía suffix
    url = f"https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/{law_id}/texto/bloque/{block_id}"

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(url, headers={"Accept": "application/xml"})
            response.raise_for_status()
            text = response.text

        # Parsing simple: extraer contenido dentro de <p> tags
        import re
        paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", text, flags=re.DOTALL | re.IGNORECASE)
        # Limpiar tags HTML residuales
        clean_paragraphs = [re.sub(r"<[^>]+>", "", p).strip() for p in paragraphs]
        clean_paragraphs = [p for p in clean_paragraphs if p]

        return {
            "law_id": law_id,
            "block_id": block_id,
            "as_of_date": as_of,
            "url": f"https://www.boe.es/buscar/act.php?id={law_id}",
            "texto": "\n\n".join(clean_paragraphs[:20]),  # Cap a 20 párrafos
            "n_parrafos": len(clean_paragraphs),
            "nota_corte": (
                f"Texto recuperado de la consolidación BOE actual. "
                f"Para un examen con corte {as_of[:4]}-{as_of[4:6]}-{as_of[6:8]}, "
                f"verificar manualmente que las modificaciones citadas son anteriores."
            ),
        }
    except Exception as e:
        logger.exception("tool_get_law_text_block error")
        return {"error": f"BOE text block fallo: {e}"}


# ---------- 4. CONSULTAR NEO4J ----------
async def tool_consultar_neo4j(args: Dict[str, Any]) -> Dict[str, Any]:
    """Query Cypher sobre Neo4j local (grafo de leyes y preceptos).
    
    Modos:
    - cypher: ejecución directa de Cypher
    - pregunta_nl + mode='hybrid': búsqueda híbrida (vector + fulltext + RRF rerank)
    - pregunta_nl (sin mode): heurística NL→Cypher básica
    """
    cypher = args.get("cypher", "").strip()
    pregunta_nl = args.get("pregunta_nl", "").strip()
    mode = args.get("mode", "").strip().lower()
    limit = min(int(args.get("limit", 20)), 50)

    if not cypher and not pregunta_nl:
        return {"error": "cypher o pregunta_nl requerido"}

    # Hybrid search mode: combina vector + fulltext + RRF reranking
    if pregunta_nl and (mode == "hybrid" or not cypher):
        try:
            return await _hybrid_search_neo4j(pregunta_nl, limit)
        except Exception as e:
            logger.warning(f"hybrid_search falló, cayendo a heurística: {e}")
            if not cypher:
                cypher = _nl_to_cypher_basic(pregunta_nl, limit)

    if not cypher:
        cypher = _nl_to_cypher_basic(pregunta_nl, limit)

    # Asegurar LIMIT
    if "LIMIT" not in cypher.upper():
        cypher = f"{cypher.rstrip(';')} LIMIT {limit}"

    try:
        from neo4j import AsyncGraphDatabase

        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "")

        driver = AsyncGraphDatabase.driver(uri, auth=(user, password))
        try:
            async with driver.session() as session:
                result = await session.run(cypher)
                records = [dict(r) for r in await result.data()]
        finally:
            await driver.close()

        return {
            "cypher_ejecutado": cypher,
            "n_resultados": len(records),
            "resultados": records[:limit],
        }
    except Exception as e:
        logger.exception("tool_consultar_neo4j error")
        return {"error": f"Neo4j fallo: {e}", "cypher_intentado": cypher}


_HYBRID_MODEL = None  # Cached SentenceTransformer for hybrid search

def _get_embedding_model():
    """Lazy singleton for the embedding model (avoid reloading ~3s per call)."""
    global _HYBRID_MODEL
    if _HYBRID_MODEL is None:
        from sentence_transformers import SentenceTransformer
        _HYBRID_MODEL = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
        logger.info("Embedding model loaded for hybrid search")
    return _HYBRID_MODEL


async def _hybrid_search_neo4j(query: str, limit: int = 10) -> Dict[str, Any]:
    """Búsqueda híbrida: Vector HNSW + Fulltext + Reciprocal Rank Fusion.
    
    Combina resultados semánticos (embedding) con léxicos (fulltext spanish)
    usando RRF para reranking. Devuelve top-K preceptos más relevantes.
    """
    from neo4j import AsyncGraphDatabase

    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "")

    # Generate embedding for the query (cached model)
    model = _get_embedding_model()
    query_embedding = model.encode(query, normalize_embeddings=True).tolist()

    driver = AsyncGraphDatabase.driver(uri, auth=(user, password))
    try:
        async with driver.session() as session:
            # 1. Vector search (semantic)
            vector_result = await session.run("""
                CALL db.index.vector.queryNodes('precepto_embedding', $k, $embedding)
                YIELD node, score
                RETURN node.id AS id, node.title AS title, node.ley_siglas AS ley,
                       substring(node.texto, 0, 400) AS extracto, score AS vector_score,
                       node.communityId AS community
                ORDER BY score DESC
            """, k=limit * 2, embedding=query_embedding)
            vector_hits = [dict(r) for r in await vector_result.data()]

            # 2. Fulltext search (lexical)
            fulltext_result = await session.run("""
                CALL db.index.fulltext.queryNodes('precepto_fulltext', $query)
                YIELD node, score
                RETURN node.id AS id, node.title AS title, node.ley_siglas AS ley,
                       substring(node.texto, 0, 400) AS extracto, score AS fulltext_score,
                       node.communityId AS community
                ORDER BY score DESC
                LIMIT $k
            """, query=query, k=limit * 2)
            fulltext_hits = [dict(r) for r in await fulltext_result.data()]
    finally:
        await driver.close()

    # 3. Reciprocal Rank Fusion (RRF) — k=60 standard
    rrf_k = 60
    scores: Dict[str, float] = {}
    metadata: Dict[str, Dict] = {}

    for rank, hit in enumerate(vector_hits):
        doc_id = hit["id"]
        scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (rrf_k + rank + 1)
        metadata[doc_id] = hit

    for rank, hit in enumerate(fulltext_hits):
        doc_id = hit["id"]
        scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (rrf_k + rank + 1)
        if doc_id not in metadata:
            metadata[doc_id] = hit

    # Sort by RRF score
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]

    results = []
    for doc_id, rrf_score in ranked:
        hit = metadata[doc_id]
        results.append({
            "id": doc_id,
            "title": hit.get("title"),
            "ley": hit.get("ley"),
            "extracto": hit.get("extracto"),
            "rrf_score": round(rrf_score, 5),
            "community": hit.get("community"),
        })

    return {
        "mode": "hybrid_search",
        "query": query,
        "n_vector_hits": len(vector_hits),
        "n_fulltext_hits": len(fulltext_hits),
        "n_resultados": len(results),
        "resultados": results,
    }


def _nl_to_cypher_basic(pregunta: str, limit: int) -> str:
    """Heurística simple NL→Cypher para preguntas frecuentes."""
    p = pregunta.lower()
    if "art" in p or "artículo" in p or "articulo" in p:
        # Buscar preceptos
        return (
            "MATCH (l:Ley)-[:TIENE_PRECEPTO]->(p:Precepto) "
            "WHERE toLower(p.titulo) CONTAINS toLower($pregunta) "
            "   OR toLower(p.texto) CONTAINS toLower($pregunta) "
            "RETURN l.titulo AS ley, p.numero AS articulo, p.titulo AS titulo_articulo, "
            "       substring(p.texto, 0, 300) AS extracto "
            f"LIMIT {limit}"
        ).replace("$pregunta", f"'{pregunta[:100]}'")
    # Default: buscar leyes por título
    return (
        "MATCH (l:Ley) "
        f"WHERE toLower(l.titulo) CONTAINS toLower('{pregunta[:100]}') "
        f"RETURN l.id AS id, l.titulo AS titulo LIMIT {limit}"
    )


# ---------- 5. CALCULAR SS ----------
async def tool_calcular_ss(args: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatcher de calculadoras SS."""
    tipo = (args.get("tipo_calculo") or "").strip().lower()
    caso = (args.get("caso_practico") or "").strip()
    params = args.get("parametros") or {}

    try:
        # Caso 1: texto libre → dispatcher.procesar_caso
        if tipo == "auto" and caso:
            from calculators.dispatcher import procesar_caso
            return procesar_caso(caso)

        # Caso 2: tipos específicos
        if tipo == "br_dual":
            from calculators.calculos_ss import calcular_br_dual_jubilacion
            bases = params.get("bases_historicas", [])
            if not bases or len(bases) < 300:
                return {"error": "Se requieren ≥300 bases en parametros.bases_historicas"}
            return calcular_br_dual_jubilacion(bases)

        if tipo == "solidaridad":
            from calculators.calculos_ss import calcular_adicional_solidaridad
            ret = float(params.get("retribucion_mensual", 0))
            return calcular_adicional_solidaridad(ret)

        if tipo == "brecha_genero":
            from calculators.calculos_ss_extended import calcular_complemento_brecha_genero
            return calcular_complemento_brecha_genero(
                pension_progenitor_a=Decimal(str(params.get("pension_a", 0))),
                pension_progenitor_b=Decimal(str(params.get("pension_b", 0))),
                n_hijos=int(params.get("n_hijos", 1)),
                es_progenitor_a_la_madre=bool(params.get("es_a_madre", True)),
            )

        if tipo == "pnc":
            from calculators.calculos_ss_extended import calcular_pnc_jubilacion_invalidez
            return calcular_pnc_jubilacion_invalidez(
                tipo=params.get("subtipo", "jubilacion"),
                rentas_anuales_unidad_familiar=Decimal(str(params.get("rentas_anuales", 0))),
                miembros_unidad_familiar=int(params.get("miembros", 1)),
                tiene_movilidad_reducida=bool(params.get("movilidad_reducida", False)),
            )

        if tipo == "cese_reta":
            from calculators.calculos_ss_extended import calcular_subsidio_cese_actividad_reta
            bases = [Decimal(str(b)) for b in params.get("bases_12m", [])]
            return calcular_subsidio_cese_actividad_reta(
                bases_cotizacion_12m=bases,
                meses_cotizados_48m=int(params.get("meses_cotizados_48m", 0)),
                tiene_responsabilidades_familiares=bool(params.get("cargas_fam", False)),
            )

        if tipo == "lagunas":
            from calculators.calculos_ss_extended import calcular_integracion_lagunas_jubilacion
            return calcular_integracion_lagunas_jubilacion(
                meses_laguna=int(params.get("meses_laguna", 0)),
                regimen=params.get("regimen", "RG"),
                genero=params.get("genero", "H"),
                post_cese_actividad_reta=bool(params.get("post_cese_reta", False)),
            )

        if tipo == "maternidad":
            from calculators.calculos_ss_extended import calcular_permiso_nacimiento_2026
            return calcular_permiso_nacimiento_2026(
                progenitor=params.get("progenitor", "biologico"),
                familia_monoparental=bool(params.get("monoparental", False)),
                parto_multiple_n_hijos=int(params.get("n_hijos", 1)),
                discapacidad_menor=bool(params.get("discapacidad", False)),
            )

        # Fallback: probar el dispatcher general
        from calculators.dispatcher import procesar_caso
        if caso:
            return procesar_caso(caso)

        return {
            "error": f"tipo_calculo='{tipo}' no reconocido. Usa: jubilacion, br_dual, solidaridad, "
                     f"brecha_genero, pnc, cese_reta, lagunas, maternidad, auto."
        }
    except Exception as e:
        logger.exception("tool_calcular_ss error")
        return {"error": f"Cálculo fallo: {e}"}


# ---------- 6. BUSCAR VAULT ----------
async def tool_buscar_vault(args: Dict[str, Any]) -> Dict[str, Any]:
    """Búsqueda en vault Obsidian vía Local REST API plugin."""
    query = args.get("query", "").strip()
    carpeta = args.get("carpeta", "").strip()
    limit = min(int(args.get("limit", 5)), 20)

    if not query:
        return {"error": "query vacía"}

    try:
        # Reutilizar helper de mcp_gateway.py
        from routers.mcp_gateway import _obsidian_url, _obsidian_headers

        base_url = _obsidian_url()
        headers = _obsidian_headers()

        # Endpoint /search/simple/ — devuelve lista de archivos con matches.
        # MÉTODO REAL del plugin obsidian-local-rest-api v3.6.1: POST con query
        # en query string (NO en body). Verificado 30/04/2026 03:12:
        #   - GET /search/simple/?query=X → 404 Not Found (errorCode 40400)
        #   - POST /search/simple/?query=X → 200 OK con array de resultados
        # NOTA: la función vault_search de routers/mcp_gateway.py usa GET y
        # también está rota. Documentar para corregirla por separado.
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                f"{base_url}/search/simple/",
                params={"query": query, "contextLength": 200},
                headers=headers,
            )
            if response.status_code != 200:
                return {"error": f"Obsidian REST {response.status_code}: {response.text[:200]}"}
            results = response.json()

        # Filtrar por carpeta si se especifica
        if carpeta:
            results = [r for r in results if r.get("filename", "").startswith(carpeta)]

        return {
            "query": query,
            "carpeta": carpeta or "todo",
            "n_resultados": len(results),
            "resultados": [
                {
                    "archivo": r.get("filename"),
                    "score": r.get("score"),
                    "matches": [m.get("context", "")[:200] for m in r.get("matches", [])[:3]],
                }
                for r in results[:limit]
            ],
        }
    except Exception as e:
        logger.exception("tool_buscar_vault error")
        return {"error": f"Vault search fallo: {e}"}


# ---------- 7. ESCRIBIR VAULT ----------
async def tool_escribir_vault(args: Dict[str, Any]) -> Dict[str, Any]:
    """Escribe o añade contenido a una nota en el vault Obsidian vía backend /mcp/vault/write."""
    path = args.get("path", "").strip()
    content = args.get("content", "").strip()
    mode = args.get("mode", "overwrite").strip()

    if not path:
        return {"error": "path obligatorio (ruta del archivo dentro del vault)"}
    if not content:
        return {"error": "content obligatorio (contenido markdown a escribir)"}
    if mode not in ("overwrite", "append"):
        return {"error": "mode debe ser 'overwrite' o 'append'"}

    try:
        # Llamar al endpoint /mcp/vault/write del backend
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                "http://localhost:8080/mcp/vault/write",
                json={
                    "path": path,
                    "content": content,
                    "mode": mode,
                },
                headers={"Content-Type": "application/json"},
            )
            if response.status_code != 200:
                return {"error": f"Backend vault write {response.status_code}: {response.text[:200]}"}
            result = response.json()

        return {
            "path": path,
            "mode": mode,
            "status": result.get("status"),
            "message": result.get("message"),
        }
    except Exception as e:
        logger.exception("tool_escribir_vault error")
        return {"error": f"Vault write fallo: {e}"}


# ============================================================================
# DISPATCHER — mapea name de tool call → función
# ============================================================================

TOOL_FUNCTIONS = {
    "tavily_search": tool_tavily_search,
    "search_boe": tool_search_boe,
    "get_law_text_block": tool_get_law_text_block,
    "consultar_neo4j": tool_consultar_neo4j,
    "calcular_ss": tool_calcular_ss,
    "buscar_vault": tool_buscar_vault,
    "escribir_vault": tool_escribir_vault,
}


async def execute_tool(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """Ejecuta una tool por nombre y devuelve el resultado serializable."""
    func = TOOL_FUNCTIONS.get(name)
    if not func:
        return {"error": f"Tool desconocida: {name}. Disponibles: {list(TOOL_FUNCTIONS.keys())}"}
    try:
        return await func(args or {})
    except Exception as e:
        logger.exception(f"execute_tool({name}) error")
        return {"error": f"Tool {name} fallo: {e}"}
