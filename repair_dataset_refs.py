
import json
import requests
import os

BACKEND_URL = "http://127.0.0.1:8000"
INPUT_FILE = "dataset_generator/qa_mistral_batches_20_12/qa_mass_verified_1766223039.jsonl"
OUTPUT_FILE = "dataset_generator/qa_mistral_batches_20_12/qa_mass_verified_1766223039_repaired.jsonl"

def fix_reference(item):
    refs = item.get("referencias", [])
    has_generic = any("Document" in r or "Artículo" == r or len(r) < 5 for r in refs)
    
    if has_generic:
        query = f"{item['pregunta']} {item.get('respuesta_correcta', '')}"
        try:
            resp = requests.post(f"{BACKEND_URL}/api/rag/search", json={"query": query, "top_k": 1, "min_score": 0.1})
            if resp.status_code == 200:
                docs = resp.json().get("documents", [])
                if docs:
                    meta = docs[0].get("metadata", {})
                    # Try to build a specific ref: Art X Ley Y
                    law = meta.get("norma_nombre", meta.get("material_nombre", "Ref Legal"))
                    art = meta.get("articulo", "")
                    new_ref = f"{law} - Art. {art}" if art else law
                    item["referencias"] = [new_ref]
                    item["_repaired"] = True
                    print(f"✅ Repaired: {item['pregunta'][:50]}... -> {new_ref}")
        except Exception as e:
            print(f"❌ Error repairing: {e}")
            
    return item

def main():
    with open(INPUT_FILE, "r") as f_in, open(OUTPUT_FILE, "w") as f_out:
        for line in f_in:
            if not line.strip(): continue
            item = json.loads(line)
            repaired_item = fix_reference(item)
            f_out.write(json.dumps(repaired_item, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
