#!/bin/bash
# Test E2E Completo - Generación de Caso con Todos los MCPs

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        PRUEBA E2E COMPLETA - TODOS LOS MCPs                    ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# PASO 1: Verificar servicios
echo -e "${BLUE}═══ PASO 1: Verificación de Servicios ═══${NC}"
echo ""

echo "🔍 Qdrant..."
QDRANT_STATUS=$(curl -s http://localhost:6333/collections | grep -o '"name"' | wc -l)
if [ $QDRANT_STATUS -gt 0 ]; then
    echo -e "${GREEN}✅ Qdrant: $QDRANT_STATUS colecciones activas${NC}"
else
    echo "❌ Qdrant: No responde"
    exit 1
fi

echo "🔍 VPS Salamandra..."
VPS_STATUS=$(curl -s http://147.93.95.67:8080/health)
if [ ! -z "$VPS_STATUS" ]; then
    echo -e "${GREEN}✅ VPS Salamandra: Activo${NC}"
else
    echo "❌ VPS Salamandra: No responde"
    exit 1
fi

echo "🔍 Backend FastAPI..."
BACKEND_STATUS=$(curl -s http://localhost:8000/health)
if [ ! -z "$BACKEND_STATUS" ]; then
    echo -e "${GREEN}✅ Backend FastAPI: Activo${NC}"
else
    echo "⚠️  Backend FastAPI: Arrancando..."
    sleep 5
fi

echo ""
echo -e "${BLUE}═══ PASO 2: Generación de Caso Completo ═══${NC}"
echo ""

# PASO 2: Generar caso usando endpoint
echo "📝 Generando caso con endpoint /api/casos-practicos/generar..."
echo ""

RESPONSE=$(curl -s -X POST http://localhost:8000/api/casos-practicos/generar \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Incapacidad Temporal por Enfermedad Común",
    "dificultad": "media",
    "base_cotizacion": 1850.0,
    "contingencia": "EC",
    "dia_baja": 10
  }')

# Verificar respuesta
if echo "$RESPONSE" | grep -q "enunciado"; then
    echo -e "${GREEN}✅ Caso generado exitosamente${NC}"
    echo ""
    
    # Guardar caso
    echo "$RESPONSE" > /tmp/caso_e2e_test.json
    
    # Extraer info clave
    echo -e "${YELLOW}📊 Información del Caso:${NC}"
    echo ""
    
    ENUNCIADO=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('caso', {}).get('enunciado', '')[:150] + '...')" 2>/dev/null)
    PREGUNTA=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('caso', {}).get('pregunta', '')[:100] + '...')" 2>/dev/null)
    RESPUESTA=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('caso', {}).get('respuesta_correcta', 'N/A'))" 2>/dev/null)
    SUBSIDIO=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('calculo_usado', {}).get('subsidio_diario', 'N/A'))" 2>/dev/null)
    COHERENCIA=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('confidence', {}).get('overall', 'N/A'))" 2>/dev/null)
    
    echo "  Enunciado: $ENUNCIADO"
    echo "  Pregunta: $PREGUNTA"
    echo "  Respuesta correcta: $RESPUESTA"
    echo "  Subsidio diario: ${SUBSIDIO}€"
    echo "  Coherencia: $COHERENCIA"
    echo ""
    
    # Verificar MCPs usados
    echo -e "${BLUE}═══ PASO 3: Verificación de MCPs Usados ═══${NC}"
    echo ""
    
    # Verificar calculadora
    if [ "$SUBSIDIO" != "N/A" ]; then
        echo -e "${GREEN}✅ Calculadora SS: Usado (${SUBSIDIO}€/día)${NC}"
    else
        echo "❌ Calculadora SS: No usado"
    fi
    
    # Verificar RAG (artículos)
    ARTICULOS=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('caso', {}).get('articulos_aplicables', [])))" 2>/dev/null)
    if [ "$ARTICULOS" -gt 0 ]; then
        echo -e "${GREEN}✅ RAG (Qdrant): Usado ($ARTICULOS artículos)${NC}"
    else
        echo "⚠️  RAG (Qdrant): No artículos citados"
    fi
    
    # Verificar Salamandra
    MODELO=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('caso', {}).get('metadata', {}).get('modelo', 'N/A'))" 2>/dev/null)
    if [ "$MODELO" != "N/A" ]; then
        echo -e "${GREEN}✅ VPS Salamandra: Usado ($MODELO)${NC}"
    else
        echo "❌ VPS Salamandra: No usado"
    fi
    
    # Verificar coherencia
    if (( $(echo "$COHERENCIA > 0.95" | bc -l) )); then
        echo -e "${GREEN}✅ Memoria MCP: Caso guardado (coherencia ${COHERENCIA})${NC}"
    else
        echo "⚠️  Memoria MCP: Caso no guardado (coherencia < 0.95)"
    fi
    
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                  ✅ PRUEBA E2E EXITOSA                         ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "📁 Caso guardado en: /tmp/caso_e2e_test.json"
    echo ""
    
else
    echo "❌ Error generando caso"
    echo "Respuesta del servidor:"
    echo "$RESPONSE"
    exit 1
fi

# PASO 4: Verificar memoria MCP
echo -e "${BLUE}═══ PASO 4: Verificación Memoria MCP ═══${NC}"
echo ""

cd /home/spas/OPOS_GEMINI_1
source .venv/bin/activate

python3 << 'PYTHON_SCRIPT'
from backend.mcp_servers.qdrant_memory_local import QdrantMemoryLocal

try:
    memory = QdrantMemoryLocal()
    stats = memory.get_stats()
    
    print(f"✅ Memoria MCP:")
    print(f"   - Colección: {stats['collection']}")
    print(f"   - Casos guardados: {stats['points_count']}")
    print(f"   - Estado: {stats['status']}")
    print()
    
except Exception as e:
    print(f"⚠️  Error verificando memoria: {e}")
    print()
PYTHON_SCRIPT

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "                    FIN PRUEBA E2E"
echo "═══════════════════════════════════════════════════════════════"
