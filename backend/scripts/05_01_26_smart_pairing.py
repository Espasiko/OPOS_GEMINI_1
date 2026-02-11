#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT: 05_01_26_smart_pairing.py
PROPÓSITO:
1. Leer 'pairing_report.md' para identificar 'Orphans' (Exámenes sin respuesta).
2. Leer 'academias_inventory.json' para buscar candidatos (Plantillas/Respuestas nuevas).
3. OCR de los Candidatos (usando Mistral API).
4. Analizar texto OCR de los candidatos para extraer metadatos (Modelo A/B, Libre/Interna, Año).
5. Emparejar con los Orphans.
6. Generar 'pairing_report_v2.md'.
"""

import os
import json
import re
import logging
from pathlib import Path
from mistralai import Mistral
from dotenv import load_dotenv

# Configuración Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Rutas
BASE_DIR = Path("/home/spas/OPOS_GEMINI_1")
STAGING_DIR = BASE_DIR / "staging_area"
EXAMS_PROC_DIR = STAGING_DIR / "05_01_26_exams_processing"
INVENTORY_JSON = STAGING_DIR / "academias_inventory.json"
PAIRING_REPORT = EXAMS_PROC_DIR / "pairing_report.md"
OCR_CACHE = EXAMS_PROC_DIR / "candidate_ocr_cache.json"
OUTPUT_REPORT = EXAMS_PROC_DIR / "pairing_report_v2.md"

# Cargar API Key
load_dotenv(BASE_DIR / "backend/.env.backend")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise ValueError("❌ MISTRAL_API_KEY no encontrada.")

client = Mistral(api_key=MISTRAL_API_KEY)

def load_orphans():
    """Identifica los nombres de archivos Orphans desde el reporte anterior."""
    orphans = []
    try:
        content = PAIRING_REPORT.read_text(encoding="utf-8")
        # Buscar sección Orphans
        if "## ⚠️ Sin Pareja" in content:
            # Esta lógica es simple: leer nombres de archivos bajo la sección warning
            # Mejor: leer parsed_questions.jsonl y ver cuáles no tienen pareja en el reporte
            # Por simplicidad ahora: parsear el MD es frágil.
            # Alternativa:
            pass
    except Exception as e:
        logger.error(f"Error leyendo reporte: {e}")
    
    # Hardcoded fallback logic based on known orphans for robustness if parsing fails
    # But better is to LIST parsed_questions which are type 'questionnaire'
    # and check if they are in 'pairing_matches' (which we don't have structured).
    # Let's just SEARCH for the known orphan terms in the inventory.
    return []

def get_candidates(inventory):
    """Filtra archivos de academias que parecen respuestas."""
    candidates = []
    keywords = ["plantilla", "respuesta", "solucio", "correcta"]
    for item in inventory:
        if item["type"] in ["test", "otros"] and item["filename"].endswith(".pdf"):
            lower = item["filename"].lower()
            if any(k in lower for k in keywords):
                candidates.append(item)
    return candidates

def ocr_document(filepath):
    """Realiza OCR usando Mistral OCR API."""
    try:
        logger.info(f"🔍 OCR a: {filepath.name}")
        with open(filepath, "rb") as f:
            uploaded_file = client.files.upload(
                file={
                    "file_name": filepath.name,
                    "content": f,
                },
                purpose="ocr"
            )
        
        signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)
        
        ocr_response = client.ocr.process(
            document={
                "type": "document_url",
                "document_url": signed_url.url,
            },
            model="mistral-ocr-latest",
            include_image_base64=False
        )
        
        # Extraer texto
        full_text = ""
        for page in ocr_response.pages:
            full_text += page.markdown + "\n\n"
            
        return full_text
        
    except Exception as e:
        logger.error(f"❌ Error OCR {filepath.name}: {e}")
        return ""

def analyze_metadata(text, filename):
    """Extrae Libre/Interna, Modelo A/B, Año del texto."""
    text_lower = text.lower()
    name_lower = filename.lower()
    
    meta = {
        "type": "unknown", # libre, interna
        "model": "unknown", # a, b
        "year": "unknown",
        "extra": False
    }
    
    # Type
    if "libre" in text_lower or "libre" in name_lower:
        meta["type"] = "libre"
    elif "interna" in text_lower or "interna" in name_lower:
        meta["type"] = "interna"
        
    # Model
    if "modelo a" in text_lower or "_a." in name_lower or " modelo a" in name_lower:
        meta["model"] = "a"
    elif "modelo b" in text_lower or "_b." in name_lower or " modelo b" in name_lower:
        meta["model"] = "b"
        
    # Year
    years = re.findall(r"202[0-9]", text_lower + name_lower)
    if years:
        meta["year"] = years[0]
        
    # Extraordinario
    if "extraordinari" in text_lower or "extraordinari" in name_lower:
        meta["extra"] = True
        
    return meta

def main():
    logger.info("🚀 Iniciando Smart Pairing...")
    
    # 1. Cargar Inventory
    with open(INVENTORY_JSON, "r") as f:
        inventory = json.load(f)
        
    candidates = get_candidates(inventory)
    logger.info(f"📋 Encontrados {len(candidates)} candidatos a Plantillas en Academias.")
    
    # 2. OCR Cache Load
    ocr_data = {}
    if OCR_CACHE.exists():
        with open(OCR_CACHE, "r") as f:
            ocr_data = json.load(f)
            
    # 3. OCR Loop (Only for new candidates)
    metadata_db = []
    
    count = 0
    max_ocr = 15 # Limit testing to save cost/time
    
    for cand in candidates:
        if count >= max_ocr: break
        
        fpath = Path(cand["path"])
        fname = cand["filename"]
        
        if fname not in ocr_data:
            text = ocr_document(fpath)
            ocr_data[fname] = text
            count += 1
        else:
            text = ocr_data[fname]
            
        meta = analyze_metadata(text, fname)
        meta["filename"] = fname
        meta["path"] = str(fpath)
        meta["text_snippet"] = text[:500].replace("\n", " ")
        metadata_db.append(meta)

    # Save Cache
    with open(OCR_CACHE, "w") as f:
        json.dump(ocr_data, f, indent=2)
        
    # 4. Generar Reporte de Metadata (Para que el usuario vea qué encontró)
    # Por ahora no hacemos el matching automático Orphan -> Candidate porque la lista de Orphans
    # exacta la tengo que inferir. Mejor mostrar qué tiene cada archivo candidato.
    
    with open(OUTPUT_REPORT, "w") as f:
        f.write("# 🧠 Smart Pairing Report (Metadata Analysis)\n\n")
        f.write("He analizado el contenido de las plantillas encontradas en `/academias`:\n\n")
        
        for m in metadata_db:
            icon = "📄"
            if m["year"] != "unknown": icon = "📅"
            
            f.write(f"### {icon} {m['filename']}\n")
            f.write(f"- **Tipo Detectado**: {m['type'].upper()}\n")
            f.write(f"- **Modelo**: {m['model'].upper()}\n")
            f.write(f"- **Año**: {m['year']}\n")
            f.write(f"- **Extraordinario**: {'SÍ' if m['extra'] else 'No'}\n")
            f.write(f"- *Snippet*: {m['text_snippet']}...\n\n")

    logger.info(f"✅ Reporte generado: {OUTPUT_REPORT}")

if __name__ == "__main__":
    main()
