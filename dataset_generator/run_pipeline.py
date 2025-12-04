#!/usr/bin/env python3
"""
Script todo-en-uno para ejecutar el pipeline completo.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()


def run_command(cmd: list, description: str):
    """Ejecuta un comando y muestra el resultado."""
    console.print(f"\n[bold blue]→ {description}[/bold blue]")
    console.print(f"[dim]{' '.join(cmd)}[/dim]\n")
    
    result = subprocess.run(cmd, capture_output=False)
    
    if result.returncode != 0:
        console.print(f"[bold red]✗ Error en: {description}[/bold red]")
        sys.exit(1)
    
    console.print(f"[bold green]✓ Completado: {description}[/bold green]")


def main():
    parser = argparse.ArgumentParser(description="Pipeline completo de generación de dataset")
    parser.add_argument("--input", required=True, help="Directorio con PDFs o textos")
    parser.add_argument("--output-dir", default="output", help="Directorio de salida")
    parser.add_argument("--skip-extract", action="store_true", 
                       help="Saltar extracción (si ya tienes .txt)")
    parser.add_argument("--skip-verify", action="store_true",
                       help="Saltar verificación")
    parser.add_argument("--skip-url-check", action="store_true",
                       help="Saltar verificación de URLs")
    
    args = parser.parse_args()
    
    # Banner
    console.print(Panel.fit(
        "[bold blue]🚀 Pipeline de Generación de Dataset Q&A[/bold blue]\n"
        "[cyan]Multi-agente con verificación automática[/cyan]",
        border_style="blue"
    ))
    
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Determinar si son PDFs o textos
    has_pdfs = list(input_path.glob("**/*.pdf"))
    has_txts = list(input_path.glob("**/*.txt"))
    
    txt_dir = input_path if has_txts else output_dir / "data_txt"
    
    # PASO 1: Extracción (si es necesario)
    if has_pdfs and not args.skip_extract:
        txt_dir.mkdir(parents=True, exist_ok=True)
        run_command(
            ["python", "extract_text.py", "--input", str(input_path), "--output", str(txt_dir)],
            "Extrayendo texto de PDFs"
        )
    
    # PASO 2: Generación de Q&A
    qa_raw_path = output_dir / "qa_raw.json"
    run_command(
        ["python", "generate_qa.py", "--input", str(txt_dir), "--output", str(qa_raw_path)],
        "Generando Q&A con multi-agente"
    )
    
    # PASO 3: Verificación (opcional)
    if not args.skip_verify:
        qa_verified_path = output_dir / "qa_verified.json"
        run_command(
            ["python", "verify_qa.py", "--input", str(qa_raw_path), "--output", str(qa_verified_path)],
            "Verificando calidad de Q&A"
        )
        final_qa = qa_verified_path
    else:
        final_qa = qa_raw_path
    
    # PASO 4: Verificación de URLs (nuevo)
    if not args.skip_url_check:
        qa_url_verified_path = output_dir / "qa_url_verified.jsonl"
        # Convertir a JSONL si es necesario
        if str(final_qa).endswith('.json'):
            import json
            with open(final_qa, 'r', encoding='utf-8') as f:
                data = json.load(f)
            temp_jsonl = output_dir / "temp.jsonl"
            with open(temp_jsonl, 'w', encoding='utf-8') as f:
                for item in data:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
            final_qa = temp_jsonl
        
        run_command(
            ["python", "url_verifier.py", str(final_qa), "-o", str(qa_url_verified_path)],
            "Verificando URLs en Q&A"
        )
        final_qa = qa_url_verified_path
    
    # PASO 5: Exportación
    dataset_path = output_dir / "dataset_final.jsonl"
    run_command(
        ["python", "export_dataset.py", "--input", str(final_qa), "--output", str(dataset_path), "--split"],
        "Exportando dataset para fine-tuning"
    )
    
    # Resumen final
    console.print("\n" + "="*60)
    console.print(Panel.fit(
        f"[bold green]✓ Pipeline completado exitosamente[/bold green]\n\n"
        f"[cyan]Archivos generados:[/cyan]\n"
        f"  • Dataset train: {output_dir}/dataset_final_train.jsonl\n"
        f"  • Dataset val: {output_dir}/dataset_final_val.jsonl\n"
        f"  • Dataset test: {output_dir}/dataset_final_test.jsonl\n\n"
        f"[yellow]Siguiente paso:[/yellow]\n"
        f"  Usa estos archivos para fine-tuning de Mistral 7B",
        border_style="green"
    ))


if __name__ == "__main__":
    main()
