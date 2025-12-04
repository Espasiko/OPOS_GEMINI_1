#!/bin/bash
# Setup entorno virtual e instalación de dependencias

echo "🔧 Configurando entorno virtual para indexación..."

# Crear entorno virtual si no existe
if [ ! -d "venv_indexer" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv_indexer
    echo "✅ Entorno virtual creado"
else
    echo "✅ Entorno virtual ya existe"
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source venv_indexer/bin/activate

# Actualizar pip
echo "📦 Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install sentence-transformers
pip install qdrant-client
pip install PyMuPDF
pip install torch --index-url https://download.pytorch.org/whl/cpu

echo ""
echo "✅ Instalación completada!"
echo ""
echo "Verificando instalación..."
python dataset_generator/test_dependencies.py

echo ""
echo "🎯 Para usar el indexador, activa el entorno virtual con:"
echo "   source venv_indexer/bin/activate"
