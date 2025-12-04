#!/bin/bash
# Instalación de dependencias para indexación con BGE-M3

echo "🔧 Instalando dependencias para indexación..."

# Actualizar pip
echo "📦 Actualizando pip..."
pip3 install --upgrade pip

# Instalar dependencias principales
echo "📥 Instalando sentence-transformers (BGE-M3)..."
pip3 install sentence-transformers

echo "📥 Instalando qdrant-client..."
pip3 install qdrant-client

echo "📥 Instalando PyMuPDF (para PDFs)..."
pip3 install PyMuPDF

echo "📥 Instalando torch (si no está)..."
pip3 install torch --index-url https://download.pytorch.org/whl/cpu

echo ""
echo "✅ Instalación completada!"
echo ""
echo "Verificando instalación..."
python3 dataset_generator/test_dependencies.py
