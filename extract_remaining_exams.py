#!/usr/bin/env python3
"""
Extrae los 6 exámenes faltantes con OCR
"""
import pytesseract
from pdf2image import convert_from_path
from pathlib import Path
from rich.console import Console
from rich.progress import track

console = Console()

def extract_pdf_with_ocr(pdf_path: str, output_dir: str):
    """Extrae texto de PDF escaneado usando OCR"""
    
    pdf_name = Path(pdf_path).name
    console.print(f"[cyan]Procesando {pdf_name} con OCR...[/cyan]")
    
    try:
        # Convertir PDF a imágenes (DPI 300 para mejor calidad)
        images = convert_from_path(pdf_path, dpi=300)
        console.print(f"  Convertido a {len(images)} imágenes")
        
        # Extraer texto de cada página
        full_text = ""
        for i, image in enumerate(track(images, description="  Extrayendo texto"), 1):
            text = pytesseract.image_to_string(image, lang='spa')
            full_text += f"\n\n--- PÁGINA {i} ---\n\n{text}"
        
        # Guardar
        output_file = Path(output_dir) / f"{Path(pdf_path).stem}_ocr.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        console.print(f"[green]✓ {output_file.name} ({len(full_text)} chars)[/green]")
        return full_text
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        return None

def main():
    # PDFs faltantes (sin OCR previo)
    remaining_pdfs = [
        "05._gestion_libre_2023.pdf",
        "06._gestion_pi_2023.pdf",
        "07._gestion_pi_extraordinaria_2023.pdf",
        "08._gestion_libre_extraordinaria_2023.pdf",
        "11._examen_c1_pi_extraord_enero_25.pdf",
        "12._examen_c1_extraord_enero_25.pdf"
    ]
    
    base_dir = "basura/del_ordenador/de_mi_hija/bajados_academia"
    output_dir = "extracted_texts/examenes_oficiales"
    
    console.print("[bold blue]🔍 Extractor OCR - Exámenes Faltantes[/bold blue]\n")
    console.print(f"Total PDFs a procesar: {len(remaining_pdfs)}\n")
    
    success = 0
    failed = 0
    
    for pdf in remaining_pdfs:
        pdf_path = f"{base_dir}/{pdf}"
        
        if not Path(pdf_path).exists():
            console.print(f"[yellow]⚠️  No encontrado: {pdf}[/yellow]")
            continue
        
        result = extract_pdf_with_ocr(pdf_path, output_dir)
        if result:
            success += 1
        else:
            failed += 1
    
    console.print(f"\n[bold green]✓ Extracción completada[/bold green]")
    console.print(f"  Exitosos: {success}")
    console.print(f"  Fallidos: {failed}")

if __name__ == "__main__":
    main()
