import os
import yaml
import json
import logging
import asyncio
import httpx
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Configurar logging básico para el motor
logger = logging.getLogger(__name__)

# 1. ENTORNO: Cargar variables ANTES de importar otros módulos internos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE_DIR, ".env"))
load_dotenv(os.path.join(BASE_DIR, "backend", ".env.backend"), override=True)

from json_repair import repair_json
from agents.llm_providers import PROVIDERS
from agents.rag_helper import get_rag_helper
from calculators.dispatcher import CasosPracticosDispatcher

class AgentEngine:
    """
    Motor que traduce definiciones YAML de agentes en ejecuciones reales.
    Soporta estructuras anidadas y resolución de variables globales.
    """
    
    def __init__(self, agents_path: str = "opos-agents/agents"):
        # 1. Ajustar paths absolutos
        self.base_dir = BASE_DIR
        self.agents_dir = os.path.join(self.base_dir, agents_path)
        self.agents_cache: Dict[str, Dict[str, Any]] = {}
        
        # 2. Cargar configuración global (si existe)
        self.global_config = self._load_global_config()

    def _load_global_config(self) -> Dict[str, Any]:
        """Carga opos-agents/config.yaml"""
        config_path = os.path.join(self.base_dir, "opos-agents", "config.yaml")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f).get("config", {})
        return {}

    def _load_agent_manifest(self, agent_id: str) -> Dict[str, Any]:
        """Carga el archivo YAML del agente y normaliza su estructura"""
        if agent_id in self.agents_cache:
            return self.agents_cache[agent_id]
        
        file_path = os.path.join(self.agents_dir, f"{agent_id}.yaml")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Agente {agent_id} no encontrado en {file_path}")
            
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            
            # Normalizar: Si tiene la llave 'agent', colapsarla o apuntar a ella
            if "agent" in data:
                manifest = data["agent"]
                # Preservar el nombre si está en metadata
                if "metadata" in manifest and "name" in manifest["metadata"]:
                    manifest["name"] = manifest["metadata"]["name"]
            else:
                manifest = data
                
            self.agents_cache[agent_id] = manifest
            return manifest

    def _resolve_variables(self, text: str, context: Dict[str, Any]) -> str:
        """
        Resuelve variables en formato {variable} o {config.key} o {{query}}.
        """
        if not text or not isinstance(text, str):
            return text
            
        # Reemplazar {{query}} etc por variables de input
        for key, value in context.get("inputs", {}).items():
            text = text.replace(f"{{{{{key}}}}}", str(value))
            text = text.replace(f"{{{key}}}", str(value))
            
        # Reemplazar {config.xxx} por variables globales
        for key, value in self.global_config.items():
            if isinstance(value, str):
                text = text.replace(f"{{config.{key}}}", value)
            elif isinstance(value, dict):
                # Caso recursivo simple para modelos (ej. config.models.local_finetuned)
                for subkey, subval in value.items():
                    if isinstance(subval, str):
                        text = text.replace(f"{{config.{key}.{subkey}}}", subval)
                    elif isinstance(subval, dict) and "name" in subval:
                        text = text.replace(f"{{config.{key}.{subkey}}}", subval["name"])
        
        return text

    async def execute(self, agent_id: str, inputs: Dict[str, Any], model_override: Optional[str] = None) -> Dict[str, Any]:
        """
        Ejecuta un agente cargando su manifest y llamando al proveedor de LLM.
        """
        manifest = self._load_agent_manifest(agent_id)
        context = {"inputs": inputs, "config": self.global_config}
        
        # 1. Configurar Modelo y Proveedor
        if model_override:
            model_name = model_override
        else:
            # Resolver el modelo si es una variable {config...}
            model_ref = manifest.get("model", "mistral-small")
            model_name = self._resolve_variables(model_ref, context)
            
        provider = PROVIDERS.get(model_name, PROVIDERS.get("mistral-small"))
        print(f"DEBUG: AgentEngine executing with model: {model_name} (Provider: {type(provider).__name__})")
            
        # 2. Preparar Prompts
        system_template = manifest.get("system_prompt", "Eres un asistente útil.")
        system_prompt = self._resolve_variables(system_template, context)
        
        user_template = manifest.get("user_prompt", "{{query}}")
        user_content = self._resolve_variables(user_template, context)
        
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        # Añadir la petición real del usuario
        messages.append({"role": "user", "content": user_content})

        # 3. Herramientas
        tools = self._get_tools_schema(manifest)

        # 4. Auditoría y Control (Ejecución)
        max_iterations = 40
        current_iteration = 0
        last_calc_results = []
        processed = {}
        
        try:
            while current_iteration < max_iterations:
                current_iteration += 1
                
                if tools:
                    # Generar con herramientas (Function Calling)
                    raw_response = await provider.generate_with_tools(
                        messages=messages,
                        tools=tools,
                        temperature=manifest.get("temperature", 0.7),
                        max_tokens=manifest.get("max_tokens", 4000),
                        response_format=manifest.get("response_format")
                    )
                    
                    logger.debug(f"Iteración {current_iteration} para agente {agent_id}")

                    # Procesar respuesta
                    processed = await self._process_tool_response(raw_response, provider, context)
                    
                    print(f"👉 [DEBUG-R1] Iteration {current_iteration} Tool Calls:", processed.get("tool_calls"))
                    print(f"👉 [DEBUG-R1] Iteration {current_iteration} Tool Results:", [r.get("output") for r in processed.get("tool_results", [])][:2])
                    
                    # Capturar resultados de cálculos para validación post-generación
                    if processed.get("tool_results"):
                        for res in processed["tool_results"]:
                            last_calc_results.append(res["output"])

                    if processed.get("needs_second_pass"):
                        # Añadir respuesta del asistente (con tool_calls) al historial
                        tool_calls = processed.get("tool_calls")
                        assistant_msg = {
                            "role": "assistant",
                            "content": processed.get("content") or "",
                            "tool_calls": tool_calls
                        }
                        
                        # REQUISITO DEEPSEEK R1: incluir reasoning_content/thought si existe
                        # Esto es VITAL para que el modelo no entre en bucle infinito
                        thought = processed.get("reasoning_content") or processed.get("thought")
                        if thought:
                            # Algunos proveedores u APIs prefieren el campo específico
                            assistant_msg["reasoning_content"] = thought
                            
                        messages.append(assistant_msg)
                        
                        # Añadir resultados de herramientas
                        for res in processed.get("tool_results", []):
                            messages.append({
                                "role": "tool",
                                "tool_call_id": res["tool_call_id"],
                                "content": str(res["output"])
                            })
                        
                        continue
                    else:
                        break # Salir si no hay más herramientas
                else:
                    # Generar normal (Streaming) si no hay herramientas
                    full_text = ""
                    async for chunk in provider.generate_stream(messages):
                        full_text += chunk
                    processed = {"content": full_text}
                    break

            if current_iteration >= max_iterations:
                logger.warning(f"Agente {agent_id} alcanzó el máximo de iteraciones ({max_iterations})")
                # Pasada forzada sin herramientas para obtener conclusiones
                print(f"👉 [DEBUG-R1] Límite alcanzado, forzando pasada final imperativa.")
                try:
                    # Añadir mensaje de sistema imperativo para la pasada final
                    messages.append({
                        "role": "system",
                        "content": "SISTEMA: Se ha alcanzado el límite de herramientas. IGNORA cualquier necesidad de más cálculos o búsquedas. REDACTA EL RESULTADO FINAL COMPLETO AHORA MISMO basándote únicamente en los datos ya obtenidos."
                    })
                    
                    final_pass = await provider.generate_with_tools(
                        messages=messages,
                        tools=None,  # Forzar sin tools
                        temperature=manifest.get("temperature", 0.7)
                    )
                    final_choices = final_pass.get("choices", [])
                    if final_choices:
                        # Extraer contenido de forma segura
                        msg_data = final_choices[0].get("message", {})
                        processed["content"] = msg_data.get("content") or ""
                        # Si R1 puso el contenido en reasoning_content por error (pasa a veces), lo capturamos
                        if not processed["content"] and msg_data.get("reasoning_content"):
                            processed["content"] = f"> [RAZONAMIENTO FINAL]\n{msg_data['reasoning_content']}"
                except Exception as e:
                    logger.error(f"Error en pasada final: {e}")
                
            # --- CAPA DE VALIDACIÓN POST-GENERACIÓN (Auditoría Claude) ---
            final_content = processed.get("content", "") or ""
            if last_calc_results and final_content:
                self._validate_numerical_consistency(final_content, last_calc_results)

            return {
                "content": final_content,
                "agent": agent_id,
                "model": model_name,
                "iterations": current_iteration
            }
            
        except Exception as e:
            logger.error(f"Error ejecutando agente {agent_id}: {e}")
            return {"error": str(e), "agent": agent_id}

    def _get_tools_schema(self, manifest: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Mapea las herramientas declaradas en el YAML a esquemas reales"""
        tools = []
        declared_tools = manifest.get("tools", [])
        
        for t in declared_tools:
            name = t if isinstance(t, str) else t.get("name")
            
            if name in ["calculator", "ejecutar_calculo"]:
                tools.append({
                    "type": "function",
                    "function": {
                        "name": "ejecutar_calculo",
                        "description": "Calculadora legal: SS (it, jubilación, IMV) y AGE (plazos, silencio).",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "consulta": {"type": "string", "description": "Ej. 'Plazo recurso alzada'"}
                            },
                            "required": ["consulta"]
                        }
                    }
                })
            
            elif name == "search_rag":
                tools.append({
                    "type": "function",
                    "function": {
                        "name": "search_rag",
                        "description": "Busca legislación en el RAG de Seguridad Social y AGE.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Término legal o artículo a buscar"},
                                "limit": {"type": "integer", "description": "Número de resultados", "default": 5},
                                "fecha_referencia": {"type": "string", "description": "Fecha del caso para filtrar vigencia (YYYY-MM-DD)"}
                            },
                            "required": ["query"]
                        }
                    }
                })

            elif name == "verify_boe":
                tools.append({
                    "type": "function",
                    "function": {
                        "name": "verify_boe",
                        "description": "Verifica vigencia de una ley en el BOE oficial.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "ley_id": {"type": "string", "description": "ID del BOE (ej. BOE-A-2015-11724)"},
                                "fecha_examen": {"type": "string", "description": "Fecha de vigencia a verificar (YYYY-MM-DD)"}
                            },
                            "required": ["ley_id"]
                        }
                    }
                })
        return tools

    async def _invoke_mcp_tool(self, name: str, args: Dict[str, Any]) -> str:
        """Simula o invoca una herramienta del servidor MCP local"""
        # En una implementación real, esto llamaría al servidor MCP vía stdio o HTTP
        # Por ahora, simulamos la respuesta basada en la lógica del servidor MCP analizado
        if name == "search_rag":
            # Aquí iría la llamada al wrapper HTTP del MCP
            return f"RESULTADO RAG PARA '{args.get('query')}': [Simulado] Artículos encontrados en Qdrant..."
        elif name == "verify_boe":
            return f"VERIFICACIÓN BOE PARA '{args.get('ley_id')}': [Simulado] La norma se encuentra VIGENTE a fecha {args.get('fecha_examen', 'hoy')}."
        return f"Error: Herramienta {name} no soportada en el proxy."

    async def _process_tool_response(self, response: Dict[str, Any], provider: Any, context: Dict[str, Any] = {}) -> Dict[str, Any]:
        """Procesa la respuesta del LLM cuando invoca herramientas"""
        choices = response.get("choices", [])
        if not choices: return {"content": str(response)}
            
        message = choices[0].get("message", {})
        tool_calls = message.get("tool_calls", [])
        
        if tool_calls:
            results = []
            for call in tool_calls:
                func_name = call["function"]["name"]
                args_str = call["function"]["arguments"]
                try:
                    # Usar json-repair para manejar errores de sintaxis comunes en R1 (comillas faltantes, etc)
                    args = repair_json(args_str, return_objects=True)
                    if not isinstance(args, dict):
                        # Si devuelve una lista o un string tras reparar, intentamos forzarlo
                        args = {"consulta": str(args)}
                except Exception as e:
                    logger.warning(f"Error parseando argumentos de {func_name} tras reparación: {e}")
                    args = {"consulta": args_str}
                
                # Normalización de argumentos comunes
                if "query" not in args and "consulta" in args:
                    args["query"] = args["consulta"]
                elif "consulta" not in args and "query" in args:
                    args["consulta"] = args["query"]
                
                if func_name in ["ejecutar_calculo", "calculator"]:
                    consulta = args.get("consulta", "").lower()
                    # Delegar todo al dispatcher sin hacks de nombres propios
                    calc_res = CasosPracticosDispatcher.ejecutar(consulta)
                    results.append({"tool_call_id": call["id"], "output": calc_res})

                elif func_name == "search_rag":
                    query = args.get("query", "")
                    limit = args.get("limit", 5)
                    
                    # Búsqueda real en Qdrant
                    rag = get_rag_helper()
                    articles = rag.search_articles(query, limit=limit)
                    rag_data = rag.format_articles_for_prompt(articles)
                    
                    results.append({"tool_call_id": call["id"], "output": f"RESULTADOS RAG REAL:\n{rag_data}"})

                elif func_name == "verify_boe":
                    ley_id = args.get("ley_id", "")
                    articulo = args.get("articulo")
                    
                    # Llamada real al MCP Gateway (vía API REST interna)
                    port = os.getenv("PORT", "8000")
                    mcp_url = f"http://localhost:{port}/mcp/verify_boe"
                    
                    try:
                        async with httpx.AsyncClient(timeout=30.0) as client:
                            resp = await client.post(mcp_url, json={"ley_id": ley_id, "articulo": articulo})
                            if resp.status_code == 200:
                                mcp_data = resp.json()
                                results.append({"tool_call_id": call["id"], "output": mcp_data})
                            else:
                                results.append({"tool_call_id": call["id"], "output": f"Error MCP Gateway ({resp.status_code}): {resp.text}"})
                    except Exception as e:
                        logger.error(f"Error llamando al MCP Gateway: {e}")
                        results.append({"tool_call_id": call["id"], "output": f"Error de conexión con MCP Gateway: {str(e)}"})
            
            return {
                "content": message.get("content"),
                "tool_results": results,
                "needs_second_pass": True,
                "tool_calls": tool_calls,
                "reasoning_content": message.get("reasoning_content") or message.get("thought") # Compatibilidad R1
            }
            
        return {"content": message.get("content"), "needs_second_pass": False}

    def _validate_numerical_consistency(self, text: str, calc_results: List[Any]):
        """
        Verifica si los números devueltos por las calculadoras aparecen en el texto final.
        Ayuda a detectar alucinaciones numéricas post-generación.
        """
        import re
        for res in calc_results:
            # Extraer números de los resultados del dispatcher
            # (El dispatcher suele devolver strings o dicts con números)
            num_matches = re.findall(r"\d+(?:[\.,]\d+)?", str(res))
            for num in num_matches:
                # Normalizar número (quitar puntos de miles, cambiar coma por punto)
                clean_num = num.replace(".", "").replace(",", ".")
                if float(clean_num) > 10 and clean_num not in text.replace(",", "."):
                    logger.warning(f"POSIBLE ALUCINACIÓN: El cálculo devolvió {num} pero no se encuentra en el texto final.")
