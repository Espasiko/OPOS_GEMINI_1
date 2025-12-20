#!/usr/bin/env python3
"""
Empareja preguntas de exámenes con sus respuestas oficiales
"""
import re
import json
from pathlib import Path
from typing import List, Dict
from rich.console import Console
from rich.progress import track

# Importar parsers
import sys
sys.path.insert(0, str(Path(__file__).parent))
from parse_answer_sheet import parse_answer_sheet
from parse_exam_questions import parse_exam_questions

console = Console()

def extract_year(filename: str) -> int:
    """Extrae año del nombre del archivo"""
    match = re.search(r'20\d{2}', filename)
    return int(match.group()) if match else None

def extract_exam_type(filename: str) -> str:
    """Extrae tipo de examen del nombre"""
    filename_lower = filename.lower()
    
    if 'c1_ss' in filename_lower or 'examen_c1' in filename_lower:
        return 'C1_SS'
    elif 'gestion_libre' in filename_lower:
        return 'Gestión_Libre'
    elif 'gestion_pi' in filename_lower:
        return 'Gestión_PI'
    else:
        return 'Desconocido'

def pair_exam_with_answers(exam_file: str, answer_file: str) -> List[Dict]:
    """
    Empareja preguntas con respuestas
    
    Returns:
        Lista de Q&A completas con ground truth
    """
    console.print(f"\n[cyan]Emparejando:[/cyan]")
    console.print(f"  Examen: {Path(exam_file).name}")
    console.print(f"  Respuestas: {Path(answer_file).name}")
    
    # Parsear preguntas
    questions = parse_exam_questions(exam_file)
    console.print(f"  [green]✓ {len(questions)} preguntas parseadas[/green]")
    
    # Parsear respuestas
    answers = parse_answer_sheet(answer_file)
    console.print(f"  [green]✓ {len(answers)} respuestas parseadas[/green]")
    
    # Emparejar
    qa_pairs = []
    missing_answers = []
    
    for q in questions:
        num = q["num"]
        
        if num not in answers:
            missing_answers.append(num)
            continue
        
        qa_pairs.append({
            "id": f"{Path(exam_file).stem}_q{num}",
            "pregunta_num": num,
            "pregunta": q["pregunta"],
            "opciones": q["opciones"],
            "respuesta_correcta": answers[num],
            "respuesta_texto": q["opciones"][answers[num]],
            "examen": Path(exam_file).stem,
            "fuente": "BOE Oficial",
            "año": extract_year(exam_file),
            "tipo": extract_exam_type(exam_file),
            "verificado": True,
            "ground_truth": True
        })
    
    if missing_answers:
        console.print(f"  [yellow]⚠️  {len(missing_answers)} preguntas sin respuesta: {missing_answers[:5]}...[/yellow]")
    
    console.print(f"  [green]✓ {len(qa_pairs)} pares Q&A creados[/green]")
    
    return qa_pairs

def find_exam_answer_pairs(directory: str) -> List[tuple]:
    """
    Encuentra pares de exámenes y respuestas
    
    Returns:
        Lista de tuplas (exam_file, answer_file)
    """
    directory = Path(directory)
    pairs = []
    
    # Buscar archivos de respuestas
    answer_files = list(directory.glob("*respuesta*.txt"))
    
    for answer_file in answer_files:
        # Buscar examen correspondiente
        # Ejemplo: "01._respuestas_examen_c1_ss_26-03-2022.txt"
        # Buscar: "01._examen_c1_ss_26-03-2022.txt" o "01._examen_c1_ss_26-03-2022_ocr.txt"
        
        answer_name = answer_file.name
        
        # Remover "respuestas_" del nombre
        exam_name = answer_name.replace("respuestas_", "")
        
        # PRIORIDAD 1: Buscar archivo _ocr_improved (mejor calidad)
        exam_name_improved = exam_name.replace(".txt", "_ocr_improved.txt")
        exam_file = directory / exam_name_improved
        
        # PRIORIDAD 2: Si no existe, intentar con _ocr
        if not exam_file.exists():
            exam_name_ocr = exam_name.replace(".txt", "_ocr.txt")
            exam_file = directory / exam_name_ocr
        
        # PRIORIDAD 3: Si tampoco existe, archivo sin sufijo
        if not exam_file.exists():
            exam_file = directory / exam_name
        
        if exam_file.exists():
            pairs.append((str(exam_file), str(answer_file)))
        else:
            console.print(f"[yellow]⚠️  No se encontró examen para: {answer_file.name}[/yellow]")
    
    return pairs

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Empareja exámenes con respuestas")
    parser.add_argument("--input", required=True, help="Directorio con exámenes y respuestas")
    parser.add_argument("--output", required=True, help="Archivo JSONL de salida")
    
    args = parser.parse_args()
    
    console.print("[bold blue]🔗 Emparejador de Preguntas y Respuestas[/bold blue]\n")
    
    # Encontrar pares
    pairs = find_exam_answer_pairs(args.input)
    console.print(f"[green]✓ {len(pairs)} pares de exámenes encontrados[/green]\n")
    
    # Procesar cada par
    all_qa_pairs = []
    
    for exam_file, answer_file in track(pairs, description="Procesando exámenes"):
        try:
            qa_pairs = pair_exam_with_answers(exam_file, answer_file)
            all_qa_pairs.extend(qa_pairs)
        except Exception as e:
            console.print(f"[red]❌ Error en {Path(exam_file).name}: {e}[/red]")
    
    # Guardar en JSONL
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for qa in all_qa_pairs:
            f.write(json.dumps(qa, ensure_ascii=False) + '\n')
    
    console.print(f"\n[bold green]✓ Emparejamiento completado[/bold green]")
    console.print(f"  Total Q&A: {len(all_qa_pairs)}")
    console.print(f"  Guardado en: {output_path}")
    
    # Estadísticas
    years = {}
    types = {}
    for qa in all_qa_pairs:
        year = qa.get('año')
        tipo = qa.get('tipo')
        if year:  # Filtrar None
            years[year] = years.get(year, 0) + 1
        types[tipo] = types.get(tipo, 0) + 1
    
    console.print(f"\n[bold]Estadísticas:[/bold]")
    console.print(f"  Por año: {dict(sorted(years.items()))}")
    console.print(f"  Por tipo: {types}")

if __name__ == "__main__":
    main()
