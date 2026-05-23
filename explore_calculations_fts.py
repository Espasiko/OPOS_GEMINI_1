import os
from neo4j import GraphDatabase

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "opositaia2026")

def explore_calculations():
    print("Conectando a Neo4j para explorar cálculos usando Full Text Search...")
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    try:
        with driver.session() as session:
            print("\n>> 1. BASES REGULADORAS Y PENSIONES")
            res_br = session.run("""
            CALL db.index.fulltext.queryNodes("precepto_fulltext", '"base reguladora" OR cuantía OR porcentaje') YIELD node, score
            MATCH (node)-[:PERTENECE_A]->(l:Ley)
            RETURN l.siglas as ley, node.numero as art, substring(node.texto, 0, 150) as snippet, score
            ORDER BY score DESC LIMIT 10
            """)
            for record in res_br:
                print(f"[{record['ley']} - {record['art']}]: {record['snippet'].replace(chr(10), ' ')}...")
                
            print("\n>> 2. RECARGOS E INTERESES")
            res_rec = session.run("""
            CALL db.index.fulltext.queryNodes("precepto_fulltext", 'recargo OR "interés de demora" OR "tipo de cotización"') YIELD node, score
            MATCH (node)-[:PERTENECE_A]->(l:Ley)
            RETURN l.siglas as ley, node.numero as art, substring(node.texto, 0, 150) as snippet, score
            ORDER BY score DESC LIMIT 10
            """)
            for record in res_rec:
                print(f"[{record['ley']} - {record['art']}]: {record['snippet'].replace(chr(10), ' ')}...")
                
            print("\n>> 3. INFRACCIONES Y SANCIONES")
            res_inf = session.run("""
            CALL db.index.fulltext.queryNodes("precepto_fulltext", 'multa OR sanción OR importe OR grados') YIELD node, score
            MATCH (node)-[:PERTENECE_A]->(l:Ley)
            WHERE l.siglas = 'LISOS'
            RETURN l.siglas as ley, node.numero as art, substring(node.texto, 0, 150) as snippet, score
            ORDER BY score DESC LIMIT 10
            """)
            for record in res_inf:
                print(f"[{record['ley']} - {record['art']}]: {record['snippet'].replace(chr(10), ' ')}...")
                
            print("\n>> 4. FÓRMULAS MATEMÁTICAS EXPLÍCITAS")
            res_math = session.run("""
            CALL db.index.fulltext.queryNodes("precepto_fulltext", 'multiplicado OR dividido OR cociente OR fracción') YIELD node, score
            MATCH (node)-[:PERTENECE_A]->(l:Ley)
            RETURN l.siglas as ley, node.numero as art, substring(node.texto, 0, 150) as snippet, score
            ORDER BY score DESC LIMIT 10
            """)
            for record in res_math:
                print(f"[{record['ley']} - {record['art']}]: {record['snippet'].replace(chr(10), ' ')}...")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    explore_calculations()
