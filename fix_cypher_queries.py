import re
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = "neo4j"
PASS = "opositaia2026"
MD_FILE_PATH = "/home/spas/.gemini/antigravity/brain/44a94c17-0e1d-45ba-bd66-0023f94d2497/ANALISIS_MANUAL_Y_PLAN_ETIQUETADO.md"

with open(MD_FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix norm names
content = content.replace('"39/2015"', '"LPAC"')
content = content.replace('"40/2015"', '"LRJSP"')
content = content.replace('"5/2000"', '"LISOS"')
content = content.replace('"20/2007"', '"LETA"')
content = content.replace('"Estatuto de los Trabajadores"', '"ET"')
content = content.replace('"2/2015"', '"ET"')
content = content.replace('"8/2015"', '"TRLGSS"')
content = content.replace('"LGSS"', '"TRLGSS"')
content = content.replace('"5/2015"', '"TREBEP"')

# Now, we have a problem where some IDs don't have "Art. ". 
# For example, `n.id CONTAINS "Art. 13"` might not match `13 LPAC`.
# But `n.id STARTS WITH "13 "` will match `13 LPAC`.
# Actually, we can just replace `n.id CONTAINS "Art. X"` with `(n.id CONTAINS "Art. X" OR n.id STARTS WITH "X ")`
# Or better, just let regex do it.

def replace_art(match):
    art_num = match.group(1)
    return f'(n.id CONTAINS "Art. {art_num}" OR n.id STARTS WITH "{art_num} " OR n.id = "{art_num}")'

# Find n.id CONTAINS "Art. <number>"
content = re.sub(r'n\.id\s+CONTAINS\s+"Art\.\s+([^"]+)"', replace_art, content)

with open(MD_FILE_PATH + ".fixed", 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed queries written to .fixed file.")
