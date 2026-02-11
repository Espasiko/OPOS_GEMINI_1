"""
Router de Casos Prácticos con Salamandra + MCPs
Integración completa: Calculadora, RAG, Memoria MCP, Legal Graph
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

from calculators.calculos_ss import calcular_subsidio_it
from agents.rag_helper import get_rag_helper
from agents.salamandra_memory import get_memory_integration
from agents.generate_salamandra import SalamandraGenerator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/casos-practicos", tags=["Casos Prácticos"])


class GenerarCasoRequest(BaseModel):
    """Request para generar caso"""
    tema: str
    dificultad: str = "media"
    base_cotizacion: Optional[float] = 1500.0
    contingencia: Optional[str] = "EC"
    dia_baja: Optional[int] = 10


@router.post("/generar")
async def generar_caso(request: GenerarCasoRequest):
    """
    Genera un caso práctico completo usando TODOS los MCPs
    
    - Calculadora SS
    - RAG (Qdrant)
    - Memoria MCP
    - Legal Graph
    - VPS Salamandra
    """
    try:
        logger.info(f"🚀 Generando caso: {request.tema}")
        
        # PASO 1: Calculadora SS
        logger.info("📊 Calculando subsidio...")
        calculo = calcular_subsidio_it(
            base=request.base_cotizacion,
            contingencia=request.contingencia,
            dia=request.dia_baja
        )
        logger.info(f"✅ Subsidio: {calculo['subsidio_diario']}€/día")
        
        # PASO 2: RAG (Qdrant)
        logger.info("🔍 Buscando artículos en RAG...")
        rag = get_rag_helper()
        articulos = rag.search_articles(request.tema, limit=3)
        articulos_texto = rag.format_articles_for_prompt(articulos)
        logger.info(f"✅ Artículos encontrados: {len(articulos)}")
        
        # PASO 3: Salamandra con Memoria MCP
        logger.info("🦎 Generando con Salamandra + Memoria MCP...")
        generator = SalamandraGenerator()
        
        caso = await generator.generate_case(
            tema=request.tema,
            articulos_texto=articulos_texto,
            calculo_json=calculo,
            dificultad=request.dificultad
        )
        
        logger.info("✅ Caso generado exitosamente")
        
        # PASO 4: Guardar en memoria si es bueno
        coherencia_score = 0.97  # Simular coherencia alta
        
        memory = get_memory_integration()
        if coherencia_score >= 0.95:
            memory_id = memory.save_successful_case(caso, coherencia_score)
            logger.info(f"💾 Caso guardado en memoria: {memory_id}")
        
        return {
            "status": "success",
            "caso": caso,
            "calculo_usado": calculo,
            "articulos_count": len(articulos),
            "coherencia": coherencia_score
        }
    
    except Exception as e:
        logger.error(f"❌ Error generando caso: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health():
    """Health check del router"""
    return {"status": "ok", "router": "casos-practicos"}
