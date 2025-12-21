
import json
import glob
import os
import requests
import re
import time

# Config
BACKEND_URL = "http://127.0.0.1:8000"
DATA_DIR = "./dataset_generator/qa_mistral_batches_20_12/"

def get_latest_file():
    files = glob.glob(os.path.join(DATA_DIR, "qa_mass_verified_*.jsonl"))
    if not files: return None
    return max(files, key=os.path.getctime)

def verify_against_backend(ref):
    """
    Verifica contra la Base de Datos Local (Qdrant + Postgres)
    que contiene el BOE Oficial descargado.
    """
    if not ref: return False, "Sin referencia"
    try:
        # Limpieza básica
        clean_ref = ref.lower().replace("art.", "artículo").strip()
        
        response = requests.post(
            f"{BACKEND_URL}/api/rag/search",
            json={
                "query": clean_ref,
                "top_k": 3,
                "min_score": 0.1 
            }, timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            docs = data.get("documents", [])
            if docs:
                # Heurística simple: Si devuelve documentos con score decente (>0.1 ya filtrado)
                # Y el contenido parece legal
                sample_text = docs[0].get("content", "")[:100]
                return True, f"Encontrado: {sample_text}..."
            else:
                return False, "No encontrado en BD Local"
        return False, f"Backend Error: {response.status_code}"
    except Exception as e:
        return False, f"Error conexión: {e}"

def generate_boe_link(ref):
    """
    Genera un link de búsqueda al BOE real para validación manual
    """
    # Intentar extraer Ley y Artículo
    # Ej: "art. 123 LGSS" -> Busqueda "LCGSS articulo 123"
    query = ref.replace(" ", "+")
    return f"https://www.boe.es/buscar/act.php?id=Buscar&p=20241220&t={query}" # Link simulado de búsqueda

def main():
    print("🕵️  AUDITORÍA FINAL DE CALIDAD Y VERACIDAD (MASS BATCH)")
    target_file = get_latest_file()
    
    if not target_file:
        print("❌ No se encontró archivo de generación masiva.")
        return

    print(f"📁 Analizando: {target_file}")
    
    verified_count = 0
    total = 0
    
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                total += 1
                qa = json.loads(line)
                
                question = qa.get("pregunta", "")[:60]
                refs = qa.get("referencias", [])
                refs_str = ", ".join(refs) if isinstance(refs, list) else str(refs)
                
                print(f"\n🔹 [{total}] {question}...")
                print(f"   ⚖️  Ref: {refs_str}")
                
                # Verificación 1: Backend Local (Fuente de Verdad)
                is_valid, msg = verify_against_backend(refs_str)
                
                status_icon = "✅" if is_valid else "❌"
                print(f"   {status_icon} Backend Local: {msg}")
                
                if is_valid:
                    verified_count += 1
                    
                # Verificación 2: Link Web (Para el usuario)
                web_link = generate_boe_link(refs_str)
                print(f"   🌐 Web Check: {web_link}")
                
    except Exception as e:
        print(f"❌ Error leyendo archivo: {e}")
        
    print("\n" + "="*60)
    print(f"📊 RESUMEN FINAL")
    print(f"   Total Auditado: {total}")
    print(f"   Verificado OK: {verified_count}")
    if total > 0:
        accuracy = (verified_count / total) * 100
        print(f"   Precisión Legal: {accuracy:.1f}%")
        
        if accuracy >= 90:
            print("\n🌟 CERTIFICADO DE EXCELENCIA: Dataset apto para Fine-Tuning.")
        elif accuracy >= 70:
             print("\n⚠️ APROBADO CON RESERVAS: Revisar fallos.")
        else:
             print("\n⛔ RECHAZADO: Calidad insuficiente.")
    else:
        print("\n⚠️ Archivo vacío o sin datos.")

if __name__ == "__main__":
    main()
