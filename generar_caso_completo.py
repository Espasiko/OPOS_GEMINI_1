#!/usr/bin/env python3
"""
Script completo para generar caso usando TODOS los MCPs
Incluye: Calculadora, RAG, Memoria MCP, Legal Graph, Salamandra
"""

import sys
import json
import asyncio
from pathlib import Path

# Añadir backend al path
sys.path.insert(0, str(Path(__file__).parent))

from backend.calculators.calculos_ss import calcular_subsidio_it
from backend.agents.rag_helper import get_rag_helper
from backend.agents.salamandra_memory import get_memory_integration
from backend.agents.generate_salamandra import SalamandraGenerator


async def generar_caso_completo():
    """
    Genera un caso práctico usando TODO el sistema
    """
    print("=" * 70)
    print("GENERACIÓN DE CASO COMPLETO CON TODOS LOS MCPs")
    print("=" * 70)
    print()
    
    # PASO 1: CALCULADORA SS
    print("📊 PASO 1: Calculadora de Seguridad Social")
    print("-" * 70)
    
    calculo = calcular_subsidio_it(
        base=1850.0,
        contingencia="EC",
        dia=10
    )
    
    print(f"✅ Base cotización: {calculo['base_cotizacion']}€")
    print(f"✅ Base diaria: {calculo['base_diaria']}€")
    print(f"✅ Porcentaje: {calculo['porcentaje']}%")
    print(f"✅ Subsidio diario: {calculo['subsidio_diario']}€")
    print(f"✅ Artículo: {calculo['articulo_aplicable']}")
    print()
    
    # PASO 2: RAG (Qdrant)
    print("🔍 PASO 2: Búsqueda RAG en Qdrant")
    print("-" * 70)
    
    rag = get_rag_helper()
    articulos = rag.search_articles("Incapacidad Temporal subsidio", limit=3)
    
    print(f"✅ Artículos encontrados: {len(articulos)}")
    for i, art in enumerate(articulos, 1):
        print(f"  {i}. {art.get('article_id', 'N/A')} (score: {art.get('score', 0):.2f})")
    
    articulos_texto = rag.format_articles_for_prompt(articulos)
    print()
    
    # PASO 3: MEMORIA MCP
    print("🧠 PASO 3: Memoria MCP (casos similares)")
    print("-" * 70)
    
    memory = get_memory_integration()
    
    # Buscar casos similares
    query_memoria = f"Base {calculo['base_cotizacion']}€ contingencia {calculo['contingencia']}"
    casos_similares = memory.find_similar_cases(query_memoria, limit=2)
    
    print(f"✅ Casos similares encontrados: {len(casos_similares)}")
    for i, caso in enumerate(casos_similares, 1):
        print(f"  {i}. Score: {caso['score']:.2f}")
        print(f"     Text: {caso['text'][:80]}...")
    print()
    
    # PASO 4: LEGAL GRAPH
    print("🔗 PASO 4: Grafo Legal (artículos relacionados)")
    print("-" * 70)
    
    related = memory.get_related_articles("Art. 173")
    
    print(f"✅ Artículos relacionados con Art. 173: {len(related)}")
    for i, art in enumerate(related[:5], 1):
        print(f"  {i}. {art['id']} ({art['relation_type']}): {art['name']}")
    print()
    
    # PASO 5: SALAMANDRA
    print("🦎 PASO 5: Generación con Salamandra")
    print("-" * 70)
    
    generator = SalamandraGenerator()
    
    caso = await generator.generate_case(
        tema="Incapacidad Temporal por Enfermedad Común",
        articulos_texto=articulos_texto,
        calculo_json=calculo,
        dificultad="media"
    )
    
    print("✅ Caso generado:")
    print(f"  Enunciado: {caso.get('enunciado', '')[:150]}...")
    print(f"  Pregunta: {caso.get('pregunta', '')[:100]}...")
    print(f"  Respuesta correcta: {caso.get('respuesta_correcta', 'N/A')}")
    print(f"  Artículos aplicables: {caso.get('articulos_aplicables', [])}")
    print()
    
    # PASO 6: GUARDAR EN MEMORIA (si es bueno)
    print("💾 PASO 6: Guardar en memoria MCP")
    print("-" * 70)
    
    # Simular coherencia alta
    coherencia_score = 0.97
    
    if coherencia_score >= 0.95:
        memory_id = memory.save_successful_case(caso, coherencia_score)
        print(f"✅ Caso guardado en memoria: {memory_id}")
    else:
        print("⚠️  Caso no guardado (coherencia < 0.95)")
    print()
    
    # RESULTADO FINAL
    print("=" * 70)
    print("CASO COMPLETO GENERADO")
    print("=" * 70)
    print()
    print(json.dumps(caso, indent=2, ensure_ascii=False))
    print()
    
    return caso


if __name__ == "__main__":
    # Ejecutar
    caso_final = asyncio.run(generar_caso_completo())
    
    # Guardar en archivo
    output_file = Path(__file__).parent / "caso_generado_con_mcps.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(caso_final, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Caso guardado en: {output_file}")
