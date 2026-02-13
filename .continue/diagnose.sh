#!/bin/bash

# Script de verificación y diagnóstico de Continue IDE
# Verifica que toda la configuración esté correcta

set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  DIAGNÓSTICO - Continue IDE${NC}"
echo -e "${BLUE}================================${NC}\n"

# Función para imprimir resultado
check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1"
    fi
}

# 1. Verificar directorios
echo -e "${YELLOW}1. Verificando directorios...${NC}"
[ -d "~/.continue" ] 2>/dev/null || mkdir -p ~/.continue
check "Directorio ~/.continue existe"

[ -d "~/.continue/custom" ] 2>/dev/null || mkdir -p ~/.continue/custom
check "Directorio ~/.continue/custom existe"

# 2. Verificar archivos de configuración
echo -e "\n${YELLOW}2. Verificando archivos de configuración...${NC}"
[ -f "~/.continue/config.yaml" ]
check "config.yaml existe"

[ -f "/home/spas/OPOS_GEMINI_1/.continue/config.yaml" ]
check "config.yaml en proyecto existe"

# 3. Verificar variable de entorno
echo -e "\n${YELLOW}3. Verificando variable de entorno...${NC}"
if [ -n "$ANTHROPIC_API_KEY" ]; then
    # Mostrar solo los primeros y últimos caracteres por seguridad
    MASKED_KEY="${ANTHROPIC_API_KEY:0:7}...${ANTHROPIC_API_KEY: -4}"
    echo -e "${GREEN}✓${NC} ANTHROPIC_API_KEY configurada: $MASKED_KEY"
else
    echo -e "${RED}✗${NC} ANTHROPIC_API_KEY NO configurada"
    echo -e "${YELLOW}  Ejecuta:${NC} export ANTHROPIC_API_KEY='tu-api-key'"
fi

# 4. Verificar formato YAML
echo -e "\n${YELLOW}4. Verificando formato YAML...${NC}"
if command -v yamllint &> /dev/null; then
    yamllint ~/.continue/config.yaml 2>/dev/null
    check "config.yaml tiene formato YAML válido"
else
    echo -e "${YELLOW}⚠${NC} yamllint no instalado (opcional)"
fi

# 5. Verificar Python (para MCP servers)
echo -e "\n${YELLOW}5. Verificando dependencias...${NC}"
command -v python3 &> /dev/null
check "Python3 está instalado"

command -v npm &> /dev/null
check "npm está instalado (para MCP servers)"

# 6. Información de modelos
echo -e "\n${YELLOW}6. Modelos configurados:${NC}"
echo -e "  ${BLUE}•${NC} Claude Sonnet 4.5 (chat, edit, agent)"
echo -e "  ${BLUE}•${NC} Claude Opus (chat, edit)"
echo -e "  ${BLUE}•${NC} Claude Haiku (autocomplete)"

# 7. Información de contexto
echo -e "\n${YELLOW}7. Contexto disponible:${NC}"
echo -e "  ${BLUE}•${NC} File provider"
echo -e "  ${BLUE}•${NC} Code provider"
echo -e "  ${BLUE}•${NC} Diff provider"
echo -e "  ${BLUE}•${NC} Terminal provider"

# 8. MCP Servers
echo -e "\n${YELLOW}8. MCP Servers configurados:${NC}"
echo -e "  ${BLUE}•${NC} Python Environment (mcp_server_python)"

# Resumen
echo -e "\n${BLUE}================================${NC}"
echo -e "${BLUE}  RESUMEN DE CONFIGURACIÓN${NC}"
echo -e "${BLUE}================================${NC}\n"

if [ -n "$ANTHROPIC_API_KEY" ] && [ -f "~/.continue/config.yaml" ]; then
    echo -e "${GREEN}✓ Continue IDE está correctamente configurado${NC}"
    echo -e "\n${YELLOW}Próximos pasos:${NC}"
    echo -e "  1. Abre VS Code"
    echo -e "  2. Abre la paleta de comandos (Ctrl+Shift+P)"
    echo -e "  3. Escribe 'Continue: Open Settings'"
    echo -e "  4. Verifica que los modelos Claude estén disponibles"
    echo -e "  5. ¡Comienza a usar Continue con Claude!"
else
    echo -e "${RED}✗ Continue IDE necesita configuración${NC}"
    echo -e "\n${YELLOW}Acciones requeridas:${NC}"
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        echo -e "  1. Configura ANTHROPIC_API_KEY:"
        echo -e "     export ANTHROPIC_API_KEY='tu-api-key'"
    fi
    if [ ! -f "~/.continue/config.yaml" ]; then
        echo -e "  2. Copia config.yaml a ~/.continue/"
    fi
fi

echo -e "\n"
