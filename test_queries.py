import re
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = "neo4j"
PASS = "opositaia2026"
MD_FILE_PATH = "/home/spas/.gemini/antigravity/brain/44a94c17-0e1d-45ba-bd66-0023f94d2497/ANALISIS_MANUAL_Y_PLAN_ETIQUETADO.md.fixed"

with open(MD_FILE_PATH, 'r') as f:
    content = f.read()

pattern = re.compile(r'MATCH\s+\(n:Precepto\)\s+WHERE\s+(.*?)\s*MERGE', re.DOTALL)
matches = pattern.findall(content)

driver = GraphDatabase.driver(URI, auth=(USER, PASS))
with driver.session() as session:
    for i, where_clause in enumerate(matches):
        query = f"MATCH (n:Precepto) WHERE {where_clause} RETURN count(n) AS c"
        try:
            res = session.run(query)
            count = res.single()['c']
            if count == 0:
                print(f"[{i}] ZERO MATCHES: {where_clause.strip()}")
        except Exception as e:
            print(f"[{i}] ERROR: {where_clause.strip()} - {e}")
