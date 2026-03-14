#!/usr/bin/env python3
import sys
import logging
from qdrant_client import QdrantClient
from qdrant_client.http import models

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "opositaia_knowledge_FULL_XML"

BASURA = [
    "BOE-A-1982-9050", "BOE-A-1985-22915", "BOE-A-1988-9526", "BOE-A-1995-2081",
    "BOE-A-1995-24156", "BOE-A-2001-20795", "BOE-A-2006-16891", "BOE-A-2006-19348",
    "BOE-A-2008-17156", "BOE-A-2009-3780", "BOE-A-2009-5693", "BOE-A-2020-6898",
    "BOE-A-2022-7260", "BOE-A-2023-25411", "BOE-A-2023-6945", "BOE-A-2011-15673", 
    "BOE-A-2020-2047", "BOE-A-1995-10652", "BOE-A-1995-10653", "BOE-A-2010-1172"
]

def purgar_basura():
    client = QdrantClient(url=QDRANT_URL)
    logger.info("=========================================")
    logger.info("1. PURGANDO LEYES BASURA DEL RAG (Qdrant)")
    logger.info("=========================================")
    for bad_id in BASURA:
        try:
            client.delete(
                collection_name=COLLECTION_NAME,
                points_selector=models.Filter(
                    must=[models.FieldCondition(key="boe_id", match=models.MatchValue(value=bad_id))]
                )
            )
            logger.info(f"✅ Eliminado de Qdrant permanentemente: {bad_id}")
        except Exception as e:
            logger.error(f"Error borrando {bad_id}: {e}")

if __name__ == "__main__":
    purgar_basura()
