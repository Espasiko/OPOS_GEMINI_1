#!/usr/bin/env python3
"""
Prueba CLAUDE 4.5 Sonnet
- Genera Q&A sobre legislación
- Verifica URLs
- Calcula costes
"""

import requests
import json
import time
import re

CLAUDE_KEY = os.getenv("CLAUDE_API_KEY")
if not CLAUDE_KEY:
    print("⚠️ CLAUDE_API_KEY not set")

PROMPT = """Genera una pregunta tipo test sobre el artículo 205 de la Ley General de la Seguridad Social (LGSS) sobre la edad de jubilación en España.

La pregunta debe incluir:
1. Enunciado claro
2. 4 opciones de respuesta (a, b, c, d)
3. Respuesta correcta
4. Explicación detallada con referencias legales
5. URLs a fuentes oficiales (BOE, INSS, Seguridad Social)

Formato JSON."""

print("="*80)
print("🤖 PRUEBA: CLAUDE 4.5 SONNET")
print("="*80)

# Test Claude
print("\n⏳ Enviando request...")
start = time.time()

response = requests.post(
    "https://api.anthropic.com/v1/messages",
    headers={
        "x-api-key": CLAUDE_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    },
    json={
        "model": "claude-sonnet-4-5",
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": PROMPT}]
    }
)

duration = time.time() - start

if response.status_code == 200:
    data = response.json()
    content = data["content"][0]["text"]
    usage = data["usage"]
    
    # Calcular coste
    input_tokens = usage["input_tokens"]
    output_tokens = usage["output_tokens"]
    cost = (input_tokens / 1_000_000) * 3.0 + (output_tokens / 1_000_000) * 15.0
    
    print(f"\n✅ Respuesta recibida en {duration:.2f}s")
    print(f"\n📊 TOKENS:")
    print(f"   Input:  {input_tokens:,} tokens")
    print(f"   Output: {output_tokens:,} tokens")
    print(f"   Total:  {input_tokens + output_tokens:,} tokens")
    
    print(f"\n💰 COSTE:")
    print(f"   Input:  ${(input_tokens / 1_000_000) * 3.0:.6f}")
    print(f"   Output: ${(output_tokens / 1_000_000) * 15.0:.6f}")
    print(f"   TOTAL:  ${cost:.6f}")
    
    print(f"\n📈 PROYECCIÓN 10,000 Q&A:")
    print(f"   Coste total: ${cost * 10000:.2f}")
    print(f"   Con tu saldo de €5: {5 / cost:.0f} Q&A posibles")
    
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
                # Verificar URL
                r = requests.head(url, timeout=10, allow_redirects=True)
                
                if r.status_code == 200:
                    print(f"✅ VÁLIDA (HTTP {r.status_code})")
                elif r.status_code == 404:
                    print(f"❌ NO EXISTE (HTTP 404)")
                    print(f"   ⚠️ CLAUDE INVENTÓ ESTA URL")
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
        "model": "Claude 4.5 Sonnet",
        "duration": duration,
        "tokens": {
            "input": input_tokens,
            "output": output_tokens,
            "total": input_tokens + output_tokens
        },
        "cost": cost,
        "cost_10k": cost * 10000,
        "qa_possible_with_5eur": int(5 / cost),
        "content": content,
        "urls_found": urls
    }
    
    with open("test_claude_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("✅ PRUEBA COMPLETADA")
    print("="*80)
    print("\n📄 Resultado guardado en: test_claude_result.json")
    
else:
    print(f"\n❌ Error: {response.status_code}")
    print(response.text)

print("\n")
