#!/usr/bin/env python3
"""
MCP Server: Grafo de Conocimiento Legal
100% GRATIS - SQLite + Qdrant local
Compatible con Model Context Protocol (MCP)
"""

import json
import sys
import sqlite3
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

class LegalGraphMCP:
    def __init__(self):
        """Inicializar MCP Server con SQLite y Qdrant"""
        # SQLite para grafo (relaciones)
        self.db_path = "/home/spas/.opositaia/legal_graph.db"
        print(f"🔄 Conectando a SQLite: {self.db_path}", file=sys.stderr)
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()
        
        # Qdrant para búsqueda semántica
        print("🔄 Conectando a Qdrant local...", file=sys.stderr)
        self.qdrant = QdrantClient(url="http://localhost:6333")
        
        # Modelo local
        print("🔄 Cargando modelo bge-m3...", file=sys.stderr)
        self.model = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
        
        print("✅ Legal Graph MCP Server inicializado", file=sys.stderr)
    
    def _init_db(self):
        """Crear tablas del grafo"""
        cursor = self.conn.cursor()
        
        # Tabla de entidades (artículos)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS entities (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                metadata TEXT
            )
        """)
        
        # Tabla de relaciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS relations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_id TEXT NOT NULL,
                to_id TEXT NOT NULL,
                relation_type TEXT NOT NULL,
                metadata TEXT,
                FOREIGN KEY (from_id) REFERENCES entities(id),
                FOREIGN KEY (to_id) REFERENCES entities(id)
            )
        """)
        
        self.conn.commit()
        print("✅ Tablas del grafo creadas/verificadas", file=sys.stderr)
    
    def add_entity(self, entity_id: str, entity_type: str, name: str, 
                   description: str = None, metadata: Dict = None) -> str:
        """
        MCP Tool: Añadir entidad al grafo
        """
        print(f"🔄 Añadiendo entidad: {entity_id}", file=sys.stderr)
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO entities (id, type, name, description, metadata)
            VALUES (?, ?, ?, ?, ?)
        """, (entity_id, entity_type, name, description, json.dumps(metadata or {})))
        self.conn.commit()
        print(f"✅ Entidad añadida: {entity_id}", file=sys.stderr)
        return entity_id
    
    def add_relation(self, from_id: str, to_id: str, relation_type: str,
                     metadata: Dict = None) -> int:
        """
        MCP Tool: Añadir relación entre entidades
        """
        print(f"🔄 Añadiendo relación: {from_id} --[{relation_type}]--> {to_id}", file=sys.stderr)
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO relations (from_id, to_id, relation_type, metadata)
            VALUES (?, ?, ?, ?)
        """, (from_id, to_id, relation_type, json.dumps(metadata or {})))
        self.conn.commit()
        relation_id = cursor.lastrowid
        print(f"✅ Relación añadida: ID {relation_id}", file=sys.stderr)
        return relation_id
    
    def get_related(self, entity_id: str, relation_type: str = None) -> List[Dict]:
        """
        MCP Tool: Obtener entidades relacionadas
        """
        print(f"🔍 Buscando entidades relacionadas con: {entity_id}", file=sys.stderr)
        cursor = self.conn.cursor()
        
        if relation_type:
            query = """
                SELECT e.*, r.relation_type
                FROM entities e
                JOIN relations r ON e.id = r.to_id
                WHERE r.from_id = ? AND r.relation_type = ?
            """
            cursor.execute(query, (entity_id, relation_type))
        else:
            query = """
                SELECT e.*, r.relation_type
                FROM entities e
                JOIN relations r ON e.id = r.to_id
                WHERE r.from_id = ?
            """
            cursor.execute(query, (entity_id,))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "id": row[0],
                "type": row[1],
                "name": row[2],
                "description": row[3],
                "metadata": json.loads(row[4]) if row[4] else {},
                "relation_type": row[5]
            })
        
        print(f"✅ Encontradas {len(results)} entidades relacionadas", file=sys.stderr)
        return results
    
    def search_entities(self, query: str, entity_type: str = None, 
                        limit: int = 5) -> List[Dict]:
        """
        MCP Tool: Buscar entidades (SQLite)
        """
        print(f"🔍 Buscando entidades: {query}", file=sys.stderr)
        cursor = self.conn.cursor()
        
        # Búsqueda SQL básica
        if entity_type:
            sql_query = """
                SELECT * FROM entities 
                WHERE type = ? AND (name LIKE ? OR description LIKE ?)
                LIMIT ?
            """
            cursor.execute(sql_query, (entity_type, f"%{query}%", f"%{query}%", limit))
        else:
            sql_query = """
                SELECT * FROM entities 
                WHERE name LIKE ? OR description LIKE ?
                LIMIT ?
            """
            cursor.execute(sql_query, (f"%{query}%", f"%{query}%", limit))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "id": row[0],
                "type": row[1],
                "name": row[2],
                "description": row[3],
                "metadata": json.loads(row[4]) if row[4] else {}
            })
        
        print(f"✅ Encontradas {len(results)} entidades", file=sys.stderr)
        return results
    
    def populate_legal_structure(self) -> Dict:
        """
        MCP Tool: Poblar estructura legal del TRLGSS
        """
        print("🔄 Poblando estructura legal...", file=sys.stderr)
        
        # Artículos principales
        articles = [
            ("Art. 173", "articulo", "Artículo 173 TRLGSS", "Incapacidad Temporal"),
            ("Art. 173.1", "subarticulo", "Artículo 173.1 TRLGSS", "Definición IT"),
            ("Art. 173.2", "subarticulo", "Artículo 173.2 TRLGSS", "Contingencias IT"),
            ("Art. 174", "articulo", "Artículo 174 TRLGSS", "Prestación económica IT"),
            ("Art. 174.1", "subarticulo", "Artículo 174.1 TRLGSS", "Subsidio diario"),
            ("Art. 174.2", "subarticulo", "Artículo 174.2 TRLGSS", "Porcentajes subsidio"),
        ]
        
        for art_id, art_type, name, desc in articles:
            self.add_entity(art_id, art_type, name, desc)
        
        # Relaciones
        relations = [
            ("Art. 173", "Art. 173.1", "contiene"),
            ("Art. 173", "Art. 173.2", "contiene"),
            ("Art. 174", "Art. 174.1", "contiene"),
            ("Art. 174", "Art. 174.2", "contiene"),
            ("Art. 173.1", "Art. 174.2", "complementa"),
            ("Art. 173", "Art. 174", "relacionado_con"),
        ]
        
        for from_id, to_id, rel_type in relations:
            self.add_relation(from_id, to_id, rel_type)
        
        result = {
            "status": "populated",
            "entities": len(articles),
            "relations": len(relations)
        }
        
        print(f"✅ Estructura poblada: {len(articles)} entidades, {len(relations)} relaciones", file=sys.stderr)
        return result
    
    def get_stats(self):
        """
        MCP Tool: Obtener estadísticas del grafo
        """
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM entities")
        entities_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM relations")
        relations_count = cursor.fetchone()[0]
        
        return {
            "database": self.db_path,
            "entities_count": entities_count,
            "relations_count": relations_count,
            "status": "active"
        }
    
    def handle_mcp_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handler MCP estándar"""
        method = request.get("method")
        params = request.get("params", {})
        
        try:
            if method == "add_entity":
                result = self.add_entity(**params)
                return {"result": {"id": result, "status": "success"}}
            
            elif method == "add_relation":
                result = self.add_relation(**params)
                return {"result": {"id": result, "status": "success"}}
            
            elif method == "get_related":
                result = self.get_related(**params)
                return {"result": result}
            
            elif method == "search_entities":
                result = self.search_entities(**params)
                return {"result": result}
            
            elif method == "populate_legal_structure":
                result = self.populate_legal_structure()
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
    """MCP Server main loop"""
    print("🚀 Iniciando Legal Graph MCP Server...", file=sys.stderr)
    server = LegalGraphMCP()
    
    print("📡 Esperando requests MCP...", file=sys.stderr)
    
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
