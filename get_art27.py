import os
from neo4j import GraphDatabase

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "opositaia2026")

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
with driver.session() as session:
    res = session.run("""
    MATCH (p:Precepto)-[:PERTENECE_A]->(l:Ley)
    WHERE l.siglas CONTAINS 'LGSS' AND p.numero = '27'
    RETURN substring(p.texto, 0, 500) as snippet
    """)
    for r in res:
        print(f"{r['snippet']}")
driver.close()
