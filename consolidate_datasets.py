
import json
import os
import hashlib
from datetime import datetime


# Directorios donde buscar archivos JSONL
SEARCH_DIRS = [
    "./dataset_generator",
    "./golden_dataset",
    "./conceptual_materials"
]

OUTPUT_DIR = "./golden_dataset/consolidated"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"golden_dataset_consolidated_{datetime.now().strftime('%Y%m%d')}.jsonl")

def get_question_hash(question_text):
    """Genera hash simple de la pregunta normalizada para detectar duplicados"""
    normalized = question_text.lower().strip().replace("¿", "").replace("?", "")
    return hashlib.md5(normalized.encode('utf-8')).hexdigest()

def find_jsonl_files(directories):
    """Encuentra recursivamente todos los archivos .jsonl en los directorios dados"""
    jsonl_files = []
    for root_dir in directories:
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith(".jsonl") and "consolidated" not in filename:
                    full_path = os.path.join(dirpath, filename)
                    jsonl_files.append(full_path)
    return jsonl_files

def main():
    print("🧹 Iniciando consolidación y deduplicación de datasets...")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Buscar archivos dinámicamente
    input_files = find_jsonl_files(SEARCH_DIRS)
    print(f"📂 Encontrados {len(input_files)} archivos JSONL para procesar.")
    
    unique_questions = {}
    stats = {
        "files_processed": 0,
        "total_read": 0,
        "duplicates": 0,
        "invalid": 0,
        "final_count": 0
    }
    
    for file_path in input_files:
        if not os.path.exists(file_path):
            print(f"⚠️ Archivo no encontrado (saltando): {file_path}")
            continue
            
        print(f"📖 Leyendo: {file_path}")
        stats["files_processed"] += 1
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line: continue
                    
                    try:
                        qa = json.loads(line)
                        stats["total_read"] += 1
                        
                        # Validaciones básicas
                        question = qa.get("pregunta")
                        if not question: 
                            stats["invalid"] += 1
                            continue
                            
                        # Deduplicación
                        q_hash = get_question_hash(question)
                        
                        # Si ya existe, nos quedamos con la versión más completa (ej. si tiene 'id' o 'generated_at')
                        if q_hash in unique_questions:
                            stats["duplicates"] += 1
                            # Lógica simple: si la nueva tiene 'referencias' y la vieja no, reemplazamos
                            existing = unique_questions[q_hash]
                            if not existing.get("referencias") and qa.get("referencias"):
                                unique_questions[q_hash] = qa
                        else:
                            unique_questions[q_hash] = qa
                            
                    except json.JSONDecodeError:
                        stats["invalid"] += 1
                        
        except Exception as e:
            print(f"❌ Error leyendo {file_path}: {e}")

    # Escribir resultado
    stats["final_count"] = len(unique_questions)
    print(f"\n💾 Guardando {stats['final_count']} preguntas únicas en {OUTPUT_FILE}...")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for qa in unique_questions.values():
            # Añadir metadatos de consolidación
            qa["consolidation_date"] = datetime.now().isoformat()
            f.write(json.dumps(qa, ensure_ascii=False) + '\n')
            
    print("\n📊 ESTADÍSTICAS FINALES:")
    print(f"   Archivos procesados: {stats['files_processed']}")
    print(f"   Total preguntas leídas: {stats['total_read']}")
    print(f"   Duplicados eliminados: {stats['duplicates']}")
    print(f"   Inválidos/Errores: {stats['invalid']}")
    print(f"   ✅ TOTAL CONSOLIDADO: {stats['final_count']}")

if __name__ == "__main__":
    main()
