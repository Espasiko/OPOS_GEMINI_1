import json
import os

input_file = "/home/spas/OPOS_GEMINI_1/gastos_ tokens/MASTER_DATASET_v9_GOLD_OPTIMIZED_MAPPED.jsonl"
output_file = "/home/spas/OPOS_GEMINI_1/gastos_ tokens/MASTER_DATASET_v10_COLAB_READY.jsonl"

def fix_dataset():
    print(f"Processing {input_file}...")
    valid_count = 0
    error_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line_num, line in enumerate(infile, 1):
            line = line.strip()
            if not line:
                continue
            
            try:
                data = json.loads(line)
                
                # Default mapping for "question" / "answer" format
                instruction = ""
                output = ""
                
                if "question" in data and "answer" in data:
                    instruction = data["question"]
                    output = data["answer"]
                # Fallback for "instruction" / "output" if already present
                elif "instruction" in data and "output" in data:
                    instruction = data["instruction"]
                    output = data["output"]
                # Fallback for "prompt" / "completion"
                elif "prompt" in data and "completion" in data:
                    instruction = data["prompt"]
                    output = data["completion"]
                # Fallback for messages (ShareGPT/ChatML) - flatten to single turn if possible
                elif "messages" in data:
                     # Simple flattening for single turn QA
                     for msg in data["messages"]:
                         if msg["role"] == "user":
                             instruction = msg["content"]
                         elif msg["role"] == "assistant":
                             output = msg["content"]
                
                if not instruction or not output:
                    print(f"Skipping line {line_num}: Missing vital fields. Keys found: {list(data.keys())}")
                    error_count += 1
                    continue

                # Normalize options to ensure consistency (List of strings)
                standardized_options = []
                if "options" in data:
                    raw_opts = data["options"]
                    if isinstance(raw_opts, list):
                        for opt in raw_opts:
                            if isinstance(opt, dict):
                                # Format 1: {'letra': 'A', 'texto': '...'}
                                if 'letra' in opt and 'texto' in opt:
                                    standardized_options.append(f"{opt['letra']}) {opt['texto']}")
                                # Format 2: {'A': '...'}
                                else:
                                    for key, val in opt.items():
                                        if len(key) == 1 and key.isupper(): # Assume single letter key is option label
                                            standardized_options.append(f"{key}) {val}")
                            elif isinstance(opt, str):
                                standardized_options.append(opt)
                
                # Create Alpaca format object
                # FIX: Add 'question'/'answer' aliases to satisfy custom naming conventions in Colab scripts
                new_entry = {
                    "instruction": instruction,
                    "input": "", 
                    "output": output,
                    "question": instruction, # Alias for compatibility
                    "answer": output,        # Alias for compatibility
                    "options": standardized_options # Standardized field
                }
                
                outfile.write(json.dumps(new_entry, ensure_ascii=False) + "\n")
                valid_count += 1
                
            except json.JSONDecodeError:
                print(f"Skipping line {line_num}: Invalid JSON")
                error_count += 1
            except Exception as e:
                print(f"Skipping line {line_num}: Unexpected error {e}")
                error_count += 1

    print("-" * 30)
    print(f"Processing Complete.")
    print(f"Total Valid Lines Written: {valid_count}")
    print(f"Total Errors/Skipped: {error_count}")
    print(f"Output saved to: {output_file}")

if __name__ == "__main__":
    fix_dataset()
