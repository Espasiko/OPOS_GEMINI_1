"""
Parser y indexador de legislación consolidada desde la API del BOE.
Parsea el XML consolidado, extrae bloques/artículos, genera embeddings con bge-m3-spa-law-qa y los indexa en Qdrant.

MODELO RECOMENDADO: pablosi/bge-m3-spa-law-qa-trained-2 (sin restricciones)
- Fine-tuned desde littlejohn-ai/bge-m3-spa-law-qa
- 567.8M parámetros, 1024 dims
- Dataset: 5,036 pares BOE sintéticos
- Licencia: Apache 2.0, acceso inmediato
"""
import sys
sys.path.insert(0, '/mnt/e/1/OPOS_GEMINI_1/backend/agents')

import xml.etree.ElementTree as ET
from boe_api_client import BOEApiClient
from rag_agent_v2 import RAGAgentV2
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parsear_bloques_lgss(xml_file: str) -> list:
    """
    Parsea el XML consolidado y extrae bloques de texto.
    
    Returns:
        Lista de dicts con {id_bloque, titulo, tipo, texto}
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Navegar hasta el nodo <data><texto>
    data = root.find('.//data')
    if data is None:
        logger.error("No se encontró el nodo <data>")
        return []
    
    texto = data.find('texto')
    if texto is None:
        logger.error("No se encontró el nodo <texto>")
        return []
    
    bloques = []
    for bloque in texto.findall('bloque'):
        id_bloque = bloque.get('id', '')
        titulo = bloque.get('titulo', '')
        tipo = bloque.get('tipo', '')
        
        # Extraer el texto de la versión más reciente (última versión)
        versiones = bloque.findall('version')
        if not versiones:
            continue
        
        version = versiones[-1]  # Última versión (más reciente)
        
        # Extraer párrafos de texto
        textos = []
        for p in version.findall('.//p'):
            if p.text:
                textos.append(p.text.strip())
        
        texto_completo = ' '.join(textos)
        
        if texto_completo and len(texto_completo) > 50:  # Filtrar bloques muy cortos
            bloques.append({
                'id': id_bloque,
                'titulo': titulo,
                'tipo': tipo,
                'texto': texto_completo[:2000]  # Limitar a 2000 chars para embeddings
            })
    
    return bloques

def crear_coleccion_qdrant(collection_name: str = "opositaia_lgss_test"):
    """Crea una colección en Qdrant para los embeddings de la LGSS."""
    client = QdrantClient(url="http://localhost:6333")
    
    try:
        client.delete_collection(collection_name)
        logger.info(f"Colección {collection_name} eliminada (existía)")
    except:
        pass
    
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=1024, distance=Distance.COSINE)  # bge-m3 tiene 1024 dims
    )
    logger.info(f"✅ Colección {collection_name} creada")

def indexar_lgss_en_qdrant(bloques: list, collection_name: str = "opositaia_lgss_test"):
    """Genera embeddings locales con pablosi/bge-m3-spa-law-qa-trained-2 e indexa en Qdrant."""
    logger.info(f"Inicializando RAG Agent V2 con embeddings locales...")
    
    rag = RAGAgentV2(
        qdrant_url="http://localhost:6333",
        collection_name=collection_name,
        embedding_model="pablosi/bge-m3-spa-law-qa-trained-2",  # ✅ Sin restricciones
        use_local_embeddings=True,
        api_key=None  # evitar usar API key cloud en localhost
    )
    
    logger.info(f"Indexando {len(bloques)} bloques en Qdrant...")
    
    for i, bloque in enumerate(bloques):
        try:
            # Generar embedding local
            embedding = rag.generate_embedding(bloque['texto'])
            
            if not embedding or len(embedding) == 0:
                logger.warning(f"Embedding vacío para bloque {bloque['id']}")
                continue
            
            # Crear payload con metadata
            payload = {
                "id_bloque": bloque['id'],
                "titulo": bloque['titulo'],
                "tipo": bloque['tipo'],
                "texto": bloque['texto'],
                "ley": "LGSS",
                "boe_id": "BOE-A-2015-11724"
            }
            
            # Indexar en Qdrant
            rag.qdrant_client.upsert(
                collection_name=collection_name,
                points=[PointStruct(
                    id=i,
                    vector=embedding,
                    payload=payload
                )]
            )
            
            if i < 3:
                logger.info(f"  [{i+1}] {bloque['titulo'][:50]}... → {len(embedding)} dims")
        
        except Exception as e:
            logger.error(f"Error indexando bloque {bloque['id']}: {e}")
    
    logger.info(f"✅ {len(bloques)} bloques indexados correctamente")


if __name__ == "__main__":
    # 1. Descargar LGSS desde API BOE
    logger.info("=== DESCARGA LGSS DESDE API BOE ===")
    xml_file = "/mnt/e/1/OPOS_GEMINI_1/backend/data/leyes/LGSS_consolidada.xml"
    
    # 2. Parsear bloques
    logger.info("\n=== PARSEO DE BLOQUES XML ===")
    bloques = parsear_bloques_lgss(xml_file)
    logger.info(f"Total bloques extraídos: {len(bloques)}")
    
    if len(bloques) > 0:
        logger.info(f"\nEjemplos de bloques:")
        for bloque in bloques[:3]:
            logger.info(f"  - {bloque['titulo']}: {bloque['texto'][:100]}...")
    
    # 3. Crear colección Qdrant
    logger.info("\n=== CREACIÓN COLECCIÓN QDRANT ===")
    crear_coleccion_qdrant()
    
    # 4. Indexar bloques con embeddings
    logger.info("\n=== INDEXACIÓN CON EMBEDDINGS BGE-M3 ===")
    indexar_lgss_en_qdrant(bloques[:50])  # Probar con los primeros 50 bloques
    
    logger.info("\n✅ PROCESO COMPLETO EXITOSO")
