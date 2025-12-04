#!/bin/bash
# Pipeline completo para generar ~5,000 Q&A con Mistral en WSL
# Tiempo estimado: 6-10 horas

set -e  # Salir si hay error

echo "🚀 Pipeline Completo de Generación de Dataset Q&A"
echo "=================================================="
echo ""

# Verificar que estamos en WSL
if ! grep -qi microsoft /proc/version; then
    echo "❌ Este script debe ejecutarse en WSL"
    exit 1
fi

# Directorio base
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Verificar venv
if [ ! -d "venv" ]; then
    echo "❌ No se encontró venv en dataset_generator/"
    echo "   Ejecuta primero: python3 -m venv venv"
    exit 1
fi

# Activar venv
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Verificar dependencias
echo "📦 Verificando dependencias..."
pip install -q -r requirements.txt

# Verificar Ollama
echo "🤖 Verificando Ollama..."
if ! ollama list &> /dev/null; then
    echo "❌ Ollama no está disponible"
    echo "   Ejecuta en otra terminal: ollama serve"
    exit 1
fi

# Verificar modelo Mistral
if ! ollama list | grep -q "mistral"; then
    echo "📥 Descargando modelo Mistral..."
    ollama pull mistral
fi

echo "✅ Todo listo para comenzar"
echo ""

# Opción de pipeline
echo "Selecciona el pipeline a ejecutar:"
echo "1) Pipeline Básico (pipeline_ollama_local.py)"
echo "2) Pipeline Seguro con Qdrant (pipeline_seguro_local.py) - RECOMENDADO"
echo ""
read -p "Opción [1-2]: " OPCION

case $OPCION in
    1)
        echo ""
        echo "🚀 Ejecutando Pipeline Básico..."
        echo "================================"
        python3 pipeline_ollama_local.py
        ;;
    2)
        echo ""
        # Verificar Qdrant
        echo "🔍 Verificando Qdrant..."
        if ! curl -s http://localhost:6333/collections &> /dev/null; then
            echo "⚠️  Qdrant no está disponible"
            echo "   ¿Quieres continuar sin Qdrant? (se usará solo Ollama) [s/N]"
            read -p "> " CONTINUAR
            if [[ ! $CONTINUAR =~ ^[Ss]$ ]]; then
                echo "❌ Abortado. Inicia Qdrant con: docker-compose up -d"
                exit 1
            fi
        else
            echo "✅ Qdrant disponible"
        fi
        
        echo ""
        echo "🚀 Ejecutando Pipeline Seguro..."
        echo "================================"
        python3 pipeline_seguro_local.py
        ;;
    *)
        echo "❌ Opción inválida"
        exit 1
        ;;
esac

echo ""
echo "=================================================="
echo "✅ Pipeline completado"
echo ""
echo "📁 Revisa los resultados en:"
if [ "$OPCION" = "1" ]; then
    echo "   dataset_output/"
else
    echo "   dataset_output_seguro/"
fi
echo ""
echo "🎯 Próximos pasos:"
echo "   1. Revisar calidad del dataset generado"
echo "   2. Ejecutar human_review.py para validación manual"
echo "   3. Exportar con export_dataset.py"
echo "   4. Subir a Mistral Fine-tuning API"
echo ""

deactivate
