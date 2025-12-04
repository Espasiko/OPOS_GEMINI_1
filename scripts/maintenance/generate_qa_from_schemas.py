#!/usr/bin/env python3
"""
Generador de Q&A desde Esquemas de Prestaciones
Usa Mistral local para crear preguntas de alta calidad
"""

import ollama
import json
import re
from pathlib import Path
from typing import List, Dict
import PyPDF2
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class GeneratedQA:
    pregunta: str
    opciones: List[str]
    respuesta_correcta: str
    explicacion: str
    fuente: str
    tema: str
    dificultad: str
    fecha_generacion: str

class SchemaQAGenerator:
    def __init__(self, model="mistral"):
        self.model = model
        try:
            self.client = ollama.Client()
        except Exception as e:
            print(f"⚠️ Error conectando con Ollama: {e}")
            self.client = None
        
        # Mapeo de archivos a temas
        self.schema_topics = {
            "it.pdf": "Incapacidad Temporal",
            "ip_parcial.pdf": "Incapacidad Permanente Parcial",
            "ip_total.pdf": "Incapacidad Permanente Total",
            "jubilacion_ordinaria.pdf": "Jubilación Ordinaria",
            "jubilacion_anticipada_voluntaria.pdf": "Jubilación Anticipada Voluntaria",
            "viudedad.pdf": "Pensión de Viudedad",
            "orfandad.pdf": "Pensión de Orfandad",
            "cotizacion_2025_1.pdf": "Cotización 2025"
        }
    
    def extract_schema_content(self, pdf_path: Path) -> str:
        """Extrae contenido de esquemas PDF"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages[:3]:  # Solo primeras 3 páginas
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            print(f"❌ Error extrayendo {pdf_path.name}: {e}")
            return ""
    
    def generate_qa_from_schema(self, schema_text: str, topic: str, filename: str) -> List[GeneratedQA]:
        """Genera Q&A desde un esquema"""
        if not self.client:
            return []
        
        prompt = f"""Eres un experto creando preguntas de oposiciones de Seguridad Social.

ESQUEMA: {schema_text[:1500]}
TEMA: {topic}

Crea 3 preguntas tipo test (4 opciones cada una).

FORMATO (responde SOLO con JSON válido):
[
  {{
    "pregunta": "¿Cuál es el período mínimo de cotización para...?",
    "opciones": ["a) 15 años", "b) 25 años", "c) 35 años", "d) 37 años"],
    "respuesta_correcta": "a",
    "explicacion": "Según la LGSS, el período mínimo es...",
    "dificultad": "media"
  }}
]

IMPORTANTE:
- Basate SOLO en el esquema
- Incluye datos específicos
- Una respuesta correcta, tres incorrectas plausibles"""
        
        try:
            response = self.client.chat(model=self.model, messages=[
                {'role': 'user', 'content': prompt}
            ])
            
            content = response['message']['content']
            
            # Buscar JSON en la respuesta
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                qa_data = json.loads(json_match.group())
                
                generated = []
                for qa in qa_data:
                    generated.append(GeneratedQA(
                        pregunta=qa['pregunta'],
                        opciones=qa['opciones'],
                        respuesta_correcta=qa['respuesta_correcta'],
                        explicacion=qa['explicacion'],
                        fuente=filename,
                        tema=topic,
                        dificultad=qa.get('dificultad', 'media'),
                        fecha_generacion=datetime.now().isoformat()
                    ))
                
                return generated
            else:
                print(f"   ⚠️ No se pudo parsear JSON para {topic}")
                return []
                
        except Exception as e:
            print(f"   ❌ Error generando Q&A para {topic}: {e}")
            return []
    
    def process_all_schemas(self, base_path: str) -> Dict:
        """Procesa todos los esquemas"""
        base_path = Path(base_path)
        schema_path = base_path / "bajados_academia"
        
        results = {
            "generated_qa": [],
            "statistics": {
                "total_schemas": 0,
                "total_qa": 0
            }
        }
        
        print("🚀 Generando Q&A desde esquemas...\n")
        
        for filename, topic in list(self.schema_topics.items())[:3]:  # Limitar a 3
            schema_file = schema_path / filename
            
            if schema_file.exists():
                print(f"📄 Procesando: {topic}")
                
                schema_content = self.extract_schema_content(schema_file)
                
                if schema_content:
                    generated_qa = self.generate_qa_from_schema(
                        schema_content, topic, filename
                    )
                    
                    print(f"   ✅ Generadas {len(generated_qa)} preguntas")
                    
                    for qa in generated_qa:
                        results["generated_qa"].append(asdict(qa))
                    
                    results["statistics"]["total_qa"] += len(generated_qa)
                    results["statistics"]["total_schemas"] += 1
            else:
                print(f"   ⚠️ No encontrado: {filename}")
        
        return results
    
    def export_dataset(self, results: Dict, output_file: str = "dataset_schemas_qa.jsonl"):
        """Exporta dataset en formato JSONL"""
        with open(output_file, 'w', encoding='utf-8') as f:
            for qa_data in results["generated_qa"]:
                dataset_entry = {
                    "instruction": qa_data["pregunta"],
                    "input": "\n".join(qa_data["opciones"]),
                    "output": f"Respuesta: {qa_data['respuesta_correcta']}\n\nExplicación: {qa_data['explicacion']}",
                    "metadata": {
                        "tema": qa_data["tema"],
                        "fuente": qa_data["fuente"],
                        "dificultad": qa_data["dificultad"]
                    }
                }
                
                f.write(json.dumps(dataset_entry, ensure_ascii=False) + "\n")
        
        print(f"\n💾 Dataset exportado a: {output_file}")

def main():
    print("🚀 Generador de Q&A desde Esquemas\n")
    
    # Verificar Ollama
    try:
        client = ollama.Client()
        print("✅ Ollama disponible\n")
    except Exception as e:
        print(f"❌ Ollama no disponible: {e}")
        return
    
    # Generar
    generator = SchemaQAGenerator()
    base_path = "elemplos_leyes_info/de_mi_hija"
    
    results = generator.process_all_schemas(base_path)
    
    # Guardar
    with open("resultados_generacion_schemas.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Exportar dataset
    generator.export_dataset(results)
    
    # Estadísticas
    stats = results["statistics"]
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"   Esquemas procesados: {stats['total_schemas']}")
    print(f"   Q&A generadas: {stats['total_qa']}")

if __name__ == "__main__":
    main()
