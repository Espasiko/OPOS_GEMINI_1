import re
import sys
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = "neo4j"
PASS = "opositaia2026"
MD_FILE_PATH = "/home/spas/.gemini/antigravity/brain/44a94c17-0e1d-45ba-bd66-0023f94d2497/ANALISIS_MANUAL_Y_PLAN_ETIQUETADO.md.fixed"

def extract_cypher_queries(filepath):
    queries = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = re.compile(r'```cypher(.*?)```', re.DOTALL)
    matches = pattern.findall(content)
    
    for match in matches:
        query = match.strip()
        if query:
            # Strip comments
            lines = query.split('\n')
            clean_lines = [l for l in lines if not l.strip().startswith('//')]
            query = '\n'.join(clean_lines).strip()
            queries.append(query)
            
    return queries

def execute_queries(queries):
    print(f"Encontradas {len(queries)} consultas Cypher en el documento.")
    
    driver = GraphDatabase.driver(URI, auth=(USER, PASS))
    
    total_created = 0
    total_updated = 0
    zero_matches = 0
    
    try:
        with driver.session() as session:
            for i, stmt in enumerate(queries):
                # Ensure we run each MERGE carefully.
                print(f"\n[{i+1}/{len(queries)}] Ejecutando...")
                try:
                    result = session.run(stmt)
                    summary = result.consume()
                    created = summary.counters.relationships_created
                    props = summary.counters.properties_set
                    
                    # We can also verify if any nodes were MATCHed!
                    # A trick is that if created == 0 and props == 0, maybe 0 nodes matched, or maybe all props were identical.
                    # But if we want to be sure, let's just log created and props.
                    if created > 0:
                        print(f"  -> OK: Creadas {created} relaciones.")
                        total_created += created
                    elif props > 0:
                        print(f"  -> OK: Propiedades actualizadas: {props} (relaciones existentes).")
                        total_updated += props
                    else:
                        print(f"  -> WARNING: 0 creadas, 0 actualizadas. (Posible MATCH fallido o ya estaba idéntico).")
                        zero_matches += 1
                        print(f"     Sentencia: {stmt[:100]}...")
                except Exception as e:
                    print(f"  -> ERROR: {e}")
                    print(f"     Sentencia: {stmt[:100]}...")
                    
    finally:
        driver.close()
        
    print(f"\n==========================================")
    print(f"INYECCIÓN COMPLETADA.")
    print(f"Total nuevas relaciones: {total_created}")
    print(f"Total de propiedades actualizadas: {total_updated}")
    print(f"Total de consultas sin efecto: {zero_matches}")
    print(f"==========================================")

if __name__ == "__main__":
    queries = extract_cypher_queries(MD_FILE_PATH)
    execute_queries(queries)
