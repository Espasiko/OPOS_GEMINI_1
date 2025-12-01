#!/usr/bin/env python3
"""
TEST SIMPLE RAG - Búsqueda directa en Qdrant
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Cargar variables de entorno
env_path = Path(__file__).parent / 'backend' / '.env.backend'
load_dotenv(env_path)

QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'opositaia_leyes_seguridad_social')

print("="*80)
print("🧪 TEST SIMPLE RAG - BÚSQUEDA DIRECTA")
print("="*80)

# Conectar a Qdrant
print("\n🔌 Conectando a Qdrant Cloud...")
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
print("✅ Conectado")

# Cargar modelo de embeddings
print("\n🧠 Cargando modelo de embeddings...")
model = SentenceTransformer('PlanTL-GOB-ES/RoBERTalex')
print("✅ Modelo cargado")

# Preguntas de prueba
PREGUNTAS = [
    ("¿Qué dice el artículo 41 de la Constitución?", "Constitucion"),
    ("¿Cuáles son los requisitos de afiliación?", "RD_84_1996"),
    ("¿Cómo se calculan las bases de cotización?", "RD_2064_1995"),
    ("¿Qué establece sobre la recaudación?", "RD_1415_2004"),
    ("¿Qué es el Ingreso Mínimo Vital?", "Ley_19_2021_IMV"),
]

print(f"\n{'='*80}")
print(f"🧪 EJECUTANDO {len(PREGUNTAS)} TESTS")
print(f"{'='*80}")

tests_exitosos = 0

for i, (pregunta, ley_esperada) in enumerate(PREGUNTAS, 1):
    print(f"\n{'-'*80}")
    print(f"TEST {i}/{len(PREGUNTAS)}")
    print(f"{'-'*80}")
    print(f"❓ Pregunta: {pregunta}")
    print(f"📚 Ley esperada: {ley_esperada}")
    
    try:
        # Generar embedding de la pregunta
        query_vector = model.encode(pregunta).tolist()
        
        # Buscar en Qdrant
        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=3
        )
        
        print(f"\n✅ Encontrados {len(results)} resultados")
        
        # Mostrar resultados
        leyes_encontradas = set()
        for j, hit in enumerate(results, 1):
            norma = hit.payload.get('norma', 'N/A')
            articulo = hit.payload.get('articulo', 'N/A')
            score = hit.score
            text = hit.payload.get('text', '')[:100]
            
            leyes_encontradas.add(norma)
            
            print(f"\n   📄 Resultado {j}:")
            print(f"      Norma: {norma}")
            print(f"      Artículo: {articulo}")
            print(f"      Score: {score:.4f}")
            print(f"      Preview: {text}...")
        
        # Verificar si encontró la ley esperada
        if ley_esperada in leyes_encontradas:
            print(f"\n✅ TEST EXITOSO: '{ley_esperada}' encontrada")
            tests_exitosos += 1
        else:
            print(f"\n⚠️  TEST FALLIDO: '{ley_esperada}' NO encontrada")
            print(f"   Leyes encontradas: {', '.join(leyes_encontradas)}")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

# Resumen
print(f"\n{'='*80}")
print(f"📊 RESUMEN")
print(f"{'='*80}")
print(f"   Total: {len(PREGUNTAS)}")
print(f"   ✅ Exitosos: {tests_exitosos}")
print(f"   ❌ Fallidos: {len(PREGUNTAS) - tests_exitosos}")
print(f"   📈 Tasa de éxito: {tests_exitosos/len(PREGUNTAS)*100:.1f}%")

if tests_exitosos == len(PREGUNTAS):
    print(f"\n🎉 ¡TODOS LOS TESTS PASARON!")
elif tests_exitosos >= len(PREGUNTAS) / 2:
    print(f"\n✅ La mayoría de tests pasaron")
else:
    print(f"\n⚠️  Revisar configuración del RAG")

print(f"\n{'='*80}")
