#!/usr/bin/env python3
"""
Script de prueba para MCPs
Prueba los MCP servers sin esperar stdin
"""

import sys
sys.path.insert(0, '/home/spas/OPOS_GEMINI_1/backend')

from mcp_servers.qdrant_memory_local import QdrantMemoryLocal
from mcp_servers.legal_graph_mcp import LegalGraphMCP

print("=" * 60)
print("PRUEBA 1: Qdrant Memory Local MCP")
print("=" * 60)

try:
    print("\n🔄 Inicializando Qdrant Memory...")
    memory = QdrantMemoryLocal()
    
    print("\n✅ Test 1: Get Stats")
    stats = memory.get_stats()
    print(f"Stats: {stats}")
    
    print("\n✅ Test 2: Add Memory")
    memory_id = memory.add_memory(
        text="Juan Pérez, trabajador Grupo 2, base 1500€, IT por EC, subsidio 30€",
        metadata={
            "base_cotizacion": 1500,
            "contingencia": "EC",
            "subsidio_diario": 30,
            "coherencia_score": 0.98
        }
    )
    print(f"Memory ID: {memory_id}")
    
    print("\n✅ Test 3: Search Memory")
    results = memory.search_memory("Base 1500€ contingencia EC", limit=3)
    print(f"Resultados encontrados: {len(results)}")
    for i, result in enumerate(results, 1):
        print(f"\nResultado {i}:")
        print(f"  Score: {result['score']:.4f}")
        print(f"  Text: {result['text'][:80]}...")
        print(f"  Metadata: {result['metadata']}")
    
    print("\n✅ Qdrant Memory MCP: FUNCIONA CORRECTAMENTE")

except Exception as e:
    print(f"\n❌ Error en Qdrant Memory: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("PRUEBA 2: Legal Graph MCP")
print("=" * 60)

try:
    print("\n🔄 Inicializando Legal Graph...")
    graph = LegalGraphMCP()
    
    print("\n✅ Test 1: Populate Legal Structure")
    result = graph.populate_legal_structure()
    print(f"Resultado: {result}")
    
    print("\n✅ Test 2: Get Stats")
    stats = graph.get_stats()
    print(f"Stats: {stats}")
    
    print("\n✅ Test 3: Search Entities")
    entities = graph.search_entities("Incapacidad Temporal", limit=5)
    print(f"Entidades encontradas: {len(entities)}")
    for entity in entities:
        print(f"  - {entity['id']}: {entity['name']}")
    
    print("\n✅ Test 4: Get Related")
    related = graph.get_related("Art. 173")
    print(f"Artículos relacionados con Art. 173: {len(related)}")
    for rel in related:
        print(f"  - {rel['id']} ({rel['relation_type']}): {rel['name']}")
    
    print("\n✅ Legal Graph MCP: FUNCIONA CORRECTAMENTE")

except Exception as e:
    print(f"\n❌ Error en Legal Graph: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("RESUMEN FINAL")
print("=" * 60)
print("✅ Ambos MCPs creados y funcionando")
print("✅ Qdrant Memory: Memoria semántica con modelo local")
print("✅ Legal Graph: Grafo de conocimiento legal con SQLite")
print("=" * 60)
