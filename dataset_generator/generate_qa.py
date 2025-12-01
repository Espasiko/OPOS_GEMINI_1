#!/usr/bin/env python3
"""
Genera pares Q&A desde textos usando pipeline multi-agente.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv
import groq
import anthropic
from rich.console import Console
from rich.progress import track
import tiktoken

load_dotenv()
console = Console()


class QAGenerator:
    """Generador de Q&A con soporte multi-modelo."""
    
    def __init__(self, config_path: str = "config.json"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # Inicializar clientes
        self.groq_client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key) if anthropic_key else None
        
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def chunk_text(self, text: str) -> List[str]:
        """Divide texto en chunks manejables."""
        chunk_size = self.config["chunking"]["chunk_size"]
        overlap = self.config["chunking"]["overlap"]
        min_size = self.config["chunking"]["min_chunk_size"]
        
        # Dividir por párrafos
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            if len(current_chunk) + len(para) < chunk_size:
                current_chunk += para + "\n\n"
            else:
                if len(current_chunk) >= min_size:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"
        
        if len(current_chunk) >= min_size:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def classify_complexity(self, text: str) -> str:
        """Clasifica si el texto es simple o complejo."""
        text_lower = text.lower()
        
        simple_count = sum(1 for kw in self.config["complexity_keywords"]["simple"] 
                          if kw in text_lower)
        complex_count = sum(1 for kw in self.config["complexity_keywords"]["complex"] 
                           if kw in text_lower)
        
        # Si tiene palabras clave de complejidad o es muy largo
        if complex_count > simple_count or len(text) > 2000:
            return "complex"
        return "simple"
    
    def classify_risk_level(self, qa: Dict, chunk: str) -> str:
        """
        Clasifica el nivel de riesgo de una Q&A.
        
        ALTO: Normativa, leyes, jurisprudencia, cálculos legales
        MEDIO: Procedimientos, trámites generales
        BAJO: Definiciones simples, conceptos básicos
        """
        risk_config = self.config["risk_classification"]
        
        # Combinar pregunta + respuesta + chunk para análisis
        full_text = f"{qa.get('pregunta', '')} {qa.get('respuesta', '')} {chunk}".lower()
        
        # ALTO RIESGO: Si contiene referencias legales específicas
        for keyword in risk_config["always_review_if_contains"]:
            if keyword.lower() in full_text:
                return "high"
        
        # Contar keywords de alto riesgo
        high_risk_count = sum(1 for kw in risk_config["high_risk_keywords"] 
                             if kw in full_text)
        
        # Contar keywords de medio riesgo
        medium_risk_count = sum(1 for kw in risk_config["medium_risk_keywords"] 
                               if kw in full_text)
        
        # Clasificar por umbral
        if high_risk_count >= 2:
            return "high"
        elif high_risk_count >= 1 or medium_risk_count >= 2:
            return "medium"
        else:
            return "low"
    
    def determine_content_type(self, qa: Dict, chunk: str) -> str:
        """Determina el tipo de contenido de la Q&A."""
        text = f"{qa.get('pregunta', '')} {qa.get('respuesta', '')}".lower()
        
        # Detectar tipo de contenido
        if any(word in text for word in ["artículo", "art.", "ley", "real decreto", "rd"]):
            return "normativa"
        elif any(word in text for word in ["sentencia", "tribunal", "jurisprudencia"]):
            return "jurisprudencia"
        elif any(word in text for word in ["calcular", "cálculo", "base reguladora", "cuantía"]):
            return "calculo_legal"
        elif "caso práctico" in text or "supuesto" in text:
            return "caso_practico"
        elif any(word in text for word in ["a)", "b)", "c)", "d)"]):
            return "test_multiple_choice"
        elif any(word in text for word in ["procedimiento", "trámite", "solicitud"]):
            return "procedimiento"
        elif any(word in text for word in ["definición", "concepto", "qué es"]):
            return "definicion"
        else:
            return "general"
    
    def generate_with_groq(self, chunk: str, num_questions: int = 3) -> List[Dict]:
        """Genera Q&A usando Groq."""
        model_config = self.config["models"]["generator_simple"]
        
        prompt = f"""Eres un experto en Seguridad Social española y oposiciones.

Basándote en este texto legal:

{chunk}

Genera {num_questions} pares de pregunta-respuesta tipo oposición.

REQUISITOS:
- Preguntas claras y concisas (1-2 líneas)
- Respuestas precisas con referencias legales (2-4 líneas)
- Incluir artículo/ley específica cuando aplique
- Estilo formal de oposición española

Formato JSON:
[
  {{
    "pregunta": "...",
    "respuesta": "...",
    "referencia": "Art. X LGSS"
  }}
]"""
        
        try:
            response = self.groq_client.chat.completions.create(
                model=model_config["model"],
                messages=[{"role": "user", "content": prompt}],
                temperature=model_config["temperature"],
                max_tokens=model_config["max_tokens"]
            )
            
            content = response.choices[0].message.content
            
            # Extraer JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            qa_pairs = json.loads(content.strip())
            return qa_pairs if isinstance(qa_pairs, list) else [qa_pairs]
            
        except Exception as e:
            console.print(f"[red]Error con Groq: {e}[/red]")
            return []
    
    def generate_with_claude(self, chunk: str, num_questions: int = 2) -> List[Dict]:
        """Genera Q&A complejos usando Claude."""
        if not self.anthropic_client:
            console.print("[yellow]Claude no configurado, usando Groq[/yellow]")
            return self.generate_with_groq(chunk, num_questions)
        
        model_config = self.config["models"]["generator_complex"]
        
        prompt = f"""Eres un experto en Seguridad Social española especializado en casos prácticos de oposiciones.

Basándote en este texto legal:

{chunk}

Genera {num_questions} casos prácticos complejos tipo oposición con pregunta y respuesta detallada.

REQUISITOS:
- Casos realistas y complejos
- Preguntas que requieran razonamiento jurídico
- Respuestas completas con fundamentación legal
- Referencias exactas a artículos
- Estilo profesional de oposición

Formato JSON:
[
  {{
    "pregunta": "...",
    "respuesta": "...",
    "referencia": "Arts. X, Y LGSS"
  }}
]"""
        
        try:
            response = self.anthropic_client.messages.create(
                model=model_config["model"],
                max_tokens=model_config["max_tokens"],
                temperature=model_config["temperature"],
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            
            # Extraer JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            qa_pairs = json.loads(content.strip())
            return qa_pairs if isinstance(qa_pairs, list) else [qa_pairs]
            
        except Exception as e:
            console.print(f"[red]Error con Claude: {e}[/red]")
            return []
    
    def generate_from_chunk(self, chunk: str, source: str) -> List[Dict]:
        """Genera Q&A desde un chunk, eligiendo el modelo apropiado."""
        complexity = self.classify_complexity(chunk)
        
        if complexity == "complex":
            console.print(f"[blue]→ Usando Claude (complejo)[/blue]")
            qa_pairs = self.generate_with_claude(chunk, num_questions=2)
        else:
            console.print(f"[cyan]→ Usando Groq (simple)[/cyan]")
            qa_pairs = self.generate_with_groq(chunk, num_questions=3)
        
        # Añadir metadata completa con clasificación de riesgo
        for qa in qa_pairs:
            qa["source"] = source
            qa["complexity"] = complexity
            qa["verified"] = False
            qa["human_reviewed"] = False
            
            # Clasificar riesgo y tipo de contenido
            qa["risk_level"] = self.classify_risk_level(qa, chunk)
            qa["content_type"] = self.determine_content_type(qa, chunk)
            
            # Determinar si necesita revisión humana obligatoria
            review_strategy = self.config["human_review_strategy"]
            if qa["risk_level"] == "high":
                qa["needs_human_review"] = True
                qa["review_priority"] = "critical"
            elif qa["risk_level"] == "medium":
                # 20% de las medium risk necesitan revisión
                import random
                qa["needs_human_review"] = random.random() < review_strategy["medium_risk_review_rate"]
                qa["review_priority"] = "medium"
            else:
                # 5% de las low risk necesitan revisión (muestreo)
                import random
                qa["needs_human_review"] = random.random() < review_strategy["low_risk_review_rate"]
                qa["review_priority"] = "low"
        
        return qa_pairs
    
    def process_file(self, file_path: str) -> List[Dict]:
        """Procesa un archivo de texto completo."""
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        chunks = self.chunk_text(text)
        console.print(f"[green]Dividido en {len(chunks)} chunks[/green]")
        
        all_qa = []
        for i, chunk in enumerate(chunks, 1):
            console.print(f"\n[bold]Chunk {i}/{len(chunks)}[/bold]")
            qa_pairs = self.generate_from_chunk(chunk, Path(file_path).name)
            all_qa.extend(qa_pairs)
            console.print(f"[green]✓ Generadas {len(qa_pairs)} Q&A[/green]")
        
        return all_qa


def main():
    parser = argparse.ArgumentParser(description="Genera Q&A desde textos")
    parser.add_argument("--input", required=True, help="Directorio con textos o archivo único")
    parser.add_argument("--output", required=True, help="Archivo JSON de salida")
    parser.add_argument("--config", default="config.json", help="Archivo de configuración")
    
    args = parser.parse_args()
    
    console.print("[bold blue]🤖 Generador de Q&A Multi-Agente[/bold blue]\n")
    
    generator = QAGenerator(args.config)
    all_qa = []
    
    input_path = Path(args.input)
    
    if input_path.is_file():
        # Procesar un solo archivo
        console.print(f"[cyan]Procesando: {input_path.name}[/cyan]\n")
        qa_pairs = generator.process_file(str(input_path))
        all_qa.extend(qa_pairs)
    else:
        # Procesar directorio
        txt_files = list(input_path.glob("*.txt"))
        console.print(f"[green]Encontrados {len(txt_files)} archivos[/green]\n")
        
        for txt_file in txt_files:
            console.print(f"\n[bold cyan]📄 {txt_file.name}[/bold cyan]")
            qa_pairs = generator.process_file(str(txt_file))
            all_qa.extend(qa_pairs)
    
    # Guardar resultados
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_qa, f, ensure_ascii=False, indent=2)
    
    console.print(f"\n[bold green]✓ Generadas {len(all_qa)} Q&A → {output_path}[/bold green]")
    
    # Estadísticas
    simple_count = sum(1 for qa in all_qa if qa.get("complexity") == "simple")
    complex_count = sum(1 for qa in all_qa if qa.get("complexity") == "complex")
    
    console.print(f"\n[cyan]Estadísticas:[/cyan]")
    console.print(f"  Simple: {simple_count}")
    console.print(f"  Complejo: {complex_count}")


if __name__ == "__main__":
    main()
