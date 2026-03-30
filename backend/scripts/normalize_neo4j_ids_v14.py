import os
import re
from neo4j import GraphDatabase

NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
NEO4J_PASS = os.getenv('NEO4J_PASSWORD', 'opositaia2026')

def get_siglas(ley_fullname):
    """Mapeo de nombres largos a siglas de oposición."""
    ley_fullname = ley_fullname.upper()
    if 'SEGURIDAD SOCIAL' in ley_fullname: return 'TRLGSS'
    if 'ESTATUTO DE LOS TRABAJADORES' in ley_fullname: return 'ET'
    if 'PROCEDIMIENTO ADMINISTRATIVO' in ley_fullname: return 'LPAC'
    if 'RÉGIMEN JURÍDICO DEL SECTOR PÚBLICO' in ley_fullname: return 'LRJSP'
    if 'ESTATUTO BÁSICO DEL EMPLEADO PÚBLICO' in ley_fullname: return 'TREBEP'
    if 'CONSTITUCIÓN ESPAÑOLA' in ley_fullname: return 'CE'
    if 'JURISDICCIÓN SOCIAL' in ley_fullname: return 'LRJS'
    if 'CONTRATOS DEL SECTOR PÚBLICO' in ley_fullname: return 'LCSP'
    if 'PRÁCTICA DEL PODER JUDICIAL' in ley_fullname: return 'LOPJ'
    if 'CONTENCIOSO-ADMINISTRATIVA' in ley_fullname: return 'LJCA'
    return 'LEY'

def normalize_title(title):
    """
    Convierte 'Artículo 204. Concepto.' -> 'Art. 204'
    Convierte 'Disposición transitoria séptima.' -> 'DT 7ª'
    """
    title = title.strip()
    # Caso Artículos
    match_art = re.match(r'Artículo\s+(\d+)', title, re.I)
    if match_art:
        return f"Art. {match_art.group(1)}"
    
    # Caso Disposiciones Transitorias (ordinales comunes)
    dt_mapping = {
        'primera': '1ª', 'segunda': '2ª', 'tercera': '3ª', 'cuarta': '4ª', 'quinta': '5ª',
        'sexta': '6ª', 'séptima': '7ª', 'octava': '8ª', 'novena': '9ª', 'décima': '10ª'
    }
    match_dt = re.search(r'Disposición\s+transitoria\s+(\w+)', title, re.I)
    if match_dt:
        ord_word = match_dt.group(1).lower()
        ord_num = dt_mapping.get(ord_word, ord_word)
        return f"DT {ord_num}"
    
    return title

def run_normalization():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    
    print("Iniciando Normalización Quirúrgica de Neo4j V14...")
    
    with driver.session() as s:
        # 1. Obtener todos los artículos
        nodes = s.run("MATCH (a:Articulo) RETURN id(a) as node_id, a.id as old_id, a.title as title, a.ley as ley")
        
        count = 0
        for rec in nodes:
            node_id = rec["node_id"]
            old_id = rec["old_id"]
            title = rec["title"]
            ley = rec["ley"]
            
            if not title or not ley: continue
            
            prefix = normalize_title(title)
            siglas = get_siglas(ley)
            
            # Intentar ID amigable: "Art. 204 TRLGSS"
            new_id = f"{prefix} {siglas}".strip()
            
            if new_id != old_id:
                try:
                    # Intentar actualización simple
                    s.run("MATCH (a) WHERE id(a) = $node_id SET a.id = $new_id", {"node_id": node_id, "new_id": new_id})
                except Exception:
                    # Desambiguación definitiva: Usar el ID interno de Neo4j como sufijo
                    # Esto garantiza UNICIDAD absoluta
                    new_id_unique = f"{new_id} [{node_id}]"
                    s.run("MATCH (a) WHERE id(a) = $node_id SET a.id = $new_id_unique", {"node_id": node_id, "new_id_unique": new_id_unique})
                
                count += 1
                if count % 100 == 0:
                    print(f"Normalizados {count} artículos...")

        print(f"\n¡ÉXITO! Se han normalizado {count} identificadores.")
        print("Ejemplos:")
        print("Antes: BOE-A-2015-11724_p_209 -> Ahora: Art. 204 TRLGSS")
        
    driver.close()

if __name__ == '__main__':
    run_normalization()
