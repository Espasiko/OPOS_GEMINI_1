
import asyncio
import os
import sys
from datetime import date

# Añadir el path del backend para poder importar
sys.path.append(os.path.join(os.getcwd(), "backend"))

from agents.rag_agent_v2 import get_rag_agent_v2
from calculators.dispatcher import CasosPracticosDispatcher

async def test_rag_v2_simplificado():
    print("\n--- TEST RAG V2 SIMPLIFICADO ---")
    rag = get_rag_agent_v2()
    print(f"Colección activa: {rag.collection_name}")
    
    query = "requisitos subsidio cuidado menor cancer"
    print(f"Buscando: {query}")
    results = await rag.search_documents(query, top_k=2)
    
    for r in results:
        print(f"[{r['score']:.4f}] {r['metadata']['article_id']} - {r['metadata']['law_name']}")
        # print(f"Contenido: {r['content'][:100]}...")

async def test_nuevas_calculadoras():
    print("\n--- TEST NUEVAS CALCULADORAS ---")
    dispatcher = CasosPracticosDispatcher()
    
    # Test CUME
    print("Prueba CUME:")
    res_cume = dispatcher.ejecutar("Un trabajador reduce su jornada un 50% para cuidar a su hijo con cáncer. Su base reguladora de IT es de 2000 euros.")
    print(f"  Resultado: {res_cume}")
    
    # Test Beneficios Hijos
    print("\nPrueba Beneficios Hijos (Art 235-237):")
    res_hijos = dispatcher.ejecutar("Calcula la asimilación por parto de 2 hijos y 1 año de excedencia.")
    print(f"  Resultado: {res_hijos}")
    
    # Test Supervivencia IPC 2026
    print("\nPrueba Supervivencia IPC 2026:")
    res_muerte = dispatcher.ejecutar("Accidente de trabajo el 15/05/2026. Base reguladora 3000€. Viuda y 2 hijos.")
    print(f"  Resultado: {res_muerte}")

if __name__ == "__main__":
    asyncio.run(test_rag_v2_simplificado())
    asyncio.run(test_nuevas_calculadoras())
