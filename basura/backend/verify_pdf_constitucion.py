"""
Verificar contenido del PDF de la Constitución
"""
import pypdf
from pathlib import Path

# Verificar ambos PDFs
pdfs = [
    "backend/data/leyes/BOE-151_Constitucion_Espanola.pdf",
    "backend/data/leyes/Constitución_Española.pdf"
]

for pdf_path_str in pdfs:
    pdf_path = Path(pdf_path_str)
    
    if not pdf_path.exists():
        print(f"❌ No existe: {pdf_path}")
        continue
    
    print(f"\n{'='*80}")
    print(f"📄 Archivo: {pdf_path.name}")
    print(f"📊 Tamaño: {pdf_path.stat().st_size / (1024*1024):.2f} MB")
    
    try:
        pdf = pypdf.PdfReader(pdf_path)
        print(f"📑 Páginas: {len(pdf.pages)}")
        
        # Buscar artículo 168
        found_168 = False
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if "168" in text and ("Artículo" in text or "artículo" in text):
                print(f"\n✅ Artículo 168 encontrado en página {i+1}")
                # Extraer contexto
                lines = text.split('\n')
                for j, line in enumerate(lines):
                    if "168" in line:
                        context_start = max(0, j-2)
                        context_end = min(len(lines), j+10)
                        print("\nContexto:")
                        print('\n'.join(lines[context_start:context_end]))
                        found_168 = True
                        break
                if found_168:
                    break
        
        if not found_168:
            print(f"\n❌ Artículo 168 NO encontrado en este PDF")
            
    except Exception as e:
        print(f"❌ Error leyendo PDF: {e}")

print(f"\n{'='*80}")
