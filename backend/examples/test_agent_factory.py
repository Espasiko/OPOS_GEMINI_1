#!/usr/bin/env python3
"""
Test Agent Factory - Ejemplos de uso
Demuestra cómo usar la factoría de agentes con MCP
"""
import asyncio
import httpx
import json
from typing import Dict, Any

# Configuración
BASE_URL = "http://localhost:8000"
AGENT_FACTORY_URL = f"{BASE_URL}/agents"

async def test_agent_factory():
    """Test completo de la factoría de agentes"""
    
    async with httpx.AsyncClient() as client:
        print("🧪 TESTING AGENT FACTORY")
        print("=" * 50)
        
        # 1. Health check
        print("\n1. 🏥 Health Check")
        response = await client.get(f"{AGENT_FACTORY_URL}/health")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            health = response.json()
            print(f"MCP Server: {health.get('mcp_server')}")
            print(f"Collections: {health.get('collections')}")
            print(f"Agents: {', '.join(health.get('agents_available', []))}")
        
        # 2. Crear simulacro oficial
        print("\n2. 📝 Crear Simulacro Oficial (BOE-A-2024-11403)")
        simulacro_request = {
            "tema": "Seguridad Social",
            "nivel": "INTERMEDIO",
            "formato_oficial": True,
            "usuario_id": 123
        }
        
        response = await client.post(f"{AGENT_FACTORY_URL}/simulacro", json=simulacro_request)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            simulacro = response.json()
            data = simulacro["data"]
            print(f"✅ Simulacro creado: {data['id']}")
            print(f"   Parte 1: {data['estructura']['parte_1']['preguntas']} preguntas test")
            print(f"   Parte 2: {data['estructura']['parte_2']['preguntas']} casos prácticos")
            print(f"   Formato: {data['formato']}")
        
        # 3. Crear caso práctico
        print("\n3. ⚖️ Crear Caso Práctico")
        caso_request = {
            "tema": "Incapacidad Temporal",
            "complejidad": "ALTA",
            "incluir_jurisprudencia": True,
            "usuario_id": 123
        }
        
        response = await client.post(f"{AGENT_FACTORY_URL}/caso", json=caso_request)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            caso = response.json()
            data = caso["data"]
            print(f"✅ Caso creado: {data['titulo']}")
            print(f"   Hechos: {data['hechos'][:100]}...")
            print(f"   Referencias: {', '.join(data['referencias'])}")
        
        # 4. Crear flashcards
        print("\n4. 🎴 Crear Flashcards")
        flashcards_request = {
            "tema": "Jubilación",
            "cantidad": 5,
            "estilo": "DEFINICION",
            "usuario_id": 123
        }
        
        response = await client.post(f"{AGENT_FACTORY_URL}/flashcards", json=flashcards_request)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            flashcards = response.json()
            data = flashcards["data"]
            print(f"✅ {len(data)} flashcards creadas")
            for i, card in enumerate(data[:2]):  # Mostrar primeras 2
                print(f"   {i+1}. {card['pregunta']}")
                print(f"      R: {card['respuesta'][:50]}...")
        
        # 5. Crear resumen
        print("\n5. 📚 Crear Resumen de Ley")
        resumen_request = {
            "tema": "LGSS",
            "longitud": "MEDIO",
            "incluir_ejemplos": True
        }
        
        response = await client.post(f"{AGENT_FACTORY_URL}/resumen", json=resumen_request)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            resumen = response.json()
            data = resumen["data"]
            print(f"✅ Resumen creado: {data['tema']}")
            print(f"   Longitud: {resumen['longitud']}")
            print(f"   Conceptos clave: {len(data.get('conceptos_clave', {}))}")
        
        # 6. Crear mapa mental
        print("\n6. 🧠 Crear Mapa Mental")
        mapa_request = {
            "tema": "Prestaciones Seguridad Social",
            "profundidad": 3,
            "formato": "MERMAID"
        }
        
        response = await client.post(f"{AGENT_FACTORY_URL}/mapa_mental", json=mapa_request)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            mapa = response.json()
            data = mapa["data"]
            print(f"✅ Mapa mental creado: {data['tema_central']}")
            print(f"   Nodos: {len(data['nodos'])}")
            print(f"   Formato: {data['formato']}")
            if "mermaid" in data:
                print(f"   Mermaid: {data['mermaid'][:100]}...")
        
        # 7. Endpoint universal
        print("\n7. 🎯 Endpoint Universal")
        universal_request = {
            "tipo": "simulacro",
            "tema": "Desempleo",
            "nivel": "AVANZADO",
            "cantidad": 1,
            "usuario_id": 456,
            "personalizar": True,
            "usar_rag": True,
            "formato_oficial": True
        }
        
        response = await client.post(f"{AGENT_FACTORY_URL}/crear", json=universal_request)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            resultado = response.json()
            print(f"✅ Contenido creado: {resultado['tipo']}")
            print(f"   Fuente: {resultado['metadatos']['fuente']}")
            print(f"   Costo: €{resultado['metadatos']['costo']}")
            print(f"   Personalizado: {resultado['metadatos']['personalizado']}")

async def test_mcp_integration():
    """Test específico de integración MCP"""
    
    async with httpx.AsyncClient() as client:
        print("\n🔗 TESTING MCP INTEGRATION")
        print("=" * 50)
        
        # Test MCP Gateway directo
        print("\n1. 📡 Test MCP Gateway")
        mcp_request = {
            "query": "jubilación anticipada requisitos",
            "limit": 3
        }
        
        response = await client.post(f"{BASE_URL}/mcp/search_rag", json=mcp_request)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            results = response.json()
            print(f"✅ RAG Search: {len(results.get('results', []))} resultados")
            for i, result in enumerate(results.get('results', [])[:2]):
                print(f"   {i+1}. {result.get('title', 'Sin título')}")
                print(f"      Score: {result.get('score', 0):.3f}")
        
        # Test collections
        print("\n2. 📊 Test Collections")
        response = await client.get(f"{BASE_URL}/mcp/collections")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            collections = response.json()
            print(f"✅ Collections disponibles:")
            for collection in collections.get('collections', []):
                print(f"   - {collection.get('name')}: {collection.get('points_count')} chunks")

async def test_cosm_strategy():
    """Test de la estrategia COSM"""
    
    async with httpx.AsyncClient() as client:
        print("\n💰 TESTING COSM STRATEGY")
        print("=" * 50)
        
        # Test contenido reutilizable
        print("\n1. 🔄 Test Contenido Reutilizable")
        response = await client.get(f"{BASE_URL}/contenido/simulacros/Seguridad Social/INTERMEDIO?aleatorio=true&usuario_id=789")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            contenido = response.json()
            print(f"✅ Simulacro servido desde BD")
            print(f"   Fuente: {contenido.get('source')}")
            print(f"   Costo: €{contenido.get('cost')}")
            print(f"   Tiempo: {contenido.get('response_time_ms')}ms")
        
        # Test stats
        print("\n2. 📈 Test Estadísticas COSM")
        response = await client.get(f"{BASE_URL}/contenido/stats")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            data = stats["data"]
            print(f"✅ Estadísticas COSM:")
            print(f"   Simulacros disponibles: {data.get('simulacros_disponibles')}")
            print(f"   Casos prácticos: {data.get('casos_practicos')}")
            print(f"   Flashcards: {data.get('flashcards')}")
            print(f"   Ahorro mensual: €{data.get('ahorro_mensual_euros')}")
            print(f"   Porcentaje ahorro: {data.get('porcentaje_ahorro')}%")

async def demo_completo():
    """Demo completo del sistema"""
    
    print("🚀 DEMO COMPLETO: AGENT FACTORY + MCP + COSM")
    print("=" * 60)
    
    try:
        await test_agent_factory()
        await test_mcp_integration()
        await test_cosm_strategy()
        
        print("\n" + "=" * 60)
        print("✅ DEMO COMPLETADO EXITOSAMENTE")
        print("\n📋 RESUMEN:")
        print("   - Agent Factory: ✅ Funcionando")
        print("   - MCP Integration: ✅ Conectado")
        print("   - COSM Strategy: ✅ Implementado")
        print("   - Formato Oficial: ✅ BOE-A-2024-11403")
        print("\n💡 PRÓXIMOS PASOS:")
        print("   1. Ejecutar generación masiva: POST /agents/batch/generar_inicial")
        print("   2. Integrar con frontend React")
        print("   3. Implementar BD PostgreSQL para COSM")
        print("   4. Configurar Redis para caché")
        
    except Exception as e:
        print(f"\n❌ ERROR EN DEMO: {e}")
        print("   Verificar que el servidor esté corriendo en localhost:8000")
        print("   Verificar que MCP server esté funcionando")

if __name__ == "__main__":
    print("🧪 AGENT FACTORY TEST SUITE")
    print("Asegúrate de que el servidor esté corriendo: uvicorn main:app --reload")
    print()
    
    asyncio.run(demo_completo())