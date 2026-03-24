"""
populate_neo4j_from_qdrant.py
Lee todos los puntos de opositaia_knowledge_FULL_XML (Qdrant)
y crea nodos + relaciones en Neo4j (bolt://localhost:7687).
Ejecución: python backend/scripts/populate_neo4j_from_qdrant.py
"""
import sys
import os
import logging
from qdrant_client import QdrantClient
from neo4j import GraphDatabase
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Intentamos cargar .env si es necesario para variables, aunque el roadmap
# especifica de momento usar configuraciones por defecto / hardcoded para local.
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
except ImportError:
    pass

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION = "opositaia_knowledge_FULL_XML"
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASSWORD", "opositaia2026")

def main():
    try:
        qdrant = QdrantClient(url=QDRANT_URL)
        logger.info(f"Conectado a Qdrant en {QDRANT_URL}")
    except Exception as e:
        logger.error(f"Error conectando a Qdrant: {e}")
        return

    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
        logger.info(f"Conectado a Neo4j en {NEO4J_URI}")
    except Exception as e:
        logger.error(f"Error conectando a Neo4j: {e}")
        return

    offset = None
    batch_size = 100
    total = 0
    relaciones_derogadas = 0

    with driver.session() as session:
        # Crear índice único para evitar duplicados en Articulo y Ley
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (a:Articulo) REQUIRE a.id IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (l:Ley) REQUIRE l.id IS UNIQUE")
        
        # Iterar sobre todo Qdrant
        while True:
            # Scroll usando la API de qdrant_client
            results, offset = qdrant.scroll(
                collection_name=COLLECTION,
                limit=batch_size,
                offset=offset,
                with_payload=True
            )
            
            if not results:
                break
                
            for point in results:
                p = point.payload
                article_id = p.get("article_id") or p.get("precepto") or f"{p.get('boe_id', 'NO_BOE')}_{p.get('article_number', 'NO_ART')}"
                
                if article_id == "NO_BOE_NO_ART":
                    continue
                
                # Para cruzar SS y AGE usar etiqueta triple
                labels = "Articulo:SS:AGE"
                
                # Crear nodo artículo
                session.run(f"""
                    MERGE (a:{labels} {{id: $id}})
                    SET a.title = $title,
                        a.texto = $texto,
                        a.ley = $ley,
                        a.boe_id = $boe_id,
                        a.vigente = $vigente,
                        a.fecha_vigencia = $fecha_vigencia,
                        a.url_boe = $url_boe
                """, {
                    "id": article_id,
                    "title": p.get("article_title") or p.get("title") or article_id,
                    "texto": (p.get("text_snippet") or p.get("text") or "")[:1000],  # Limitar texto para grafo ligero
                    "ley": p.get("law_name") or p.get("law_title") or "",
                    "boe_id": p.get("boe_id", ""),
                    "vigente": p.get("vigente", True),
                    "fecha_vigencia": p.get("fecha_vigencia", ""),
                    "url_boe": p.get("url_boe") or p.get("url", ""),
                })
                
                ley_title = p.get("law_name") or p.get("law_title")
                # Crear nodo de Ley y relación PERTENECE_A
                if ley_title:
                    session.run(f"""
                        MERGE (l:Ley {{id: $ley_id}})
                        SET l.titulo = $ley_id
                        WITH l
                        MATCH (a:{labels} {{id: $art_id}})
                        MERGE (a)-[:PERTENECE_A]->(l)
                    """, {
                        "ley_id": ley_title,
                        "art_id": article_id
                    })
                
                # Crear relación DEROGADO_POR si existe
                if p.get("derogated_by"):
                    session.run(f"""
                        MATCH (a:Articulo {{id: $derogado_id}})
                        MERGE (nuevo:Articulo {{id: $nuevo_id}})
                        MERGE (a)-[:DEROGADO_POR]->(nuevo)
                    """, {
                        "derogado_id": article_id,
                        "nuevo_id": p.get("derogated_by")
                    })
                    relaciones_derogadas += 1
                
                # Crear relaciones MODIFICA_A / MODIFICADO_POR
                if p.get("modifies"):
                    for mod in p.get("modifies", []):
                        session.run(f"""
                            MATCH (a:Articulo {{id: $id}})
                            MERGE (target:Articulo {{id: $mod_id}})
                            MERGE (a)-[:MODIFICA_A]->(target)
                        """, {
                            "id": article_id,
                            "mod_id": mod
                        })
                
                total += 1
                
            logger.info(f"Procesados {total} artículos...")
            
            if offset is None:
                break

    driver.close()
    logger.info(f"✅ Población completada. Nodos Articulo: {total}. Relaciones DEROGADO_POR: {relaciones_derogadas}")

if __name__ == "__main__":
    main()
