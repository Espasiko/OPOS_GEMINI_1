
import json
import logging
import re
from pathlib import Path

# Configuración
BASE_DIR = Path("/home/spas/OPOS_GEMINI_1")
STAGING_DIR = BASE_DIR / "staging_area/05_01_26_exams_processing"
INPUT_QUESTIONS = STAGING_DIR / "parsed_questions.jsonl"
OUTPUT_PAIRED = STAGING_DIR / "smart_paired_exams.jsonl"
OCR_CACHE = STAGING_DIR / "candidate_ocr_cache.json"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smart_pairing_app")

# Definición de Huérfanos (Hardcoded basándonos en pairing_report.md anterior)
# En un pipeline ideal, esto se detectaría dinámicamente.
ORPHANS = {
    "CUESTIONARIO+PROMOCION+INTERNA+MODELO+A2023.pdf": {
        "type": "interna", "year": "2023", "model": "a", "extra": False
    },
    "CUESTIONARIO+LIBRE+MODELO+A2023.pdf": {
        "type": "libre", "year": "2023", "model": "a", "extra": False
    },
    "CUESTIONARIO+LIBRE+MODELO+B2023.pdf": {
        "type": "libre", "year": "2023", "model": "b", "extra": False
    },
    "EXAMEN+EXTRAORDINARIO+PROMOCIÓN+INTERNA+CON+SUPUESTO2023.pdf": {
        "type": "interna", "year": "2023", "model": "unknown", "extra": True
    },
    "EXAMEN+LIBRE+EXTRAORDINARIOMIE20250320DOC23MO.pdf": {
         "type": "libre", "year": "2025", "extra": True  # A veces etiquetado como 2023/2025 confuso, asumimos lo que dice el nombre
    }
}

def load_ocr_cache():
    if not OCR_CACHE.exists():
        logger.error("No OCR Cache found")
        return {}
    with open(OCR_CACHE, "r") as f:
        return json.load(f)

def parse_answer_table_text(text):
    """
    Intenta extraer pares (Numero, Letra) de texto OCR sucio.
    Busca patrones como "1 A", "1. A", "1 | A", etc.
    """
    answers = {}
    
    # Patrón robusto: Inicio de línea o espacio, Número (1-150), separador opcional, Letra (A-D), fin o espacio
    # Ejemplo: "1   C", "1. C", "| 1 | C |"
    pattern = re.compile(r"(?:^|\s|\|)(\d{1,3})(?:[\.\)\s\|]+)([a-dA-D])(?=\s|\||$)")
    
    matches = pattern.findall(text)
    for num, let in matches:
        answers[str(int(num))] = let.upper() # int() para quitar ceros a la izq
        
    return answers

def find_candidate_match(orphan_meta, ocr_data):
    """
    Busca en el texto OCR cached un candidato que coincida con los metadatos del huérfano.
    """
    best_candidate = None
    best_score = 0
    
    for filename, text in ocr_data.items():
        score = 0
        text_lower = text.lower()
        fname_lower = filename.lower()
        
        # 1. Año
        if orphan_meta['year'] in text_lower or orphan_meta['year'] in fname_lower:
            score += 2
        
        # 2. Tipo (Libre / Interna)
        if orphan_meta['type'] == 'libre':
            if 'libre' in text_lower and 'interna' not in text_lower.replace("acceso libre y promoción interna", ""): # Evitar falsos positivos en encabezados combinados
                 score += 2
            elif 'libre' in fname_lower:
                 score += 2
        elif orphan_meta['type'] == 'interna':
            if 'interna' in text_lower: # Promocion interna suele ser específico
                score += 2
            elif 'interna' in fname_lower:
                score += 2

        # 3. Model
        if orphan_meta.get('model') and orphan_meta['model'] != 'unknown':
            mod = orphan_meta['model']
            if f"modelo {mod}" in text_lower or f"modelo {mod}" in fname_lower:
                score += 1
        
        # 4. Extraordinario
        if orphan_meta['extra']:
            if 'extraordinaria' in text_lower or 'extraordinari' in fname_lower:
                score += 3 # Peso alto
        else:
             if 'extraordinaria' not in text_lower and 'extraordinari' not in fname_lower:
                score += 1
        
        # Palabras clave de plantilla
        if "plantilla" in fname_lower or "respuestas" in fname_lower:
            score += 1

        if score > best_score and score >= 5: # Umbral mínimo de confianza
            best_score = score
            best_candidate = filename

    return best_candidate, best_score

def main():
    logger.info("🚀 Iniciando Aplicación de Pairing (Resolución de Huérfanos)")
    
    ocr_data = load_ocr_cache()
    if not ocr_data: return

    # Cargar preguntas parseadas
    questions_map = {}
    with open(INPUT_QUESTIONS, "r") as f:
        for line in f:
            data = json.loads(line)
            questions_map[data['filename']] = data

    paired_count = 0
    
    with open(OUTPUT_PAIRED, "w", encoding="utf-8") as f_out:
        for orphan_file, meta in ORPHANS.items():
            if orphan_file not in questions_map:
                logger.warning(f"Orphan {orphan_file} no encontrada en parsed_questions.jsonl")
                continue
                
            logger.info(f"🔍 Buscando pareja para: {orphan_file} ({meta})")
            
            cand_name, score = find_candidate_match(meta, ocr_data)
            
            if cand_name:
                logger.info(f"   ✅ MATCH!!! -> {cand_name} (Score: {score})")
                
                # Extraer respuestas
                answers = parse_answer_table_text(ocr_data[cand_name])
                logger.info(f"      Respuestas extraídas: {len(answers)}")
                
                if len(answers) > 20: # Sanity check
                    # Construir objeto final
                    exam_data = questions_map[orphan_file]
                    
                    # Inyectar respuesta correcta en cada pregunta
                    for q in exam_data.get('parsed_data', []):
                        q_num = str(q.get('question_number'))
                        if q_num in answers:
                            q['correct_answer'] = answers[q_num]
                            
                    # Guardar
                    final_obj = {
                        "filename": orphan_file,
                        "original_Exam": orphan_file,
                        "paired_with": cand_name,
                        "content": exam_data['parsed_data'], # Lista de preguntas enriquecida
                        "metadata": meta
                    }
                    f_out.write(json.dumps(final_obj, ensure_ascii=False) + "\n")
                    paired_count += 1
                else:
                    logger.warning("      ⚠️ Pocas respuestas extraídas. Saltando.")
            else:
                logger.warning("   ❌ No se encontró candidato.")

    logger.info(f"🏁 Proceso terminado. {paired_count} exámenes emparejados guardados en {OUTPUT_PAIRED}")

if __name__ == "__main__":
    main()
