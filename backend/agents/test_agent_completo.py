#!/usr/bin/env python3
"""
Test completo del Agente Mistral V2
Prueba: RAG, verificación URLs, BOE
"""

import os
import sys
import json
from pathlib import Path

# Cargar .env.backend
env_path = Path(__file__).parent.parent / ".env.backend"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip())

# Añadir path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.mistral_tools import get_mistral_tools

def test_herramientas_reales():
    """Test de herramientas reales sin llamar a Mistral API"""
    print("\n" + "=" * 70)
    print("🧪 TEST HERRAMIENTAS REALES DEL AGENTE")
    print("=" * 70)
    
    tools = get_mistral_tools()
    
    # Test 1: Buscar en RAG
    print("\n📚 TEST 1: Búsqueda RAG (Qdrant)")
    print("-" * 50)
    rag_result = tools.buscar_rag_qdrant(
        query="edad jubilación ordinaria requisitos",
        top_k=3
    )
    print(f"✅ Success: {rag_result.get('success')}")
    print(f"📊 Resultados: {rag_result.get('total_results', 0)}")
    if rag_result.get('results'):
        for i, r in enumerate(rag_result['results'][:2], 1):
            print(f"   {i}. Fuente: {r.get('fuente', 'N/A')[:50]}")
            print(f"      Texto: {r.get('text', '')[:150]}...")
    
    # Test 2: Buscar en BOE
    print("\n📜 TEST 2: Búsqueda BOE Oficial")
    print("-" * 50)
    boe_result = tools.buscar_boe_oficial(
        tipo_busqueda='articulo_especifico',
        articulo='205',
        ley='LGSS'
    )
    print(f"✅ Success: {boe_result.get('success')}")
    print(f"🔗 URL: {boe_result.get('url_boe', 'N/A')}")
    print(f"📋 Metadatos: {boe_result.get('metadatos', {})}")
    
    # Test 3: Verificar URL del BOE
    print("\n🔗 TEST 3: Verificación URL BOE")
    print("-" * 50)
    url_test = "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724"
    url_result = tools.verificar_url_boe(
        url=url_test,
        articulo_esperado="205",
        verificar_contenido=True
    )
    print(f"🌐 URL: {url_test}")
    print(f"✅ Válida: {url_result.get('valida')}")
    print(f"✅ Accesible: {url_result.get('accesible')}")
    print(f"✅ Contiene artículo 205: {url_result.get('contiene_articulo')}")
    if url_result.get('contenido_preview'):
        print(f"📄 Preview: {url_result.get('contenido_preview', '')[:200]}...")
    
    # Test 4: Verificar URL incorrecta
    print("\n🔗 TEST 4: Verificación URL Incorrecta")
    print("-" * 50)
    url_bad = "https://www.boe.es/buscar/act.php?id=BOE-A-FAKE-12345"
    url_bad_result = tools.verificar_url_boe(url=url_bad)
    print(f"🌐 URL: {url_bad}")
    print(f"✅ Válida: {url_bad_result.get('valida')}")
    print(f"❌ Accesible: {url_bad_result.get('accesible')}")
    
    # Test 5: Cálculo de prestación
    print("\n🧮 TEST 5: Cálculo Prestación SS")
    print("-" * 50)
    bases = [2500.0] * 300  # 25 años a 2500€/mes
    calc_result = tools.calcular_prestacion_ss(
        tipo_prestacion='base_reguladora_jubilacion',
        bases_cotizacion=bases,
        num_meses=300
    )
    print(f"📊 Tipo: {calc_result.get('tipo_prestacion')}")
    print(f"💰 Resultado: {calc_result.get('resultado')}€")
    print(f"📝 Fórmula: {calc_result.get('formula')}")
    print(f"📖 Normativa: {calc_result.get('normativa')}")
    
    # Test 6: Extraer artículos de texto
    print("\n📑 TEST 6: Extracción de Artículos")
    print("-" * 50)
    texto_legal = """
    Según el artículo 205.1.a de la LGSS, la edad ordinaria de jubilación es 67 años.
    El art. 208 LGSS regula la jubilación anticipada voluntaria.
    Ver también Art. 209 sobre base reguladora y Art. 210 sobre porcentajes.
    La Ley 39/2015 (LPAC) en su artículo 21 establece los plazos.
    """
    extract_result = tools.extraer_articulos_texto(texto_legal)
    print(f"📊 Total referencias: {extract_result.get('total')}")
    for ref in extract_result.get('referencias', []):
        print(f"   - {ref.get('referencia_completa')}")
    
    # Test 7: Clasificar Q&A
    print("\n🏷️ TEST 7: Clasificación Q&A")
    print("-" * 50)
    clasif_result = tools.clasificar_qa_tema(
        pregunta="¿Cuántos años de cotización se necesitan para acceder a la jubilación anticipada voluntaria?",
        respuesta="Se necesitan al menos 35 años de cotización efectiva",
        explicacion="Según el artículo 208 de la LGSS"
    )
    print(f"📚 Tema: {clasif_result.get('tema')}")
    print(f"📊 Dificultad: {clasif_result.get('dificultad')}")
    print(f"🎯 Tipo: {clasif_result.get('tipo')}")
    
    print("\n" + "=" * 70)
    print("✅ TESTS COMPLETADOS")
    print("=" * 70)
    
    return True


def test_mistral_api():
    """Test llamando a Mistral API (requiere API key)"""
    print("\n" + "=" * 70)
    print("🤖 TEST MISTRAL API")
    print("=" * 70)
    
    api_key = os.getenv("MISTRAL_API_KEY", "")
    agent_id = os.getenv("MISTRAL_AGENT_ID", "")
    
    print(f"🔑 API Key: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else 'N/A'}")
    print(f"🤖 Agent ID: {agent_id}")
    
    if not api_key:
        print("❌ No hay API key configurada")
        return False
    
    try:
        from mistralai import Mistral
        client = Mistral(api_key=api_key)
        
        # Test simple
        print("\n📝 Enviando consulta al agente...")
        response = client.chat.complete(
            model=agent_id,  # Usar agent_id como modelo
            messages=[
                {"role": "user", "content": "¿Cuál es la edad de jubilación ordinaria en España? Responde brevemente."}
            ]
        )
        
        if response.choices:
            content = response.choices[0].message.content
            print(f"\n✅ Respuesta del agente:")
            print("-" * 50)
            print(content)
            print("-" * 50)
            
            if hasattr(response, 'usage'):
                print(f"\n📊 Tokens usados: {response.usage.total_tokens}")
            
            return True
        else:
            print("❌ No se recibió respuesta")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    # Primero test de herramientas locales
    test_herramientas_reales()
    
    # Luego test de API (opcional)
    print("\n" + "=" * 70)
    respuesta = input("¿Probar Mistral API? (s/n): ").strip().lower()
    if respuesta == 's':
        test_mistral_api()
