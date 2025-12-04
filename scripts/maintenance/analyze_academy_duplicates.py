#!/usr/bin/env python3
"""
Analizador de Duplicados en Materiales de Academia
Usa Mistral local (Ollama) para detectar preguntas similares
"""

import ollama
import json
import re
from pathlib import Path
from typing import List, Dict
import PyPDF2
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class Question:
    text: str
    source_file: str
    page_number: int
    normalized_text: str = ""

class DuplicateAnalyzer:
    def __init__(self, model="mistral"):
        self.model = model
        try:
            self.client = ollama.Client()
        except Exception as e:
            print(f"⚠️ Error conectando con Ollama: {e}")
            print("💡 Asegúrate de que Ollama esté instalado y ejecutándose")
            self.client = None
        
    def extract_questions_from_pdf(self, pdf_path: Path) -> List[Question]:
        """Extrae preguntas de PDFs"""
        questions = []
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(reader.pages):
                    text = page.extract_text()
                    
                    # Patrones para detectar preguntas
                    patterns = [
                        r'(\d+\.\s+.+?)(?=\d+\.|$)',
                        r'(Pregunta\s+\d+:.*?)(?=Pregunta\s+\d+:|$)',
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, text, re.MULTILINE | re.DOTALL)
                        for match in matches:
                            if len(match.strip()) > 20:
                                question = Question(
                                    text=match.strip(),
                                    source_file=str(pdf_path.name),
                                    page_number=page_num + 1
                                )
                                questions.append(question)
                                
        except Exception as e:
            print(f"❌ Error procesando {pdf_path.name}: {e}")
            
        return questions
    
    def normalize_question(self, text: str) -> str:
        """Normaliza pregunta para detectar patrones"""
        normalized = text.lower()
        
        # Reemplazar números con placeholders
        normalized = re.sub(r'\b\d{4}\b', '[AÑO]', normalized)
        normalized = re.sub(r'\b\d{1,2}\b', '[NUM]', normalized)
        normalized = re.sub(r'\b\d+%\b', '[%]', normalized)
        normalized = re.sub(r'\b\d+\s*euros?\b', '[€]', normalized)
        
        # Reemplazar nombres comunes
        nombres = ['juan', 'maría', 'pedro', 'ana', 'josé', 'carmen']
        for nombre in nombres:
            normalized = re.sub(rf'\b{nombre}\b', '[NOMBRE]', normalized)
        
        return re.sub(r'\s+', ' ', normalized).strip()
    
    def analyze_similarity(self, q1: Question, q2: Question) -> Dict:
        """Analiza similitud entre dos preguntas"""
        if not self.client:
            return {"similitud": "ERROR", "explicacion": "Ollama no disponible"}
        
        prompt = f"""Analiza la similitud entre estas preguntas de oposiciones:

PREGUNTA 1: {q1.text[:300]}
PREGUNTA 2: {q2.text[:300]}

Clasifica como:
- EXACTA: Idénticas
- ALTA: Misma pregunta, datos diferentes
- MEDIA: Mismo concepto, enfoque diferente
- BAJA: Tema relacionado
- NINGUNA: Completamente diferentes

Responde SOLO con: SIMILITUD|explicación breve"""
        
        try:
            response = self.client.chat(model=self.model, messages=[
                {'role': 'user', 'content': prompt}
            ])
            
            content = response['message']['content']
            parts = content.split('|')
            
            return {
                "similitud": parts[0].strip().upper() if parts else "NINGUNA",
                "explicacion": parts[1].strip() if len(parts) > 1 else content[:100]
            }
                
        except Exception as e:
            return {"similitud": "ERROR", "explicacion": str(e)[:100]}
    
    def process_materials(self, base_path: str) -> Dict:
        """Procesa todos los materiales"""
        base_path = Path(base_path)
        
        folders = [
            "bajados_academia",
            "tests cortes",
            "Supuestos extrq",
            "AÑOS ANTERIORES"
        ]
        
        all_questions = []
        
        print("🔍 Extrayendo preguntas...")
        
        for folder in folders:
            folder_path = base_path / folder
            if folder_path.exists():
                pdf_files = list(folder_path.rglob("*.pdf"))[:5]  # Limitar a 5 por carpeta
                print(f"📁 {folder}: {len(pdf_files)} PDFs")
                
                for pdf_file in pdf_files:
                    questions = self.extract_questions_from_pdf(pdf_file)
                    for q in questions:
                        q.normalized_text = self.normalize_question(q.text)
                    all_questions.extend(questions)
                    print(f"   ✅ {pdf_file.name}: {len(questions)} preguntas")
        
        print(f"\n📊 Total: {len(all_questions)} preguntas")
        
        # Analizar duplicados (muestra)
        print("\n🔍 Analizando duplicados (muestra)...")
        duplicates = self._analyze_sample(all_questions[:20])
        
        return {
            "total_questions": len(all_questions),
            "duplicates_analysis": duplicates,
            "questions_sample": [asdict(q) for q in all_questions[:10]]
        }
    
    def _analyze_sample(self, questions: List[Question]) -> Dict:
        """Analiza muestra de preguntas"""
        duplicates = {
            "exactas": [],
            "altas": [],
            "medias": []
        }
        
        for i, q1 in enumerate(questions[:10]):
            for q2 in questions[i+1:i+3]:
                similarity = self.analyze_similarity(q1, q2)
                
                if similarity["similitud"] in ["EXACTA", "ALTA", "MEDIA"]:
                    duplicates[similarity["similitud"].lower() + "s"].append({
                        "pregunta1": q1.text[:100],
                        "pregunta2": q2.text[:100],
                        "analisis": similarity
                    })
                
                print(f"   Comparando {i+1}...", end="\r")
        
        print()
        return duplicates

def main():
    print("🚀 Analizador de Duplicados con Mistral Local\n")
    
    # Verificar Ollama
    try:
        client = ollama.Client()
        models = client.list()
        print(f"✅ Ollama disponible")
    except Exception as e:
        print(f"❌ Ollama no disponible: {e}")
        print("💡 Instala: curl -fsSL https://ollama.ai/install.sh | sh")
        print("💡 Descarga Mistral: ollama pull mistral")
        return
    
    # Analizar
    analyzer = DuplicateAnalyzer()
    base_path = "elemplos_leyes_info/de_mi_hija"
    
    results = analyzer.process_materials(base_path)
    
    # Guardar
    output_file = "analisis_duplicados_academia.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 RESULTADOS:")
    print(f"   Total preguntas: {results['total_questions']}")
    print(f"   Duplicados exactos: {len(results['duplicates_analysis']['exactas'])}")
    print(f"   Similitudes altas: {len(results['duplicates_analysis']['altas'])}")
    print(f"   📁 Guardado en: {output_file}")

if __name__ == "__main__":
    main()
