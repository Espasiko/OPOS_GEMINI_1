#!/usr/bin/env python3
"""
Test rápido del pipeline con Mistral local
"""

import ollama
import json

def test_ollama_connection():
    """Verifica conexión con Ollama"""
    print("🔍 Verificando Ollama...")
    try:
        client = ollama.Client()
        models = client.list()
        print("✅ Ollama conectado")
        print(f"   Modelos disponibles: {[m['name'] for m in models['models']]}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 SOLUCIÓN:")
        print("   1. Instala Ollama: curl -fsSL https://ollama.ai/install.sh | sh")
        print("   2. Descarga Mistral: ollama pull mistral")
        print("   3. Verifica: ollama list")
        return False

def test_mistral_generation():
    """Prueba generación con Mistral"""
    print("\n🧪 Probando generación de Q&A...")
    
    try:
        client = ollama.Client()
        
        prompt = """Crea 1 pregunta tipo test sobre jubilación en España.

Formato JSON:
{
  "pregunta": "¿Cuál es la edad ordinaria de jubilación en 2025?",
  "opciones": ["a) 65 años", "b) 67 años", "c) 70 años", "d) 62 años"],
  "respuesta_correcta": "b",
  "explicacion": "La edad ordinaria es 67 años según la LGSS"
}"""
        
        response = client.chat(model="mistral", messages=[
            {'role': 'user', 'content': prompt}
        ])
        
        content = response['message']['content']
        print("✅ Respuesta generada:")
        print(content[:300] + "...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_similarity_analysis():
    """Prueba análisis de similitud"""
    print("\n🔍 Probando análisis de similitud...")
    
    try:
        client = ollama.Client()
        
        q1 = "¿Cuál es la edad de jubilación de Juan nacido en 1960?"
        q2 = "¿A qué edad puede jubilarse María nacida en 1962?"
        
        prompt = f"""Analiza si estas preguntas son similares:

PREGUNTA 1: {q1}
PREGUNTA 2: {q2}

Responde: SIMILITUD|explicación
Donde SIMILITUD es: EXACTA, ALTA, MEDIA, BAJA o NINGUNA"""
        
        response = client.chat(model="mistral", messages=[
            {'role': 'user', 'content': prompt}
        ])
        
        content = response['message']['content']
        print("✅ Análisis:")
        print(f"   {content[:200]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 TEST DEL PIPELINE MISTRAL LOCAL")
    print("=" * 60)
    
    # Test 1: Conexión
    if not test_ollama_connection():
        return
    
    # Test 2: Generación
    if not test_mistral_generation():
        return
    
    # Test 3: Análisis
    if not test_similarity_analysis():
        return
    
    print("\n" + "=" * 60)
    print("✅ TODOS LOS TESTS PASARON")
    print("=" * 60)
    print("\n💡 SIGUIENTE PASO:")
    print("   python analyze_academy_duplicates.py")
    print("   python generate_qa_from_schemas.py")

if __name__ == "__main__":
    main()
