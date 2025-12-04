#!/usr/bin/env python3
"""Test de dependencias"""

print("Verificando dependencias...")

try:
    from sentence_transformers import SentenceTransformer
    print("✅ sentence-transformers instalado")
except ImportError:
    print("❌ sentence-transformers NO instalado")
    print("   Instalar con: pip install sentence-transformers")

try:
    from qdrant_client import QdrantClient
    print("✅ qdrant-client instalado")
except ImportError:
    print("❌ qdrant-client NO instalado")
    print("   Instalar con: pip install qdrant-client")

try:
    import fitz
    print("✅ PyMuPDF instalado")
except ImportError:
    print("❌ PyMuPDF NO instalado")
    print("   Instalar con: pip install PyMuPDF")

print("\nTodas las dependencias verificadas!")
