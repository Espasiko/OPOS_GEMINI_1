# GUÍA RÁPIDA: Configurar Continue IDE con Modelos Coder (2026)

## ⚡ 5 PASOS PARA EMPEZAR

### Paso 1: Obtener API Keys (2 minutos)

#### 🔑 Opción GRATIS (Recomendada)
**OpenRouter** - Para LiquidAI (completamente gratis)
1. Ve: https://openrouter.ai/keys
2. Crea cuenta gratuita
3. Copia la API key

#### 🔑 Opción Profesional (Pago)
**Mistral** - Para Codestral oficial
1. Ve: https://console.mistral.ai/api-keys
2. Crea cuenta
3. Copia la API key

### Paso 2: Configurar Variables de Entorno

**Opción A - Temporal (esta sesión):**
```bash
# Para modelos GRATIS
export OPENROUTER_API_KEY='sk-or-v1-xxxxxxxxxxxxxxxx'

# Para Codestral oficial (opcional)
export MISTRAL_API_KEY='sk-xxxxxxxxxxxxxxxx'
```

**Opción B - Permanente (recomendado):**
```bash
# Abre el archivo
nano ~/.bashrc
# o para zsh:
nano ~/.zshrc

# Agrega estas líneas:
export OPENROUTER_API_KEY='sk-or-v1-xxxxxxxxxxxxxxxx'
export MISTRAL_API_KEY='sk-xxxxxxxxxxxxxxxx'  # opcional

# Guarda (Ctrl+O, Enter, Ctrl+X)
# Recarga:
source ~/.bashrc
```

### Paso 3: Verificar Configuración

```bash
# Copia la configuración actualizada
cp /home/spas/OPOS_GEMINI_1/.continue/config.yaml ~/.continue/config.yaml

# Verifica que todo esté bien
bash /home/spas/OPOS_GEMINI_1/.continue/diagnose.sh
```

### Paso 4: Reiniciar VS Code

- Cierra VS Code completamente
- Reabre VS Code
- Presiona Ctrl+Shift+P → "Continue: Open Settings"

### Paso 5: ¡Usar Continue!

- Presiona `Ctrl+L` para abrir chat
- Los modelos deberían aparecer automáticamente
- **Primero**: LiquidAI LFM2.5 (GRATIS)
- **Backup**: Codestral API (Mistral)

---

## 🎯 MODELOS DISPONIBLES (2026)

### ⭐⭐⭐⭐⭐ RECOMENDADOS

| Modelo | Costo | Velocidad | Calidad | API Key |
|--------|-------|-----------|---------|---------|
| **LiquidAI LFM2.5 Thinking** | **$0.00** | ⚡⚡⚡ | ⭐⭐⭐⭐ | OpenRouter |
| **LiquidAI LFM2.5 Instruct** | **$0.00** | ⚡⚡⚡ | ⭐⭐⭐⭐ | OpenRouter |
| **Codestral API (Mistral)** | $0.20/M | ⚡⚡ | ⭐⭐⭐⭐⭐ | Mistral |
| **GLM 4.7 Flash** | $0.07/M | ⚡⚡⚡⚡ | ⭐⭐⭐ | OpenRouter |

### 🔄 PRIORIDADES CONFIGURADAS

1. **Codestral Local (Ollama)** - Si funciona bien
2. **Mistral Local** - Tu modelo actual
3. **Codestral API (Mistral)** - Oficial, pago
4. **LiquidAI (GRATIS)** - Mejor opción gratis
5. **GLM 4.7 Flash** - Muy barato
6. **Claude** - Backup premium

---

## 📋 CHECKLIST DE CONFIGURACIÓN

- [ ] API key de OpenRouter obtenida
- [ ] Variable `OPENROUTER_API_KEY` configurada
- [ ] Archivo config.yaml copiado a ~/.continue/
- [ ] VS Code reiniciado
- [ ] Modelos visibles en Continue
- [ ] Primera prueba exitosa

---

## 🚨 SI ALGO FALLA

### "API key not found"
```bash
# Verifica que esté configurada
echo $OPENROUTER_API_KEY

# Si está vacía, configúrala
export OPENROUTER_API_KEY='tu-api-key'
```

### "Model not available"
- Recarga VS Code (Ctrl+R)
- Verifica que config.yaml esté en ~/.continue/
- Revisa logs en VS Code console

### "Connection failed"
- Verifica conexión a internet
- Confirma que la API key es válida
- Prueba con otro modelo

---

## 💰 COSTOS ESTIMADOS (2026)

| Uso | LiquidAI | GLM 4.7 | Codestral | Claude |
|-----|----------|---------|-----------|--------|
| **Chat diario** | **$0.00** | $0.50/mes | $3.00/mes | $30.00/mes |
| **Coding intenso** | **$0.00** | $2.00/mes | $10.00/mes | $100.00/mes |
| **Proyecto grande** | **$0.00** | $5.00/mes | $25.00/mes | $200.00/mes |

---

## 🔧 PERSONALIZACIÓN

### Cambiar modelo predeterminado
Edita `~/.continue/config.yaml` y mueve tu modelo favorito al inicio.

### Agregar más modelos
Ve el archivo completo `INFO-APIS-CODER-2026.md` para todas las opciones.

### Ajustar temperatura/creatividad
```yaml
defaultCompletionOptions:
  temperature: 0.7  # 0.0 = determinista, 1.0 = creativo
```

---

## 📚 REFERENCIAS

- **OpenRouter**: https://openrouter.ai/models
- **Mistral API**: https://docs.mistral.ai/api
- **LiquidAI**: https://openrouter.ai/liquid
- **GLM**: https://openrouter.ai/z-ai/glm-4.7-flash

---

## 🎯 CONCLUSIÓN

**Empieza con LiquidAI** - Es gratis, funciona bien, y tienes Codestral como backup.

**Si necesitas más calidad** - Agrega Mistral API.

**Si Codestral local funciona** - Úsalo primero (más rápido).

¡La configuración está optimizada para darte lo mejor de ambos mundos: velocidad + calidad + costo cero!

---

**Última actualización**: Enero 2026

```bash
# 1. Variable de entorno está configurada
echo $ANTHROPIC_API_KEY

# 2. Archivos de configuración existen
ls -la ~/.continue/config.yaml

# 3. Ejecuta diagnóstico
bash /home/spas/OPOS_GEMINI_1/.continue/diagnose.sh
```

---

## 📋 ESTRUCTURA DE ARCHIVOS

```
~/.continue/
├── config.yaml                 ← Configuración principal
├── custom/                     ← Personalizaciones
├── rules/                      ← Reglas personalizadas
└── prompts/                    ← Prompts personalizados

/home/spas/OPOS_GEMINI_1/.continue/
├── config.yaml                 ← Config del proyecto
├── README-CONFIGURACION.md     ← Guía detallada
├── setup-continue.sh           ← Script de setup
├── diagnose.sh                 ← Script de diagnóstico
└── mcpServers/                 ← Servidores MCP
```

---

## 🚀 MODELOS DISPONIBLES

| Modelo | Uso | Velocidad | Costo |
|--------|-----|-----------|-------|
| **Claude Sonnet** | Chat, Edición, Agent (RECOMENDADO) | ⚡⚡⚡ | $ |
| **Claude Opus** | Tareas complejas | ⚡⚡ | $$ |
| **Claude Haiku** | Autocomplete rápido | ⚡⚡⚡⚡ | $ |

---

## ⚠️ ERRORES COMUNES

### "API key not found"
```bash
# Solución: Configurar la variable
export ANTHROPIC_API_KEY='tu-api-key'
```

### "Model not available"
```bash
# Solución: Recargar VS Code
# Ctrl+R (Windows/Linux) o Cmd+R (Mac)
```

### "config.yaml not found"
```bash
# Solución: Copiar archivo
cp /home/spas/OPOS_GEMINI_1/.continue/config.yaml ~/.continue/
```

---

## 📚 REFERENCIAS

- **Docs de Continue:** https://docs.continue.dev/
- **API de Anthropic:** https://docs.anthropic.com/
- **Modelos:** https://docs.anthropic.com/en/docs/about/models/overview
- **Keys:** https://console.anthropic.com/account/keys

---

## 💡 TIPS

1. **Usa Sonnet por defecto** - Mejor balance precio/rendimiento
2. **Opus para complejos** - Mejor precisión en tareas difíciles
3. **Haiku para autocomplete** - Muy rápido, perfecto para sugerencias
4. **Prompt Caching** - Reduce costos activando en config.yaml
5. **Guarda tu API key** - Úsala solo en ambiente seguro

---

**¿Preguntas?** Revisa la guía completa: [README-CONFIGURACION.md](README-CONFIGURACION.md)
