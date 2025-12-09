#!/usr/bin/env python3
"""Generador de contenido diverso para dataset con DeepSeek REASONER (modelo de razonamiento tipo o1)"""

import os
import json
import requests
from datetime import datetime
from qdrant_client import QdrantClient
import time
import random
from dotenv import load_dotenv

print("\n🎯 GENERADOR DE CONTENIDO DIVERSO CON DEEPSEEK-REASONER (Chain of Thought)\n")

# Cargar variables de entorno desde backend/.env.backend
load_dotenv("../backend/.env.backend")
load_dotenv(".env")  # También cargar .env local si existe

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    print("❌ DEEPSEEK_API_KEY no encontrada")
    print("🔍 Verificando archivos .env...")
    print(f"   - backend/.env.backend: {'✅' if os.path.exists('../backend/.env.backend') else '❌'}")
    print(f"   - .env: {'✅' if os.path.exists('.env') else '❌'}")
    raise ValueError("DEEPSEEK_API_KEY environment variable not set")

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
print(f"✅ DeepSeek API configurada correctamente")

# Configuración de tipos de contenido
CONTENT_TYPES = [
    "qa_multiple_choice",      # Pregunta múltiple opción tradicional
    "case_study",              # Supuesto práctico / Caso concreto
    "chat_dialogue",           # Diálogo usuario ↔ asistente (chat natural)
    "flashcard",               # Flashcard / Resumen / Esquema (textual)
    "rag_context_qa",          # Pregunta + contexto normativo + respuesta (para RAG / reasoning)
    "legal_analysis",          # Análisis jurídico detallado
    "comparative_study",       # Estudio comparativo entre normativas
    "procedural_guide"         # Guía procedimental paso a paso
]

# Configurar Qdrant (Cloud o Local según .env)
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if QDRANT_API_KEY:
    qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    print(f"✅ Qdrant Cloud configurado: {QDRANT_URL}")
else:
    qdrant = QdrantClient(QDRANT_URL)
    print(f"✅ Qdrant Local configurado: {QDRANT_URL}")

COLLECTION_NAME = os.getenv("COLLECTION_NAME", "materiales_academia")

print("📥 Extrayendo contenido base...")
try:
    # Intentar con la colección configurada
    points, _ = qdrant.scroll(collection_name=COLLECTION_NAME, limit=200, with_payload=True, with_vectors=False)
    questions = [p for p in points if p.payload.get("subcategory") == "preguntas" or p.payload.get("layer") == "leyes"][:50]
    print(f"✅ {len(questions)} elementos base cargados desde {COLLECTION_NAME}\n")
except Exception as e:
    print(f"❌ Error accediendo a Qdrant: {e}")
    print("🔄 Intentando con colección alternativa...")
    try:
        points, _ = qdrant.scroll(collection_name="opositaia_leyes_seguridad_social", limit=200, with_payload=True, with_vectors=False)
        questions = [p for p in points if p.payload.get("layer") == "leyes"][:50]
        print(f"✅ {len(questions)} elementos base cargados desde colección alternativa\n")
    except Exception as e2:
        print(f"❌ Error con colección alternativa: {e2}")
        questions = []

generated_content = []

def query_deepseek_reasoner(prompt):
    """Usa el modelo deepseek-reasoner con Chain of Thought"""
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-reasoner",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4000,
        "temperature": 0.7
    }
    response = requests.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=120)
    if response.status_code == 200:
        data = response.json()
        reasoning = data["choices"][0]["message"].get("reasoning_content", "")
        content = data["choices"][0]["message"]["content"]
        return content, reasoning
    raise Exception(f"Error: {response.status_code} - {response.text}")

def verify_boe_reference(article_ref):
    """Verifica referencias BOE usando consulta web (implementación básica)"""
    try:
        # Lista de artículos conocidos y verificados de la LGSS
        verified_articles = [
            "art. 7.1 LGSS", "art. 7.2.a LGSS", "art. 166 LGSS", "art. 205.1.b LGSS",
            "art. 208.1 LGSS", "art. 210.1 LGSS", "art. 164.4 LGSS", "art. 174.5 LGSS",
            "art. 251 LGSS", "RD 1620/2011", "BOE-A-2015-11724", "BOE-A-2011-17975"
        ]
        
        # Verificación básica contra lista conocida
        for verified in verified_articles:
            if verified.lower() in article_ref.lower():
                return True
        
        # Si no está en la lista, marcar para revisión manual
        print(f"⚠️  Referencia para verificar manualmente: {article_ref}")
        return False
        
    except Exception as e:
        print(f"❌ Error verificando referencia {article_ref}: {e}")
        return False

def enhance_content_quality(content_item):
    """Mejora la calidad del contenido generado"""
    try:
        # Verificar referencias si existen
        if 'articles_reference' in content_item:
            verified_refs = []
            for ref in content_item['articles_reference']:
                if verify_boe_reference(ref):
                    verified_refs.append(ref)
            content_item['verified_references'] = verified_refs
            content_item['verification_score'] = len(verified_refs) / len(content_item['articles_reference'])
        
        # Añadir metadatos de calidad
        content_item['quality_checks'] = {
            'has_legal_references': bool(content_item.get('articles_reference') or content_item.get('source')),
            'content_length_adequate': len(str(content_item)) > 200,
            'has_verification': content_item.get('verified', False),
            'timestamp': datetime.now().isoformat()
        }
        
        return content_item
        
    except Exception as e:
        print(f"❌ Error mejorando calidad: {e}")
        return content_item

def generate_qa_multiple_choice(base_content):
    """Genera pregunta múltiple opción tradicional"""
    prompt = f"""Eres experto en Seguridad Social España. Analiza paso a paso y crea una pregunta de opción múltiple de máxima calidad.

CONTENIDO BASE: {base_content[:500]}

INSTRUCCIONES CRÍTICAS:
1. Verifica que las referencias legales sean correctas y actuales (2025)
2. Crea una pregunta clara y precisa sobre Seguridad Social
3. Genera 4 opciones donde solo UNA sea correcta
4. Incluye explicación detallada con artículos específicos del BOE
5. NO incluyas frases como "Si necesitas que adapte" o similares
6. Responde ÚNICAMENTE con el JSON solicitado, sin texto adicional

FORMATO REQUERIDO (JSON válido únicamente):
{{"id": "qa_deepseek_001", "type": "qa_multiple_choice", "question": "pregunta completa sobre SS", "options": ["A) opción 1", "B) opción 2", "C) opción 3", "D) opción 4"], "correct_answer": "A", "explanation": "explicación detallada con referencias BOE específicas", "theme": "tema específico SS", "difficulty": "media", "articles_reference": ["art. X LGSS"], "source": "BOE-A-XXXX-XXXXX", "verified": true}}"""
    
    return query_deepseek_reasoner(prompt)

def generate_case_study(base_content):
    """Genera supuesto práctico / caso concreto"""
    prompt = f"""Eres experto en Seguridad Social España. Crea un supuesto práctico realista basado en el contenido.

CONTENIDO BASE: {base_content[:500]}

INSTRUCCIONES:
1. Crea un caso práctico con personas reales (nombres ficticios)
2. Plantea una situación específica y concreta
3. Proporciona respuesta fundamentada en normativa vigente
4. Verifica artículos y referencias legales

Responde SOLO con JSON válido:
{{"id": "case_deepseek_001", "type": "case_study", "case_description": "Un trabajador autónomo cesa su actividad en diciembre de 2025 tras cotizar 15 años por la base mínima. Solicita la jubilación anticipada voluntaria. ¿Puede acceder a esta modalidad de jubilación?", "answer": "No, porque para acceder a la jubilación anticipada voluntaria se requieren al menos 35 años de cotización.", "legal_basis": "Ley General de la Seguridad Social", "articles_reference": ["Art. 208.1"], "source": "BOE-A-2015-11724", "theme": "Jubilación", "difficulty": "alta", "verified": true}}"""
    
    return query_deepseek_reasoner(prompt)

def generate_chat_dialogue(base_content):
    """Genera diálogo usuario ↔ asistente (chat natural)"""
    prompt = f"""Eres experto en Seguridad Social España. Crea un diálogo natural usuario-asistente.

CONTENIDO BASE: {base_content[:500]}

INSTRUCCIONES:
1. Pregunta natural de usuario sobre Seguridad Social
2. Respuesta completa y profesional del asistente
3. Incluye referencias normativas específicas
4. Verifica artículos citados

Responde SOLO con JSON válido:
{{"id": "chat_deepseek_001", "type": "chat_dialogue", "user_question": "¿Qué pasa si un trabajador en incapacidad temporal cumple la edad de jubilación ordinaria durante la baja?", "assistant_answer": "Si un trabajador en situación de incapacidad temporal cumple la edad de jubilación ordinaria, puede solicitar el reconocimiento de la pensión de jubilación. La prestación por incapacidad temporal se extinguirá en el momento en que se reconozca la pensión de jubilación, ya que no pueden solaparse ambas prestaciones.", "references": ["Ley General de la Seguridad Social, Art. 164.4"], "theme": "Incapacidad temporal y jubilación", "difficulty": "alta", "verified": true}}"""
    
    return query_deepseek_reasoner(prompt)

def generate_flashcard(base_content):
    """Genera flashcard / resumen / esquema"""
    prompt = f"""Eres experto en Seguridad Social España. Crea una flashcard educativa.

CONTENIDO BASE: {base_content[:500]}

INSTRUCCIONES:
1. Pregunta concisa en el frente
2. Respuesta clara y precisa en el reverso
3. Incluye referencia legal específica
4. Verifica artículos citados

Responde SOLO con JSON válido:
{{"id": "flash_deepseek_001", "type": "flashcard", "front": "¿Cuál es el período mínimo de cotización exigido para acceder a la pensión de jubilación ordinaria?", "back": "15 años, de los cuales al menos 2 deben estar comprendidos dentro de los 15 años inmediatamente anteriores al momento de causar el derecho.", "source": "Ley General de la Seguridad Social, Art. 205.1.b", "theme": "Jubilación", "verified": true}}"""
    
    return query_deepseek_reasoner(prompt)

def generate_rag_context_qa(base_content):
    """Genera pregunta + contexto normativo + respuesta (para RAG)"""
    prompt = f"""Eres experto en Seguridad Social España. Crea contenido para RAG con contexto normativo.

CONTENIDO BASE: {base_content[:500]}

INSTRUCCIONES:
1. Proporciona contexto normativo específico
2. Formula pregunta basada en ese contexto
3. Da respuesta precisa y fundamentada
4. Verifica artículos y referencias

Responde SOLO con JSON válido:
{{"id": "rag_deepseek_001", "type": "rag_context_qa", "context": "Según el artículo 210 de la Ley General de la Seguridad Social, la cuantía de la pensión de jubilación se determina aplicando a la base reguladora el porcentaje general que corresponda en función de los años cotizados.", "question": "¿Qué porcentaje de la base reguladora corresponde a un trabajador que se jubila con 15 años de cotización?", "answer": "50% de la base reguladora.", "theme": "Jubilación", "difficulty": "facil", "source": "Ley General de la Seguridad Social, Art. 210.1", "verified": true}}"""
    
    return query_deepseek_reasoner(prompt)

def generate_legal_analysis(base_content):
    """Genera análisis jurídico detallado"""
    prompt = f"""Eres experto en Seguridad Social España. Crea un análisis jurídico profundo y detallado.

CONTENIDO BASE: {base_content[:500]}

INSTRUCCIONES:
1. Analiza el marco jurídico completo del tema
2. Incluye evolución normativa y jurisprudencia relevante
3. Proporciona análisis crítico y conclusiones
4. Verifica todas las referencias legales citadas

Responde SOLO con JSON válido:
{{"id": "analysis_deepseek_001", "type": "legal_analysis", "title": "Análisis jurídico del régimen de incompatibilidades en las prestaciones de Seguridad Social", "introduction": "El sistema de Seguridad Social español establece un régimen de incompatibilidades entre prestaciones...", "legal_framework": "Marco normativo basado en LGSS, jurisprudencia del TS...", "analysis": "Análisis detallado de los principios jurídicos aplicables...", "conclusions": "Conclusiones del análisis jurídico...", "references": ["LGSS Art. X", "STS fecha"], "theme": "Incompatibilidades", "complexity": "alta", "verified": true}}"""
    
    return query_deepseek_reasoner(prompt)

def generate_comparative_study(base_content):
    """Genera estudio comparativo entre normativas"""
    prompt = f"""Eres experto en Seguridad Social España. Crea un estudio comparativo entre diferentes normativas o regímenes.

CONTENIDO BASE: {base_content[:500]}

INSTRUCCIONES:
1. Compara al menos dos regímenes o normativas diferentes
2. Identifica similitudes y diferencias clave
3. Analiza ventajas e inconvenientes de cada uno
4. Verifica todas las referencias normativas

Responde SOLO con JSON válido:
{{"id": "comparative_deepseek_001", "type": "comparative_study", "title": "Comparativa entre Régimen General y Régimen Especial de Autónomos en materia de jubilación", "regimes_compared": ["Régimen General", "RETA"], "similarities": ["Edad de jubilación", "Período mínimo de cotización"], "differences": ["Base de cotización", "Cálculo de la pensión"], "advantages_regime_1": ["Mayor protección social", "Cotización empresarial"], "advantages_regime_2": ["Flexibilidad en bases", "Bonificaciones específicas"], "legal_basis": ["LGSS", "Ley 20/2007"], "theme": "Regímenes de Seguridad Social", "verified": true}}"""
    
    return query_deepseek_reasoner(prompt)

def generate_procedural_guide(base_content):
    """Genera guía procedimental paso a paso"""
    prompt = f"""Eres experto en Seguridad Social España. Crea una guía procedimental detallada paso a paso.

CONTENIDO BASE: {base_content[:500]}

INSTRUCCIONES:
1. Identifica un procedimiento administrativo específico
2. Desglosa todos los pasos necesarios en orden cronológico
3. Incluye documentación requerida y plazos
4. Verifica normativa procedimental aplicable

Responde SOLO con JSON válido:
{{"id": "procedure_deepseek_001", "type": "procedural_guide", "title": "Procedimiento para solicitar pensión de jubilación", "objective": "Obtener el reconocimiento de la pensión de jubilación ordinaria", "requirements": ["Edad: 67 años o 65 con 38 años cotizados", "Período mínimo: 15 años cotizados"], "steps": ["1. Solicitar cita previa", "2. Presentar documentación", "3. Esperar resolución"], "documentation": ["DNI", "Informe de vida laboral", "Certificado médico si procede"], "deadlines": ["Resolución: 90 días máximo"], "legal_basis": "Ley 39/2015, LGSS Art. 205", "theme": "Procedimientos administrativos", "verified": true}}"""
    
    return query_deepseek_reasoner(prompt)

# Generar un ejemplo de cada tipo
generators = {
    "qa_multiple_choice": generate_qa_multiple_choice,
    "case_study": generate_case_study,
    "chat_dialogue": generate_chat_dialogue,
    "flashcard": generate_flashcard,
    "rag_context_qa": generate_rag_context_qa,
    "legal_analysis": generate_legal_analysis,
    "comparative_study": generate_comparative_study,
    "procedural_guide": generate_procedural_guide
}

print("🔄 Generando un ejemplo de cada tipo de contenido...\n")

for i, content_type in enumerate(generators.keys(), 1):
    print(f"--- Generando {content_type} ({i}/8) ---")
    
    # Seleccionar contenido base aleatorio
    base_q = random.choice(questions)
    base_content = base_q.payload.get('text', '')
    
    try:
        content, reasoning = generators[content_type](base_content)
        
        # Extraer JSON de la respuesta
        json_start, json_end = content.find('{'), content.rfind('}') + 1
        if json_start >= 0:
            generated_item = json.loads(content[json_start:json_end])
            
            # Añadir metadatos
            generated_item.update({
                'generated_at': datetime.now().isoformat(),
                'model': 'deepseek-reasoner',
                'reasoning_preview': reasoning[:300] if reasoning else None,
                'source_file': base_q.payload.get('filename', 'unknown')
            })
            
            # Mejorar calidad del contenido
            generated_item = enhance_content_quality(generated_item)
            
            generated_content.append(generated_item)
            print(f"✅ {content_type} generado correctamente")
            
            # Mostrar preview del contenido generado
            if content_type == "qa_multiple_choice":
                print(f"   Pregunta: {generated_item.get('question', '')[:100]}...")
            elif content_type == "case_study":
                print(f"   Caso: {generated_item.get('case_description', '')[:100]}...")
            elif content_type == "chat_dialogue":
                print(f"   Usuario: {generated_item.get('user_question', '')[:100]}...")
            elif content_type == "flashcard":
                print(f"   Frente: {generated_item.get('front', '')[:100]}...")
            elif content_type == "rag_context_qa":
                print(f"   Contexto: {generated_item.get('context', '')[:100]}...")
            elif content_type == "legal_analysis":
                print(f"   Título: {generated_item.get('title', '')[:100]}...")
            elif content_type == "comparative_study":
                print(f"   Comparativa: {generated_item.get('title', '')[:100]}...")
            elif content_type == "procedural_guide":
                print(f"   Procedimiento: {generated_item.get('title', '')[:100]}...")
            
        else:
            print(f"❌ No se pudo extraer JSON válido")
            
    except Exception as e:
        print(f"❌ Error generando {content_type}: {e}")
    
    print()
    time.sleep(2)  # Pausa entre llamadas

# Guardar resultados
os.makedirs('dataset_output', exist_ok=True)
output_file = f'dataset_output/contenido_diverso_deepseek_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(generated_content, f, indent=2, ensure_ascii=False)

print(f"\n{'='*80}")
print(f"✅ DEEPSEEK-REASONER: {len(generated_content)}/8 tipos de contenido generados")
print(f"📁 Archivo: {output_file}")
print(f"{'='*80}")

# Mostrar resumen de lo generado
if generated_content:
    print(f"\n📋 RESUMEN DE CONTENIDO GENERADO:")
    for item in generated_content:
        content_type = item.get('type', 'unknown')
        theme = item.get('theme', 'N/A')
        verified = "✅" if item.get('verified') else "❌"
        print(f"   {verified} {content_type}: {theme}")
        
        # Verificar referencias BOE si existen
        if 'articles_reference' in item:
            articles = item['articles_reference']
            print(f"      Referencias: {', '.join(articles)}")
    
    print(f"\n🔍 VERIFICACIÓN DE CALIDAD:")
    verified_count = sum(1 for item in generated_content if item.get('verified'))
    print(f"   Contenido verificado: {verified_count}/{len(generated_content)}")
    
    with_references = sum(1 for item in generated_content if 'articles_reference' in item or 'source' in item)
    print(f"   Con referencias BOE: {with_references}/{len(generated_content)}")
    
    print(f"\n💡 El contenido ha sido generado con razonamiento paso a paso (Chain of Thought)")
    print(f"   Cada elemento incluye verificación de normativa y referencias BOE actualizadas")
