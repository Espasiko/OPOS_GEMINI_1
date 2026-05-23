import re
import sys
from neo4j import GraphDatabase

# Configuración
URI = "bolt://localhost:7687"
USER = "neo4j"
PASS = "opositaia2026"
MD_FILE_PATH = "/home/spas/.gemini/antigravity/brain/44a94c17-0e1d-45ba-bd66-0023f94d2497/ANALISIS_MANUAL_Y_PLAN_ETIQUETADO.md"

def extract_cypher_queries(filepath):
    queries = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Busca bloques de código cypher
    pattern = re.compile(r'```cypher(.*?)```', re.DOTALL)
    matches = pattern.findall(content)
    
    for match in matches:
        query = match.strip()
        if query:
            queries.append(query)
            
    return queries

def execute_queries(queries):
    print(f"Encontradas {len(queries)} consultas Cypher en el documento.")
    
    driver = GraphDatabase.driver(URI, auth=(USER, PASS))
    
    total_relationships_created = 0
    total_relationships_updated = 0
    
    try:
        with driver.session() as session:
            for i, query in enumerate(queries):
                # Omitir queries comentadas enteramente si las hay, o dividir múltiples sentencias si neo4j-driver lo requiere
                # neo4j-driver puede tener problemas si se le pasan múltiples sentencias MERGE separadas por ';' en una sola llamada a .run() a veces.
                # Es más seguro separar por ';' y ejecutar cada una.
                statements = [s.strip() for s in query.split(';') if s.strip()]
                
                for stmt in statements:
                    # Si es un comentario puro, omitir
                    if stmt.startswith('//'):
                        lines = stmt.split('\n')
                        valid_lines = [l for l in lines if not l.strip().startswith('//')]
                        stmt = '\n'.join(valid_lines).strip()
                        if not stmt:
                            continue

                    print(f"Ejecutando bloque [{i+1}/{len(queries)}]...")
                    try:
                        result = session.run(stmt)
                        summary = result.consume()
                        created = summary.counters.relationships_created
                        total_relationships_created += created
                        if created > 0:
                            print(f"  -> Creadas {created} relaciones.")
                        else:
                            # It's possible the relationship already existed and was updated, or no nodes matched
                            properties_set = summary.counters.properties_set
                            if properties_set > 0:
                                print(f"  -> Propiedades actualizadas: {properties_set}")
                            else:
                                print(f"  -> No se crearon relaciones (puede que los nodos no hicieran MATCH).")
                    except Exception as e:
                        print(f"  -> ERROR al ejecutar la sentencia: {e}")
                        print(f"  -> Sentencia problemática: {stmt[:100]}...")
                        
    finally:
        driver.close()
        
    print(f"\n==========================================")
    print(f"INYECCIÓN COMPLETADA.")
    print(f"Total de relaciones :EXCEPCION_A creadas: {total_relationships_created}")
    print(f"==========================================")

if __name__ == "__main__":
    queries = extract_cypher_queries(MD_FILE_PATH)
    execute_queries(queries)
