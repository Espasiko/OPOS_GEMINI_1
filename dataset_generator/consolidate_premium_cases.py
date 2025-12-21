import os
import shutil
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directorios de Origen
SOURCES = [
    Path("dataset_generator/premium_content/deepseek_pilot"),
    Path("dataset_generator/premium_content/groq_rematch"),
    Path("dataset_generator/premium_content/mistral_rematch") # Future proof
]

# Directorio Destino
DEST = Path("golden_dataset/premium_final")
DEST.mkdir(parents=True, exist_ok=True)

def validate_case(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Flexibilidad: El caso puede estar en la raíz o en "case"
        case_data = data.get("case", data)
        
        qs = case_data.get("preguntas", [])
        scenario = case_data.get("escenario", "")
        
        # Criterios Premium
        if len(qs) < 15: return False, "Menos de 15 preguntas"
        if len(scenario) < 200: return False, "Escenario demasiado corto"
        
        return True, "OK"
    except Exception as e:
        return False, f"Error JSON: {e}"

def consolidate():
    count = 0
    for src_dir in SOURCES:
        if not src_dir.exists(): continue
        
        logger.info(f"📂 Escaneando: {src_dir}")
        for file in src_dir.glob("*.json"):
            is_valid, msg = validate_case(file)
            
            if is_valid:
                dest_file = DEST / file.name
                shutil.copy2(file, dest_file)
                logger.info(f"✅ Copiado: {file.name}")
                count += 1
            else:
                logger.warning(f"⚠️ Ignorado {file.name}: {msg}")

    logger.info(f"🎉 Consolidación terminada. Total casos Premium: {count}")

if __name__ == "__main__":
    consolidate()
