import json
import urllib.request

EXPRESIONES_PRIMARIAS = [
    "salvo que",
    "salvo en los",
    "salvo prueba en contrario",
    "con excepción de",
    "excepción hecha de",
    "sin otra excepción que",
    "no obstante",
    "excepto",
    "excepcionalmente",
    "sin embargo",
    "salvo expresa autorización",
    "sin perjuicio"
]

def query_neo4j(filtro_titulo):
    lucene_query = "salvo OR obstante OR excepci* OR excepto OR embargo OR perjuicio"
    
    # Buscamos con CONTAINS para el título por si hay variaciones ("Real Decreto Legislativo 2/2015", etc.)
    cypher = """
    CALL db.index.fulltext.queryNodes("precepto_fulltext", $lucene_query) YIELD node AS p, score
    MATCH (p)-[:PERTENECE_A]->(l:Ley)
    WHERE l.titulo CONTAINS $filtro
    RETURN l.titulo AS titulo_ley, p.numero, p.texto, score
    """
    
    payload = {
        "statements": [{
            "statement": cypher,
            "parameters": {
                "lucene_query": lucene_query,
                "filtro": filtro_titulo
            }
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
                print(f"Error Neo4j: {res['errors']}")
                return []
            return res["results"][0]["data"]
    except Exception as e:
        print(f"Excepción HTTP: {e}")
        return []

def analizar_ley(filtro_titulo, nombre_corto):
    print(f"\n{'='*50}")
    print(f"ANALIZANDO TANDA: {nombre_corto} ({filtro_titulo})")
    print(f"{'='*50}")
    
    datos = query_neo4j(filtro_titulo)
    if not datos:
        print("No se encontraron preceptos para esta ley.")
        return

    resultados = []
    
    for row in datos:
        titulo_ley, numero, texto, score = row["row"]
        if not texto: continue
        
        frases = [f.strip() for f in texto.split('.') if f.strip()]
        frases_con_trampas = []
        
        for frase in frases:
            frase_lower = frase.lower()
            match = any(exp.lower() in frase_lower for exp in EXPRESIONES_PRIMARIAS)
            if match:
                frases_con_trampas.append(frase)
                
        if frases_con_trampas:
            try:
                num_sort = int(numero)
            except:
                num_sort = 9999
            resultados.append((num_sort, numero, titulo_ley, frases_con_trampas))
            
    resultados.sort(key=lambda x: x[0])
    
    print(f"-> Total artículos verificados en esta Tanda: {len(resultados)}\n")
    
    for _, num, tit, frases in resultados:
        print(f"--- Art. {num} ---")
        for f in frases:
            print(f"   * {f}")
        print()

if __name__ == "__main__":
    analizar_ley("1415/2004", "Tanda 4: Reglamento General de Recaudación")
    analizar_ley("5/2000", "Tanda 6: LISOS")
    analizar_ley("928/1998", "Tanda 6: Reglamento Inspección")
