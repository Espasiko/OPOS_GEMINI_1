import os
import sys
import uuid
import logging
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.append(project_root)

print("DEBUG: Script started...", flush=True)

try:
    print("DEBUG: Importing QdrantClient...", flush=True)
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
    print("DEBUG: Importing SentenceTransformer...", flush=True)
    from sentence_transformers import SentenceTransformer
    print("DEBUG: Importing BeautifulSoup...", flush=True)
    from bs4 import BeautifulSoup
    print("DEBUG: Importing BOEApiClient...", flush=True)
    try:
        from backend.agents.boe_api_client import BOEApiClient
    except ImportError:
        from boe_api_client import BOEApiClient
    print("DEBUG: Imports successful.", flush=True)
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    sys.exit(1)

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "opositaia_knowledge"
MODEL_NAME = "pablosi/bge-m3-spa-law-qa-trained-2"
VECTOR_SIZE = 1024

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BOEIndexer:
    def __init__(self):
        print("DEBUG: Initializing BOEIndexer...")
        try:
            self.client = QdrantClient(url=QDRANT_URL)
            print(f"DEBUG: Qdrant Client initialized with URL: {QDRANT_URL}")
        except Exception as e:
            print(f"DEBUG: Failed to init Qdrant Client: {e}")
            
        logger.info(f"Loading model: {MODEL_NAME}...")
        self.model = SentenceTransformer(MODEL_NAME)
        self.boe_client = BOEApiClient()

    def ensure_collection(self):
        """Creates the collection with 4-layer compatible schema if it doesn't exist."""
        max_retries = 10
        for i in range(max_retries):
            try:
                if not self.client.collection_exists(COLLECTION_NAME):
                    logger.info(f"Creating collection {COLLECTION_NAME}...")
                    self.client.create_collection(
                        collection_name=COLLECTION_NAME,
                        vectors_config={
                            "dense": models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE)
                        },
                    )
                    
                    # Create payload indexes for faster filtering
                    self.client.create_payload_index(COLLECTION_NAME, "layer", models.PayloadSchemaType.KEYWORD)
                    self.client.create_payload_index(COLLECTION_NAME, "boe_id", models.PayloadSchemaType.KEYWORD)
                    self.client.create_payload_index(COLLECTION_NAME, "parent_id", models.PayloadSchemaType.KEYWORD)
                    logger.info("Collection created successfully.")
                    return
                else:
                    logger.info(f"Collection {COLLECTION_NAME} already exists.")
                    return
            except Exception as e:
                logger.warning(f"Connection attempt {i+1}/{max_retries} failed: {e}. Retrying in 5s...")
                time.sleep(5)
        
        logger.error("Could not connect to Qdrant after multiple retries.")
        sys.exit(1)

    def process_law(self, boe_id: str):
        """Full pipeline: Download -> Parse -> Vectorize -> Index (4 Layers)"""
        logger.info(f"Processing Law: {boe_id}")
        
        try:
            # Metadatos generales de la norma
            metadatos = self.boe_client.get_metadatos(boe_id)
            
            # Texto consolidado completo (XML)
            texto_xml = self.boe_client.get_texto_consolidado(boe_id)
            
            if not texto_xml:
                logger.warning(f"No XML content for {boe_id}")
                return

            # Parsear artículos (simulado por ahora, idealmente usar parser XML real)
            # Aquí asumimos que get_texto_consolidado devuelve el texto completo
            # En una implementación real, parsearíamos el XML para extraer artículos individuales
            
            # Layer 1: Documento completo (metadata)
            doc_id = str(uuid.uuid4())
            self.client.upsert(
                collection_name=COLLECTION_NAME,
                points=[
                    models.PointStruct(
                        id=doc_id,
                        vector={"dense": self.model.encode(metadatos.get('titulo', ''))},
                        payload={
                            "layer": "document",
                            "boe_id": boe_id,
                            "title": metadatos.get('titulo', ''),
                            "text": metadatos.get('titulo', ''),
                            "metadata": metadatos
                        }
                    )
                ]
            )

            # Layer 2: Artículos (Smart Chunking con BeautifulSoup)
            soup = BeautifulSoup(texto_xml, 'xml')
            articulos = soup.find_all('articulo')
            
            if not articulos:
                logger.warning(f"No articles found in XML for {boe_id}. Fallback to simple chunking.")
                chunks = [texto_xml[i:i+1000] for i in range(0, len(texto_xml), 1000)]
                # Simple chunking logic (fallback)
                points = []
                for i, chunk in enumerate(chunks):
                    chunk_id = str(uuid.uuid4())
                    embedding = self.model.encode(chunk)
                    points.append(models.PointStruct(
                        id=chunk_id,
                        vector={"dense": embedding},
                        payload={
                            "layer": "article_chunk",
                            "boe_id": boe_id,
                            "parent_id": doc_id,
                            "chunk_index": i,
                            "text": chunk,
                            "metadata": metadatos,
                            "is_fallback": True
                        }
                    ))
                    if len(points) >= 50:
                        self.client.upsert(collection_name=COLLECTION_NAME, points=points)
                        points = []
                if points:
                    self.client.upsert(collection_name=COLLECTION_NAME, points=points)
            else:
                logger.info(f"Found {len(articulos)} articles. Processing with Smart Chunking...")
                points = []
                for i, art in enumerate(articulos):
                    # Extract text from article
                    # Usually <articulo id="..."><texto>...</texto></articulo>
                    # Or just the full text of the tag
                    art_text = art.get_text(separator=" ", strip=True)
                    art_id_boe = art.get('id', f"art_{i}")
                    
                    if len(art_text) < 50: # Skip very short articles/placeholders
                        continue

                    chunk_id = str(uuid.uuid4())
                    embedding = self.model.encode(art_text)
                    
                    points.append(models.PointStruct(
                        id=chunk_id,
                        vector={"dense": embedding},
                        payload={
                            "layer": "article_chunk",
                            "boe_id": boe_id,
                            "parent_id": doc_id,
                            "chunk_index": i,
                            "text": art_text,
                            "article_id": art_id_boe,
                            "metadata": metadatos,
                            "is_smart_chunk": True
                        }
                    ))
                    
                    if len(points) >= 50:
                        self.client.upsert(collection_name=COLLECTION_NAME, points=points)
                        points = []
                
                if points:
                    self.client.upsert(collection_name=COLLECTION_NAME, points=points)
                
            logger.info(f"Successfully indexed {boe_id}")

        except Exception as e:
            logger.error(f"Error processing {boe_id}: {e}")

def main():
    indexer = BOEIndexer()
    indexer.ensure_collection()
    
    # Lista de leyes principales (extraída de boe_xml_urls.md) - LIMPIA DE ERRORES 404
    leyes_principales = [
        "BOE-A-2015-11430", # Estatuto de los Trabajadores
        "BOE-A-2015-11431", # Ley de Empleo
        "BOE-A-2015-9734",  # Ley 30/2015 FP
        "BOE-A-1994-12554", # Ley ETT
        "BOE-A-1985-16660", # Libertad Sindical
        "BOE-A-2022-11589", # Igualdad de trato
        "BOE-A-2021-21652", # Reforma laboral
        # "BOE-A-1995-21112", # Jornadas especiales - ERROR 404
        # "BOE-A-2024-2790",  # SMI 2024 - ERROR 404
        "BOE-A-2020-12215", # Igualdad retributiva
        "BOE-A-2020-12214", # Planes de igualdad
        "BOE-A-2023-5366",  # Ley de Empleo 3/2023
        # "BOE-A-2015-7867",  # TR Ley de Empleo - ERROR 404
        # "BOE-A-2015-2770",  # RDL 4/2015 FP Empleo - ERROR 404
        "BOE-A-2022-4975",  # LO 3/2022 FP
        "BOE-A-2017-7769",  # RD 694/2017
        # "BOE-A-2008-1782",  # RD 34/2008 - ERROR 404
        # "BOE-A-2008-4900",  # Orden TAS/718/2008 - ERROR 404
        # "BOE-A-2015-7058",  # RD 7/2015 - ERROR 404
        # "BOE-A-2022-21341", # Estrategia Empleo - ERROR 404
        # "BOE-A-1995-1322",  # RD 4/1995 ETT - ERROR 404
        # "BOE-A-2010-18860", # Agencias colocación - ERROR 404
        # "BOE-A-2007-19991", # Empresas inserción - ERROR 404
        # "BOE-A-2022-6265",  # RDL 4/2022 - ERROR 404
        # "BOE-A-2011-17052", # Prácticas no laborales - ERROR 404
        # "BOE-A-2019-3819",  # Cartera Común SNE - ERROR 404
        # "BOE-A-1994-18814", # Elecciones representación - ERROR 404
        # "BOE-A-1977-8805",  # RDL relaciones de trabajo 17/1977 (Añadido de boe_xml_urls.md) - ERROR 404
    ]
    
    print(f"Starting ingestion of {len(leyes_principales)} laws...")
    
    for boe_id in leyes_principales:
        indexer.process_law(boe_id)
        time.sleep(1) # Rate limiting preventivo

if __name__ == "__main__":
    main()
