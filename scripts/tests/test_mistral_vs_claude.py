#!/usr/bin/env python3
"""
Prueba comparativa: Mistral Large 2 vs Claude 3.5 Sonnet
- Genera Q&A sobre legislación española
- Verifica URLs devueltas
- Calcula costes reales
"""

import os
import json
import requests
from datetime import datetime
from anthropic import Anthropic
from mistralai.client import MistralClient

# Configuración
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

# Precios (por 1M tokens)
MISTRAL_PRICES = {"input": 2.00, "output": 6.00}
CLAUDE_PRICES = {"input": 3.00, "output": 15.00}

# Prompt de prueba
PROMPT = """
Genera una pregunta tipo test sobre el artículo 205 de la Ley General de la Seguridad Social (LGSS) sobre la edad de jubilación en España.

La pregunta debe incluir:
1. Enunciado claro
2. 4 opciones de respuesta (a, b, c, d)
3. Respuesta correcta
4. Explicación detallada con referencias legales
5. URLs a fuentes oficiales (BOE, INSS, etc.)

Formato JSON:
{
  "question": "...",
  "options": {
    "a": "...",
    "b": "...",
    "c": "...",
    "d": "..."
  },
  "correct_answer": "c",
  "explanation": "...",
  "legal_references": ["Art. 205 LGSS", "..."],
  "sources": ["https://www.boe.es/...", "..."]
}
"""

def test_mistral():
    """Prueba con Mistral Large 2"""
    print("\n" + "="*80)
    print("🤖 PRUEBA 1: MISTRAL LARGE 2")
    print("="*80)
    
    try:
        client = MistralClient(api_key=MISTRAL_API_KEY)
        
        print("\n⏳ Enviando request a Mistral...")
        start_time = datetime.now()
        
        response = client.chat(
            model="mistral-large-latest",
            messages=[{
                "role": "user",
                "content": PROMPT
            }]
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Extraer respuesta
        content = response.choices[0].message.content
        
        # Calcular tokens y coste
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens
        
        input_cost = (input_tokens / 1_000_000) * MISTRAL_PRICES["input"]
        output_cost = (output_tokens / 1_000_000) * MISTRAL_PRICES["output"]
        total_cost = input_cost + output_cost
        
        print(f"\n✅ Respuesta recibida en {duration:.2f}s")
        print(f"\n📊 TOKENS:")
        print(f"   Input:  {input_tokens:,} tokens")
        print(f"   Output: {output_tokens:,} tokens")
        print(f"   Total:  {total_tokens:,} tokens")
        
        print(f"\n💰 COSTE:")
        print(f"   Input:  ${input_cost:.6f}")
        print(f"   Output: ${output_cost:.6f}")
        print(f"   TOTAL:  ${total_cost:.6f}")
        
        print(f"\n📝 RESPUESTA:")
        print(content[:500] + "..." if len(content) > 500 else content)
        
        # Intentar parsear JSON
        try:
            qa_data = json.loads(content)
            sources = qa_data.get("sources", [])
            
            if sources:
                print(f"\n🔗 URLs ENCONTRADAS ({len(sources)}):")
                for i, url in enumerate(sources, 1):
                    print(f"   {i}. {url}")
                    verify_url(url)
            else:
                print("\n⚠️ No se encontraron URLs en la respuesta")
                
        except json.JSONDecodeError:
            print("\n⚠️ La respuesta no es JSON válido")
            # Buscar URLs manualmente
            import re
            urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', content)
            if urls:
                print(f"\n🔗 URLs ENCONTRADAS EN TEXTO ({len(urls)}):")
                for i, url in enumerate(urls, 1):
                    print(f"   {i}. {url}")
                    verify_url(url)
        
        return {
            "model": "Mistral Large 2",
            "duration": duration,
            "tokens": {
                "input": input_tokens,
                "output": output_tokens,
                "total": total_tokens
            },
            "cost": total_cost,
            "content": content
        }
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return None

def test_claude():
    """Prueba con Claude 3.5 Sonnet"""
    print("\n" + "="*80)
    print("🤖 PRUEBA 2: CLAUDE 3.5 SONNET")
    print("="*80)
    
    try:
        client = Anthropic(api_key=CLAUDE_API_KEY)
        
        print("\n⏳ Enviando request a Claude...")
        start_time = datetime.now()
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": PROMPT
            }]
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Extraer respuesta
        content = response.content[0].text
        
        # Calcular tokens y coste
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        total_tokens = input_tokens + output_tokens
        
        input_cost = (input_tokens / 1_000_000) * CLAUDE_PRICES["input"]
        output_cost = (output_tokens / 1_000_000) * CLAUDE_PRICES["output"]
        total_cost = input_cost + output_cost
        
        print(f"\n✅ Respuesta recibida en {duration:.2f}s")
        print(f"\n📊 TOKENS:")
        print(f"   Input:  {input_tokens:,} tokens")
        print(f"   Output: {output_tokens:,} tokens")
        print(f"   Total:  {total_tokens:,} tokens")
        
        print(f"\n💰 COSTE:")
        print(f"   Input:  ${input_cost:.6f}")
        print(f"   Output: ${output_cost:.6f}")
        print(f"   TOTAL:  ${total_cost:.6f}")
        
        print(f"\n📝 RESPUESTA:")
        print(content[:500] + "..." if len(content) > 500 else content)
        
        # Intentar parsear JSON
        try:
            qa_data = json.loads(content)
            sources = qa_data.get("sources", [])
            
            if sources:
                print(f"\n🔗 URLs ENCONTRADAS ({len(sources)}):")
                for i, url in enumerate(sources, 1):
                    print(f"   {i}. {url}")
                    verify_url(url)
            else:
                print("\n⚠️ No se encontraron URLs en la respuesta")
                
        except json.JSONDecodeError:
            print("\n⚠️ La respuesta no es JSON válido")
            # Buscar URLs manualmente
            import re
            urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', content)
            if urls:
                print(f"\n🔗 URLs ENCONTRADAS EN TEXTO ({len(urls)}):")
                for i, url in enumerate(urls, 1):
                    print(f"   {i}. {url}")
                    verify_url(url)
        
        return {
            "model": "Claude 3.5 Sonnet",
            "duration": duration,
            "tokens": {
                "input": input_tokens,
                "output": output_tokens,
                "total": total_tokens
            },
            "cost": total_cost,
            "content": content
        }
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return None

def verify_url(url):
    """Verifica si una URL es válida y accesible"""
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        if response.status_code == 200:
            print(f"      ✅ VÁLIDA (HTTP {response.status_code})")
        elif response.status_code == 404:
            print(f"      ❌ NO EXISTE (HTTP 404)")
        else:
            print(f"      ⚠️ HTTP {response.status_code}")
    except requests.exceptions.Timeout:
        print(f"      ⏱️ TIMEOUT (>5s)")
    except requests.exceptions.RequestException as e:
        print(f"      ❌ ERROR: {str(e)[:50]}")

def compare_results(mistral_result, claude_result):
    """Compara los resultados de ambos modelos"""
    print("\n" + "="*80)
    print("📊 COMPARACIÓN FINAL")
    print("="*80)
    
    if not mistral_result or not claude_result:
        print("\n⚠️ No se pueden comparar: falta algún resultado")
        return
    
    print(f"\n⏱️ VELOCIDAD:")
    print(f"   Mistral: {mistral_result['duration']:.2f}s")
    print(f"   Claude:  {claude_result['duration']:.2f}s")
    faster = "Mistral" if mistral_result['duration'] < claude_result['duration'] else "Claude"
    print(f"   🏆 Más rápido: {faster}")
    
    print(f"\n📊 TOKENS:")
    print(f"   Mistral: {mistral_result['tokens']['total']:,} tokens")
    print(f"   Claude:  {claude_result['tokens']['total']:,} tokens")
    
    print(f"\n💰 COSTE:")
    print(f"   Mistral: ${mistral_result['cost']:.6f}")
    print(f"   Claude:  ${claude_result['cost']:.6f}")
    diff = claude_result['cost'] - mistral_result['cost']
    pct = (diff / mistral_result['cost']) * 100
    print(f"   💸 Claude es {pct:.1f}% más caro (${diff:.6f} más)")
    
    print(f"\n📈 PROYECCIÓN PARA 10,000 Q&A:")
    mistral_10k = mistral_result['cost'] * 10000
    claude_10k = claude_result['cost'] * 10000
    print(f"   Mistral: ${mistral_10k:.2f}")
    print(f"   Claude:  ${claude_10k:.2f}")
    print(f"   Ahorro con Mistral: ${claude_10k - mistral_10k:.2f}")
    
    print(f"\n📝 LONGITUD RESPUESTA:")
    print(f"   Mistral: {len(mistral_result['content'])} caracteres")
    print(f"   Claude:  {len(claude_result['content'])} caracteres")

def main():
    """Función principal"""
    print("\n" + "="*80)
    print("🧪 PRUEBA COMPARATIVA: MISTRAL vs CLAUDE")
    print("="*80)
    print("\nPregunta de prueba:")
    print("Generar Q&A sobre artículo 205 LGSS (edad de jubilación)")
    print("\nObjetivos:")
    print("1. Comparar calidad de respuestas")
    print("2. Verificar URLs devueltas")
    print("3. Calcular costes reales")
    
    # Ejecutar pruebas
    mistral_result = test_mistral()
    claude_result = test_claude()
    
    # Comparar resultados
    if mistral_result and claude_result:
        compare_results(mistral_result, claude_result)
    
    # Guardar resultados
    results = {
        "timestamp": datetime.now().isoformat(),
        "mistral": mistral_result,
        "claude": claude_result
    }
    
    with open("test_mistral_vs_claude_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("✅ PRUEBA COMPLETADA")
    print("="*80)
    print("\n📄 Resultados guardados en: test_mistral_vs_claude_results.json")
    print("\n")

if __name__ == "__main__":
    main()
