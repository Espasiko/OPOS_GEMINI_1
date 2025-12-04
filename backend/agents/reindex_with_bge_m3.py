#!/usr/bin/env python3
"""
Re-indexa Qdrant con modelo de embeddings mejorado
littlejohn-ai/bge-m3-spa-law-qa
"""

import os
import sys
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import PyPDF2
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

load_dotenv()
console = Console()

class QdrantReindexer:
    """Re-indexa Qdrant con embeddings mejorados"""
    
    def __init__(self):
        # Nuevo modelo de embeddings
        console.print("[cyan]Cargando modelo bge-m3-spa-law-qa...[/cyan]")
        self.model = SentenceTransformer("littlejohn-ai/bge-m3-spa-law-qa")
        console.print("[green]✓ Modelo cargado (1024 dims, 8192 tokens)[/green]\n")
        
        # Cliente Qdrant
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        
        self.collection_name = "leyes_seguridad_social_v2"
        self.chunk_size = 1000
        self.chunk_overlap = 200
    
    def create_collection(self):
        """Crea colección nueva con dimensión 1024"""
        console.print(f"[cyan]Creando colección: {self.collection_name}[/cyan]")
        
        try:
            self.client.delete_collection(self.collection_name)
            console.print("[yellow]Colección anterior eliminada[/yellow]")
        except:
            pass
        
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=1024,  # Nueva dimensión
                distance=Distance.COSINE
            )
        )
        console.print("[green]✓ Colección creada[/green]\n")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extrae texto de PDF"""
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def chunk_text(self, text: str, metadata: Dict) -> List[Dict]:
        """Divide texto en chunks"""
        chunks = []
        words = text.split()
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            
            if len(chunk_text) > 100:  # Mínimo 100 caracteres
                chunks.append({
                    "text": chunk_text,
                    "metadata": {
                        **metadata,
                        "chunk_index": len(chunks),
                        "chunk_size": len(chunk_text)
                    }
                })
        
        return chunks
    
    def index_pdf(self, pdf_path: Path, ley_info: Dict):
        """Indexa un PDF completo"""
        console.print(f"[bold cyan]📄 {ley_info['nombre']}[/bold cyan]")
        console.print(f"   {ley_info['descripcion']}")
        
        # Extraer texto
        text = self.extract_text_from_pdf(str(pdf_path))
        console.print(f"   Texto extraído: {len(text):,} caracteres")
        
        # Crear chunks
        chunks = self.chunk_text(text, {
            "ley": ley_info['nombre'],
            "boe_id": ley_info['boe_id'],
            "descripcion": ley_info['descripcion'],
            "source": str(pdf_path)
        })
        console.print(f"   Chunks creados: {len(chunks)}")
        
        # Generar embeddings
        console.print(f"   Generando embeddings...")
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.model.encode(texts, show_progress_bar=False)
        
        # Crear points para Qdrant
        points = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            points.append(PointStruct(
                id=hash(f"{ley_info['nombre']}_{i}") % (2**63),
                vector=embedding.tolist(),
                payload={
                    "text": chunk["text"],
                    **chunk["metadata"]
                }
            ))
        
        # Subir a Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        console.print(f"   [green]✓ {len(points)} chunks indexados[/green]\n")
        
        return len(points)
    
    def reindex_all(self):
        """Re-indexa todas las leyes"""
        leyes_dir = Path("backend/data/leyes")
        
        if not leyes_dir.exists():
            console.print("[red]Error: Directorio backend/data/leyes no existe[/red]")
            console.print("[yellow]Ejecuta primero: python backend/agents/boe_downloader.py[/yellow]")
            return
        
        # Lista de leyes principales
        leyes = [
            {
                "nombre": "LGSS",
                "boe_id": "BOE-A-2015-11724",
                "descripcion": "Ley General de la Seguridad Social"
            },
            {
                "nombre": "Ley_39_2015",
                "boe_id": "BOE-A-2015-10565",
                "descripcion": "Procedimiento Administrativo Común"
            },
            {
                "nombre": "Ley_40_2015",
                "boe_id": "BOE-A-2015-10566",
                "descripcion": "Régimen Jurídico del Sector Público"
            },
            {
                "nombre": "EBEP",
                "boe_id": "BOE-A-2015-11719",
                "descripcion": "Estatuto Básico del Empleado Público"
            },
            {
                "nombre": "RD_Recaudacion",
                "boe_id": "BOE-A-2004-11836",
                "descripcion": "Reglamento General de Recaudación SS"
            },
            {
                "nombre": "RD_Afiliacion",
                "boe_id": "BOE-A-1996-4447",
                "descripcion": "Reglamento de Afiliación, Altas y Bajas"
            },
            {
                "nombre": "Ley_IMV",
                "boe_id": "BOE-A-2021-21007",
                "descripcion": "Ley del Ingreso Mínimo Vital"
            },
            {
                "nombre": "LOPDGDD",
                "boe_id": "BOE-A-2018-16673",
                "descripcion": "Ley Orgánica de Protección de Datos"
            }
        ]
        
        console.print("\n" + "="*60)
        console.print("[bold blue]🔄 RE-INDEXACIÓN CON BGE-M3-SPA-LAW-QA[/bold blue]")
        console.print("="*60 + "\n")
        
        # Crear colección
        self.create_collection()
        
        # Indexar cada ley
        total_chunks = 0
        start_time = time.time()
        
        for ley in leyes:
            pdf_path = leyes_dir / f"{ley['nombre']}.pdf"
            
            if not pdf_path.exists():
                console.print(f"[yellow]⚠ {ley['nombre']}.pdf no encontrado[/yellow]\n")
                continue
            
            try:
                chunks = self.index_pdf(pdf_path, ley)
                total_chunks += chunks
            except Exception as e:
                console.print(f"[red]✗ Error: {e}[/red]\n")
        
        duration = time.time() - start_time
        
        # Resumen
        console.print("="*60)
        console.print("[bold green]✅ RE-INDEXACIÓN COMPLETADA[/bold green]")
        console.print("="*60)
        console.print(f"Colección: {self.collection_name}")
        console.print(f"Modelo: littlejohn-ai/bge-m3-spa-law-qa")
        console.print(f"Dimensión: 1024")
        console.print(f"Total chunks: {total_chunks:,}")
        console.print(f"Tiempo: {duration/60:.1f} minutos")
        console.print(f"\n[cyan]Próximo paso:[/cyan]")
        console.print(f"Actualizar backend/agents/rag_agent_v2.py para usar:")
        console.print(f"  - collection_name = '{self.collection_name}'")
        console.print(f"  - model = 'littlejohn-ai/bge-m3-spa-law-qa'")


if __name__ == "__main__":
    reindexer = QdrantReindexer()
    reindexer.reindex_all()
