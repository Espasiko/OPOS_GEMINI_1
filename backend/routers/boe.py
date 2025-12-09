"""
BOE Router - FastAPI endpoints para la API oficial del BOE
Permite descargar y gestionar legislación consolidada desde datos abiertos del BOE
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, Dict, List
import logging
import sys
from pathlib import Path

# Add agents to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'agents'))

from boe_api_client import BOEApiClient

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/boe",
    tags=["boe"],
    responses={404: {"description": "Not found"}},
)


# ==========================================
# MODELOS PYDANTIC
# ==========================================

class BOESearchRequest(BaseModel):
    """Parámetros para búsqueda de legislación consolidada"""
    from_date: Optional[str] = None  # YYYYMMDD
    to_date: Optional[str] = None    # YYYYMMDD
    query: Optional[Dict] = None     # Criterios de búsqueda
    offset: int = 0
    limit: int = 50


class BOEDownloadRequest(BaseModel):
    """Parámetros para descargar una ley específica"""
    id_norma: str
    formato: str = "json"  # "xml" o "json"
    incluir_analisis: bool = False
    incluir_metadata_eli: bool = False


class BOEIndexRequest(BaseModel):
    """Parámetros para obtener índice de un documento"""
    id_norma: str
    formato: str = "json"


# ==========================================
# ENDPOINTS - LEGISLACIÓN CONSOLIDADA
# ==========================================

@router.get("/legislacion/lista")
async def listar_legislacion(
    from_date: Optional[str] = Query(None, description="Fecha inicio YYYYMMDD"),
    to_date: Optional[str] = Query(None, description="Fecha fin YYYYMMDD"),
    offset: int = Query(0, description="Primer resultado"),
    limit: int = Query(50, description="Máximo resultados")
):
    """
    Lista la legislación consolidada disponible en el BOE.
    
    Ejemplos:
    - /api/boe/legislacion/lista
    - /api/boe/legislacion/lista?limit=10
    - /api/boe/legislacion/lista?from_date=20220101&to_date=20221231
    """
    try:
        with BOEApiClient() as client:
            resultado = client.get_legislacion_consolidada(
                from_date=from_date,
                to_date=to_date,
                offset=offset,
                limit=limit
            )
            return resultado
    except Exception as e:
        logger.error(f"Error listando legislación: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/legislacion/documento/{id_norma}")
async def obtener_documento_completo(
    id_norma: str,
    formato: str = Query("json", description="json o xml")
):
    """
    Obtiene el documento completo de una norma consolidada.
    
    Incluye: metadatos + análisis + metadata-eli + texto completo
    
    Ejemplos:
    - /api/boe/legislacion/documento/BOE-A-2015-11724
    - /api/boe/legislacion/documento/BOE-A-2015-11724?formato=xml
    """
    try:
        with BOEApiClient() as client:
            resultado = client.get_documento_consolidado(
                id_norma=id_norma,
                formato=formato
            )
            return resultado
    except Exception as e:
        logger.error(f"Error obteniendo documento {id_norma}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/legislacion/metadatos/{id_norma}")
async def obtener_metadatos(
    id_norma: str,
    formato: str = Query("json", description="json o xml")
):
    """
    Obtiene solo los metadatos de una norma consolidada.
    
    Incluye: fecha_actualizacion, identificador, título, fechas, estado, etc.
    
    Ejemplos:
    - /api/boe/legislacion/metadatos/BOE-A-2015-11724
    - /api/boe/legislacion/metadatos/BOE-A-1978-31229?formato=xml
    """
    try:
        with BOEApiClient() as client:
            resultado = client.get_metadatos(
                id_norma=id_norma,
                formato=formato
            )
            return resultado
    except Exception as e:
        logger.error(f"Error obteniendo metadatos {id_norma}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/legislacion/texto/{id_norma}")
async def obtener_texto_consolidado(id_norma: str):
    """
    Obtiene el texto consolidado completo con todas las versiones.
    
    ⚠️ IMPORTANTE: Este endpoint devuelve XML (puede ser muy grande).
    
    Ejemplos:
    - /api/boe/legislacion/texto/BOE-A-2015-11724
    """
    try:
        with BOEApiClient() as client:
            resultado = client.get_texto_consolidado(id_norma)
            return {"id_norma": id_norma, "texto_xml": resultado}
    except Exception as e:
        logger.error(f"Error obteniendo texto {id_norma}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/legislacion/indice/{id_norma}")
async def obtener_indice(
    id_norma: str,
    formato: str = Query("json", description="json o xml")
):
    """
    Obtiene el índice del texto consolidado (lista de bloques/artículos).
    
    Útil para saber qué bloques tiene el documento sin descargar todo el texto.
    
    Ejemplos:
    - /api/boe/legislacion/indice/BOE-A-2015-11724
    """
    try:
        with BOEApiClient() as client:
            resultado = client.get_indice_texto(
                id_norma=id_norma,
                formato=formato
            )
            return resultado
    except Exception as e:
        logger.error(f"Error obteniendo índice {id_norma}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/legislacion/bloque/{id_norma}/{id_bloque}")
async def obtener_bloque_texto(
    id_norma: str,
    id_bloque: str
):
    """
    Obtiene un bloque específico del texto consolidado (ej: un artículo).
    
    Ejemplos:
    - /api/boe/legislacion/bloque/BOE-A-2015-11724/a1
    - /api/boe/legislacion/bloque/BOE-A-1978-31229/pr
    """
    try:
        with BOEApiClient() as client:
            resultado = client.get_bloque_texto(
                id_norma=id_norma,
                id_bloque=id_bloque
            )
            return {"id_norma": id_norma, "id_bloque": id_bloque, "bloque_xml": resultado}
    except Exception as e:
        logger.error(f"Error obteniendo bloque {id_bloque} de {id_norma}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# ENDPOINTS - SUMARIOS BOE
# ==========================================

@router.get("/sumario/{fecha}")
async def obtener_sumario(fecha: str):
    """
    Obtiene el sumario del BOE para una fecha específica.
    
    Args:
        fecha: Fecha en formato YYYYMMDD
    
    Ejemplos:
    - /api/boe/sumario/20231201
    """
    try:
        with BOEApiClient() as client:
            resultado = client.get_sumario(fecha)
            return resultado
    except Exception as e:
        logger.error(f"Error obteniendo sumario {fecha}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documento/{id_documento}")
async def obtener_documento_boe(
    id_documento: str,
    formato: str = Query("xml", description="xml, json o pdf")
):
    """
    Obtiene un documento específico del BOE.
    
    Args:
        id_documento: ID del documento BOE (ej: BOE-A-2023-12345)
        formato: xml, json o pdf
    
    Ejemplos:
    - /api/boe/documento/BOE-A-2023-12345
    - /api/boe/documento/BOE-A-2023-12345?formato=pdf
    """
    try:
        with BOEApiClient() as client:
            resultado = client.get_documento_boe(id_documento, formato)
            return {"id_documento": id_documento, "formato": formato, "contenido": resultado}
    except Exception as e:
        logger.error(f"Error obteniendo documento {id_documento}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# ENDPOINTS - HELPERS ESPECÍFICOS
# ==========================================

@router.post("/descargar/lgss")
async def descargar_lgss(
    guardar_en: Optional[str] = Query(None, description="Ruta absoluta donde guardar el XML")
):
    """
    Descarga la LGSS consolidada (BOE-A-2015-11724) y opcionalmente la guarda.
    
    Ejemplos:
    - POST /api/boe/descargar/lgss
    - POST /api/boe/descargar/lgss?guardar_en=/ruta/completa/LGSS.xml
    """
    try:
        id_norma = "BOE-A-2015-11724"
        
        with BOEApiClient() as client:
            logger.info(f"Descargando LGSS consolidada ({id_norma})...")
            texto_xml = client.get_texto_consolidado(id_norma)
            
            if guardar_en:
                with open(guardar_en, 'w', encoding='utf-8') as f:
                    f.write(texto_xml)
                logger.info(f"LGSS guardada en: {guardar_en}")
                return {
                    "id_norma": id_norma,
                    "archivo": guardar_en,
                    "size": len(texto_xml),
                    "status": "success"
                }
            else:
                return {
                    "id_norma": id_norma,
                    "size": len(texto_xml),
                    "texto_xml": texto_xml[:1000] + "...",  # Primeros 1000 chars
                    "status": "success"
                }
    except Exception as e:
        logger.error(f"Error descargando LGSS: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/descargar/constitucion")
async def descargar_constitucion(
    guardar_en: Optional[str] = Query(None, description="Ruta absoluta donde guardar el XML")
):
    """
    Descarga la Constitución Española consolidada (BOE-A-1978-31229).
    
    Ejemplos:
    - POST /api/boe/descargar/constitucion
    - POST /api/boe/descargar/constitucion?guardar_en=/ruta/Constitucion.xml
    """
    try:
        id_norma = "BOE-A-1978-31229"
        
        with BOEApiClient() as client:
            logger.info(f"Descargando Constitución ({id_norma})...")
            texto_xml = client.get_texto_consolidado(id_norma)
            
            if guardar_en:
                with open(guardar_en, 'w', encoding='utf-8') as f:
                    f.write(texto_xml)
                logger.info(f"Constitución guardada en: {guardar_en}")
                return {
                    "id_norma": id_norma,
                    "archivo": guardar_en,
                    "size": len(texto_xml),
                    "status": "success"
                }
            else:
                return {
                    "id_norma": id_norma,
                    "size": len(texto_xml),
                    "texto_xml": texto_xml[:1000] + "...",
                    "status": "success"
                }
    except Exception as e:
        logger.error(f"Error descargando Constitución: {e}")
        raise HTTPException(status_code=500, detail=str(e))
