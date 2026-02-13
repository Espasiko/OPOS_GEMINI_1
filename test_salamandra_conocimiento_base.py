#!/usr/bin/env python3
"""
Test de conocimiento base de Salamandra R1 sobre Seguridad Social
Sin RAG - Solo conocimiento del modelo
"""

import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "salamandra-r1:latest"

def preguntar_salamandra(pregunta: str, max_tokens: int = 500):
    """Hace una pregunta a Salamandra R1"""
    
    prompt = f"""Eres un experto en Seguridad Social española. Responde de forma concisa y precisa.

Pregunta: {pregunta}

Respuesta:"""
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,  # Baja para respuestas más precisas
            "num_predict": max_tokens
        }
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "Sin respuesta").strip()
    except Exception as e:
        return f"ERROR: {str(e)}"

def main():
    print("=" * 80)
    print("🧪 TEST CONOCIMIENTO BASE: SALAMANDRA R1 (SIN RAG)")
    print("=" * 80)
    print(f"Modelo: {MODEL}")
    print(f"Endpoint: {OLLAMA_URL}")
    print("=" * 80)
    
    # Preguntas de diferentes niveles
    preguntas = [
        {
            "nivel": "BÁSICO",
            "pregunta": "¿Qué es la LGSS?"
        },
        {
            "nivel": "BÁSICO",
            "pregunta": "¿Cuál es la edad de jubilación ordinaria en España en 2024?"
        },
        {
            "nivel": "INTERMEDIO",
            "pregunta": "¿Cuántos días de incapacidad temporal paga la empresa antes de que pague la Seguridad Social?"
        },
        {
            "nivel": "INTERMEDIO",
            "pregunta": "¿Qué es la base reguladora de una prestación?"
        },
        {
            "nivel": "AVANZADO",
            "pregunta": "¿Cómo se calcula la base de cotización por contingencias comunes de un trabajador autónomo en 2024?"
        },
        {
            "nivel": "AVANZADO",
            "pregunta": "¿Qué artículo de la LGSS regula la incapacidad temporal?"
        },
        {
            "nivel": "CASO PRÁCTICO",
            "pregunta": "Un trabajador con 35 años cotizados y 60 años de edad quiere jubilarse anticipadamente. ¿Puede hacerlo? ¿Qué requisitos debe cumplir?"
        }
    ]
    
    resultados = []
    
    for i, item in enumerate(preguntas, 1):
        print(f"\n{'=' * 80}")
        print(f"PREGUNTA {i}/{len(preguntas)} - NIVEL: {item['nivel']}")
        print(f"{'=' * 80}")
        print(f"❓ {item['pregunta']}")
        print(f"\n{'Pensando...'}")
        
        respuesta = preguntar_salamandra(item['pregunta'])
        
        print(f"\n💬 RESPUESTA:")
        print(f"{respuesta}")
        
        resultados.append({
            "nivel": item['nivel'],
            "pregunta": item['pregunta'],
            "respuesta": respuesta
        })
    
    # Guardar resultados
    with open("test_salamandra_conocimiento_base_resultados.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'=' * 80}")
    print("✅ TEST COMPLETADO")
    print(f"{'=' * 80}")
    print(f"Resultados guardados en: test_salamandra_conocimiento_base_resultados.json")
    print(f"Total preguntas: {len(preguntas)}")
    print(f"{'=' * 80}")

if __name__ == "__main__":
    main()
