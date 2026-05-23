MD_FILE_PATH = "/home/spas/.gemini/antigravity/brain/44a94c17-0e1d-45ba-bd66-0023f94d2497/ANALISIS_MANUAL_Y_PLAN_ETIQUETADO.md.fixed"

with open(MD_FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('n.id CONTAINS "Disposición final séptima" AND n.id CONTAINS "1/2004"', 'n.id CONTAINS "7ª" AND n.id CONTAINS "1/2004"')
content = content.replace('n.id CONTAINS "Disposición adicional primera" AND n.id CONTAINS "1/2004"', 'n.id CONTAINS "1ª" AND n.id CONTAINS "1/2004"')

content = content.replace('"2064/1995"', '"RD 2064/1995"')
content = content.replace('"1415/2004"', '"RD 1415/2004"')
content = content.replace('"1993/1995"', '"RD 1993/1995"')

# Also fix the weird Ley 50/1997 double MATCH block
import re
content = re.sub(r'MATCH\s+\(n:Precepto\)\s+WHERE\s+[^\n]*?Ley 50/1997[^\n]*?\n\s*//[^\n]*?\n\s*//[^\n]*?\n\s*MATCH', 'MATCH', content, flags=re.DOTALL)

with open(MD_FILE_PATH, 'w', encoding='utf-8') as f:
    f.write(content)
