#!/usr/bin/env python3
"""
Parser de hojas de respuestas de exámenes oficiales
"""
import re
from pathlib import Path
from typing import Dict
from rich.console import Console

console = Console()

def parse_answer_sheet(file_path: str) -> Dict[int, str]:
    """
    Parsea hoja de respuestas
    
    Returns:
        {pregunta_num: respuesta_letra}
        Ejemplo: {1: "A", 2: "C", 3: "B", ...}
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    answers = {}
    
    # Patrón 1: "1 C" o "1  C" (número + espacios + letra)
    pattern1 = r'(\d+)\s+([A-D])\s'
    matches1 = re.findall(pattern1, content, re.IGNORECASE)
    
    for num, letter in matches1:
        answers[int(num)] = letter.upper()
    
    # Patrón 2: "1. A" o "1) A" o "1.- A"
    pattern2 = r'(\d+)[\.\)\-]+\s*([A-D])'
    matches2 = re.findall(pattern2, content, re.IGNORECASE)
    
    for num, letter in matches2:
        if int(num) not in answers:  # No sobrescribir si ya existe
            answers[int(num)] = letter.upper()
    
    # Patrón 3: "| 1 | C |" (formato tabla)
    pattern3 = r'\|\s*(\d+)\s*\|\s*([A-D])\s*\|'
    matches3 = re.findall(pattern3, content, re.IGNORECASE)
    
    for num, letter in matches3:
        if int(num) not in answers:
            answers[int(num)] = letter.upper()
    
    # Filtrar "ANULADA"
    filtered_answers = {}
    for num, letter in answers.items():
        if letter in ['A', 'B', 'C', 'D']:
            filtered_answers[num] = letter
    
    return filtered_answers

def main():
    import sys
    
    if len(sys.argv) < 2:
        console.print("[red]Uso: python parse_answer_sheet.py <archivo_respuestas.txt>[/red]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    console.print(f"[cyan]Parseando: {Path(file_path).name}[/cyan]")
    
    answers = parse_answer_sheet(file_path)
    
    console.print(f"\n[green]✓ {len(answers)} respuestas encontradas[/green]\n")
    
    # Mostrar primeras 10
    console.print("[bold]Primeras 10 respuestas:[/bold]")
    for i in range(1, min(11, len(answers) + 1)):
        if i in answers:
            console.print(f"  {i}. {answers[i]}")
    
    if len(answers) > 10:
        console.print(f"  ...")
        console.print(f"  {len(answers)}. {answers[len(answers)]}")

if __name__ == "__main__":
    main()
