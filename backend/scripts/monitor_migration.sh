#!/bin/bash
# Monitor migración Qdrant y notificar cuando termine

LOG_FILE="/tmp/qdrant_migration_v2.log"
CHECK_INTERVAL=300  # 5 minutos

echo "🔍 Monitoreando migración Qdrant..."
echo "Log: $LOG_FILE"
echo "Revisando cada $CHECK_INTERVAL segundos..."
echo ""

while true; do
    # Verificar si proceso sigue corriendo
    if ! pgrep -f "migrate_cloud_to_hybrid" > /dev/null; then
        echo ""
        echo "=" | tr '\n' '=' | head -c 80; echo ""
        echo "✅ MIGRACIÓN COMPLETADA"
        echo "=" | tr '\n' '=' | head -c 80; echo ""
        
        # Ver últimas líneas del log
        echo ""
        echo "Últimas líneas del log:"
        tail -20 "$LOG_FILE"
        
        # Verificar puntos en colección
        echo ""
        echo "Verificando colección híbrida..."
        curl -s http://localhost:6333/collections/opositaia_knowledge_hybrid | \
            jq '{points: .result.points_count, status: .result.status}'
        
        echo ""
        echo "🎯 SIGUIENTE PASO:"
        echo "   python backend/scripts/compare_search_dense_vs_hybrid.py"
        
        break
    fi
    
    # Mostrar progreso actual
    if [ -f "$LOG_FILE" ]; then
        PROGRESS=$(tail -1 "$LOG_FILE" | grep -oP 'Migrating:\s+\K[0-9]+%' || echo "En progreso...")
        POINTS=$(tail -1 "$LOG_FILE" | grep -oP 'Migrating:\s+[0-9]+%\|[^|]+\|\s+\K[0-9]+' || echo "?")
        echo "[$(date +'%H:%M:%S')] Progreso: $PROGRESS ($POINTS puntos procesados)"
    fi
    
    sleep $CHECK_INTERVAL
done
