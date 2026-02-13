
import json
import glob
import os
from pathlib import Path

INPUT_PATTERNS = [
    "/home/spas/OPOS_GEMINI_1/scripts/tests/test_claude_*.json",
    "/home/spas/OPOS_GEMINI_1/scripts/tests/test_mistral_vs_claude*.json"
]
TARGET_FILE = "/home/spas/OPOS_GEMINI_1/MASTER_DATASET_v11_UTF8_FIXED.jsonl"
SYSTEM_PROMPT = "Eres un experto en oposiciones de la Seguridad Social y Derecho Administrativo. Analiza el siguiente caso práctico o pregunta compleja y proporciona la respuesta correcta razonada, citando la normativa aplicable."

def extract_claude_content(filepath):
    items = []
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            
            # Helper to process a single QA object
            def process_qa(qa_obj):
                # Check structure
                if not qa_obj.get('pregunta'): return None
                
                p = qa_obj['pregunta']
                enunciado = p.get('enunciado', '')
                if not enunciado: return None
                
                # Options
                opts = []
                raw_opts = p.get('opciones', [])
                if isinstance(raw_opts, list):
                    for o in raw_opts:
                        opts.append(f"{o.get('id', '').upper()}) {o.get('texto', '')}")
                elif isinstance(raw_opts, dict):
                    for k,v in raw_opts.items():
                        opts.append(f"{k.upper()}) {v}")
                        
                # Answer
                ans = p.get('respuesta_correcta', '').upper()
                
                # Explanation
                expl = p.get('explicacion', {})
                if isinstance(expl, dict):
                    text_expl = expl.get('detalle', '') or expl.get('texto', '')
                    art = expl.get('articulo_aplicable', '')
                    full_expl = f"{text_expl}\n\nNormativa: {art}"
                else:
                    full_expl = str(expl)
                    
                return (enunciado, opts, ans, full_expl)

            # Structure 1: Root object is the wrapper
            if 'content' in data:
                # Content is a string containing JSON code block? 
                content_str = data['content']
                if "```json" in content_str:
                    json_str = content_str.split("```json")[1].split("```")[0]
                    inner_data = json.loads(json_str)
                    res = process_qa(inner_data)
                    if res: items.append(res)
            
            # Structure 2: Direct keys "claude" -> "content"
            elif 'claude' in data:
                c_data = data['claude']
                if 'content' in c_data:
                    content_str = c_data['content']
                    if "```json" in content_str:
                        json_str = content_str.split("```json")[1].split("```")[0]
                        inner_data = json.loads(json_str)
                        res = process_qa(inner_data)
                        if res: items.append(res)
                        
    except Exception as e:
        print(f"Skipping {filepath}: {e}")
        
    return items

def main():
    print("💎 Buscando Casos 'Oro Puro' de Claude...")
    all_files = []
    for p in INPUT_PATTERNS:
        all_files.extend(glob.glob(p))
        
    total_new = 0
    
    # Read existing to avoid dupes (hash check)
    existing_hashes = set()
    if os.path.exists(TARGET_FILE):
        with open(TARGET_FILE, 'r') as f:
            for line in f:
                try:
                    d = json.loads(line)
                    user_msg = d['messages'][1]['content']
                    h = hash(user_msg.split('\n')[0][:50])
                    existing_hashes.add(h)
                except: pass
    
    new_items_formatted = []
    
    for fw in all_files:
        extracted = extract_claude_content(fw)
        for q, opts, ans, exp in extracted:
            h = hash(q[:50])
            if h in existing_hashes:
                continue
            
            # Format
            user_text = f"{q}\n\nOpciones:\n" + "\n".join(opts)
            asst_text = f"selected_option: {ans}\n\nRazonamiento:\n{exp}"
            
            msg = {
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_text},
                    {"role": "assistant", "content": asst_text}
                ]
            }
            new_items_formatted.append(msg)
            existing_hashes.add(h)
            total_new += 1
            
    if total_new > 0:
        print(f"✨ Encontrados {total_new} casos nuevos. Añadiendo al dataset...")
        with open(TARGET_FILE, 'a') as f: # Append mode
            for item in new_items_formatted:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        print("✅ Integración completada.")
    else:
        print("⚠️ No se encontraron casos nuevos (o ya existían).")

if __name__ == "__main__":
    main()
