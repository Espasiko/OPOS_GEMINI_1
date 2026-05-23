import os
import re
from neo4j import GraphDatabase

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "opositaia2026")

def explore_calculations():
    print("Conectando a Neo4j para explorar cálculos...")
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    # Expresión regular para buscar términos relacionados con cálculos matemáticos
    # cálculo, calcula, calcular, porcentaje, cuantía, base reguladora, recargo, importe, deducción, multiplicación, cociente
    regex_pattern = '(?i).*(cálculo|calcular|calcula|porcentaje|cuantía|base reguladora|recargo|interés|importe|multiplic|dividid|cociente|fracción|%|descuento|bonificación).*'

    try:
        with driver.session() as session:
            # 1. Agrupar por ley para ver dónde están los cálculos
            print("--- Leyes con más términos de cálculo ---")
            res_leyes = session.run("""
            MATCH (p:Precepto)-[:PERTENECE_A]->(l:Ley)
            WHERE p.texto =~ $regex
            RETURN l.siglas as ley, count(p) as num, l.titulo as titulo
            ORDER BY num DESC LIMIT 15
            """, regex=regex_pattern)
            
            for record in res_leyes:
                print(f"{record['ley']}: {record['num']} preceptos ({record['titulo'][:60]}...)")
            
            print("\n--- Categorías de Cálculos (ToT / CoT Exploratory) ---")
            
            # 2. Extraer ejemplos específicos de Base Reguladora (Prestaciones)
            print("\n>> 1. BASES REGULADORAS Y PENSIONES (TRLGSS, RD 1430/2009, etc.)")
            res_br = session.run("""
            MATCH (p:Precepto)-[:PERTENECE_A]->(l:Ley)
            WHERE p.texto =~ '(?i).*(base reguladora|cuantía de la pensión).*'
            RETURN l.siglas as ley, p.numero as art, substring(p.texto, 0, 150) as snippet
            LIMIT 5
            """)
            for record in res_br:
                print(f"[{record['ley']} - {record['art']}]: {record['snippet'].replace(chr(10), ' ')}...")
                
            # 3. Extraer ejemplos de Recargos e Intereses (Recaudación)
            print("\n>> 2. RECARGOS, INTERESES Y COTIZACIÓN (RD 1415/2004, TRLGSS)")
            res_recargos = session.run("""
            MATCH (p:Precepto)-[:PERTENECE_A]->(l:Ley)
            WHERE p.texto =~ '(?i).*(recargo|interés de demora|tipo de cotización).*'
            RETURN l.siglas as ley, p.numero as art, substring(p.texto, 0, 150) as snippet
            LIMIT 5
            """)
            for record in res_recargos:
                print(f"[{record['ley']} - {record['art']}]: {record['snippet'].replace(chr(10), ' ')}...")
                
            # 4. Extraer ejemplos de Infracciones y Sanciones (LISOS)
            print("\n>> 3. INFRACCIONES Y SANCIONES - MULTAS (LISOS)")
            res_multas = session.run("""
            MATCH (p:Precepto)-[:PERTENECE_A]->(l:Ley)
            WHERE p.texto =~ '(?i).*(importe|multa|sanción|euros|%).*' AND l.siglas = 'LISOS'
            RETURN l.siglas as ley, p.numero as art, substring(p.texto, 0, 150) as snippet
            LIMIT 5
            """)
            for record in res_multas:
                print(f"[{record['ley']} - {record['art']}]: {record['snippet'].replace(chr(10), ' ')}...")
                
            # 5. Fórmulas específicas (buscando división, suma, multiplicación)
            print("\n>> 4. FÓRMULAS MATEMÁTICAS EXPLÍCITAS")
            res_formulas = session.run("""
            MATCH (p:Precepto)-[:PERTENECE_A]->(l:Ley)
            WHERE p.texto =~ '(?i).*(dividido|multiplicado|cociente|suma de).*'
            RETURN l.siglas as ley, p.numero as art, substring(p.texto, 0, 150) as snippet
            LIMIT 5
            """)
            for record in res_formulas:
                print(f"[{record['ley']} - {record['art']}]: {record['snippet'].replace(chr(10), ' ')}...")
                
    finally:
        driver.close()

if __name__ == "__main__":
    explore_calculations()
