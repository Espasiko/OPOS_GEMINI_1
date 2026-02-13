📑 ÍNDICE COMPLETO - Configuración Continue IDE
═══════════════════════════════════════════════════════════════

🎯 INICIO RÁPIDO (COMIENZA AQUÍ)
═══════════════════════════════════════════════════════════════

1. 📖 LECTURA OBLIGATORIA
   • [QUICK-START.md](QUICK-START.md) ⭐
     └─ 5 pasos para empezar en 10 minutos
   
   • [RESUMEN_CONFIGURACION.txt](RESUMEN_CONFIGURACION.txt)
     └─ Resumen completo de todo lo hecho

2. 🔧 CONFIGURACIÓN
   • [config.yaml](config.yaml) ← ARCHIVO PRINCIPAL
     └─ Configuración de Claude/Anthropic
     └─ Copiar a ~/.continue/config.yaml
   
   • [config-alternativa.yaml](config-alternativa.yaml)
     └─ Ejemplos con otros proveedores (OpenAI, Gemini, etc)

3. 📚 DOCUMENTACIÓN COMPLETA
   • [README-CONFIGURACION.md](README-CONFIGURACION.md)
     └─ Guía detallada con todas las opciones

4. ⚙️ UTILIDADES
   • [setup-continue.sh](setup-continue.sh)
     └─ Script automatizado de instalación
     └─ bash setup-continue.sh
   
   • [diagnose.sh](diagnose.sh)
     └─ Verificar que todo esté correctamente configurado
     └─ bash diagnose.sh

5. 🛠️ PERSONALIZACIÓN
   • [rules.md](rules.md)
     └─ Reglas personalizadas para el agente
     └─ Directrices de código, seguridad, performance
   
   • [prompts.md](prompts.md)
     └─ Prompts personalizados (comandos /)
     └─ Refactor, testing, documentación, seguridad, etc

🚀 PASOS DE INSTALACIÓN
═══════════════════════════════════════════════════════════════

PASO 1: Obtener API Key
┌─────────────────────────────────────────────────────────────┐
│ 1. Abre: https://console.anthropic.com/account/keys         │
│ 2. Copia la clave (comienza con "sk-ant-")                  │
│ 3. Guárdala de forma segura                                 │
└─────────────────────────────────────────────────────────────┘

PASO 2: Configurar Variable de Entorno
┌─────────────────────────────────────────────────────────────┐
│ $ export ANTHROPIC_API_KEY='sk-ant-xxxxxxxxxxxxx'           │
│                                                              │
│ O PERMANENTE en ~/.bashrc o ~/.zshrc:                       │
│ export ANTHROPIC_API_KEY='sk-ant-xxxxxxxxxxxxx'             │
│ source ~/.bashrc  # o source ~/.zshrc                       │
└─────────────────────────────────────────────────────────────┘

PASO 3: Copiar Configuración
┌─────────────────────────────────────────────────────────────┐
│ $ cp /home/spas/OPOS_GEMINI_1/.continue/config.yaml \       │
│     ~/.continue/config.yaml                                 │
└─────────────────────────────────────────────────────────────┘

PASO 4: Verificar (Opcional pero Recomendado)
┌─────────────────────────────────────────────────────────────┐
│ $ bash /home/spas/OPOS_GEMINI_1/.continue/diagnose.sh      │
└─────────────────────────────────────────────────────────────┘

PASO 5: Usar en VS Code
┌─────────────────────────────────────────────────────────────┐
│ 1. Cierra y reabre VS Code                                  │
│ 2. Presiona Ctrl+L (o Cmd+L en Mac)                         │
│ 3. ¡Comienza a chatear con Claude!                          │
└─────────────────────────────────────────────────────────────┘

📋 ARCHIVOS POR PROPÓSITO
═══════════════════════════════════════════════════════════════

CONFIGURACIÓN
─────────────
config.yaml                  ← PRINCIPAL: modelos Claude
config-alternativa.yaml      ← Otros proveedores (ejemplos)

DOCUMENTACIÓN
─────────────
QUICK-START.md               ← Guía rápida (10 min)
README-CONFIGURACION.md      ← Guía completa (detallada)
RESUMEN_CONFIGURACION.txt    ← Resumen ejecutivo
INDEX.md                     ← Este archivo

SCRIPTS
───────
setup-continue.sh            ← Instalación automatizada
diagnose.sh                  ← Verificación y diagnóstico

PERSONALIZACIÓN
───────────────
rules.md                     ← Reglas del agente
prompts.md                   ← Prompts personalizados (/)

🎛️ MODELOS DISPONIBLES
═══════════════════════════════════════════════════════════════

Claude Sonnet 4.5 (RECOMENDADO)
  ├─ Roles: chat, edit, apply, agent
  ├─ Velocidad: ⚡⚡⚡
  ├─ Inteligencia: ⭐⭐⭐⭐⭐
  ├─ Costo: $ (bajo)
  └─ Mejor para: Mayoría de tareas

Claude Opus
  ├─ Roles: chat, edit
  ├─ Velocidad: ⚡⚡
  ├─ Inteligencia: ⭐⭐⭐⭐⭐⭐
  ├─ Costo: $$ (medio)
  └─ Mejor para: Problemas complejos

Claude Haiku
  ├─ Roles: autocomplete
  ├─ Velocidad: ⚡⚡⚡⚡
  ├─ Inteligencia: ⭐⭐⭐
  ├─ Costo: $ (muy bajo)
  └─ Mejor para: Sugerencias rápidas

🔌 CONTEXTO & HERRAMIENTAS
═══════════════════════════════════════════════════════════════

Context Providers (Información disponible para Claude)
  ├─ file      → Acceso a archivos del proyecto
  ├─ code      → Análisis inteligente de código
  ├─ diff      → Cambios recientes
  └─ terminal  → Salida de terminal

MCP Servers (Herramientas)
  └─ Python Environment → Ejecutar código Python

🎯 PROMPTS PERSONALIZADOS
═══════════════════════════════════════════════════════════════

Comando             Descripción
────────────────────────────────────────────────────────────
/refactor           Refactoriza código seleccionado
/document           Genera documentación
/test               Escribe pruebas unitarias
/security-review    Revisa por vulnerabilidades
/performance        Analiza performance (Big O)
/explain            Explica qué hace el código
/rag-integration    Integra con sistema RAG
/mcp-handler        Crea handler MCP
/api-endpoint       Crea endpoint REST
/async-refactor     Convierte a asincrónico

ℹ️ INFORMACIÓN DE CARPETAS
═══════════════════════════════════════════════════════════════

WORKSPACE
/home/spas/OPOS_GEMINI_1/.continue/
├── config.yaml                      ← Configuración principal
├── config-alternativa.yaml          ← Alternativas
├── *.md                             ← Documentación
├── *.sh                             ← Scripts
├── *.txt                            ← Resúmenes
├── INDEX.md                         ← Este archivo
├── mcpServers/                      ← MCP configurations
│   ├── new-mcp-server.yaml
│   ├── new-mcp-server-1.yaml
│   └── new-mcp-server-2.yaml
└── [otros archivos del proyecto]

HOME
~/.continue/
├── config.yaml                      ← Copia para VS Code (IMPORTANTE)
├── custom/                          ← Personalizaciones
├── rules/                           ← Reglas adicionales
└── prompts/                         ← Prompts adicionales

❓ PREGUNTAS FRECUENTES
═══════════════════════════════════════════════════════════════

P: ¿Dónde obtengo la API key?
R: https://console.anthropic.com/account/keys

P: ¿Cómo cambio el modelo predeterminado?
R: Edita config.yaml, mueve el modelo deseado al inicio

P: ¿Qué si no tengo ANTHROPIC_API_KEY configurada?
R: Ejecuta: export ANTHROPIC_API_KEY='tu-api-key'

P: ¿Por qué no carga la configuración?
R: Recarga VS Code (Ctrl+R), verifica que config.yaml esté en ~/.continue/

P: ¿Puedo usar otros proveedores?
R: Sí, ve config-alternativa.yaml para ejemplos

P: ¿Cuál modelo es más barato?
R: Haiku < Sonnet < Opus (en ese orden)

P: ¿Qué es "Agent Mode"?
R: Claude trabajando autónomamente en tareas, con acceso a herramientas

P: ¿Qué es MCP?
R: Model Context Protocol - estándar para integrar herramientas externas

🔒 SEGURIDAD
═══════════════════════════════════════════════════════════════

✓ API Key en variable de entorno (NO en código)
✓ NO se commit a git
✓ NO se mostrará en logs públicos
✓ Revocable en console.anthropic.com
✓ Almacenamiento seguro en ~/.bashrc o ~/.zshrc

NUNCA hagas esto:
✗ export ANTHROPIC_API_KEY en scripts públicos
✗ Commit de .env a git
✗ Compartir API key
✗ Usar en sitios no confiables

📞 CONTACTO & RECURSOS
═══════════════════════════════════════════════════════════════

Documentación
  • Continue IDE: https://docs.continue.dev/
  • Anthropic: https://docs.anthropic.com/
  • Modelos: https://docs.anthropic.com/en/docs/about/models/overview

Consolas
  • API Keys: https://console.anthropic.com/account/keys
  • Dashboard: https://console.anthropic.com/

Comunidad
  • GitHub Continue: https://github.com/continuedev/continue
  • Discord: https://discord.gg/vapESyrFmJ
  • GitHub Discussions: https://github.com/continuedev/continue/discussions

═══════════════════════════════════════════════════════════════
SIGUIENTE: Lee QUICK-START.md para los 5 pasos finales
═══════════════════════════════════════════════════════════════
