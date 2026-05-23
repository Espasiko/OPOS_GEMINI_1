import json
import urllib.request
import re

# Lista exacta de expresiones del Análisis Lingüístico (implementation_plan.md)
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
    "sin perjuicio" # secundaria pero requerida
]

def query_neo4j(ley_titulo):
    # Usamos sintaxis Lucene para el índice fulltext
    # Buscamos las raíces de nuestras expresiones para que el índice trabaje rápido
    lucene_query = "salvo OR obstante OR excepci* OR excepto OR embargo OR perjuicio"
    
    cypher = """
    CALL db.index.fulltext.queryNodes("precepto_fulltext", $lucene_query) YIELD node AS p, score
    MATCH (p)-[:PERTENECE_A]->(l:Ley)
    WHERE l.titulo STARTS WITH $ley
    RETURN p.numero, p.texto, score
    """
    
    payload = {
        "statements": [{
            "statement": cypher,
            "parameters": {
                "lucene_query": lucene_query,
                "ley": ley_titulo
            }
        }]
    }
    
    req = urllib.request.Request(
        "http://localhost:7474/db/neo4j/tx/commit",
        data=json.dumps(payload).encode('utf-8'),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Basic bmVvNGo6b3Bvc2l0YWlhMjAyNg==" # neo4j:opositaia2026 en Base64
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

def analizar_ley(ley_titulo):
    print(f"\n=============================================")
    print(f"ANALIZANDO LEY: {ley_titulo}")
    print(f"=============================================")
    
    datos = query_neo4j(ley_titulo)
    if not datos:
        print("No se obtuvieron resultados o hubo un error.")
        return

    resultados = []
    
    for row in datos:
        numero, texto, score = row["row"]
        if not texto: continue
        
        # Dividir por puntos para sacar las frases exactas
        frases = [f.strip() for f in texto.split('.') if f.strip()]
        frases_con_trampas = []
        
        for frase in frases:
            frase_lower = frase.lower()
            # Validar contra el listado exhaustivo
            match = any(exp.lower() in frase_lower for exp in EXPRESIONES_PRIMARIAS)
            if match:
                frases_con_trampas.append(frase)
                
        if frases_con_trampas:
            try:
                num_sort = int(numero)
            except:
                num_sort = 9999
            resultados.append((num_sort, numero, frases_con_trampas))
            
    # Ordenar por número de artículo
    resultados.sort(key=lambda x: x[0])
    
    print(f"-> Total artículos con trampas verificadas en {ley_titulo}: {len(resultados)}\n")
    
    for _, num, frases in resultados:
        print(f"--- Art. {num} ---")
        for f in frases:
            # Resaltar la trampa
            f_print = f
            print(f"   * {f_print}")
        print()

if __name__ == "__main__":
    analizar_ley("Ley 39/2015")
    analizar_ley("Ley 40/2015")
