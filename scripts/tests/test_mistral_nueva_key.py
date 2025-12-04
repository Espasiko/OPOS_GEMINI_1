#!/usr/bin/env python3
"""
Prueba MISTRAL con nueva key
"""

import requests
import json
import time
import re

MISTRAL_KEY = "FpxxgzuLHRIWlPL6PMUOkzdPblGNBuHF"

PROMPT = """Genera una pregunta tipo test sobre el artículo 205 de la Ley General de la Seguridad Social (LGSS) sobre la edad de jubilación en España.

La pregunta debe incluir:
1. Enunciado claro
2. 4 opciones de respuesta (a, b, c, d)
3. Respuesta correcta
4. Explicación detallada con referencias legales
5. URLs a fuentes oficiales (BOE, INSS, Seguridad Social)

Formato JSON."""

print("="*80)
print("🤖 PRUEBA: MISTRAL MEDIUM 3.1 (NUEVA KEY)")
print("="*80)
print(f"\n🔑 Key: {MISTRAL_KEY[:20]}...")

# Test Mistral
print("\n⏳ Enviando request...")
start = time.time()

response = requests.post(
    "https://api.mistral.ai/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {MISTRAL_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "mistral-medium-latest",
        "messages": [{"role": "user", "content": PROMPT}]
    }
)

duration = time.time() - start

if response.status_code == 200:
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    usage = data["usage"]
    
    # Calcular coste (Mistral Medium: $0.4 input + $2 output)
    input_tokens = usage["prompt_tokens"]
    output_tokens = usage["completion_tokens"]
    cost = (input_tokens / 1_000_000) * 0.4 + (output_tokens / 1_000_000) * 2.0
    
    print(f"\n✅ Respuesta recibida en {duration:.2f}s")
    print(f"\n📊 TOKENS:")
    print(f"   Input:  {input_tokens:,} tokens")
    print(f"   Output: {output_tokens:,} tokens")
    print(f"   Total:  {usage['total_tokens']:,} tokens")
    
    print(f"\n💰 COSTE:")
    print(f"   Input:  ${(input_tokens / 1_000_000) * 0.4:.6f}")
    print(f"   Output: ${(output_tokens / 1_000_000) * 2.0:.6f}")
    print(f"   TOTAL:  ${cost:.6f}")
    
    print(f"\n📈 PROYECCIÓN 10,000 Q&A:")
    print(f"   Coste total: ${cost * 10000:.2f}")
    print(f"   Con tu saldo de €10: {10 / cost:.0f} Q&A posibles")
    
    print(f"\n📝 RESPUESTA COMPLETA:")
    print("-"*80)
    print(content)
    print("-"*80)
    
    # Buscar URLs
    urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', content)
    
    if urls:
        print(f"\n🔗 URLs ENCONTRADAS ({len(urls)}):")
        print("="*80)
        
        for i, url in enumerate(urls, 1):
            print(f"\n{i}. {url}")
            print("   Verificando...", end=" ")
            
            try:
                r = requests.head(url, timeout=10, allow_redirects=True)
                
                if r.status_code == 200:
                    print(f"✅ VÁLIDA (HTTP {r.status_code})")
                elif r.status_code == 404:
                    print(f"❌ NO EXISTE (HTTP 404)")
                    print(f"   ⚠️ MISTRAL INVENTÓ ESTA URL")
                elif r.status_code >= 400:
                    print(f"❌ ERROR (HTTP {r.status_code})")
                    print(f"   ⚠️ URL NO ACCESIBLE")
                else:
                    print(f"⚠️ HTTP {r.status_code}")
                    
            except requests.exceptions.Timeout:
                print(f"⏱️ TIMEOUT (>10s)")
            except requests.exceptions.ConnectionError:
                print(f"❌ NO SE PUEDE CONECTAR")
                print(f"   ⚠️ POSIBLEMENTE INVENTADA")
            except Exception as e:
                print(f"❌ ERROR: {str(e)[:50]}")
    else:
        print("\n⚠️ No se encontraron URLs en la respuesta")
    
    # Guardar resultado
    result = {
        "model": "Mistral Medium 3.1",
        "duration": duration,
        "tokens": {
            "input": input_tokens,
            "output": output_tokens,
            "total": usage['total_tokens']
        },
        "cost": cost,
        "cost_10k": cost * 10000,
        "qa_possible_with_10eur": int(10 / cost),
        "content": content,
        "urls_found": urls
    }
    
    with open("test_mistral_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("✅ PRUEBA COMPLETADA")
    print("="*80)
    print("\n📄 Resultado guardado en: test_mistral_result.json")
    
else:
    print(f"\n❌ Error: {response.status_code}")
    print(response.text)

print("\n")
