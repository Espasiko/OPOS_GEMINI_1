#!/usr/bin/env python3
"""
ingest_neo4j_v15.py — Re-ingestión Limpia Neo4j (Neo4j-ONLY, sin Qdrant)

Fuente de Verdad Legal SS (Bloque Específico C1/A2)
- Lee catalog_boe_verified_20260303.json
- PURGE total de Neo4j (sin backup)
- Para cada ley: obtiene XML de API BOE (o HTML scraping como fallback)
- Crea nodos :Ley, :Precepto:Articulo, :Precepto:Disposicion
- Calcula embeddings (pablosi/bge-m3-spa-law-qa-trained-2, 1024 dims)
- Guarda embeddings en propiedad `embedding` del nodo Neo4j
- Crea índice vectorial nativo Neo4j 5.x
- Checkpoint cada 5 leyes → permite reanudar con --resume

Uso:
  python ingest_neo4j_v15.py                   # Ingestión completa (PURGE + ingest)
  python ingest_neo4j_v15.py --resume           # Reanudar desde checkpoint
  python ingest_neo4j_v15.py --dry-run          # Solo parsear, no escribir en Neo4j
  python ingest_neo4j_v15.py --skip-purge       # Ingestar sin borrar datos previos
  python ingest_neo4j_v15.py --only-law BOE-A-2015-11724  # Solo una ley
"""

import os
import sys
import json
import logging
import argparse
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field, asdict

import numpy as np

# Configuración de Logging
LOG_FILE = Path(__file__).parent / "ingest_v15.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Rutas
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent.resolve()
BACKEND_DIR = PROJECT_ROOT / "backend"
DATA_DIR = BACKEND_DIR / "data"
CATALOG_FILE = DATA_DIR / "catalog_FINAL_v2.json"
CHECKPOINT_FILE = DATA_DIR / "ingest_v15_checkpoint.json"

sys.path.append(str(BACKEND_DIR))

# Configuración
EMBEDDING_MODEL_NAME = "pablosi/bge-m3-spa-law-qa-trained-2"
EMBEDDING_DIM = 1024
MAX_TOKENS_PER_CHUNK = 8000  # si artículo excede, chunking
CHUNK_OVERLAP_TOKENS = 200
BOE_API_DELAY = 1.0  # seconds between XML API requests
HTML_SCRAPE_DELAY = 2.0  # seconds between HTML scraping requests
BATCH_SIZE_EMBEDDINGS = 32
CHECKPOINT_EVERY_N_LAWS = 5

# Mapeo BOE ID → Siglas canónicas (del plan)
SIGLAS_MAP = {
    "BOE-A-2015-11724": "TRLGSS",
    "BOE-A-1978-31229": "CE",
    "BOE-A-1996-4447": "RD 84/1996",
    "BOE-A-1996-1579": "RD 2064/1995",
    "BOE-A-2004-11836": "RD 1415/2004",
    "BOE-A-2009-15442": "RD 1430/2009",
    "BOE-A-2014-7684": "RD 625/2014",
    "BOE-A-2009-4724": "RD 295/2009",
    "BOE-A-2011-13119": "RD 1148/2011",
    "BOE-A-1995-19848": "RD 1300/1995",
    "BOE-A-2002-23038": "RD 1132/2002",
    "BOE-A-2005-19151": "RD 1335/2005",
    "BOE-A-1991-7270": "RD 357/1991",
    "BOE-A-2021-21007": "Ley 19/2021 IMV",
    "BOE-A-1985-8124": "RD 625/1985 Desempleo",
    "BOE-A-2015-11719": "EBEP",
    "BOE-A-2015-11430": "ET",
    "BOE-A-2007-13409": "LETA",
    "BOE-A-2022-12482": "RDL 13/2022",
    "BOE-A-1995-24292": "Ley 31/1995 PRL",
    "BOE-A-1997-1853": "RD 39/1997",
    "BOE-A-2000-323": "LEC",
    # ── 21 leyes nuevas (ingestión 30/03/2026) ──
    "BOE-A-1972-944": "Decreto 1646/1972",
    "BOE-A-1973-282": "Decreto 298/1973",
    "BOE-A-1966-21116": "Decreto 3158/1966",
    "BOE-A-1970-1000": "Decreto 2530/1970",
    "BOE-A-1992-24743": "RD 1221/1992",
    "BOE-A-1997-24163": "RD 1647/1997",
    "BOE-A-2003-19281": "Orden TAS/2865/2003",
    "BOE-A-2003-19458": "RD 1273/2003",
    "BOE-A-2003-23401": "RD 1539/2003",
    "BOE-A-2006-22169": "RD 1299/2006",
    "BOE-A-2006-22865": "Ley 42/2006",
    "BOE-A-2007-9690": "RD 615/2007",
    "BOE-A-2007-21092": "Ley 40/2007",
    "BOE-A-2015-11346": "Ley 47/2015 Mar",
    "BOE-A-2018-10397": "RD 900/2018",
    "BOE-A-1999-15681": "Ley 27/1999 Cooperativas",
    "BOE-A-2022-14630": "LO 10/2022",
    "BOE-A-2000-15060": "LISOS",
    "BOE-A-2024-10237": "RD 501/2024",
    "BOE-A-2025-3780": "Orden PJC/178/2025",
    "BOE-A-2025-8567": "Ley 2/2025",
}

# Regex para extraer número de artículo (incluido bis/ter/quater/quinquies/sexies/septies/octies)
RE_ARTICULO = re.compile(
    r'(?:Art[íi]culo|Art\.?)\s*(\d+(?:\.\d+)?)\s*(bis|ter|quater|quinquies|sexies|septies|octies)?',
    re.IGNORECASE
)

# Regex para disposiciones
RE_DISPOSICION = re.compile(
    r'Disposici[óo]n\s+(adicional|transitoria|final|derogatoria)\s+'
    r'(primera|segunda|tercera|cuarta|quinta|sexta|séptima|octava|novena|décima|'
    r'undécima|duodécima|decimotercera|decimocuarta|decimoquinta|decimosexta|'
    r'decimoséptima|decimoctava|decimonovena|vigésima|vigésimo\s*primera|'
    r'vigésimo\s*segunda|vigésimo\s*tercera|vigésimo\s*cuarta|vigésimo\s*quinta|'
    r'vigésimo\s*sexta|vigésimo\s*séptima|vigésimo\s*octava|vigésimo\s*novena|'
    r'trigésima|trigésimo\s*primera|trigésimo\s*segunda|trigésimo\s*tercera|'
    r'cuadragésima|quincuagésima|sexagésima|septuagésima|octogésima|'
    r'nonagésima|centésima|única|1ª|2ª|3ª|4ª|5ª|6ª|7ª|8ª|9ª|10ª|'
    r'\d+ª)',
    re.IGNORECASE
)

RE_DISPOSICION_UNICA = re.compile(
    r'Disposici[óo]n\s+(adicional|transitoria|final|derogatoria)\s*(única)?',
    re.IGNORECASE
)


# =============================================================================
# Data classes
# =============================================================================

@dataclass
class PreceptoData:
    """Datos de un precepto (artículo o disposición) para insertar en Neo4j."""
    id_canonico: str
    title: str
    texto: str
    ley_id: str
    ley_siglas: str
    vigente: bool = True
    fecha_vigencia: str = "2026-03-03"
    url_boe: str = ""
    source: str = "BOE_XML_v15"
    # Artículo
    numero: str = ""
    sufijo: str = ""
    # Disposición
    tipo_disposicion: str = ""  # adicional | transitoria | final | derogatoria
    ordinal: str = ""
    # Embedding (set later)
    embedding: Optional[List[float]] = None
    # Node type
    es_disposicion: bool = False


@dataclass
class LeyData:
    """Datos de una ley para insertar en Neo4j."""
    boe_id: str
    titulo: str
    siglas: str
    tipo: str = ""
    fecha_pub: str = ""
    fecha_consolidacion: str = ""
    num_articulos_boe: int = 0
    num_disposiciones_boe: int = 0
    historica: bool = False
    tiene_xml_api: bool = True


@dataclass
class Checkpoint:
    """Estado de checkpoint para reanudar ingestión."""
    completed_boe_ids: List[str] = field(default_factory=list)
    completed_count: int = 0
    failed: List[str] = field(default_factory=list)
    timestamp: str = ""


# =============================================================================
# Neo4j connection
# =============================================================================

class Neo4jConnection:
    """Wrapper for Neo4j driver."""

    def __init__(self, uri: str, user: str, password: str):
        try:
            from neo4j import GraphDatabase
        except ImportError:
            logger.error("❌ neo4j driver not installed. Run: pip install neo4j")
            sys.exit(1)
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        # Test connection
        with self.driver.session() as session:
            result = session.run("RETURN 1 AS n")
            assert result.single()["n"] == 1
        logger.info(f"✅ Conectado a Neo4j: {uri}")

    def close(self):
        self.driver.close()

    def purge(self):
        """PURGE TOTAL — borra todo."""
        with self.driver.session() as session:
            result = session.run("MATCH (n) RETURN count(n) AS cnt")
            cnt = result.single()["cnt"]
            logger.warning(f"⚠️  PURGE: Borrando {cnt} nodos...")
            session.run("MATCH (n) DETACH DELETE n")
        logger.info("✅ PURGE completado — Neo4j vacío.")

    def create_constraints_and_indexes(self):
        """Crea constraints e índices necesarios."""
        with self.driver.session() as session:
            # Constraint de unicidad para Ley
            session.run(
                "CREATE CONSTRAINT ley_boe_id IF NOT EXISTS "
                "FOR (l:Ley) REQUIRE l.boe_id IS UNIQUE"
            )
            # Constraint de unicidad para Precepto
            session.run(
                "CREATE CONSTRAINT precepto_id IF NOT EXISTS "
                "FOR (p:Precepto) REQUIRE p.id IS UNIQUE"
            )
            logger.info("✅ Constraints creados.")

    def create_vector_index(self):
        """Crea índice vectorial nativo Neo4j 5.x."""
        with self.driver.session() as session:
            session.run("""
                CREATE VECTOR INDEX precepto_embedding IF NOT EXISTS
                FOR (p:Precepto) ON p.embedding
                OPTIONS {indexConfig: {
                    `vector.dimensions`: $dims,
                    `vector.similarity_function`: 'cosine'
                }}
            """, dims=EMBEDDING_DIM)
        logger.info(f"✅ Vector index 'precepto_embedding' creado ({EMBEDDING_DIM} dims, cosine).")

    def insert_ley(self, ley: LeyData):
        """Inserta un nodo :Ley."""
        with self.driver.session() as session:
            session.run("""
                MERGE (l:Ley {boe_id: $boe_id})
                SET l.titulo = $titulo,
                    l.siglas = $siglas,
                    l.tipo = $tipo,
                    l.fecha_pub = $fecha_pub,
                    l.fecha_consolidacion = $fecha_consolidacion,
                    l.num_articulos_boe = $num_articulos_boe,
                    l.num_disposiciones_boe = $num_disposiciones_boe,
                    l.tiene_xml_api = $tiene_xml_api,
                    l.historica = $historica
            """, boe_id=ley.boe_id, titulo=ley.titulo, siglas=ley.siglas,
                tipo=ley.tipo, fecha_pub=ley.fecha_pub,
                fecha_consolidacion=ley.fecha_consolidacion,
                num_articulos_boe=ley.num_articulos_boe,
                num_disposiciones_boe=ley.num_disposiciones_boe,
                tiene_xml_api=ley.tiene_xml_api,
                historica=ley.historica)

    def insert_preceptos_batch(self, preceptos: List[PreceptoData]):
        """Inserta batch de preceptos con embeddings y relación a Ley."""
        if not preceptos:
            return

        with self.driver.session() as session:
            for p in preceptos:
                labels = ":Precepto:Disposicion" if p.es_disposicion else ":Precepto:Articulo"

                # Build properties dict
                props = {
                    "id": p.id_canonico,
                    "title": p.title,
                    "texto": p.texto,
                    "ley_id": p.ley_id,
                    "ley_siglas": p.ley_siglas,
                    "vigente": p.vigente,
                    "fecha_vigencia": p.fecha_vigencia,
                    "url_boe": p.url_boe,
                    "source": p.source,
                }

                if p.es_disposicion:
                    props["tipo_disposicion"] = p.tipo_disposicion
                    props["ordinal"] = p.ordinal
                else:
                    props["numero"] = p.numero
                    props["sufijo"] = p.sufijo

                if p.embedding:
                    props["embedding"] = p.embedding

                # Use MERGE to be idempotent
                query = f"""
                    MERGE (p{labels} {{id: $props.id}})
                    SET p += $props
                    WITH p
                    MATCH (l:Ley {{boe_id: $ley_boe_id}})
                    MERGE (p)-[:PERTENECE_A]->(l)
                """
                session.run(query, props=props, ley_boe_id=p.ley_id)

    def get_stats(self) -> Dict:
        """Obtiene estadísticas de la BD."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (l:Ley) WITH count(l) AS leyes
                MATCH (a:Articulo) WITH leyes, count(a) AS articulos
                MATCH (d:Disposicion) WITH leyes, articulos, count(d) AS disposiciones
                MATCH (p:Precepto) WHERE p.embedding IS NOT NULL
                WITH leyes, articulos, disposiciones, count(p) AS con_embedding
                RETURN leyes, articulos, disposiciones, con_embedding
            """)
            row = result.single()
            return {
                "leyes": row["leyes"],
                "articulos": row["articulos"],
                "disposiciones": row["disposiciones"],
                "con_embedding": row["con_embedding"]
            }


# =============================================================================
# Embedding model
# =============================================================================

class EmbeddingEngine:
    """Manages the sentence-transformer model for legal embeddings."""

    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME):
        from sentence_transformers import SentenceTransformer
        logger.info(f"🔄 Cargando modelo embeddings: {model_name}")
        self.model = SentenceTransformer(model_name)
        logger.info(f"✅ Modelo cargado. Dimensiones: {self.model.get_sentence_embedding_dimension()}")

    def encode_texts(self, texts: List[str]) -> List[List[float]]:
        """Encode multiple texts, returns list of float lists."""
        embeddings = self.model.encode(texts, show_progress_bar=False, batch_size=BATCH_SIZE_EMBEDDINGS)
        return [emb.tolist() for emb in embeddings]

    def encode_single(self, text: str) -> List[float]:
        """Encode single text, with chunking if too long."""
        # Rough token estimate: ~4 chars per token for Spanish
        estimated_tokens = len(text) / 4
        if estimated_tokens <= MAX_TOKENS_PER_CHUNK:
            return self.model.encode(text).tolist()

        # Chunk and mean-pool
        chunks = self._chunk_text(text)
        if not chunks:
            return self.model.encode(text[:MAX_TOKENS_PER_CHUNK * 4]).tolist()

        chunk_embeddings = self.model.encode(chunks, batch_size=BATCH_SIZE_EMBEDDINGS)
        mean_embedding = np.mean(chunk_embeddings, axis=0)
        # Normalize
        norm = np.linalg.norm(mean_embedding)
        if norm > 0:
            mean_embedding = mean_embedding / norm
        return mean_embedding.tolist()

    def _chunk_text(self, text: str) -> List[str]:
        """Split text into chunks with overlap for mean pooling."""
        chars_per_chunk = MAX_TOKENS_PER_CHUNK * 4  # rough estimate
        overlap_chars = CHUNK_OVERLAP_TOKENS * 4
        chunks = []
        start = 0
        while start < len(text):
            end = start + chars_per_chunk
            chunk = text[start:end]
            if chunk.strip():
                chunks.append(chunk.strip())
            start = end - overlap_chars
            if start < 0:
                start = 0
        return chunks


# =============================================================================
# BOE XML parser
# =============================================================================

def extract_article_info(title: str) -> Tuple[str, str]:
    """Extract article number and suffix (bis/ter/etc) from title.
    Returns (numero, sufijo)."""
    m = RE_ARTICULO.search(title)
    if m:
        return m.group(1), (m.group(2) or "").lower()
    return "", ""


def extract_disposicion_info(title: str) -> Tuple[str, str]:
    """Extract tipo and ordinal from disposición title.
    Returns (tipo_disposicion, ordinal)."""
    m = RE_DISPOSICION.search(title)
    if m:
        return m.group(1).lower(), m.group(2).lower().strip()

    # Try "única"
    m2 = RE_DISPOSICION_UNICA.search(title)
    if m2:
        tipo = m2.group(1).lower()
        unica = (m2.group(2) or "").lower().strip()
        return tipo, unica if unica else "única"

    return "", ""


def build_canonical_id(title: str, ley_siglas: str) -> Tuple[str, bool]:
    """Build canonical ID from title and ley siglas.
    Returns (id_canonico, es_disposicion)."""

    # Check if it's a disposición
    tipo_disp, ordinal = extract_disposicion_info(title)
    if tipo_disp:
        abbrevs = {
            "adicional": "DA",
            "transitoria": "DT",
            "final": "DF",
            "derogatoria": "DD",
        }
        abbr = abbrevs.get(tipo_disp, tipo_disp.upper())
        # Convert ordinal to short form
        ordinal_short = ordinal_to_short(ordinal)
        return f"{abbr} {ordinal_short} {ley_siglas}", True

    # Check if it's an artículo
    numero, sufijo = extract_article_info(title)
    if numero:
        sufijo_str = f" {sufijo}" if sufijo else ""
        return f"Art. {numero}{sufijo_str} {ley_siglas}", False

    # Fallback: use sanitized title
    clean = re.sub(r'[^a-zA-Z0-9áéíóúñÁÉÍÓÚÑ\s]', '', title)[:50].strip()
    return f"{clean} {ley_siglas}", False


def ordinal_to_short(ordinal: str) -> str:
    """Convert ordinal text to short form: 'primera' -> '1ª', 'única' -> 'única'."""
    ordinal = ordinal.strip().lower()
    ordinals_map = {
        "primera": "1ª", "segunda": "2ª", "tercera": "3ª", "cuarta": "4ª",
        "quinta": "5ª", "sexta": "6ª", "séptima": "7ª", "octava": "8ª",
        "novena": "9ª", "décima": "10ª", "undécima": "11ª", "duodécima": "12ª",
        "decimotercera": "13ª", "decimocuarta": "14ª", "decimoquinta": "15ª",
        "decimosexta": "16ª", "decimoséptima": "17ª", "decimoctava": "18ª",
        "decimonovena": "19ª", "vigésima": "20ª",
        "vigésimo primera": "21ª", "vigésimo segunda": "22ª",
        "vigésimo tercera": "23ª", "vigésimo cuarta": "24ª",
        "vigésimo quinta": "25ª", "vigésimo sexta": "26ª",
        "vigésimo séptima": "27ª", "vigésimo octava": "28ª",
        "vigésimo novena": "29ª", "trigésima": "30ª",
        "trigésimo primera": "31ª", "trigésimo segunda": "32ª",
        "trigésimo tercera": "33ª",
        "cuadragésima": "40ª", "quincuagésima": "50ª",
        "sexagésima": "60ª", "septuagésima": "70ª",
        "octogésima": "80ª", "nonagésima": "90ª", "centésima": "100ª",
        "única": "única",
    }
    # Normalize whitespace
    ordinal_normalized = re.sub(r'\s+', ' ', ordinal)
    if ordinal_normalized in ordinals_map:
        return ordinals_map[ordinal_normalized]
    # If already short form like "1ª"
    if re.match(r'\d+ª$', ordinal):
        return ordinal
    return ordinal if ordinal else "única"


def parse_xml_bloques(xml_text: str, boe_id: str, ley_siglas: str) -> List[PreceptoData]:
    """Parse BOE XML text and extract all preceptos (artículos + disposiciones)."""
    preceptos = []

    try:
        root = ET.fromstring(xml_text.encode('utf-8'))
    except ET.ParseError as e:
        logger.error(f"  ❌ Error parseando XML para {boe_id}: {e}")
        return preceptos

    # Try <bloque> elements first (modern format)
    bloques = root.findall('.//bloque')
    if not bloques:
        # Try <articulo> elements (old format)
        bloques = root.findall('.//articulo')

    for node in bloques:
        tipo_bloque = node.get('tipo', '')
        titulo_raw = node.get('titulo', '')

        # Only process preceptos and disposiciones
        if tipo_bloque and tipo_bloque not in ('precepto', 'disposicion'):
            continue

        # Skip empty titles
        if not titulo_raw:
            # For old format <articulo>, try to get title from child
            title_elem = node.find('./titulo')
            if title_elem is not None:
                titulo_raw = "".join(title_elem.itertext()).strip()
            if not titulo_raw:
                continue

        # Determine if this is an artículo or disposición
        is_articulo = bool(RE_ARTICULO.search(titulo_raw))
        is_disposicion = bool(
            re.search(r'disposici[óo]n', titulo_raw, re.IGNORECASE)
        )

        # Skip items that are neither
        if not is_articulo and not is_disposicion:
            # Could be a section header (Título, Capítulo, etc.) - skip
            if re.match(r'(T[íi]tulo|Cap[íi]tulo|Secci[óo]n|Pre[áa]mbulo|Exposici[óo]n|ANEXO)',
                       titulo_raw, re.IGNORECASE):
                continue
            # For old-format articles without clear title pattern
            num_elem = node.find('./num')
            if num_elem is not None and num_elem.text:
                is_articulo = True
                titulo_raw = f"Artículo {num_elem.text.strip()}"

        if not is_articulo and not is_disposicion:
            continue

        # Extract text from latest version
        versiones = node.findall('./version')
        if versiones:
            version_actual = versiones[-1]
            p_elems = version_actual.findall('.//p')
            if p_elems:
                texto = "\n".join(["".join(p.itertext()).strip() for p in p_elems])
            else:
                texto = "".join(version_actual.itertext()).strip()
        else:
            # Old format: text directly in <articulo>
            p_elems = node.findall('./p')
            if p_elems:
                texto = "\n".join(["".join(p.itertext()).strip() for p in p_elems])
            else:
                texto = "".join(node.itertext()).strip()

        # Clean text
        texto = re.sub(r'\s+', ' ', texto).strip()
        if len(texto) < 15:
            continue

        # Build canonical ID
        id_canonico, es_disp = build_canonical_id(titulo_raw, ley_siglas)

        # Check vigencia
        vigente = True
        vig_elem = node.find('./vigencia_texto')
        if versiones:
            vig_elem = vig_elem or versiones[-1].find('./vigencia_texto')
        if vig_elem is not None:
            vig_text = "".join(vig_elem.itertext()).strip().lower()
            if "derogad" in vig_text or "sin efecto" in vig_text:
                vigente = False

        # Build precepto
        p = PreceptoData(
            id_canonico=id_canonico,
            title=titulo_raw,
            texto=texto,
            ley_id=boe_id,
            ley_siglas=ley_siglas,
            vigente=vigente,
            fecha_vigencia="2026-03-03",
            url_boe=f"https://www.boe.es/buscar/act.php?id={boe_id}",
            source="BOE_XML_v15",
            es_disposicion=es_disp,
        )

        if is_disposicion or es_disp:
            tipo_disp, ordinal = extract_disposicion_info(titulo_raw)
            p.tipo_disposicion = tipo_disp
            p.ordinal = ordinal
            p.es_disposicion = True
        else:
            numero, sufijo = extract_article_info(titulo_raw)
            p.numero = numero
            p.sufijo = sufijo

        preceptos.append(p)

    return preceptos


# =============================================================================
# Checkpoint management
# =============================================================================

def load_checkpoint() -> Checkpoint:
    """Load checkpoint from file."""
    if CHECKPOINT_FILE.exists():
        with open(CHECKPOINT_FILE, 'r') as f:
            data = json.load(f)
        return Checkpoint(
            completed_boe_ids=data.get("completed_boe_ids", []),
            completed_count=data.get("completed_count", 0),
            failed=data.get("failed", []),
            timestamp=data.get("timestamp", "")
        )
    return Checkpoint()


def save_checkpoint(cp: Checkpoint):
    """Save checkpoint to file."""
    cp.timestamp = datetime.now().isoformat()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(asdict(cp), f, indent=2, ensure_ascii=False)
    logger.info(f"💾 Checkpoint guardado: {cp.completed_count} leyes completadas.")


# =============================================================================
# Main ingest logic
# =============================================================================

def load_catalog(catalog_file: Path = CATALOG_FILE) -> List[Dict]:
    """Load the verified BOE catalog."""
    if not catalog_file.exists():
        logger.error(f"❌ Catálogo no encontrado: {catalog_file}")
        sys.exit(1)
    with open(catalog_file, 'r') as f:
        catalog = json.load(f)
    logger.info(f"📂 Catálogo cargado ({catalog_file.name}): {len(catalog)} leyes.")
    return catalog


def get_siglas(boe_id: str, catalog_entry: Dict) -> str:
    """Get canonical siglas for a BOE ID."""
    if boe_id in SIGLAS_MAP:
        return SIGLAS_MAP[boe_id]
    # Use catalog siglas if not the boe_id itself
    cat_siglas = catalog_entry.get("siglas", "")
    if cat_siglas and cat_siglas != boe_id:
        return cat_siglas
    return boe_id


def fetch_xml_text(boe_id: str) -> Optional[str]:
    """Fetch XML text from BOE API with retry."""
    from agents.boe_api_client import BOEApiClient

    max_retries = 5
    delay = BOE_API_DELAY

    for attempt in range(max_retries):
        try:
            with BOEApiClient(timeout=60) as client:
                xml_text = client.get_texto_consolidado(boe_id)
            if xml_text and len(xml_text) > 100:
                return xml_text
            else:
                logger.warning(f"  ⚠️ XML vacío o muy corto para {boe_id}")
                return None
        except Exception as e:
            status_code = getattr(getattr(e, 'response', None), 'status_code', None)
            if status_code == 404:
                logger.warning(f"  ⚠️ 404 — {boe_id} no tiene XML API.")
                return None
            if status_code in (429, 503):
                wait = delay * (2 ** attempt)
                logger.warning(f"  ⏳ {status_code} — retry {attempt+1}/{max_retries} en {wait}s...")
                time.sleep(wait)
                continue
            logger.error(f"  ❌ Error fetching XML for {boe_id} (attempt {attempt+1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(delay * (2 ** attempt))
            continue

    return None


def run_ingest(args):
    """Main ingest function."""

    # 1. Load catalog
    catalog_path = Path(args.catalog) if args.catalog else CATALOG_FILE
    catalog = load_catalog(catalog_path)

    # Filter by --only-law if specified
    if args.only_law:
        catalog = [c for c in catalog if c["boe_id"] == args.only_law]
        if not catalog:
            logger.error(f"❌ Ley {args.only_law} no encontrada en catálogo.")
            sys.exit(1)

    # 2. Connect to Neo4j
    neo4j_uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user = os.environ.get("NEO4J_USER", "neo4j")
    neo4j_pass = os.environ.get("NEO4J_PASSWORD", "opositaia2026")

    if args.dry_run:
        logger.info("🔍 DRY RUN — no se escribirá en Neo4j.")
        db = None
    else:
        db = Neo4jConnection(neo4j_uri, neo4j_user, neo4j_pass)

    # 3. PURGE (unless --skip-purge or --resume)
    if not args.dry_run and not args.skip_purge and not args.resume:
        logger.warning("🚨 PURGE TOTAL — Borrando TODA la base de datos Neo4j...")
        db.purge()
        db.create_constraints_and_indexes()

    # 4. Load checkpoint if --resume
    checkpoint = Checkpoint()
    if args.resume:
        checkpoint = load_checkpoint()
        logger.info(f"🔄 Reanudando desde checkpoint: {checkpoint.completed_count} leyes ya completadas.")
    elif not args.dry_run:
        # Fresh start: create constraints
        if args.skip_purge:
            db.create_constraints_and_indexes()

    # 5. Load embedding model
    if not args.skip_embeddings:
        embedder = EmbeddingEngine()
    else:
        embedder = None
        logger.info("⏭️ Embeddings desactivados (--skip-embeddings).")

    # 6. Process each law
    total_preceptos = 0
    processed_count = 0

    for i, entry in enumerate(catalog):
        boe_id = entry["boe_id"]

        # Skip if already completed (resume mode)
        if boe_id in checkpoint.completed_boe_ids:
            logger.info(f"  ⏭️ {boe_id} ya completado — saltando.")
            continue

        siglas = get_siglas(boe_id, entry)
        titulo = entry.get("titulo", "")
        logger.info(f"\n{'='*60}")
        logger.info(f"[{i+1}/{len(catalog)}] 📜 {boe_id} ({siglas})")
        logger.info(f"  {titulo[:80]}...")

        # 6a. Create :Ley node
        ley = LeyData(
            boe_id=boe_id,
            titulo=titulo,
            siglas=siglas,
            tipo=entry.get("tipo", ""),
            num_articulos_boe=entry.get("num_articulos_boe", 0),
            num_disposiciones_boe=entry.get("num_disposiciones_boe", 0),
            tiene_xml_api=entry.get("tiene_xml_api", True),
            historica=entry.get("historica", False),
        )

        if not args.dry_run:
            db.insert_ley(ley)

        # 6b. Fetch XML
        if not entry.get("tiene_xml_api", True):
            logger.warning(f"  ⚠️ {boe_id} sin XML API — marcando como fallido.")
            checkpoint.failed.append(boe_id)
            continue

        xml_text = fetch_xml_text(boe_id)
        if not xml_text:
            logger.warning(f"  ⚠️ No se pudo obtener XML para {boe_id}.")
            checkpoint.failed.append(boe_id)
            time.sleep(BOE_API_DELAY)
            continue

        # 6c. Parse XML into preceptos
        preceptos = parse_xml_bloques(xml_text, boe_id, siglas)
        logger.info(f"  📋 Parseados: {len(preceptos)} preceptos "
                     f"(arts={sum(1 for p in preceptos if not p.es_disposicion)}, "
                     f"disps={sum(1 for p in preceptos if p.es_disposicion)})")

        if not preceptos:
            logger.warning(f"  ⚠️ 0 preceptos extraídos de {boe_id}.")
            checkpoint.failed.append(boe_id)
            checkpoint.completed_boe_ids.append(boe_id)
            checkpoint.completed_count += 1
            time.sleep(BOE_API_DELAY)
            continue

        # 6d. Generate embeddings
        if embedder and not args.skip_embeddings:
            logger.info(f"  🧠 Generando embeddings para {len(preceptos)} preceptos...")
            texts = [p.texto for p in preceptos]
            # Process in batches
            for batch_start in range(0, len(texts), BATCH_SIZE_EMBEDDINGS):
                batch_texts = texts[batch_start:batch_start + BATCH_SIZE_EMBEDDINGS]
                batch_embeddings = []
                for t in batch_texts:
                    emb = embedder.encode_single(t)
                    batch_embeddings.append(emb)
                for j, emb in enumerate(batch_embeddings):
                    preceptos[batch_start + j].embedding = emb
            logger.info(f"  ✅ Embeddings generados.")

        # 6e. Insert into Neo4j
        if not args.dry_run:
            db.insert_preceptos_batch(preceptos)
            logger.info(f"  ✅ {len(preceptos)} preceptos insertados en Neo4j.")
        else:
            logger.info(f"  🔍 (dry-run) Se habrían insertado {len(preceptos)} preceptos.")

        total_preceptos += len(preceptos)
        processed_count += 1
        checkpoint.completed_boe_ids.append(boe_id)
        checkpoint.completed_count += 1

        # 6f. Checkpoint every N laws
        if not args.dry_run and processed_count % CHECKPOINT_EVERY_N_LAWS == 0:
            save_checkpoint(checkpoint)

        # Rate limiting
        time.sleep(BOE_API_DELAY)

    # 7. Final checkpoint
    if not args.dry_run:
        save_checkpoint(checkpoint)

    # 8. Create vector index
    if not args.dry_run and not args.skip_embeddings:
        db.create_vector_index()

    # 9. Print summary
    logger.info(f"\n{'='*60}")
    logger.info(f"🚀 INGESTIÓN COMPLETADA")
    logger.info(f"  Leyes procesadas: {processed_count}")
    logger.info(f"  Preceptos totales: {total_preceptos}")
    logger.info(f"  Fallidas: {len(checkpoint.failed)} → {checkpoint.failed}")

    if not args.dry_run and db:
        stats = db.get_stats()
        logger.info(f"\n📊 ESTADÍSTICAS Neo4j:")
        logger.info(f"  Leyes:        {stats['leyes']}")
        logger.info(f"  Artículos:    {stats['articulos']}")
        logger.info(f"  Disposiciones:{stats['disposiciones']}")
        logger.info(f"  Con embedding:{stats['con_embedding']}")
        db.close()


def main():
    # Load .env
    try:
        from dotenv import load_dotenv
        env_file = BACKEND_DIR / ".env.backend"
        if env_file.exists():
            load_dotenv(env_file)
            logger.info(f"📂 .env cargado: {env_file}")
    except ImportError:
        pass

    parser = argparse.ArgumentParser(
        description="ingest_neo4j_v15.py — Re-ingestión Limpia Neo4j (Neo4j-ONLY)"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Solo parsear XML, no escribir en Neo4j")
    parser.add_argument("--resume", action="store_true",
                        help="Reanudar desde checkpoint anterior")
    parser.add_argument("--skip-purge", action="store_true",
                        help="No borrar datos existentes")
    parser.add_argument("--skip-embeddings", action="store_true",
                        help="No generar embeddings (insertar sin vectores)")
    parser.add_argument("--only-law", type=str, default=None,
                        help="Solo procesar una ley específica (BOE ID)")
    parser.add_argument("--catalog", type=str, default=None,
                        help="Ruta al archivo JSON de catálogo personalizado")
    args = parser.parse_args()

    run_ingest(args)


if __name__ == "__main__":
    main()
