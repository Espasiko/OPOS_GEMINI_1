#!/usr/bin/env python3
"""
Análisis de dificultad de preguntas en exámenes oficiales y de academia
Determina el porcentaje de preguntas difíciles vs fáciles/medias
"""

import os
import json
import requests
from qdrant_client import QdrantClient

MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
QDRANT_URL = "http://localhost:6333"

def call_mistral(prompt: str) -> str:
    try:
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {MISTRAL_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistral-large-latest",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
                "max_tokens": 2000
            },
            timeout=120
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    print("\n📊 ANÁLISIS DE DIFICULTAD DE EXÁMENES OFICIALES")
    print("=" * 60)
    
    # Conectar a Qdrant
    qdrant = QdrantClient(url=QDRANT_URL)
    
    # Extraer preguntas de exámenes
    points, _ = qdrant.scroll(
        collection_name="materiales_academia",
        limit=500,
        with_payload=True,
        with_vectors=False
    )
    
    # Filtrar solo preguntas de exámenes
    preguntas = []
    for p in points:
        if p.payload.get('subcategory') == 'preguntas' or 'examen' in p.payload.get('filename', '').lower():
            text = p.payload.get('text', '')
            if len(text) > 50 and '?' in text:
                preguntas.append({
                    'text': text[:800],
                    'filename': p.payload.get('filename', ''),
                    'is_official': p.payload.get('is_official', False)
                })
    
    print(f"\n📥 Encontradas {len(preguntas)} preguntas de exámenes")
    
    # Seleccionar muestra representativa (30 preguntas)
    muestra = preguntas[:30]
    
    # Analizar dificultad con Mistral
    prompt = f"""Eres experto en oposiciones de Seguridad Social España.

Analiza estas {len(muestra)} preguntas de exámenes REALES y clasifica cada una por dificultad.

CRITERIOS DE DIFICULTAD:
- FÁCIL: Pregunta directa sobre un concepto básico, memorización simple
- MEDIA: Requiere relacionar 2-3 conceptos, aplicación básica de normativa
- DIFÍCIL: Caso práctico complejo, excepciones, cálculos, trampas sutiles
- MUY_DIFÍCIL: Combina múltiples conceptos, jurisprudencia, casos límite

PREGUNTAS A ANALIZAR:
{json.dumps([{'num': i+1, 'pregunta': p['text'][:400], 'oficial': p['is_official']} for i, p in enumerate(muestra)], indent=2, ensure_ascii=False)}

RESPONDE CON JSON:
{{
    "analisis": [
        {{"num": 1, "dificultad": "FACIL/MEDIA/DIFICIL/MUY_DIFICIL", "razon": "breve explicación"}},
        ...
    ],
    "estadisticas": {{
        "total": {len(muestra)},
        "facil": X,
        "media": X,
        "dificil": X,
        "muy_dificil": X,
        "porcentaje_dificiles": X.X
    }},
    "conclusion": "texto sobre distribución típica de dificultad en exámenes"
}}"""

    print("\n🔄 Analizando dificultad con Mistral...")
    response = call_mistral(prompt)
    
    if response:
        try:
            # Buscar JSON en respuesta
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0:
                result = json.loads(response[start:end])
                
                print("\n" + "=" * 60)
                print("📊 RESULTADOS DEL ANÁLISIS")
                print("=" * 60)
                
                stats = result.get('estadisticas', {})
                print(f"\n📈 DISTRIBUCIÓN DE DIFICULTAD:")
                print(f"   🟢 Fácil: {stats.get('facil', 0)} ({stats.get('facil', 0)/len(muestra)*100:.1f}%)")
                print(f"   🟡 Media: {stats.get('media', 0)} ({stats.get('media', 0)/len(muestra)*100:.1f}%)")
                print(f"   🟠 Difícil: {stats.get('dificil', 0)} ({stats.get('dificil', 0)/len(muestra)*100:.1f}%)")
                print(f"   🔴 Muy difícil: {stats.get('muy_dificil', 0)} ({stats.get('muy_dificil', 0)/len(muestra)*100:.1f}%)")
                
                pct_dif = stats.get('porcentaje_dificiles', 0)
                print(f"\n🎯 PORCENTAJE PREGUNTAS DIFÍCILES: {pct_dif}%")
                
                print(f"\n📝 CONCLUSIÓN:")
                print(f"   {result.get('conclusion', 'N/A')}")
                
                # Mostrar algunas clasificaciones
                print(f"\n📋 EJEMPLOS DE CLASIFICACIÓN:")
                for item in result.get('analisis', [])[:5]:
                    print(f"   #{item['num']}: {item['dificultad']} - {item['razon'][:60]}...")
                
                # Guardar resultado
                with open('dataset_output/analisis_dificultad_examenes.json', 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"\n📁 Guardado: dataset_output/analisis_dificultad_examenes.json")
                
        except Exception as e:
            print(f"Error parseando: {e}")
            print(f"Respuesta: {response[:500]}")
    else:
        print("❌ No se pudo analizar")

if __name__ == "__main__":
    main()
