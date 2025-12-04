#!/usr/bin/env python3
"""
Pipeline SEGURO con Mistral Local + Qdrant Local
Genera Q&A de máxima calidad sin dejar rastros identificables
"""

import os
import json
import requests
from pathlib import Path
from typing import List, Dict, Optional
import PyPDF2
from datetime import datetime
import re

class SecurePipeline:
    def __init__(self, 
                 materials_path: str,
                 qdrant_url: str = "http://localhost:6333",
                 ollama_url: str = "http://localhost:11434",
                 model: str = "mistral"):
        self.materials_path = Path(materials_path)
        self.qdrant_url = qdrant_url
        self.ollama_url = ollama_url
        self.model = model
        self.output_dir = Path("dataset_output_seguro")
        self.output_dir.mkdir(exist_ok=True)
        
        # Patrones a detectar y eliminar
        self.forbidden_patterns = {
            "nombres_autores": [
                r"Sara Domínguez", r"Carlos Hernández", r"Alfonso Hidalgo",
                r"Víctor Cabeza", r"Pablo Segado"
            ],
            "academias": [
                r"Las Cortes", r"TEMA DIGITAL", r"GoKoan", r"Oposiciones\.es"
            ],
            "identificadores": [
                r"5001-", r"5002-", r"8035-", r"8038-", r"8039-", r"8040-",
                r"Anexo\d+A\d+", r"ISBN.*", r"Ref\.\s*\d+"
            ],
            "copyright": [
                r"Queda prohibido", r"©\s*\d{4}", r"Copyright",
                r"Todos los derechos reservados", r"Material protegido"
            ],
            "estructuras_especificas": [
                r"villancico", r"Simulacro.*\d{1,2}.*\d{4}",
                r"Cuadernillo.*ejercicio"
            ]
        }
    
    def check_ollama(self) -> bool:
        """Verifica Ollama"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def check_qdrant(self) -> bool:
        """Verifica Qdrant"""
        try:
            response = requests.get(f"{self.qdrant_url}/collections", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def query_qdrant(self, query: str, collection: str = "leyes_ss", limit: int = 5) -> List[Dict]:
        """Consulta Qdrant para obtener contexto legal"""
        try:
            # Primero obtener embedding del query
            embed_response = requests.post(
                f"{self.ollama_url}/api/embeddings",
                json={"model": self.model, "prompt": query},
                timeout=30
            )
            
            if embed_response.status_code != 200:
                return []
            
            embedding = embed_response.json()["embedding"]
            
            # Buscar en Qdrant
            search_response = requests.post(
                f"{self.qdrant_url}/collections/{collection}/points/search",
                json={
                    "vector": embedding,
                    "limit": limit,
                    "with_payload": True
                },
                timeout=10
            )
            
            if search_response.status_code == 200:
                results = search_response.json()["result"]
                return [r["payload"] for r in results]
            
            return []
        except Exception as e:
            print(f"Error consultando Qdrant: {e}")
            return []
    
    def generate_with_ollama(self, prompt: str, system: str = "") -> str:
        """Genera con Ollama"""
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
            return ""
        except Exception as e:
            print(f"Error en Ollama: {e}")
            return ""
    
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extrae texto de PDF"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"Error extrayendo {pdf_path}: {e}")
            return ""
    
    def clean_revealing_data(self, text: str) -> tuple[str, List[str]]:
        """Limpia datos reveladores del texto"""
        cleaned = text
        found_patterns = []
        
        for category, patterns in self.forbidden_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, cleaned, re.IGNORECASE)
                if matches:
                    found_patterns.extend([f"{category}: {m}" for m in matches])
                    # Reemplazar con [REDACTADO]
                    cleaned = re.sub(pattern, "[REDACTADO]", cleaned, flags=re.IGNORECASE)
        
        return cleaned, found_patterns
    
    def generate_qa_with_legal_context(self, tema: str, num_questions: int = 5) -> List[Dict]:
        """Genera Q&A consultando Qdrant para contexto legal"""
        
        # Consultar Qdrant
        legal_context = self.query_qdrant(tema, limit=10)
        
        if not legal_context:
            print(f"⚠️  No se encontró contexto legal para: {tema}")
            return []
        
        # Construir contexto legal
        context_text = "\n\n".join([
            f"ARTÍCULO {ctx.get('articulo', 'N/A')}:\n{ctx.get('texto', '')[:500]}"
            for ctx in legal_context[:5]
        ])
        
        system_prompt = """Eres un experto en Seguridad Social española.
Creas preguntas tipo test de MÁXIMA CALIDAD para oposiciones.

REGLAS ESTRICTAS DE SEGURIDAD:
1. NO menciones NUNCA nombres de autores, academias o editoriales
2. NO uses identificadores específicos (ISBN, referencias, códigos)
3. NO copies frases textuales de materiales con copyright
4. NO uses estructuras características de academias específicas
5. Basa TODO en la legislación oficial que te proporciono
6. Cita SIEMPRE el artículo de ley correspondiente
7. Crea preguntas ORIGINALES pero legalmente correctas

IMPORTANTE: Estás creando contenido NUEVO basado en legislación PÚBLICA.
No estás copiando ni adaptando material protegido.

Formato JSON:
{
  "preguntas": [
    {
      "pregunta": "texto de la pregunta",
      "opciones": ["a) ...", "b) ...", "c) ...", "d) ..."],
      "respuesta_correcta": "letra",
      "base_legal": "Art. X LGSS",
      "explicacion": "por qué es correcta"
    }
  ]
}"""
        
        prompt = f"""Genera {num_questions} preguntas tipo test sobre: {tema}

CONTEXTO LEGAL OFICIAL (BOE):
{context_text}

INSTRUCCIONES:
- Basa las preguntas SOLO en el contexto legal proporcionado
- Crea preguntas sobre: requisitos, cuantías, plazos, procedimientos
- Las 4 opciones deben ser plausibles pero solo 1 correcta
- Incluye el artículo de ley en cada pregunta
- NO uses nombres de autores ni academias
- NO copies frases textuales

Responde SOLO con el JSON, sin texto adicional."""

        response = self.generate_with_ollama(prompt, system_prompt)
        
        try:
            # Parsear JSON
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            
            data = json.loads(response.strip())
            
            # Limpiar y validar cada pregunta
            cleaned_questions = []
            for q in data.get("preguntas", []):
                # Limpiar datos reveladores
                pregunta_limpia, found1 = self.clean_revealing_data(q.get("pregunta", ""))
                explicacion_limpia, found2 = self.clean_revealing_data(q.get("explicacion", ""))
                
                # Si se encontraron patrones prohibidos, marcar para revisión
                needs_review = len(found1) > 0 or len(found2) > 0
                
                cleaned_q = {
                    "pregunta": pregunta_limpia,
                    "opciones": q.get("opciones", []),
                    "respuesta_correcta": q.get("respuesta_correcta", ""),
                    "base_legal": q.get("base_legal", ""),
                    "explicacion": explicacion_limpia,
                    "tema": tema,
                    "metadata": {
                        "metodo": "generacion_qdrant_local",
                        "fecha_generacion": datetime.now().isoformat(),
                        "requiere_revision": needs_review,
                        "patrones_encontrados": found1 + found2 if needs_review else []
                    }
                }
                
                cleaned_questions.append(cleaned_q)
            
            return cleaned_questions
            
        except json.JSONDecodeError as e:
            print(f"Error parseando JSON: {e}")
            return []
    
    def generate_test_batch(self, num_questions: int = 20) -> List[Dict]:
        """Genera lote de prueba de 20 preguntas"""
        print(f"🚀 Generando {num_questions} preguntas de prueba...")
        
        # Temas a cubrir
        temas = [
            "Incapacidad Temporal",
            "Incapacidad Permanente Parcial",
            "Jubilación ordinaria",
            "Prestación de viudedad"
        ]
        
        all_questions = []
        questions_per_tema = num_questions // len(temas)
        
        for tema in temas:
            print(f"\n📚 Tema: {tema}")
            questions = self.generate_qa_with_legal_context(tema, questions_per_tema)
            all_questions.extend(questions)
            print(f"  ✓ Generadas {len(questions)} preguntas")
            
            # Mostrar si hay patrones prohibidos
            needs_review = [q for q in questions if q["metadata"]["requiere_revision"]]
            if needs_review:
                print(f"  ⚠️  {len(needs_review)} preguntas requieren revisión")
        
        return all_questions
    
    def save_results(self, questions: List[Dict], filename: str = "test_20_preguntas.json"):
        """Guarda resultados"""
        output_file = self.output_dir / filename
        
        output = {
            "metadata": {
                "fecha_generacion": datetime.now().isoformat(),
                "modelo": self.model,
                "total_preguntas": len(questions),
                "requieren_revision": len([q for q in questions if q["metadata"]["requiere_revision"]]),
                "metodo": "qdrant_local + mistral_local"
            },
            "preguntas": questions
        }
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Resultados guardados en: {output_file}")
        return output_file
    
    def generate_review_report(self, questions: List[Dict]):
        """Genera reporte de revisión"""
        needs_review = [q for q in questions if q["metadata"]["requiere_revision"]]
        
        if not needs_review:
            print("\n✅ ¡Perfecto! Ninguna pregunta requiere revisión")
            return
        
        print(f"\n⚠️  REPORTE DE REVISIÓN:")
        print(f"Total preguntas que requieren revisión: {len(needs_review)}")
        print("\nPatrones encontrados:")
        
        all_patterns = {}
        for q in needs_review:
            for pattern in q["metadata"]["patrones_encontrados"]:
                category = pattern.split(":")[0]
                all_patterns[category] = all_patterns.get(category, 0) + 1
        
        for category, count in all_patterns.items():
            print(f"  - {category}: {count} ocurrencias")
        
        print("\nEjemplos de preguntas a revisar:")
        for i, q in enumerate(needs_review[:3], 1):
            print(f"\n{i}. {q['pregunta'][:100]}...")
            print(f"   Patrones: {q['metadata']['patrones_encontrados']}")
    
    def run_test(self):
        """Ejecuta prueba de 20 preguntas"""
        print("🔒 Pipeline SEGURO - Prueba de 20 preguntas")
        print("=" * 60)
        
        # Verificar servicios
        print("\n🔍 Verificando servicios...")
        
        if not self.check_ollama():
            print("❌ Ollama no está disponible")
            print("   Ejecuta en WSL: ollama serve")
            return
        print("✅ Ollama OK")
        
        if not self.check_qdrant():
            print("❌ Qdrant no está disponible")
            print("   Ejecuta: docker-compose up -d")
            return
        print("✅ Qdrant OK")
        
        # Generar preguntas
        questions = self.generate_test_batch(20)
        
        if not questions:
            print("\n❌ No se generaron preguntas")
            return
        
        # Guardar resultados
        output_file = self.save_results(questions)
        
        # Generar reporte de revisión
        self.generate_review_report(questions)
        
        # Resumen
        print("\n" + "=" * 60)
        print("📊 RESUMEN:")
        print(f"   Total preguntas: {len(questions)}")
        print(f"   Requieren revisión: {len([q for q in questions if q['metadata']['requiere_revision']])}")
        print(f"   Limpias: {len([q for q in questions if not q['metadata']['requiere_revision']])}")
        print(f"   Archivo: {output_file}")

def main():
    pipeline = SecurePipeline(
        materials_path="elemplos_leyes_info/de_mi_hija",
        model="mistral"
    )
    
    pipeline.run_test()

if __name__ == "__main__":
    main()
