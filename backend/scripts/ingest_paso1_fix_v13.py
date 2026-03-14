#!/usr/bin/env python3
import time
import uuid
import logging
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "opositaia_knowledge_FULL_XML"
EMBEDDING_MODEL = "pablosi/bge-m3-spa-law-qa-trained-2"

def main():
    qdrant = QdrantClient(url=QDRANT_URL)
    model = SentenceTransformer(EMBEDDING_MODEL)

    # chunks a inyectar manual
    chunks = [
        {
            "boe_id": "BOE-A-2023-6945",
            "law_name": "RDL 2/2023 (DT 34ª jubilación)",
            "article_title": "Disposición transitoria trigésima cuarta TRLGSS",
            "text_snippet": "Disposición transitoria trigésima cuarta TRLGSS. Cálculo de la base reguladora de la pensión de jubilación. A partir del 1 de enero de 2026, la base reguladora será el cociente que resulte de dividir por 352,33 la suma de las 302 bases de cotización de mayor cuantía comprendidas dentro de los 304 meses inmediatamente anteriores al mes previo al del hecho causante."
        },
        {
            "boe_id": "BOE-A-2004-11836",
            "law_name": "RD 1415/2004 (Reglamento Recaudación SS)",
            "article_title": "Artículo 33. Garantías.",
            "text_snippet": "Artículo 33. Garantías. 4. No se exigirán garantías para la concesión de aplazamientos o fraccionamientos cuando el solicitante sea una de las Administraciones públicas o un organismo o entidad de derecho público estatal, autonómico o local."
        },
        {
            "boe_id": "BOE-A-2004-11836",
            "law_name": "RD 1415/2004 (Reglamento Recaudación SS)",
            "article_title": "Artículo 39. Procedimiento de deducción.",
            "text_snippet": "Artículo 39. Procedimiento de deducción. 1. El procedimiento de recadudación por deducción será de aplicación a las entidades que integran el sector público, que incluye las Administraciones Públicas, quedando excluidas del procedimiento ordinario de apremio."
        },
        {
            "boe_id": "BOE-A-2004-11836",
            "law_name": "RD 1415/2004 (Reglamento Recaudación SS)",
            "article_title": "Artículo 80. Bienes gananciales.",
            "text_snippet": "Artículo 80. Embargo de bienes gananciales. Cuando se proceda al embargo de bienes rústicos o urbanos cuya titularidad conste en el Registro de la Propiedad como gananciales, se notificará obligatoriamente el embargo al cónyuge del deudor, bajo pena de nulidad del procedimiento."
        },
        {
            "boe_id": "BOE-A-2004-11836",
            "law_name": "RD 1415/2004 (Reglamento Recaudación SS)",
            "article_title": "Artículo 103. Tipo de enajenación.",
            "text_snippet": "Artículo 103. Tipo de enajenación para la subasta. Para la fijación final del tipo de enajenación (precio de salida en subasta), se descontarán irremediablemente del valor de tasación del bien embargado el importe de todas las cargas, gravámenes o derechos anteriores y preferentes, no descontándose jamás las posteriores."
        }
    ]

    points = []
    for i, c in enumerate(chunks):
        dense = model.encode(c["text_snippet"]).tolist()
        payload = {
            "boe_id": c["boe_id"],
            "law_name": c["law_name"],
            "article_title": c["article_title"],
            "text_snippet": c["text_snippet"],
            "layer": "article_chunk",
            "vigente": True
        }
        pt_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"FORCED_{c['boe_id']}_{i}"))
        points.append(models.PointStruct(id=pt_id, vector={"dense": dense, "text": {"indices":[], "values":[]}}, payload=payload))

    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
    logger.info(f"✅ Se han inyectado {len(points)} chunks forzados con éxito en la colección.")

if __name__ == "__main__":
    main()
