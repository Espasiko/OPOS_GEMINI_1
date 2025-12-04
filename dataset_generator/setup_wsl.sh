#!/bin/bash
# Script de configuración para WSL

echo "🚀 Configurando Pipeline Seguro en WSL"
echo "========================================"
echo ""

# Verificar si estamos en WSL
if ! grep -qi microsoft /proc/version; then
    echo "⚠️  Este script debe ejecutarse en WSL"
    exit 1
fi

echo "✅ Ejecutando en WSL"

# 1. Verificar/Instalar Ollama
echo ""
echo "📦 Verificando Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "   Instalando Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
else
    echo "   ✅ Ollama ya instalado"
fi

# 2. Iniciar Ollama si no está corriendo
echo ""
echo "🔄 Verificando servicio Ollama..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "   Iniciando Ollama..."
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
    echo "   ✅ Ollama iniciado"
else
    echo "   ✅ Ollama ya está corriendo"
fi

# 3. Descargar modelo Mistral
echo ""
echo "📥 Verificando modelo Mistral..."
if ! ollama list | grep -q "mistral"; then
    echo "   Descargando Mistral (esto puede tardar varios minutos)..."
    ollama pull mistral
    echo "   ✅ Mistral descargado"
else
    echo "   ✅ Mistral ya disponible"
fi

# 4. Verificar Qdrant
echo ""
echo "🗄️  Verificando Qdrant..."
if curl -s http://localhost:6333/collections > /dev/null 2>&1; then
    echo "   ✅ Qdrant está corriendo"
else
    echo "   ⚠️  Qdrant no está disponible"
    echo "   Ejecuta: docker-compose up -d"
fi

# 5. Instalar dependencias Python
echo ""
echo "🐍 Instalando dependencias Python..."
pip3 install -q PyPDF2 requests 2>/dev/null || pip install -q PyPDF2 requests
echo "   ✅ Dependencias instaladas"

# 6. Crear directorios
echo ""
echo "📁 Creando directorios..."
mkdir -p dataset_output_seguro
mkdir -p logs
echo "   ✅ Directorios creados"

# 7. Test de conexión
echo ""
echo "🧪 Probando conexiones..."

# Test Ollama
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "   ✅ Ollama: OK"
else
    echo "   ❌ Ollama: FALLO"
fi

# Test Qdrant
if curl -s http://localhost:6333/collections > /dev/null 2>&1; then
    echo "   ✅ Qdrant: OK"
else
    echo "   ⚠️  Qdrant: No disponible"
fi

echo ""
echo "========================================"
echo "✅ Configuración completada"
echo ""
echo "📋 Próximos pasos:"
echo "   1. Si Qdrant no está corriendo:"
echo "      docker-compose up -d"
echo ""
echo "   2. Ejecutar prueba de 20 preguntas:"
echo "      python3 dataset_generator/pipeline_seguro_local.py"
echo ""
echo "   3. Revisar resultados en:"
echo "      dataset_output_seguro/test_20_preguntas.json"
echo ""
