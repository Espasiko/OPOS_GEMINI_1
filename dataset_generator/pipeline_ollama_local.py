#!/usr/bin/env python3
"""
Pipeline de generación de Q&A usando Mistral local en Ollama
Procesa materiales de academia de forma segura y ética
"""

import os
import json
import requests
from pathlib import Path
from typing import List, Dict, Optional
import PyPDF2
from datetime import datetime

class OllamaPipeline:
    def __init__(self, 
                 materials_path: str,
                 ollama_url: str = "http://localhost:11434",
                 model: str = "mistral"):
        self.materials_path = Path(materials_path)
        self.ollama_url = ollama_url
        self.model = model
        self.output_dir = Path("dataset_output")
        self.output_dir.mkdir(exist_ok=True)
        
    def check_ollama_connection(self) -> bool:
        """Verifica conexión con Ollama"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            return response.status_code == 200
        except:
            return False
    
    def generate_with_ollama(self, prompt: str, system: str = "") -> str:
        """Genera respuesta usando Ollama"""
        url = f"{self.ollama_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=120)
            if response.status_code == 200:
                return response.json()["response"]
            else:
                print(f"Error en Ollama: {response.status_code}")
                return ""
        except Exception as e:
            print(f"Error llamando a Ollama: {e}")
            return ""
    
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extrae texto de un PDF"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"Error extrayendo texto de {pdf_path}: {e}")
            return ""
    
    def create_qa_from_exam(self, exam_text: str, source: str) -> List[Dict]:
        """Crea Q&A desde un examen oficial"""
        
        system_prompt = """Eres un experto en oposiciones de Seguridad Social en España.
Tu tarea es extraer preguntas y respuestas de exámenes oficiales.

REGLAS ESTRICTAS:
1. SOLO extrae preguntas que estén COMPLETAS en el texto
2. SOLO incluye respuestas que estén EXPLÍCITAMENTE marcadas como correctas
3. NO inventes ni modifiques preguntas
4. NO añadas información que no esté en el texto
5. Mantén la redacción EXACTA de las preguntas originales
6. Si una pregunta está incompleta, OMÍTELA

Formato de salida JSON:
{
  "preguntas": [
    {
      "pregunta": "texto exacto de la pregunta",
      "opciones": ["a) ...", "b) ...", "c) ...", "d) ..."],
      "respuesta_correcta": "letra de la opción correcta",
      "explicacion": "explicación si está disponible",
      "tema": "tema al que pertenece",
      "fuente": "nombre del examen"
    }
  ]
}"""
        
        prompt = f"""Extrae TODAS las preguntas tipo test del siguiente examen oficial.
Recuerda: SOLO preguntas completas con respuestas marcadas.

EXAMEN:
{exam_text[:8000]}  # Limitamos para no saturar

Responde SOLO con el JSON, sin texto adicional."""

        response = self.generate_with_ollama(prompt, system_prompt)
        
        try:
            # Intentar parsear JSON
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            
            data = json.loads(response.strip())
            
            # Añadir metadata
            for q in data.get("preguntas", []):
                q["fuente_original"] = source
                q["fecha_extraccion"] = datetime.now().isoformat()
                q["metodo"] = "extraccion_ollama"
            
            return data.get("preguntas", [])
        except json.JSONDecodeError as e:
            print(f"Error parseando JSON: {e}")
            print(f"Respuesta: {response[:500]}")
            return []
    
    def generate_variations(self, original_qa: Dict) -> List[Dict]:
        """Genera variaciones de una pregunta original"""
        
        system_prompt = """Eres un experto en crear variaciones de preguntas de oposiciones.

REGLAS ESTRICTAS:
1. Mantén el MISMO concepto legal que la pregunta original
2. Cambia SOLO: fechas, cantidades, nombres de ejemplo, orden de opciones
3. La respuesta correcta debe seguir siendo válida legalmente
4. NO cambies artículos de ley ni conceptos jurídicos
5. Genera 3 variaciones diferentes

Formato JSON:
{
  "variaciones": [
    {
      "pregunta": "...",
      "opciones": ["a) ...", "b) ...", "c) ...", "d) ..."],
      "respuesta_correcta": "...",
      "cambios_realizados": "descripción de qué cambiaste"
    }
  ]
}"""
        
        prompt = f"""Genera 3 variaciones de esta pregunta de oposición:

PREGUNTA ORIGINAL:
{original_qa['pregunta']}

OPCIONES:
{chr(10).join(original_qa.get('opciones', []))}

RESPUESTA CORRECTA: {original_qa.get('respuesta_correcta', '')}

Genera variaciones manteniendo la validez legal."""

        response = self.generate_with_ollama(prompt, system_prompt)
        
        try:
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            
            data = json.loads(response.strip())
            
            # Añadir metadata
            for v in data.get("variaciones", []):
                v["pregunta_original_id"] = original_qa.get("id", "")
                v["fuente_base"] = original_qa.get("fuente_original", "")
                v["metodo"] = "variacion_ollama"
                v["fecha_generacion"] = datetime.now().isoformat()
            
            return data.get("variaciones", [])
        except:
            return []
    
    def generate_from_schema(self, schema_text: str, tema: str) -> List[Dict]:
        """Genera Q&A desde un esquema de prestación"""
        
        system_prompt = """Eres un experto en Seguridad Social española.
Creas preguntas tipo test basadas en esquemas de prestaciones.

REGLAS ESTRICTAS:
1. Basa las preguntas SOLO en información del esquema
2. Crea preguntas sobre: requisitos, cuantías, plazos, procedimientos
3. Las 4 opciones deben ser plausibles pero solo 1 correcta
4. Incluye la base legal (artículo LGSS) si está en el esquema
5. Genera 10 preguntas variadas

Formato JSON:
{
  "preguntas": [
    {
      "pregunta": "...",
      "opciones": ["a) ...", "b) ...", "c) ...", "d) ..."],
      "respuesta_correcta": "...",
      "base_legal": "Art. X LGSS",
      "tema": "nombre del tema"
    }
  ]
}"""
        
        prompt = f"""Genera 10 preguntas tipo test sobre este tema de Seguridad Social:

TEMA: {tema}

ESQUEMA:
{schema_text[:6000]}

Genera preguntas variadas y realistas."""

        response = self.generate_with_ollama(prompt, system_prompt)
        
        try:
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            
            data = json.loads(response.strip())
            
            for q in data.get("preguntas", []):
                q["fuente_esquema"] = tema
                q["metodo"] = "generacion_esquema_ollama"
                q["fecha_generacion"] = datetime.now().isoformat()
            
            return data.get("preguntas", [])
        except:
            return []
    
    def process_official_exams(self) -> List[Dict]:
        """Procesa exámenes oficiales"""
        print("📝 Procesando exámenes oficiales...")
        
        exam_dir = self.materials_path / "bajados_academia"
        all_qa = []
        
        if not exam_dir.exists():
            print(f"⚠️  Directorio no encontrado: {exam_dir}")
            return []
        
        # Procesar solo exámenes (no respuestas)
        exam_files = [f for f in exam_dir.glob("*.pdf") 
                     if "respuesta" not in f.name.lower()]
        
        for exam_file in exam_files[:3]:  # Limitar a 3 para prueba
            print(f"  Procesando: {exam_file.name}")
            text = self.extract_text_from_pdf(exam_file)
            if text:
                qa_list = self.create_qa_from_exam(text, exam_file.name)
                all_qa.extend(qa_list)
                print(f"    ✓ Extraídas {len(qa_list)} preguntas")
        
        return all_qa
    
    def process_schemas(self) -> List[Dict]:
        """Procesa esquemas de prestaciones"""
        print("📊 Procesando esquemas de prestaciones...")
        
        schema_dir = self.materials_path / "bajados_academia"
        all_qa = []
        
        if not schema_dir.exists():
            return []
        
        # Esquemas de prestaciones
        schemas = {
            "it.pdf": "Incapacidad Temporal",
            "ip_parcial.pdf": "Incapacidad Permanente Parcial",
            "jubilacion_ordinaria.pdf": "Jubilación Ordinaria",
        }
        
        for filename, tema in schemas.items():
            schema_file = schema_dir / filename
            if schema_file.exists():
                print(f"  Procesando: {tema}")
                text = self.extract_text_from_pdf(schema_file)
                if text:
                    qa_list = self.generate_from_schema(text, tema)
                    all_qa.extend(qa_list)
                    print(f"    ✓ Generadas {len(qa_list)} preguntas")
        
        return all_qa
    
    def run_pipeline(self):
        """Ejecuta pipeline completo"""
        print("🚀 Iniciando pipeline de generación con Ollama local")
        print(f"📁 Materiales: {self.materials_path}")
        print(f"🤖 Modelo: {self.model}")
        
        # Verificar Ollama
        if not self.check_ollama_connection():
            print("❌ No se puede conectar con Ollama")
            print("   Asegúrate de que Ollama esté corriendo: ollama serve")
            return
        
        print("✅ Conexión con Ollama OK\n")
        
        # Fase 1: Extraer de exámenes oficiales
        official_qa = self.process_official_exams()
        print(f"\n✅ Fase 1 completada: {len(official_qa)} Q&A extraídas\n")
        
        # Fase 2: Generar desde esquemas
        schema_qa = self.process_schemas()
        print(f"\n✅ Fase 2 completada: {len(schema_qa)} Q&A generadas\n")
        
        # Fase 3: Generar variaciones (solo de algunas)
        print("🔄 Generando variaciones...")
        variations = []
        for qa in official_qa[:5]:  # Solo 5 para prueba
            vars = self.generate_variations(qa)
            variations.extend(vars)
        print(f"✅ Fase 3 completada: {len(variations)} variaciones\n")
        
        # Guardar resultados
        output = {
            "metadata": {
                "fecha_generacion": datetime.now().isoformat(),
                "modelo": self.model,
                "total_qa": len(official_qa) + len(schema_qa) + len(variations)
            },
            "qa_oficiales": official_qa,
            "qa_esquemas": schema_qa,
            "variaciones": variations
        }
        
        output_file = self.output_dir / f"dataset_ollama_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Dataset guardado en: {output_file}")
        print(f"\n📊 RESUMEN:")
        print(f"   - Q&A oficiales: {len(official_qa)}")
        print(f"   - Q&A esquemas: {len(schema_qa)}")
        print(f"   - Variaciones: {len(variations)}")
        print(f"   - TOTAL: {output['metadata']['total_qa']}")

def main():
    pipeline = OllamaPipeline(
        materials_path="elemplos_leyes_info/de_mi_hija",
        model="mistral"  # o "mistral:7b-instruct" si lo tienes
    )
    
    pipeline.run_pipeline()

if __name__ == "__main__":
    main()
