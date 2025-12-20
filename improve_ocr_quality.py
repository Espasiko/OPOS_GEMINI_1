#!/usr/bin/env python3
"""
Mejora calidad OCR con preprocesamiento de imágenes
"""
import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter
from pathlib import Path
from rich.console import Console
from rich.progress import track

console = Console()

def preprocess_image(image):
    """
    Mejora calidad de imagen para OCR
    
    Aplica:
    - Conversión a escala de grises
    - Aumento de contraste
    - Binarización
    - Reducción de ruido
    """
    # Convertir a escala de grises
    image = image.convert('L')
    
    # Aumentar contraste
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    
    # Aumentar nitidez
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(1.5)
    
    # Binarización (Otsu threshold)
    # Convertir a blanco y negro puro
    threshold = 128
    image = image.point(lambda p: 255 if p > threshold else 0)
    
    # Reducir ruido con filtro de mediana
    image = image.filter(ImageFilter.MedianFilter(size=3))
    
    return image

def extract_pdf_with_improved_ocr(pdf_path: str, output_dir: str):
    """Extrae texto con OCR mejorado"""
    
    pdf_name = Path(pdf_path).name
    console.print(f"\n[cyan]Procesando {pdf_name} con OCR MEJORADO...[/cyan]")
    
    try:
        # Convertir PDF a imágenes (DPI 300 para mejor calidad)
        console.print("  [yellow]Convirtiendo PDF a imágenes (DPI 300)...[/yellow]")
        images = convert_from_path(pdf_path, dpi=300)
        console.print(f"  [green]✓ {len(images)} imágenes convertidas[/green]")
        
        # Extraer texto de cada página con preprocesamiento
        full_text = ""
        
        for i, image in enumerate(track(images, description="  Extrayendo con OCR mejorado"), 1):
            # Preprocesar imagen
            image_clean = preprocess_image(image)
            
            # OCR con configuración optimizada
            # --oem 3: LSTM neural net mode (mejor para texto moderno)
            # --psm 6: Assume a single uniform block of text
            custom_config = r'--oem 3 --psm 6 -c preserve_interword_spaces=1'
            
            text = pytesseract.image_to_string(
                image_clean, 
                lang='spa',
                config=custom_config
            )
            
            full_text += f"\n\n--- PÁGINA {i} ---\n\n{text}"
        
        # Guardar
        output_file = Path(output_dir) / f"{Path(pdf_path).stem}_ocr_improved.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        console.print(f"[bold green]✓ {output_file.name} ({len(full_text)} chars)[/bold green]")
        
        # Verificar calidad
        if "JRIJR" in full_text or "RIJR" in full_text:
            console.print(f"[yellow]⚠️  Aún hay ruido en el texto[/yellow]")
            return None
        else:
            console.print(f"[green]✓ Texto limpio (sin ruido detectado)[/green]")
            return full_text
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        return None

def main():
    # PDFs con OCR corrupto
    problematic_pdfs = [
        "05._gestion_libre_2023.pdf",
        "06._gestion_pi_2023.pdf",
        "07._gestion_pi_extraordinaria_2023.pdf",
        "08._gestion_libre_extraordinaria_2023.pdf",
        "11._examen_c1_pi_extraord_enero_25.pdf",
        "12._examen_c1_extraord_enero_25.pdf"
    ]
    
    base_dir = "basura/del_ordenador/de_mi_hija/bajados_academia"
    output_dir = "extracted_texts/examenes_oficiales"
    
    console.print("[bold blue]🔧 Mejora de Calidad OCR[/bold blue]")
    console.print("[bold]Preprocesamiento: Contraste + Binarización + Denoising[/bold]\n")
    console.print(f"Total PDFs a procesar: {len(problematic_pdfs)}\n")
    
    success = 0
    failed = 0
    failed_files = []
    
    for pdf in problematic_pdfs:
        pdf_path = f"{base_dir}/{pdf}"
        
        if not Path(pdf_path).exists():
            console.print(f"[yellow]⚠️  No encontrado: {pdf}[/yellow]")
            continue
        
        result = extract_pdf_with_improved_ocr(pdf_path, output_dir)
        if result:
            success += 1
        else:
            failed += 1
            failed_files.append(pdf)
    
    console.print(f"\n[bold]{'='*60}[/bold]")
    console.print(f"[bold green]✓ Extracción completada[/bold green]")
    console.print(f"  Exitosos: {success}")
    console.print(f"  Fallidos: {failed}")
    
    if failed_files:
        console.print(f"\n[yellow]⚠️  Archivos que requieren extracción manual:[/yellow]")
        for f in failed_files:
            console.print(f"    - {f}")

if __name__ == "__main__":
    main()
