"""
PDF Processor - Extrae y chunkea texto de PDFs legales
"""
import re
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
import pypdf

@dataclass
class Chunk:
    """Representa un chunk de texto procesado"""
    text: str
    articulo: Optional[str] = None
    page_num: int = 0
    chunk_id: int = 0
    total_chunks: int = 0

class PDFProcessor:
    """Procesa PDFs del BOE y extrae chunks inteligentes"""
    
    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
        
        # Patrones para detectar artículos
        self.articulo_patterns = [
            r'Artículo\s+(\d+[a-z]?)\.',
            r'Art\.\s+(\d+[a-z]?)\.',
            r'ARTÍCULO\s+(\d+[a-z]?)\.',
        ]
    
    def extract_text_from_pdf(self, pdf_path: Path) -> List[Dict]:
        """Extrae texto de PDF página por página"""
        print(f"📖 Extrayendo texto de: {pdf_path.name}")
        
        pages = []
        with open(pdf_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()
                
                if text.strip():
                    pages.append({
                        'page_num': page_num,
                        'text': text,
                        'total_pages': total_pages
                    })
                
                if page_num % 50 == 0:
                    print(f"   Procesadas {page_num}/{total_pages} páginas...")
        
        print(f"✅ {len(pages)} páginas extraídas")
        return pages
    
    def detect_articulo(self, text: str) -> Optional[str]:
        """Detecta número de artículo en el texto"""
        for pattern in self.articulo_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None
    
    def clean_text(self, text: str) -> str:
        """Limpia texto extraído del PDF"""
        # Eliminar saltos de línea múltiples
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Eliminar espacios múltiples
        text = re.sub(r' {2,}', ' ', text)
        
        # Eliminar guiones de separación de palabras
        text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
        
        return text.strip()
    
    def create_chunks(self, pages: List[Dict]) -> List[Chunk]:
        """Crea chunks respetando estructura de artículos"""
        print(f"✂️  Creando chunks (tamaño: {self.chunk_size}, overlap: {self.overlap})...")
        
        chunks = []
        current_articulo = None
        
        for page_data in pages:
            text = self.clean_text(page_data['text'])
            page_num = page_data['page_num']
            
            # Detectar artículo en esta página
            articulo = self.detect_articulo(text)
            if articulo:
                current_articulo = articulo
            
            # Dividir en chunks
            words = text.split()
            
            for i in range(0, len(words), self.chunk_size - self.overlap):
                chunk_words = words[i:i + self.chunk_size]
                chunk_text = ' '.join(chunk_words)
                
                if len(chunk_text.strip()) > 50:  # Mínimo 50 caracteres
                    chunks.append(Chunk(
                        text=chunk_text,
                        articulo=current_articulo,
                        page_num=page_num,
                        chunk_id=len(chunks) + 1
                    ))
        
        # Actualizar total_chunks
        total = len(chunks)
        for chunk in chunks:
            chunk.total_chunks = total
        
        print(f"✅ {total} chunks creados")
        return chunks
    
    def process_pdf(self, pdf_path: Path) -> List[Chunk]:
        """Procesa un PDF completo"""
        print(f"\n{'='*60}")
        print(f"🔄 PROCESANDO: {pdf_path.name}")
        print(f"{'='*60}\n")
        
        # Extraer texto
        pages = self.extract_text_from_pdf(pdf_path)
        
        # Crear chunks
        chunks = self.create_chunks(pages)
        
        print(f"\n📊 Resumen:")
        print(f"   - Páginas: {len(pages)}")
        print(f"   - Chunks: {len(chunks)}")
        print(f"   - Artículos detectados: {len(set(c.articulo for c in chunks if c.articulo))}")
        
        return chunks

if __name__ == "__main__":
    # Test con LGSS
    processor = PDFProcessor(chunk_size=512, overlap=50)
    
    lgss_path = Path("backend/data/leyes/LGSS.pdf")
    
    if lgss_path.exists():
        chunks = processor.process_pdf(lgss_path)
        
        # Mostrar ejemplos
        print(f"\n{'='*60}")
        print("📝 EJEMPLOS DE CHUNKS:")
        print(f"{'='*60}\n")
        
        for i, chunk in enumerate(chunks[:3], 1):
            print(f"Chunk {i}:")
            print(f"  Artículo: {chunk.articulo or 'N/A'}")
            print(f"  Página: {chunk.page_num}")
            print(f"  Texto: {chunk.text[:200]}...")
            print()
    else:
        print(f"❌ No se encontró {lgss_path}")
        print("   Ejecuta primero: python backend/agents/download_lgss_only.py")
