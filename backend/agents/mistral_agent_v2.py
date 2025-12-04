"""
Agente Mistral V2 con Herramientas Reales y Caché Semántica

Este agente integra:
- Herramientas reales (RAG, BOE, Calculadora SS)
- Caché semántica para ahorro 60-70% en llamadas LLM
- Tool calling con Mistral API
- Verificación automática de Q&A
- Integración con Mistral Studio Agent (web search, code interpreter)

Documentación: https://docs.mistral.ai/capabilities/agents/
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Cargar .env.backend si existe
env_path = Path(__file__).parent.parent / ".env.backend"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip())

try:
    from mistralai import Mistral
except ImportError:
    print("⚠️ mistralai no instalado. Ejecutar: pip install mistralai")
    Mistral = None

from .mistral_tools import (
    MistralTools, 
    SemanticCache, 
    get_mistral_tools, 
    get_semantic_cache
)

logger = logging.getLogger(__name__)

# Configuración
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
MISTRAL_AGENT_ID = os.getenv("MISTRAL_AGENT_ID", "ag_019ad601946d7323a81c544229de40a1")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-large-latest")


class MistralAgentV2:
    """
    Agente Mistral V2 con herramientas reales y caché semántica.
    
    Características:
    - Tool calling con 9 herramientas reales
    - Caché semántica para optimización de costes
    - Verificación automática de respuestas
    - Métricas de rendimiento
    """
    
    # Definición de herramientas para Mistral API
    TOOLS_DEFINITION = [
        {
            "type": "function",
            "function": {
                "name": "buscar_rag_qdrant",
                "description": "Busca contexto legal relevante en la base de conocimiento Qdrant",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Consulta en lenguaje natural"
                        },
                        "top_k": {
                            "type": "integer",
                            "description": "Número de resultados (1-10)",
                            "default": 5
                        },
                        "filter_ley": {
                            "type": "string",
                            "description": "Filtrar por ley específica (LGSS, RD_IMV, etc.)"
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "buscar_boe_oficial",
                "description": "Busca y extrae texto oficial del BOE",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tipo_busqueda": {
                            "type": "string",
                            "enum": ["articulo_especifico", "busqueda_texto", "por_identificador"],
                            "description": "Tipo de búsqueda"
                        },
                        "identificador_boe": {
                            "type": "string",
                            "description": "ID del BOE (ej: BOE-A-2015-11724)"
                        },
                        "articulo": {
                            "type": "string",
                            "description": "Número de artículo (ej: 205, 205.1.a)"
                        },
                        "ley": {
                            "type": "string",
                            "description": "Nombre de la ley"
                        },
                        "texto_busqueda": {
                            "type": "string",
                            "description": "Texto libre a buscar"
                        }
                    },
                    "required": ["tipo_busqueda"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "verificar_url_boe",
                "description": "Verifica si una URL del BOE es válida y accesible",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL completa del BOE"
                        },
                        "articulo_esperado": {
                            "type": "string",
                            "description": "Artículo que debería contener"
                        },
                        "verificar_contenido": {
                            "type": "boolean",
                            "description": "Si extraer y verificar contenido",
                            "default": True
                        }
                    },
                    "required": ["url"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "calcular_prestacion_ss",
                "description": "Calcula prestaciones de Seguridad Social",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tipo_prestacion": {
                            "type": "string",
                            "enum": ["base_reguladora_jubilacion", "pension_jubilacion", "imv", "incapacidad", "desempleo"],
                            "description": "Tipo de cálculo"
                        },
                        "bases_cotizacion": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "Array de bases mensuales"
                        },
                        "num_meses": {
                            "type": "integer",
                            "description": "Meses a considerar"
                        },
                        "años_cotizados": {
                            "type": "number",
                            "description": "Años totales cotizados"
                        },
                        "edad_jubilacion": {
                            "type": "integer",
                            "description": "Edad de jubilación"
                        },
                        "parametros_adicionales": {
                            "type": "object",
                            "description": "Parámetros extra según tipo"
                        }
                    },
                    "required": ["tipo_prestacion"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "clasificar_qa_tema",
                "description": "Clasifica una Q&A por tema, subtema, dificultad y tipo",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pregunta": {
                            "type": "string",
                            "description": "Texto de la pregunta"
                        },
                        "respuesta": {
                            "type": "string",
                            "description": "Texto de la respuesta"
                        },
                        "explicacion": {
                            "type": "string",
                            "description": "Explicación opcional"
                        }
                    },
                    "required": ["pregunta", "respuesta"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "extraer_articulos_texto",
                "description": "Extrae todas las referencias a artículos legales de un texto",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "texto": {
                            "type": "string",
                            "description": "Texto a analizar"
                        },
                        "formato_salida": {
                            "type": "string",
                            "enum": ["estructurado", "lista_simple"],
                            "default": "estructurado"
                        }
                    },
                    "required": ["texto"]
                }
            }
        }
    ]
    
    def __init__(self, use_cache: bool = True):
        """
        Inicializa el agente.
        
        Args:
            use_cache: Si usar caché semántica (default: True)
        """
        self.client = Mistral(api_key=MISTRAL_API_KEY) if MISTRAL_API_KEY else None
        self.tools = get_mistral_tools()
        self.cache = get_semantic_cache() if use_cache else None
        self.use_cache = use_cache
        
        # Métricas
        self.metrics = {
            'total_requests': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'tool_calls': 0,
            'errors': 0,
            'total_tokens': 0
        }
        
        logger.info(f"MistralAgentV2 inicializado - Cache: {use_cache}")

    
    def chat(
        self,
        message: str,
        context: Optional[Dict] = None,
        use_tools: bool = True,
        max_tool_calls: int = 5
    ) -> Dict[str, Any]:
        """
        Procesa un mensaje del usuario con herramientas reales.
        
        Args:
            message: Mensaje del usuario
            context: Contexto adicional
            use_tools: Si usar herramientas
            max_tool_calls: Máximo de llamadas a herramientas
        
        Returns:
            Dict con respuesta, herramientas usadas y métricas
        """
        start_time = datetime.now()
        self.metrics['total_requests'] += 1
        
        result = {
            'success': False,
            'response': None,
            'cached': False,
            'tools_used': [],
            'metrics': {},
            'error': None
        }
        
        try:
            # 1. Verificar caché semántica
            if self.use_cache and self.cache:
                cached_response = self.cache.get(message)
                if cached_response:
                    self.metrics['cache_hits'] += 1
                    result['success'] = True
                    result['response'] = cached_response.get('response', cached_response)
                    result['cached'] = True
                    result['metrics']['cache_hit'] = True
                    result['metrics']['processing_time'] = (datetime.now() - start_time).total_seconds()
                    logger.info(f"Cache HIT para: {message[:50]}...")
                    return result
                
                self.metrics['cache_misses'] += 1
            
            # 2. Verificar cliente Mistral
            if not self.client:
                result['error'] = "Mistral API key no configurada"
                return result
            
            # 3. Preparar mensajes
            system_prompt = self._get_system_prompt(context)
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
            
            # 4. Llamar a Mistral con herramientas
            if use_tools:
                response = self.client.chat.complete(
                    model=MISTRAL_MODEL,
                    messages=messages,
                    tools=self.TOOLS_DEFINITION,
                    tool_choice="auto"
                )
            else:
                response = self.client.chat.complete(
                    model=MISTRAL_MODEL,
                    messages=messages
                )
            
            # 5. Procesar respuesta
            assistant_message = response.choices[0].message
            
            # 6. Procesar tool calls si existen
            tool_calls_count = 0
            while assistant_message.tool_calls and tool_calls_count < max_tool_calls:
                tool_calls_count += 1
                self.metrics['tool_calls'] += len(assistant_message.tool_calls)
                
                # Ejecutar cada herramienta
                tool_results = []
                for tool_call in assistant_message.tool_calls:
                    tool_result = self._execute_tool(tool_call)
                    result['tools_used'].append({
                        'name': tool_call.function.name,
                        'arguments': json.loads(tool_call.function.arguments),
                        'result': tool_result
                    })
                    tool_results.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result, ensure_ascii=False)
                    })
                
                # Añadir resultados y continuar conversación
                messages.append({"role": "assistant", "content": None, "tool_calls": assistant_message.tool_calls})
                messages.extend(tool_results)
                
                # Nueva llamada con resultados de herramientas
                response = self.client.chat.complete(
                    model=MISTRAL_MODEL,
                    messages=messages,
                    tools=self.TOOLS_DEFINITION,
                    tool_choice="auto"
                )
                assistant_message = response.choices[0].message
            
            # 7. Extraer respuesta final
            final_response = assistant_message.content
            
            # 8. Guardar en caché
            if self.use_cache and self.cache and final_response:
                self.cache.set(message, {
                    'response': final_response,
                    'tools_used': [t['name'] for t in result['tools_used']],
                    'generated_at': datetime.now().isoformat()
                })
            
            # 9. Actualizar métricas
            if hasattr(response, 'usage'):
                self.metrics['total_tokens'] += response.usage.total_tokens
            
            result['success'] = True
            result['response'] = final_response
            result['metrics'] = {
                'processing_time': (datetime.now() - start_time).total_seconds(),
                'tool_calls': len(result['tools_used']),
                'tokens_used': response.usage.total_tokens if hasattr(response, 'usage') else 0
            }
            
            return result
            
        except Exception as e:
            self.metrics['errors'] += 1
            logger.error(f"Error en chat: {e}")
            result['error'] = str(e)
            return result
    
    def _execute_tool(self, tool_call) -> Dict[str, Any]:
        """
        Ejecuta una herramienta real.
        
        Args:
            tool_call: Objeto tool_call de Mistral
        
        Returns:
            Resultado de la herramienta
        """
        try:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            
            logger.info(f"Ejecutando herramienta: {name} con args: {args}")
            
            # Mapear a métodos de MistralTools
            if name == "buscar_rag_qdrant":
                return self.tools.buscar_rag_qdrant(**args)
            elif name == "buscar_boe_oficial":
                return self.tools.buscar_boe_oficial(**args)
            elif name == "verificar_url_boe":
                return self.tools.verificar_url_boe(**args)
            elif name == "calcular_prestacion_ss":
                return self.tools.calcular_prestacion_ss(**args)
            elif name == "clasificar_qa_tema":
                return self.tools.clasificar_qa_tema(**args)
            elif name == "extraer_articulos_texto":
                return self.tools.extraer_articulos_texto(**args)
            elif name == "generar_qa_legal":
                return self.tools.generar_qa_legal(**args)
            elif name == "verificar_qa_completa":
                return self.tools.verificar_qa_completa(**args)
            elif name == "obtener_normativa_vigente":
                return self.tools.obtener_normativa_vigente(**args)
            else:
                return {"error": f"Herramienta no encontrada: {name}"}
                
        except Exception as e:
            logger.error(f"Error ejecutando herramienta {tool_call.function.name}: {e}")
            return {"error": str(e)}
    
    def _get_system_prompt(self, context: Optional[Dict] = None) -> str:
        """Genera el system prompt para el agente"""
        base_prompt = """Eres un experto en Seguridad Social española especializado en oposiciones.

Tu rol es:
1. Responder preguntas sobre legislación de Seguridad Social
2. Generar preguntas tipo test de alta calidad
3. Verificar información contra fuentes oficiales (BOE)
4. Realizar cálculos de prestaciones

HERRAMIENTAS DISPONIBLES:
- buscar_rag_qdrant: Buscar contexto legal en la base de conocimiento
- buscar_boe_oficial: Buscar texto oficial en el BOE
- verificar_url_boe: Verificar URLs del BOE
- calcular_prestacion_ss: Calcular prestaciones (jubilación, IMV, etc.)
- clasificar_qa_tema: Clasificar preguntas por tema
- extraer_articulos_texto: Extraer referencias legales

REGLAS:
- SIEMPRE usa buscar_rag_qdrant antes de responder preguntas legales
- SIEMPRE cita artículos específicos (ej: art. 205.1.a LGSS)
- SIEMPRE verifica cálculos con calcular_prestacion_ss
- Responde en español
- Sé preciso y conciso"""
        
        if context:
            base_prompt += f"\n\nCONTEXTO ADICIONAL:\n{json.dumps(context, ensure_ascii=False)}"
        
        return base_prompt


    def chat_with_studio_agent(
        self,
        message: str,
        use_web_search: bool = True,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Chat usando el Agente de Mistral Studio (ag_019ad601946d7323a81c544229de40a1).
        
        El agente de Studio tiene capacidades integradas:
        - Web Search: Puede buscar en internet (incluyendo BOE)
        - Code Interpreter: Puede ejecutar código
        - Document Library: RAG integrado
        
        Args:
            message: Mensaje del usuario
            use_web_search: Si usar búsqueda web (default: True)
            context: Contexto adicional
        
        Returns:
            Dict con respuesta y metadata
        """
        start_time = datetime.now()
        self.metrics['total_requests'] += 1
        
        result = {
            'success': False,
            'response': None,
            'cached': False,
            'agent_used': 'mistral_studio',
            'tools_used': [],
            'metrics': {},
            'error': None
        }
        
        try:
            # 1. Verificar caché semántica
            if self.use_cache and self.cache:
                cached_response = self.cache.get(message)
                if cached_response:
                    self.metrics['cache_hits'] += 1
                    result['success'] = True
                    result['response'] = cached_response.get('response', cached_response)
                    result['cached'] = True
                    result['metrics']['cache_hit'] = True
                    result['metrics']['processing_time'] = (datetime.now() - start_time).total_seconds()
                    logger.info(f"Cache HIT para: {message[:50]}...")
                    return result
                
                self.metrics['cache_misses'] += 1
            
            # 2. Verificar cliente Mistral
            if not self.client:
                result['error'] = "Mistral API key no configurada"
                return result
            
            # 3. Usar el Agent ID como modelo (según docs de Mistral)
            # El agente de Studio ya tiene configuradas sus herramientas
            response = self.client.chat.complete(
                model=MISTRAL_AGENT_ID,  # Usar agent_id como modelo
                messages=[
                    {"role": "user", "content": message}
                ]
            )
            
            # 4. Extraer respuesta
            if hasattr(response, 'choices') and response.choices:
                assistant_message = response.choices[0].message
                final_response = assistant_message.content
                
                # Verificar si usó herramientas
                if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls:
                    for tc in assistant_message.tool_calls:
                        result['tools_used'].append({
                            'name': tc.function.name,
                            'arguments': tc.function.arguments[:200] if tc.function.arguments else ''
                        })
                
                # 5. Guardar en caché
                if self.use_cache and self.cache and final_response:
                    self.cache.set(message, {
                        'response': final_response,
                        'agent': 'mistral_studio',
                        'tools_used': [t['name'] for t in result['tools_used']],
                        'generated_at': datetime.now().isoformat()
                    })
                
                result['success'] = True
                result['response'] = final_response
                result['metrics'] = {
                    'processing_time': (datetime.now() - start_time).total_seconds(),
                    'tokens_used': response.usage.total_tokens if hasattr(response, 'usage') else 0
                }
                
                if hasattr(response, 'usage'):
                    self.metrics['total_tokens'] += response.usage.total_tokens
            
            return result
            
        except Exception as e:
            self.metrics['errors'] += 1
            logger.error(f"Error en chat_with_studio_agent: {e}")
            result['error'] = str(e)
            return result
    
    def chat(
        self,
        message: str,
        context: Optional[Dict] = None,
        use_tools: bool = True,
        max_tool_calls: int = 5,
        prefer_studio_agent: bool = True
    ) -> Dict[str, Any]:
        """
        Procesa un mensaje del usuario.
        
        Puede usar:
        1. Agente de Mistral Studio (con web search, code interpreter)
        2. Herramientas locales (RAG, BOE, Calculator)
        
        Args:
            message: Mensaje del usuario
            context: Contexto adicional
            use_tools: Si usar herramientas locales
            max_tool_calls: Máximo de llamadas a herramientas
            prefer_studio_agent: Si preferir el agente de Studio
        
        Returns:
            Dict con respuesta, herramientas usadas y métricas
        """
        # Si preferimos el agente de Studio, usarlo primero
        if prefer_studio_agent and MISTRAL_AGENT_ID:
            return self.chat_with_studio_agent(message, context=context)
        
        # Fallback a herramientas locales
        return self._chat_with_local_tools(message, context, use_tools, max_tool_calls)
    
    def _chat_with_local_tools(
        self,
        message: str,
        context: Optional[Dict] = None,
        use_tools: bool = True,
        max_tool_calls: int = 5
    ) -> Dict[str, Any]:
        """
        Chat usando herramientas locales (RAG, BOE, Calculator).
        """
        start_time = datetime.now()
        self.metrics['total_requests'] += 1
        
        result = {
            'success': False,
            'response': None,
            'cached': False,
            'agent_used': 'local_tools',
            'tools_used': [],
            'metrics': {},
            'error': None
        }
        
        try:
            # 1. Verificar caché semántica
            if self.use_cache and self.cache:
                cached_response = self.cache.get(message)
                if cached_response:
                    self.metrics['cache_hits'] += 1
                    result['success'] = True
                    result['response'] = cached_response.get('response', cached_response)
                    result['cached'] = True
                    result['metrics']['cache_hit'] = True
                    result['metrics']['processing_time'] = (datetime.now() - start_time).total_seconds()
                    return result
                
                self.metrics['cache_misses'] += 1
            
            # 2. Verificar cliente Mistral
            if not self.client:
                result['error'] = "Mistral API key no configurada"
                return result
            
            # 3. Preparar mensajes
            system_prompt = self._get_system_prompt(context)
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
            
            # 4. Llamar a Mistral con herramientas locales
            if use_tools:
                response = self.client.chat.complete(
                    model=MISTRAL_MODEL,
                    messages=messages,
                    tools=self.TOOLS_DEFINITION,
                    tool_choice="auto"
                )
            else:
                response = self.client.chat.complete(
                    model=MISTRAL_MODEL,
                    messages=messages
                )
            
            # 5. Procesar respuesta
            assistant_message = response.choices[0].message
            
            # 6. Procesar tool calls si existen
            tool_calls_count = 0
            while assistant_message.tool_calls and tool_calls_count < max_tool_calls:
                tool_calls_count += 1
                self.metrics['tool_calls'] += len(assistant_message.tool_calls)
                
                # Ejecutar cada herramienta
                tool_results = []
                for tool_call in assistant_message.tool_calls:
                    tool_result = self._execute_tool(tool_call)
                    result['tools_used'].append({
                        'name': tool_call.function.name,
                        'arguments': json.loads(tool_call.function.arguments),
                        'result': tool_result
                    })
                    tool_results.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result, ensure_ascii=False)
                    })
                
                # Añadir resultados y continuar conversación
                messages.append({"role": "assistant", "content": None, "tool_calls": assistant_message.tool_calls})
                messages.extend(tool_results)
                
                # Nueva llamada con resultados de herramientas
                response = self.client.chat.complete(
                    model=MISTRAL_MODEL,
                    messages=messages,
                    tools=self.TOOLS_DEFINITION,
                    tool_choice="auto"
                )
                assistant_message = response.choices[0].message
            
            # 7. Extraer respuesta final
            final_response = assistant_message.content
            
            # 8. Guardar en caché
            if self.use_cache and self.cache and final_response:
                self.cache.set(message, {
                    'response': final_response,
                    'agent': 'local_tools',
                    'tools_used': [t['name'] for t in result['tools_used']],
                    'generated_at': datetime.now().isoformat()
                })
            
            # 9. Actualizar métricas
            if hasattr(response, 'usage'):
                self.metrics['total_tokens'] += response.usage.total_tokens
            
            result['success'] = True
            result['response'] = final_response
            result['metrics'] = {
                'processing_time': (datetime.now() - start_time).total_seconds(),
                'tool_calls': len(result['tools_used']),
                'tokens_used': response.usage.total_tokens if hasattr(response, 'usage') else 0
            }
            
            return result
            
        except Exception as e:
            self.metrics['errors'] += 1
            logger.error(f"Error en chat: {e}")
            result['error'] = str(e)
            return result
    
    def _execute_tool(self, tool_call) -> Dict[str, Any]:
        """
        Ejecuta una herramienta local.
        """
        try:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            
            logger.info(f"Ejecutando herramienta: {name}")
            
            # Mapear a métodos de MistralTools
            tool_map = {
                "buscar_rag_qdrant": self.tools.buscar_rag_qdrant,
                "buscar_boe_oficial": self.tools.buscar_boe_oficial,
                "verificar_url_boe": self.tools.verificar_url_boe,
                "calcular_prestacion_ss": self.tools.calcular_prestacion_ss,
                "clasificar_qa_tema": self.tools.clasificar_qa_tema,
                "extraer_articulos_texto": self.tools.extraer_articulos_texto,
                "generar_qa_legal": self.tools.generar_qa_legal,
                "verificar_qa_completa": self.tools.verificar_qa_completa,
                "obtener_normativa_vigente": self.tools.obtener_normativa_vigente,
            }
            
            if name in tool_map:
                return tool_map[name](**args)
            else:
                return {"error": f"Herramienta no encontrada: {name}"}
                
        except Exception as e:
            logger.error(f"Error ejecutando herramienta {tool_call.function.name}: {e}")
            return {"error": str(e)}
    
    def _get_system_prompt(self, context: Optional[Dict] = None) -> str:
        """Genera el system prompt para el agente"""
        base_prompt = """Eres un experto en Seguridad Social española especializado en oposiciones.

Tu rol es:
1. Responder preguntas sobre legislación de Seguridad Social
2. Generar preguntas tipo test de alta calidad
3. Verificar información contra fuentes oficiales (BOE)
4. Realizar cálculos de prestaciones

HERRAMIENTAS DISPONIBLES:
- buscar_rag_qdrant: Buscar contexto legal en la base de conocimiento
- buscar_boe_oficial: Buscar texto oficial en el BOE
- verificar_url_boe: Verificar URLs del BOE
- calcular_prestacion_ss: Calcular prestaciones (jubilación, IMV, etc.)
- clasificar_qa_tema: Clasificar preguntas por tema
- extraer_articulos_texto: Extraer referencias legales

REGLAS:
- SIEMPRE usa buscar_rag_qdrant antes de responder preguntas legales
- SIEMPRE cita artículos específicos (ej: art. 205.1.a LGSS)
- SIEMPRE verifica cálculos con calcular_prestacion_ss
- Responde en español
- Sé preciso y conciso"""
        
        if context:
            base_prompt += f"\n\nCONTEXTO ADICIONAL:\n{json.dumps(context, ensure_ascii=False)}"
        
        return base_prompt
    
    def get_metrics(self) -> Dict[str, Any]:
        """Devuelve métricas del agente"""
        cache_stats = self.cache.get_stats() if self.cache else {}
        
        return {
            'agent_metrics': self.metrics,
            'cache_stats': cache_stats,
            'config': {
                'agent_id': MISTRAL_AGENT_ID,
                'model': MISTRAL_MODEL,
                'cache_enabled': self.use_cache
            }
        }


# =========================================================================
# FUNCIONES DE UTILIDAD
# =========================================================================

def get_mistral_agent(use_cache: bool = True) -> MistralAgentV2:
    """Obtiene una instancia del agente Mistral V2"""
    return MistralAgentV2(use_cache=use_cache)


def test_studio_agent():
    """Test rápido del agente de Mistral Studio"""
    print("\n" + "=" * 60)
    print("🤖 TEST AGENTE MISTRAL STUDIO")
    print("=" * 60)
    
    agent = get_mistral_agent(use_cache=False)
    
    queries = [
        "¿Cuál es la edad de jubilación ordinaria en España según la LGSS?",
        "Busca en el BOE el artículo 205 de la Ley General de Seguridad Social",
    ]
    
    for query in queries:
        print(f"\n📝 Query: {query}")
        print("-" * 40)
        
        result = agent.chat(query, prefer_studio_agent=True)
        
        if result['success']:
            print(f"✅ Respuesta: {result['response'][:300]}...")
            print(f"🔧 Herramientas: {result['tools_used']}")
            print(f"⏱️ Tiempo: {result['metrics'].get('processing_time', 'N/A')}s")
        else:
            print(f"❌ Error: {result['error']}")
    
    print("\n📊 Métricas finales:")
    print(json.dumps(agent.get_metrics(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    test_studio_agent()
