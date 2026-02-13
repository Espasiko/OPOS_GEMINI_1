import os
import json
from datetime import datetime
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import requests

# Cargar variables de entorno
load_dotenv("/home/spas/OPOS_GEMINI_1/backend/.env.backend")

# Configuración QDRANT LOCAL
QDRANT_URL = "http://localhost:6333"

print(f"🔍 Conectando a Qdrant LOCAL: {QDRANT_URL}")
print(f"📦 Cargando modelo pablosi LOCAL...")

# Cliente Qdrant LOCAL
client = QdrantClient(url=QDRANT_URL)

# Modelo de embeddings LOCAL
model = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")


def generar_embedding(text: str):
    """Genera embedding con modelo pablosi LOCAL"""
    try:
        embedding = model.encode(text, convert_to_tensor=False).tolist()
        return embedding
    except Exception as e:
        print(f"❌ Error generando embedding: {e}")
        return None


def encontrar_mejor_coleccion():
    """Encuentra la colección con más datos"""
    try:
        collections = client.get_collections()
        
        print(f"\n📚 Colecciones disponibles:")
        mejor_col = None
        max_puntos = 0
        
        for col in collections.collections:
            info = client.get_collection(col.name)
            puntos = info.points_count
            print(f"   - {col.name}: {puntos:,} puntos")
            
            if puntos > max_puntos:
                max_puntos = puntos
                mejor_col = col.name
        
        print(f"\n✅ Usando colección: '{mejor_col}' ({max_puntos:,} puntos)")
        return mejor_col
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def buscar_qdrant(collection_name: str, query: str, limit: int = 5):
    """Búsqueda REAL en Qdrant local"""
    print(f"\n🔎 Buscando: '{query}'")
    
    try:
        # Generar embedding
        embedding = generar_embedding(query)
        
        if embedding is None:
            print("❌ No se pudo generar embedding")
            return []
        
        # Búsqueda en Qdrant local
        results = client.search(
            collection_name=collection_name,
            query_vector=embedding,
            limit=limit,
            with_payload=True
        )
        
        print(f"✅ Encontrados {len(results)} resultados")
        
        formatted_results = []
        for r in results:
            formatted_results.append({
                "score": round(r.score, 4),
                "ley": r.payload.get("law_name", r.payload.get("metadata", {}).get("law_name", "Desconocida")),
                "articulo": r.payload.get("article_id", r.payload.get("metadata", {}).get("article_id", "")),
                "texto": (r.payload.get("text", r.payload.get("content", ""))[:200] + "..."),
                "boe_url": r.payload.get("boe_url", r.payload.get("metadata", {}).get("boe_url", "")),
            })
            
            # Mostrar primer resultado
            if formatted_results:
                print(f"   Top result: {formatted_results[0]['ley']} - Art. {formatted_results[0]['articulo']} (score: {formatted_results[0]['score']})")
        
        return formatted_results
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def verificar_boe(ley_id: str, fecha_limite: str = "2026-12-31"):
    """Verifica ley en BOE con fecha límite"""
    print(f"\n🔍 Verificando BOE: {ley_id} (hasta {fecha_limite})")
    
    try:
        url = f"https://www.boe.es/buscar/act.php?id={ley_id}"
        response = requests.get(url, timeout=10)
        
        # Determinar estado
        if "VIGENTE" in response.text or "vigente" in response.text:
            estado = "VIGENTE"
        elif "DEROGADO" in response.text or "derogado" in response.text:
            estado = "DEROGADO"
        else:
            estado = "DESCONOCIDO (revisar manualmente)"
        
        print(f"✅ Estado: {estado}")
        
        return {
            "ley_id": ley_id,
            "estado": estado,
            "url": url,
            "fecha_consulta": datetime.now().isoformat(),
            "fecha_limite": fecha_limite
        }
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}

def main():
    """Ejecuta caso práctico REAL con herramientas LOCALES"""
    
    print("\n" + "="*80)
    print("🎯 CASO PRÁCTICO REAL: María, 61 años, jubilación anticipada")
    print("🔧 USANDO QDRANT LOCAL CON DATOS REALES")
    print("="*80)
    
    # Encontrar mejor colección
    collection_name = encontrar_mejor_coleccion()
    
    if not collection_name:
        print("\n❌ No se encontró ninguna colección con datos")
        return
    
    # Datos del caso
    caso = {
        "nombre": "María",
        "edad": 61,
        "años_cotizados": 38,
        "discapacidad": 35,  # %
        "mutualista_años": 10,
        "base_reguladora": 2800,
    }
    
    print(f"\n📋 Datos del caso:")
    print(json.dumps(caso, indent=2, ensure_ascii=False))
    
    # 10 búsquedas REALES en Qdrant LOCAL
    busquedas = [
        "jubilación anticipada edad mínima 63 años",
        "coeficientes reductores jubilación anticipada",
        "discapacidad 33% jubilación beneficios",
        "mutualista cómputo años cotizados",
        "compatibilidad pensión trabajo autónomo",
        "complemento maternidad pensión hijos",
        "jubilación flexible requisitos",
        "jubilación parcial compatibilidad",
        "procedimiento solicitud jubilación INSS",
        "plazos tramitación pensión contributiva",
    ]
    
    resultados_busquedas = {}
    
    for i, query in enumerate(busquedas, 1):
        print(f"\n{'='*80}")
        print(f"BÚSQUEDA {i}/10")
        print(f"{'='*80}")
        
        results = buscar_qdrant(collection_name, query, limit=3)
        resultados_busquedas[f"busqueda_{i}"] = {
            "query": query,
            "results": results
        }
    
    # Verificación BOE REAL
    print(f"\n{'='*80}")
    print("VERIFICACIÓN BOE")
    print(f"{'='*80}")
    
    leyes_a_verificar = [
        "BOE-A-2015-11724",  # LGSS
        "BOE-A-2021-1529",   # RDL 3/2021 (complemento maternidad)
    ]
    
    verificaciones_boe = {}
    
    for ley_id in leyes_a_verificar:
        verificacion = verificar_boe(ley_id, fecha_limite="2026-12-31")
        verificaciones_boe[ley_id] = verificacion
    
    # Guardar resultados
    output = {
        "caso": caso,
        "fecha_ejecucion": datetime.now().isoformat(),
        "qdrant_local": {
            "url": QDRANT_URL,
            "collection": collection_name,
        },
        "busquedas_qdrant": resultados_busquedas,
        "verificaciones_boe": verificaciones_boe,
        "herramientas_usadas": {
            "qdrant": "LOCAL (localhost:6333)",
            "collection": collection_name,
            "embedding_model": "pablosi/bge-m3-spa-law-qa-trained-2",
            "boe_api": "https://www.boe.es/buscar/act.php"
        }
    }
    
    output_file = "/home/spas/OPOS_GEMINI_1/caso_practico_LOCAL_REAL_resultados.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*80}")
    print(f"✅ RESULTADOS GUARDADOS EN: {output_file}")
    print(f"{'='*80}")
    
    # Resumen
    total_resultados = sum(len(b["results"]) for b in resultados_busquedas.values())
    print(f"\n📊 RESUMEN:")
    print(f"  - Qdrant local: {QDRANT_URL}")
    print(f"  - Colección usada: {collection_name}")
    print(f"  - Búsquedas realizadas: {len(busquedas)}")
    print(f"  - Resultados totales: {total_resultados}")
    print(f"  - Verificaciones BOE: {len(verificaciones_boe)}")
    print(f"  - Herramientas: Qdrant LOCAL + Embeddings pablosi + BOE API")

if __name__ == "__main__":
    main()
