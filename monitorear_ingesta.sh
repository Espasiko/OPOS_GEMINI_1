#!/bin/bash
# Script de monitoreo de ingesta Qdrant en tiempo real

cd /home/spas/OPOS_GEMINI_1
source .venv/bin/activate

echo "================================================================================"
echo "🔍 MONITOREO INGESTA QDRANT EN TIEMPO REAL"
echo "================================================================================"
echo ""

# Verificar proceso
PID=$(ps aux | grep "reingest_qdrant_DIRECT_XML.py --recreate" | grep -v grep | awk '{print $2}')

if [ -z "$PID" ]; then
    echo "❌ Proceso NO está corriendo"
    echo ""
    echo "Verificando última ingesta en Qdrant..."
    python3 << 'EOF'
from qdrant_client import QdrantClient
client = QdrantClient(url="http://localhost:6333", timeout=10)
try:
    info = client.get_collection("opositaia_knowledge_FULL_XML")
    print(f"✅ Chunks finales: {info.points_count:,}")
    print(f"✅ Status: {info.status}")
except Exception as e:
    print(f"❌ Error: {e}")
EOF
    exit 0
fi

echo "✅ Proceso corriendo: PID $PID"
echo ""

# Mostrar info del proceso
ps aux | grep $PID | grep -v grep | awk '{printf "   CPU: %s%%\n   RAM: %s MB\n   Tiempo: %s\n", $3, int($6/1024), $10}'
echo ""

# Monitoreo cada 30 segundos
echo "📊 Monitoreando progreso (Ctrl+C para salir)..."
echo "================================================================================"
echo ""

while true; do
    TIMESTAMP=$(date '+%H:%M:%S')
    
    # Verificar si el proceso sigue corriendo
    if ! ps -p $PID > /dev/null 2>&1; then
        echo "[$TIMESTAMP] ⚠️  Proceso terminado"
        break
    fi
    
    # Obtener chunks actuales
    CHUNKS=$(python3 << 'EOF'
from qdrant_client import QdrantClient
try:
    client = QdrantClient(url="http://localhost:6333", timeout=10)
    info = client.get_collection("opositaia_knowledge_FULL_XML")
    print(info.points_count)
except:
    print("0")
EOF
)
    
    # Calcular progreso
    TOTAL_ESTIMADO=68000
    PORCENTAJE=$(echo "scale=2; ($CHUNKS * 100) / $TOTAL_ESTIMADO" | bc)
    
    echo "[$TIMESTAMP] Chunks: $CHUNKS / ~$TOTAL_ESTIMADO ($PORCENTAJE%)"
    
    sleep 30
done

echo ""
echo "================================================================================"
echo "✅ MONITOREO FINALIZADO"
echo "================================================================================"
