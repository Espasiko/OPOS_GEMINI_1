#!/usr/bin/env python3
"""
Parser de exámenes oficiales (preguntas + opciones)
"""
import re
from pathlib import Path
from typing import List, Dict
from rich.console import Console

console = Console()

def parse_exam_questions(file_path: str) -> List[Dict]:
    """
    Parsea examen y extrae preguntas con opciones
    
    Returns:
        Lista de diccionarios con estructura:
        {
            "num": 1,
            "pregunta": "¿Cuál es...",
            "opciones": {"A": "...", "B": "...", "C": "...", "D": "..."}
        }
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    questions = []
    
    # Patrón MEJORADO V2 - Non-greedy y mejor delimitación
    # Captura hasta el siguiente número de pregunta o marcador
    # Usa *? (non-greedy) para evitar capturar texto extra
    pattern = r'(\d+)[\.\)]\s+(.+?)[\n\r]+\s*[Aa][\)\.]?\s*(.+?)[\n\r]+\s*[Bb][\)\.]?\s*(.+?)[\n\r]+\s*[Cc][\)\.]?\s*(.+?)[\n\r]+\s*[Dd][\)\.]?\s*(.+?)(?=[\n\r]+\s*(?:\d+[\.\)]|PREGUNTA|GAL|---|PÁGINA|$))'
    
    matches = re.findall(pattern, content, re.DOTALL | re.MULTILINE)
    
    console.print(f"[yellow]Debug: {len(matches)} matches encontrados con regex[/yellow]")
    
    for match in matches:
        num, pregunta, opt_a, opt_b, opt_c, opt_d = match
        
        # Limpiar texto (eliminar saltos de línea extra y espacios)
        pregunta = ' '.join(pregunta.split())
        opt_a = ' '.join(opt_a.split())
        opt_b = ' '.join(opt_b.split())
        opt_c = ' '.join(opt_c.split())
        opt_d = ' '.join(opt_d.split())
        
        # Limpiar opciones: cortar en el siguiente número de pregunta si existe
        for opt_name, opt_text in [('A', opt_a), ('B', opt_b), ('C', opt_c), ('D', opt_d)]:
            # Si encuentra "10." o similar al final, cortar ahí
            match_next = re.search(r'\s+\d+[\.\)]\s', opt_text)
            if match_next:
                if opt_name == 'A':
                    opt_a = opt_text[:match_next.start()].strip()
                elif opt_name == 'B':
                    opt_b = opt_text[:match_next.start()].strip()
                elif opt_name == 'C':
                    opt_c = opt_text[:match_next.start()].strip()
                elif opt_name == 'D':
                    opt_d = opt_text[:match_next.start()].strip()
        
        # Filtrar preguntas muy cortas
        if len(pregunta) < 10:
            console.print(f"[yellow]Filtrado: Pregunta {num} muy corta ({len(pregunta)} chars)[/yellow]")
            continue
        
        # Filtrar opciones muy largas (ahora con límite más alto)
        max_len = max(len(opt_a), len(opt_b), len(opt_c), len(opt_d))
        if max_len > 1500:  # Aumentado de 800 a 1500
            console.print(f"[yellow]Filtrado: Pregunta {num} con opción muy larga ({max_len} chars)[/yellow]")
            continue
        
        # Filtrar si alguna opción está vacía
        if not all([opt_a.strip(), opt_b.strip(), opt_c.strip(), opt_d.strip()]):
            console.print(f"[yellow]Filtrado: Pregunta {num} con opción vacía[/yellow]")
            continue
        
        questions.append({
            "num": int(num),
            "pregunta": pregunta,
            "opciones": {
                "A": opt_a,
                "B": opt_b,
                "C": opt_c,
                "D": opt_d
            }
        })
    
    return questions

def main():
    import sys
    
    if len(sys.argv) < 2:
        console.print("[red]Uso: python parse_exam_questions.py <archivo_examen.txt>[/red]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    console.print(f"[cyan]Parseando: {Path(file_path).name}[/cyan]")
    
    questions = parse_exam_questions(file_path)
    
    console.print(f"\n[green]✓ {len(questions)} preguntas encontradas[/green]\n")
    
    # Mostrar primera pregunta
    if questions:
        console.print("[bold]Primera pregunta:[/bold]")
        q = questions[0]
        console.print(f"\n{q['num']}. {q['pregunta'][:100]}...")
        console.print(f"\nA) {q['opciones']['A'][:50]}...")
        console.print(f"B) {q['opciones']['B'][:50]}...")
        console.print(f"C) {q['opciones']['C'][:50]}...")
        console.print(f"D) {q['opciones']['D'][:50]}...")

if __name__ == "__main__":
    main()
