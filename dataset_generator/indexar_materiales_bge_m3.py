#!/usr/bin/env python3
"""
Indexador de Materiales de Academia con BGE-M3
Indexa PDFs en Qdrant local usando embeddings BGE-M3
"""

import os
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import fitz  # PyMuPDF
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import re

class MaterialesIndexer:
    def __init__(
        self,
        qdrant_url: str = "http://localhost:6333",
        collection_name: str = "materiales_base",
        model_name: str = "littlejohn-ai/bge-m3-spa-law-qa"
    ):
        self.qdrant_url = qdrant_url
        self.collection_name = collection_name
        
        print(f"🔄 Inicializando indexador...")
        print(f"   Qdrant: {qdrant_url}")
        print(f"   Colección: {collection_name}")
        print(f"   Modelo: {model_name}")
        
        # Inicializar cliente Qdrant
        self.client = QdrantClient(url=qdrant_url)
        
        # Cargar modelo BGE-M3
        print(f"\n📥 Cargando modelo BGE-M3...")
        self.embedder = SentenceTransformer(model_name)
        self.vector_size = self.embedder.get_sentence_embedding_dimension()
        print(f"   ✅ Modelo cargado (dimensión: {self.vector_size})")
        
        # Estadísticas
        self.stats = {
            "files_processed": 0,
            "chunks_created": 0,
            "chunks_indexed": 0,
            "errors": 0
        }
    
    def create_collection(self, recreate: bool = False) -> None:
        """Crea la colección en Qdrant"""
        collections = self.client.get_collections().collections
        collection_exists = any(c.name == self.collection_name for c in collections)
        
        if collection_exists:
            if recreate:
                print(f"🗑️  Eliminando colección existente: {self.collection_name}")
                self.client.delete_collection(self.collection_name)
            else:
                print(f"✅ Colección ya existe: {self.collection_name}")
                return
        
        print(f"📦 Creando colección: {self.collection_name}")
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE
            )
        )
        print(f"   ✅ Colección creada")
    
    def extract_text_from_pdf(self, pdf_path: str) -> List[Dict]:
        """Extrae texto de PDF con información de página"""
        try:
            doc = fitz.open(pdf_path)
            pages_data = []
            
            for page_num, page in enumerate(doc):
                text = page.get_text()
                
                if len(text.strip()) > 50:  # Solo páginas con contenido
                    pages_data.append({
                        "page_number": page_num + 1,
                        "text": text.strip()
                    })
            
            doc.close()
            return pages_data
            
        except Exception as e:
            print(f"❌ Error extrayendo texto de {pdf_path}: {e}")
            return []
    
    def chunk_text_semantic(
        self,
        text: str,
        chunk_size: int = 512,
        chunk_overlap: int = 50
    ) -> List[str]:
        """Divide texto en chunks semánticos"""
        # Separadores en orden de prioridad
        separators = ["\n\n", "\n", ". ", ", ", " "]
        
        chunks = []
        current_chunk = ""
        
        # Dividir por párrafos primero
        paragraphs = text.split("\n\n")
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # Si el párrafo es muy largo, dividir por oraciones
            if len(para) > chunk_size:
                sentences = re.split(r'(?<=[.!?])\s+', para)
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) < chunk_size:
                        current_chunk += " " + sentence
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = sentence
            else:
                if len(current_chunk) + len(para) < chunk_size:
                    current_chunk += "\n\n" + para
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = para
        
        # Agregar último chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def extract_questions_from_exam(self, text: str) -> List[Dict]:
        """Extrae preguntas individuales de un examen"""
        questions = []
        
        # Patrón para preguntas numeradas con opciones
        pattern = r'(\d+)\.\s*(.+?)(?=\d+\.|$)'
        matches = re.findall(pattern, text, re.DOTALL)
        
        for num, content in matches:
            content = content.strip()
            
            # Buscar opciones A, B, C, D
            options_pattern = r'([A-D])\)\s*(.+?)(?=[A-D]\)|$)'
            options = re.findall(options_pattern, content, re.DOTALL)
            
            if options:
                # Extraer pregunta (antes de las opciones)
                question_text = re.split(r'[A-D]\)', content)[0].strip()
                
                options_list = [f"{letter}) {text.strip()}" for letter, text in options]
                
                questions.append({
                    "number": int(num),
                    "question": question_text,
                    "options": options_list,
                    "full_text": content
                })
        
        return questions
    
    def categorize_file(self, filename: str) -> Dict[str, str]:
        """Categoriza un archivo y extrae metadata"""
        filename_lower = filename.lower()
        
        category = "otros"
        subcategory = ""
        is_official = False
        has_answers = False
        
        # Exámenes oficiales
        if any(kw in filename_lower for kw in ['examen_c1', 'gestion_libre', 'gestion_pi']):
            category = "examenes_oficiales"
            is_official = True
            
            if 'respuestas' in filename_lower:
                has_answers = True
                subcategory = "respuestas"
            else:
                subcategory = "preguntas"
        
        # Esquemas de prestaciones
        prestaciones = {
            'it.pdf': 'Incapacidad Temporal',
            'ip_absoluta': 'IP Absoluta',
            'ip_parcial': 'IP Parcial',
            'ip_total': 'IP Total',
            'jubilacion_ordinaria': 'Jubilación Ordinaria',
            'jubilacion_anticipada': 'Jubilación Anticipada',
            'viudedad': 'Viudedad',
            'orfandad': 'Orfandad',
            'nycm': 'Nacimiento y Cuidado del Menor',
            'encuadramiento': 'Encuadramiento',
            'cotizacion': 'Cotización'
        }
        
        for key, value in prestaciones.items():
            if key in filename_lower:
                category = "esquemas"
                subcategory = value
                break
        
        # Extraer año si existe
        year_match = re.search(r'20\d{2}', filename)
        year = int(year_match.group()) if year_match else None
        
        return {
            "category": category,
            "subcategory": subcategory,
            "is_official": is_official,
            "has_answers": has_answers,
            "year": year
        }
    
    def index_pdf(
        self,
        pdf_path: str,
        category_filter: Optional[str] = None
    ) -> int:
        """Indexa un PDF en Qdrant"""
        filename = os.path.basename(pdf_path)
        
        # Categorizar archivo
        metadata = self.categorize_file(filename)
        
        # Filtrar por categoría si se especifica
        if category_filter and metadata["category"] != category_filter:
            return 0
        
        print(f"\n📄 Procesando: {filename}")
        print(f"   Categoría: {metadata['category']}")
        if metadata['subcategory']:
            print(f"   Subcategoría: {metadata['subcategory']}")
        
        # Extraer texto
        pages_data = self.extract_text_from_pdf(pdf_path)
        if not pages_data:
            print(f"   ⚠️  No se pudo extraer texto")
            self.stats["errors"] += 1
            return 0
        
        print(f"   📖 Páginas extraídas: {len(pages_data)}")
        
        # Procesar según categoría
        chunks_indexed = 0
        
        if metadata["category"] == "examenes_oficiales" and not metadata["has_answers"]:
            # Para exámenes, extraer preguntas individuales
            for page_data in pages_data:
                questions = self.extract_questions_from_exam(page_data["text"])
                
                if questions:
                    print(f"   ❓ Preguntas encontradas en página {page_data['page_number']}: {len(questions)}")
                    
                    for q in questions:
                        chunk_text = f"Pregunta {q['number']}: {q['question']}\n\nOpciones:\n" + "\n".join(q['options'])
                        
                        # Generar embedding
                        embedding = self.embedder.encode(chunk_text).tolist()
                        
                        # Crear punto para Qdrant
                        point_id = hashlib.md5(
                            f"{filename}_{page_data['page_number']}_{q['number']}".encode()
                        ).hexdigest()
                        
                        point = PointStruct(
                            id=point_id,
                            vector=embedding,
                            payload={
                                "filename": filename,
                                "filepath": pdf_path,
                                "category": metadata["category"],
                                "subcategory": metadata["subcategory"],
                                "is_official": metadata["is_official"],
                                "year": metadata["year"],
                                "page_number": page_data["page_number"],
                                "question_number": q["number"],
                                "text": chunk_text,
                                "indexed_at": datetime.now().isoformat()
                            }
                        )
                        
                        # Indexar en Qdrant
                        self.client.upsert(
                            collection_name=self.collection_name,
                            points=[point]
                        )
                        
                        chunks_indexed += 1
                        self.stats["chunks_indexed"] += 1
                else:
                    # Si no se detectan preguntas, hacer chunking normal
                    chunks = self.chunk_text_semantic(page_data["text"])
                    chunks_indexed += self._index_chunks(
                        chunks, filename, pdf_path, metadata, page_data["page_number"]
                    )
        else:
            # Para otros documentos, chunking semántico normal
            for page_data in pages_data:
                chunks = self.chunk_text_semantic(page_data["text"])
                chunks_indexed += self._index_chunks(
                    chunks, filename, pdf_path, metadata, page_data["page_number"]
                )
        
        print(f"   ✅ Chunks indexados: {chunks_indexed}")
        self.stats["files_processed"] += 1
        
        return chunks_indexed
    
    def _index_chunks(
        self,
        chunks: List[str],
        filename: str,
        filepath: str,
        metadata: Dict,
        page_number: int
    ) -> int:
        """Indexa una lista de chunks"""
        indexed = 0
        
        for idx, chunk in enumerate(chunks):
            if len(chunk.strip()) < 50:  # Ignorar chunks muy pequeños
                continue
            
            # Generar embedding
            embedding = self.embedder.encode(chunk).tolist()
            
            # Crear ID único
            point_id = hashlib.md5(
                f"{filename}_{page_number}_{idx}".encode()
            ).hexdigest()
            
            # Crear punto
            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "filename": filename,
                    "filepath": filepath,
                    "category": metadata["category"],
                    "subcategory": metadata["subcategory"],
                    "is_official": metadata.get("is_official", False),
                    "year": metadata.get("year"),
                    "page_number": page_number,
                    "chunk_index": idx,
                    "text": chunk,
                    "indexed_at": datetime.now().isoformat()
                }
            )
            
            # Indexar
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            
            indexed += 1
            self.stats["chunks_indexed"] += 1
        
        return indexed
    
    def index_directory(
        self,
        directory: str,
        category_filter: Optional[str] = None,
        max_files: Optional[int] = None
    ) -> None:
        """Indexa todos los PDFs en un directorio"""
        print(f"\n🔍 Escaneando directorio: {directory}")
        
        pdf_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
        
        print(f"   📚 PDFs encontrados: {len(pdf_files)}")
        
        if category_filter:
            print(f"   🔍 Filtrando por categoría: {category_filter}")
        
        if max_files:
            pdf_files = pdf_files[:max_files]
            print(f"   ⚠️  Limitando a {max_files} archivos")
        
        # Indexar archivos
        for pdf_path in pdf_files:
            try:
                self.index_pdf(pdf_path, category_filter)
            except Exception as e:
                print(f"   ❌ Error procesando {pdf_path}: {e}")
                self.stats["errors"] += 1
        
        # Mostrar estadísticas finales
        self.print_stats()
    
    def print_stats(self) -> None:
        """Muestra estadísticas de indexación"""
        print("\n" + "="*60)
        print("📊 ESTADÍSTICAS DE INDEXACIÓN")
        print("="*60)
        print(f"Archivos procesados: {self.stats['files_processed']}")
        print(f"Chunks indexados: {self.stats['chunks_indexed']}")
        print(f"Errores: {self.stats['errors']}")
        
        # Estadísticas de Qdrant
        collection_info = self.client.get_collection(self.collection_name)
        print(f"\n📦 Colección: {self.collection_name}")
        print(f"   Vectores totales: {collection_info.points_count}")
    
    def search(
        self,
        query: str,
        limit: int = 5,
        category_filter: Optional[str] = None
    ) -> List[Dict]:
        """Busca en la colección"""
        # Generar embedding de la query
        query_vector = self.embedder.encode(query).tolist()
        
        # Preparar filtro
        query_filter = None
        if category_filter:
            from qdrant_client.models import Filter, FieldCondition, MatchValue
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="category",
                        match=MatchValue(value=category_filter)
                    )
                ]
            )
        
        # Buscar
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            query_filter=query_filter
        )
        
        return [
            {
                "score": hit.score,
                "text": hit.payload.get("text", ""),
                "filename": hit.payload.get("filename", ""),
                "category": hit.payload.get("category", ""),
                "page": hit.payload.get("page_number", 0)
            }
            for hit in results
        ]

def main():
    """Función principal"""
    # Configuración
    BASE_PATH = "/home/espasiko/OPOS_GEMINI_1/elemplos_leyes_info/de_mi_hija"
    
    # Crear indexador
    indexer = MaterialesIndexer(
        qdrant_url="http://localhost:6333",
        collection_name="materiales_base",
        model_name="BAAI/bge-m3"
    )
    
    # Crear colección (recrear si existe)
    indexer.create_collection(recreate=True)
    
    # FASE 1: Indexar solo exámenes oficiales
    print("\n" + "="*60)
    print("🎯 FASE 1: INDEXANDO EXÁMENES OFICIALES")
    print("="*60)
    
    indexer.index_directory(
        directory=os.path.join(BASE_PATH, "bajados_academia"),
        category_filter="examenes_oficiales",
        max_files=None  # Todos los exámenes
    )
    
    # Prueba de búsqueda
    print("\n" + "="*60)
    print("🔍 PRUEBA DE BÚSQUEDA")
    print("="*60)
    
    test_query = "¿Cuál es el período mínimo de cotización para la jubilación?"
    print(f"\nQuery: {test_query}")
    
    results = indexer.search(test_query, limit=3, category_filter="examenes_oficiales")
    
    for i, result in enumerate(results, 1):
        print(f"\n--- Resultado {i} (score: {result['score']:.3f}) ---")
        print(f"Archivo: {result['filename']}")
        print(f"Página: {result['page']}")
        print(f"Texto: {result['text'][:200]}...")
    
    print("\n✅ Indexación completada!")

if __name__ == "__main__":
    main()
