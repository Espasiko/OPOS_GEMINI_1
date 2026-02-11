#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT: 05_01_26_pair_exams.py
PROPÓSITO: Emparejar Cuestionarios con Plantillas usando heurística de nombres.
"""

import json
import re
from pathlib import Path
from difflib import SequenceMatcher

INPUT_FILE = Path("/home/spas/OPOS_GEMINI_1/staging_area/05_01_26_exams_processing/parsed_questions.jsonl")
OUTPUT_REPORT = Path("/home/spas/OPOS_GEMINI_1/staging_area/05_01_26_exams_processing/pairing_report.md")
MAX_SCORE_THRESHOLD = 2 # Minimum overlap to consider

def normalize_name(name):
    # Tokens clave: libre, interna, modelo a, modelo b, 2023, 2024, 2025
    tokens = set()
    name = name.lower()
    
    if "libre" in name: tokens.add("libre")
    if "interna" in name: tokens.add("interna")
    if "modelo a" in name or "modelo+a" in name: tokens.add("modelo_a")
    if "modelo b" in name or "modelo+b" in name: tokens.add("modelo_b")
    
    years = re.findall(r'202[3-6]', name)
    for y in years: tokens.add(y)
    
    return tokens

def main():
    questions = []
    answers = []
    
    with open(INPUT_FILE, "r") as f:
        for line in f:
            data = json.loads(line)
            if data["type"] == "questionnaire":
                questions.append(data)
            elif data["type"] == "answer_key":
                answers.append(data)

    pairs = []
    used_answers = set()
    
    with open(OUTPUT_REPORT, "w") as rep:
        rep.write("# 🤝 Informe de Emparejamiento (Pairing)\n\n")
        
        for q in questions:
            q_tokens = normalize_name(q["filename"])
            best_match = None
            best_score = 0
            
            for a in answers:
                if a["filename"] in used_answers: continue
                
                a_tokens = normalize_name(a["filename"])
                intersection = len(q_tokens.intersection(a_tokens))
                
                # Bonus por coincidencia de sufijos raros (MIE...)
                if q["filename"][-15:] == a["filename"][-15:]:
                    intersection += 2
                    
                if intersection > best_score:
                    best_score = intersection
                    best_match = a
            
            if best_match and best_score >= MAX_SCORE_THRESHOLD:
                used_answers.add(best_match["filename"])
                pairs.append((q, best_match))
                
                rep.write(f"## ✅ PAIR FOUND\n")
                rep.write(f"- **Preguntas**: {q['filename']} ({q['count']} Qs)\n")
                rep.write(f"- **Respuestas**: {best_match['filename']} ({best_match['count']} As)\n")
                rep.write(f"- *Score*: {best_score} | *Tokens*: {q_tokens}\n\n")
                
                # Generar archivo fusionado en el futuro
                
            else:
                rep.write(f"## ❌ NO MATCH\n")
                rep.write(f"- **Preguntas**: {q['filename']} ({q['count']} Qs)\n")
                rep.write(f"- *Mejor Candidato*: {best_match['filename'] if best_match else 'None'} (Score: {best_score})\n\n")

        rep.write("\n## ⚠️ Sin Pareja (Orphan Answers)\n")
        for a in answers:
             if a["filename"] not in used_answers:
                 rep.write(f"- {a['filename']}\n")

    print(f"Reporte generado en: {OUTPUT_REPORT}")

if __name__ == "__main__":
    main()
