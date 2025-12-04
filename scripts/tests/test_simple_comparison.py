#!/usr/bin/env python3
"""
Prueba simple: Mistral vs Claude
Sin dependencias externas, solo requests
"""

import os
import json
import time

# Cargar .env
import sys
sys.path.insert(0, 'backend')

try:
    from dotenv import load_dotenv
    load_dotenv('backend/.env.backend')
except:
    pass

# API Keys
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")
CLAUDE_KEY = os.getenv("CLAUDE_API_KEY")

print(f"🔑 Mistral Key: {MISTRAL_KEY[:20]}...")
print(f"🔑 Claude Key: {CLAUDE_KEY[:20]}...")

# Prompt
PROMPT = """Genera una pregunta tipo test sobre el artículo 205 de la LGSS sobre edad de jubilación en España.

Incluye:
1. Pregunta clara
2. 4 opciones (a,b,c,d)
3. Respuesta correcta
4. Explicación con referencias legales
5. URLs a fuentes oficiales (BOE, INSS)

Formato JSON."""

print("="*80)
print("PRUEBA: MISTRAL vs CLAUDE")
print("="*80)

# Test Mistral
print("\n1. MISTRAL LARGE 2")
print("-"*80)

try:
    import requests
    
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
    duration_mistral = time.time() - start
    
    if response.status_code == 200:
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        usage = data["usage"]
        
        # Calcular coste
        input_tokens = usage["prompt_tokens"]
        output_tokens = usage["completion_tokens"]
        cost = (input_tokens / 1_000_000) * 2.0 + (output_tokens / 1_000_000) * 6.0
        
        print(f"✅ Respuesta en {duration_mistral:.2f}s")
        print(f"📊 Tokens: {input_tokens} input + {output_tokens} output = {usage['total_tokens']} total")
        print(f"💰 Coste: ${cost:.6f}")
        print(f"\n📝 Respuesta:")
        print(content[:300] + "...")
        
        # Buscar URLs
        import re
        urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', content)
        if urls:
            print(f"\n🔗 URLs encontradas ({len(urls)}):")
            for url in urls:
                print(f"   - {url}")
        
        mistral_cost = cost
        mistral_tokens = usage['total_tokens']
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        mistral_cost = 0
        mistral_tokens = 0
        
except Exception as e:
    print(f"❌ Error: {e}")
    mistral_cost = 0
    mistral_tokens = 0

# Test Claude
print("\n\n2. CLAUDE 3.5 SONNET")
print("-"*80)

try:
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
    duration_claude = time.time() - start
    
    if response.status_code == 200:
        data = response.json()
        content = data["content"][0]["text"]
        usage = data["usage"]
        
        # Calcular coste
        input_tokens = usage["input_tokens"]
        output_tokens = usage["output_tokens"]
        cost = (input_tokens / 1_000_000) * 3.0 + (output_tokens / 1_000_000) * 15.0
        
        print(f"✅ Respuesta en {duration_claude:.2f}s")
        print(f"📊 Tokens: {input_tokens} input + {output_tokens} output = {input_tokens + output_tokens} total")
        print(f"💰 Coste: ${cost:.6f}")
        print(f"\n📝 Respuesta:")
        print(content[:300] + "...")
        
        # Buscar URLs
        import re
        urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', content)
        if urls:
            print(f"\n🔗 URLs encontradas ({len(urls)}):")
            for url in urls:
                print(f"   - {url}")
        
        claude_cost = cost
        claude_tokens = input_tokens + output_tokens
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        claude_cost = 0
        claude_tokens = 0
        
except Exception as e:
    print(f"❌ Error: {e}")
    claude_cost = 0
    claude_tokens = 0

# Comparación
print("\n\n" + "="*80)
print("COMPARACIÓN")
print("="*80)

if mistral_cost > 0 and claude_cost > 0:
    print(f"\n⏱️ VELOCIDAD:")
    print(f"   Mistral: {duration_mistral:.2f}s")
    print(f"   Claude:  {duration_claude:.2f}s")
    
    print(f"\n📊 TOKENS:")
    print(f"   Mistral: {mistral_tokens:,}")
    print(f"   Claude:  {claude_tokens:,}")
    
    print(f"\n💰 COSTE:")
    print(f"   Mistral: ${mistral_cost:.6f}")
    print(f"   Claude:  ${claude_cost:.6f}")
    diff = claude_cost - mistral_cost
    pct = (diff / mistral_cost) * 100 if mistral_cost > 0 else 0
    print(f"   Diferencia: Claude es {pct:.1f}% más caro (${diff:.6f})")
    
    print(f"\n📈 PROYECCIÓN 10,000 Q&A:")
    print(f"   Mistral: ${mistral_cost * 10000:.2f}")
    print(f"   Claude:  ${claude_cost * 10000:.2f}")
    print(f"   Ahorro con Mistral: ${(claude_cost - mistral_cost) * 10000:.2f}")

print("\n" + "="*80)
print("FIN")
print("="*80 + "\n")
