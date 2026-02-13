
import json
import re
import os
from collections import Counter
from pathlib import Path

# Files identified from user list and exploration
FILES_TO_ANALYZE = [
    "/home/spas/OPOS_GEMINI_1/qa_agentic_groq_20251219_182357.jsonl",
    "/home/spas/OPOS_GEMINI_1/qa_mistral_studio_v2_20251219_213835.jsonl",
    "/home/spas/OPOS_GEMINI_1/dataset_generator/dataset_output/MEGA_DATASET_v3_MASTER.jsonl",
    # Add patterns for the others
]

# Directory scanning for the user's list
SEARCH_DIRS = ["/home/spas/OPOS_GEMINI_1"]
PATTERNS = [
    "qa_mistral_real_backend_*.jsonl",
    "qa_final_*.log",
    "qa_FINAL_*.log",
    "qa_generation_*.log",
    "qa_RAG_*.log",
    "qa_REAL_*.log",
    "qa_mistral_*.log"
]

def find_files():
    found_files = []
    for pattern in PATTERNS:
        # crude glob
        import glob
        for p in glob.glob(os.path.join(SEARCH_DIRS[0], pattern)):
            found_files.append(p)
    return list(set(found_files + FILES_TO_ANALYZE))

def analyze_file(filepath):
    valid_items = 0
    with_reasoning = 0
    answer_dist = Counter()
    types_dist = Counter()
    
    print(f"--- Analyzing {os.path.basename(filepath)} ---")
    
    try:
        with open(filepath, 'r', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                
                data = None
                # Try JSON parse
                try:
                    data = json.loads(line)
                except:
                    # Try finding JSON blob in log line
                    match = re.search(r'(\{.*\})', line)
                    if match:
                        try:
                            data = json.loads(match.group(1))
                        except: pass
                
                if not data: continue
                
                # Check if it looks like a dataset item
                # Minimal requirements: question (or pregunta) and answer (or respuesta_correcta)
                q = data.get('question') or data.get('pregunta')
                a = data.get('answer') or data.get('respuesta_correcta') or data.get('correct_answer')
                
                if q and a:
                    valid_items += 1
                    
                    # Check reasoning/explanation
                    if data.get('reasoning') or data.get('explicacion') or data.get('explanation') or data.get('thinking'):
                        with_reasoning += 1
                        
                    # Check Answer Dist
                    a_norm = str(a).strip().upper()[0] if str(a).strip() else '?'
                    if a_norm in ['A', 'B', 'C', 'D']:
                        answer_dist[a_norm] += 1
                        
                    # Check Type
                    t = data.get('tipo', 'unknown')
                    types_dist[t] += 1

    except Exception as e:
        print(f"Error reading file: {e}")

    return {
        "file": os.path.basename(filepath),
        "valid": valid_items,
        "reasoning": with_reasoning,
        "answers": dict(answer_dist),
        "types": dict(types_dist)
    }

def main():
    all_files = find_files()
    summary = []
    
    total_valid = 0
    total_reasoning = 0
    
    for f in all_files:
        if os.path.exists(f):
            stats = analyze_file(f)
            if stats['valid'] > 0:
                summary.append(stats)
                total_valid += stats['valid']
                total_reasoning += stats['reasoning']
                
                # Print quick stat
                print(f"  Valid: {stats['valid']}, Reasoning: {stats['reasoning']}")
                print(f"  Answers: {stats['answers']}")
                print(f"  Types: {stats['types']}")
                print("")

    print("="*60)
    print(f"TOTAL VALID ITEMS FOUND: {total_valid}")
    print(f"TOTAL WITH REASONING: {total_reasoning}")
    print("="*60)
    
    # Suggestion
    print("\nSUGGESTED ACTION:")
    print("We should merge these files, normalize fields (pregunta->question, respuesta->answer),")
    print("shuffle options to fix answer distribution, and filter for high quality (reasoning present).")

if __name__ == "__main__":
    main()
