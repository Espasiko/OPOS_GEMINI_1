
import json
import os

TOPICS = [
    "La protección social de los trabajadores autónomos (RETA)",
    "Régimen Especial de la Minería del Carbón y del Mar",
    "Pensión de Jubilación: Requisitos, Cuantía y Modalidades",
    "Incapacidad Temporal: Concepto, Duración y Subsidio",
    "El presupuesto de la Seguridad Social: Elaboración y Ejecución",
    "Ingreso Mínimo Vital: Requisitos y Beneficiarios",
    "La Corona: Sucesión, Regencia y Funciones del Rey",
    "Las Cortes Generales: Composición y atribuciones",
    "Políticas de Igualdad y Violencia de Género",
    "Derechos y Deberes Fundamentales",
    "El Gobierno y la Administración",
    "Organización Territorial del Estado",
    "El Acto Administrativo: Concepto y Clases",
    "El Procedimiento Administrativo Común",
    "Contratos del Sector Público: Clasificación",
    "El Personal al Servicio de las Administraciones Públicas",
    "Gestión Económico-Financiera de la SS",
    "Pensiones de Muerte y Supervivencia",
    "El Seguro Obligatorio de Vejez e Invalidez (SOVI)",
    "Asistencia Sanitaria: Competencias y Gestión",
    "Incapacidad Permanente: Grados",
    "Lesiones Permanentes No Invalidantes",
    "Convenios Internacionales de SS",
    "Protección por Desempleo",
    "Servicios Sociales: El IMSERSO",
    "Infracciones y Sanciones en el Orden Social"
]

def generate_batch_requests(total_count=500):
    requests = []
    items_per_topic = (total_count // len(TOPICS)) + 1
    
    system_prompt = """Eres un experto en oposiciones de Seguridad Social de España.
Genera 1 pregunta de NIVEL EXPERTO con 4 opciones (A, B, C, D), respuesta correcta, explicación legal y referencias.
Responde ÚNICAMENTE en JSON:
{
  "pregunta": "...",
  "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."],
  "respuesta_correcta": "A/B/C/D",
  "explicacion": "...",
  "referencias": ["Art. X Ley Y"],
  "tipo": "TEST/CASO/RAZONAMIENTO"
}"""

    count = 0
    for topic in TOPICS:
        for _ in range(items_per_topic):
            if count >= total_count: break
            
            req = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Genera una pregunta única sobre: '{topic}'"}
                ],
                "temperature": 0.2,
                "response_format": {"type": "json_object"}
            }
            requests.append(req)
            count += 1
            
    return requests

if __name__ == "__main__":
    from groq_batch_service import GroqBatchService
    service = GroqBatchService()
    reqs = generate_batch_requests(500)
    service.prepare_batch_file(reqs, "dataset_generator/groq_batch_500.jsonl")
    print(f"✅ Preparadas {len(reqs)} peticiones.")
