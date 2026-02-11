#!/usr/bin/env python3
"""
Verificar emparejamiento examen enero_25 con sus respuestas
"""
import re

print("=" * 80)
print("VERIFICACIÓN EMPAREJAMIENTO - EXAMEN ENERO 25")
print("=" * 80)

# Leer archivo de examen
print("\n1. Leyendo examen enero_25...")
with open('extracted_texts/examenes_oficiales_academias/11._examen_c1_pi_extraord_enero_25_ocr.txt', encoding='utf-8') as f:
    exam_content = f.read()

# Leer archivo de respuestas
print("2. Leyendo respuestas enero_25...")
with open('extracted_texts/examenes_oficiales_academias/11._respuestas_examen_c1_pi_extraord_enero_25.txt', encoding='utf-8') as f:
    answers_content = f.read()

# Extraer respuestas oficiales
pattern = r'(\d+)\s+([A-D])'
matches = re.findall(pattern, answers_content)
official_answers = {int(n): a.upper() for n, a in matches if int(n) <= 50}  # Solo preguntas 1-50

print(f"   ✅ Extraídas {len(official_answers)} respuestas oficiales\n")

# Extraer preguntas del examen (primeras 10 para verificar)
questions = []
for i in range(1, 11):  # Primeras 10 preguntas
    pattern_q = rf'{i}\.\s+(.+?)(?=\n[abcd]\))'
    match = re.search(pattern_q, exam_content, re.DOTALL)
    if match:
        q_text = match.group(1).strip()[:100]  # Primeros 100 chars
        questions.append({
            'num': i,
            'text': q_text,
            'answer': official_answers.get(i, 'N/A')
        })

# Mostrar verificación
print("3. VERIFICACIÓN DE EMPAREJAMIENTO (primeras 10):\n")
print(f"{'Q#':<4} {'Respuesta':<10} {'Texto':<70}")
print("=" * 85)

for q in questions:
    print(f"{q['num']:<4} {q['answer']:<10} {q['text'][:67]}...")

# Verificar que hay opciones a, b, c, d para cada pregunta
print(f"\n4. VERIFICANDO ESTRUCTURA DE OPCIONES:\n")
for i in range(1, 6):  # Primeras 5
    options_found = []
    for opt in ['a', 'b', 'c', 'd']:
        if re.search(rf'{i}\..+?{re.escape(opt)}\\)', exam_content, re.DOTALL):
            options_found.append(opt)
    
    status = "✅" if len(options_found) == 4 else "❌"
    print(f"{status} Pregunta {i}: Opciones encontradas: {', '.join(options_found)}")

# Resumen final
print(f"\n{'='*80}")
print("RESUMEN:")
print(f"{'='*80}")
print(f"Total preguntas en examen: ~50")
print(f"Total respuestas oficiales: {len(official_answers)}")
print(f"Estado: {'✅ CORRECTAMENTE EMPAREJADO' if len(official_answers) >= 50 else '❌ POSIBLE PROBLEMA'}")
print(f"\nPrimera pregunta:")
print(f"  Número: 1")
print(f"  Respuesta oficial: {official_answers.get(1)}")
print(f"  Texto: {questions[0]['text'][:80] if questions else 'N/A'}...")
print("=" * 80)

# Guardar resultado
import json
with open('/tmp/enero_25_pairing_verification.json', 'w', encoding='utf-8') as f:
    json.dump({
        'total_questions': 50,
        'extracted_answers': len(official_answers),
        'sample_questions': questions,
        'answers': official_answers,
        'status': 'PAIRED' if len(official_answers) >= 50 else 'ISSUE'
    }, f, indent=2, ensure_ascii=False)

print(f"\n📄 Guardado: /tmp/enero_25_pairing_verification.json")
