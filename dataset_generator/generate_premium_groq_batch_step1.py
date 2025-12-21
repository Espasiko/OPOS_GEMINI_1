import json
import os
from pathlib import Path

# Lista de 100 Temas Premium (Extracto representativo para el ejemplo)
TOPICS = [
    "Jubilación Activa: Cómputo de cotizaciones recíprocas RETA-RG",
    "Incapacidad Permanente: Revisión por mejoría antes de los 2 años",
    "IMV: Unidad de convivencia con familiares de 2º y 3º grado",
    "Desempleo: Pago único y compatibilidad con RETA",
    "Viudedad: Parejas de hecho sin inscripción registral (Jurisprudencia reciente)",
    "Accidente de Trabajo: In itinere con desvíos personales",
    "Recargo de Prestaciones: Responsabilidad solidaria en contratas",
    "Jubilación Anticipada: Coeficientes reductores en trabajos penosos",
    "Subsidio mayores 52 años: Cómputo de rentas de la unidad familiar",
    "Incapacidad Temporal: Pago directo vs Pago delegado en extinción de contrato",
    # ... (Se añadirían hasta 100 temas reales del temario)
]

# Relleno hasta 100 para la prueba de carga
while len(TOPICS) < 100:
    TOPICS.append(f"Tema Genérico de Derecho Administrativo {len(TOPICS)+1}")

OUTPUT_FILE = Path("dataset_generator/groq_batch_thinking_100.jsonl")

SYSTEM_PROMPT_ARCHITECT = """Eres un Miembro del Tribunal de Oposiciones de la Seguridad Social.
Diseña el esquema LEGAL de un caso práctico de Dificultad Extrema.
Identifica 3 trampas legales, normativa conflictiva y hechos clave.
NO escribas el examen. Solo el PLAN."""

def generate_thinking_batch():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for i, topic in enumerate(TOPICS):
            # Request ID para trackeo
            req_id = f"thinking_{i:03d}"
            
            prompt = f"Analiza el tema: '{topic}'. Diseña un caso práctico con 3 trampas mortales. Responde con el PLAN DE DISEÑO."
            
            req_structure = {
                "custom_id": req_id,
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT_ARCHITECT},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 4096
                }
            }
            f.write(json.dumps(req_structure) + "\n")
            
    print(f"✅ Generado archivo Batch 1 (Thinking): {OUTPUT_FILE} ({len(TOPICS)} items)")
    print("📋 Pasos siguientes:")
    print("1. Subir este archivo a Groq Batch API.")
    print("2. Esperar procesamiento (~24h).")
    print("3. Descargar resultados (los 'Pensamientos').")
    print("4. Usar esos resultados para generar el Batch 2 (Writing).")

if __name__ == "__main__":
    generate_thinking_batch()
