#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT: 05_01_26_clean_exams_ocr.py
PROPÓSITO: Limpieza y Emparejamiento de Exámenes (Raw -> Clean & Paired).
"""

import json
import re
import logging
from pathlib import Path

# Configuración de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

INPUT_FILE = Path("/home/spas/OPOS_GEMINI_1/staging_area/05_01_26_exams_processing/extracted_content_raw.jsonl")
OUTPUT_FILE = Path("/home/spas/OPOS_GEMINI_1/staging_area/05_01_26_exams_processing/clean_paired_exams.jsonl")

def clean_markdown(text: str) -> str:
    """Limpia artefactos comunes de OCR/Markdown."""
    if not text: return ""
    # Quitar cabeceras/pies de página repetitivos (heurística simple)
    text = re.sub(r'Página \d+ de \d+', '', text)
    text = re.sub(r'--- PÁGINA \d+ ---', '', text)
    return text.strip()

def extract_questions_answers(text: str) -> list:
    """
    Intenta extraer preguntas y opciones.
    Esta es una heurística básica que mejoraremos.
    """
    # Patrón: número. Texto... a) ... b) ... c) ...
    # Simplificado para esta versión inicial.
    return [] # Placeholder

def process_line(line: str) -> dict:
    try:
        data = json.loads(line)
        raw_text = data.get("content", "")
        clean_text = clean_markdown(raw_text)
        
        return {
            "filename": data.get("filename"),
            "original_type": data.get("type"),
            "clean_text": clean_text,
            "status": "cleaned"
        }
    except Exception as e:
        logger.error(f"Error processing line: {e}")
        return None

def main():
    logger.info("🧹 INICIANDO LIMPIEZA DE EXÁMENES...")
    
    if not INPUT_FILE.exists():
        logger.error(f"❌ No existe archivo de entrada: {INPUT_FILE}")
        return

    count = 0
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
        with open(INPUT_FILE, "r", encoding="utf-8") as in_f:
            for line in in_f:
                processed = process_line(line)
                if processed:
                    out_f.write(json.dumps(processed, ensure_ascii=False) + "\n")
                    count += 1

    logger.info(f"✅ Limpieza completada. {count} items procesados en: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
