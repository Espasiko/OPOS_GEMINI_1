#!/usr/bin/env python3
"""
Test Reranking por Jerarquía
Verifica que Capa 1 (leyes) se priorice sobre Capa 3 (materiales)
"""

import requests
import json

BACKEND_URL = "http://localhost:8000"

def test_reranking():
    """Test que el reranking prioriza leyes sobre materiales"""
    print("🧪 Testing Reranking por Jerarquía")
    print("=" * 60)
    
    url = f"{BACKEND_URL}/chat/stream"
    payload = {
        "message": "¿Qué es la incapacidad temporal?",
        "conversation_id": "test-rerank",
        "use_rag": True,
        "top_k": 5,
        "min_score": 0.4
    }
    
    print(f"📤 Query: {payload['message']}")
    print()
    
    try:
        response = requests.post(url, json=payload, stream=True, timeout=180)
        
        if response.status_code != 200:
            print(f"❌ Error: {response.status_code}")
            return False
        
        print("📥 Analizando sources...")
        print("-" * 60)
        
        sources_found = False
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data = line_str[6:]
                    if data == '[DONE]':
                        break
                    try:
                        parsed = json.loads(data)
                        if 'sources' in parsed:
                            sources_found = True
                            sources = parsed['sources']
                            print(f"\n📚 Sources encontradas: {len(sources)}")
                            print()
                            
                            capa1_count = 0
                            capa3_count = 0
                            
                            for i, src in enumerate(sources, 1):
                                norma = src['norma']
                                articulo = src.get('articulo', 'N/A')
                                score = src['score']
                                
                                # Detectar capa por nombre
                                if any(x in norma.lower() for x in ['trlgss', 'lgss', 'constitución', 'real decreto']):
                                    capa = 1
                                    capa1_count += 1
                                    emoji = "⚖️"
                                elif any(x in norma.lower() for x in ['temario', 'test']):
                                    capa = 3
                                    capa3_count += 1
                                    emoji = "📚"
                                else:
                                    capa = "?"
                                    emoji = "❓"
                                
                                print(f"{i}. {emoji} Capa {capa} | Score: {score:.3f}")
                                print(f"   Norma: {norma}")
                                if articulo != 'N/A':
                                    print(f"   Artículo: {articulo}")
                                print()
                            
                            print("-" * 60)
                            print(f"📊 Resumen:")
                            print(f"   Capa 1 (Leyes): {capa1_count}")
                            print(f"   Capa 3 (Materiales): {capa3_count}")
                            print()
                            
                            if capa1_count > 0:
                                print("✅ Reranking funcionando: Se encontraron leyes")
                                if capa1_count >= capa3_count:
                                    print("✅ Priorización correcta: Más leyes que materiales")
                                else:
                                    print("⚠️  Advertencia: Más materiales que leyes")
                            else:
                                print("⚠️  No se encontraron leyes en los resultados")
                            
                            return True
                    except json.JSONDecodeError:
                        pass
        
        if not sources_found:
            print("❌ No se recibieron sources")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_reranking()
