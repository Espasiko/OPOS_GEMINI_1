import os
from neo4j import GraphDatabase
import re

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "opositaia2026")

KEYWORDS = [
    "salvo", "excepto", "sin perjuicio", "no obstante", 
    "con excepción", "a excepción", "únicamente", "exclusivamente",
    "excepción hecha", "sin embargo", "siempre que", "siempre y cuando",
    "podrá no ser exigible"
]

TANDAS = {
    "Tanda 3 (Cotización)": ["2064/1995"],
    "Tanda 4 (Recaudación)": ["1415/2004"],
    "Tanda 5 (Prestaciones/Mutuas)": ["1993/1995"],
    "Tanda 6 (LISOS e Inspección)": ["5/2000", "928/1998"],
    "Tanda 7 (Leyes Administrativas)": ["39/2015", "40/2015"],
    "Tanda 8 (Sustantivas varias)": ["20/2007", "84/1996", "295/2009"],
    "Tanda 9 (Complementarias)": ["3/2007", "1/2004", "Constitución", "PGE"]
}

def get_full_text(tx, start_node_id):
    # Retrieve the text of the node and any subsequent nodes linked via SIGUIENTE
    query = """
    MATCH path = (p:Precepto)-[:SIGUIENTE*0..]->(next_p:Precepto)
    WHERE id(p) = $node_id
    RETURN [n IN nodes(path) | n.texto] AS textos
    ORDER BY length(path) DESC
    LIMIT 1
    """
    result = tx.run(query, node_id=start_node_id)
    record = result.single()
    if record and record["textos"]:
        return " ".join(record["textos"])
    
    # If no SIGUIENTE path exists, just return the node's text
    query_single = "MATCH (p:Precepto) WHERE id(p) = $node_id RETURN p.texto AS texto"
    result_single = tx.run(query_single, node_id=start_node_id)
    record_single = result_single.single()
    return record_single["texto"] if record_single else ""

def run():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    report_lines = []
    report_lines.append("# Informe Riguroso de Excepciones (Tandas 3 a 9)")
    report_lines.append("> Extracción completa verificando artículos concatenados (relación SIGUIENTE).")
    report_lines.append("> Palabras clave buscadas: " + ", ".join(KEYWORDS) + "\n")
    
    with driver.session() as session:
        for tanda, filters in TANDAS.items():
            report_lines.append(f"## {tanda}")
            for f in filters:
                report_lines.append(f"### Filtro Ley: {f}")
                
                # We find all root precepts (those that are not the destination of a SIGUIENTE relation)
                # matching the law filter
                query_roots = """
                MATCH (p:Precepto)-[:PERTENECE_A]->(l:Ley)
                WHERE l.boe_id CONTAINS $filtro OR l.siglas CONTAINS $filtro
                AND NOT ()-[:SIGUIENTE]->(p)
                RETURN id(p) AS node_id, p.numero AS ref, p.title AS title
                ORDER BY p.numero
                """
                
                roots = session.execute_read(lambda tx: list(tx.run(query_roots, filtro=f)))
                
                found_any = False
                for record in roots:
                    node_id = record["node_id"]
                    ref = record["title"] or record["ref"] or "Art. Indeterminado"
                    
                    full_text = session.execute_read(get_full_text, node_id)
                    
                    # Search for keywords
                    pattern = re.compile(r'\b(?:' + '|'.join(KEYWORDS) + r')\b', re.IGNORECASE)
                    
                    if pattern.search(full_text):
                        # Extract sentences with keywords
                        sentences = re.split(r'(?<=[.!?])\s+', full_text)
                        matching_sentences = [s.strip() for s in sentences if pattern.search(s)]
                        
                        if matching_sentences:
                            found_any = True
                            report_lines.append(f"#### {ref}")
                            for s in matching_sentences:
                                # Highlight the keyword
                                s_high = pattern.sub(lambda m: f"**{m.group(0)}**", s)
                                report_lines.append(f"- {s_high}")
                
                if not found_any:
                    report_lines.append("*No se encontraron excepciones con las palabras clave.*")
            report_lines.append("\n")
            
    with open("/home/spas/OPOS_GEMINI_1/INFORME_RIGUROSO_TANDAS_3_A_9.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

if __name__ == "__main__":
    run()
