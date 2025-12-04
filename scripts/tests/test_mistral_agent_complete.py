#!/usr/bin/env python3
"""
Prueba completa del Agente Mistral
- Prueba API key nueva
- Prueba endpoint de agentes
- Verifica URLs
- Compara con Claude
"""

import requests
import json
import time
import re

# API Keys
# API Keys
MISTRAL_KEY_OLD = os.getenv("MISTRAL_API_KEY_OLD")
MISTRAL_KEY_NEW = os.getenv("MISTRAL_API_KEY_NEW")
MISTRAL_AGENT_ID = os.getenv("MISTRAL_AGENT_ID", "ag_019ad601946d7323a81c544229de40a1")
CLAUDE_KEY = os.getenv("CLAUDE_API_KEY")

PROMPT = """Genera una pregunta tipo test sobre el artículo 205 de la Ley General de la Seguridad Social (LGSS) sobre la edad de jubilación en España.

Incluye:
1. Enunciado claro
2. 4 opciones (a,b,c,d)
3. Respuesta correcta
4. Explicación con referencias legales
5. URLs a fuentes oficiales (BOE, INSS)

Formato JSON."""

def verify_url(url):
    """Verifica si una URL es válida"""
    try:
        r = requests.head(url, timeout=10, allow_redirects=True)
        if r.status_code == 200:
            return "✅ VÁLIDA", r.status_code
        elif r.status_code == 404:
            return "❌ NO EXISTE", r.status_code
        elif r.status_code == 403:
            return "⚠️ BLOQUEADA", r.status_code
        else:
            return f"⚠️ HTTP {r.status_code}", r.status_code
    except requests.exceptions.Timeout:
        return "⏱️ TIMEOUT", 0
    except requests.exceptions.ConnectionError:
        return "❌ NO CONECTA", 0
    except Exception as e:
        return f"❌ ERROR", 0

print("="*80)
print("🧪 PRUEBA COMPLETA: MISTRAL AGENT vs CLAUDE")
print("="*80)

# ============================================================================
# PRUEBA 1: Mistral API Key Vieja
# ============================================================================
print("\n" + "="*80)
print("1️⃣ PROBANDO MISTRAL API KEY VIEJA")
print("="*80)
print(f"Key: {MISTRAL_KEY_OLD[:20]}...")

response = requests.post(
    "https://api.mistral.ai/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {MISTRAL_KEY_OLD}",
        "Content-Type": "application/json"
    },
    json={
        "model": "mistral-medium-latest",
        "messages": [{"role": "user", "content": "Hola"}]
    }
)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("✅ KEY VIEJA FUNCIONA")
else:
    print(f"❌ KEY VIEJA NO FUNCIONA: {response.text[:100]}")

# ============================================================================
# PRUEBA 2: Mistral API Key Nueva
# ============================================================================
print("\n" + "="*80)
print("2️⃣ PROBANDO MISTRAL API KEY NUEVA")
print("="*80)
print(f"Key: {MISTRAL_KEY_NEW[:20]}...")

response = requests.post(
    "https://api.mistral.ai/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {MISTRAL_KEY_NEW}",
        "Content-Type": "application/json"
    },
    json={
        "model": "mistral-medium-latest",
        "messages": [{"role": "user", "content": "Hola"}]
    }
)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("✅ KEY NUEVA FUNCIONA")
    MISTRAL_KEY = MISTRAL_KEY_NEW
else:
    print(f"❌ KEY NUEVA NO FUNCIONA: {response.text[:100]}")
    MISTRAL_KEY = MISTRAL_KEY_OLD

# ============================================================================
# PRUEBA 3: Mistral Agent Endpoint
# ============================================================================
print("\n" + "="*80)
print("3️⃣ PROBANDO MISTRAL AGENT")
print("="*80)
print(f"Agent ID: {MISTRAL_AGENT_ID}")

start = time.time()
response = requests.post(
    "https://api.mistral.ai/v1/agents/completions",
    headers={
        "Authorization": f"Bearer {MISTRAL_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "agent_id": MISTRAL_AGENT_ID,
        "messages": [{"role": "user", "content": PROMPT}]
    }
)
duration_mistral = time.time() - start

print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    usage = data["usage"]
    
    input_tokens = usage["prompt_tokens"]
    output_tokens = usage["completion_tokens"]
    
    # Costes del agente
    # Modelo base: $0.4 input + $2 output (Mistral Medium)
    # + Web search: $0.03/llamada
    # + Code execution: $0.03/llamada
    cost_base = (input_tokens / 1_000_000) * 0.4 + (output_tokens / 1_000_000) * 2.0
    
    print(f"\n✅ Respuesta en {duration_mistral:.2f}s")
    print(f"\n📊 TOKENS:")
    print(f"   Input:  {input_tokens:,}")
    print(f"   Output: {output_tokens:,}")
    print(f"   Total:  {usage['total_tokens']:,}")
    
    print(f"\n💰 COSTE:")
    print(f"   Base: ${cost_base:.6f}")
    print(f"   (+ herramientas si se usaron)")
    
    print(f"\n📝 RESPUESTA:")
    print("-"*80)
    print(content[:500] + "..." if len(content) > 500 else content)
    print("-"*80)
    
    # Buscar URLs
    urls_mistral = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', content)
    
    if urls_mistral:
        print(f"\n🔗 URLs ENCONTRADAS ({len(urls_mistral)}):")
        mistral_url_results = []
        for i, url in enumerate(urls_mistral, 1):
            print(f"\n{i}. {url}")
            print("   Verificando...", end=" ")
            status, code = verify_url(url)
            print(status)
            mistral_url_results.append({
                "url": url,
                "status": status,
                "code": code
            })
    
    mistral_result = {
        "success": True,
        "duration": duration_mistral,
        "tokens": usage,
        "cost": cost_base,
        "content": content,
        "urls": urls_mistral if urls_mistral else [],
        "url_results": mistral_url_results if urls_mistral else []
    }
    
else:
    print(f"❌ ERROR: {response.text}")
    mistral_result = {"success": False, "error": response.text}

# ============================================================================
# PRUEBA 4: Claude para comparar
# ============================================================================
print("\n" + "="*80)
print("4️⃣ PROBANDO CLAUDE 4.5 SONNET")
print("="*80)

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
    
    input_tokens = usage["input_tokens"]
    output_tokens = usage["output_tokens"]
    cost = (input_tokens / 1_000_000) * 3.0 + (output_tokens / 1_000_000) * 15.0
    
    print(f"\n✅ Respuesta en {duration_claude:.2f}s")
    print(f"\n📊 TOKENS:")
    print(f"   Input:  {input_tokens:,}")
    print(f"   Output: {output_tokens:,}")
    
    print(f"\n💰 COSTE: ${cost:.6f}")
    
    print(f"\n📝 RESPUESTA:")
    print("-"*80)
    print(content[:500] + "..." if len(content) > 500 else content)
    print("-"*80)
    
    # Buscar URLs
    urls_claude = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', content)
    
    if urls_claude:
        print(f"\n🔗 URLs ENCONTRADAS ({len(urls_claude)}):")
        claude_url_results = []
        for i, url in enumerate(urls_claude, 1):
            print(f"\n{i}. {url}")
            print("   Verificando...", end=" ")
            status, code = verify_url(url)
            print(status)
            claude_url_results.append({
                "url": url,
                "status": status,
                "code": code
            })
    
    claude_result = {
        "success": True,
        "duration": duration_claude,
        "tokens": {"input": input_tokens, "output": output_tokens},
        "cost": cost,
        "content": content,
        "urls": urls_claude if urls_claude else [],
        "url_results": claude_url_results if urls_claude else []
    }
else:
    print(f"❌ ERROR: {response.text}")
    claude_result = {"success": False, "error": response.text}

# ============================================================================
# COMPARACIÓN FINAL
# ============================================================================
print("\n" + "="*80)
print("📊 COMPARACIÓN FINAL")
print("="*80)

if mistral_result.get("success") and claude_result.get("success"):
    print(f"\n⏱️ VELOCIDAD:")
    print(f"   Mistral Agent: {mistral_result['duration']:.2f}s")
    print(f"   Claude:        {claude_result['duration']:.2f}s")
    faster = "Mistral" if mistral_result['duration'] < claude_result['duration'] else "Claude"
    print(f"   🏆 Más rápido: {faster}")
    
    print(f"\n💰 COSTE:")
    print(f"   Mistral Agent: ${mistral_result['cost']:.6f}")
    print(f"   Claude:        ${claude_result['cost']:.6f}")
    diff = claude_result['cost'] - mistral_result['cost']
    if diff > 0:
        pct = (diff / mistral_result['cost']) * 100
        print(f"   💸 Claude es {pct:.1f}% más caro")
    else:
        pct = (abs(diff) / claude_result['cost']) * 100
        print(f"   💸 Mistral es {pct:.1f}% más caro")
    
    print(f"\n📈 PROYECCIÓN 10,000 Q&A:")
    print(f"   Mistral: ${mistral_result['cost'] * 10000:.2f}")
    print(f"   Claude:  ${claude_result['cost'] * 10000:.2f}")
    
    print(f"\n🔗 VERIFICACIÓN URLs:")
    
    # Mistral URLs
    if mistral_result.get('url_results'):
        valid_mistral = sum(1 for r in mistral_result['url_results'] if '✅' in r['status'])
        total_mistral = len(mistral_result['url_results'])
        print(f"   Mistral: {valid_mistral}/{total_mistral} válidas ({valid_mistral/total_mistral*100:.0f}%)")
    else:
        print(f"   Mistral: Sin URLs")
    
    # Claude URLs
    if claude_result.get('url_results'):
        valid_claude = sum(1 for r in claude_result['url_results'] if '✅' in r['status'])
        total_claude = len(claude_result['url_results'])
        print(f"   Claude:  {valid_claude}/{total_claude} válidas ({valid_claude/total_claude*100:.0f}%)")
    else:
        print(f"   Claude: Sin URLs")

# Guardar resultados
results = {
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    "mistral_agent": mistral_result,
    "claude": claude_result
}

with open("test_mistral_vs_claude_complete.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\n" + "="*80)
print("✅ PRUEBA COMPLETADA")
print("="*80)
print("\n📄 Resultados guardados en: test_mistral_vs_claude_complete.json\n")
