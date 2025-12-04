#!/usr/bin/env python3
"""
Generador de Q&A con Mistral Local (Ollama)
Extrae preguntas de exámenes indexados y genera variaciones
"""

import os
import json
import requests
from datetime import datetime
from typing import List, Dict, Optional
from qdrant_client import QdrantClient
import hashlib

class MistralLocalQAGenerator:
    def __init__(
        self,
        qdrant_url: str = "http://localhost:6333",
        ollama_url: str = "http://localhost:11434",
        collection_name: str = "materiales_academia"
    ):
        self.qdrant_url = qdrant_url
        self.ollama_url = ollama_url
        self.collection_name = collection_name
        
        print(f"🔄 Inicializando generador...")
        print(f"   Qdrant: {qdrant_url}")
        print(f"   Ollama: {ollama_url}")
        print(f"   Colección: {collection_name}")
        
        # Conectar a Qdrant
        self.qdrant = QdrantClient(url=qdrant_url)
        
        # Verificar Ollama
        if not self.check_ollama():
            raise Exception("❌ Ollama no está disponible")
        
        print("✅ Conexiones establecidas\n")
        
        self.generated_qa = []
        self.stats = {
            "preguntas_extraidas": 0,
            "variaciones_generadas": 0,
            "validadas": 0,
            "rechazadas": 0
        }
    
    def check_ollama(self) -> bool:
        """Verifica que Ollama esté funcionando"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def extract_questions_from_qdrant(self, limit: int = 10) -> List[Dict]:
        """Extrae preguntas de exámenes indexados en Qdrant"""
        print(f"📥 Extrayendo {limit} preguntas de Qdrant...")
        
        try:
            # Scroll para obtener puntos
            points, _ = self.qdrant.scroll(
                collection_name=self.collection_name,
                limit=limit,
                with_payload=True,
                with_vectors=False
            )
            
            questions = []
            for point in points:
                payload = point.payload
                
                # Filtrar solo preguntas (subcategory = "preguntas")
                if payload.get("subcategory") == "preguntas":
                    questions.append({
                        "id": point.id,
                        "text": payload.get("text", ""),
                        "filename": payload.get("filename", ""),
                        "page": payload.get("page_number", 0),
                        "category": payload.get("category", ""),
                        "subcategory": payload.get("subcategory", ""),
                        "year": payload.get("year")
                    })
            
            print(f"   ✅ Extraídas {len(questions)} preguntas")
            self.stats["preguntas_extraidas"] = len(questions)
            return questions
            
        except Exception as e:
            print(f"   ❌ Error extrayendo preguntas: {e}")
            return []
    
    def query_mistral(self, prompt: str, temperature: float = 0.3) -> Optional[str]:
        """Consulta a Mistral local via Ollama"""
        try:
            payload = {
                "model": "mistral:latest",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "top_p": 0.9,
                    "max_tokens": 2000
                }
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=300
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                print(f"   ⚠️  Error en Ollama: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error consultando Mistral: {e}")
            return None
    
    def generate_variations(self, question: Dict, num_variations: int = 2) -> List[Dict]:
        """Genera variaciones de una pregunta usando Mistral local"""
        print(f"\n🔄 Generando {num_variations} variaciones...")
        
        prompt = f"""Eres experto en Seguridad Social España. Crea {num_variations} variaciones de esta pregunta transformándola completamente.

PREGUNTA: {question['text'][:400]}

Responde SOLO JSON:
[{{"pregunta": "texto reformulado", "opciones": ["A) op1", "B) op2", "C) op3", "D) op4"], "respuesta_correcta": "A", "explicacion": "explicacion", "tema": "tema SS", "dificultad": "intermedia"}}]"""

        response = self.query_mistral(prompt, temperature=0.3)
        
        if not response:
            print("   ❌ No se obtuvo respuesta de Mistral")
            return []
        
        try:
            # Extraer JSON de la respuesta
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                variations = json.loads(json_str)
                
                # Validar y enriquecer
                valid_variations = []
                for var in variations:
                    if self.validate_qa(var):
                        var["source_id"] = question["id"]
                        var["source_file"] = question["filename"]
                        var["generated_at"] = datetime.now().isoformat()
                        var["model"] = "mistral:latest (ollama)"
                        var["hash"] = self.generate_hash(var["pregunta"])
                        
                        valid_variations.append(var)
                        self.stats["variaciones_generadas"] += 1
                        print(f"   ✅ Variación {len(valid_variations)} generada y validada")
                    else:
                        self.stats["rechazadas"] += 1
                        print(f"   ⚠️  Variación rechazada (no cumple validación)")
                
                return valid_variations
            else:
                print("   ❌ No se encontró JSON válido en la respuesta")
                return []
                
        except json.JSONDecodeError as e:
            print(f"   ❌ Error parseando JSON: {e}")
            print(f"   Respuesta recibida: {response[:200]}...")
            return []
    
    def validate_qa(self, qa: Dict) -> bool:
        """Valida que una Q&A cumpla los requisitos mínimos"""
        required_fields = ['pregunta', 'opciones', 'respuesta_correcta', 'explicacion', 'tema', 'dificultad']
        
        # Verificar campos requeridos
        if not all(field in qa for field in required_fields):
            return False
        
        # Verificar opciones
        if not isinstance(qa['opciones'], list) or len(qa['opciones']) != 4:
            return False
        
        # Verificar respuesta correcta
        if qa['respuesta_correcta'] not in ['A', 'B', 'C', 'D']:
            return False
        
        # Verificar longitud mínima
        if len(qa['pregunta']) < 30:
            return False
        
        # Verificar que cada opción tenga contenido
        for opcion in qa['opciones']:
            if len(opcion) < 5:
                return False
        
        self.stats["validadas"] += 1
        return True
    
    def generate_hash(self, text: str) -> str:
        """Genera hash único para una pregunta"""
        return hashlib.md5(text.lower().strip().encode()).hexdigest()[:12]
    
    def generate_dataset(self, num_questions: int = 10, variations_per_question: int = 2) -> List[Dict]:
        """Genera dataset completo"""
        print(f"\n{'='*60}")
        print(f"🚀 GENERACIÓN DE DATASET CON MISTRAL LOCAL")
        print(f"{'='*60}")
        print(f"Objetivo: {num_questions} preguntas × {variations_per_question} variaciones = {num_questions * variations_per_question} Q&A\n")
        
        # 1. Extraer preguntas de Qdrant
        questions = self.extract_questions_from_qdrant(limit=num_questions)
        
        if not questions:
            print("❌ No se pudieron extraer preguntas de Qdrant")
            return []
        
        # 2. Generar variaciones para cada pregunta
        all_variations = []
        for i, question in enumerate(questions, 1):
            print(f"\n--- Pregunta {i}/{len(questions)} ---")
            print(f"Archivo: {question['filename']}")
            print(f"Página: {question['page']}")
            print(f"Texto: {question['text'][:100]}...")
            
            variations = self.generate_variations(question, variations_per_question)
            all_variations.extend(variations)
            
            # Pequeña pausa entre preguntas
            if i < len(questions):
                import time
                time.sleep(1)
        
        self.generated_qa = all_variations
        
        # 3. Mostrar estadísticas
        self.print_stats()
        
        return all_variations
    
    def export_dataset(self, output_file: str = "dataset_mistral_local.jsonl"):
        """Exporta dataset a JSONL"""
        if not self.generated_qa:
            print("⚠️  No hay Q&A para exportar")
            return
        
        output_path = f"dataset_output/{output_file}"
        os.makedirs("dataset_output", exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for qa in self.generated_qa:
                f.write(json.dumps(qa, ensure_ascii=False) + '\n')
        
        print(f"\n📁 Dataset exportado: {output_path}")
        print(f"   Total Q&A: {len(self.generated_qa)}")
        
        # También exportar en formato legible
        readable_file = output_file.replace('.jsonl', '_readable.json')
        readable_path = f"dataset_output/{readable_file}"
        
        with open(readable_path, 'w', encoding='utf-8') as f:
            json.dump(self.generated_qa, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Versión legible: {readable_path}")
    
    def print_stats(self):
        """Muestra estadísticas de generación"""
        print(f"\n{'='*60}")
        print(f"📊 ESTADÍSTICAS DE GENERACIÓN")
        print(f"{'='*60}")
        print(f"Preguntas extraídas:      {self.stats['preguntas_extraidas']}")
        print(f"Variaciones generadas:    {self.stats['variaciones_generadas']}")
        print(f"Validadas correctamente:  {self.stats['validadas']}")
        print(f"Rechazadas:               {self.stats['rechazadas']}")
        
        if self.stats['variaciones_generadas'] > 0:
            success_rate = (self.stats['validadas'] / self.stats['variaciones_generadas']) * 100
            print(f"Tasa de éxito:            {success_rate:.1f}%")
        
        print(f"{'='*60}\n")
    
    def show_sample(self, num_samples: int = 2):
        """Muestra muestras del dataset generado"""
        if not self.generated_qa:
            print("⚠️  No hay Q&A para mostrar")
            return
        
        print(f"\n{'='*60}")
        print(f"📋 MUESTRAS DEL DATASET GENERADO")
        print(f"{'='*60}\n")
        
        for i, qa in enumerate(self.generated_qa[:num_samples], 1):
            print(f"--- Muestra {i} ---")
            print(f"Tema: {qa['tema']}")
            print(f"Dificultad: {qa['dificultad']}")
            print(f"\nPregunta:")
            print(f"{qa['pregunta']}\n")
            print(f"Opciones:")
            for opcion in qa['opciones']:
                print(f"  {opcion}")
            print(f"\nRespuesta correcta: {qa['respuesta_correcta']}")
            print(f"Explicación: {qa['explicacion']}")
            print(f"\nModelo: {qa['model']}")
            print(f"Archivo origen: {qa['source_file']}")
            print(f"\n{'='*60}\n")

def main():
    """Función principal"""
    print("\n🎯 GENERADOR DE Q&A CON MISTRAL LOCAL\n")
    
    # Crear generador
    generator = MistralLocalQAGenerator(
        qdrant_url="http://localhost:6333",
        ollama_url="http://localhost:11434",
        collection_name="materiales_academia"
    )
    
    # Generar dataset
    # 3 preguntas × 1 variación = 3 Q&A (prueba)
    dataset = generator.generate_dataset(
        num_questions=3,
        variations_per_question=1
    )
    
    if dataset:
        # Mostrar muestras
        generator.show_sample(num_samples=2)
        
        # Exportar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        generator.export_dataset(f"qa_mistral_local_{timestamp}.jsonl")
        
        print("✅ Generación completada exitosamente!")
    else:
        print("❌ No se pudo generar el dataset")

if __name__ == "__main__":
    main()