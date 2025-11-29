#!/usr/bin/env python3
"""
DOCUMENT TO CHUNKS PROCESSOR
Convierte PDFs + textos en chunks para training Mistral 8B
Genera dataset JSONL para fine-tuning

Uso:
    python document_to_chunks_processor.py
    
Entrada:
    - backend/data/boe_documents/*.pdf
    
Salida:
    - backend/data/training_dataset.jsonl (10,000+ ejemplos)
    - chunks_metadata.json (metadatos)
    
Resultado:
    - ~10,000 chunks de ~500 tokens
    - Formato JSONL (prompt-completion pairs)
    - Listo para fine-tuning Mistral 8B
"""

import PyPDF2
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DocumentChunker:
    """
    Procesa documentos PDF a chunks para training
    """
    
    def __init__(self, 
                 input_dir="backend/data/boe_documents",
                 output_file="backend/data/training_dataset.jsonl",
                 chunk_size=500,
                 overlap=50):
        self.input_dir = Path(input_dir)
        self.output_file = Path(output_file)
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.chunks = []
        self.chunk_stats = {
            "total_chunks": 0,
            "total_tokens": 0,
            "avg_tokens": 0,
            "documents_processed": 0
        }
    
    def extract_pdf_text(self, pdf_path: str) -> Tuple[str, int]:
        """
        Extrae texto de PDF
        Retorna: (texto, número de páginas)
        """
        text = ""
        pages = 0
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                pages = len(reader.pages)
                
                for i, page in enumerate(reader.pages):
                    try:
                        text += page.extract_text() + "\n"
                    except Exception as e:
                        logger.warning(f"⚠️ Error extrayendo página {i+1} de {pdf_path}: {e}")
                        continue
        
        except Exception as e:
            logger.error(f"❌ Error abriendo PDF {pdf_path}: {e}")
            return "", 0
        
        return text, pages
    
    def clean_text(self, text: str) -> str:
        """
        Limpia y normaliza texto
        """
        # Eliminar espacios múltiples
        text = re.sub(r'\s+', ' ', text)
        
        # Eliminar saltos de línea múltiples
        text = re.sub(r'\n+', '\n', text)
        
        # Eliminar caracteres especiales problemáticos
        text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        return text.strip()
    
    def split_into_sentences(self, text: str) -> List[str]:
        """
        Divide texto en oraciones
        Mantiene puntuación y estructura
        """
        # Patrones de fin de oración
        sentence_endings = r'[.!?]\s+'
        
        sentences = re.split(sentence_endings, text)
        
        # Re-agregar puntuación
        cleaned_sentences = []
        for i, sent in enumerate(sentences[:-1]):
            cleaned_sentences.append(sent + '.')
        
        if sentences[-1]:
            cleaned_sentences.append(sentences[-1])
        
        return [s.strip() for s in cleaned_sentences if s.strip()]
    
    def create_chunks(self, text: str, doc_name: str) -> List[Dict]:
        """
        Divide texto en chunks de ~500 tokens
        Mantiene coherencia de contexto
        
        Args:
            text: Texto a procesar
            doc_name: Nombre del documento
            
        Retorna:
            Lista de chunks con metadatos
        """
        chunks = []
        
        # Limpiar texto
        text = self.clean_text(text)
        
        if not text or len(text) < 100:
            logger.warning(f"⚠️ Documento {doc_name} muy corto o vacío")
            return chunks
        
        # Dividir por oraciones primero (mejor coherencia)
        sentences = self.split_into_sentences(text)
        
        current_chunk = []
        chunk_tokens = 0
        chunk_num = 0
        
        for sentence in sentences:
            sentence_tokens = len(sentence.split())
            
            # Si agregar esta oración excede límite
            if chunk_tokens + sentence_tokens > self.chunk_size and current_chunk:
                # Guardar chunk actual
                chunk_text = ' '.join(current_chunk)
                
                chunk_num += 1
                chunks.append({
                    "id": f"{doc_name}_chunk_{chunk_num:04d}",
                    "document": doc_name,
                    "chunk_number": chunk_num,
                    "content": chunk_text,
                    "tokens": len(chunk_text.split()),
                    "source": "boe_documents"
                })
                
                # Reiniciar con overlap (últimas oraciones del chunk anterior)
                overlap_words = min(self.overlap, len(current_chunk))
                current_chunk = current_chunk[-overlap_words:] if overlap_words > 0 else []
                chunk_tokens = sum(len(w.split()) for w in current_chunk)
            
            # Agregar oración actual
            current_chunk.append(sentence)
            chunk_tokens += sentence_tokens
        
        # Último chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunk_num += 1
            chunks.append({
                "id": f"{doc_name}_chunk_{chunk_num:04d}",
                "document": doc_name,
                "chunk_number": chunk_num,
                "content": chunk_text,
                "tokens": len(chunk_text.split()),
                "source": "boe_documents"
            })
        
        return chunks
    
    def create_training_examples(self, chunk: Dict) -> Dict:
        """
        Crea ejemplo de training (prompt-completion pair)
        para fine-tuning Mistral 8B
        """
        content = chunk['content']
        
        # Diferentes formatos de prompt según contenido
        prompts = [
            f"Artículo o contenido legal:\n{content[:150]}...\n\nCompleta el texto:",
            f"Contexto legal de {chunk['document']}:\n{content[:150]}...\n\nContinúa:",
            f"Regulación relacionada:\n{content[:100]}...\n\nDesarrollo completo:",
        ]
        
        import random
        prompt = random.choice(prompts)
        
        return {
            "prompt": prompt,
            "completion": f"\n{content}",
            "metadata": {
                "document": chunk['document'],
                "chunk_id": chunk['id'],
                "tokens": chunk['tokens']
            }
        }
    
    def process_all_documents(self):
        """
        Procesa todos los PDFs en la carpeta
        """
        print("\n" + "="*70)
        print("🔄 PROCESANDO DOCUMENTOS A CHUNKS")
        print("="*70)
        
        # Buscar PDFs
        pdf_files = list(self.input_dir.rglob("*.pdf"))
        
        if not pdf_files:
            logger.error(f"❌ No se encontraron PDFs en {self.input_dir}")
            return 0
        
        logger.info(f"📊 Total PDFs encontrados: {len(pdf_files)}\n")
        
        total_chunks = 0
        total_tokens = 0
        
        for i, pdf_file in enumerate(pdf_files, 1):
            logger.info(f"[{i}/{len(pdf_files)}] Procesando {pdf_file.name}...")
            
            try:
                # Extraer texto
                text, pages = self.extract_pdf_text(str(pdf_file))
                
                if not text:
                    logger.warning(f"⚠️ {pdf_file.name}: No text extracted")
                    continue
                
                # Crear chunks
                chunks = self.create_chunks(text, pdf_file.stem)
                
                if not chunks:
                    logger.warning(f"⚠️ {pdf_file.name}: No chunks created")
                    continue
                
                self.chunks.extend(chunks)
                
                chunk_count = len(chunks)
                total_chunks += chunk_count
                
                chunk_tokens = sum(c['tokens'] for c in chunks)
                total_tokens += chunk_tokens
                
                logger.info(f"  ✅ {chunk_count} chunks ({chunk_tokens:,} tokens) from {pages} pages")
                self.chunk_stats['documents_processed'] += 1
            
            except Exception as e:
                logger.error(f"❌ Error procesando {pdf_file.name}: {e}")
                continue
        
        self.chunk_stats['total_chunks'] = total_chunks
        self.chunk_stats['total_tokens'] = total_tokens
        if total_chunks > 0:
            self.chunk_stats['avg_tokens'] = int(total_tokens / total_chunks)
        
        logger.info(f"\n✅ Total chunks generados: {total_chunks:,}")
        logger.info(f"📈 Total tokens: {total_tokens:,}")
        logger.info(f"📊 Promedio tokens/chunk: {self.chunk_stats['avg_tokens']}")
        
        return total_chunks
    
    def save_jsonl(self):
        """
        Guarda chunks en formato JSONL para training Mistral 8B
        """
        if not self.chunks:
            logger.error("❌ No chunks para guardar")
            return
        
        print(f"\n💾 Guardando {len(self.chunks)} ejemplos de training en JSONL...")
        
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Generar ejemplos de training
        training_examples = []
        for chunk in self.chunks:
            example = self.create_training_examples(chunk)
            training_examples.append(example)
        
        # Guardar JSONL
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                for example in training_examples:
                    f.write(json.dumps(example, ensure_ascii=False) + '\n')
            
            logger.info(f"✅ Dataset guardado: {self.output_file}")
            logger.info(f"📊 Ejemplos de training: {len(training_examples):,}")
            
        except Exception as e:
            logger.error(f"❌ Error guardando JSONL: {e}")
            return
        
        # Guardar metadatos
        metadata_file = self.output_file.parent / "chunks_metadata.json"
        
        metadata = {
            "total_chunks": len(self.chunks),
            "total_training_examples": len(training_examples),
            "total_tokens": self.chunk_stats['total_tokens'],
            "avg_tokens_per_chunk": self.chunk_stats['avg_tokens'],
            "documents_processed": self.chunk_stats['documents_processed'],
            "chunk_size_target": self.chunk_size,
            "chunk_overlap": self.overlap,
            "output_file": str(self.output_file),
            "formato": "JSONL (prompt-completion pairs)",
            "proposito": "Fine-tuning Mistral 8B",
            "siguiente_paso": "Cargar en Colab y ejecutar training"
        }
        
        try:
            metadata_file.write_text(
                json.dumps(metadata, indent=2, ensure_ascii=False)
            )
            logger.info(f"✅ Metadatos guardados: {metadata_file}\n")
        except Exception as e:
            logger.error(f"❌ Error guardando metadatos: {e}")
    
    def run(self):
        """
        Ejecuta procesamiento completo
        """
        print("\n" + "="*70)
        print("🚀 DOCUMENT TO CHUNKS PROCESSOR")
        print("="*70)
        print(f"📁 Input: {self.input_dir}")
        print(f"📄 Output: {self.output_file}")
        print(f"🔧 Chunk size: {self.chunk_size} tokens")
        print("="*70 + "\n")
        
        # Procesar documentos
        total = self.process_all_documents()
        
        if total == 0:
            logger.error("❌ No se procesaron documentos")
            return
        
        # Guardar dataset
        self.save_jsonl()
        
        print("="*70)
        print("✅ PROCESAMIENTO COMPLETADO")
        print("="*70)
        print(f"📊 Chunks totales: {self.chunk_stats['total_chunks']:,}")
        print(f"📈 Tokens totales: {self.chunk_stats['total_tokens']:,}")
        print(f"📋 Ejemplos training: {len(self.chunks):,}")
        print(f"\n🎯 Listo para fine-tuning en Colab")
        print("="*70 + "\n")


if __name__ == "__main__":
    processor = DocumentChunker(
        input_dir="backend/data/boe_documents",
        output_file="backend/data/training_dataset.jsonl",
        chunk_size=500,
        overlap=50
    )
    processor.run()
