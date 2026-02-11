#!/usr/bin/env python3
"""
Script de Procesamiento y Chunking Inteligente
FASE 2-3 del Plan Maestro: Limpieza XML → Texto → Chunks con Solapamiento
"""
import os
import sys
import json
import re
import uuid
import logging
import psycopg2
from html import unescape
from typing import List, Dict, Tuple, Optional
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
env_path = "/home/spas/OPOS_GEMINI_1/backend/.env.backend"
if os.path.exists(env_path):
    load_dotenv(env_path)
    logger.info(f"✅ Loaded env from {env_path}")

# Chunking parameters
PARAMS = {
    "chunk_size": 800,        # caracteres por chunk
    "overlap": 150,           # solapamiento entre chunks
    "min_chunk_size": 200,    # mínimo para no tener trozos inútiles
}

# Postgres config
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "opositaia")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

# Input/Output directories
INPUT_DIR = "/home/spas/OPOS_GEMINI_1/data/boe_xml"


def clean_html(text: str) -> str:
    """Limpia etiquetas HTML y entidades del texto."""
    if not text:
        return ""
    
    # Unescape HTML entities
    text = unescape(text)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    
    # Fix multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def validate_encoding(text: str) -> bool:
    """Verifica que no hay caracteres rotos (encoding malo)."""
    bad_patterns = ['Ã¡', 'Ã©', 'Ã­', 'Ã³', 'Ãº', 'Ã±', 'Â¡', 'Â¿', 'â€']
    return not any(p in text for p in bad_patterns)


def find_sentence_boundary(text: str, position: int, direction: str = "forward") -> int:
    """
    Busca el fin de frase más cercano a la posición dada.
    direction: "forward" busca hacia adelante, "backward" hacia atrás.
    """
    sentence_endings = ['. ', '.\n', '? ', '?\n', '! ', '!\n', ':\n', ')\n']
    
    if direction == "forward":
        search_range = range(position, min(position + 100, len(text)))
        for i in search_range:
            for ending in sentence_endings:
                if text[i:i+len(ending)] == ending:
                    return i + 1  # Include the period/punct
        return min(position + 50, len(text))  # Fallback
    else:
        search_range = range(position, max(position - 100, 0), -1)
        for i in search_range:
            for ending in sentence_endings:
                if i >= len(ending) and text[i-len(ending)+1:i+1] == ending:
                    return i + 1
        return max(position - 50, 0)


def chunk_text_with_overlap(text: str, chunk_size: int = 800, overlap: int = 150) -> List[Tuple[str, int]]:
    """
    Divide texto en chunks con solapamiento, respetando límites de oraciones.
    Returns: Lista de (chunk_text, chunk_index)
    """
    if len(text) <= chunk_size:
        return [(text, 0)]
    
    chunks = []
    start = 0
    chunk_index = 0
    
    while start < len(text):
        # Determine end position
        end = start + chunk_size
        
        if end >= len(text):
            # Last chunk
            chunk = text[start:].strip()
            if len(chunk) >= PARAMS["min_chunk_size"]:
                chunks.append((chunk, chunk_index))
            break
        
        # Find sentence boundary near the end
        boundary = find_sentence_boundary(text, end, "forward")
        chunk = text[start:boundary].strip()
        
        if len(chunk) >= PARAMS["min_chunk_size"]:
            chunks.append((chunk, chunk_index))
            chunk_index += 1
        
        # Move start with overlap
        start = boundary - overlap
        if start < 0:
            start = 0
    
    return chunks


def extract_articles_from_json(data: Dict, boe_id: str) -> List[Dict]:
    """
    Extrae artículos desde la estructura del JSON del BOE.
    Estructura real: data.texto.bloque[n].version.p[m]._text
    """
    articles = []
    
    # Get basic metadata
    metadata = data.get("data", {}).get("metadatos", {})
    titulo_ley = metadata.get("titulo", {}).get("_text", boe_id)
    url_html = metadata.get("url_html_consolidada", {}).get("_text", "")
    fecha_vigencia = metadata.get("fecha_vigencia", {}).get("_text", "")
    departamento = metadata.get("departamento", {}).get("_text", "")
    
    # Get bloques from texto
    texto_data = data.get("data", {}).get("texto", {})
    bloques = texto_data.get("bloque", [])
    
    if not bloques:
        logger.warning(f"⚠️  {boe_id}: No se encontraron bloques")
        return articles
    
    # Ensure bloques is a list
    if isinstance(bloques, dict):
        bloques = [bloques]
    
    # Process each bloque
    for bloque in bloques:
        if not isinstance(bloque, dict):
            continue
        
        bloque_id = bloque.get("id", "unknown")
        tipo = bloque.get("tipo", "")
        
        # Get version (can be dict or list of versions)
        version = bloque.get("version", {})
        
        # If version is a list, take the first one (most recent)
        if isinstance(version, list):
            if len(version) > 0:
                version = version[0]
            else:
                continue
        
        if not isinstance(version, dict):
            continue
        
        # Get paragraphs from version
        parrafos = version.get("p", [])
        
        # Ensure parrafos is a list
        if isinstance(parrafos, dict):
            parrafos = [parrafos]
        
        # Extract text from all paragraphs
        contenido_parts = []
        titulo_bloque = f"Bloque {bloque_id}"
        
        for p in parrafos:
            if isinstance(p, dict):
                texto = p.get("_text", "")
                clase = p.get("class", "")
                
                # If it's an article class, get title from first paragraph
                if clase in ["articulo", "titulo"] and texto:
                    titulo_bloque = texto
                
                if texto:
                    contenido_parts.append(clean_html(texto))
            elif isinstance(p, str):
                contenido_parts.append(clean_html(p))
        
        # Join all content
        contenido = " ".join(contenido_parts)
        
        # Skip if too short
        if len(contenido) < 50:
            continue
        
        # Validate encoding
        if not validate_encoding(contenido):
            logger.warning(f"⚠️  {boe_id}/{bloque_id}: Encoding issues detected")
        
        articles.append({
            "article_id": bloque_id,
            "title": titulo_bloque[:200],  # Truncate if too long
            "content": contenido,
            "law_title": titulo_ley,
            "url_html": url_html,
            "fecha_vigencia": fecha_vigencia,
            "departamento": departamento,
            "tipo": tipo
        })
    
    return articles


def process_law_file(filepath: str) -> Tuple[Dict, List[Dict]]:
    """
    Procesa un archivo JSON de ley y devuelve:
    - catalog_entry: Datos para leyes_catalogo
    - chunks: Lista de chunks para tabla laws
    """
    boe_id = os.path.basename(filepath).replace(".json", "")
    
    logger.info(f"📄 Procesando: {boe_id}")
    
    # Load JSON
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract metadata for catalog
    metadata = data.get("data", {}).get("metadatos", {})
    
    catalog_entry = {
        "boe_id": boe_id,
        "titulo": metadata.get("titulo", {}).get("_text", boe_id),
        "rango": metadata.get("rango", {}).get("_text", ""),
        "fecha_publicacion": metadata.get("fecha_publicacion", {}).get("_text", ""),
        "fecha_entrada_vigor": metadata.get("fecha_vigencia", {}).get("_text", ""),
        "url_html_consolidada": metadata.get("url_html_consolidada", {}).get("_text", ""),
        "departamento_nombre": metadata.get("departamento", {}).get("_text", ""),
        "vigente": metadata.get("estatus_derogacion", {}).get("_text", "") != "S",
    }
    
    # Extract articles
    articles = extract_articles_from_json(data, boe_id)
    logger.info(f"   → Encontrados {len(articles)} artículos/bloques")
    
    # Chunk each article
    all_chunks = []
    
    for article in articles:
        content = article["content"]
        article_id = article["article_id"]
        article_title = article["title"]
        
        # Chunk the article
        text_chunks = chunk_text_with_overlap(
            content, 
            PARAMS["chunk_size"], 
            PARAMS["overlap"]
        )
        
        for chunk_text, chunk_index in text_chunks:
            chunk_id = str(uuid.uuid4())
            
            # Determine layer
            if len(text_chunks) == 1:
                layer = "article_full"
            else:
                layer = "article_chunk"
            
            all_chunks.append({
                "id": chunk_id,
                "law_id": boe_id,
                "law_name": catalog_entry["titulo"][:100],  # Truncate if too long
                "article_id": article_id,
                "title": f"{article_title} (Chunk {chunk_index})" if chunk_index > 0 else article_title,
                "content": chunk_text,
                "chunk_index": chunk_index,
                "has_overlap": chunk_index > 0,
                "layer": layer,
            })
    
    logger.info(f"   → Generados {len(all_chunks)} chunks")
    
    return catalog_entry, all_chunks


def insert_to_database(catalog_entries: List[Dict], all_chunks: List[Dict]):
    """
    Inserta los datos en PostgreSQL.
    """
    logger.info("📥 Insertando en PostgreSQL...")
    
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD,
        options="-c client_encoding=UTF8"
    )
    cursor = conn.cursor()
    
    # Insert catalog entries
    logger.info(f"   Insertando {len(catalog_entries)} leyes en leyes_catalogo...")
    
    for entry in catalog_entries:
        try:
            cursor.execute("""
                INSERT INTO leyes_catalogo (boe_id, titulo, tipo_norma, 
                    departamento_nombre, vigente, url_html)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (boe_id) DO UPDATE SET
                    titulo = EXCLUDED.titulo,
                    url_html = EXCLUDED.url_html
            """, (
                entry["boe_id"],
                entry["titulo"],
                entry["rango"],
                entry.get("departamento_nombre"),
                entry.get("vigente", True),
                entry.get("url_html_consolidada")
            ))
        except Exception as e:
            logger.error(f"   Error insertando {entry['boe_id']}: {e}")
    
    conn.commit()
    logger.info("   ✅ Catálogo insertado")
    
    # Insert chunks
    logger.info(f"   Insertando {len(all_chunks)} chunks en laws...")
    
    batch_size = 100
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i:i+batch_size]
        for chunk in batch:
            try:
                cursor.execute("""
                    INSERT INTO laws (id, law_id, law_name, title, content)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """, (
                    chunk["id"],
                    chunk["law_id"],
                    chunk["law_name"],
                    chunk["title"],
                    chunk["content"]
                ))
            except Exception as e:
                logger.error(f"   Error insertando chunk: {e}")
        
        conn.commit()
        print(f"\r   Insertados {min(i + batch_size, len(all_chunks))}/{len(all_chunks)} chunks...", end="", flush=True)
    
    print("")
    conn.close()
    logger.info("   ✅ Chunks insertados")


def main():
    """Main function."""
    logger.info("🚀 Iniciando procesamiento de leyes...")
    
    # Get all JSON files
    json_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.json') and not f.startswith('_')]
    logger.info(f"📁 Encontrados {len(json_files)} archivos JSON")
    
    all_catalog_entries = []
    all_chunks = []
    
    for filename in sorted(json_files):
        filepath = os.path.join(INPUT_DIR, filename)
        try:
            catalog_entry, chunks = process_law_file(filepath)
            all_catalog_entries.append(catalog_entry)
            all_chunks.extend(chunks)
        except Exception as e:
            logger.error(f"❌ Error procesando {filename}: {e}")
            continue
    
    logger.info(f"\n{'='*60}")
    logger.info(f"📊 RESUMEN:")
    logger.info(f"   Leyes procesadas: {len(all_catalog_entries)}")
    logger.info(f"   Chunks generados: {len(all_chunks)}")
    
    # Insert to database
    insert_to_database(all_catalog_entries, all_chunks)
    
    logger.info(f"\n✅ PROCESAMIENTO COMPLETADO")


if __name__ == "__main__":
    main()
