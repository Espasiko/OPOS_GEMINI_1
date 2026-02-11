#!/usr/bin/env python3
"""
MCP Server: Qdrant Memory con Embeddings Locales
100% GRATIS - Usa modelo bge-m3-spa-law-qa local
Compatible con Model Context Protocol (MCP)
"""

import json
import sys
import hashlib
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

class QdrantMemoryLocal:
    def __init__(self):
        """Inicializar MCP Server con Qdrant local y modelo local"""
        # Modelo local (sin OpenAI)
        print("🔄 Cargando modelo bge-m3-spa-law-qa...", file=sys.stderr)
        self.model = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
        
        # Qdrant local
        print("🔄 Conectando a Qdrant local...", file=sys.stderr)
        self.client = QdrantClient(url="http://localhost:6333")
        self.collection = "opositaia_memory_mcp"
        
        # Crear colección si no existe
        self._ensure_collection()
        print("✅ MCP Server inicializado", file=sys.stderr)
    
    def _ensure_collection(self):
        """Crear colección si no existe"""
        try:
            self.client.get_collection(self.collection)
            print(f"✅ Colección '{self.collection}' encontrada", file=sys.stderr)
        except:
            print(f"🔄 Creando colección '{self.collection}'...", file=sys.stderr)
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=1024,  # bge-m3 dimension
                    distance=Distance.COSINE
                )
            )
            print(f"✅ Colección '{self.collection}' creada", file=sys.stderr)
    
    def add_memory(self, text: str, metadata: Dict[str, Any] = None) -> str:
        """
        MCP Tool: Añadir memoria
        
        Args:
            text: Texto a guardar en memoria
            metadata: Metadatos adicionales (dict)
        
        Returns:
            ID de la memoria guardada
        """
        print(f"🔄 Añadiendo memoria: {text[:50]}...", file=sys.stderr)
        
        # Generar embedding
        embedding = self.model.encode(text).tolist()
        
        # Generar ID único
        memory_id = hashlib.md5(text.encode()).hexdigest()
        
        # Guardar en Qdrant
        self.client.upsert(
            collection_name=self.collection,
            points=[PointStruct(
                id=memory_id,
                vector=embedding,
                payload={
                    "text": text,
                    **(metadata or {})
                }
            )]
        )
        
        print(f"✅ Memoria guardada: {memory_id}", file=sys.stderr)
        return memory_id
    
    def search_memory(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        MCP Tool: Buscar en memoria
        
        Args:
            query: Query de búsqueda
            limit: Número máximo de resultados
        
        Returns:
            Lista de memorias encontradas
        """
        print(f"🔍 Buscando: {query}", file=sys.stderr)
        
        # Generar embedding de query
        query_vector = self.model.encode(query).tolist()
        
        # Buscar en Qdrant
        results = self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            limit=limit,
            score_threshold=0.7
        )
        
        memories = [
            {
                "id": hit.id,
                "score": hit.score,
                "text": hit.payload.get("text"),
                "metadata": {k: v for k, v in hit.payload.items() if k != "text"}
            }
            for hit in results
        ]
        
        print(f"✅ Encontradas {len(memories)} memorias", file=sys.stderr)
        return memories
    
    def clear_memory(self):
        """
        MCP Tool: Limpiar toda la memoria
        """
        print("🗑️  Limpiando memoria...", file=sys.stderr)
        self.client.delete_collection(self.collection)
        self._ensure_collection()
        print("✅ Memoria limpiada", file=sys.stderr)
        return {"status": "cleared"}
    
    def get_stats(self):
        """
        MCP Tool: Obtener estadísticas de memoria
        """
        try:
            collection_info = self.client.get_collection(self.collection)
            return {
                "collection": self.collection,
                "points_count": collection_info.points_count,
                "vectors_count": collection_info.vectors_count,
                "status": "active"
            }
        except Exception as e:
            return {
                "collection": self.collection,
                "error": str(e),
                "status": "error"
            }
    
    def handle_mcp_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handler MCP estándar
        """
        method = request.get("method")
        params = request.get("params", {})
        
        try:
            if method == "add_memory":
                memory_id = self.add_memory(
                    text=params.get("text", ""),
                    metadata=params.get("metadata", {})
                )
                return {"result": {"id": memory_id, "status": "success"}}
            
            elif method == "search_memory":
                results = self.search_memory(
                    query=params.get("query", ""),
                    limit=params.get("limit", 5)
                )
                return {"result": results}
            
            elif method == "clear_memory":
                result = self.clear_memory()
                return {"result": result}
            
            elif method == "get_stats":
                stats = self.get_stats()
                return {"result": stats}
            
            else:
                return {"error": f"Unknown method: {method}"}
        
        except Exception as e:
            print(f"❌ Error: {e}", file=sys.stderr)
            return {"error": str(e)}

def main():
    """
    MCP Server main loop
    Lee requests de stdin y escribe responses a stdout
    """
    print("🚀 Iniciando Qdrant Memory MCP Server...", file=sys.stderr)
    server = QdrantMemoryLocal()
    
    print("📡 Esperando requests MCP...", file=sys.stderr)
    
    # Leer requests de stdin (protocolo MCP)
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            response = server.handle_mcp_request(request)
            print(json.dumps(response))
            sys.stdout.flush()
        except json.JSONDecodeError as e:
            error_response = {"error": f"Invalid JSON: {e}"}
            print(json.dumps(error_response))
            sys.stdout.flush()
        except Exception as e:
            error_response = {"error": str(e)}
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
