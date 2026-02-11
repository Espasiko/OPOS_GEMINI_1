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

# Añadir el directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

# Imports opcionales para indexación (no necesarios para --dry-run)
INDEXING_AVAILABLE = True
try:
    import pickle
    from collections import Counter
    import PyPDF2
    from qdrant_client import QdrantClient
    from qdrant_client.models import (
        Distance, VectorParams, PointStruct,
        SparseVector, SparseVectorParams, SparseIndexParams
    )
    from sentence_transformers import SentenceTransformer
except ImportError as e:
    print(f"⚠️ Algunos módulos no disponibles: {e}")
    print("   Modo --dry-run disponible, indexación deshabilitada")
    INDEXING_AVAILABLE = False

class AcademyMaterialsIndexer:
    def __init__(self, skip_model=False):
        if not INDEXING_AVAILABLE:
            raise RuntimeError("Módulos de indexación no disponibles. Instala: pip install PyPDF2 qdrant-client sentence-transformers")
        
        # Conectar a Qdrant local
        self.qdrant = QdrantClient(host="localhost", port=6333)
        
        if not skip_model:
            # Cargar modelo BGE-M3 con sentence-transformers
            print("🔄 Cargando modelo BGE-M3...")
            self.model = SentenceTransformer('pablosi/bge-m3-spa-law-qa-trained-2')
            print(f"✅ Modelo cargado. Dimensión: {self.model.get_sentence_embedding_dimension()}")
        else:
            self.model = None
        
        self.collection_name = "materiales_academia"
        self.chunk_size = 500  # Caracteres por chunk
        self.chunk_overlap = 150  # 30% solapamiento
        
        # Cargar BM25 vocab
        self.bm25_vocab = None
        self.bm25_avgdl = 38.1
        self._load_bm25_vocab()
    
    def _load_bm25_vocab(self):
        """Carga vocabulario BM25 para sparse vectors"""
        vocab_path = Path(__file__).parent.parent / "data" / "bm25_vocab.pkl"
        if vocab_path.exists():
            try:
                with open(vocab_path, 'rb') as f:
                    data = pickle.load(f)
                self.bm25_vocab = data.get('vocab', {})
                self.bm25_avgdl = data.get('avgdl', 38.1)
                print(f"📚 BM25 vocab: {len(self.bm25_vocab):,} términos, avgdl={self.bm25_avgdl:.1f}")
            except Exception as e:
                print(f"⚠️ Error cargando BM25 vocab: {e}")
                self.bm25_vocab = {}
        else:
            print(f"⚠️ No se encontró BM25 vocab en {vocab_path}")
            self.bm25_vocab = {}
    
    def _tokenize(self, text: str) -> list:
        """Tokeniza texto para BM25"""
        import re
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens
    
    def _generate_sparse_vector(self, text: str) -> SparseVector:
        """Genera vector sparse BM25 para texto"""
        if not self.bm25_vocab:
            return SparseVector(indices=[], values=[])
        
        tokens = self._tokenize(text)
        if not tokens:
            return SparseVector(indices=[], values=[])
        
        # Contar frecuencias
        tf = Counter(tokens)
        doc_len = len(tokens)
        k1, b = 1.5, 0.75
        
        indices = []
        values = []
        
        for term, freq in tf.items():
            if term in self.bm25_vocab:
                idx = self.bm25_vocab[term]
                # BM25 score simplificado
                tf_norm = (freq * (k1 + 1)) / (freq + k1 * (1 - b + b * doc_len / self.bm25_avgdl))
                indices.append(idx)
                values.append(float(tf_norm))
        
        return SparseVector(indices=indices, values=values)
        
    def clean_and_anonymize_text(self, text: str) -> str:
        """Limpia metadatos de copyright/legal y anonimiza datos sensibles"""
        
        # ============================================
        # FASE 1: ELIMINAR BLOQUES DE COPYRIGHT/LEGAL
        # ============================================
        
        # URLs completas
        text = re.sub(r'https?://[^\s]+', '', text)
        text = re.sub(r'www\.[^\s]+', '', text)
        text = re.sub(r'\b\w+\.(com|es|net|org|info|pdf)\b', '', text, flags=re.IGNORECASE)
        
        # ISBN, NIPO, Depósito Legal
        text = re.sub(r'ISBN[:\s]*[\d\-X]+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'NIPO[^:]*:[^\n]+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Depósito\s+Legal[^\n]+', '', text, flags=re.IGNORECASE)
        
        # Copyright y símbolos ©
        text = re.sub(r'©[^\n]+', '', text)
        text = re.sub(r'Copyright[^\n]+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Todos\s+los\s+derechos\s+reservados[^\n]*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Derechos\s+de\s+autor[^\n]*', '', text, flags=re.IGNORECASE)
        
        # Bloques de "prohibida reproducción"
        text = re.sub(r'(?:Queda\s+)?(?:expresamente\s+)?prohibid[oa][^\n]+(?:reproducción|distribución|publicación)[^\n]*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Duplicar[^\n]+ilegal[^\n]*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'acciones\s+legales[^\n]*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'persecución\s+por[^\n]*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'daños\s+y\s+perjuicios[^\n]*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'propiedad\s+intelectual[^\n]*', '', text, flags=re.IGNORECASE)
        
        # Ediciones y años de publicación
        text = re.sub(r'Ed\.\s*\d{4}', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Ed\.\s*TEMA\s+DIGITAL[^\n]*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Edición[^\n]*\d{4}', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(?:ENERO|FEBRERO|MARZO|ABRIL|MAYO|JUNIO|JULIO|AGOSTO|SEPTIEMBRE|OCTUBRE|NOVIEMBRE|DICIEMBRE)\s+\d{4}\b', '', text, flags=re.IGNORECASE)
        
        # Autores con formato "por Nombre Apellido" o "CEO en..."
        text = re.sub(r'CEO\s+en[^\n]+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'por\s+[A-ZÁÉÍÓÚ][a-záéíóú]+\s+[A-ZÁÉÍÓÚ][a-záéíóú]+[^\n]*', '', text)
        text = re.sub(r'Autor[a]?:\s*[^\n]+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\(coord\.\)[^\n]*', '', text)
        
        # Menciones de "curso online", "videoclase", etc.
        text = re.sub(r'curso\s+online', '', text, flags=re.IGNORECASE)
        text = re.sub(r'videoclase', '', text, flags=re.IGNORECASE)
        text = re.sub(r'video', '', text, flags=re.IGNORECASE)
        text = re.sub(r'código[s]?\s+qr', '', text, flags=re.IGNORECASE)
        
        # Academias y webs de oposiciones (nombres específicos)
        academias_eliminar = [
            r'TEMA\s+DIGITAL',
            r'Education\s+Factory',
            r'opomania',
            r'opositores\.?net',
            r'TemariooposicionesPDF',
            r'temariooposi\w+',
            r'Administrativo\s+AGE',
            r'ACADEMIA\s+IRIGOYEN',
            r'tu\s+aprobado\s+en\s+un\s+click',
            r'opoesquemas',
            r'Agencia\s+Estatal\s+Boletín\s+Oficial',
            r'cpage\.mpr\.gob\.es',
            r'Catálogo\s+de\s+Publicaciones',
            r'Valorada\s+como\s+la\s+mejor',
            r'Visita\s+nuestra\s+página',
            r'descarga\s+gratis',
            r'preparación\s+de\s+Oposiciones',
        ]
        for pattern in academias_eliminar:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # IDs de documento (varios formatos)
        text = re.sub(r'\b[A-Z]{2,}_[A-Z0-9_]+\b', '', text)  # Como "AD_L_GE_X5200..."
        text = re.sub(r'‐o‐o‐o\d*o‐o‐o‐', '', text)  # Separadores decorativos
        
        # ============================================
        # FASE 2: ANONIMIZAR DATOS PERSONALES
        # ============================================
        
        # Nombres propios (palabras capitalizadas seguidas) - CUIDADO: puede eliminar nombres de leyes
        # Solo aplicar si hay contexto de persona (antes de DNI, después de "D./Dña.")
        text = re.sub(r'(?:D\.|Dña\.|Don|Doña)\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+', '[NOMBRE]', text)
        
        # DNI/NIE
        text = re.sub(r'\b\d{8}[A-Z]\b', '[DNI]', text)
        text = re.sub(r'\b[XYZ]\d{7}[A-Z]\b', '[NIE]', text)
        
        # Teléfonos
        text = re.sub(r'\b[6-9]\d{8}\b', '[TELEFONO]', text)
        text = re.sub(r'\b\+34\s*[6-9]\d{8}\b', '[TELEFONO]', text)
        
        # Emails
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        
        # Números de SS (12 dígitos)
        text = re.sub(r'\b\d{12}\b', '[NUM_SS]', text)
        
        # Direcciones
        text = re.sub(r'\b(?:Calle|C/|Avenida|Avda|Plaza|Pl\.)\s+[^,\n]+(?:,\s*\d+)?', '[DIRECCION]', text)
        
        # Académias restantes
        academias = [
            'Las Cortes', 'GoKoan', 'OpoEsquemas', 'Academia Adams', 'Adams',
            'CEF', 'MAD', 'Educa', 'Centro de Estudios', 'CEDE', 'MasterD',
            'Preparadores', 'Academia', 'Preparador', 'Beatriz Carballo',
            'José Miguel Montalvá', 'Javier Peñafiel', 'Julián Galán'
        ]
        for academia in academias:
            text = re.sub(rf'\b{re.escape(academia)}\b', '[ELIMINADO]', text, flags=re.IGNORECASE)
        
        # Limpiar líneas vacías múltiples
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        text = re.sub(r'^\s+', '', text, flags=re.MULTILINE)
        
        return text.strip()
    
    # Alias para mantener compatibilidad
    def anonymize_text(self, text: str) -> str:
        return self.clean_and_anonymize_text(text)
    
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
        """Crea colección híbrida en Qdrant (dense + sparse)"""
        try:
            self.qdrant.delete_collection(self.collection_name)
            print(f"🗑️  Colección '{self.collection_name}' eliminada")
        except:
            pass
        
        # Colección híbrida: dense + sparse BM25
        self.qdrant.create_collection(
            collection_name=self.collection_name,
            vectors_config={
                "dense": VectorParams(size=1024, distance=Distance.COSINE)
            },
            sparse_vectors_config={
                "text": SparseVectorParams(
                    index=SparseIndexParams(on_disk=False)
                )
            }
        )
        print(f"✅ Colección '{self.collection_name}' creada (híbrida: dense + sparse BM25)")
    
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
                    # Generar embedding dense con sentence-transformers
                    dense_embedding = self.model.encode(chunk['text'], normalize_embeddings=True)
                    
                    # Generar vector sparse BM25
                    sparse_vector = self._generate_sparse_vector(chunk['text'])
                    
                    point = PointStruct(
                        id=point_id,
                        vector={
                            "dense": dense_embedding.tolist(),
                            "text": sparse_vector
                        },
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
        elif 'caso' in filename_lower or 'practico' in filename_lower or 'supuesto' in filename_lower:
            return 'caso_practico'
        elif 'tabla' in filename_lower:
            return 'tabla'
        else:
            return 'otro'

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Indexador de Materiales de Academia')
    parser.add_argument('--dir', type=str, 
                        default='/home/spas/OPOS_GEMINI_1/academias',
                        help='Directorio con materiales de academia')
    parser.add_argument('--exclude', type=str, nargs='*',
                        default=['Del portatil nuevo Voposia', 'temario_oficial'],
                        help='Carpetas a excluir')
    parser.add_argument('--dry-run', action='store_true',
                        help='Solo mostrar qué se procesaría, sin indexar')
    args = parser.parse_args()
    
    print("🚀 Indexador de Materiales de Academia")
    print("=" * 50)
    print(f"📂 Directorio: {args.dir}")
    print(f"🚫 Excluir: {args.exclude}")
    
    materials_dir = Path(args.dir)
    
    if not materials_dir.exists():
        print(f"❌ Error: No se encuentra el directorio {materials_dir}")
        return
    
    # Filtrar archivos excluyendo carpetas
    def should_exclude(path: Path) -> bool:
        for exclude in args.exclude:
            if exclude in str(path):
                return True
        return False
    
    indexer = AcademyMaterialsIndexer()
    
    if args.dry_run:
        # Solo listar archivos
        pdf_files = [f for f in materials_dir.rglob("*.pdf") if not should_exclude(f)]
        docx_files = [f for f in materials_dir.rglob("*.docx") if not should_exclude(f)]
        print(f"\n📄 PDFs encontrados: {len(pdf_files)}")
        print(f"� DOCX encontrados: {len(docx_files)}")
        for f in pdf_files[:10]:
            print(f"  - {f.name}")
        if len(pdf_files) > 10:
            print(f"  ... y {len(pdf_files) - 10} más")
    else:
        indexer.index_materials(str(materials_dir))
    
    print("\n✅ Proceso completado")

if __name__ == "__main__":
    main()
