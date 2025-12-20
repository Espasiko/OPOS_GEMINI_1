#!/usr/bin/env python3
"""
Extrae texto de PDFs escaneados usando OCR (Tesseract)
"""
import pytesseract
from pdf2image import convert_from_path
from pathlib import Path
import sys
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
    # PDFs fallidos (requieren OCR)
    failed_pdfs = [
        "10._examen_c1_pi_parte_2_noviembre_2024.pdf",
        "04._examen_c1_3-4-23.pdf",
        "02._gestion_libre_2022.pdf",
        "10._examen_c1_pi_parte_1_noviembre_2024.pdf",
        "09._examen_c1_parte_2_noviembre_2024.pdf",
        "09._examen_c1_parte_1_noviembre_2024.pdf",
        "03._gestion_pi_2022.pdf",
        "01._examen_c1_ss_26-03-2022.pdf"
    ]
    
    base_dir = "basura/del_ordenador/de_mi_hija/bajados_academia"
    output_dir = "extracted_texts/examenes_oficiales"
    
    console.print("[bold blue]🔍 Extractor OCR de PDFs Escaneados[/bold blue]\n")
    console.print(f"Total PDFs a procesar: {len(failed_pdfs)}\n")
    
    success = 0
    failed = 0
    
    for pdf in failed_pdfs:
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
