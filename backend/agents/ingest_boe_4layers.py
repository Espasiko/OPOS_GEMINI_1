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
            # Metadatos generales de la norma
            metadatos = self.boe_client.get_metadatos(boe_id)

            # Texto consolidado completo (XML) → fuente principal para artículos
            if hasattr(self.boe_client, 'get_texto_consolidado'):
                texto_xml = self.boe_client.get_texto_consolidado(boe_id)
            else:
                logger.warning(f"get_texto_consolidado not found in client, skipping full-text fetch for {boe_id}")
                texto_xml = ""

        except Exception as e:
            logger.error(f"Failed to fetch data for {boe_id}: {e}")
            return

        data_meta = metadatos.get('data', {}) if isinstance(metadatos, dict) else {}
        law_title = data_meta.get('titulo', 'Desconocido')
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
                "type": data_meta.get('rango') or "Ley",
                "date": data_meta.get('fecha_publicacion'),
                "url": data_meta.get('url_html_consolidada') or data_meta.get('url_html'),
                "estado": data_meta.get('estado') or data_meta.get('estado_consolidacion'),
                "norma": data_meta.get('identificador') or data_meta.get('titulo_corto') or law_title,
                "departamento": data_meta.get('departamento'),
                "ambito": data_meta.get('ambito_geografico'),
                "numero_oficial": data_meta.get('numero_oficial'),
                "materia": data_meta.get('materia'),
                "fecha_entrada_en_vigor": data_meta.get('fecha_entrada_en_vigor'),
                "fecha_ultima_modificacion": data_meta.get('fecha_ultima_modificacion'),
                "fecha_derogacion": data_meta.get('fecha_derogacion'),
                "version_eli": data_meta.get('eli')
            }
        )

        logger.info(f"indexed source layer for {boe_id}. Now indexing article-level articles from full XML (layer=1)...")

        # --- LAYER 1: ARTÍCULOS DESDE XML COMPLETO ---
        total_chunks = 0

        if texto_xml:
            articles = self._extract_articles_from_xml(texto_xml)
        else:
            articles = []

        for art_idx, art in enumerate(articles):
            art_text = art.get("text") or ""
            if not art_text.strip():
                continue

            # Chunking aproximado por longitud de caracteres (proxy 512 tokens ~ 1500-2000 chars)
            chunks = self._chunk_text(art_text, max_chars=1800, overlap_chars=200)
            if not chunks:
                continue

            articulo_num = art.get("articulo_num")
            titulo_bloque = art.get("articulo_titulo") or art.get("titulo_norma") or ""

            for chunk_idx, chunk_text in enumerate(chunks):
                # ID determinista por norma + artículo + chunk
                base_id = f"{boe_id}-art-{articulo_num or art_idx}-{chunk_idx}"
                point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, base_id))

                payload = {
                    "boe_id": boe_id,
                    "block_id": art.get("block_id"),  # opcional, por si se quiere mapear a índice
                    "chunk_index": chunk_idx,
                    "title": law_title,
                    "block_title": titulo_bloque,
                    "type": data_meta.get('rango') or "Ley",
                    "date": data_meta.get('fecha_publicacion'),
                    "url": data_meta.get('url_html_consolidada') or data_meta.get('url_html'),
                    "estado": data_meta.get('estado') or data_meta.get('estado_consolidacion'),
                    "norma": data_meta.get('identificador') or data_meta.get('titulo_corto') or law_title,
                    "departamento": data_meta.get('departamento'),
                    "ambito": data_meta.get('ambito_geografico'),
                    "numero_oficial": data_meta.get('numero_oficial'),
                    "materia": data_meta.get('materia'),
                    "fecha_entrada_en_vigor": data_meta.get('fecha_entrada_en_vigor'),
                    "fecha_ultima_modificacion": data_meta.get('fecha_ultima_modificacion'),
                    "fecha_derogacion": data_meta.get('fecha_derogacion'),
                    "version_eli": data_meta.get('eli'),
                    # Campos derivados de la estructura del artículo
                    "articulo_num": art.get("articulo_num"),
                    "articulo_titulo": art.get("articulo_titulo"),
                    "titulo_norma": art.get("titulo_norma"),
                    "capitulo": art.get("capitulo"),
                    "seccion": art.get("seccion"),
                    "subseccion": art.get("subseccion"),
                    "disposicion": art.get("disposicion"),
                    "modificaciones": art.get("modificaciones"),
                    "notas": art.get("notas"),
                }

                self._index_item(
                    id=point_id,
                    text=chunk_text,
                    layer="1",
                    payload=payload,
                )

                total_chunks += 1

        logger.info(f"Indexed {total_chunks} article-level chunks for {boe_id} (layer=1) from full XML")

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

    def _clean_xml_to_text(self, xml_content: str) -> str:
        """Very simple XML to text cleaner: strips tags and normalizes whitespace."""
        import re

        if not xml_content:
            return ""

        # Remove XML/HTML tags
        text = re.sub(r"<[^>]+>", " ", xml_content)
        # Collapse whitespace
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _extract_articles_from_xml(self, xml_content: str) -> List[Dict[str, Any]]:
        """Extrae artículos (<articulo>) del XML consolidado de una norma.

        Para cada artículo localiza número, rúbrica y contexto jerárquico
        reutilizando la lógica de _extract_block_structure.
        """
        import xml.etree.ElementTree as ET

        articles: List[Dict[str, Any]] = []
        if not xml_content:
            return articles

        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError:
            return articles

        # Recorremos todos los nodos <articulo>/<artículo>
        for art_el in root.iter():
            tag_lower = art_el.tag.lower()
            if not (tag_lower.endswith("articulo") or tag_lower.endswith("artículo")):
                continue

            # Serializar solo este artículo a XML independiente
            art_xml = ET.tostring(art_el, encoding="unicode")

            # Estructura legal best-effort
            struct = self._extract_block_structure(art_xml)

            # Texto plano del artículo
            art_text = self._clean_xml_to_text(art_xml)
            if not art_text.strip():
                continue

            # Asegurar campos clave
            num = struct.get("articulo_num") or art_el.attrib.get("num") or art_el.attrib.get("n")
            struct["articulo_num"] = num
            struct["text"] = art_text

            articles.append(struct)

        return articles

    def _extract_block_structure(self, xml_content: str) -> Dict[str, Any]:
        """Extrae, de forma best-effort, la estructura legal de un bloque XML del BOE.

        Intenta localizar información típica: artículo, título, capítulo, secciones,
        disposiciones, notas y referencias de modificación.
        """
        import xml.etree.ElementTree as ET

        result: Dict[str, Any] = {}
        if not xml_content:
            return result

        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError:
            return result

        # Helpers
        def find_first_by_tag_endswith(node: ET.Element, suffixes) -> Optional[ET.Element]:
            if isinstance(suffixes, str):
                suffixes_local = (suffixes,)
            else:
                suffixes_local = tuple(suffixes)
            for el in node.iter():
                if any(el.tag.lower().endswith(suf) for suf in suffixes_local):
                    return el
            return None

        def clean_text(el: Optional[ET.Element]) -> Optional[str]:
            if el is None:
                return None
            text_parts = [el.text or ""]
            for child in el:
                if child.text:
                    text_parts.append(child.text)
                if child.tail:
                    text_parts.append(child.tail)
            text = " ".join(text_parts).strip()
            return text or None

        # Artículo principal
        articulo_el = find_first_by_tag_endswith(root, ["articulo", "artículo"])
        if articulo_el is not None:
            num = articulo_el.attrib.get("num") or articulo_el.attrib.get("n")
            if num:
                result["articulo_num"] = num

            # Título/rúbrica del artículo
            rubrica_el = find_first_by_tag_endswith(articulo_el, ["rubrica", "rúbrica", "titulo", "título"])
            if rubrica_el is not None:
                result["articulo_titulo"] = clean_text(rubrica_el)

        # Título / Capítulo / Sección
        titulo_el = find_first_by_tag_endswith(root, ["titulo", "título"])
        if titulo_el is not None:
            result["titulo_norma"] = clean_text(titulo_el)

        capitulo_el = find_first_by_tag_endswith(root, ["capitulo", "capítulo"])
        if capitulo_el is not None:
            result["capitulo"] = clean_text(capitulo_el)

        seccion_el = find_first_by_tag_endswith(root, ["seccion", "sección"])
        if seccion_el is not None:
            result["seccion"] = clean_text(seccion_el)

        subseccion_el = find_first_by_tag_endswith(root, ["subseccion", "subsección"])
        if subseccion_el is not None:
            result["subseccion"] = clean_text(subseccion_el)

        # Disposiciones adicionales/transitorias/etc.
        disp_el = find_first_by_tag_endswith(root, ["disposicion", "disposición"])
        if disp_el is not None:
            result["disposicion"] = clean_text(disp_el)

        # Notas y modificaciones
        notas = []
        modificaciones = []
        for el in root.iter():
            tag_lower = el.tag.lower()
            if tag_lower.endswith("nota") or tag_lower.endswith("notas"):
                txt = clean_text(el)
                if txt:
                    notas.append(txt)
            if "modifica" in tag_lower or "modificacion" in tag_lower or "modificación" in tag_lower:
                txt = clean_text(el)
                if txt:
                    modificaciones.append(txt)

        if notas:
            result["notas"] = notas
        if modificaciones:
            result["modificaciones"] = modificaciones

        return result

    def _chunk_text(self, text: str, max_chars: int = 1800, overlap_chars: int = 200) -> List[str]:
        """Simple character-based chunking as proxy for token-based 512/50 strategy."""
        if not text:
            return []

        if max_chars <= 0:
            return [text]

        chunks: List[str] = []
        start = 0
        length = len(text)

        while start < length:
            end = min(start + max_chars, length)
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            if end == length:
                break

            # Move start forward with overlap
            start = max(0, end - overlap_chars)

        return chunks

if __name__ == "__main__":
    indexer = BOEIndexer()
    indexer.ensure_collection()
    
    # 17 Leyes prioritarias (13 principales + 4 faltantes del temario oficial)
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
        {"id": "BOE-A-2006-21990", "nombre": "Ley Dependencia"},
        # 4 leyes faltantes del temario oficial (LEYES_FALTANTES_TEMARIO_OFICIAL.md)
        {"id": "BOE-A-2014-13517", "nombre": "Ley 34/2014 Liquidación cuotas SS"},
        {"id": "BOE-A-1985-12666", "nombre": "LO 6/1985 LOPJ"},
        {"id": "BOE-A-1979-23709", "nombre": "LO 2/1979 LOTC"},
        {"id": "BOE-A-1985-11672", "nombre": "LO 5/1985 LOREG"}
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

    # Resumen final de la colección en Qdrant
    try:
        info = indexer.client.get_collection(COLLECTION_NAME)
        points = info.points_count
        vector_size = VECTOR_SIZE
        # Estimación muy aproximada de tamaño: puntos * vector_size * 4 bytes (float32) → MB
        estimated_mb = (points * vector_size * 4) / (1024 * 1024)
        print("\n" + "=" * 80)
        print(f"📊 RESUMEN COLECCIÓN QDRANT: {COLLECTION_NAME}")
        print(f"   Puntos totales: {points:,}")
        print(f"   Dimensión vector: {vector_size}")
        print(f"   Tamaño estimado (solo vectores densos): {estimated_mb:,.2f} MB")
        print("=" * 80)
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas de Qdrant: {e}")
