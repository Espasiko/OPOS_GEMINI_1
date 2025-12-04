#!/usr/bin/env python3
"""
Analizador de duplicados en materiales de academia
Detecta preguntas similares o duplicadas entre diferentes fuentes
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple
import PyPDF2
from difflib import SequenceMatcher
import json

class DuplicateAnalyzer:
    def __init__(self, materials_path: str):
        self.materials_path = Path(materials_path)
        self.questions = {}  # {source: [questions]}
        self.similarity_threshold = 0.85  # 85% similitud
        
    def extract_questions_from_pdf(self, pdf_path: Path) -> List[str]:
        """Extrae preguntas de un PDF"""
        questions = []
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                
                # Buscar patrones de preguntas
                # Patrón 1: Numeradas (1., 2., etc.)
                pattern1 = r'\d+\.\s+([^\.]+(?:\.[^\.]+){0,2}\.)'
                # Patrón 2: Con opciones a), b), c), d)
                pattern2 = r'([^\n]+\?[^\n]*(?:\n\s*[a-d]\).*){2,4})'
                
                matches1 = re.findall(pattern1, text)
                matches2 = re.findall(pattern2, text, re.MULTILINE)
                
                questions.extend(matches1)
                questions.extend(matches2)
                
        except Exception as e:
            print(f"Error procesando {pdf_path}: {e}")
        
        return [q.strip() for q in questions if len(q.strip()) > 20]
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calcula similitud entre dos textos"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def find_duplicates(self) -> Dict[str, List[Tuple[str, str, float]]]:
        """Encuentra duplicados entre fuentes"""
        duplicates = {}
        
        sources = list(self.questions.keys())
        for i, source1 in enumerate(sources):
            for source2 in sources[i+1:]:
                matches = []
                for q1 in self.questions[source1]:
                    for q2 in self.questions[source2]:
                        similarity = self.calculate_similarity(q1, q2)
                        if similarity >= self.similarity_threshold:
                            matches.append((q1, q2, similarity))
                
                if matches:
                    key = f"{source1} <-> {source2}"
                    duplicates[key] = matches
        
        return duplicates
    
    def analyze_directory(self, directory: Path, label: str):
        """Analiza un directorio de PDFs"""
        if not directory.exists():
            return
        
        pdf_files = list(directory.glob("*.pdf"))
        all_questions = []
        
        for pdf_file in pdf_files:
            questions = self.extract_questions_from_pdf(pdf_file)
            all_questions.extend(questions)
        
        if all_questions:
            self.questions[label] = all_questions
    
    def run_analysis(self) -> Dict:
        """Ejecuta análisis completo"""
        print("🔍 Analizando materiales de academia...")
        
        # Analizar diferentes fuentes
        sources = {
            "Exámenes Oficiales 2022-2025": self.materials_path / "bajados_academia",
            "Simulacros Las Cortes": self.materials_path / "2024 opos ss y advo-20250327T124030Z-001/2024 opos ss y advo/SEGURIDAD SOCIAL LAS CORTES/tests cortes",
            "Exámenes Años Anteriores": self.materials_path / "AÑOS ANTERIORES-20250327T124026Z-001/AÑOS ANTERIORES",
            "Simulacros Generales": self.materials_path / "Simulacros-20250327T124008Z-001/Simulacros",
        }
        
        for label, path in sources.items():
            self.analyze_directory(path, label)
        
        # Encontrar duplicados
        duplicates = self.find_duplicates()
        
        # Generar reporte
        report = {
            "total_sources": len(self.questions),
            "questions_per_source": {k: len(v) for k, v in self.questions.items()},
            "duplicates_found": len(duplicates),
            "duplicate_details": {}
        }
        
        for key, matches in duplicates.items():
            report["duplicate_details"][key] = {
                "count": len(matches),
                "avg_similarity": sum(m[2] for m in matches) / len(matches),
                "examples": matches[:3]  # Primeros 3 ejemplos
            }
        
        return report

def main():
    materials_path = "elemplos_leyes_info/de_mi_hija"
    
    analyzer = DuplicateAnalyzer(materials_path)
    report = analyzer.run_analysis()
    
    # Guardar reporte
    with open("analisis_duplicados_academia.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Mostrar resumen
    print("\n📊 RESUMEN DEL ANÁLISIS:")
    print(f"Total de fuentes analizadas: {report['total_sources']}")
    print(f"\nPreguntas por fuente:")
    for source, count in report['questions_per_source'].items():
        print(f"  - {source}: {count} preguntas")
    
    print(f"\n🔄 Duplicados encontrados: {report['duplicates_found']} pares de fuentes")
    
    if report['duplicate_details']:
        print("\nDetalle de duplicados:")
        for pair, details in report['duplicate_details'].items():
            print(f"\n  {pair}:")
            print(f"    - {details['count']} preguntas similares")
            print(f"    - Similitud promedio: {details['avg_similarity']:.1%}")
    
    print("\n✅ Reporte completo guardado en: analisis_duplicados_academia.json")

if __name__ == "__main__":
    main()
