
import json
import os
from verify_boe_links import verify_on_boe
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def audit_dataset(file_path):
    report = []
    if not os.path.exists(file_path):
        logger.error(f"Archivo no encontrado: {file_path}")
        return
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    logger.info(f"Auditando {len(lines)} registros en {file_path}...")
    
    hallucinations = 0
    checked = 0
    
    for line in lines[:20]: # Auditar una muestra para ahorrar tiempo/recursos
        item = json.loads(line)
        pregunta = item.get("pregunta", "")
        referencias = item.get("referencias", [])
        
        item_audit = {
            "pregunta": pregunta[:50] + "...",
            "referencias": [],
            "status": "PASS"
        }
        
        for ref in referencias:
            # Intentar extraer artículo y ley (formato común: 'Art. X de la Ley Y')
            # Para este script, usaremos una lógica simplificada o pasaremos la ref completa
            # Si el formato es 'Art. 165 de la LGSS'
            import re
            match = re.search(r"Art\.?\s*(\d+)", ref, re.IGNORECASE)
            art = match.group(1) if match else "1"
            ley = ref.split(" de la ")[-1] if " de la " in ref else ref
            
            res = verify_on_boe(art, ley)
            item_audit["referencias"].append({
                "ref": ref,
                "valid": res["valid"],
                "msg": res["message"]
            })
            if res["valid"] is False:
                item_audit["status"] = "FAIL"
                hallucinations += 1
        
        report.append(item_audit)
        checked += 1
        logger.info(f"Checked {checked}/{len(lines[:20])} - Result: {item_audit['status']}")

    print("\n--- INFORME DE AUDITORÍA (MUESTRA BOE) ---")
    print(f"Total Auditado: {checked}")
    print(f"Alucinaciones Detectadas: {hallucinations}")
    print(f"Precisión: {((checked - hallucinations) / checked) * 100:.1f}%")

if __name__ == "__main__":
    audit_dataset("dataset_generator/multi_model_20_12/qa_groq_master_100.jsonl")
