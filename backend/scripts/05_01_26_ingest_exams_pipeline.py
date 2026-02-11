#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT: 05_01_26_ingest_exams_pipeline.py
PROPÓSITO: Ingesta real de Exámenes (OCR Mistral) + Conceptuales.
"""

import os
import json
import logging
import time
import base64
from pathlib import Path
from dotenv import load_dotenv
from mistralai import Mistral

# Configuración de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/tmp/ingest_exams_05_01_26.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Cargar variables
load_dotenv(dotenv_path='/home/spas/OPOS_GEMINI_1/backend/.env.backend')

BASE_DIR = Path("/home/spas/OPOS_GEMINI_1")
EXAMS_DIR = BASE_DIR / "extracted_texts/docs_opos_bajados_oficiales"
CONCEPTUAL_DIR = BASE_DIR / "conceptual_materials/extracted_texts"
OUTPUT_DIR = BASE_DIR / "staging_area/05_01_26_exams_processing"
OUTPUT_FILE = OUTPUT_DIR / "extracted_content_raw.jsonl"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def get_mistral_client():
    # Diagnostic showed MISTRAL_API_KEY works, while MISTRAL_OCR_API_KEY failed.
    # Prioritizing the general key.
    key = os.getenv("MISTRAL_API_KEY") or os.getenv("MISTRAL_OCR_API_KEY")
    if not key:
        raise ValueError("❌ No MISTRAL_API_KEY found")
    logger.info(f"🔑 Usando API Key: {key[:5]}...")
    return Mistral(api_key=key)

def process_pdf_with_mistral(client, file_path: Path) -> dict:
    """Sube el PDF a Mistral OCR y extrae markdown."""
    try:
        logger.info(f"📤 Subiendo: {file_path.name}...")
        
        uploaded_file = client.files.upload(
            file={
                "file_name": file_path.name,
                "content": open(file_path, "rb"),
            },
            purpose="ocr"
        )
        
        logger.info(f"🔄 Procesando OCR: {file_path.name}...")
        signed_url = client.files.get_signed_url(file_id=uploaded_file.id)
        
        ocr_response = client.ocr.process(
            document={
                "document_name": file_path.name,
                "document_url": signed_url.url
            },
            model="mistral-ocr-latest",
            include_image_base64=False 
        )
        
        # Extraer el markdown de todas las páginas
        full_markdown = ""
        for page in ocr_response.pages:
            full_markdown += page.markdown + "\n\n"
            
        return {
            "filename": file_path.name,
            "content": full_markdown,
            "type": "exam_pdf",
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"❌ Error OCR {file_path.name}: {e}")
        return {
            "filename": file_path.name,
            "error": str(e),
            "status": "error"
        }

def read_conceptual_txt(file_path: Path) -> dict:
    try:
        return {
            "filename": file_path.name,
            "content": file_path.read_text(encoding="utf-8", errors="replace"),
            "type": "conceptual_txt",
            "status": "success"
        }
    except Exception as e:
        return {"filename": file_path.name, "status": "error", "error": str(e)}

def main():
    logger.info("🚀 INICIANDO EJECUCIÓN REAL (MISTRAL OCR)")
    client = get_mistral_client()
    
    # 1. Filtros
    all_pdfs = list(EXAMS_DIR.glob("*.pdf"))
    valid_pdfs = [p for p in all_pdfs if not p.name.startswith("report_") and "Nota+informativa" not in p.name]
    
    conceptual_txts = list(CONCEPTUAL_DIR.glob("*.txt"))
    
    logger.info(f"🎯 Objetivos: {len(valid_pdfs)} PDFs (Exámenes) + {len(conceptual_txts)} TXTs")
    
    # 2. Procesamiento
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        # A) Conceptuales (Rápido)
        for txt in conceptual_txts:
            res = read_conceptual_txt(txt)
            f.write(json.dumps(res, ensure_ascii=False) + "\n")
            
        # B) PDFs (Lento - OCR)
        for i, pdf in enumerate(valid_pdfs):
            logger.info(f"⏳ [{i+1}/{len(valid_pdfs)}] Procesando {pdf.name}")
            res = process_pdf_with_mistral(client, pdf)
            f.write(json.dumps(res, ensure_ascii=False) + "\n")
            f.flush()
            time.sleep(1) # Rate limit protection

    logger.info(f"✅ FINALIZADO. Resultados en: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
