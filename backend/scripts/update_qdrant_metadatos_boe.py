#!/usr/bin/env python3
import sys
import os
import json
import logging
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.http import models

# Configuración y paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT / "backend"))

from agents.boe_api_client import BOEApiClient

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "opositaia_knowledge_FULL_XML"

def parsear_referencias(nodo_referencias):
    """Extrae una lista de strings con las referencias legales a partir del nodo del BOE."""
    if not nodo_referencias:
        return []
    
    lista = []
    if isinstance(nodo_referencias, dict) and "referencia" in nodo_referencias:
        refs = nodo_referencias["referencia"]
        if isinstance(refs, list):
            for r in refs:
                texto = r.get("texto", "")
                palabra = r.get("palabra", "")
                if palabra and texto:
                    lista.append(f"{palabra} {texto}")
                elif texto:
                    lista.append(texto)
        elif isinstance(refs, dict):
            texto = refs.get("texto", "")
            palabra = refs.get("palabra", "")
            if palabra and texto:
                lista.append(f"{palabra} {texto}")
            elif texto:
                lista.append(texto)
    return lista

def parsear_materias(nodo_materias):
    """Extrae las materias como una lista de strings."""
    if not nodo_materias:
        return []
        
    lista = []
    if isinstance(nodo_materias, dict) and "materia" in nodo_materias:
        mats = nodo_materias["materia"]
        if isinstance(mats, list):
            for m in mats:
                if isinstance(m, str):
                    lista.append(m)
                elif isinstance(m, dict) and "texto" in m:
                    lista.append(m["texto"])
        elif isinstance(mats, dict):
            if "texto" in mats:
                lista.append(mats["texto"])
        elif isinstance(mats, str):
            lista.append(mats)
    return lista

def get_metadatos_completos_boe(boe_id, boe_api):
    try:
        # Intento bajar el json del consolidado
        doc = boe_api.get_metadatos(boe_id, formato="json")
        if not doc:
            return None
            
        data = doc.get("data", {}) if isinstance(doc, dict) else {}
        documento = data.get("documento", {}) if isinstance(data, dict) else {}
        metadatos = documento.get("metadatos", {}) if isinstance(documento, dict) else {}
        analisis = documento.get("analisis", {}) if isinstance(documento, dict) else {}
        
        if not metadatos and not analisis:
            # Quizás sea una lista
            if isinstance(doc, list) and len(doc) > 0:
                documento = doc[0].get("documento", {}) if isinstance(doc[0], dict) else {}
                metadatos = documento.get("metadatos", {})
                analisis = documento.get("analisis", {})
        
        # Extracción segura
        materias = parsear_materias(analisis.get("materias", {})) if isinstance(analisis, dict) else []
        notas = analisis.get("notas", {}).get("nota", []) if isinstance(analisis, dict) and isinstance(analisis.get("notas"), dict) else []
        if isinstance(notas, str): notas = [notas]
        elif isinstance(notas, dict) and "texto" in notas: notas = [notas["texto"]]
        
        ref_ant = parsear_referencias(analisis.get("referencias_anteriores", {})) if isinstance(analisis, dict) else []
        ref_post = parsear_referencias(analisis.get("referencias_posteriores", {})) if isinstance(analisis, dict) else []
        
        # Fechas y Alertas
        fecha_pub = metadatos.get("fecha_publicacion", "") if isinstance(metadatos, dict) else ""
        fecha_disp = metadatos.get("fecha_disposicion", "") if isinstance(metadatos, dict) else ""
        estatus = metadatos.get("estatus", "") if isinstance(metadatos, dict) else ""
        
        return {
            "materias": materias,
            "notas": notas,
            "referencias_anteriores": ref_ant,
            "referencias_posteriores": ref_post,
            "fecha_publicacion": fecha_pub,
            "fecha_disposicion": fecha_disp,
            "estatus": estatus,
            "metadatos_completos": True
        }
    except Exception as e:
        logger.error(f"Error obteniendo metadatos completos para {boe_id}: {e}")
        return None

def main():
    logger.info("=========================================")
    logger.info("INICIANDO ACTUALIZACIÓN RETROACTIVA DE METADATOS")
    logger.info("=========================================")
    
    client = QdrantClient(url=QDRANT_URL, timeout=60)
    boe_api = BOEApiClient(timeout=15)
    
    # 1. Obtener todos los BOE IDs únicos en Qdrant
    # Scroll por la DB para recolectar el campo 'boe_id'
    logger.info("Escaneando colección en Qdrant para encontrar todas las leyes...")
    boe_ids_unicos = set()
    offset = None
    
    while True:
        resultados, next_offset = client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=None,
            limit=1000,
            with_payload=["boe_id", "metadatos_completos"],
            with_vectors=False,
            offset=offset
        )
        for r in resultados:
            b_id = r.payload.get("boe_id")
            if b_id:
                boe_ids_unicos.add(b_id)
        
        if next_offset is None:
            break
        offset = next_offset
        
    logger.info(f"Encontrados {len(boe_ids_unicos)} BOE IDs únicos en Qdrant.")
    
    # 2. Iterar cada BOE ID y extraer del BOE oficial
    actualizados = 0
    fallidos = 0
    
    for boe_id in boe_ids_unicos:
        logger.info(f"🌍 Procesando: {boe_id}")
        metadatos_extra = get_metadatos_completos_boe(boe_id, boe_api)
        
        if metadatos_extra:
            # Hacer UPDATE (Set Payload) en Qdrant a TODOS los puntos que tengan este boe_id
            try:
                client.set_payload(
                    collection_name=COLLECTION_NAME,
                    payload=metadatos_extra,
                    points=models.Filter(
                        must=[models.FieldCondition(
                            key="boe_id",
                            match=models.MatchValue(value=boe_id)
                        )]
                    )
                )
                logger.info(f"   ✅ Metadatos enriquecidos inyectados en {boe_id}")
                actualizados += 1
            except Exception as e:
                logger.error(f"   ❌ Error al actualizar payload en Qdrant para {boe_id}: {e}")
                fallidos += 1
        else:
            logger.warning(f"   ⚠️ No se pudieron obtener metadatos de la API BOE para {boe_id}")
            fallidos += 1
            
    logger.info("=========================================")
    logger.info(f"RESUMEN: {actualizados} Leyes actualizadas con éxito. {fallidos} fallidas.")
    logger.info("=========================================")

if __name__ == "__main__":
    main()
