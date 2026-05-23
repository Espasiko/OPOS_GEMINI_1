import os
from neo4j import GraphDatabase

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "opositaia2026")

def run_post_etiquetado():
    print("Conectando a Neo4j...")
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    try:
        with driver.session() as session:
            # 1. Update EXCEPCION_A to add verificado_humano: true
            print("Actualizando relaciones EXCEPCION_A con verificado_humano: true...")
            res_update = session.run("""
            MATCH ()-[r:EXCEPCION_A]->()
            SET r.verificado_humano = true
            RETURN count(r) as total_actualizadas
            """)
            total_actualizadas = res_update.single()['total_actualizadas']
            print(f"Total EXCEPCION_A actualizadas: {total_actualizadas}")

            # 2. Create TIENE_EXCEPCION_EN inverse relationships
            print("Creando relaciones inversas TIENE_EXCEPCION_EN...")
            res_inverse = session.run("""
            MATCH (origen:Precepto)-[r:EXCEPCION_A]->(destino:Precepto)
            MERGE (destino)-[ri:TIENE_EXCEPCION_EN {tipo: r.tipo}]->(origen)
            ON CREATE SET ri.creado = datetime(), ri.verificado_humano = true
            RETURN count(ri) as total_inversas
            """)
            total_inversas = res_inverse.single()['total_inversas']
            print(f"Total TIENE_EXCEPCION_EN procesadas (MERGE): {total_inversas}")

            # 3. Create or update Indice node
            print("Creando nodo Indice...")
            res_indice = session.run("""
            MERGE (n:Indice {nombre: "Indice Excepciones"})
            SET n.total_excepciones = $total, 
                n.ultima_actualizacion = datetime()
            RETURN n
            """, total=total_actualizadas)
            
            print("Nodo Indice creado/actualizado correctamente.")
    finally:
        driver.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    run_post_etiquetado()
