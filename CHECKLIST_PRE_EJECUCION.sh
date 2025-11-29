#!/bin/bash
# 🎯 CHECKLIST EJECUTABLE: Verificar estado antes de comenzar
# Uso: bash CHECKLIST_PRE_EJECUCION.sh

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     🎯 CHECKLIST PRE-EJECUCIÓN (29 Nov 2025)                 ║"
echo "║     Verifica que todo está listo para comenzar                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Contador
CHECKS_PASSED=0
CHECKS_TOTAL=0

# Función para verificar
check() {
    CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
    local item="$1"
    local command="$2"
    
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅${NC} $item"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
        echo -e "${RED}❌${NC} $item"
    fi
}

# Función para información
info() {
    echo -e "${BLUE}ℹ️${NC}  $1"
}

# Función para advertencia
warning() {
    echo -e "${YELLOW}⚠️${NC}  $1"
}

echo "1️⃣  VERIFICANDO UBICACIÓN..."
echo "─────────────────────────────────────────────────────────────────"
check "Ubicación correcta" "test -d /home/espasiko/OPOS_GEMINI_1"
check "Carpeta backend existe" "test -d /home/espasiko/OPOS_GEMINI_1/backend"
check "Carpeta agents existe" "test -d /home/espasiko/OPOS_GEMINI_1/backend/agents"
echo ""

echo "2️⃣  VERIFICANDO DOCUMENTACIÓN..."
echo "─────────────────────────────────────────────────────────────────"
check "QUICK_START.md" "test -f /home/espasiko/OPOS_GEMINI_1/QUICK_START.md"
check "COMIENZA_HOY.md" "test -f /home/espasiko/OPOS_GEMINI_1/COMIENZA_HOY.md"
check "RESUMEN_FINAL_STATUS.md" "test -f /home/espasiko/OPOS_GEMINI_1/RESUMEN_FINAL_STATUS.md"
check "PLAN_IMPLEMENTACION.md" "test -f /home/espasiko/OPOS_GEMINI_1/PLAN_IMPLEMENTACION_COMPLETO_10K_CHUNKS.md"
check "MAPEO_ARCHIVOS.md" "test -f /home/espasiko/OPOS_GEMINI_1/MAPEO_ARCHIVOS_ESTRUCTURA.md"
check "INDEX_IMPLEMENTACION.md" "test -f /home/espasiko/OPOS_GEMINI_1/INDEX_IMPLEMENTACION_FINAL.md"
check "FLUJO_VISUAL.md" "test -f /home/espasiko/OPOS_GEMINI_1/FLUJO_VISUAL.md"
check "RESUMEN_EJECUTIVO.md" "test -f /home/espasiko/OPOS_GEMINI_1/RESUMEN_EJECUTIVO.md"
echo ""

echo "3️⃣  VERIFICANDO SCRIPTS PYTHON..."
echo "─────────────────────────────────────────────────────────────────"
check "cambiar_embedding_model.py" "test -f /home/espasiko/OPOS_GEMINI_1/backend/agents/cambiar_embedding_model.py"
check "boe_downloader_completo.py" "test -f /home/espasiko/OPOS_GEMINI_1/backend/agents/boe_downloader_completo.py"
check "document_to_chunks_processor.py" "test -f /home/espasiko/OPOS_GEMINI_1/backend/agents/document_to_chunks_processor.py"
echo ""

echo "4️⃣  VERIFICANDO CONFIGURACIÓN..."
echo "─────────────────────────────────────────────────────────────────"
check "Archivo .env existe" "test -f /home/espasiko/OPOS_GEMINI_1/backend/.env"
check "Python 3 instalado" "command -v python3"
check "pip instalado" "command -v pip"
echo ""

echo "5️⃣  VERIFICANDO DEPENDENCIAS PYTHON..."
echo "─────────────────────────────────────────────────────────────────"
check "sentence-transformers" "python3 -c 'import sentence_transformers' 2>/dev/null"
check "qdrant-client" "python3 -c 'import qdrant_client' 2>/dev/null"
check "PyPDF2" "python3 -c 'import PyPDF2' 2>/dev/null"
check "requests" "python3 -c 'import requests' 2>/dev/null"
echo ""

echo "6️⃣  VERIFICANDO ESPACIO EN DISCO..."
echo "─────────────────────────────────────────────────────────────────"
DISKFREE=$(df /home/espasiko | awk 'NR==2 {print $4}' | numfmt --to=iec 2>/dev/null || echo "desconocido")
echo "Espacio disponible: $DISKFREE"
check "Espacio suficiente (>500GB)" "test $(df /home/espasiko | awk 'NR==2 {print $4}') -gt 524288000"
echo ""

echo "7️⃣  VERIFICANDO VARIABLES DE ENTORNO..."
echo "─────────────────────────────────────────────────────────────────"
if grep -q "QDRANT_URL" /home/espasiko/OPOS_GEMINI_1/backend/.env 2>/dev/null; then
    echo -e "${GREEN}✅${NC} QDRANT_URL configurada"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo -e "${RED}❌${NC} QDRANT_URL no configurada"
fi
CHECKS_TOTAL=$((CHECKS_TOTAL + 1))

if grep -q "QDRANT_API_KEY" /home/espasiko/OPOS_GEMINI_1/backend/.env 2>/dev/null; then
    echo -e "${GREEN}✅${NC} QDRANT_API_KEY configurada"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo -e "${RED}❌${NC} QDRANT_API_KEY no configurada"
fi
CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
echo ""

echo "8️⃣  VERIFICANDO CONECTIVIDAD..."
echo "─────────────────────────────────────────────────────────────────"
check "Conexión a internet" "curl -s https://www.boe.es > /dev/null 2>&1"
check "API BOE accesible" "curl -s https://www.boe.es/datosabiertos/api/ > /dev/null 2>&1"
echo ""

echo "9️⃣  INFORMACIÓN DEL SISTEMA..."
echo "─────────────────────────────────────────────────────────────────"
info "OS: $(uname -s)"
info "Kernel: $(uname -r)"
info "Python: $(python3 --version 2>&1)"
info "Home: /home/espasiko/OPOS_GEMINI_1"
echo ""

echo "🔟 RESUMEN FINAL..."
echo "─────────────────────────────────────────────────────────────────"

if [ $CHECKS_PASSED -eq $CHECKS_TOTAL ]; then
    echo -e "${GREEN}✅ TODOS LOS CHECKS PASADOS ($CHECKS_PASSED/$CHECKS_TOTAL)${NC}"
    echo ""
    echo "🚀 LISTO PARA COMENZAR"
    echo ""
    echo "Ejecuta en la terminal:"
    echo "  cd /home/espasiko/OPOS_GEMINI_1/backend"
    echo "  source venv/bin/activate"
    echo "  python agents/cambiar_embedding_model.py"
    echo ""
    exit 0
else
    CHECKS_FAILED=$((CHECKS_TOTAL - CHECKS_PASSED))
    echo -e "${YELLOW}⚠️  FALLOS DETECTADOS: $CHECKS_FAILED/$CHECKS_TOTAL${NC}"
    echo ""
    echo "Soluciona los items fallidos y vuelve a ejecutar este checklist."
    echo ""
    echo "Problemas comunes:"
    echo "  - Dependencias: pip install sentence-transformers PyPDF2 requests"
    echo "  - Qdrant: Verificar QDRANT_URL y QDRANT_API_KEY en .env"
    echo "  - Espacio: Liberar espacio en disco (necesita 500GB+)"
    echo ""
    exit 1
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     Última actualización: 29 Nov 2025                         ║"
echo "║     Versión: 1.0                                              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
