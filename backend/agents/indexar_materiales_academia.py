#!/usr/bin/env python3
"""
Indexa materiales de academia en Qdrant local con BGE-M3
Anonimiza datos sensibles antes de indexar
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict
import PyPDF2
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from FlagEmbedding import BGEM3FlagModel

# Añadir el directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

class AcademyMaterialsIndexer:
    def __init__(self):
        # Conectar a Qdrant local
        self.qdrant = QdrantClient(host="localhost", port=6333)
        
        # Cargar modelo BGE-M3
        print("🔄 Cargando modelo BGE-M3...")
        self.model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)
        print("✅ Modelo BGE-M3 cargado")
        
        self.collection_name = "materiales_academia"
        self.chunk_size = 500  # Caracteres por chunk
        self.chunk_overlap = 50
        
    def anonymize_text(self, text: str) -> str:
        """Anonimiza datos sensibles del texto"""
        # Nombres propios (patrón simple: palabras capitalizadas seguidas)
        text = re.sub(r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*\b', '[NOMBRE]', text)
        
        # DNI/NIE
        text = re.sub(r'\b\d{8}[A-Z]\b', '[DNI]', text)
        text = re.sub(r'\b[XYZ]\d{7}[A-Z]\b', '[NIE]', text)
        
        # Números de teléfono
        text = re.sub(r'\b[6-9]\d{8}\b', '[TELEFONO]', text)
        text = re.sub(r'\b\+34\s*[6-9]\d{8}\b', '[TELEFONO]', text)
        
        # Emails
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        
        # Números de Seguridad Social
        text = re.sub(r'\b\d{12}\b', '[NUM_SS]', text)
        
        # Direcciones (patrón simple)
        text = re.sub(r'\b(?:Calle|C/|Avenida|Avda|Plaza|Pl\.)\s+[^,\n]+(?:,\s*\d+)?', '[DIRECCION]', text)
        
        # Códigos postales
        text = re.sub(r'\b\d{5}\b', '[CP]', text)
        
        # Nombres de academias específicas (añade más si es necesario)
        academias = ['Las Cortes', 'GoKoan', 'OpoEsquemas', 'Academia Adams']
        for academia in academias:
            text = re.sub(rf'\b{academia}\b', '[ACADEMIA]', text, flags=re.IGNORECASE)
        
        return text
    
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extrae texto de un PDF"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"⚠️  Error procesando {pdf_path.name}: {e}")
            return ""
    
    def chunk_text(self, text: str, metadata: Dict) -> List[Dict]:
        """Divide texto en chunks con metadata"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            
            # Intentar cortar en punto o salto de línea
            if end < len(text):
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                cut_point = max(last_period, last_newline)
                if cut_point > self.chunk_size * 0.7:  # Al menos 70% del chunk
                    end = start + cut_point + 1
                    chunk = text[start:end]
            
            if chunk.strip():
                chunks.append({
                    'text': chunk.strip(),
                    'metadata': {**metadata, 'chunk_index': len(chunks)}
                })
            
            start = end - self.chunk_overlap
        
        return chunks
    
    def create_collection(self):
        """Crea colección en Qdrant"""
        try:
            self.qdrant.delete_collection(self.collection_name)
            print(f"🗑️  Colección '{self.collection_name}' eliminada")
        except:
            pass
        
        self.qdrant.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
        )
        print(f"✅ Colección '{self.collection_name}' creada")
    
    def index_materials(self, materials_dir: str):
        """Indexa todos los materiales de academia"""
        materials_path = Path(materials_dir)
        
        # Crear colección
        self.create_collection()
        
        # Buscar todos los PDFs
        pdf_files = list(materials_path.rglob("*.pdf"))
        print(f"\n📚 Encontrados {len(pdf_files)} archivos PDF")
        
        total_chunks = 0
        points = []
        point_id = 0
        
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"\n[{i}/{len(pdf_files)}] Procesando: {pdf_file.name}")
            
            # Extraer texto
            text = self.extract_text_from_pdf(pdf_file)
            if not text:
                continue
            
            # Anonimizar
            text_anonymized = self.anonymize_text(text)
            
            # Metadata
            metadata = {
                'source': 'academia',
                'filename': pdf_file.name,
                'relative_path': str(pdf_file.relative_to(materials_path)),
                'type': self._classify_document(pdf_file.name)
            }
            
            # Crear chunks
            chunks = self.chunk_text(text_anonymized, metadata)
            print(f"  📄 {len(chunks)} chunks creados")
            
            # Generar embeddings y crear points
            for chunk in chunks:
                try:
                    # Generar embedding con BGE-M3
                    embedding = self.model.encode([chunk['text']])['dense_vecs'][0]
                    
                    point = PointStruct(
                        id=point_id,
                        vector=embedding.tolist(),
                        payload={
                            'text': chunk['text'],
                            **chunk['metadata']
                        }
                    )
                    points.append(point)
                    point_id += 1
                    
                    # Insertar en lotes de 100
                    if len(points) >= 100:
                        self.qdrant.upsert(
                            collection_name=self.collection_name,
                            points=points
                        )
                        total_chunks += len(points)
                        print(f"  ✅ {total_chunks} chunks indexados")
                        points = []
                        
                except Exception as e:
                    print(f"  ⚠️  Error en chunk: {e}")
                    continue
        
        # Insertar chunks restantes
        if points:
            self.qdrant.upsert(
                collection_name=self.collection_name,
                points=points
            )
            total_chunks += len(points)
        
        print(f"\n✅ Indexación completada: {total_chunks} chunks totales")
        
        # Estadísticas
        collection_info = self.qdrant.get_collection(self.collection_name)
        print(f"\n📊 Estadísticas de la colección:")
        print(f"  - Nombre: {self.collection_name}")
        print(f"  - Vectores: {collection_info.points_count}")
        print(f"  - Dimensión: 1024 (BGE-M3)")
    
    def _classify_document(self, filename: str) -> str:
        """Clasifica el tipo de documento por nombre"""
        filename_lower = filename.lower()
        
        if 'examen' in filename_lower or 'test' in filename_lower:
            return 'examen'
        elif 'simulacro' in filename_lower:
            return 'simulacro'
        elif 'respuesta' in filename_lower:
            return 'respuestas'
        elif 'temario' in filename_lower or 'tema' in filename_lower:
            return 'temario'
        elif 'esquema' in filename_lower:
            return 'esquema'
        elif 'caso' in filename_lower or 'practico' in filename_lower:
            return 'caso_practico'
        else:
            return 'otro'

def main():
    print("🚀 Indexador de Materiales de Academia")
    print("=" * 50)
    
    materials_dir = "elemplos_leyes_info/de_mi_hija"
    
    if not Path(materials_dir).exists():
        print(f"❌ Error: No se encuentra el directorio {materials_dir}")
        return
    
    indexer = AcademyMaterialsIndexer()
    indexer.index_materials(materials_dir)
    
    print("\n✅ Proceso completado")
    print("\n💡 Ahora puedes probar búsquedas con:")
    print("   python backend/agents/test_search_academia.py")

if __name__ == "__main__":
    main()
