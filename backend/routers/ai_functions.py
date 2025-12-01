"""
AI Functions Router - Sprint 8
Endpoints para todas las funciones de IA usando multi-proveedor
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import logging
import random
import tempfile
import os
from fastapi.responses import FileResponse
import genanki

# Import LLM providers
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from agents.llm_providers import get_provider

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["ai-functions"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class PracticalCaseRequest(BaseModel):
    topic: str
    difficulty: str = "medium"
    provider: str = "groq-70b"

class MindMapRequest(BaseModel):
    topic: str
    provider: str = "groq-70b"

class MockExamRequest(BaseModel):
    topics: List[str]
    num_questions: int = 10
    provider: str = "groq-70b"

class FlashcardsRequest(BaseModel):
    topic: str
    num_cards: int = 10
    provider: str = "groq-8b"

class SchemaRequest(BaseModel):
    topic: str
    provider: str = "groq-70b"

class SummaryRequest(BaseModel):
    text: str
    provider: str = "groq-8b"

class CompareRequest(BaseModel):
    text1: str
    text2: str
    provider: str = "groq-70b"

class SearchRequest(BaseModel):
    query: str
    provider: str = "gemini-pro"

class StudyPlanRequest(BaseModel):
    exam_date: str
    topics: List[str]
    hours_per_day: int
    provider: str = "groq-70b"


# ============================================================================
# HELPER FUNCTION
# ============================================================================

async def call_llm(provider_id: str, system_prompt: str, user_prompt: str, max_tokens: int = 3000) -> str:
    """Helper para llamar a cualquier LLM"""
    try:
        provider = get_provider(provider_id)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = ""
        async for chunk in provider.generate_stream(messages, temperature=0.7, max_tokens=max_tokens):
            response += chunk
        
        return response
    except Exception as e:
        logger.error(f"Error calling LLM {provider_id}: {e}")
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/practical-case")
async def generate_practical_case(request: PracticalCaseRequest):
    """Genera un caso práctico"""
    
    system_prompt = """Eres un experto en crear casos prácticos para oposiciones de Seguridad Social.
Genera casos realistas con escenarios detallados y preguntas tipo test.

FORMATO JSON REQUERIDO:
{
  "scenario": "Descripción detallada del caso (200-300 palabras)",
  "questions": [
    {
      "id": "q1",
      "question": "Pregunta sobre el caso",
      "options": [
        {"id": "a", "text": "Opción A"},
        {"id": "b", "text": "Opción B"},
        {"id": "c", "text": "Opción C"},
        {"id": "d", "text": "Opción D"}
      ],
      "correct_option_id": "a",
      "explanation": "Explicación detallada de por qué es correcta"
    }
  ]
}"""
    
    user_prompt = f"""Crea un caso práctico sobre: {request.topic}
Dificultad: {request.difficulty}
Incluye 3-4 preguntas tipo test.
Responde SOLO con el JSON, sin texto adicional."""
    
    response_text = await call_llm(request.provider, system_prompt, user_prompt)
    
    # Parse JSON
    try:
        # Limpiar respuesta (quitar markdown si existe)
        clean_text = response_text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.startswith("```"):
            clean_text = clean_text[3:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        clean_text = clean_text.strip()
        
        case_data = json.loads(clean_text)
        return case_data
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}\nResponse: {response_text[:500]}")
        raise HTTPException(status_code=500, detail="Error parsing LLM response")


@router.post("/mind-map")
async def generate_mind_map(request: MindMapRequest):
    """Genera un mapa mental"""
    
    system_prompt = """Eres un experto en crear mapas mentales para estudio.
Crea mapas mentales jerárquicos en formato JSON.

FORMATO JSON REQUERIDO:
{
  "id": "root",
  "label": "Tema Principal",
  "children": [
    {
      "id": "1",
      "label": "Subtema 1",
      "children": [
        {"id": "1.1", "label": "Detalle 1.1", "children": []},
        {"id": "1.2", "label": "Detalle 1.2", "children": []}
      ]
    }
  ]
}"""
    
    user_prompt = f"""Crea un mapa mental sobre: {request.topic}
Incluye 3-4 niveles de profundidad.
Responde SOLO con el JSON, sin texto adicional."""
    
    response_text = await call_llm(request.provider, system_prompt, user_prompt)
    
    try:
        clean_text = response_text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.startswith("```"):
            clean_text = clean_text[3:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        clean_text = clean_text.strip()
        
        mind_map = json.loads(clean_text)
        return mind_map
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        raise HTTPException(status_code=500, detail="Error parsing LLM response")


@router.post("/flashcards")
async def generate_flashcards(request: FlashcardsRequest):
    """Genera flashcards"""
    
    system_prompt = """Eres un experto en crear flashcards para estudio.
Crea flashcards con preguntas concisas y respuestas claras.

FORMATO JSON REQUERIDO:
{
  "cards": [
    {
      "id": "1",
      "front": "Pregunta o concepto",
      "back": "Respuesta o explicación"
    }
  ]
}"""
    
    user_prompt = f"""Crea {request.num_cards} flashcards sobre: {request.topic}
Responde SOLO con el JSON, sin texto adicional."""
    
    response_text = await call_llm(request.provider, system_prompt, user_prompt)
    
    try:
        clean_text = response_text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.startswith("```"):
            clean_text = clean_text[3:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        clean_text = clean_text.strip()
        
        flashcards = json.loads(clean_text)
        return flashcards
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        raise HTTPException(status_code=500, detail="Error parsing LLM response")


@router.post("/schema")
async def generate_schema(request: SchemaRequest):
    """Genera un esquema"""
    
    system_prompt = """Eres un experto en crear esquemas de estudio.
Crea esquemas estructurados y claros en formato texto."""
    
    user_prompt = f"""Crea un esquema detallado sobre: {request.topic}
Usa formato jerárquico con números y letras.
Incluye los puntos más importantes."""
    
    response_text = await call_llm(request.provider, system_prompt, user_prompt)
    
    return {"schema": response_text}


@router.post("/summary")
async def generate_summary(request: SummaryRequest):
    """Genera un resumen"""
    
    system_prompt = """Eres un experto en resumir textos legales y académicos.
Crea resúmenes concisos que capturen los puntos clave."""
    
    user_prompt = f"""Resume el siguiente texto:

{request.text[:5000]}

Crea un resumen de 200-300 palabras con los puntos más importantes."""
    
    response_text = await call_llm(request.provider, system_prompt, user_prompt)
    
    return {"summary": response_text}


@router.post("/compare")
async def compare_texts(request: CompareRequest):
    """Compara dos textos"""
    
    system_prompt = """Eres un experto en comparar textos legales.
Identifica diferencias, similitudes y cambios importantes."""
    
    user_prompt = f"""Compara estos dos textos:

TEXTO 1:
{request.text1[:2000]}

TEXTO 2:
{request.text2[:2000]}

Identifica:
1. Diferencias principales
2. Similitudes
3. Cambios importantes"""
    
    response_text = await call_llm(request.provider, system_prompt, user_prompt)
    
    return {"comparison": response_text}


@router.post("/study-plan")
async def generate_study_plan(request: StudyPlanRequest):
    """Genera un plan de estudio"""
    
    system_prompt = """Eres un experto en crear planes de estudio para oposiciones.
Crea planes realistas y estructurados."""
    
    topics_str = ", ".join(request.topics)
    user_prompt = f"""Crea un plan de estudio para:
- Fecha examen: {request.exam_date}
- Temas: {topics_str}
- Horas disponibles por día: {request.hours_per_day}

Incluye:
1. Distribución semanal
2. Tiempo por tema
3. Recomendaciones"""
    
    response_text = await call_llm(request.provider, system_prompt, user_prompt)
    
    return {"plan": response_text}


@router.post("/mock-exam")
async def generate_mock_exam(request: MockExamRequest):
    """Genera un simulacro de examen (en lotes si es necesario)"""
    
    # Si son más de 15 preguntas, generar en lotes
    if request.num_questions > 15:
        return await generate_mock_exam_batched(request)
    
    system_prompt = """Eres un experto examinador de oposiciones de Seguridad Social en España.
Genera ÚNICAMENTE JSON válido. NO incluyas explicaciones, markdown, ni texto adicional.

FORMATO EXACTO (copia esta estructura):
{
  "title": "Simulacro de Examen - Seguridad Social",
  "questions": [
    {
      "id": "q1",
      "question": "Texto de la pregunta",
      "options": [
        {"id": "a", "text": "Opción A"},
        {"id": "b", "text": "Opción B"},
        {"id": "c", "text": "Opción C"},
        {"id": "d", "text": "Opción D"}
      ],
      "correct_option_id": "a",
      "explanation": "Explicación con base legal"
    }
  ]
}"""
    
    topics_str = ", ".join(request.topics)
    user_prompt = f"""Genera {request.num_questions} preguntas sobre: {topics_str}

IMPORTANTE: Responde SOLO con JSON. Sin ```json, sin explicaciones, sin texto extra.
Empieza directamente con {{ y termina con }}"""
    
    try:
        # Usar más tokens para exámenes grandes
        max_tokens = 4000 if request.num_questions > 10 else 3000
        response_text = await call_llm(request.provider, system_prompt, user_prompt, max_tokens=max_tokens)
        logger.info(f"Raw LLM response (first 500 chars): {response_text[:500]}")
        
        # Limpiar respuesta más agresivamente
        clean_text = response_text.strip()
        
        # Remover bloques de código markdown
        if "```json" in clean_text:
            clean_text = clean_text.split("```json")[1].split("```")[0]
        elif "```" in clean_text:
            parts = clean_text.split("```")
            if len(parts) >= 3:
                clean_text = parts[1]
            else:
                clean_text = parts[-1]
        
        clean_text = clean_text.strip()
        
        # Intentar encontrar el JSON si hay texto antes/después
        if not clean_text.startswith("{"):
            # Buscar el primer {
            start_idx = clean_text.find("{")
            if start_idx != -1:
                clean_text = clean_text[start_idx:]
            else:
                logger.error(f"No JSON object found in response: {clean_text[:500]}")
                raise ValueError("No JSON object found in LLM response")
        
        if not clean_text.endswith("}"):
            # Buscar el último }
            end_idx = clean_text.rfind("}")
            if end_idx != -1:
                clean_text = clean_text[:end_idx+1]
            else:
                logger.error(f"No closing brace found in response: {clean_text[:500]}")
                raise ValueError("Incomplete JSON object in LLM response")
        
        logger.info(f"Cleaned text (first 500 chars): {clean_text[:500]}")
        logger.info(f"Cleaned text (last 200 chars): {clean_text[-200:]}")
        
        exam_data = json.loads(clean_text)
        
        # Validar estructura
        if "questions" not in exam_data:
            raise ValueError("Missing 'questions' field")
        if not isinstance(exam_data["questions"], list):
            raise ValueError("'questions' must be a list")
        if len(exam_data["questions"]) == 0:
            raise ValueError("No questions generated")
        
        # Validar cada pregunta
        for i, q in enumerate(exam_data["questions"]):
            if "id" not in q or "question" not in q or "options" not in q or "correct_option_id" not in q:
                raise ValueError(f"Question {i} is missing required fields")
        
        logger.info(f"Successfully generated {len(exam_data['questions'])} questions")
        return exam_data
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}\nCleaned text: {clean_text[:1000]}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error parsing LLM response. The model did not return valid JSON. Error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error in mock-exam: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating exam: {str(e)}")


async def generate_mock_exam_batched(request: MockExamRequest):
    """Genera examen en lotes optimizados (10-15 preguntas por lote)"""
    # Determinar tamaño de lote según el proveedor
    if "gemini" in request.provider.lower():
        batch_size = 15  # Gemini puede manejar más
    else:
        batch_size = 10  # Groq/otros más conservador
    
    num_batches = (request.num_questions + batch_size - 1) // batch_size
    
    all_questions = []
    topics_str = ", ".join(request.topics)
    
    logger.info(f"Generating {request.num_questions} questions in {num_batches} batches of ~{batch_size}")
    
    for batch_num in range(num_batches):
        questions_in_batch = min(batch_size, request.num_questions - len(all_questions))
        start_id = len(all_questions) + 1
        
        logger.info(f"Batch {batch_num + 1}/{num_batches}: Generating {questions_in_batch} questions (IDs {start_id}-{start_id + questions_in_batch - 1})")
        
        # Crear request para este lote
        batch_request = MockExamRequest(
            topics=request.topics,
            num_questions=questions_in_batch,
            provider=request.provider
        )
        
        try:
            # Generar lote
            batch_result = await generate_mock_exam(batch_request)
            
            # Renumerar IDs para que sean únicos
            for i, q in enumerate(batch_result["questions"]):
                q["id"] = f"q{start_id + i}"
            
            all_questions.extend(batch_result["questions"])
            logger.info(f"Batch {batch_num + 1}/{num_batches} completed successfully")
            
        except Exception as e:
            logger.error(f"Error in batch {batch_num + 1}: {e}")
            # Si falla un lote, continuar con los demás
            continue
    
    if not all_questions:
        raise HTTPException(status_code=500, detail="Failed to generate any questions")
    
    logger.info(f"Successfully generated {len(all_questions)}/{request.num_questions} questions")
    
    return {
        "title": f"Simulacro de Examen C1 - Seguridad Social ({len(all_questions)} preguntas)",
        "questions": all_questions
    }


@router.post("/flashcards/export")
async def export_anki(request: FlashcardsRequest):
    """Genera y descarga un mazo de Anki (.apkg)"""
    
    # 1. Generar flashcards si no se pasan (reutilizamos lógica existente)
    # En un caso real, el frontend enviaría las cards ya generadas.
    # Aquí asumimos que el usuario quiere generar Y exportar.
    
    flashcards_data = await generate_flashcards(request)
    cards = flashcards_data.get("cards", [])
    
    if not cards:
        raise HTTPException(status_code=400, detail="No flashcards generated")

    # 2. Crear Mazo Anki
    # ID aleatorio para el mazo
    deck_id = random.randrange(1 << 30, 1 << 31)
    deck = genanki.Deck(deck_id, f"OpositaIA: {request.topic}")

    # Modelo básico
    model = genanki.Model(
        1607392319,
        'OpositaIA Flashcard',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ])

    # 3. Añadir notas
    for card in cards:
        note = genanki.Note(
            model=model,
            fields=[card.get("front", ""), card.get("back", "")]
        )
        deck.add_note(note)

    # 4. Generar archivo temporal
    try:
        # Usar directorio temporal del sistema
        temp_dir = tempfile.gettempdir()
        output_file = os.path.join(temp_dir, f"opositaia_deck_{deck_id}.apkg")
        
        package = genanki.Package(deck)
        package.write_to_file(output_file)
        
        return FileResponse(
            path=output_file,
            filename=f"opositaia_{request.topic.replace(' ', '_')}.apkg",
            media_type='application/octet-stream'
        )
    except Exception as e:
        logger.error(f"Error generating Anki package: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating Anki package: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check del servicio de funciones IA"""
    return {
        "status": "healthy",
        "available_functions": [
            "practical-case",
            "mind-map",
            "flashcards",
            "schema",
            "summary",
            "compare",
            "study-plan",
            "mock-exam",
            "flashcards/export"
        ]
    }
