#!/bin/bash
# Script de configuración para pipeline Ollama

echo "🚀 Configurando pipeline de generación con Ollama"
echo ""

# Verificar si Ollama está instalado
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama no está instalado"
    echo "   Instala desde: https://ollama.ai"
    exit 1
fi

echo "✅ Ollama instalado"

# Verificar si Ollama está corriendo
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama no está corriendo"
    echo "   Ejecuta en otra terminal: ollama serve"
    echo ""
    read -p "¿Quieres que lo inicie ahora? (s/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        ollama serve &
        sleep 3
    else
        exit 1
    fi
fi

echo "✅ Ollama corriendo"

# Verificar si Mistral está descargado
if ! ollama list | grep -q "mistral"; then
    echo "📥 Descargando modelo Mistral..."
    ollama pull mistral
fi

echo "✅ Modelo Mistral disponible"

# Instalar dependencias Python
echo "📦 Instalando dependencias Python..."
pip install -q PyPDF2 requests

echo "✅ Dependencias instaladas"

# Crear directorios necesarios
mkdir -p dataset_output
mkdir -p logs

echo ""
echo "✅ Configuración completada"
echo ""
echo "📋 Próximos pasos:"
echo "   1. Analizar duplicados: python dataset_generator/analyze_duplicates.py"
echo "   2. Ejecutar pipeline: python dataset_generator/pipeline_ollama_local.py"
echo ""
