
import json

bad_line = '{"instruction": "Â¿QuÃ© se considera recaÃ­da en un mismo proceso de incapacidad temporal segÃºn el art. 169.2 TRLGSS?", "input": "", "output": "A"}'

try:
    data = json.loads(bad_line)
    text = data['instruction']
    print(f"Original: {text}")
    
    fixed = text.encode('latin1').decode('utf-8')
    print(f"Fixed:    {fixed}")
except Exception as e:
    print(f"Error: {e}")
