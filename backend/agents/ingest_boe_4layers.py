import os
import sys
import uuid
import logging
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
        import time
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
                        # Future: Add sparse_vectors_config here when SPLADE/BGE-M3-Sparse is integrated
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
            # We assume get_metadatos returns a dict and get_texto_consolidado returns text/xml
            metadatos = self.boe_client.get_metadatos(boe_id)
            # Fetch text (consolidated XML usually)
            # Note: get_texto_consolidado might return a large string
            # In a real impl, we might stream or chunk this.
            # For now, we fetch it (assuming memory holds it)
            # If get_texto_consolidado isn't available, we use helpers from previous findings
            if hasattr(self.boe_client, 'get_texto_consolidado'):
                 texto_xml = self.boe_client.get_texto_consolidado(boe_id)
            else:
                 logger.warning(f"get_texto_consolidado not found in client, skipping text processing for {boe_id}")
                 texto_xml = ""
                 
        except Exception as e:
            logger.error(f"Failed to fetch data for {boe_id}: {e}")
            return

        law_title = metadatos.get('data', {}).get('titulo', 'Desconocido')
        logger.info(f"Law Title: {law_title}")

        # --- LAYER 1: DOCUMENT / SOURCE ---
        source_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, boe_id))
        self._index_item(
            id=source_id,
            text=f"{law_title}. {metadatos.get('data', {}).get('departamento', '')}",
            layer="source",
            payload={
                "boe_id": boe_id,
                "title": law_title,
                "type": "Ley",
                "date": metadatos.get('data', {}).get('fecha_publicacion'),
                "url": metadatos.get('data', {}).get('url_html_consolidada')
            }
        )
        
        # Placeholder for full XML parsing
        logger.info(f"indexed source layer for {boe_id}. (Parsing logic would go here for other layers)")

    def _index_item(self, id: str, text: str, layer: str, payload: Dict[str, Any]):
        """Helper to vectorize and upsert a single item"""
        # Generate Embedding (Dense)
        vector = self.model.encode(text).tolist()
        
        # Add basic metadata to payload
        payload["text"] = text[0:1000] # Store snippet in payload, not full text if huge
        payload["layer"] = layer
        payload["timestamp"] = datetime.now().isoformat()

        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                models.PointStruct(
                    id=id,
                    vector={"dense": vector},
                    payload=payload
                )
            ]
        )

if __name__ == "__main__":
    indexer = BOEIndexer()
    indexer.ensure_collection()
    
    # 13 Leyes Prioritarias (Criticas + Altas + Medias)
    CATALOGO_LEYES = [
        {"id": "BOE-A-2015-11724", "nombre": "LGSS"},
        {"id": "BOE-A-1996-3981", "nombre": "RD 84/1996 Afiliación"},
        {"id": "BOE-A-1995-26497", "nombre": "RD 2064/1995 Cotización"},
        {"id": "BOE-A-2004-11607", "nombre": "RD 1415/2004 Recaudación"},
        {"id": "BOE-A-1978-31229", "nombre": "Constitución Española"},
        {"id": "BOE-A-2015-10565", "nombre": "Ley 39/2015 LPACAP"},
        {"id": "BOE-A-2015-10566", "nombre": "Ley 40/2015 LRJSP"},
        {"id": "BOE-A-2015-11719", "nombre": "EBEP"},
        {"id": "BOE-A-2009-15442", "nombre": "RD 1430/2009 IT"},
        {"id": "BOE-A-1995-19848", "nombre": "RD 1300/1995 IP"},
        {"id": "BOE-A-2021-9155",  "nombre": "Ley IMV"},
        {"id": "BOE-A-2018-16673", "nombre": "LOPDGDD"},
        {"id": "BOE-A-2006-21990", "nombre": "Ley Dependencia"}
    ]
    
    print(f"🚀 Iniciando ingesta masiva de {len(CATALOGO_LEYES)} leyes...")
    
    for i, ley in enumerate(CATALOGO_LEYES, 1):
        print(f"\n[{i}/{len(CATALOGO_LEYES)}] Procesando {ley['nombre']} ({ley['id']})...")
        try:
            indexer.process_law(ley['id'])
            print(f"✅ {ley['nombre']} completada.")
        except KeyboardInterrupt:
            print("\n🛑 Ingesta detenida por el usuario.")
            break
        except Exception as e:
            logger.error(f"❌ Error critique en {ley['nombre']}: {e}")
            continue

    logger.info("Indexing Job Complete.")
