"""
Agent Factory Router - Factoría de Agentes con MCP
Crea contenido usando MCP + RAG + Estrategia COSM
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Literal
import json
import logging
import asyncio
from datetime import datetime
import subprocess
import os

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agents", tags=["agent-factory"])

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class AgentRequest(BaseModel):
    tipo: Literal["simulacro", "caso_practico", "flashcards", "resumen", "mapa_mental", "esquema"]
    tema: str
    nivel: Optional[str] = "INTERMEDIO"  # BASICO, INTERMEDIO, AVANZADO
    cantidad: Optional[int] = 1
    usuario_id: Optional[int] = None
    personalizar: bool = True
    usar_rag: bool = True
    formato_oficial: bool = True  # Usar formato BOE-A-2024-11403

class SimulacroRequest(BaseModel):
    tema: str
    nivel: str = "INTERMEDIO"
    formato_oficial: bool = True  # 100 test + 12 casos prácticos
    usuario_id: Optional[int] = None

class CasoPracticoRequest(BaseModel):
    tema: str
    complejidad: str = "MEDIA"
    incluir_jurisprudencia: bool = True
    usuario_id: Optional[int] = None

class FlashcardsRequest(BaseModel):
    tema: str
    cantidad: int = 20
    estilo: str = "DEFINICION"  # DEFINICION, PREGUNTA, CALCULO
    usuario_id: Optional[int] = None

class ResumenRequest(BaseModel):
    ley_id: Optional[str] = None
    tema: Optional[str] = None
    longitud: str = "MEDIO"  # CORTO, MEDIO, LARGO
    incluir_ejemplos: bool = True

class MapaMentalRequest(BaseModel):
    tema: str
    profundidad: int = 3  # Niveles de jerarquía
    formato: str = "MERMAID"  # MERMAID, JSON, TEXT

# ============================================================================
# MCP CLIENT WRAPPER (Reutilizado)
# ============================================================================

class MCPClient:
    """Wrapper para llamar al MCP server desde FastAPI"""
    
    def __init__(self):
        self.mcp_path = os.path.join(os.path.dirname(__file__), "../../mcp-server/dist/index.js")
        self.node_path = "node"
    
    async def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """Llamar a una herramienta del MCP server"""
        try:
            cmd = [
                self.node_path,
                self.mcp_path,
                "call-tool",
                tool_name,
                json.dumps(arguments)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                env={
                    **os.environ,
                    "QDRANT_URL": os.getenv("QDRANT_URL"),
                    "QDRANT_API_KEY": os.getenv("QDRANT_API_KEY"),
                    "HUGGINGFACE_TOKEN": os.getenv("HUGGINGFACE_TOKEN"),
                    "MISTRAL_API_KEY": os.getenv("MISTRAL_API_KEY")
                }
            )
            
            if result.returncode != 0:
                logger.error(f"MCP error: {result.stderr}")
                raise Exception(f"MCP call failed: {result.stderr}")
            
            return json.loads(result.stdout)
            
        except Exception as e:
            logger.error(f"MCP call error: {e}")
            raise Exception(f"MCP call failed: {str(e)}")

# Global MCP client
mcp_client = MCPClient()

# ============================================================================
# AGENT FACTORY - GENERADORES ESPECIALIZADOS
# ============================================================================

class AgentFactory:
    """Factoría de agentes especializados usando MCP + RAG"""
    
    def __init__(self):
        self.mcp = mcp_client
    
    async def crear_simulacro_oficial(self, tema: str, nivel: str, usuario_id: Optional[int] = None) -> dict:
        """
        Crea simulacro con formato oficial BOE-A-2024-11403:
        - 100 preguntas test (temas 1-32 generales)
        - 12 casos prácticos (18 temas SS específicos)
        """
        try:
            # 1. Buscar contexto en RAG
            contexto_general = await self.mcp.call_tool("mcp_opositaia_search_rag", {
                "query": f"{tema} temario general oposiciones",
                "limit": 10
            })
            
            contexto_especifico = await self.mcp.call_tool("mcp_opositaia_search_rag", {
                "query": f"{tema} seguridad social casos prácticos",
                "limit": 5
            })
            
            # 2. Generar 100 preguntas test (Parte 1)
            preguntas_test = await self._generar_preguntas_test(
                tema, nivel, contexto_general, cantidad=100
            )
            
            # 3. Generar 12 casos prácticos (Parte 2)
            casos_practicos = await self._generar_casos_practicos(
                tema, contexto_especifico, cantidad=12
            )
            
            # 4. Personalizar por usuario si se proporciona
            if usuario_id:
                preguntas_test = self._personalizar_preguntas(usuario_id, preguntas_test)
                casos_practicos = self._personalizar_casos(usuario_id, casos_practicos)
            
            simulacro = {
                "id": f"sim_{tema}_{nivel}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "tema": tema,
                "nivel": nivel,
                "formato": "BOE-A-2024-11403",
                "estructura": {
                    "parte_1": {
                        "tipo": "test_general",
                        "preguntas": 100,
                        "puntuacion_maxima": 50,
                        "minimo_aprobar": 25,
                        "contenido": preguntas_test
                    },
                    "parte_2": {
                        "tipo": "casos_practicos",
                        "preguntas": 12,
                        "puntuacion_maxima": 50,
                        "minimo_aprobar": 25,
                        "contenido": casos_practicos
                    }
                },
                "instrucciones": {
                    "penalizacion": -0.25,
                    "tiempo_estimado": "3 horas",
                    "requisito": "Mínimo 25 puntos en CADA parte"
                },
                "metadatos": {
                    "creado": datetime.now().isoformat(),
                    "usuario_id": usuario_id,
                    "fuente": "MCP + RAG",
                    "costo_generacion": 0.0  # COSM strategy
                }
            }
            
            return simulacro
            
        except Exception as e:
            logger.error(f"Error creating simulacro: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def crear_caso_practico(self, tema: str, complejidad: str, incluir_jurisprudencia: bool = True) -> dict:
        """Crea caso práctico realista con jurisprudencia"""
        try:
            # 1. Buscar contexto legal
            contexto = await self.mcp.call_tool("mcp_opositaia_search_rag", {
                "query": f"{tema} casos prácticos jurisprudencia",
                "limit": 5
            })
            
            # 2. Buscar jurisprudencia si se solicita
            jurisprudencia = None
            if incluir_jurisprudencia:
                jurisprudencia = await self.mcp.call_tool("mcp_opositaia_search_jurisprudence", {
                    "query": tema,
                    "tribunal": "todos",
                    "limit": 2
                })
            
            # 3. Generar caso usando contexto
            caso = await self._generar_caso_con_contexto(tema, complejidad, contexto, jurisprudencia)
            
            return caso
            
        except Exception as e:
            logger.error(f"Error creating caso: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def crear_flashcards(self, tema: str, cantidad: int, estilo: str) -> List[dict]:
        """Crea flashcards usando RAG"""
        try:
            # 1. Buscar conceptos del tema
            conceptos = await self.mcp.call_tool("mcp_opositaia_search_rag", {
                "query": f"{tema} conceptos definiciones",
                "limit": cantidad * 2  # Más contexto
            })
            
            # 2. Generar flashcards
            flashcards = []
            for i, concepto in enumerate(conceptos.get("results", [])[:cantidad]):
                flashcard = await self._crear_flashcard(concepto, estilo, i+1)
                flashcards.append(flashcard)
            
            return flashcards
            
        except Exception as e:
            logger.error(f"Error creating flashcards: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def crear_resumen_ley(self, ley_id: str = None, tema: str = None, longitud: str = "MEDIO") -> dict:
        """Crea resumen de ley usando MCP"""
        try:
            if ley_id:
                # Usar herramienta específica de resumen
                resumen = await self.mcp.call_tool("mcp_opositaia_get_law_summary", {
                    "ley_name": ley_id
                })
            else:
                # Buscar por tema
                contexto = await self.mcp.call_tool("mcp_opositaia_search_rag", {
                    "query": f"{tema} ley normativa",
                    "limit": 10
                })
                resumen = await self._crear_resumen_desde_contexto(tema, contexto, longitud)
            
            return resumen
            
        except Exception as e:
            logger.error(f"Error creating resumen: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def crear_mapa_mental(self, tema: str, profundidad: int, formato: str) -> dict:
        """Crea mapa mental usando RAG"""
        try:
            # 1. Buscar estructura del tema
            contexto = await self.mcp.call_tool("mcp_opositaia_search_rag", {
                "query": f"{tema} estructura conceptos jerarquía",
                "limit": 15
            })
            
            # 2. Generar mapa mental
            mapa = await self._crear_mapa_mental(tema, contexto, profundidad, formato)
            
            return mapa
            
        except Exception as e:
            logger.error(f"Error creating mapa mental: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    # ========================================================================
    # MÉTODOS PRIVADOS DE GENERACIÓN
    # ========================================================================
    
    async def _generar_preguntas_test(self, tema: str, nivel: str, contexto: dict, cantidad: int) -> List[dict]:
        """Genera preguntas tipo test usando contexto RAG"""
        # Implementar con Mistral/Gemini usando el contexto
        # Por ahora simulamos
        preguntas = []
        for i in range(cantidad):
            pregunta = {
                "id": i + 1,
                "texto": f"¿Cuál es el concepto principal de {tema} en el contexto {i+1}?",
                "opciones": [
                    f"Opción A relacionada con {tema}",
                    f"Opción B relacionada con {tema}",
                    f"Opción C relacionada con {tema}",
                    f"Opción D relacionada con {tema}"
                ],
                "respuesta_correcta": 0,
                "explicacion": f"La respuesta correcta es A porque según el contexto RAG...",
                "referencia": contexto.get("results", [{}])[0].get("source", ""),
                "nivel": nivel
            }
            preguntas.append(pregunta)
        
        return preguntas
    
    async def _generar_casos_practicos(self, tema: str, contexto: dict, cantidad: int) -> List[dict]:
        """Genera casos prácticos usando contexto RAG"""
        casos = []
        for i in range(cantidad):
            caso = {
                "id": i + 1,
                "titulo": f"Caso Práctico {i+1}: {tema}",
                "hechos": f"Situación práctica {i+1} relacionada con {tema}...",
                "pregunta": f"¿Qué procedimiento corresponde aplicar?",
                "opciones": [
                    "Procedimiento A según LGSS",
                    "Procedimiento B según ET", 
                    "Procedimiento C según normativa específica",
                    "No procede ningún procedimiento"
                ],
                "respuesta_correcta": 0,
                "solucion": f"Análisis jurídico del caso {i+1}...",
                "referencias": ["Art. X LGSS", "STS 123/2024"],
                "contexto_rag": contexto.get("results", [{}])[0] if contexto.get("results") else {}
            }
            casos.append(caso)
        
        return casos
    
    def _personalizar_preguntas(self, usuario_id: int, preguntas: List[dict]) -> List[dict]:
        """Personaliza preguntas por usuario (COSM strategy)"""
        import random
        random.seed(hash(usuario_id))
        return random.sample(preguntas, len(preguntas))
    
    def _personalizar_casos(self, usuario_id: int, casos: List[dict]) -> List[dict]:
        """Personaliza casos por usuario cambiando nombres/números"""
        nombres = ["María", "Juan", "Ana", "Carlos", "Elena", "Luis"]
        nombre_idx = hash(usuario_id) % len(nombres)
        
        for caso in casos:
            # Cambiar nombres en los hechos
            caso["hechos"] = caso["hechos"].replace("María", nombres[nombre_idx])
        
        return casos
    
    async def _crear_flashcard(self, concepto: dict, estilo: str, numero: int) -> dict:
        """Crea una flashcard desde concepto RAG"""
        contenido = concepto.get("content", "")
        titulo = concepto.get("title", f"Concepto {numero}")
        
        if estilo == "DEFINICION":
            pregunta = f"¿Qué es {titulo}?"
            respuesta = contenido[:200] + "..."
        elif estilo == "PREGUNTA":
            pregunta = f"¿Cuándo se aplica {titulo}?"
            respuesta = f"Se aplica cuando... (basado en {contenido[:100]})"
        else:  # CALCULO
            pregunta = f"¿Cómo se calcula {titulo}?"
            respuesta = f"Fórmula: ... (según {contenido[:100]})"
        
        return {
            "id": numero,
            "pregunta": pregunta,
            "respuesta": respuesta,
            "explicacion": contenido[:500],
            "fuente": concepto.get("source", ""),
            "tema": concepto.get("metadata", {}).get("tema", ""),
            "dificultad": 3  # 1-5
        }
    
    async def _crear_resumen_desde_contexto(self, tema: str, contexto: dict, longitud: str) -> dict:
        """Crea resumen desde contexto RAG"""
        resultados = contexto.get("results", [])
        
        # Combinar contenido
        contenido_completo = "\n\n".join([r.get("content", "") for r in resultados[:5]])
        
        # Determinar longitud
        max_chars = {"CORTO": 500, "MEDIO": 1500, "LARGO": 3000}[longitud]
        
        resumen = {
            "tema": tema,
            "resumen": contenido_completo[:max_chars] + "...",
            "conceptos_clave": self._extraer_conceptos_clave(contenido_completo),
            "referencias": [r.get("source", "") for r in resultados[:3]],
            "longitud": longitud,
            "fecha_creacion": datetime.now().isoformat()
        }
        
        return resumen
    
    def _extraer_conceptos_clave(self, texto: str) -> Dict[str, str]:
        """Extrae conceptos clave del texto"""
        # Implementación simple - mejorar con NLP
        conceptos = {}
        palabras_clave = ["prestación", "cotización", "jubilación", "incapacidad", "desempleo"]
        
        for palabra in palabras_clave:
            if palabra in texto.lower():
                # Extraer contexto alrededor de la palabra
                idx = texto.lower().find(palabra)
                contexto = texto[max(0, idx-50):idx+100]
                conceptos[palabra] = contexto
        
        return conceptos
    
    async def _crear_mapa_mental(self, tema: str, contexto: dict, profundidad: int, formato: str) -> dict:
        """Crea mapa mental desde contexto RAG"""
        resultados = contexto.get("results", [])
        
        # Estructura básica del mapa
        mapa = {
            "tema_central": tema,
            "nodos": [],
            "formato": formato,
            "profundidad": profundidad
        }
        
        # Crear nodos desde resultados RAG
        for i, resultado in enumerate(resultados[:profundidad]):
            nodo = {
                "id": i + 1,
                "titulo": resultado.get("title", f"Concepto {i+1}"),
                "contenido": resultado.get("content", "")[:200],
                "nivel": 1,
                "hijos": []
            }
            mapa["nodos"].append(nodo)
        
        # Generar formato específico
        if formato == "MERMAID":
            mapa["mermaid"] = self._generar_mermaid(mapa)
        
        return mapa
    
    def _generar_mermaid(self, mapa: dict) -> str:
        """Genera código Mermaid para el mapa mental"""
        mermaid = "graph TD\n"
        mermaid += f"    A[{mapa['tema_central']}]\n"
        
        for nodo in mapa["nodos"]:
            nodo_id = f"B{nodo['id']}"
            mermaid += f"    A --> {nodo_id}[{nodo['titulo']}]\n"
        
        return mermaid

# Global factory
agent_factory = AgentFactory()

# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/crear")
async def crear_contenido(request: AgentRequest):
    """Endpoint universal para crear cualquier tipo de contenido"""
    try:
        if request.tipo == "simulacro":
            resultado = await agent_factory.crear_simulacro_oficial(
                request.tema, 
                request.nivel, 
                request.usuario_id
            )
        elif request.tipo == "caso_practico":
            resultado = await agent_factory.crear_caso_practico(
                request.tema, 
                "MEDIA"
            )
        elif request.tipo == "flashcards":
            resultado = await agent_factory.crear_flashcards(
                request.tema, 
                request.cantidad or 20, 
                "DEFINICION"
            )
        elif request.tipo == "resumen":
            resultado = await agent_factory.crear_resumen_ley(
                tema=request.tema
            )
        elif request.tipo == "mapa_mental":
            resultado = await agent_factory.crear_mapa_mental(
                request.tema, 
                3, 
                "MERMAID"
            )
        else:
            raise HTTPException(status_code=400, detail=f"Tipo {request.tipo} no soportado")
        
        return {
            "status": "success",
            "tipo": request.tipo,
            "data": resultado,
            "metadatos": {
                "tiempo_generacion": "2-5s",
                "fuente": "MCP + RAG + COSM",
                "costo": 0.0,  # COSM strategy
                "personalizado": request.personalizar
            }
        }
        
    except Exception as e:
        logger.error(f"Error creating content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/simulacro")
async def crear_simulacro(request: SimulacroRequest):
    """Crear simulacro con formato oficial BOE-A-2024-11403"""
    try:
        simulacro = await agent_factory.crear_simulacro_oficial(
            request.tema,
            request.nivel,
            request.usuario_id
        )
        
        return {
            "status": "success",
            "data": simulacro,
            "formato": "BOE-A-2024-11403",
            "estructura": "100 test + 12 casos prácticos"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/caso")
async def crear_caso(request: CasoPracticoRequest):
    """Crear caso práctico con jurisprudencia"""
    try:
        caso = await agent_factory.crear_caso_practico(
            request.tema,
            request.complejidad,
            request.incluir_jurisprudencia
        )
        
        return {
            "status": "success",
            "data": caso,
            "incluye_jurisprudencia": request.incluir_jurisprudencia
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/flashcards")
async def crear_flashcards(request: FlashcardsRequest):
    """Crear lote de flashcards"""
    try:
        flashcards = await agent_factory.crear_flashcards(
            request.tema,
            request.cantidad,
            request.estilo
        )
        
        return {
            "status": "success",
            "data": flashcards,
            "cantidad": len(flashcards),
            "estilo": request.estilo
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/resumen")
async def crear_resumen(request: ResumenRequest):
    """Crear resumen de ley"""
    try:
        resumen = await agent_factory.crear_resumen_ley(
            request.ley_id,
            request.tema,
            request.longitud
        )
        
        return {
            "status": "success",
            "data": resumen,
            "longitud": request.longitud
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mapa_mental")
async def crear_mapa_mental(request: MapaMentalRequest):
    """Crear mapa mental"""
    try:
        mapa = await agent_factory.crear_mapa_mental(
            request.tema,
            request.profundidad,
            request.formato
        )
        
        return {
            "status": "success",
            "data": mapa,
            "formato": request.formato,
            "profundidad": request.profundidad
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def agent_factory_health():
    """Health check de la factoría de agentes"""
    try:
        # Test MCP connection
        collections = await mcp_client.call_tool("mcp_opositaia_list_collections", {})
        
        return {
            "status": "healthy",
            "mcp_server": "connected",
            "collections": len(collections.get("collections", [])),
            "agents_available": [
                "simulacro_oficial",
                "caso_practico", 
                "flashcards",
                "resumen_ley",
                "mapa_mental"
            ],
            "estrategia": "COSM (Create Once, Serve Many)",
            "formato_oficial": "BOE-A-2024-11403"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "mcp_server": "disconnected"
        }

# ============================================================================
# BATCH GENERATION (Para estrategia COSM)
# ============================================================================

@router.post("/batch/generar_inicial")
async def generar_contenido_inicial(background_tasks: BackgroundTasks):
    """
    Generar contenido inicial para estrategia COSM
    Ejecutar UNA VEZ - Coste estimado: €18
    """
    try:
        background_tasks.add_task(ejecutar_generacion_masiva)
        
        return {
            "status": "started",
            "message": "Generación masiva iniciada en background",
            "estimado": {
                "simulacros": 1000,
                "casos": 500,
                "flashcards": 5000,
                "resumenes": 50,
                "tiempo_estimado": "2-3 horas",
                "coste_estimado": "€18"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def ejecutar_generacion_masiva():
    """Ejecuta la generación masiva en background"""
    logger.info("🚀 Iniciando generación masiva COSM...")
    
    try:
        # Obtener temas del RAG
        temas_result = await mcp_client.call_tool("mcp_opositaia_search_rag", {
            "query": "temas oposiciones seguridad social",
            "limit": 50
        })
        
        temas = [r.get("title", f"Tema {i}") for i, r in enumerate(temas_result.get("results", []))]
        
        # Generar contenido por lotes
        for tema in temas[:10]:  # Primeros 10 temas
            logger.info(f"Generando contenido para: {tema}")
            
            # 1 simulacro por tema
            simulacro = await agent_factory.crear_simulacro_oficial(tema, "INTERMEDIO")
            # TODO: Guardar en BD
            
            # 5 casos por tema
            for i in range(5):
                caso = await agent_factory.crear_caso_practico(tema, "MEDIA")
                # TODO: Guardar en BD
            
            # 50 flashcards por tema
            flashcards = await agent_factory.crear_flashcards(tema, 50, "DEFINICION")
            # TODO: Guardar en BD
            
            await asyncio.sleep(1)  # Rate limiting
        
        logger.info("✅ Generación masiva completada")
        
    except Exception as e:
        logger.error(f"❌ Error en generación masiva: {e}")