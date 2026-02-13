#!/bin/bash
# SETUP 0: Validación completa de recursos OpositaIA
# Verifica: Salamandra, Qdrant, BOE API, Calculadoras
# Fecha: 13/02/2026

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  SETUP VALIDACIÓN: OpositaIA Viabilidad                      ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS_COUNT=0
FAIL_COUNT=0

# Helper function
check_status() {
    local exit_code=$1
    local message=$2
    
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✅ PASS${NC}: $message"
        ((PASS_COUNT++))
    else
        echo -e "${RED}❌ FAIL${NC}: $message"
        ((FAIL_COUNT++))
    fi
}

echo ""
echo "📋 VERIFICACIÓN 1: SALAMANDRA R1 LOCAL (Ollama)"
echo "─────────────────────────────────────────────────"

# Check Ollama running
curl -s http://localhost:11434/api/tags > /dev/null 2>&1
check_status $? "Ollama API accesible en http://localhost:11434"

# Check Salamandra model
ollama list 2>/dev/null | grep -q "salamandra-r1\|salamandra"
check_status $? "Modelo Salamandra R1 en Ollama"

echo ""
echo "📋 VERIFICACIÓN 2: QDRANT LOCAL"
echo "───────────────────────────────"

# Check Qdrant running
curl -s http://localhost:6333/health > /dev/null 2>&1
check_status $? "Qdrant API accesible en http://localhost:6333"

# Check collections
QDRANT_COLLECTIONS=$(curl -s http://localhost:6333/collections 2>/dev/null)
echo "$QDRANT_COLLECTIONS" | grep -q "opositaia_knowledge_FULL_XML" 2>/dev/null
check_status $? "Colección opositaia_knowledge_FULL_XML existe"

echo "$QDRANT_COLLECTIONS" | grep -q "opositaia_leyes_master" 2>/dev/null
check_status $? "Colección opositaia_leyes_master existe"

# Check vector count
VECTOR_COUNT=$(curl -s http://localhost:6333/collections/opositaia_knowledge_FULL_XML 2>/dev/null | python3 -c "import sys, json; print(json.load(sys.stdin).get('result', {}).get('points_count', 0))" 2>/dev/null)
if [ "$VECTOR_COUNT" -gt 1000 ]; then
    check_status 0 "Qdrant tiene vectors indexados (>1000) - Total: $VECTOR_COUNT"
else
    check_status 1 "Qdrant tiene vectors indexados (>1000)"
fi

echo ""
echo "📋 VERIFICACIÓN 3: BOE API GRATUITA"
echo "──────────────────────────────────"

# Test BOE connectivity
curl -s -I https://www.boe.es/ > /dev/null 2>&1
check_status $? "BOE website accesible"

# Test BOE search API
curl -s "https://www.boe.es/buscar/act.php?id=BOE-A-2020-3824" > /dev/null 2>&1
check_status $? "BOE search API responde"

echo ""
echo "📋 VERIFICACIÓN 4: CALCULADORAS PYTHON"
echo "──────────────────────────────────────"

cd /home/spas/OPOS_GEMINI_1

# Test calculos_ss.py
python3 << 'PYEOF' > /dev/null 2>&1
from backend.calculators.calculos_ss import CalculadoraSS
resultado = CalculadoraSS.calcular_subsidio_it(1500, 'EC', 25)
assert resultado.subsidio_diario > 0
PYEOF
check_status $? "calculos_ss.py importa y ejecuta"

# Test calculos_imv.py
python3 << 'PYEOF' > /dev/null 2>&1
from backend.calculators.calculos_imv import CalculadoraIMV, TipoUnidadFamiliar
from decimal import Decimal
resultado = CalculadoraIMV.calcular_imv(TipoUnidadFamiliar.PERSONA_SOLA, 0)
assert resultado.imv_a_recibir == Decimal('564.60')
PYEOF
check_status $? "calculos_imv.py importa y ejecuta"

echo ""
echo "📋 VERIFICACIÓN 5: ESTRUCTURA PROYECTO"
echo "──────────────────────────────────────"

# Check backend agents
[ -d "backend/agents" ]
check_status $? "Directorio backend/agents existe"

[ -f "backend/agents/rag_agent_v2.py" ]
check_status $? "RAG Agent V2 existe"

[ -f "backend/agents/llm_providers.py" ]
check_status $? "LLM Providers existe"

[ -f "backend/agents/boe_api_client.py" ]
check_status $? "BOE API Client existe"

# Check calculators
[ -d "backend/calculators" ]
check_status $? "Directorio backend/calculators existe"

[ -f "backend/calculators/calculos_ss.py" ]
check_status $? "calculos_ss.py existe"

[ -f "backend/calculators/calculos_imv.py" ]
check_status $? "calculos_imv.py existe"

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                    RESUMEN SETUP                              ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}✅ PASADAS: $PASS_COUNT${NC}"
echo -e "${RED}❌ FALLIDAS: $FAIL_COUNT${NC}"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}✅ SETUP COMPLETADO: TODOS LOS RECURSOS OPERATIVOS${NC}"
    echo ""
    echo "Próximo paso: FASE 1 - Expandir calculadoras SS"
    echo "  → Crear calculos_ss_extended.py"
    echo "  → Implementar 9 tipos nuevos de cálculos"
    echo "  → Tests unitarios"
    exit 0
else
    echo -e "${RED}❌ SETUP INCOMPLETO: FALLOS DETECTADOS${NC}"
    echo ""
    echo "Próximos pasos:"
    echo "  1. Verificar que Ollama está corriendo: ollama serve"
    echo "  2. Verificar que Qdrant está corriendo: docker-compose up -d qdrant"
    echo "  3. Verificar conexión a internet para BOE"
    echo "  4. Ejecutar este script nuevamente"
    exit 1
fi
