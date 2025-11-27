"""
Verificar PDF de la Constitución
"""
import pypdf
from pathlib import Path

pdf_path = Path("backend/data/leyes/BOE-151_Constitucion_Espanola.pdf")

print(f"Archivo: {pdf_path}")
print(f"Tamaño: {pdf_path.stat().st_size / (1024*1024):.2f} MB")

pdf = pypdf.PdfReader(pdf_path)
print(f"Páginas: {len(pdf.pages)}")
print(f"\nPrimera página:")
print(pdf.pages[0].extract_text()[:500])
