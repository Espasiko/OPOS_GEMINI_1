#!/usr/bin/env python3
"""
INDEXAR MATERIALES - MODO PRUEBA (Solo 3-5 PDFs)
Versión de prueba para validar el proceso antes de indexar todo

Uso:
    python index_materials_PRUEBA.py
    
Resultado:
    - Indexa solo 3-5 PDFs como prueba
    - Genera embeddings con bge-m3-spa-law-qa (1024 dims)
    - Inserta en colección de prueba: materiales_oposiciones_TEST
    - Valida búsquedas
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Importar del script principal
import sys
sys.path.insert(0, str(Path(__file__).parent))

try:
    import PyPDF2
except ImportError:
    print("⚠️  Instalando PyPDF2...")
    os.system("pip install PyPDF2")
    import PyPDF2

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("⚠️  Instalando sentence-transformers...")
    os.system("pip install sentence-transformers")
    from sentence_transformers import SentenceTransformer

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct
except ImportError:
    print("⚠️  Instalando qdrant-client...")
    os.system("pip install qdrant-client")
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MaterialesIndexerPrueba:
    """
    Versión de PRUEBA - Solo indexa 3-5 PDFs para validar
    """
    
    def __init__(self):
        logger.info("🧪 MODO PRUEBA - INDEXADOR DE MATERIALES")
        
        # Modelo de embeddings
        logger.info("📦 Cargando modelo: littlejohn-ai/bge-m3-spa-law-qa")
        
        try:
            self.model = SentenceTransformer('littlejohn-ai/bge-m3-spa-law-qa')
            self.vector_size = 1024
            logger.info("✅ Modelo bge-m3-spa-law-qa cargado (1024 dims)")
        except Exception as e:
            logger.warning(f"⚠️  bge-m3 no disponible: {e}")
            logger.info("📦 Fallback a: dariolopez/roberta-base-bne-finetuned-msmarco-qa-es")
            self.model = SentenceTransformer('dariolopez/roberta-base-bne-finetuned-msmarco-qa-es')
            self.vector_size = 768
        
        # Qdrant LOCAL
        logger.info("🔌 Conectando a Qdrant LOCAL: http://localhost:6333")
        self.client = QdrantClient(host="localhost", port=6333)
        
        self.collection_name = "materiales_oposiciones_TEST"
        self.materiales_dir = Path(__file__).parent.parent / "data" / "materiales_opos"
        
        logger.info(f"📁 Directorio: {self.materiales_dir}")
        logger.info("✅ Inicialización completada\n")
    
    def extract_text_from_pdf(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """Extrae texto de PDF página por página"""
        pages = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                logger.info(f"   📄 {pdf_path.name}: {total_pages} páginas")
                
                for page_num in range(total_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text().strip()
                    
                    if len(text) > 50:
                        pages.append({
                            'pagina': page_num + 1,
                            'texto': text
                        })
                
                logger.info(f"   ✅ Extraídas {len(pages)} páginas con contenido")
                
        except Exception as e:
            logger.error(f"   ❌ Error: {e}")
        
        return pages
    
    def chunk_text(self, text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
        """Divide texto en chunks con overlap"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            if end < len(text):
                last_period = chunk.rfind('.')
                if last_period > chunk_size * 0.7:
                    end = start + last_period + 1
                    chunk = text[start:end]
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return chunks
    
    def detect_categoria(self, file_path: Path) -> Dict[str, str]:
        """Detecta categoría y metadata del archivo"""
        path_parts = file_path.parts
        filename = file_path.stem.lower()
        
        if "examenes_oficiales" in path_parts:
            tipo = "examen_oficial"
            categoria = "C1_SS"
        elif "tests_age" in path_parts:
            tipo = "test"
            categoria = "AGE"
        elif "temarios" in path_parts:
            tipo = "temario"
            categoria = "SS_AGE"
        elif "esquemas" in path_parts:
            tipo = "esquema"
            categoria = "varios"
        elif "bases_convocatorias" in path_parts:
            tipo = "base_convocatoria"
            categoria = "oficial"
        else:
            tipo = "documento"
            categoria = "general"
        
        import re
        year_match = re.search(r'20\d{2}', filename)
        año = year_match.group(0) if year_match else "unknown"
        
        tema = "general"
        if "constitucion" in filename:
            tema = "constitucion"
        elif "pac" in filename:
            tema = "pac"
        elif "trebep" in filename or "ebep" in filename:
            tema = "trebep"
        elif "estatuto" in filename:
            tema = "estatuto"
        elif "lgss" in filename or "seguridad_social" in filename:
            tema = "seguridad_social"
        
        return {
            "tipo": tipo,
            "categoria": categoria,
            "año": año,
            "tema": tema,
            "archivo": file_path.name
        }
    
    def create_collection(self):
        """Crea colección de PRUEBA"""
        logger.info("\n🗂️  CREANDO COLECCIÓN DE PRUEBA")
        
        collections = self.client.get_collections().collections
        collection_exists = any(c.name == self.collection_name for c in collections)
        
        if collection_exists:
            logger.warning(f"⚠️  Colección de prueba ya existe, eliminando...")
            self.client.delete_collection(self.collection_name)
        
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE
            )
        )
        
        logger.info(f"✅ Colección '{self.collection_name}' creada")
        logger.info(f"   ├─ Dimensión: {self.vector_size} vectores")
        logger.info(f"   └─ Distancia: COSINE")
    
    def index_sample_materials(self, max_files: int = 5):
        """
        Indexa solo ALGUNOS PDFs como prueba
        
        Args:
            max_files: Máximo de PDFs a procesar (default 5)
        """
        logger.info(f"\n📚 INDEXANDO MATERIALES - MODO PRUEBA (Máximo {max_files} PDFs)")
        print("="*70)
        
        if not self.materiales_dir.exists():
            logger.error(f"❌ Directorio no existe: {self.materiales_dir}")
            return
        
        # Buscar PDFs - Selección diversa
        all_pdfs = list(self.materiales_dir.rglob("*.pdf"))
        
        # Seleccionar muestra diversa (1 de cada categoría si posible)
        sample_pdfs = []
        categories_found = set()
        
        for pdf_path in all_pdfs:
            category = None
            for part in pdf_path.parts:
                if part in ["examenes_oficiales_c1_ss", "tests_age", "temarios_ss_age", 
                           "esquemas", "bases_convocatorias"]:
                    category = part
                    break
            
            if category and category not in categories_found:
                sample_pdfs.append(pdf_path)
                categories_found.add(category)
                logger.info(f"📌 Seleccionado: {pdf_path.name} ({category})")
                
                if len(sample_pdfs) >= max_files:
                    break
        
        # Si no hay suficientes, tomar los primeros
        if len(sample_pdfs) < max_files:
            remaining = max_files - len(sample_pdfs)
            for pdf in all_pdfs:
                if pdf not in sample_pdfs:
                    sample_pdfs.append(pdf)
                    logger.info(f"📌 Seleccionado adicional: {pdf.name}")
                    if len(sample_pdfs) >= max_files:
                        break
        
        logger.info(f"\n📊 Total PDFs para prueba: {len(sample_pdfs)}")
        
        # Estadísticas
        stats = {
            'total_files': len(sample_pdfs),
            'total_pages': 0,
            'total_chunks': 0,
            'total_vectors': 0,
            'errors': 0
        }
        
        # Procesar PDFs seleccionados
        all_points = []
        point_id = 1
        
        for idx, pdf_path in enumerate(sample_pdfs, 1):
            logger.info(f"\n📄 [{idx}/{len(sample_pdfs)}] {pdf_path.name}")
            
            try:
                # 1. Extraer texto
                pages = self.extract_text_from_pdf(pdf_path)
                stats['total_pages'] += len(pages)
                
                # 2. Metadata
                metadata = self.detect_categoria(pdf_path)
                
                # 3. Procesar cada página
                for page_data in pages:
                    chunks = self.chunk_text(page_data['texto'])
                    stats['total_chunks'] += len(chunks)
                    
                    for chunk_idx, chunk in enumerate(chunks):
                        try:
                            # Embedding
                            embedding = self.model.encode(chunk).tolist()
                            
                            # Punto Qdrant
                            point = PointStruct(
                                id=point_id,
                                vector=embedding,
                                payload={
                                    **metadata,
                                    'pagina': page_data['pagina'],
                                    'chunk_index': chunk_idx,
                                    'texto': chunk,
                                    'indexed_at': datetime.now().isoformat()
                                }
                            )
                            
                            all_points.append(point)
                            point_id += 1
                            stats['total_vectors'] += 1
                            
                        except Exception as e:
                            logger.error(f"   ⚠️  Error embedding: {e}")
                            stats['errors'] += 1
                
                logger.info(f"   ✅ {len(pages)} páginas → {stats['total_vectors']} vectores")
                
            except Exception as e:
                logger.error(f"   ❌ Error: {e}")
                stats['errors'] += 1
        
        # Insertar en Qdrant
        if all_points:
            logger.info(f"\n💾 INSERTANDO {len(all_points)} vectores...")
            
            batch_size = 100
            for i in range(0, len(all_points), batch_size):
                batch = all_points[i:i+batch_size]
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch
                )
                logger.info(f"   ✅ {i+len(batch)}/{len(all_points)} vectores")
        
        # Resumen
        print("\n" + "="*70)
        print("✅ PRUEBA COMPLETADA")
        print("="*70)
        logger.info(f"📊 ESTADÍSTICAS:")
        logger.info(f"   ├─ PDFs procesados: {stats['total_files']}")
        logger.info(f"   ├─ Páginas: {stats['total_pages']}")
        logger.info(f"   ├─ Chunks: {stats['total_chunks']}")
        logger.info(f"   ├─ Vectores: {stats['total_vectors']}")
        logger.info(f"   └─ Errores: {stats['errors']}")
        
        return stats
    
    def test_search(self, query: str, top_k: int = 3):
        """Prueba búsqueda"""
        logger.info(f"\n🔍 PROBANDO: '{query}'")
        
        query_vector = self.model.encode(query).tolist()
        
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k
        )
        
        logger.info(f"\n📋 Top {top_k} resultados:")
        for idx, result in enumerate(results, 1):
            logger.info(f"\n{idx}. Score: {result.score:.4f}")
            logger.info(f"   Archivo: {result.payload['archivo']}")
            logger.info(f"   Tipo: {result.payload['tipo']}")
            logger.info(f"   Tema: {result.payload['tema']}")
            logger.info(f"   Texto: {result.payload['texto'][:150]}...")


def main():
    """Función principal de PRUEBA"""
    print("\n" + "="*70)
    print("🧪 INDEXADOR DE MATERIALES - MODO PRUEBA")
    print("="*70)
    print("\n⚠️  IMPORTANTE: Esto es una PRUEBA con solo 5 PDFs")
    print("   Si funciona bien, ejecutar index_materials_to_qdrant.py completo\n")
    
    # Crear indexador
    indexer = MaterialesIndexerPrueba()
    
    # Crear colección
    indexer.create_collection()
    
    # Indexar SOLO 5 PDFs como prueba
    stats = indexer.index_sample_materials(max_files=5)
    
    # Pruebas de búsqueda
    if stats['total_vectors'] > 0:
        print("\n" + "="*70)
        print("🔍 PRUEBAS DE BÚSQUEDA")
        print("="*70)
        
        indexer.test_search("¿Qué es el TREBEP?", top_k=3)
        indexer.test_search("Examen oficial Seguridad Social", top_k=3)
        indexer.test_search("Constitución española artículos", top_k=3)
    
    print("\n✅ PRUEBA COMPLETADA")
    print("\nSi todo funciona correctamente, ejecutar:")
    print("  python scripts/index_materials_to_qdrant.py")


if __name__ == "__main__":
    main()
