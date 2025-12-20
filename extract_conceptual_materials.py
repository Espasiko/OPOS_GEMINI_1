#!/usr/bin/env python3
"""
Extractor OCR para materiales conceptuales (esquemas, mapas mentales)
"""
import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter
from pathlib import Path
from rich.console import Console
from rich.progress import track
import sys

console = Console()

def preprocess_image(image):
    """Mejora calidad de imagen para OCR de esquemas"""
    try:
        # Convertir a escala de grises
        image = image.convert('L')
        
        # Aumentar contraste (más agresivo para esquemas)
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.5)
        
        # Aumentar nitidez
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(2.0)
        
        # Binarización
        threshold = 140
        image = image.point(lambda p: 255 if p > threshold else 0)
        
        # Reducir ruido
        image = image.filter(ImageFilter.MedianFilter(size=3))
        
        return image
    except Exception as e:
        console.print(f"[red]Error en preprocesamiento: {e}[/red]")
        return image

def extract_conceptual_pdf(pdf_path: str, output_dir: str):
    """Extrae texto de PDF conceptual con OCR optimizado"""
    
    pdf_name = Path(pdf_path).name
    console.print(f"\n[cyan]📄 Procesando {pdf_name}...[/cyan]")
    
    try:
        # Convertir PDF a imágenes (DPI 300)
        console.print("  [yellow]Convirtiendo a imágenes...[/yellow]")
        images = convert_from_path(pdf_path, dpi=300)
        console.print(f"  [green]✓ {len(images)} páginas[/green]")
        
        # Extraer texto
        full_text = ""
        
        for i, image in enumerate(track(images, description="  Extrayendo"), 1):
            try:
                # Preprocesar
                image_clean = preprocess_image(image)
                
                # OCR con configuración optimizada para esquemas
                # PSM 6 = Assume a single uniform block of text
                custom_config = r'--oem 3 --psm 6 -c preserve_interword_spaces=1'
                text = pytesseract.image_to_string(
                    image_clean, 
                    lang='spa',
                    config=custom_config
                )
                
                full_text += f"\n\n--- PÁGINA {i} ---\n\n{text}"
            except Exception as e:
                console.print(f"[yellow]⚠️  Error en página {i}: {e}[/yellow]")
                continue
        
        # Guardar
        output_file = Path(output_dir) / f"{Path(pdf_path).stem}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        console.print(f"[bold green]✓ {output_file.name} ({len(full_text):,} chars)[/bold green]")
        
        return full_text
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        import traceback
        traceback.print_exc()
        return None

def main():
    pdf_dir = Path("conceptual_materials/pdfs")
    output_dir = Path("conceptual_materials/extracted_texts")
    
    # Crear directorio de salida
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Obtener lista de PDFs
    pdfs = sorted(pdf_dir.glob("*.pdf"))
    
    console.print(f"[bold blue]🔍 Extractor OCR - Materiales Conceptuales[/bold blue]\n")
    console.print(f"Total PDFs: {len(pdfs)}\n")
    
    success = 0
    failed = 0
    total_chars = 0
    
    for pdf in pdfs:
        result = extract_conceptual_pdf(str(pdf), str(output_dir))
        if result:
            success += 1
            total_chars += len(result)
        else:
            failed += 1
    
    console.print(f"\n[bold]{'='*60}[/bold]")
    console.print(f"[bold green]✓ Extracción completada[/bold green]")
    console.print(f"  Exitosos: {success}")
    console.print(f"  Fallidos: {failed}")
    console.print(f"  Total caracteres: {total_chars:,}")
    console.print(f"  Promedio por archivo: {total_chars//success if success > 0 else 0:,} chars")

if __name__ == "__main__":
    main()
