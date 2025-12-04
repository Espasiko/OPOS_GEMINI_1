#!/usr/bin/env python3
"""
Generador SIMPLE de 10 Q&A de MÁXIMA DIFICULTAD con Mistral API
Sin herramientas complejas - directo y efectivo
"""

import os
import json
import requests
from datetime import datetime
import hashlib

MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')

def call_mistral(prompt: str, temperature: float = 0.4) -> str:
    """Llama a Mistral API"""
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
                "temperature": temperature,
                "max_tokens": 3000
            },
            timeout=180
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            print(f"   ❌ Error API: {response.status_code}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def parse_json_safe(text: str) -> dict:
    """Parsea JSON de forma segura"""
    try:
        start = text.find('{')
        if start < 0:
            return None
        depth = 0
        end = start
        for i, c in enumerate(text[start:], start):
            if c == '{': depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        return json.loads(text[start:end])
    except:
        return None

# Temas de MÁXIMA dificultad con contexto legal específico
TEMAS_MAXDIF = [
    {
        "tema": "Cálculo base reguladora jubilación con lagunas",
        "contexto": "Art. 209 LGSS: base reguladora = cociente bases cotización 300 meses / 350. Lagunas: primeras 48 mensualidades = base mínima vigente, resto = 50% base mínima. Períodos asimilados al alta sin cotización.",
        "trampa": "Confundir tratamiento lagunas primeros 48 meses vs resto"
    },
    {
        "tema": "Jubilación anticipada voluntaria coeficientes",
        "contexto": "Art. 208 LGSS: coeficientes reductores trimestrales según años cotizados. Con 38.5 años: 1.625% trimestre. Excepción discapacidad ≥65%: sin coeficientes. Mutualistas antes 1967: régimen especial.",
        "trampa": "No aplicar excepción discapacidad o confundir coeficientes"
    },
    {
        "tema": "Compatibilidad jubilación activa",
        "contexto": "Art. 214 LGSS: jubilación activa = 50% pensión + trabajo. Requisitos: 100% base reguladora, 1 año desde jubilación. Autónomos con empleado: 100% pensión. Incompatible con jubilación parcial previa.",
        "trampa": "Confundir porcentajes o requisito del empleado en autónomos"
    },
    {
        "tema": "Incapacidad permanente revisión plazos",
        "contexto": "Art. 200 LGSS: revisión por mejoría/agravación. Plazo 2 años desde resolución firme. Excepción: error diagnóstico sin plazo. Revisión de oficio vs a instancia. Efectos económicos desde solicitud.",
        "trampa": "Confundir plazos o efectos económicos de la revisión"
    },
    {
        "tema": "Prestación desempleo suspensión vs extinción",
        "contexto": "Arts. 271-272 LGSS: Suspensión (trabajo <12 meses, sanción, IT) vs Extinción (trabajo ≥12 meses, rechazo oferta, fraude). Reanudación: 15 días desde cese. Subsidio: requisitos diferentes.",
        "trampa": "Confundir causas suspensión con extinción"
    },
    {
        "tema": "IMV cómputo rentas y patrimonio",
        "contexto": "RD 20/2020: Rentas computables año anterior. Patrimonio: excluye vivienda habitual hasta 300.000€. Rendimientos patrimonio: 100% si >50.000€. Unidad convivencia: todos los miembros.",
        "trampa": "No excluir vivienda habitual o computar mal patrimonio"
    },
    {
        "tema": "Cotización RETA tramos rendimientos 2024",
        "contexto": "RD-ley 13/2022: Sistema tramos rendimientos netos. Tramo 1 (<670€): base mín 735,29€. Tramo máximo (>6.000€): base mín 1.732,03€. Regularización anual. Tarifa plana: 80€ primeros 12 meses.",
        "trampa": "Confundir bases mínimas por tramo o regularización"
    },
    {
        "tema": "Pensión viudedad parejas de hecho",
        "contexto": "Art. 221 LGSS: Pareja hecho = 5 años convivencia + inscripción registro 2 años antes. Ingresos <1.5 SMI o <50% total. Excepción hijos comunes: sin requisito ingresos. Incompatible con otra viudedad.",
        "trampa": "No cumplir requisito registro o confundir plazos"
    },
    {
        "tema": "Recargo prestaciones falta medidas seguridad",
        "contexto": "Art. 164 LGSS: Recargo 30-50% según gravedad. Responsable: empresario. No asegurable. Compatible con indemnización civil. Prescripción 5 años. STS: culpa in vigilando.",
        "trampa": "Pensar que es asegurable o confundir porcentajes"
    },
    {
        "tema": "Integración lagunas contingencias profesionales",
        "contexto": "Art. 209.1.b LGSS: Contingencias profesionales = bases cotización AT/EP. Sin integración lagunas (a diferencia de comunes). Base reguladora: salario real día accidente × 365. Mejoras voluntarias.",
        "trampa": "Aplicar integración lagunas a contingencias profesionales"
    }
]

def generar_qa(tema_info: dict, num: int) -> dict:
    """Genera una Q&A de máxima dificultad"""
    
    prompt = f"""Eres EXPERTO en oposiciones de Seguridad Social España. Crea UNA pregunta de MÁXIMA DIFICULTAD.

TEMA: {tema_info['tema']}
CONTEXTO LEGAL: {tema_info['contexto']}
TRAMPA A USAR: {tema_info['trampa']}

REQUISITOS:
1. Pregunta tipo caso práctico con datos específicos (fechas, cantidades, edades)
2. Solo 10-15% de opositores acertaría
3. 4 opciones donde las incorrectas sean errores COMUNES
4. Explicación con artículos específicos
5. La trampa debe ser SUTIL

RESPONDE SOLO CON ESTE JSON (sin texto adicional):
{{
    "pregunta": "caso práctico detallado con datos concretos",
    "opciones": ["A) opción", "B) opción", "C) opción", "D) opción"],
    "respuesta_correcta": "A/B/C/D",
    "explicacion": "explicación detallada citando artículos",
    "tema": "{tema_info['tema']}",
    "dificultad": "muy_alta",
    "articulos": ["art. X LGSS"],
    "trampa_usada": "{tema_info['trampa']}",
    "porcentaje_acierto": 12
}}"""

    print(f"\n--- Pregunta {num}/10 ---")
    print(f"📚 {tema_info['tema'][:50]}...")
    print(f"🎭 Trampa: {tema_info['trampa'][:40]}...")
    
    response = call_mistral(prompt)
    if not response:
        return None
    
    qa = parse_json_safe(response)
    if qa and 'pregunta' in qa:
        qa['generated_at'] = datetime.now().isoformat()
        qa['model'] = 'mistral-large-latest'
        qa['hash'] = hashlib.md5(qa['pregunta'].encode()).hexdigest()[:12]
        print(f"✅ Generada (acierto estimado: {qa.get('porcentaje_acierto', 12)}%)")
        return qa
    else:
        print(f"❌ Error parsing JSON")
        return None

def main():
    print("\n🎯 GENERADOR 10 Q&A MÁXIMA DIFICULTAD - MISTRAL")
    print("=" * 50)
    
    if not MISTRAL_API_KEY:
        print("❌ MISTRAL_API_KEY no configurada")
        return
    
    generated = []
    for i, tema in enumerate(TEMAS_MAXDIF, 1):
        qa = generar_qa(tema, i)
        if qa:
            generated.append(qa)
    
    # Exportar
    if generated:
        os.makedirs('dataset_output', exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        outfile = f'dataset_output/qa_mistral_10_maxdif_{ts}.json'
        
        with open(outfile, 'w', encoding='utf-8') as f:
            json.dump(generated, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*50}")
        print(f"✅ COMPLETADO: {len(generated)}/10 Q&A")
        print(f"📁 Archivo: {outfile}")
        
        # Muestra
        if generated:
            qa = generated[0]
            print(f"\n📋 MUESTRA:")
            print(f"Tema: {qa.get('tema', 'N/A')}")
            print(f"Pregunta: {qa.get('pregunta', '')[:150]}...")
            print(f"Trampa: {qa.get('trampa_usada', 'N/A')}")
            print(f"Artículos: {qa.get('articulos', [])}")

if __name__ == "__main__":
    main()
