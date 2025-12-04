#!/usr/bin/env python3
"""
TEST FINAL - BÚSQUEDA DE LEY IMV
Verifica que la Ley IMV re-indexada se encuentra correctamente
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
print("🧪 TEST FINAL - BÚSQUEDA LEY IMV")
print("="*80)

# Conectar a Qdrant
print("\n🔌 Conectando a Qdrant Cloud...")
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
print("✅ Conectado")

# Cargar modelo
print("\n🧠 Cargando modelo de embeddings...")
model = SentenceTransformer('PlanTL-GOB-ES/RoBERTalex')
print("✅ Modelo cargado")

# Preguntas específicas sobre IMV
PREGUNTAS_IMV = [
    "¿Qué es el Ingreso Mínimo Vital según la Ley 19/2021?",
    "¿Cuáles son los requisitos para acceder al Ingreso Mínimo Vital?",
    "¿Qué prestación económica establece la Ley 19/2021?",
    "¿Cómo se solicita el IMV según la normativa vigente?",
    "¿Qué dice la ley sobre el Ingreso Mínimo Vital?"
]

print(f"\n{'='*80}")
print(f"🧪 EJECUTANDO {len(PREGUNTAS_IMV)} TESTS")
print(f"{'='*80}")

tests_exitosos = 0

for i, pregunta in enumerate(PREGUNTAS_IMV, 1):
    print(f"\n{'-'*80}")
    print(f"TEST {i}/{len(PREGUNTAS_IMV)}")
    print(f"{'-'*80}")
    print(f"❓ Pregunta: {pregunta}")
    
    try:
        # Generar embedding
        query_vector = model.encode(pregunta).tolist()
        
        # Buscar en Qdrant
        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=5
        )
        
        print(f"\n✅ Encontrados {len(results)} resultados")
        
        # Verificar si IMV está en los resultados
        imv_encontrado = False
        posicion_imv = None
        
        for j, hit in enumerate(results, 1):
            norma = hit.payload.get('norma', 'N/A')
            articulo = hit.payload.get('articulo', 'N/A')
            score = hit.score
            text = hit.payload.get('text', '')[:80]
            
            emoji = "🎯" if norma == "Ley_19_2021_IMV" else "  "
            print(f"\n   {emoji} Resultado {j}:")
            print(f"      Norma: {norma}")
            print(f"      Artículo: {articulo}")
            print(f"      Score: {score:.4f}")
            print(f"      Preview: {text}...")
            
            if norma == "Ley_19_2021_IMV":
                imv_encontrado = True
                posicion_imv = j
        
        # Evaluar resultado
        if imv_encontrado:
            if posicion_imv == 1:
                print(f"\n✅ TEST EXITOSO: IMV en posición #1 (óptimo)")
            elif posicion_imv <= 3:
                print(f"\n✅ TEST EXITOSO: IMV en posición #{posicion_imv} (bueno)")
            else:
                print(f"\n⚠️  TEST PARCIAL: IMV en posición #{posicion_imv} (mejorable)")
            tests_exitosos += 1
        else:
            print(f"\n❌ TEST FALLIDO: IMV NO encontrada en top-5")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

# Resumen
print(f"\n{'='*80}")
print(f"📊 RESUMEN FINAL")
print(f"{'='*80}")
print(f"   Total tests: {len(PREGUNTAS_IMV)}")
print(f"   ✅ Exitosos: {tests_exitosos}")
print(f"   ❌ Fallidos: {len(PREGUNTAS_IMV) - tests_exitosos}")
print(f"   📈 Tasa de éxito: {tests_exitosos/len(PREGUNTAS_IMV)*100:.1f}%")

if tests_exitosos == len(PREGUNTAS_IMV):
    print(f"\n🎉 ¡PERFECTO! Todos los tests pasaron")
    print(f"   La Ley IMV ahora se encuentra correctamente en las búsquedas")
elif tests_exitosos >= len(PREGUNTAS_IMV) * 0.6:
    print(f"\n✅ BUENO: La mayoría de tests pasaron")
    print(f"   La re-indexación mejoró significativamente la búsqueda de IMV")
else:
    print(f"\n⚠️  MEJORABLE: Pocos tests pasaron")
    print(f"   Considerar ajustar el scoring o añadir más contenido")

# Estadísticas de IMV
print(f"\n{'='*80}")
print(f"📊 ESTADÍSTICAS DE LEY IMV")
print(f"{'='*80}")

try:
    from qdrant_client.models import Filter, FieldCondition, MatchValue
    
    # Contar chunks de IMV
    scroll_result = client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="norma",
                    match=MatchValue(value="Ley_19_2021_IMV")
                )
            ]
        ),
        limit=100
    )
    
    chunks_imv = len(scroll_result[0])
    print(f"   Total chunks IMV: {chunks_imv}")
    
    if chunks_imv > 0:
        # Mostrar algunos chunks
        print(f"\n   Muestra de chunks:")
        for i, point in enumerate(scroll_result[0][:3], 1):
            articulo = point.payload.get('articulo', 'N/A')
            text = point.payload.get('text', '')[:60]
            print(f"   {i}. Artículo: {articulo}")
            print(f"      Preview: {text}...")
            
except Exception as e:
    print(f"   ⚠️  Error obteniendo estadísticas: {e}")

print(f"\n{'='*80}")
