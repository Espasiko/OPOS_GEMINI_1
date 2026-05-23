import os
from neo4j import GraphDatabase

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "opositaia2026")

def check_indexes():
    print("Conectando...")
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    try:
        with driver.session() as session:
            res = session.run("SHOW INDEXES")
            indexes = [r['name'] for r in res]
            print(f"Indices: {indexes}")

            print("\n>> Cálculos y Bases Reguladoras:")
            res = session.run("""
            MATCH (p:Precepto)-[:PERTENECE_A]->(l:Ley)
            WHERE p.texto CONTAINS 'cálculo' OR p.texto CONTAINS 'base reguladora' OR p.texto CONTAINS 'porcentaje'
            RETURN l.siglas as ley, p.numero as art, substring(p.texto, 0, 100) as snippet
            LIMIT 10
            """)
            for r in res:
                print(f"[{r['ley']} - {r['art']}]: {r['snippet'].replace(chr(10), ' ')}")
                
            print("\n>> Recargos e Intereses:")
            res = session.run("""
            MATCH (p:Precepto)-[:PERTENECE_A]->(l:Ley)
            WHERE p.texto CONTAINS 'recargo' OR p.texto CONTAINS 'interés de demora'
            RETURN l.siglas as ley, p.numero as art, substring(p.texto, 0, 100) as snippet
            LIMIT 10
            """)
            for r in res:
                print(f"[{r['ley']} - {r['art']}]: {r['snippet'].replace(chr(10), ' ')}")
                
            print("\n>> LISOS Sanciones:")
            res = session.run("""
            MATCH (p:Precepto)-[:PERTENECE_A]->(l:Ley)
            WHERE l.siglas = 'LISOS' AND (p.texto CONTAINS 'multa' OR p.texto CONTAINS 'euros')
            RETURN l.siglas as ley, p.numero as art, substring(p.texto, 0, 100) as snippet
            LIMIT 10
            """)
            for r in res:
                print(f"[{r['ley']} - {r['art']}]: {r['snippet'].replace(chr(10), ' ')}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    check_indexes()
