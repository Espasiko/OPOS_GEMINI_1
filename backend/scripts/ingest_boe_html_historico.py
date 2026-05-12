#!/usr/bin/env python3
"""
Parser e ingestor de versiones históricas del BOE vía HTML + BeautifulSoup.

El visor HTML del BOE soporta ?p=YYYYMMDD para versiones históricas:
  https://www.boe.es/buscar/act.php?id=BOE-A-XXXX&p=YYYYMMDD

Este script extrae artículos de esa versión HTML y los ingesta/actualiza en Neo4j,
útil para fijar el contenido legal a la fecha de corte del examen (04/03/2026).

Uso:
  python ingest_boe_html_historico.py --fecha 20260304 --boe-ids BOE-A-2015-10566,BOE-A-2016-7935
  python ingest_boe_html_historico.py --fecha 20260304 --catalog backend/data/catalog_v17.json
  python ingest_boe_html_historico.py --fecha 20260304 --boe-ids BOE-A-2015-10566 --dry-run
"""

import os
import re
import sys
import json
import time
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# ── Neo4j (opcional — solo si se usa --ingest) ────────────────────────────────
try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False

# ── Configuración ─────────────────────────────────────────────────────────────
BASE_DIR     = Path(__file__).resolve().parent.parent.parent
DATA_DIR     = BASE_DIR / "backend" / "data"
OUTPUT_DIR   = DATA_DIR / "html_historico_output"
CATALOG_FILE = DATA_DIR / "catalog_v17.json"

NEO4J_URI   = os.getenv("NEO4J_URI",  "bolt://localhost:7687")
NEO4J_USER  = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS  = os.getenv("NEO4J_PASS", "opositaia2026")

BOE_HTML_URL = "https://www.boe.es/buscar/act.php"
DELAY_BETWEEN_LAWS = 3   # segundos entre leyes (respetar rate limit BOE)
REQUEST_TIMEOUT    = 30  # segundos

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# ── HTTP Session ──────────────────────────────────────────────────────────────
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
})


# ─────────────────────────────────────────────────────────────────────────────
# FETCHER
# ─────────────────────────────────────────────────────────────────────────────

def fetch_html(boe_id: str, fecha: str) -> Optional[str]:
    """
    Descarga la versión HTML histórica de una ley.
    fecha: YYYYMMDD
    """
    params = {"id": boe_id, "p": fecha}
    try:
        resp = SESSION.get(BOE_HTML_URL, params=params, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        # Detectar redireccionados a versión sin fecha (= no existe esa fecha)
        if "No se ha encontrado" in resp.text or "página no encontrada" in resp.text.lower():
            logger.warning(f"  ⚠️  {boe_id}@{fecha}: página no encontrada")
            return None
        return resp.text
    except requests.RequestException as e:
        logger.error(f"  ❌ Error descargando {boe_id}@{fecha}: {e}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
# PARSER
# ─────────────────────────────────────────────────────────────────────────────

# IDs de bloques que NO son artículos del articulado propiamente dicho
SKIP_IDS = {"co", "preambulo", "tpreliminar", "ci", "tabs", "textoxslt"}

# Regex para extraer número de artículo
RE_ART_NUM = re.compile(r"art[íi]culo\s+(\d+[\w\-\.]*)", re.IGNORECASE)
RE_DISP    = re.compile(r"disposici[oó]n\s+(adicional|transitoria|derogatoria|final)\s+(\w+\.?)", re.IGNORECASE)


def _extract_block_number(block_id: str, titulo: str) -> str:
    """Extrae número/clave del bloque para usarlo como 'numero' en Neo4j."""
    # a1 → "1", a12bis → "12bis"
    m = re.match(r'^a(\d+.*)$', block_id)
    if m:
        return m.group(1)
    # da → "DA", dt1 → "DT1", dd → "DD", df1 → "DF1"
    prefix_map = {'da': 'DA', 'dt': 'DT', 'dd': 'DD', 'df': 'DF'}
    for prefix, label in prefix_map.items():
        if block_id.startswith(prefix):
            suffix = block_id[len(prefix):]
            return f"{label}{suffix}" if suffix else label
    # Fallback: usar título si tiene número
    m2 = RE_ART_NUM.search(titulo)
    if m2:
        return m2.group(1)
    return block_id


def parse_law_html(html: str, boe_id: str, fecha: str) -> Dict:
    """
    Parsea el HTML histórico del BOE y devuelve estructura con preceptos.

    Returns:
      {
        "boe_id": str,
        "fecha": str,
        "titulo": str,
        "fecha_consolidacion": str,
        "preceptos": [
          {"id": str, "numero": str, "titulo": str, "texto": str}
        ],
        "num_preceptos": int,
        "warnings": [str]
      }
    """
    soup = BeautifulSoup(html, "html.parser")
    warnings = []

    # ── Título de la ley ──────────────────────────────────────────────────────
    titulo_tag = soup.find("h2") or soup.find("h1", id=re.compile(r"titulo|title", re.I))
    titulo = titulo_tag.get_text(strip=True) if titulo_tag else "Sin título"

    # ── Fecha de consolidación mostrada ──────────────────────────────────────
    cons_text = ""
    for tag in soup.find_all(string=re.compile(r"consolidado|actualización", re.I)):
        cons_text = str(tag).strip()
        break

    # ── Extraer todos los bloques div.bloque ─────────────────────────────────
    bloques = soup.find_all("div", class_="bloque")
    preceptos = []

    for bloque in bloques:
        block_id = bloque.get("id", "")
        if not block_id or block_id in SKIP_IDS:
            continue
        # Solo artículos (a1, a2...) y disposiciones (da, dt, dd, df, da1...)
        if not re.match(r'^(a\d|da|dt|dd|df)', block_id):
            continue

        # Título del precepto: h5.articulo o h3/h4/h5 genérico
        titulo_el = (
            bloque.find("h5", class_="articulo")
            or bloque.find("h5")
            or bloque.find("h4")
            or bloque.find("h3")
        )
        titulo_precepto = titulo_el.get_text(strip=True) if titulo_el else block_id

        # Texto: todos los <p class="parrafo"> o <p> (excluir metainfo [Bloque N: ...])
        parrafos = []
        for p in bloque.find_all("p"):
            txt = p.get_text(strip=True)
            if not txt or re.match(r'^\[Bloque \d+:', txt):
                continue
            parrafos.append(txt)

        texto = "\n".join(parrafos).strip()
        if not texto:
            warnings.append(f"Bloque {block_id} sin texto extraíble")
            continue

        numero = _extract_block_number(block_id, titulo_precepto)

        preceptos.append({
            "id":     block_id,
            "numero": numero,
            "titulo": titulo_precepto,
            "texto":  texto,
        })

    if not preceptos:
        warnings.append("No se extrajeron preceptos — revisar estructura HTML")

    return {
        "boe_id":              boe_id,
        "fecha":               fecha,
        "titulo":              titulo,
        "fecha_consolidacion": cons_text,
        "preceptos":           preceptos,
        "num_preceptos":       len(preceptos),
        "warnings":            warnings,
    }


# ─────────────────────────────────────────────────────────────────────────────
# NEO4J UPDATER  (opcional)
# ─────────────────────────────────────────────────────────────────────────────

class Neo4jUpdater:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def upsert_precepto(self, boe_id: str, siglas: str, precepto: Dict):
        """Actualiza el texto de un Precepto existente a la versión histórica."""
        query = """
        MATCH (p:Precepto)
        WHERE p.ley_siglas = $siglas
          AND (p.numero = $numero OR p.id = $pid)
        SET p.texto               = $texto,
            p.titulo              = $titulo,
            p.fecha_html_historico = $fecha
        RETURN count(p) AS updated
        """
        with self.driver.session() as s:
            res = s.run(query, {
                "siglas":  siglas,
                "numero":  precepto["numero"],
                "pid":     precepto["id"],
                "texto":   precepto["texto"],
                "titulo":  precepto["titulo"],
                "fecha":   precepto.get("fecha", ""),
            }).single()
            return res["updated"] if res else 0

    def get_siglas(self, boe_id: str) -> Optional[str]:
        with self.driver.session() as s:
            r = s.run("MATCH (l:Ley {boe_id: $id}) RETURN l.siglas AS s LIMIT 1",
                      {"id": boe_id}).single()
            return r["s"] if r else None


# ─────────────────────────────────────────────────────────────────────────────
# MAIN PROCESSING
# ─────────────────────────────────────────────────────────────────────────────

def process_law(boe_id: str, fecha: str, output_dir: Path,
                dry_run: bool, updater: Optional["Neo4jUpdater"]) -> Dict:
    """Procesa una ley: descarga HTML, parsea, guarda JSON, opcionalmente ingesta."""
    logger.info(f"  📥 {boe_id}  @{fecha}")

    stats = {
        "boe_id":       boe_id,
        "fecha":        fecha,
        "ok":           False,
        "num_preceptos": 0,
        "updated_neo4j": 0,
        "warnings":     [],
        "errors":       [],
    }

    # 1. Descargar HTML
    html = fetch_html(boe_id, fecha)
    if not html:
        stats["errors"].append("No se pudo descargar el HTML")
        return stats

    # 2. Parsear
    result = parse_law_html(html, boe_id, fecha)
    stats["num_preceptos"] = result["num_preceptos"]
    stats["warnings"]      = result["warnings"]

    if not result["preceptos"]:
        stats["errors"].append("Sin preceptos extraídos")
        return stats

    logger.info(f"    ✅ {result['num_preceptos']} preceptos  |  {result['titulo'][:60]}")
    if result["warnings"]:
        for w in result["warnings"][:3]:
            logger.warning(f"    ⚠️  {w}")

    # 3. Guardar JSON de salida
    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)
        out_file = output_dir / f"{boe_id.replace('-','_')}_{fecha}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        logger.info(f"    💾 Guardado: {out_file.name}")

    # 4. Actualizar Neo4j (opcional)
    if updater and not dry_run:
        siglas = updater.get_siglas(boe_id)
        if siglas:
            n_updated = 0
            for prec in result["preceptos"]:
                n = updater.upsert_precepto(boe_id, siglas, prec)
                n_updated += n
            stats["updated_neo4j"] = n_updated
            logger.info(f"    🗄️  Neo4j: {n_updated} preceptos actualizados ({siglas})")
        else:
            stats["warnings"].append(f"Ley {boe_id} no encontrada en Neo4j — no se actualizó")

    stats["ok"] = True
    return stats


def load_boe_ids_from_catalog(catalog_path: Path) -> List[str]:
    with open(catalog_path) as f:
        cat = json.load(f)
    return [l["boe_id"] for l in cat.get("leyes", []) if l.get("tiene_xml", False)]


def main():
    parser = argparse.ArgumentParser(
        description="Ingestor BOE HTML histórico con BeautifulSoup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("--fecha",    required=True,
                        help="Fecha de la versión histórica YYYYMMDD (ej: 20260304)")
    parser.add_argument("--boe-ids",  default="",
                        help="BOE IDs separados por coma (ej: BOE-A-2015-10566,BOE-A-2016-7935)")
    parser.add_argument("--catalog",  default="",
                        help="Usar todos los IDs del catálogo JSON")
    parser.add_argument("--output",   default=str(OUTPUT_DIR),
                        help=f"Directorio de salida JSON (default: {OUTPUT_DIR})")
    parser.add_argument("--ingest",   action="store_true",
                        help="Actualizar preceptos en Neo4j con el texto histórico")
    parser.add_argument("--dry-run",  action="store_true",
                        help="Solo parsear, no guardar ni actualizar Neo4j")
    parser.add_argument("--delay",    type=float, default=DELAY_BETWEEN_LAWS,
                        help=f"Segundos entre peticiones (default: {DELAY_BETWEEN_LAWS})")
    parser.add_argument("--neo4j-uri",  default=NEO4J_URI)
    parser.add_argument("--neo4j-user", default=NEO4J_USER)
    parser.add_argument("--neo4j-pass", default=NEO4J_PASS)
    args = parser.parse_args()

    # Validar fecha
    if not re.match(r'^\d{8}$', args.fecha):
        logger.error("--fecha debe ser YYYYMMDD (ej: 20260304)")
        sys.exit(1)

    # Construir lista de BOE IDs
    boe_ids: List[str] = []
    if args.boe_ids:
        boe_ids = [x.strip() for x in args.boe_ids.split(",") if x.strip()]
    elif args.catalog:
        boe_ids = load_boe_ids_from_catalog(Path(args.catalog))
        logger.info(f"📚 Cargados {len(boe_ids)} IDs del catálogo {args.catalog}")
    else:
        logger.error("Debes especificar --boe-ids o --catalog")
        sys.exit(1)

    logger.info(f"🗓️  Fecha objetivo: {args.fecha}")
    logger.info(f"📋 Leyes a procesar: {len(boe_ids)}")
    if args.dry_run:
        logger.info("🔍 DRY-RUN — no se guardará ni actualizará nada")

    # Neo4j
    updater = None
    if args.ingest:
        if not NEO4J_AVAILABLE:
            logger.error("neo4j driver no instalado: pip install neo4j")
            sys.exit(1)
        updater = Neo4jUpdater(args.neo4j_uri, args.neo4j_user, args.neo4j_pass)
        logger.info(f"🗄️  Neo4j conectado: {args.neo4j_uri}")

    # Procesar
    output_dir = Path(args.output)
    all_stats  = []
    t_start    = time.time()

    for i, boe_id in enumerate(boe_ids, 1):
        logger.info(f"\n[{i}/{len(boe_ids)}] {boe_id}")
        st = process_law(boe_id, args.fecha, output_dir, args.dry_run, updater)
        all_stats.append(st)

        if i < len(boe_ids):
            time.sleep(args.delay)

    if updater:
        updater.close()

    # Resumen
    elapsed = time.time() - t_start
    ok      = sum(1 for s in all_stats if s["ok"])
    fail    = len(all_stats) - ok
    precs   = sum(s["num_preceptos"] for s in all_stats)
    neo4j_u = sum(s.get("updated_neo4j", 0) for s in all_stats)

    print("\n" + "="*65)
    print(f"✅  OK:         {ok}/{len(all_stats)}")
    print(f"❌  Fallidos:   {fail}")
    print(f"📄  Preceptos:  {precs}")
    if args.ingest:
        print(f"🗄️   Neo4j upd:  {neo4j_u}")
    print(f"⏱️   Tiempo:     {elapsed:.1f}s")
    if not args.dry_run:
        print(f"📁  Salida:     {output_dir}")
    print("="*65)

    # Guardar resumen
    if not args.dry_run:
        summary_file = output_dir / f"summary_{args.fecha}.json"
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump({
                "fecha": args.fecha,
                "timestamp": datetime.now().isoformat(),
                "stats": {
                    "ok": ok, "fail": fail,
                    "total_preceptos": precs,
                    "neo4j_updated": neo4j_u,
                    "elapsed_s": round(elapsed, 1)
                },
                "results": all_stats
            }, f, indent=2, ensure_ascii=False)
        logger.info(f"📊 Resumen: {summary_file}")

    # Mostrar fallos
    failed = [s for s in all_stats if not s["ok"]]
    if failed:
        print("\n⚠️  FALLOS:")
        for s in failed:
            print(f"  {s['boe_id']}: {'; '.join(s['errors'])}")


if __name__ == "__main__":
    main()
