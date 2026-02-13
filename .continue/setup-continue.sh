#!/bin/bash

# Script de configuración de Continue IDE con Claude/Anthropic
# Este script configura Continue IDE para funcionar con modelos de Anthropic

echo "====================================================="
echo "  Configurando Continue IDE con Claude/Anthropic"
echo "====================================================="

# Verificar si existe la variable de entorno ANTHROPIC_API_KEY
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo ""
    echo "⚠️  ATENCIÓN: La variable ANTHROPIC_API_KEY no está configurada"
    echo ""
    echo "Para configurar Continue IDE con Claude, necesitas:"
    echo "1. Obtener tu API key en: https://console.anthropic.com/account/keys"
    echo "2. Exportar la variable:"
    echo "   export ANTHROPIC_API_KEY='tu-api-key-aqui'"
    echo "3. O agregar a ~/.bashrc o ~/.zshrc para uso permanente"
    echo ""
else
    echo "✓ ANTHROPIC_API_KEY configurada"
fi

# Crear directorios necesarios
echo ""
echo "Creando estructura de directorios..."
mkdir -p ~/.continue/custom
mkdir -p ~/.continue/rules
mkdir -p ~/.continue/prompts

# Copiar la configuración
echo "Copiando archivos de configuración..."
if [ -f "/home/spas/OPOS_GEMINI_1/.continue/config.yaml" ]; then
    cp /home/spas/OPOS_GEMINI_1/.continue/config.yaml ~/.continue/config.yaml
    echo "✓ config.yaml copiado"
else
    echo "✗ No se encontró config.yaml"
fi

# Información de próximos pasos
echo ""
echo "====================================================="
echo "  PRÓXIMOS PASOS"
echo "====================================================="
echo ""
echo "1. Configure la API key de Anthropic:"
echo "   export ANTHROPIC_API_KEY='sk-ant-...'"
echo ""
echo "2. En VS Code, abra la paleta de comandos (Ctrl+Shift+P)"
echo "   y busque 'Continue: Open Settings'"
echo ""
echo "3. Verifique que los modelos están disponibles:"
echo "   - Claude Sonnet 4.5 (chat, edit, agent)"
echo "   - Claude Opus (tareas complejas)"
echo "   - Claude Haiku (autocomplete)"
echo ""
echo "4. Los MCP servers se cargarán automáticamente"
echo ""
echo "====================================================="
echo "✓ Configuración completada"
echo "====================================================="
