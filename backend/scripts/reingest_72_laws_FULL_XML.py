#!/usr/bin/env python3
import os
import sys
import hashlib
import requests
import pickle
import re
import json
import uuid
import time
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, SparseVector, VectorParams, Distance, SparseVectorParams, OptimizersConfigDiff
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from typing import Dict, List, Optional
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
EMBEDDING_MODEL = "pablosi/bge-m3-spa-law-qa-trained-2"
EMBEDDING_DIM = 1024
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "opositaia_knowledge_FULL_XML"
BM25_VOCAB_PATH = Path("/home/spas/OPOS_GEMINI_1/backend/data/bm25_vocab.pkl")

# Fusión de las leyes (61 base + 21 missing - duplicados = 72+ leyes)
raw_leyes = [
    {"boe_id": "BOE-A-1978-31229", "nombre": "Constitución Española 1978"},
    {"boe_id": "BOE-A-1979-23709", "nombre": "LO 2/1979 Tribunal Constitucional"},
    {"boe_id": "BOE-A-1981-7118", "nombre": "LO 3/1981 Defensor del Pueblo"},
    {"boe_id": "BOE-A-1985-12666", "nombre": "LO 6/1985 Poder Judicial"},
    {"boe_id": "BOE-A-1997-25336", "nombre": "Ley 50/1997 del Gobierno"},
    {"boe_id": "BOE-A-1997-7878", "nombre": "LO 6/1997 LOFAGE"},
    {"boe_id": "BOE-A-1985-5392", "nombre": "Ley 7/1985 Bases Régimen Local"},
    {"boe_id": "BOE-A-2013-13756", "nombre": "Ley 27/2013 Racionalización Admin"},
    {"boe_id": "BOE-A-2015-10565", "nombre": "Ley 39/2015 PAC"},
    {"boe_id": "BOE-A-2015-10566", "nombre": "Ley 40/2015 LRJSP"},
    {"boe_id": "BOE-A-1998-16718", "nombre": "Ley 29/1998 Contencioso-Administrativo"},
    {"boe_id": "BOE-A-2015-11719", "nombre": "EBEP RDL 5/2015"},
    {"boe_id": "BOE-A-1984-17387", "nombre": "Ley 30/1984 Reforma Función Pública"},
    {"boe_id": "BOE-A-2007-6115", "nombre": "LO 3/2007 Igualdad Mujeres Hombres"},
    {"boe_id": "BOE-A-2004-21760", "nombre": "LO 1/2004 Violencia de Género"},
    {"boe_id": "BOE-A-2023-5366", "nombre": "Ley 4/2023 LGTBI"},
    {"boe_id": "BOE-A-2006-21990", "nombre": "Ley 39/2006 Dependencia"},
    {"boe_id": "BOE-A-2013-12632", "nombre": "RDL 1/2013 Derechos Discapacidad"},
    {"boe_id": "BOE-A-2018-16673", "nombre": "LO 3/2018 LOPDGDD"},
    {"boe_id": "BOE-A-2013-12887", "nombre": "Ley 19/2013 Transparencia"},
    {"boe_id": "BOE-A-2007-12352", "nombre": "Ley 11/2007 Acceso Electrónico"},
    {"boe_id": "BOE-A-2010-1330", "nombre": "RD 3/2010 ENI"},
    {"boe_id": "BOE-A-2010-1331", "nombre": "RD 4/2010 ENS"},
    {"boe_id": "BOE-A-2017-12902", "nombre": "Ley 9/2017 Contratos Sector Público"},
    {"boe_id": "BOE-A-2003-20977", "nombre": "Ley 38/2003 General Subvenciones"},
    {"boe_id": "BOE-A-2006-13371", "nombre": "RD 887/2006 Reglamento Subvenciones"},
    {"boe_id": "BOE-A-2003-21614", "nombre": "Ley 47/2003 General Presupuestaria"},
    {"boe_id": "BOE-A-2012-5730", "nombre": "LO 2/2012 Estabilidad Presupuestaria"},
    {"boe_id": "BOE-A-1982-9050", "nombre": "LO 2/1982 Tribunal de Cuentas"},
    {"boe_id": "BOE-A-1988-9526", "nombre": "Ley 7/1988 Funcionamiento TC"},
    {"boe_id": "BOE-A-2015-11430", "nombre": "Estatuto Trabajadores RDL 2/2015"},
    {"boe_id": "BOE-A-1995-24292", "nombre": "Ley 31/1995 PRL"},
    {"boe_id": "BOE-A-1997-1853", "nombre": "RD 39/1997 Servicios Prevención"},
    {"boe_id": "BOE-A-1999-23945", "nombre": "RD 1971/1999 Accidentes Trabajo"},
    {"boe_id": "BOE-A-2002-18099", "nombre": "Orden TAS/2926/2002 Enfermedades Prof"},
    {"boe_id": "BOE-A-2015-11724", "nombre": "LGSS RDL 8/2015"},
    {"boe_id": "BOE-A-1996-4447", "nombre": "RD 84/1996 Afiliación"},
    {"boe_id": "BOE-A-2022-7260", "nombre": "RD 504/2022 Modifica Afiliación"},
    {"boe_id": "BOE-A-1996-1579", "nombre": "RD 2064/1995 Cotización"},
    {"boe_id": "BOE-A-2004-11836", "nombre": "RD 1415/2004 Recaudación"},
    {"boe_id": "BOE-A-1996-1074", "nombre": "RD 1694/1995 Hacienda Patrimonio SS"},
    {"boe_id": "BOE-A-2009-5693", "nombre": "RD 1430/2009 Control IT"},
    {"boe_id": "BOE-A-1995-24156", "nombre": "RD 1300/1995 Incapacidades"},
    {"boe_id": "BOE-A-2006-19348", "nombre": "RD 1369/2006 Revisión Incapacidad"},
    {"boe_id": "BOE-A-2001-20795", "nombre": "RD 1415/2001 IP Accidente"},
    {"boe_id": "BOE-A-2009-3780", "nombre": "RD 295/2009 Maternidad Paternidad"},
    {"boe_id": "BOE-A-2009-15931", "nombre": "Ley 9/2009 Nacimiento Adopción"},
    {"boe_id": "BOE-A-2019-3244", "nombre": "RDL 6/2019 Igualdad Empleo"},
    {"boe_id": "BOE-A-2024-26917", "nombre": "RDL 11/2024 Mejora Pensiones"},
    {"boe_id": "BOE-A-2011-13242", "nombre": "Ley 27/2011 Modernización SS"},
    {"boe_id": "BOE-A-1995-2081", "nombre": "RD 2274/1994 Jubilación Supervivencia"},
    {"boe_id": "BOE-A-2006-16891", "nombre": "RD 1112/2006 Prescripción"},
    {"boe_id": "BOE-A-2008-17156", "nombre": "RD 1646/2008 Actualización Pensiones"},
    {"boe_id": "BOE-A-2020-6898", "nombre": "RDL 20/2020 IMV Provisional"},
    {"boe_id": "BOE-A-2021-21007", "nombre": "Ley 19/2021 IMV Definitivo"},
    {"boe_id": "BOE-A-1986-2012", "nombre": "RD 2670/1985 PNC"},
    {"boe_id": "BOE-A-1985-22915", "nombre": "RD 2617/1985 Trabajadores Mar"},
    {"boe_id": "BOE-A-2023-25411", "nombre": "RD 1009/2023 Estructura Ministerios"},
    {"boe_id": "BOE-A-2025-26605", "nombre": "Orden HAC/1517/2025 (Umbrales SARA 2026)"},
    {"boe_id": "BOE-A-2000-12140", "nombre": "MUFACE RDL 4/2000"},
    {"boe_id": "BOE-A-2003-7527", "nombre": "MUFACE Reglamento"},
    # LEYES FALTANTES DEL SCRIPTS
    {"boe_id": "BOE-A-2021-21007", "nombre": "Ley 19/2021 Ingreso Mínimo Vital (IMV)"},
    {"boe_id": "BOE-A-2014-7684", "nombre": "RD 625/2014 Gestión Incapacidad Temporal"},
    {"boe_id": "BOE-A-2000-323", "nombre": "Ley 1/2000 Enjuiciamiento Civil (LEC)"},
    {"boe_id": "BOE-A-2021-5032", "nombre": "RD 203/2021 Reglamento Actuación Sector Público Electrónico"},
    {"boe_id": "BOE-A-2007-13409", "nombre": "Ley 20/2007 Estatuto del Trabajo Autónomo (LETA)"},
    {"boe_id": "BOE-A-2011-15673", "nombre": "Ley 36/2011 Reguladora de la Jurisdicción Social"},
    {"boe_id": "BOE-A-2022-7191", "nombre": "RD 311/2022 Esquema Nacional de Seguridad (ENS)"},
    {"boe_id": "BOE-A-1987-16764", "nombre": "RDL 670/1987 Clases Pasivas del Estado"},
    {"boe_id": "BOE-A-2020-2047", "nombre": "RD 139/2020 Estructura Orgánica AGE"},
    {"boe_id": "BOE-A-2010-1172", "nombre": "RD 4/2010 Esquema Nacional de Interoperabilidad (ENI)"},
    {"boe_id": "BOE-A-1985-16660", "nombre": "LO 11/1985 Libertad Sindical"},
    {"boe_id": "BOE-A-1987-14115", "nombre": "Ley 9/1987 Representación AAPP"},
    {"boe_id": "BOE-A-2007-19814", "nombre": "Ley 37/2007 Reutilización información base"},
    {"boe_id": "BOE-A-2010-11409", "nombre": "STC 31/2010 Estatut Cataluña"},
    {"boe_id": "BOE-A-1991-7270", "nombre": "RD 357/1991 Pensiones No Contributivas"},
    {"boe_id": "BOE-A-2011-13119", "nombre": "RD 1148/2011 Cuidado Menores Enfermedad Grave"},
    {"boe_id": "BOE-A-2015-8168", "nombre": "Ley 23/2015 Ordenadora Inspección Trabajo"},
    {"boe_id": "BOE-A-1995-10652", "nombre": "RD 364/1995 Reglamento Ingreso Personal AGE"},
    {"boe_id": "BOE-A-1995-10653", "nombre": "RD 365/1995 Reglamento Situaciones Admin"}
]

# Dedup list
seen = set()
LEYES_TEMARIO = []
for ley in raw_leyes:
    if ley["boe_id"] not in seen:
        LEYES_TEMARIO.append(ley)
        seen.add(ley["boe_id"])

def safe_get_text(soup_node, default=""):
    return soup_node.get_text(strip=True) if soup_node else default

def safe_get_attr(soup_node, attr, default=""):
    return soup_node.get(attr, default) if soup_node else default

def compute_hash(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]

def tokenize_legal(text: str) -> List[str]:
    text = text.lower()
    tokens = re.findall(r'[a-záéíóúñ0-9]+', text)
    stopwords = {'el', 'la', 'de', 'que', 'en', 'y', 'a', 'los', 'las', 'del', 'se', 'por', 'para', 'con', 'un', 'una', 'al', 'lo', 'su', 'sus'}
    return [t for t in tokens if len(t) > 2 and t not in stopwords]

def generate_sparse_vector(text: str, vocab_data: Dict) -> SparseVector:
    vocab = vocab_data['vocab']
    idf_dict = vocab_data['idf']
    avgdl = vocab_data.get('avgdl', 38.0)
    k1 = vocab_data.get('k1', 1.2)
    b = vocab_data.get('b', 0.75)
    
    tokens = tokenize_legal(text)
    doc_len = len(tokens)
    if doc_len == 0: return SparseVector(indices=[], values=[])
    
    from collections import Counter
    term_freq = Counter(tokens)
    indices, values = [], []
    for term, freq in term_freq.items():
        if term in vocab:
            idx = vocab[term]
            idf = idf_dict.get(term, 0.0)
            score = idf * (freq * (k1 + 1)) / (freq + k1 * (1 - b + b * doc_len / avgdl))
            indices.append(idx)
            values.append(float(score))
    
    return SparseVector(indices=indices, values=values)

# ============================================================================
# PARSER COMPLETO BOE
# ============================================================================
def parse_boe_xml(boe_id: str, xml_content: str, fallback_title: str) -> List[dict]:
    soup = BeautifulSoup(xml_content, 'xml')
    meta_node = soup.find('metadatos')
    anal_node = soup.find('analisis')
    
    # 1. Parsear Metadatos y Análisis
    meta_dict = {}
    if meta_node:
        for child in meta_node.find_all(recursive=False):
            if child.find(recursive=False): 
                meta_dict[child.name] = {"codigo": safe_get_attr(child, "codigo"), "_text": child.get_text(strip=True)}
            else:
                meta_dict[child.name] = {"_text": child.get_text(strip=True)}
                
    titulo_ley = meta_dict.get('titulo', {}).get('_text', fallback_title)
    
    anal_dict = {"materias": [], "anteriores": [], "posteriores": []}
    if anal_node:
        for m in anal_node.find_all('materia'):
            anal_dict["materias"].append({"codigo": safe_get_attr(m, "codigo"), "_text": m.get_text(strip=True)})
        for m in anal_node.find_all('anterior'):
            anal_dict["anteriores"].append({"id_norma": safe_get_attr(m, "referencia"), "relacion": safe_get_text(m.find('palabra'))})
        for m in anal_node.find_all('posterior'):
            anal_dict["posteriores"].append({"id_norma": safe_get_attr(m, "referencia"), "relacion": safe_get_text(m.find('palabra'))})
            
    # Datos de vigencia
    estatus_derogacion = meta_dict.get('estatus_derogacion', {}).get('_text', 'N')
    vigente = estatus_derogacion == 'N'
    estado_consolidacion = meta_dict.get('estado_consolidacion', {}).get('_text', '')
    
    # 2. Parsear el Texto (Chunks)
    chunks = []
    articulos = soup.find_all('articulo')
    
    if articulos:
        for art in articulos:
            art_id = safe_get_attr(art, "id", f"art_{len(chunks)}")
            title = safe_get_text(art.find('h4')) or safe_get_text(art.find('p', class_='centro_negrita')) or f"Artículo {art_id}"
            content = art.get_text(separator="\n", strip=True)
            chunks.append({"id": art_id, "title": title, "content": content})
    else:
        all_ps = soup.find_all('p')
        metadata_tags = ['metadatos', 'analisis', 'metadata-eli', 'metadata-boe']
        legal_ps = []
        for p in all_ps:
            if not any(parent.name in metadata_tags for parent in p.parents):
                legal_ps.append(p.get_text(strip=True))
                
        texts = [p for p in legal_ps if len(p) > 5]
        cur_ps, cur_len = [], 0
        for p in texts:
            if ( ("Artículo" in p[:20] or "Disposición" in p[:25]) and cur_ps ):
                chunks.append({"id": f"p_{len(chunks)}", "title": cur_ps[0][:100], "content": "\n".join(cur_ps)})
                cur_ps, cur_len = [], 0
            cur_ps.append(p)
            cur_len += len(p)
            if cur_len > 3000:
                chunks.append({"id": f"p_{len(chunks)}", "title": cur_ps[0][:100], "content": "\n".join(cur_ps)})
                cur_ps, cur_len = [], 0
        if cur_ps:
             chunks.append({"id": f"p_{len(chunks)}", "title": cur_ps[0][:100], "content": "\n".join(cur_ps)})
             
    if not chunks:
        full = soup.get_text(separator="\n", strip=True)
        chunks.append({"id": "full", "title": "Contenido Completo", "content": full[:5000]})

    # 3. Construir Payload Completo (50+ campos) para los chunks
    results = []
    for c in chunks:
        payload = {
            # IDENTIDAD Y ESTRUCTURA
            "boe_id": boe_id,
            "law_name": titulo_ley,
            "article_number": c["id"],
            "article_title": c["title"],
            "layer": "article_chunk",
            "source": "hybrid_sync_FULL_XML_2026",
            "text_snippet": c["content"],
            
            # FECHAS Y VIGENCIA
            "organismo_emisor": meta_dict.get('departamento', {}).get('_text', ''),
            "fecha_publicacion": meta_dict.get('fecha_publicacion', {}).get('_text', ''),
            "fecha_vigencia": meta_dict.get('fecha_vigencia', {}).get('_text', ''),
            "vigente": vigente,
            "estatus_derogacion": estatus_derogacion,
            "consolidado": estado_consolidacion == "Finalizado",
            "estado_consolidacion": estado_consolidacion,
            
            # MATERIAS Y ANÁLISIS
            "rango": meta_dict.get('rango', {}).get('_text', ''),
            "materias": [m['_text'] for m in anal_dict.get('materias', [])],
            "deroga_a": [a['id_norma'] for a in anal_dict.get('anteriores', []) if 'deroga' in str(a.get('relacion', '')).lower()],
            "modificado_por": [p['id_norma'] for p in anal_dict.get('posteriores', []) if 'modifica' in str(p.get('relacion', '')).lower()],
            
            # URLs
            "url_boe": meta_dict.get('url_html_consolidada', {}).get('_text', f"https://www.boe.es/buscar/act.php?id={boe_id}"),
            "url_xml": f"https://www.boe.es/diario_boe/xml.php?id={boe_id}"
        }
        # Metadatos completos JSON stringificados
        payload["metadata_xml_dump"] = json.dumps({"metadatos": meta_dict, "analisis": anal_dict})
        results.append(payload)
        
    return results

# ============================================================================
# MAIN INGEST
# ============================================================================
def main():
    print(f"🚀 INICIANDO INGESTA DE {len(LEYES_TEMARIO)} LEYES A QDRANT: {COLLECTION_NAME}")
    
    client = QdrantClient(url=QDRANT_URL, timeout=120)
    
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in collections:
        print(f"📦 Creando colección {COLLECTION_NAME}...")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config={"dense": VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE)},
            sparse_vectors_config={"text": SparseVectorParams()},
            optimizers_config=OptimizersConfigDiff(indexing_threshold=10000)
        )
    
    print("🤖 Cargando modelos...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    with open(BM25_VOCAB_PATH, 'rb') as f:
        bm25_data = pickle.load(f)
        
    for idx, ley in enumerate(LEYES_TEMARIO[36:], 37):
        boe_id = ley["boe_id"]
        nombre = ley["nombre"]
        print(f"\n📂 [{idx}/{len(LEYES_TEMARIO)}] Descargando {boe_id} - {nombre}")
        
        urls = [f"https://www.boe.es/diario_boe/xml.php?id={boe_id}", f"https://www.boe.es/buscar/xml.php?id={boe_id}"]
        xml_content = None
        for url in urls:
            try:
                r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
                r.raise_for_status()
                if "<documento" in r.text or "<p" in r.text:
                    xml_content = r.text
                    print(f"   📥 URL XML obtenida: {url}")
                    break
            except Exception:
                pass
                
        if not xml_content:
            print(f"❌ Fallo descarga para {boe_id}")
            continue
            
        print("   ✅ Procesando XML...")
        chunks_payloads = parse_boe_xml(boe_id, xml_content, nombre)
        
        if not chunks_payloads:
            print("   ⚠️ No se encontraron chunks válidos.")
            continue
            
        points = []
        for i, payload in enumerate(chunks_payloads):
            text_to_embed = f"{payload['law_name']} {payload['article_title']} {payload['text_snippet']}"
            dense_vec = model.encode(text_to_embed, convert_to_tensor=False).tolist()
            sparse_vec = generate_sparse_vector(text_to_embed, bm25_data)
            
            # ======== UUID CORRECTO (EL BUG FIX) ========
            # Valid UUID generation requested by Qdrant (uuid v5 DNS namespace is perfect)
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{boe_id}_{payload['article_number']}_{i}"))
            
            points.append(PointStruct(id=point_id, vector={"dense": dense_vec, "text": sparse_vec}, payload=payload))
            
        if points:
            batch_size = 200
            for i in range(0, len(points), batch_size):
                client.upsert(collection_name=COLLECTION_NAME, points=points[i:i+batch_size])
            print(f"   🟩 Insertados {len(points)} puntos en Qdrant.")
        
        time.sleep(1) # BOE anti-DDoS

    print("\n✨ INGESTA MASIVA FINALIZADA ✨")

if __name__ == "__main__":
    main()
