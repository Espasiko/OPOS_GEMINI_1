#!/bin/bash
# Script para limpiar y re-indexar todas las leyes en Qdrant Cloud

echo "================================================================================"
echo "🔄 PROCESO COMPLETO: LIMPIAR Y RE-INDEXAR LEYES"
echo "================================================================================"
echo ""
echo "Este script hará:"
echo "1. Limpiar Qdrant Cloud (eliminar todo)"
echo "2. Indexar las 13 leyes desde cero"
echo ""
echo "⚠️  ADVERTENCIA: Esto eliminará TODOS los datos actuales de Qdrant Cloud"
echo ""
read -p "¿Continuar? (escribe SI para confirmar): " confirmacion

if [ "$confirmacion" != "SI" ]; then
    echo "❌ Operación cancelada"
    exit 0
fi

echo ""
echo "================================================================================"
echo "📍 PASO 1/2: Limpiar Qdrant Cloud"
echo "================================================================================"
echo ""

cd "$(dirname "$0")"
source backend/venv/bin/activate
python limpiar_qdrant_cloud.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Error en la limpieza. Abortando."
    exit 1
fi

echo ""
echo "================================================================================"
echo "📍 PASO 2/2: Indexar todas las leyes"
echo "================================================================================"
echo ""
echo "⏱️  Tiempo estimado: 1-2 horas"
echo "📊 Leyes a indexar: 13"
echo ""

python backend/agents/indexar_todas_las_leyes.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Error en la indexación"
    exit 1
fi

echo ""
echo "================================================================================"
echo "✅ PROCESO COMPLETADO"
echo "================================================================================"
echo ""
echo "💡 Próximos pasos:"
echo "   1. Verificar: python comparar_qdrant_local_vs_cloud.py"
echo "   2. Probar RAG con preguntas sobre diferentes leyes"
echo ""
