import os
import re
from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "opositaia2026"

def run_purge():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    
    # Textos obligatorios a inyectar directamente (Mockeados si no están en Qdrant fijos o para asegurar disponibilidad plena)
    # Decreto 1646/1972 (Importante para BR muerte/viudedad/IT)
    decreto_1646_art3 = "Decreto 1646/1972 - Artículo 3. La base reguladora de las prestaciones por incapacidad temporal se obtendrá dividiendo el importe de la base de cotización del trabajador en el mes anterior al de la fecha de iniciación de la incapacidad por el número de días a que corresponda dicha cotización."
    decreto_1646_art7 = "Decreto 1646/1972 - Artículo 7.2. La base reguladora de las pensiones de muerte y supervivencia derivadas de contingencias comunes será el cociente de dividir por 28 la suma de las bases de cotización del causante durante un período ininterrumpido de 24 meses elegidos por los beneficiarios dentro de los 15 años inmediatamente anteriores a la fecha del hecho causante."
    
    # Orden PJC/178/2025 Tipos Cotización 2026
    orden_pjc_2025 = "Orden PJC/178/2025 - Tipos de Cotización 2026. El tipo de cotización por horas extraordinarias estructurales será del 28,30 por ciento (23,60 por ciento a cargo de la empresa y 4,70 por ciento a cargo del trabajador). El Mecanismo de Equidad Intergeneracional (MEI) será del 0,90 por ciento (0,75% empresa, 0,15% trabajador)."
    
    with driver.session() as s:
        # Purga de basura detectada
        trash_ids = [
            "Real Decreto 842/2002",
            "Real Decreto 99/1986",
            "Norma BOE-A",
            "Resolución de 10 de septiembre de 2009",
            "Resolución de 5 de marzo de 1981",
        ]
        
        bajas = 0
        for b in trash_ids:
            res = s.run("MATCH (a:Articulo) WHERE a.ley CONTAINS $trash OR a.title CONTAINS $trash DETACH DELETE a RETURN count(a)", {"trash": b}).single()
            bajas += res[0]
            
        print(f"Purgados {bajas} nodos basura de Neo4j.")
        
        # Inyectar Leyes faltantes vitales
        s.run("""
        MERGE (a:Articulo:SS {id: 'Art. 3 Decreto 1646/1972'})
        SET a.title = 'Art. 3', a.texto = $txt, a.ley = 'Decreto 1646/1972', a.vigente = true
        """, {"txt": decreto_1646_art3})
        
        s.run("""
        MERGE (a:Articulo:SS {id: 'Art. 7.2 Decreto 1646/1972'})
        SET a.title = 'Art. 7.2', a.texto = $txt, a.ley = 'Decreto 1646/1972', a.vigente = true
        """, {"txt": decreto_1646_art7})
        
        s.run("""
        MERGE (a:Articulo:SS {id: 'Orden PJC/178/2025'})
        SET a.title = 'Tipos de Cotización', a.texto = $txt, a.ley = 'Orden PJC/178/2025', a.vigente = true
        """, {"txt": orden_pjc_2025})
        
        print("Inyectadas Leyes Vitales faltantes (1646/1972 y Orden PJC 2025).")
        
    driver.close()

if __name__ == '__main__':
    run_purge()
