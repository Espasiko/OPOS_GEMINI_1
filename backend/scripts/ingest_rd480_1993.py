import os
import sys
import uuid
import time
from backend.agents.boe_api_client import BOEApiClient
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup
from lxml import etree
import re
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "opositaia_knowledge_FULL_XML"
BOE_ID = "BOE-A-2010-11409"  # STC 31/2010 Estatut Cataluña

client = QdrantClient(url=QDRANT_URL)
boe_client = BOEApiClient()

try:
    logger.info("Cargando modelo BGE-M3...")
    model = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
except Exception as e:
    logger.error(f"Error al cargar BGE-M3: {e}")
    sys.exit(1)

def extract_metadata_from_xml(xml_content: str) -> dict:
    try:
        root = etree.fromstring(xml_content.encode('utf-8'))
        metadata = {
            "law_name": root.findtext(".//titulo", "Título Desconocido"),
            "departamento": root.findtext(".//departamento", ""),
            "rango": root.findtext(".//rango", ""),
            "fecha_disposicion": root.findtext(".//fecha_disposicion", ""),
            "fecha_publicacion": root.findtext(".//fecha_publicacion", ""),
            "notas": [n.text for n in root.findall(".//notas/nota") if n.text],
            "materias": [m.text for m in root.findall(".//materias/materia") if m.text],
            "alertas": [a.text for a in root.findall(".//alertas/alerta") if a.text],
            "modifica_a": [m.text for m in root.findall(".//modifica/referencia") if m.text],
            "modificado_por": [m.text for m in root.findall(".//modificado_por/referencia") if m.text],
            "deroga_a": [d.text for d in root.findall(".//deroga/referencia") if d.text],
            "derogado_por": [d.text for d in root.findall(".//derogado_por/referencia") if d.text],
            "vigente": True
        }
        
        for alert in metadata["alertas"]:
            if "derogad" in alert.lower() or "anulad" in alert.lower():
                metadata["vigente"] = False
                break
                
        return metadata
    except Exception as e:
        logger.warning(f"Error extrayendo metadatos: {e}")
        return {}

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> list:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

import requests
def ingest_boe(_id):
    logger.info(f"Descargando {_id}...")
    try:
        xml_url = f"https://www.boe.es/diario_boe/xml.php?id={_id}"
        response = requests.get(xml_url)
        response.raise_for_status()
        xml_content = response.text
        if not xml_content:
            logger.error("XML vacío")
            return
            
        metadata = extract_metadata_from_xml(xml_content)
        soup = BeautifulSoup(xml_content, 'xml')
        
        texto_elem = soup.find('texto')
        if not texto_elem:
            logger.error("No hay nodo <texto>")
            return
            
        full_text = texto_elem.get_text(separator=' ', strip=True)
        chunks = chunk_text(full_text)
        
        points = []
        for i, chunk in enumerate(chunks):
            chunk_metadata = metadata.copy()
            chunk_metadata.update({
                "boe_id": _id,
                "article_number": f"chunk_{i}",
                "tipo_dato": "articulo",
                "text": chunk,
                "url": xml_url
            })
            
            dense_vec = model.encode(chunk).tolist()
            # Simplistic BM25 vector for insertion
            sparse_vec = {"indices": [abs(hash(w)) % 100000 for w in chunk.split()[:50]], "values": [1.0] * min(len(chunk.split()), 50)}
            
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{_id}_chunk_{i}"))
            
            points.append(
                PointStruct(
                    id=point_id,
                    vector={
                        "dense": dense_vec,
                        "text": sparse_vec
                    },
                    payload=chunk_metadata
                )
            )
            
        if points:
            client.upsert(collection_name=COLLECTION_NAME, points=points)
            logger.info(f"✅ Insertados {len(points)} chunks para {_id}")
            
    except Exception as e:
        logger.error(f"Fallo grave en {_id}: {e}")

if __name__ == "__main__":
    ingest_boe(BOE_ID)
