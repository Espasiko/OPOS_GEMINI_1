
import json
import glob
import os
import re
import random

# 🎯 CONFIGURACIÓN DE FUENTES
SOURCES = {
    "claude_cases": "/home/spas/OPOS_GEMINI_1/scripts/tests/test_claude_*.json",
    "deepseek_cases": "/home/spas/OPOS_GEMINI_1/golden_dataset/premium_final/deepseek_r1_case_*.json",
    "premium_cases": "/home/spas/OPOS_GEMINI_1/golden_dataset/premium_final/gemini_premium_case_manual_*.json",
    "golden_enriched": "/home/spas/OPOS_GEMINI_1/golden_dataset/consolidated/golden_dataset_enriched.jsonl",
    "groq_agentic": "/home/spas/OPOS_GEMINI_1/archive/groq/groq_batch_500_results.jsonl",
    "official_exams": "/home/spas/OPOS_GEMINI_1/golden_dataset/official_exams_qa_FINAL_V3.jsonl" 
}

OUTPUT_FILE = "/home/spas/OPOS_GEMINI_1/MASTER_DATASET_v12_PLATINUM.jsonl"
SYSTEM_PROMPT = "Eres un experto en legislación española y oposiciones a la Seguridad Social. Analiza el caso práctico o pregunta, selecciona la opción correcta y justifica tu respuesta citando la normativa vigente."

def clean_text(text):
    if not isinstance(text, str): return ""
    return text.strip().replace("\r", "")

def shuffle_options(question, options, answer, reasoning):
    """
    Mezcla aleatoriamente las opciones para evitar sesgos posicionales (A/B bias).
    """
    if not options or not answer:
        return question, options, answer, reasoning
        
    ans_char = answer.strip().upper()[0]
    if ans_char not in ['A', 'B', 'C', 'D']:
        return question, options, answer, reasoning
        
    idx_correct = ord(ans_char) - ord('A')
    if idx_correct >= len(options):
        return question, options, answer, reasoning
        
    clean_opts_text = []
    correct_text_content = ""
    
    for i, opt in enumerate(options):
        text = re.sub(r'^[A-D0-9][\)\.]\s*', '', opt).strip()
        clean_opts_text.append(text)
        if i == idx_correct:
            correct_text_content = text
            
    zipped = list(clean_opts_text)
    random.shuffle(zipped)
    
    new_options = []
    new_ans_char = ""
    
    for i, txt in enumerate(zipped):
        letter = chr(ord('A') + i)
        new_options.append(f"{letter}) {txt}")
        if txt == correct_text_content:
            new_ans_char = letter
            
    return question, new_options, new_ans_char, reasoning

def format_chat(question, options, answer, reasoning):
    q, opts, ans, exp = shuffle_options(question, options, answer, reasoning)
    
    opts_str = "\n".join(opts)
    user_content = f"{clean_text(q)}\n\nOpciones:\n{opts_str}"
    
    asst_content = f"selected_option: {clean_text(ans).upper()}\n\nRazonamiento:\n{clean_text(exp)}"
    
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": asst_content}
        ]
    }

def extract_from_json_cases(filepath):
    items = []
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            
            def find_all_qas(obj):
                found = []
                if isinstance(obj, dict):
                    if 'pregunta' in obj: found.append(obj['pregunta'])
                    elif 'preguntas' in obj and isinstance(obj['preguntas'], list): found.extend(obj['preguntas'])
                    for k, v in obj.items():
                        if k not in ['pregunta', 'preguntas']: found.extend(find_all_qas(v))
                elif isinstance(obj, list):
                    for item in obj: found.extend(find_all_qas(item))
                return found

            if 'content' in data and "```json" in str(data['content']):
                try:
                    json_str = data['content'].split("```json")[1].split("```")[0]
                    inner = json.loads(json_str)
                    data = inner
                except: pass

            qas = find_all_qas(data)
            
            for qa in qas:
                q_text = qa.get('enunciado', '') or qa.get('texto', '')
                opts = []
                raw_opts = qa.get('opciones', [])
                if isinstance(raw_opts, list):
                    for o in raw_opts:
                        if isinstance(o, dict): opts.append(f"{o.get('id','').upper()}) {o.get('texto','')}")
                        else: opts.append(str(o))
                elif isinstance(raw_opts, dict):
                    for k,v in raw_opts.items(): opts.append(f"{k.upper()}) {v}")
                
                ans = qa.get('respuesta_correcta', '')
                exp = qa.get('explicacion', '') or qa.get('justificacion_legal', '')
                norma = ""
                if isinstance(exp, dict):
                    exp_text = exp.get('detalle', '') or exp.get('texto', '')
                    norma = exp.get('articulo_aplicable', '')
                    exp = exp_text
                
                full_exp = f"{exp}\nNormativa: {norma}" if norma else str(exp)
                
                if q_text and len(opts)>=4 and ans:
                    items.append(format_chat(q_text, opts, ans, full_exp))
                    
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return items

def extract_from_jsonl(filepath):
    items = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                try:
                    d = json.loads(line)
                    q = d.get('pregunta', '') or d.get('question', '')
                    ans = d.get('respuesta_correcta', '') or d.get('answer', '')
                    exp = d.get('explicacion', '') or d.get('explanation', '') or d.get('reasoning', '')
                    
                    raw_opts = d.get('opciones', []) or d.get('options', [])
                    opts = []
                    if isinstance(raw_opts, list):
                        if len(raw_opts) > 0 and isinstance(raw_opts[0], dict):
                             for o in raw_opts: opts.append(f"{o.get('letra','').upper()}) {o.get('texto','')}")
                        else: opts = raw_opts
                    
                    ans_char = str(ans).strip().upper()[0] if ans else ''
                    
                    if q and len(opts)>=4 and ans_char in ['A','B','C','D']:
                        items.append(format_chat(q, opts, ans_char, str(exp)))
                except: continue
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return items

def main():
    print("🚀 INICIANDO EXTRACCIÓN DE ORO (v12 PLATINUM) + SHUFFLING...")
    all_items = []
    hashes = set()
    
    for key in ["claude_cases", "deepseek_cases", "premium_cases"]:
        pattern = SOURCES[key]
        files = glob.glob(pattern)
        print(f"📂 Procesando {key}: {len(files)} archivos.")
        for f in files:
            extracted = extract_from_json_cases(f)
            count = 0 
            for item in extracted:
                user_content = item['messages'][1]['content']
                h = hash(user_content[:100])
                if h not in hashes:
                    all_items.append(item)
                    hashes.add(h)
                    count += 1
            if count > 0: print(f"   -> {os.path.basename(f)}: +{count} items")
    
    print(f"💎 Casos Complejos extraídos: {len(all_items)}")
    
    for key in ["golden_enriched", "groq_agentic", "official_exams"]:
        filepath = SOURCES[key]
        if os.path.exists(filepath):
            print(f"📂 Procesando {key}...")
            extracted = extract_from_jsonl(filepath)
            count = 0
            for item in extracted:
                user_content = item['messages'][1]['content']
                h = hash(user_content[:100])
                if h not in hashes:
                    all_items.append(item)
                    hashes.add(h)
                    count += 1
            print(f"   -> Añadidos {count} items nuevos.")
    
    print(f"\n💾 Guardando {len(all_items)} items en {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for item in all_items:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
            
    from collections import Counter
    res = [x['messages'][2]['content'].split('selected_option: ')[1].split()[0] for x in all_items]
    print(f"📊 Distribución Final (SHUFFLED): {Counter(res)}")

if __name__ == "__main__":
    main()
