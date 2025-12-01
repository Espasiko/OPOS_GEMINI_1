#!/usr/bin/env python3
"""
Extrae texto de PDFs y documentos para procesamiento posterior.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List
import PyPDF2
import pdfplumber
from rich.console import Console
from rich.progress import track

console = Console()


def extract_text_pypdf2(pdf_path: str) -> str:
    """Extrae texto usando PyPDF2 (rápido pero menos preciso)."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n\n"
            return text.strip()
    except Exception as e:
        console.print(f"[red]Error con PyPDF2 en {pdf_path}: {e}[/red]")
        return ""


def extract_text_pdfplumber(pdf_path: str) -> str:
    """Extrae texto usando pdfplumber (más preciso, maneja tablas)."""
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
                
                # Extraer tablas si existen
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        text += " | ".join([str(cell) if cell else "" for cell in row]) + "\n"
                    text += "\n"
        
        return text.strip()
    except Exception as e:
        console.print(f"[red]Error con pdfplumber en {pdf_path}: {e}[/red]")
        return ""


def clean_text(text: str) -> str:
    """Limpia y normaliza el texto extraído."""
    # Eliminar múltiples espacios
    text = " ".join(text.split())
    
    # Eliminar múltiples saltos de línea
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    text = "\n\n".join(lines)
    
    return text


def extract_from_pdf(pdf_path: str, method: str = "pdfplumber") -> str:
    """Extrae texto de un PDF usando el método especificado."""
    if method == "pdfplumber":
        text = extract_text_pdfplumber(pdf_path)
    else:
        text = extract_text_pypdf2(pdf_path)
    
    return clean_text(text) if text else ""


def process_directory(input_dir: str, output_dir: str, method: str = "pdfplumber"):
    """Procesa todos los PDFs en un directorio."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Buscar todos los PDFs
    pdf_files = list(input_path.glob("**/*.pdf"))
    
    if not pdf_files:
        console.print(f"[yellow]No se encontraron PDFs en {input_dir}[/yellow]")
        return
    
    console.print(f"[green]Encontrados {len(pdf_files)} PDFs[/green]")
    
    # Procesar cada PDF
    for pdf_file in track(pdf_files, description="Extrayendo texto..."):
        try:
            # Extraer texto
            text = extract_from_pdf(str(pdf_file), method)
            
            if not text:
                console.print(f"[yellow]Sin texto extraído de {pdf_file.name}[/yellow]")
                continue
            
            # Guardar como .txt
            output_file = output_path / f"{pdf_file.stem}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            console.print(f"[green]✓[/green] {pdf_file.name} → {output_file.name} ({len(text)} chars)")
            
        except Exception as e:
            console.print(f"[red]Error procesando {pdf_file.name}: {e}[/red]")
    
    console.print(f"\n[bold green]✓ Extracción completada[/bold green]")


def main():
    parser = argparse.ArgumentParser(description="Extrae texto de PDFs")
    parser.add_argument("--input", required=True, help="Directorio con PDFs")
    parser.add_argument("--output", required=True, help="Directorio para textos")
    parser.add_argument("--method", default="pdfplumber", choices=["pdfplumber", "pypdf2"],
                       help="Método de extracción")
    
    args = parser.parse_args()
    
    console.print("[bold blue]🔍 Extractor de Texto de PDFs[/bold blue]\n")
    process_directory(args.input, args.output, args.method)


if __name__ == "__main__":
    main()
