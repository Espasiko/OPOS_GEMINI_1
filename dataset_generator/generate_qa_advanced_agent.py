import os
import time
import json
import logging
import requests
import argparse
from pathlib import Path
from datetime import datetime

# --- CONFIGURACIÓN ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mistral:latest"

OUTPUT_DIR = Path("dataset_generator/premium_content/mistral_night_mode")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- PROMPTS ---
SYSTEM_PROMPT_ARCHITECT = "Eres un Estratega de Oposiciones. Diseña un Plan de Caso Práctico Dificultad Extrema."
SYSTEM_PROMPT_WRITER = "Eres Redactor Oficial. Convierte el plan en JSON con 18 preguntas (15+3)."

# --- AGENTE CON PAUSAS Y RETRIES ---

def call_ollama_safe(messages, json_mode=False, retries=3):
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
        "options": {"num_predict": 4096, "num_ctx": 8192}
    }
    if json_mode: payload["format"] = "json"

    for i in range(retries):
        try:
            logger.info(f"🔄 Intento {i+1}/{retries}...")
            # Timeout ampliado a 1200s (20 mins)
            response = requests.post(OLLAMA_URL, json=payload, timeout=1200) 
            response.raise_for_status()
            return response.json()["message"]["content"]
        except Exception as e:
            logger.warning(f"⚠️ Error Ollama: {e}. Reintentando en 10s...")
            time.sleep(10)
    
    logger.error("❌ Fallaron todos los intentos.")
    return None

def generate_case_workflow(topic):
    logger.info(f"🚀 Iniciando Agente para: {topic}")
    
    # 1. THINKING (Arquitecto)
    logger.info("🧠 Fase 1: Thinking...")
    plan = call_ollama_safe([
        {"role": "system", "content": SYSTEM_PROMPT_ARCHITECT},
        {"role": "user", "content": f"Analiza: {topic}. Diseña trampas y escenario."}
    ])
    if not plan: return
    
    # PAUSA ESTRATÉGICA (Para dejar descansar la VRAM/CPU)
    logger.info("☕ Pausa de enfriamiento (5s)...")
    time.sleep(5)

    # 2. WRITING (Redactor)
    logger.info("✍️ Fase 2: Writing...")
    json_content = call_ollama_safe([
        {"role": "system", "content": SYSTEM_PROMPT_WRITER},
        {"role": "user", "content": f"Plan: {plan}\n\nGenera JSON final."}
    ], json_mode=True)
    
    if json_content:
        # Guardar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = topic.replace(" ", "_").replace(":", "").replace("/", "_")[:30]
        file_path = OUTPUT_DIR / f"mistral_night_{safe_topic}_{timestamp}.json"
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(json_content) 
        logger.info(f"✅ Guardado: {file_path}")
    else:
        logger.error("❌ Falló Fase 2")

if __name__ == "__main__":
    # LISTA DE TEMAS (NIGHT MODE) - 50 Temas Diversos
    NIGHT_TOPICS = [
        # SEGURIDAD SOCIAL
        "Jubilación Activa: Requisitos y Cuantía",
        "Incapacidad Permanente Total vs Absoluta",
        "Gran Invalidez: Complemento y revisión",
        "IMV: Requisitos de acceso y unidad de convivencia",
        "Desempleo: Nivel Contributivo vs Asistencial",
        "Subsidio para mayores de 52 años: Rentas y Cotización",
        "Maternidad y Paternidad: Prestaciones y permisos",
        "Riesgo durante el embarazo y lactancia natural",
        "Jubilación Anticipada Voluntaria vs Involuntaria",
        "Accidente de Trabajo: Concepto y Presunciones",
        "Enfermedad Profesional: Listado y Calificación",
        "Cotización: Conceptos computables y excluidos",
        "Recaudación: Periodo voluntario y vía ejecutiva",
        "Infracciones y Sanciones en el Orden Social (LISOS)",
        "Prestaciones Familiares: Asignación por hijo a cargo",
        
        # DERECHO ADMINISTRATIVO
        "El Acto Administrativo: Elementos y clases",
        "Nulidad y Anulabilidad de los actos administrativos",
        "El Procedimiento Administrativo Común: Fases",
        "El Silencio Administrativo: Positivo y Negativo",
        "Recursos Administrativos: Alzada y Reposición",
        "Recurso Contencioso-Administrativo: Plazos",
        "Responsabilidad Patrimonial de la Administración",
        "Potestad Sancionadora: Principios y Procedimiento",
        "Contratos del Sector Público: Tipos y Procedimientos",
        "Expropiación Forzosa: Procedimiento General",
        
        # CONSTITUCIONAL Y ORGANIZACIÓN
        "La Corona: Funciones y Sucesión",
        "Las Cortes Generales: Congreso y Senado",
        "El Gobierno: Composición y Funciones",
        "El Poder Judicial: CGPJ y Tribunal Supremo",
        "El Tribunal Constitucional: Composición y Competencias",
        "Derechos Fundamentales y Libertades Públicas",
        "La Reforma de la Constitución: Procedimientos",
        "Organización Territorial: CCAA y Entidades Locales",
        "La Unión Europea: Instituciones y Derecho Comunitario",
        
        # FUNCIÓN PÚBLICA
        "TREBEP: Clases de personal y derechos",
        "Situaciones Administrativas de los funcionarios",
        "Régimen Disciplinario de los funcionarios",
        "Incompatibilidades del personal al servicio de las AAPP",
        "Acceso al empleo público: Principios rectores",
        
        # EXTRAS ESPECÍFICOS
        "Régimen Especial de Trabajadores Autónomos (RETA)",
        "Régimen Especial del Mar y Minería",
        "Convenios Especiales con la Seguridad Social",
        "Asistencia Sanitaria: Titulares y Beneficiarios",
        "Incapacidad Temporal: Pago directo y Pago delegado",
        "Jubilación Parcial y Contrato de Relevo",
        "Complemento para la reducción de la brecha de género",
        "Prestaciones por Muerte y Supervivencia: Viudedad y Orfandad",
        "El SOVI: Prestaciones y condiciones",
        "La Gestión Financiera de la Seguridad Social"
    ]

    logger.info(f"🌙 MODO NOCTURNO ACTIVADO. Total Temas: {len(NIGHT_TOPICS)}")
    
    for i, topic in enumerate(NIGHT_TOPICS):
        logger.info(f"✨ Procesando Tema {i+1}/{len(NIGHT_TOPICS)}: {topic}")
        generate_case_workflow(topic)
        
        # Pausa larga entre casos para proteger hardware local
        logger.info("💤 Pausa larga de recuperación (60s)...")
        time.sleep(60)
        
    logger.info("🌞 ¡Buenos días! Tarea nocturna finalizada.")
