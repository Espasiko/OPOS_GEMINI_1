
import json
import re
import random
import glob
from pathlib import Path

# Config
OUTPUT_FILE = "/home/spas/OPOS_GEMINI_1/MASTER_DATASET_v11_REMASTERED.jsonl"
TARGET_SIZE = 5000

# Input sources
SOURCES = [
    "/home/spas/OPOS_GEMINI_1/dataset_generator/dataset_output/MEGA_DATASET_v3_MASTER.jsonl",
    "/home/spas/OPOS_GEMINI_1/golden_dataset/consolidated/golden_dataset_consolidated_20251221.jsonl",
    "/home/spas/OPOS_GEMINI_1/golden_dataset/consolidated/FINAL_TRAINING_DATASET_20251221.jsonl",
    "/home/spas/OPOS_GEMINI_1/qa_agentic_groq_20251219_182357.jsonl",
    "/home/spas/OPOS_GEMINI_1/qa_mistral_studio_v2_20251219_213835.jsonl",
    "/home/spas/OPOS_GEMINI_1/golden_dataset/consolidated/golden_dataset_enriched.jsonl",
    "/home/spas/OPOS_GEMINI_1/golden_dataset/official_exams_qa_FINAL_V3.jsonl",
    "/home/spas/OPOS_GEMINI_1/kaggle_dataset/MASTER_DATASET_v10_FIXED.jsonl"
]
# Add wildcard sources
SOURCES.extend(glob.glob("/home/spas/OPOS_GEMINI_1/qa_mistral_real_backend_*.jsonl"))

def parse_options_from_text(text):
    """Extract options from text if they are embedded."""
    options = []
    # Look for A) ... B) ... format or ["A)..."]
    
    # Try finding JSON-like array first
    match = re.search(r'\[\s*".*?"\s*\]', text, re.DOTALL)
    if match:
        try:
            # fixes for single quotes vs double quotes
            json_str = match.group(0).replace("'", '"')
            options = json.loads(json_str)
            if len(options) == 4:
                return options
        except: pass
        
    # RegExp fallback
    pat = r'([A-D])\)\s+(.*?)(?=(?:[A-D]\)|$))'
    matches = re.findall(pat, text, re.DOTALL)
    if len(matches) >= 4:
        return [f"{opt.upper()}) {txt.strip()}" for opt, txt in matches[:4]]
        
    return []

def normalize_item(data):
    """Convert any format to standardized info dict."""
    q = ""
    opts = []
    ans = ""
    exp = ""
    
    # CASE 1: Chat/Reasoning format (Alpaca)
    if 'instruction' in data and 'output' in data:
        full_inst = data['instruction']
        output = data['output']
        
        # Extract Question (remove options if present)
        q = full_inst.split("\n\nOpciones:")[0].split("Opciones:")[0].strip()
        
        # Extract Options
        if 'Opciones:' in full_inst:
            opts = parse_options_from_text(full_inst)
        
        # Extract Answer
        # Looking for "Respuesta: A" or "Respuesta Correcta: B"
        m = re.search(r'Respuesta(?: Correcta)?:?\s*([A-D])', output, re.IGNORECASE)
        if m:
            ans = m.group(1).upper()
            
        # Extract Explanation
        exp = output.replace(f"Respuesta: {ans}", "").replace(f"Respuesta Correcta: {ans}", "").strip()
        
    # CASE 2: Structured QA
    elif 'pregunta' in data or 'question' in data:
        q = data.get('pregunta') or data.get('question')
        
        raw_opts = data.get('opciones') or data.get('options')
        if isinstance(raw_opts, list):
            opts = raw_opts
        elif isinstance(raw_opts, str):
            opts = parse_options_from_text(raw_opts)
            
        ans_raw = data.get('respuesta_correcta') or data.get('answer') or data.get('respuesta')
        if ans_raw:
             m = re.search(r'([A-D])', str(ans_raw).upper())
             if m: ans = m.group(1)
             
        exp = data.get('explicacion') or data.get('explanation') or data.get('reasoning') or ""
        
    return q, opts, ans, exp

def shuffle_item(q, opts, ans, exp):
    """Shuffle options and update answer."""
    if len(opts) != 4 or ans not in ['A', 'B', 'C', 'D']:
        return None
        
    # Extract text from "A) Text"
    clean_opts = []
    for o in opts:
        # Remove "A) ", "a. ", etc
        clean = re.sub(r'^[A-D][\)\.]\s*', '', o).strip()
        clean_opts.append(clean)
        
    # Identify correct text
    idx = ord(ans) - ord('A')
    correct_text = clean_opts[idx]
    
    # Shuffle
    random.shuffle(clean_opts)
    
    # Find new index
    new_idx = clean_opts.index(correct_text)
    new_ans = chr(ord('A') + new_idx)
    
    # Re-label options
    final_opts = [f"{chr(ord('A')+i)}) {text}" for i, text in enumerate(clean_opts)]
    
    return q, final_opts, new_ans, exp

def main():
    print("🚀 STARTING V11 REMASTER PROCESS")
    
    # 1. Collect
    items = []
    seen_hashes = set()
    
    for src in SOURCES:
        if not Path(src).exists(): continue
        print(f"Reading {Path(src).name}...")
        
        with open(src, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    q, opts, ans, exp = normalize_item(data)
                    
                    if q and len(opts)==4 and ans:
                        # Deduplicate by question text
                        h = hash(q[:50])
                        if h in seen_hashes: continue
                        seen_hashes.add(h)
                        
                        # Process
                        res = shuffle_item(q, opts, ans, exp)
                        if res:
                            items.append(res)
                except: continue
                
    print(f"Found {len(items)} valid unique items.")
    
    # 2. Format as Chat
    print("Formatting and saving...")
    
    system_prompt = "Eres un experto en oposiciones de la Seguridad Social. Responde a la pregunta tipo test seleccionando la opción correcta y justificando tu respuesta basándote estrictamente en la normativa legal vigente."
    
    with open(OUTPUT_FILE, 'w') as f:
        count = 0
        for q, opts, ans, exp in items:
            
            # Format User Message
            user_content = f"{q}\n\nOpciones:\n" + "\n".join(opts)
            
            # Format Assistant Message
            # Encapsulate logic
            assistant_content = f"selected_option: {ans}\n\nRazonamiento:\n{exp}"
            
            msg = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": assistant_content}
                ]
            }
            f.write(json.dumps(msg, ensure_ascii=False) + '\n')
            count += 1
            
    print(f"✅ DONE. Saved {count} items to {OUTPUT_FILE}")
    
    # Stats
    answers = [x[2] for x in items] # Check shuffled distribution
    from collections import Counter
    print("New Answer Distribution:", Counter(answers))

if __name__ == "__main__":
    main()
