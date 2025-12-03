#!/usr/bin/env python3
"""
INDEXAR MATERIALES DE OPOSICIONES A QDRANT LOCAL
Extrae texto de PDFs, genera embeddings e indexa en Qdrant local

Uso:
    python index_materials_to_qdrant.py
    
Resultado:
    - Indexa todos los PDFs de backend/data/materiales_opos/
    - Genera embeddings con bge-m3-spa-law-qa (1024 dims)
    - Inserta en Qdrant local (localhost:6333)
    - Metadata: {tipo, categoria, año, archivo, pagina, texto}
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# PDF processing
try:
    import PyPDF2
except ImportError:
    print("⚠️  PyPDF2 no instalado. Instalando...")
    os.system("pip install PyPDF2")
    import PyPDF2

# Embeddings
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("⚠️  sentence-transformers no instalado. Instalando...")
    os.system("pip install sentence-transformers")
    from sentence_transformers import SentenceTransformer

# Qdrant
try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct
except ImportError:
    print("⚠️  qdrant-client no instalado. Instalando...")
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


class MaterialesIndexer:
    """
    Indexa materiales de oposiciones (PDFs) en Qdrant local
    con embeddings especializados en legislación española
    """
    
    def __init__(self, use_local=True):
        """
        Inicializa indexador
        
        Args:
            use_local: True para Qdrant local (localhost:6333), 
                      False para Qdrant Cloud
        """
        logger.info("🚀 INICIANDO INDEXADOR DE MATERIALES")
        
        # Modelo de embeddings especializado en legal español
        logger.info("📦 Cargando modelo: littlejohn-ai/bge-m3-spa-law-qa")
        logger.info("   ├─ Especialización: Legislación española")
        logger.info("   ├─ Dimensión: 1024 vectores")
        logger.info("   └─ Tamaño: ~600 MB")
        
        try:
            self.model = SentenceTransformer('littlejohn-ai/bge-m3-spa-law-qa')
            self.vector_size = 1024
        except Exception as e:
            logger.warning(f"⚠️  Modelo bge-m3-spa-law-qa no disponible: {e}")
            logger.info("📦 Fallback a: dariolopez/roberta-base-bne-finetuned-msmarco-qa-es")
            self.model = SentenceTransformer(
                'dariolopez/roberta-base-bne-finetuned-msmarco-qa-es'
            )
            self.vector_size = 768
        
        # Qdrant connection
        if use_local:
            logger.info("🔌 Conectando a Qdrant LOCAL: http://localhost:6333")
            self.client = QdrantClient(host="localhost", port=6333)
        else:
            qdrant_url = os.getenv("QDRANT_URL")
            qdrant_key = os.getenv("QDRANT_API_KEY")
            logger.info(f"🔌 Conectando a Qdrant CLOUD: {qdrant_url}")
            self.client = QdrantClient(url=qdrant_url, api_key=qdrant_key)
        
        self.collection_name = "materiales_oposiciones"
        self.materiales_dir = Path(__file__).parent.parent / "data" / "materiales_opos"
        
        logger.info(f"📁 Directorio materiales: {self.materiales_dir}")
        logger.info("✅ Inicialización completada\n")
    
    def extract_text_from_pdf(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """
        Extrae texto de PDF página por página
        
        Args:
            pdf_path: Ruta al archivo PDF
            
        Returns:
            Lista de diccionarios con {pagina, texto}
        """
        pages = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                logger.info(f"   📄 {pdf_path.name}: {total_pages} páginas")
                
                for page_num in range(total_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    
                    # Limpiar texto
                    text = text.strip()
                    
                    # Solo agregar si tiene contenido relevante (>50 caracteres)
                    if len(text) > 50:
                        pages.append({
                            'pagina': page_num + 1,
                            'texto': text
                        })
                
                logger.info(f"   ✅ Extraídas {len(pages)} páginas con contenido")
                
        except Exception as e:
            logger.error(f"   ❌ Error extrayendo {pdf_path.name}: {e}")
        
        return pages
    
    def chunk_text(self, text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
        """
        Divide texto en chunks con overlap para mejor contexto
        
        Args:
            text: Texto a dividir
            chunk_size: Tamaño de cada chunk en caracteres
            overlap: Overlap entre chunks
            
        Returns:
            Lista de chunks de texto
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Buscar punto final para cortar mejor
            if end < len(text):
                last_period = chunk.rfind('.')
                if last_period > chunk_size * 0.7:  # Solo si está en últimos 30%
                    end = start + last_period + 1
                    chunk = text[start:end]
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return chunks
    
    def detect_categoria(self, file_path: Path) -> Dict[str, str]:
        """
        Detecta categoría y metadata del archivo según su ubicación y nombre
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            Dict con metadata: {tipo, categoria, año, etc}
        """
        path_parts = file_path.parts
        filename = file_path.stem.lower()
        
        # Detectar categoría por directorio
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
        
        # Detectar año en nombre de archivo
        import re
        year_match = re.search(r'20\d{2}', filename)
        año = year_match.group(0) if year_match else "unknown"
        
        # Detectar tema/materia
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
        """
        Crea colección en Qdrant con configuración optimizada
        """
        logger.info("\n🗂️  CREANDO COLECCIÓN")
        
        # Verificar si existe
        collections = self.client.get_collections().collections
        collection_exists = any(c.name == self.collection_name for c in collections)
        
        if collection_exists:
            logger.warning(f"⚠️  Colección '{self.collection_name}' ya existe")
            response = input("¿Eliminar y recrear? (s/N): ")
            if response.lower() == 's':
                self.client.delete_collection(self.collection_name)
                logger.info("🗑️  Colección eliminada")
            else:
                logger.info("📌 Usando colección existente")
                return
        
        # Crear colección
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
    
    def index_all_materials(self):
        """
        Indexa todos los PDFs de materiales_opos/
        """
        logger.info("\n📚 INDEXANDO MATERIALES")
        print("="*70)
        
        # Verificar directorio existe
        if not self.materiales_dir.exists():
            logger.error(f"❌ Directorio no existe: {self.materiales_dir}")
            return
        
        # Buscar todos los PDFs recursivamente
        pdf_files = list(self.materiales_dir.rglob("*.pdf"))
        total_files = len(pdf_files)
        
        logger.info(f"📊 Total PDFs encontrados: {total_files}")
        
        if total_files == 0:
            logger.warning("⚠️  No se encontraron PDFs para indexar")
            return
        
        # Estadísticas
        stats = {
            'total_files': total_files,
            'total_pages': 0,
            'total_chunks': 0,
            'total_vectors': 0,
            'errors': 0
        }
        
        # Procesar cada PDF
        all_points = []
        point_id = 1
        
        for idx, pdf_path in enumerate(pdf_files, 1):
            logger.info(f"\n📄 [{idx}/{total_files}] {pdf_path.name}")
            
            try:
                # 1. Extraer texto por página
                pages = self.extract_text_from_pdf(pdf_path)
                stats['total_pages'] += len(pages)
                
                # 2. Detectar metadata
                metadata = self.detect_categoria(pdf_path)
                
                # 3. Procesar cada página
                for page_data in pages:
                    # Dividir en chunks
                    chunks = self.chunk_text(page_data['texto'])
                    stats['total_chunks'] += len(chunks)
                    
                    # Generar embeddings para cada chunk
                    for chunk_idx, chunk in enumerate(chunks):
                        try:
                            # Generar embedding
                            embedding = self.model.encode(chunk).tolist()
                            
                            # Crear punto Qdrant
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
                            logger.error(f"   ⚠️  Error embedding chunk: {e}")
                            stats['errors'] += 1
                
                logger.info(f"   ✅ Procesado: {len(pages)} páginas → {stats['total_vectors']} vectores")
                
            except Exception as e:
                logger.error(f"   ❌ Error procesando {pdf_path.name}: {e}")
                stats['errors'] += 1
        
        # 4. Insertar todos los puntos en batch
        if all_points:
            logger.info(f"\n💾 INSERTANDO {len(all_points)} vectores en Qdrant...")
            
            batch_size = 100
            for i in range(0, len(all_points), batch_size):
                batch = all_points[i:i+batch_size]
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch
                )
                logger.info(f"   ✅ Insertados {i+len(batch)}/{len(all_points)} vectores")
        
        # 5. Resumen final
        print("\n" + "="*70)
        print("✅ INDEXACIÓN COMPLETADA")
        print("="*70)
        logger.info(f"📊 ESTADÍSTICAS:")
        logger.info(f"   ├─ PDFs procesados: {stats['total_files']}")
        logger.info(f"   ├─ Páginas extraídas: {stats['total_pages']}")
        logger.info(f"   ├─ Chunks generados: {stats['total_chunks']}")
        logger.info(f"   ├─ Vectores insertados: {stats['total_vectors']}")
        logger.info(f"   └─ Errores: {stats['errors']}")
        
        # Guardar estadísticas
        stats_file = self.materiales_dir / "indexacion_stats.json"
        with open(stats_file, 'w') as f:
            json.dump({
                **stats,
                'indexed_at': datetime.now().isoformat(),
                'model': 'littlejohn-ai/bge-m3-spa-law-qa',
                'vector_size': self.vector_size
            }, f, indent=2)
        
        logger.info(f"\n💾 Estadísticas guardadas en: {stats_file}")
    
    def test_search(self, query: str = "¿Qué es el TREBEP?", top_k: int = 3):
        """
        Prueba búsqueda en colección indexada
        
        Args:
            query: Query de prueba
            top_k: Número de resultados
        """
        logger.info(f"\n🔍 PROBANDO BÚSQUEDA: '{query}'")
        
        # Generar embedding del query
        query_vector = self.model.encode(query).tolist()
        
        # Buscar en Qdrant
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
            logger.info(f"   Página: {result.payload['pagina']}")
            logger.info(f"   Tema: {result.payload['tema']}")
            logger.info(f"   Texto: {result.payload['texto'][:200]}...")


def main():
    """
    Función principal
    """
    print("\n" + "="*70)
    print("🚀 INDEXADOR DE MATERIALES DE OPOSICIONES")
    print("="*70)
    
    # Crear indexador (Qdrant local por defecto)
    indexer = MaterialesIndexer(use_local=True)
    
    # Crear colección
    indexer.create_collection()
    
    # Indexar todos los materiales
    indexer.index_all_materials()
    
    # Prueba de búsqueda
    indexer.test_search("¿Qué es el TREBEP?", top_k=3)
    indexer.test_search("Examen oficial C1 Seguridad Social", top_k=3)
    
    print("\n✅ PROCESO COMPLETADO")


if __name__ == "__main__":
    main()
