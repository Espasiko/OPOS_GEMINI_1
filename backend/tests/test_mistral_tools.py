#!/usr/bin/env python3
"""
Tests para las herramientas reales del Agente Mistral
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.mistral_tools import MistralTools, SemanticCache, get_mistral_tools

def test_buscar_rag_qdrant():
    """Test de búsqueda RAG en Qdrant"""
    print("\n🔍 Test: buscar_rag_qdrant")
    print("-" * 40)
    
    tools = get_mistral_tools()
    
    # Test 1: Búsqueda básica
    result = tools.buscar_rag_qdrant(
        query="edad jubilación 2024",
        top_k=3
    )
    
    print(f"✅ Success: {result.get('success')}")
    print(f"📊 Resultados: {result.get('total_results', 0)}")
    
    if result.get('results'):
        for i, r in enumerate(result['results'][:2], 1):
            print(f"   {i}. {r.get('fuente', 'N/A')[:40]}... (rel: {r.get('relevancia', 0):.2f})")
    
    return result.get('success', False)

def test_buscar_boe_oficial():
    """Test de búsqueda en BOE"""
    print("\n📜 Test: buscar_boe_oficial")
    print("-" * 40)
    
    tools = get_mistral_tools()
    
    # Test 1: Por identificador
    result = tools.buscar_boe_oficial(
        tipo_busqueda='por_identificador',
        identificador_boe='BOE-A-2015-11724'
    )
    print(f"✅ Por ID: {result.get('success')} - URL: {result.get('url_boe', 'N/A')[:50]}...")
    
    # Test 2: Por artículo
    result = tools.buscar_boe_oficial(
        tipo_busqueda='articulo_especifico',
        articulo='205',
        ley='LGSS'
    )
    print(f"✅ Por artículo: {result.get('success')} - URL: {result.get('url_boe', 'N/A')[:50]}...")
    
    return result.get('success', False)

def test_verificar_url_boe():
    """Test de verificación de URL BOE"""
    print("\n🔗 Test: verificar_url_boe")
    print("-" * 40)
    
    tools = get_mistral_tools()
    
    # Test con URL válida
    result = tools.verificar_url_boe(
        url="https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724",
        articulo_esperado="205"
    )
    
    print(f"✅ URL válida: {result.get('valida')}")
    print(f"🌐 Accesible: {result.get('accesible')}")
    
    return result.get('valida', False)

def test_calcular_prestacion_ss():
    """Test de cálculos de prestaciones"""
    print("\n🧮 Test: calcular_prestacion_ss")
    print("-" * 40)
    
    tools = get_mistral_tools()
    
    # Test 1: Base reguladora
    bases = [2000.0] * 300  # 300 meses a 2000€
    result = tools.calcular_prestacion_ss(
        tipo_prestacion='base_reguladora_jubilacion',
        bases_cotizacion=bases,
        num_meses=300
    )
    
    print(f"📊 Base Reguladora: {result.get('resultado')}€")
    print(f"📝 Fórmula: {result.get('formula', 'N/A')[:60]}...")
    print(f"📖 Normativa: {result.get('normativa')}")
    
    # Test 2: IMV
    result = tools.calcular_prestacion_ss(
        tipo_prestacion='imv',
        parametros_adicionales={'miembros_unidad': 3, 'menores': 1}
    )
    
    print(f"💰 IMV: {result.get('resultado')}€")
    
    return result.get('resultado') is not None

def test_clasificar_qa_tema():
    """Test de clasificación de Q&A"""
    print("\n🏷️ Test: clasificar_qa_tema")
    print("-" * 40)
    
    tools = get_mistral_tools()
    
    result = tools.clasificar_qa_tema(
        pregunta="¿Cuál es la edad mínima para acceder a la jubilación anticipada voluntaria?",
        respuesta="63 años con 35 años cotizados",
        explicacion="Según el artículo 208 LGSS"
    )
    
    print(f"📚 Tema: {result.get('tema')}")
    print(f"📊 Dificultad: {result.get('dificultad')}")
    print(f"🎯 Tipo: {result.get('tipo')}")
    
    return result.get('tema') == 'jubilacion'

def test_extraer_articulos_texto():
    """Test de extracción de artículos"""
    print("\n📑 Test: extraer_articulos_texto")
    print("-" * 40)
    
    tools = get_mistral_tools()
    
    texto = """
    Según el artículo 205.1.a de la LGSS, la edad de jubilación es 67 años.
    El art. 208 establece la jubilación anticipada.
    Ver también Art. 209 sobre base reguladora.
    """
    
    result = tools.extraer_articulos_texto(texto)
    
    print(f"📊 Total referencias: {result.get('total')}")
    for ref in result.get('referencias', []):
        print(f"   - {ref.get('referencia_completa')}")
    
    return result.get('total', 0) >= 3

def test_semantic_cache():
    """Test de caché semántica"""
    print("\n💾 Test: SemanticCache")
    print("-" * 40)
    
    tools = get_mistral_tools()
    cache = SemanticCache(tools.qdrant)
    
    # Test set
    cache.set("¿Cuál es la edad de jubilación?", {"respuesta": "67 años"})
    print("✅ Cache SET completado")
    
    # Test get (miss esperado sin embeddings reales)
    result = cache.get("¿Cuál es la edad de jubilación?")
    print(f"📊 Cache GET: {'HIT' if result else 'MISS'}")
    
    # Stats
    stats = cache.get_stats()
    print(f"📈 Stats: {stats}")
    
    return True

def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "=" * 60)
    print("🧪 TESTS DE HERRAMIENTAS MISTRAL")
    print("=" * 60)
    
    tests = [
        ("buscar_rag_qdrant", test_buscar_rag_qdrant),
        ("buscar_boe_oficial", test_buscar_boe_oficial),
        ("verificar_url_boe", test_verificar_url_boe),
        ("calcular_prestacion_ss", test_calcular_prestacion_ss),
        ("clasificar_qa_tema", test_clasificar_qa_tema),
        ("extraer_articulos_texto", test_extraer_articulos_texto),
        ("semantic_cache", test_semantic_cache),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"❌ Error en {name}: {e}")
            results.append((name, False))
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS")
    print("=" * 60)
    
    passed = sum(1 for _, p in results if p)
    total = len(results)
    
    for name, p in results:
        status = "✅" if p else "❌"
        print(f"  {status} {name}")
    
    print(f"\n🎯 Resultado: {passed}/{total} tests pasados ({passed/total*100:.0f}%)")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
