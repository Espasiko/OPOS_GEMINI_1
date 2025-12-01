#!/usr/bin/env python3
"""
Exporta Q&A verificadas a formato JSONL para fine-tuning.
"""

import json
import argparse
from pathlib import Path
from typing import List, Dict
from rich.console import Console
import random

console = Console()


def format_for_finetuning(qa: Dict, system_prompt: str, qa_id: str = None) -> Dict:
    """
    Formatea Q&A para fine-tuning con metadata completa.
    Sigue el esquema JSONL estándar con trazabilidad completa.
    """
    from datetime import datetime
    
    # Generar ID si no existe
    if not qa_id:
        qa_id = qa.get("id", f"qa_{hash(qa.get('pregunta', ''))}")
    
    return {
        # Identificación
        "id": qa_id,
        
        # Contenido principal
        "question": qa.get("pregunta", ""),
        "answer": qa.get("respuesta", ""),
        
        # Fuente y ubicación
        "source_document": qa.get("source", "unknown"),
        "source_location": qa.get("source_location", ""),
        
        # Clasificación
        "content_type": qa.get("content_type", "general"),
        "difficulty_level": qa.get("difficulty_level", "medium"),
        "risk_level": qa.get("risk_level", "medium"),
        
        # Generación
        "generated_by": qa.get("generated_by", "unknown"),
        "complexity": qa.get("complexity", "unknown"),
        
        # Verificación IA
        "verified_by_ia": qa.get("verified", False),
        "confidence": qa.get("confidence", 0.0),
        "verification_issues": qa.get("verification_issues", []),
        
        # Revisión humana
        "verified_by_human": qa.get("human_reviewed", False),
        "human_reviewer": qa.get("human_reviewer", None),
        "review_date": qa.get("review_date", datetime.now().strftime("%Y-%m-%d")),
        "review_notes": qa.get("review_notes", ""),
        "final_status": qa.get("human_review_status", qa.get("final_status", "accepted")),
        
        # Metadata adicional
        "needs_human_review": qa.get("needs_human_review", False),
        "review_priority": qa.get("review_priority", "low"),
        "referencia": qa.get("referencia", ""),
        "tags": qa.get("tags", []),
        "notes": qa.get("notes", ""),
        
        # Versionado
        "version": qa.get("version", "1"),
        "created_at": qa.get("created_at", datetime.now().strftime("%Y-%m-%d")),
        "last_modified": qa.get("last_modified", datetime.now().strftime("%Y-%m-%d")),
        
        # Formato para fine-tuning (compatible OpenAI/Mistral)
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": qa.get("pregunta", "")
            },
            {
                "role": "assistant",
                "content": qa.get("respuesta", "")
            }
        ]
    }


def split_dataset(qa_list: List[Dict], train_ratio: float = 0.8, 
                 val_ratio: float = 0.1) -> tuple[List, List, List]:
    """Divide dataset en train/val/test."""
    random.shuffle(qa_list)
    
    total = len(qa_list)
    train_size = int(total * train_ratio)
    val_size = int(total * val_ratio)
    
    train = qa_list[:train_size]
    val = qa_list[train_size:train_size + val_size]
    test = qa_list[train_size + val_size:]
    
    return train, val, test


def export_jsonl(qa_list: List[Dict], output_path: str, system_prompt: str):
    """Exporta a formato JSONL con metadata completa."""
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, qa in enumerate(qa_list, 1):
            # Generar ID único si no existe
            qa_id = qa.get("id", f"qa_{i:05d}")
            formatted = format_for_finetuning(qa, system_prompt, qa_id)
            f.write(json.dumps(formatted, ensure_ascii=False) + '\n')


def main():
    parser = argparse.ArgumentParser(description="Exporta dataset para fine-tuning")
    parser.add_argument("--input", required=True, help="Archivo JSON verificado")
    parser.add_argument("--output", required=True, help="Archivo JSONL de salida")
    parser.add_argument("--split", action="store_true", 
                       help="Dividir en train/val/test")
    parser.add_argument("--train-ratio", type=float, default=0.8,
                       help="Proporción de entrenamiento (default: 0.8)")
    parser.add_argument("--val-ratio", type=float, default=0.1,
                       help="Proporción de validación (default: 0.1)")
    parser.add_argument("--system-prompt", type=str,
                       default="Eres OpositAIA, un experto en Seguridad Social española especializado en preparación de oposiciones. Proporciona respuestas precisas, fundamentadas legalmente y con referencias a la normativa vigente.",
                       help="System prompt para el modelo")
    
    args = parser.parse_args()
    
    console.print("[bold blue]📦 Exportador de Dataset[/bold blue]\n")
    
    # Cargar Q&A verificadas
    with open(args.input, 'r', encoding='utf-8') as f:
        qa_list = json.load(f)
    
    console.print(f"[cyan]Cargadas {len(qa_list)} Q&A verificadas[/cyan]\n")
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if args.split:
        # Dividir dataset
        train, val, test = split_dataset(qa_list, args.train_ratio, args.val_ratio)
        
        # Exportar cada split
        train_path = output_path.parent / f"{output_path.stem}_train.jsonl"
        val_path = output_path.parent / f"{output_path.stem}_val.jsonl"
        test_path = output_path.parent / f"{output_path.stem}_test.jsonl"
        
        export_jsonl(train, str(train_path), args.system_prompt)
        export_jsonl(val, str(val_path), args.system_prompt)
        export_jsonl(test, str(test_path), args.system_prompt)
        
        console.print(f"[green]✓ Train: {len(train)} Q&A → {train_path}[/green]")
        console.print(f"[green]✓ Val: {len(val)} Q&A → {val_path}[/green]")
        console.print(f"[green]✓ Test: {len(test)} Q&A → {test_path}[/green]")
    else:
        # Exportar todo junto
        export_jsonl(qa_list, str(output_path), args.system_prompt)
        console.print(f"[green]✓ Exportadas {len(qa_list)} Q&A → {output_path}[/green]")
    
    # Estadísticas finales
    console.print(f"\n[cyan]Estadísticas del dataset:[/cyan]")
    simple_count = sum(1 for qa in qa_list if qa.get("complexity") == "simple")
    complex_count = sum(1 for qa in qa_list if qa.get("complexity") == "complex")
    avg_confidence = sum(qa.get("confidence", 0.0) for qa in qa_list) / len(qa_list)
    
    console.print(f"  Simple: {simple_count} ({simple_count/len(qa_list)*100:.1f}%)")
    console.print(f"  Complejo: {complex_count} ({complex_count/len(qa_list)*100:.1f}%)")
    console.print(f"  Confianza promedio: {avg_confidence:.2f}")
    
    console.print(f"\n[bold green]✓ Dataset listo para fine-tuning[/bold green]")


if __name__ == "__main__":
    main()
