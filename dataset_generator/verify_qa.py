#!/usr/bin/env python3
"""
Verifica la calidad de Q&A generadas usando un agente verificador.
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, List
from dotenv import load_dotenv
import groq
from rich.console import Console
from rich.progress import track

load_dotenv()
console = Console()


class QAVerifier:
    """Verificador de calidad de Q&A."""
    
    def __init__(self, config_path: str = "config.json"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.thresholds = self.config["quality_thresholds"]
    
    def check_basic_quality(self, qa: Dict) -> tuple[bool, List[str]]:
        """Verifica calidad básica (longitud, formato)."""
        issues = []
        
        question = qa.get("pregunta", "")
        answer = qa.get("respuesta", "")
        
        # Verificar longitudes
        if len(question) < self.thresholds["min_question_length"]:
            issues.append("Pregunta demasiado corta")
        if len(question) > self.thresholds["max_question_length"]:
            issues.append("Pregunta demasiado larga")
        
        if len(answer) < self.thresholds["min_answer_length"]:
            issues.append("Respuesta demasiado corta")
        if len(answer) > self.thresholds["max_answer_length"]:
            issues.append("Respuesta demasiado larga")
        
        # Verificar que no estén vacías
        if not question.strip():
            issues.append("Pregunta vacía")
        if not answer.strip():
            issues.append("Respuesta vacía")
        
        return len(issues) == 0, issues
    
    def verify_with_llm(self, qa: Dict) -> Dict:
        """Verifica Q&A usando LLM."""
        model_config = self.config["models"]["verifier"]
        
        prompt = f"""Eres un auditor experto en Seguridad Social española.

Evalúa esta pregunta-respuesta de oposición:

PREGUNTA: {qa.get('pregunta', '')}
RESPUESTA: {qa.get('respuesta', '')}
REFERENCIA: {qa.get('referencia', 'N/A')}

Evalúa:
1. ¿La pregunta está bien formulada y es clara?
2. ¿La respuesta es correcta legalmente?
3. ¿La respuesta responde completamente la pregunta?
4. ¿Las referencias legales son apropiadas?
5. ¿Hay errores factuales o contradicciones?

Responde en JSON:
{{
  "valida": true/false,
  "confianza": 0.0-1.0,
  "problemas": ["lista de problemas encontrados"],
  "sugerencias": "mejoras opcionales"
}}"""
        
        try:
            response = self.client.chat.completions.create(
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
            
            result = json.loads(content.strip())
            return result
            
        except Exception as e:
            console.print(f"[red]Error en verificación LLM: {e}[/red]")
            return {
                "valida": False,
                "confianza": 0.0,
                "problemas": [f"Error de verificación: {str(e)}"],
                "sugerencias": ""
            }
    
    def verify_qa(self, qa: Dict) -> Dict:
        """Verifica una Q&A completa."""
        # 1. Verificación básica
        basic_ok, basic_issues = self.check_basic_quality(qa)
        
        if not basic_ok:
            qa["verified"] = False
            qa["verification_issues"] = basic_issues
            qa["confidence"] = 0.0
            return qa
        
        # 2. Verificación con LLM
        llm_result = self.verify_with_llm(qa)
        
        # 3. Combinar resultados
        qa["verified"] = llm_result.get("valida", False) and \
                        llm_result.get("confianza", 0.0) >= self.thresholds["min_confidence"]
        qa["confidence"] = llm_result.get("confianza", 0.0)
        qa["verification_issues"] = llm_result.get("problemas", [])
        qa["suggestions"] = llm_result.get("sugerencias", "")
        
        return qa
    
    def process_dataset(self, qa_list: List[Dict]) -> tuple[List[Dict], Dict]:
        """Procesa un dataset completo."""
        verified_qa = []
        stats = {
            "total": len(qa_list),
            "verified": 0,
            "rejected": 0,
            "needs_review": 0
        }
        
        for qa in track(qa_list, description="Verificando Q&A..."):
            verified = self.verify_qa(qa)
            
            if verified["verified"]:
                stats["verified"] += 1
                verified_qa.append(verified)
            elif verified.get("confidence", 0.0) > 0.5:
                stats["needs_review"] += 1
                verified["needs_human_review"] = True
                verified_qa.append(verified)
            else:
                stats["rejected"] += 1
                # No añadir a verified_qa
        
        return verified_qa, stats


def main():
    parser = argparse.ArgumentParser(description="Verifica calidad de Q&A")
    parser.add_argument("--input", required=True, help="Archivo JSON con Q&A")
    parser.add_argument("--output", required=True, help="Archivo JSON verificado")
    parser.add_argument("--config", default="config.json", help="Archivo de configuración")
    parser.add_argument("--save-rejected", action="store_true", 
                       help="Guardar Q&A rechazadas en archivo separado")
    
    args = parser.parse_args()
    
    console.print("[bold blue]✓ Verificador de Calidad Q&A[/bold blue]\n")
    
    # Cargar Q&A
    with open(args.input, 'r', encoding='utf-8') as f:
        qa_list = json.load(f)
    
    console.print(f"[cyan]Cargadas {len(qa_list)} Q&A[/cyan]\n")
    
    # Verificar
    verifier = QAVerifier(args.config)
    verified_qa, stats = verifier.process_dataset(qa_list)
    
    # Guardar verificadas
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(verified_qa, f, ensure_ascii=False, indent=2)
    
    # Estadísticas
    console.print(f"\n[bold green]✓ Verificación completada[/bold green]\n")
    console.print(f"[cyan]Estadísticas:[/cyan]")
    console.print(f"  Total: {stats['total']}")
    console.print(f"  ✓ Verificadas: {stats['verified']} ({stats['verified']/stats['total']*100:.1f}%)")
    console.print(f"  ⚠ Necesitan revisión: {stats['needs_review']} ({stats['needs_review']/stats['total']*100:.1f}%)")
    console.print(f"  ✗ Rechazadas: {stats['rejected']} ({stats['rejected']/stats['total']*100:.1f}%)")
    console.print(f"\n[green]Guardadas {len(verified_qa)} Q&A → {output_path}[/green]")


if __name__ == "__main__":
    main()
