
import json
import tqdm

input_file = "/home/spas/OPOS_GEMINI_1/gastos_ tokens/MASTER_DATASET_v10_COLAB_READY.jsonl"
output_file = "/home/spas/OPOS_GEMINI_1/gastos_ tokens/MASTER_DATASET_v10_FIXED.jsonl"

def fix_text(text):
    if not isinstance(text, str):
        return text
    try:
        # Attempt to reverse double-encoding
        fixed = text.encode('latin1').decode('utf-8')
        # If the fix results in a string different from original AND smaller/same length (usually smaller due to 2 chars -> 1)
        # But mostly we care that it's different and valid.
        if fixed != text:
            return fixed
        return text
    except UnicodeDecodeError:
        # If it fails to decode as UTF-8 after latin1 encode, it means it contained REAL high-bit chars
        # that were correctly encoded and mapped to bytes that are NOT valid UTF-8 sequences alone.
        # This usually means the text was ALREADY correct (e.g. contains real 'ó').
        return text
    except UnicodeEncodeError:
        # Should not happen for latin1 unless chars are > 255, which means they are definitely not double-encoded latin1 garbage.
        return text

fixed_count = 0
total_count = 0

with open(input_file, 'r', encoding='utf-8') as fin, \
     open(output_file, 'w', encoding='utf-8') as fout:
    
    for line in fin:
        total_count += 1
        try:
            data = json.loads(line)
            
            # recursive fix for all string fields
            def recursive_fix(obj):
                global fixed_count
                if isinstance(obj, str):
                    new_val = fix_text(obj)
                    if new_val != obj:
                        # Just counting lines changed, roughly
                        pass
                    return new_val
                elif isinstance(obj, list):
                    return [recursive_fix(x) for x in obj]
                elif isinstance(obj, dict):
                    return {k: recursive_fix(v) for k, v in obj.items()}
                return obj
            
            # Check if this line actually needs fixing to increment counter correctly
            curr_str = json.dumps(data)
            new_data = recursive_fix(data)
            new_str = json.dumps(new_data)
            
            if curr_str != new_str:
                fixed_count += 1
                
            fout.write(json.dumps(new_data, ensure_ascii=False) + "\n")
            
        except json.JSONDecodeError:
            print(f"Skipping invalid JSON at line {total_count}")

print(f"Done! Fixed encoding in {fixed_count} out of {total_count} lines.")
print(f"Saved to: {output_file}")
