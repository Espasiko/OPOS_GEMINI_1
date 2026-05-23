from neo4j import GraphDatabase
import os

uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
user = os.environ.get("NEO4J_USER", "neo4j")
password = os.environ.get("NEO4J_PASSWORD", "opositaia2026")

def check_db():
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        print("--- Constraints ---")
        res = session.run("SHOW CONSTRAINTS")
        for record in res:
            print(record['name'], record['type'], record['labelsOrTypes'], record['properties'])
        
        print("\n--- Relaciones EXCEPCION_A ---")
        res = session.run("MATCH ()-[r:EXCEPCION_A]->() RETURN count(r) as count")
        print("Total EXCEPCION_A:", res.single()['count'])
        
        res = session.run("MATCH ()-[r:EXCEPCION_A]->() RETURN r LIMIT 1")
        record = res.single()
        if record:
            print("Ejemplo de propiedades:", list(record['r'].keys()))
            
        print("\n--- Relaciones TIENE_EXCEPCION_EN ---")
        res = session.run("MATCH ()-[r:TIENE_EXCEPCION_EN]->() RETURN count(r) as count")
        print("Total TIENE_EXCEPCION_EN:", res.single()['count'])
        
        print("\n--- Nodo Indice ---")
        res = session.run("MATCH (n:Indice) RETURN n LIMIT 1")
        record = res.single()
        if record:
            print("Nodo Indice existe:", dict(record['n']))
        else:
            print("No existe nodo Indice.")

check_db()
