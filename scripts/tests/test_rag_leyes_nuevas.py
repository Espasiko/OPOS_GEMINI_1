#!/usr/bin/env python3
"""
TEST RAG CON LEYES RECIÉN INDEXADAS
Prueba que el RAG puede responder preguntas sobre las nuevas leyes
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Añadir backend al path
backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

# Cargar variables de entorno
env_path = backend_path / '.env.backend'
load_dotenv(env_path)

from agents.rag_agent_v2 import RAGAgentV2

print("="*80)
print("🧪 TEST RAG - LEYES RECIÉN INDEXADAS")
print("="*80)

# Crear agente RAG
print("\n🔌 Inicializando RAG Agent...")
try:
    rag = RAGAgentV2()
    print("✅ RAG Agent inicializado")
except Exception as e:
    print(f"❌ Error inicializando RAG: {e}")
    sys.exit(1)

# Preguntas de prueba para diferentes leyes
PREGUNTAS_TEST = [
    {
        "pregunta": "¿Qué dice el artículo 41 de la Constitución sobre la Seguridad Social?",
        "ley_esperada": "Constitucion",
        "categoria": "🔴 CRÍTICA"
    },
    {
        "pregunta": "¿Cuáles son los requisitos de afiliación según el RD 84/1996?",
        "ley_esperada": "RD_84_1996",
        "categoria": "🔴 CRÍTICA"
    },
    {
        "pregunta": "¿Cómo se calculan las bases de cotización según el RD 2064/1995?",
        "ley_esperada": "RD_2064_1995",
        "categoria": "🔴 CRÍTICA"
    },
    {
        "pregunta": "¿Qué establece el RD 1415/2004 sobre la recaudación en vía ejecutiva?",
        "ley_esperada": "RD_1415_2004",
        "categoria": "🔴 CRÍTICA"
    },
    {
        "pregunta": "¿Qué es el Ingreso Mínimo Vital según la Ley 19/2021?",
        "ley_esperada": "Ley_19_2021_IMV",
        "categoria": "🟡 MEDIA"
    },
    {
        "pregunta": "¿Qué dice la Ley 39/2015 sobre el procedimiento administrativo común?",
        "ley_esperada": "Ley_39_2015",
        "categoria": "🟠 ALTA"
    }
]

print(f"\n{'='*80}")
print(f"🧪 EJECUTANDO {len(PREGUNTAS_TEST)} TESTS")
print(f"{'='*80}")

tests_exitosos = 0
tests_fallidos = 0

for i, test in enumerate(PREGUNTAS_TEST, 1):
    print(f"\n{'-'*80}")
    print(f"TEST {i}/{len(PREGUNTAS_TEST)} - {test['categoria']}")
    print(f"{'-'*80}")
    print(f"❓ Pregunta: {test['pregunta']}")
    print(f"📚 Ley esperada: {test['ley_esperada']}")
    
    try:
        # Buscar documentos relevantes
        print(f"\n🔍 Buscando en Qdrant...")
        results = rag.search_documents(test['pregunta'], top_k=3)
        
        if not results:
            print(f"❌ No se encontraron resultados")
            tests_fallidos += 1
            continue
        
        print(f"✅ Encontrados {len(results)} documentos")
        
        # Verificar si algún resultado es de la ley esperada
        leyes_encontradas = set()
        for j, doc in enumerate(results, 1):
            norma = doc.get('norma', 'N/A')
            articulo = doc.get('articulo', 'N/A')
            score = doc.get('score', 0)
            text_preview = doc.get('text', '')[:100]
            
            leyes_encontradas.add(norma)
            
            print(f"\n   📄 Resultado {j}:")
            print(f"      Norma: {norma}")
            print(f"      Artículo: {articulo}")
            print(f"      Score: {score:.4f}")
            print(f"      Preview: {text_preview}...")
        
        # Verificar si la ley esperada está en los resultados
        if test['ley_esperada'] in leyes_encontradas:
            print(f"\n✅ TEST EXITOSO: Ley esperada '{test['ley_esperada']}' encontrada")
            tests_exitosos += 1
        else:
            print(f"\n⚠️  TEST PARCIAL: Ley esperada '{test['ley_esperada']}' NO encontrada")
            print(f"   Leyes encontradas: {', '.join(leyes_encontradas)}")
            tests_fallidos += 1
            
    except Exception as e:
        print(f"\n❌ ERROR en test: {e}")
        tests_fallidos += 1
        import traceback
        traceback.print_exc()

# Resumen final
print(f"\n{'='*80}")
print(f"📊 RESUMEN DE TESTS")
print(f"{'='*80}")
print(f"   Total tests: {len(PREGUNTAS_TEST)}")
print(f"   ✅ Exitosos: {tests_exitosos}")
print(f"   ❌ Fallidos: {tests_fallidos}")
print(f"   📈 Tasa de éxito: {tests_exitosos/len(PREGUNTAS_TEST)*100:.1f}%")

if tests_exitosos == len(PREGUNTAS_TEST):
    print(f"\n🎉 ¡TODOS LOS TESTS PASARON!")
elif tests_exitosos > len(PREGUNTAS_TEST) / 2:
    print(f"\n✅ La mayoría de tests pasaron")
else:
    print(f"\n⚠️  Muchos tests fallaron, revisar configuración")

print(f"\n{'='*80}")
print(f"✅ TEST COMPLETADO")
print(f"{'='*80}")
