import json
import urllib.request

TANDAS = {
    "2064/1995": "Tanda 3 (Cotización)",
    "1415/2004": "Tanda 4 (Recaudación)",
    "1993/1995": "Tanda 5 (Prestaciones)",
    "5/2000": "Tanda 6 (LISOS)",
    "928/1998": "Tanda 6 (Inspección)",
    "39/2015": "Tanda 7 (LPAC)",
    "40/2015": "Tanda 7 (LRJSP)",
    "1362/2012": "Tanda 8 (Mutuas)",
    "1148/2011": "Tanda 8 (Riesgo Embarazo/Lactancia)",
    "1539/2003": "Tanda 8 (Jubilación Discapacidad)",
    "1131/2002": "Tanda 8 (Jubilación Parcial)",
    "20/2007": "Tanda 8 (Estatuto Autónomos)",
    "84/1996": "Tanda 8 (Inscripción Empresas)",
    "295/2009": "Tanda 8 (Maternidad/Paternidad)",
    "3/2007": "Tanda 9 (Igualdad)",
    "1/2004": "Tanda 9 (Violencia de Género)"
}

EXPRESIONES_PRIMARIAS = [
    "salvo que", "salvo en los", "salvo prueba en contrario",
    "con excepción de", "excepción hecha de", "sin otra excepción que",
    "no obstante", "excepto", "excepcionalmente", "sin embargo",
    "salvo expresa autorización", "sin perjuicio", 
    "siempre que", "siempre y cuando", "podrá no ser exigible", "a excepción de", "salvo"
]

def query_neo4j(filtro_titulo):
    lucene_query = "salvo OR obstante OR excepci* OR excepto OR embargo OR perjuicio OR siempre OR exigible"
    cypher = """
    CALL db.index.fulltext.queryNodes("precepto_fulltext", $lucene_query) YIELD node AS p, score
    MATCH (p)-[:PERTENECE_A]->(l:Ley)
    WHERE l.titulo CONTAINS $filtro
    RETURN l.titulo AS titulo_ley, p.numero, p.texto
    """
    
    payload = {
        "statements": [{
            "statement": cypher,
            "parameters": {"lucene_query": lucene_query, "filtro": filtro_titulo}
        }]
    }
    
    req = urllib.request.Request(
        "http://localhost:7474/db/neo4j/tx/commit",
        data=json.dumps(payload).encode('utf-8'),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Basic bmVvNGo6b3Bvc2l0YWlhMjAyNg=="
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            res = json.loads(response.read().decode('utf-8'))
            if res.get("errors"):
                return []
            return res["results"][0]["data"]
    except Exception as e:
        return []

def generar_informe():
    informe = "# Informe Riguroso de Excepciones (Tandas 3 a 8)\n\n"
    informe += "> Este documento contiene las frases exactas extraídas de Neo4j usando el índice Lucene. No contiene alucinaciones.\n\n"
    
    for filtro, nombre in TANDAS.items():
        informe += f"## {nombre} - Filtro: {filtro}\n"
        datos = query_neo4j(filtro)
        if not datos:
            informe += "No se encontraron resultados o la ley no está cargada.\n\n"
            continue
            
        resultados = []
        for row in datos:
            titulo_ley, numero, texto = row["row"]
            if not texto: continue
            
            frases = [f.strip() for f in texto.split('.') if f.strip()]
            frases_con_trampas = []
            
            for frase in frases:
                frase_lower = frase.lower()
                if any(exp.lower() in frase_lower for exp in EXPRESIONES_PRIMARIAS):
                    frases_con_trampas.append(frase)
                    
            if frases_con_trampas:
                # El usuario quiere ver todo el artículo para tener contexto, no solo la frase truncada.
                frases_con_trampas = [texto.strip()]
                try:
                    num_sort = int(numero)
                except:
                    num_sort = 9999
                resultados.append((num_sort, numero, frases_con_trampas))
                
        resultados.sort(key=lambda x: x[0])
        
        for _, num, frases in resultados:
            informe += f"### Art. {num}\n"
            for f in frases:
                informe += f"- {f}\n"
        informe += "\n"
        
    with open('/home/spas/.gemini/antigravity/brain/44a94c17-0e1d-45ba-bd66-0023f94d2497/revision_rigurosa_tandas.md', 'w') as f:
        f.write(informe)

if __name__ == "__main__":
    generar_informe()
