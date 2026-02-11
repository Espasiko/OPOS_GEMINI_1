#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT: 05_01_26_parse_questions.py
PROPÓSITO: Parsear el texto crudo de Exámenes y Plantillas en estructuras JSON.
"""

import json
import re
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

INPUT_FILE = Path("/home/spas/OPOS_GEMINI_1/staging_area/05_01_26_exams_processing/extracted_content_raw.jsonl")
OUTPUT_FILE = Path("/home/spas/OPOS_GEMINI_1/staging_area/05_01_26_exams_processing/parsed_questions.jsonl")

def parse_cuestionario(text: str) -> list:
    """Extrae preguntas y opciones del texto de un Cuestionario."""
    questions = []
    # Regex preliminar basada en la muestra
    # 1. Pregunta...
    # a) Opcion...
    
    current_q = None
    lines = text.split('\n')
    
    q_pattern = re.compile(r'^\s*(\d+)\.\s+(.+)')
    opt_pattern = re.compile(r'^\s*([a-d])\)\s+(.+)')
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Detectar Pregunta
        q_match = q_pattern.match(line)
        if q_match:
            if current_q: questions.append(current_q)
            current_q = {
                "number": int(q_match.group(1)),
                "text": q_match.group(2),
                "options": {}
            }
            continue
            
        # Detectar Opción
        opt_match = opt_pattern.match(line)
        if current_q and opt_match:
            letter = opt_match.group(1).lower()
            text = opt_match.group(2)
            current_q["options"][letter] = text
            continue
            
        # Continuación de texto (multilínea)
        # Si no es preg ni opcion, asumimos que es continuación del anterior
        if current_q:
            # Si ya tenemos opciones, es continuación de la última opción
            if current_q["options"]:
                last_opt = sorted(current_q["options"].keys())[-1]
                current_q["options"][last_opt] += " " + line
            else:
                # Es continuación del texto de la pregunta
                current_q["text"] += " " + line

    if current_q: questions.append(current_q)
    return questions

def parse_plantilla(text: str) -> dict:
    """Extrae el mapa de respuestas correctas (1:a, 2:b...)"""
    # Las plantillas suelen ser tablas o listas. 
    # Buscamos patrones "1 a", "1-a", "1) a", etc.
    # Esta es una heurística agresiva.
    answers = {}
    
    # Normalizar: quitar todo lo que no sea nums o letras a-d
    # Tokenizar
    tokens = re.findall(r'[0-9]+|[a-d]', text.lower())
    
    # Iterar buscando pares (Numero, Letra)
    i = 0
    while i < len(tokens) - 1:
        curr = tokens[i]
        nxt = tokens[i+1]
        
        if curr.isdigit() and nxt.isalpha() and len(nxt)==1:
            num = int(curr)
            if num not in answers: # Evitar duplicados erróneos
                answers[num] = nxt
            i += 2
        else:
            i += 1
            
    return answers

def process_line(line: str):
    try:
        data = json.loads(line)
        if data.get("status") != "success": return None
        
        filename = data.get("filename", "")
        text = data.get("content", "")
        
        result = {
            "filename": filename,
            "type": "unknown",
            "parsed_data": None
        }
        
        # Clasificar por nombre
        name_lower = filename.lower()
        if "cuestionario" in name_lower or "examen" in name_lower:
            result["type"] = "questionnaire"
            result["parsed_data"] = parse_cuestionario(text)
            result["count"] = len(result["parsed_data"])
            
        elif "plantilla" in name_lower:
            result["type"] = "answer_key"
            result["parsed_data"] = parse_plantilla(text)
            result["count"] = len(result["parsed_data"])
            
        return result
        
    except Exception as e:
        logger.error(f"Error parseando linea: {e}")
        return None

def main():
    logger.info("🧩 INICIANDO PARSEO INTELIGENTE...")
    items = []
    
    # Leer todo y filtrar duplicados (si hay error+success, quedarse con success)
    # Mejor: procesar todo y si hay conflicto, decidir.
    
    with open(INPUT_FILE, "r") as f:
        for line_num, line in enumerate(f):
            res = process_line(line)
            if res and res["parsed_data"]:
                items.append(res)
                logger.info(f"✅ Parsed {res['filename']} ({res['count']} items)")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
            
    logger.info(f"🏁 Parseo finalizado. {len(items)} archivos procesados.")

if __name__ == "__main__":
    main()
