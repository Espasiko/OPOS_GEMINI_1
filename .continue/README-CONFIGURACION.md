# Configuración de Continue IDE con Modelos Coder (2026)

## 📋 Descripción

Esta configuración permite que Continue IDE funcione con múltiples proveedores de modelos coder, priorizando opciones gratuitas y locales, con backups en la nube.

## 🚀 Instalación Rápida

### 1. Obtener API Keys

#### 🔑 Opción GRATIS (Recomendada)
**OpenRouter** para LiquidAI:
- URL: https://openrouter.ai/keys
- Costo: $0.00 (completamente gratis)
- Modelos: LiquidAI LFM2.5 Thinking/Instruct

#### 🔑 Opción Profesional
**Mistral** para Codestral oficial:
- URL: https://console.mistral.ai/api-keys
- Costo: $0.20/M input, $0.60/M output
- Modelo: codestral-latest

### 2. Configurar Variables de Entorno

```bash
# Para modelos gratis
export OPENROUTER_API_KEY='sk-or-v1-xxxxxxxxxxxxxxxx'

# Para Codestral oficial (opcional)
export MISTRAL_API_KEY='sk-xxxxxxxxxxxxxxxx'

# Para hacer permanente
echo "export OPENROUTER_API_KEY='tu-key'" >> ~/.bashrc
source ~/.bashrc
```

### 3. Copiar Configuración

```bash
cp /home/spas/OPOS_GEMINI_1/.continue/config.yaml ~/.continue/config.yaml
```

### 4. Reiniciar VS Code

Cierra y reabre VS Code completamente.

## 📝 Archivos de Configuración

### config.yaml (Configuración Principal)

**Ubicación**: `~/.continue/config.yaml`

**Modelos Configurados**:
- ✅ Codestral Local (Ollama) - Prioridad 1
- ✅ Mistral Local (Ollama) - Prioridad 2
- ✅ Codestral API (Mistral) - Prioridad 3
- ✅ LiquidAI LFM2.5 (GRATIS) - Prioridad 4
- ✅ GLM 4.7 Flash (Muy barato) - Prioridad 5
- ✅ Claude Sonnet/Haiku (Backup) - Prioridad 6

### INFO-APIS-CODER-2026.md

**Contiene**:
- Documentación completa de todas las APIs
- Comparación de costos
- Ejemplos de uso
- Ranking de modelos
- Información actualizada para enero 2026

## 🎯 Modelos Disponibles

### ⭐⭐⭐⭐⭐ EXCELENTE

| Modelo | Proveedor | Costo | Velocidad | Calidad |
|--------|-----------|-------|-----------|---------|
| **LiquidAI LFM2.5 Thinking** | OpenRouter | **$0.00** | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| **LiquidAI LFM2.5 Instruct** | OpenRouter | **$0.00** | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| **Codestral API** | Mistral | $0.20/M | ⚡⚡ | ⭐⭐⭐⭐⭐ |
| **GLM 4.7 Flash** | OpenRouter | $0.07/M | ⚡⚡⚡⚡ | ⭐⭐⭐ |

### 🔄 Sistema de Prioridades

1. **Ollama Local** (más rápido, sin costo)
2. **Mistral API** (oficial, pago)
3. **Alternativas Gratis** (OpenRouter)
4. **Claude** (backup premium)

## 🔧 Personalización

### Cambiar Modelo Predeterminado

Edita `~/.continue/config.yaml` y mueve el modelo deseado al inicio:

```yaml
models:
  - name: LiquidAI LFM2.5 Thinking (GRATIS)  # Este será primero
    provider: openrouter
    model: liquid/lfm-2.5-1.2b-thinking:free
    ...
```

### Agregar Nuevos MCP Servers

En la sección `mcpServers` del `config.yaml`:

```yaml
mcpServers:
  - name: Mi Servidor
    command: npx
    args:
      - -y
      - mcp-server-example
    env:
      VAR: valor
```

### Modificar Reglas del Agente

Edita la sección `rules` en `config.yaml`:

```yaml
rules:
  - Tu regla personalizada aquí
  - Otra regla importante
  - Consider security implications
```

## ⚙️ Opciones Avanzadas

### Prompt Caching (Mistral)

```yaml
- name: Codestral API
  provider: mistral
  model: codestral-latest
  defaultCompletionOptions:
    promptCaching: true  # Reduce costos
```

### Autocomplete Optimizado

```yaml
autocompleteOptions:
  debounceDelay: 200     # ms antes de autocompletar
  maxPromptTokens: 512   # Máximo contexto
  onlyMyCode: true       # Solo código del proyecto
```

### Context Providers

```yaml
context:
  - provider: file       # Archivos del proyecto
  - provider: code       # Análisis inteligente
  - provider: diff       # Cambios recientes
  - provider: terminal   # Salida de comandos
```

### Ajustar Temperatura (Creatividad)

```yaml
defaultCompletionOptions:
  temperature: 0.7    # Creatividad (0.0-1.0)
  maxTokens: 4096     # Longitud máxima
  topP: 1.0          # Nucleus sampling
```

## 🐛 Solución de Problemas

### Error: "API Key not found"

**Solución**:
```bash
# Verificar variable
echo $OPENROUTER_API_KEY

# Configurar si falta
export OPENROUTER_API_KEY='tu-api-key'
```

### Error: "Model not available"

**Solución**:
1. Recargar VS Code (Ctrl+R)
2. Verificar config.yaml en ~/.continue/
3. Revisar logs en Developer Console

### Error: "Connection timeout"

**Solución**:
- Verificar conexión a internet
- Probar con otro modelo
- Verificar límites de API

### Codestral Local Lento

**Solución**: Usar LiquidAI gratis como alternativa principal.

### Continue no reconoce los cambios

**Solución:**
1. Cierra VS Code completamente
2. Ejecuta: `rm -rf ~/.continue` (cuidado: borra la caché)
3. Reabre VS Code
4. Recarga la configuración

### Los MCP Servers no se cargan

**Solución:**
1. Verifica el formato YAML (sin tabs, solo espacios)
2. Ejecuta: `yamllint ~/.continue/config.yaml`
3. Revisa los logs en el console de VS Code

## � Costos y Comparación

### Costos Mensuales Estimados

| Escenario | LiquidAI | GLM 4.7 | Codestral | Claude |
|-----------|----------|---------|-----------|--------|
| **Uso ligero** | **$0.00** | $0.50 | $3.00 | $30.00 |
| **Desarrollo** | **$0.00** | $2.00 | $10.00 | $100.00 |
| **Proyecto grande** | **$0.00** | $5.00 | $25.00 | $200.00 |

### Ventajas de Cada Opción

- **LiquidAI**: Completamente gratis, buena calidad
- **GLM 4.7**: Muy barato, muy rápido
- **Codestral**: Mejor para código, oficial
- **Claude**: Mejor general, pero caro

## 📚 Recursos Útiles

### Documentación
- **Continue IDE**: https://docs.continue.dev/
- **Mistral API**: https://docs.mistral.ai/api/
- **OpenRouter**: https://openrouter.ai/docs
- **LiquidAI**: https://openrouter.ai/liquid

### Consolas de API
- **Mistral**: https://console.mistral.ai/
- **OpenRouter**: https://openrouter.ai/keys
- **Anthropic**: https://console.anthropic.com/

### Modelos
- **OpenRouter Models**: https://openrouter.ai/models
- **Hugging Face**: https://huggingface.co/models?search=coder

## 🔐 Seguridad

### API Keys
- ✅ Nunca commits a git
- ✅ Usa variables de entorno
- ✅ Revoca si se compromete
- ✅ No compartir con nadie

### Variables de Entorno
```bash
# Correcto
export OPENROUTER_API_KEY='sk-or-v1-xxx'

# Incorrecto (nunca)
export OPENROUTER_API_KEY='sk-or-v1-xxx'  # en scripts públicos
```

## 📊 Monitoreo y Logs

### Ver Logs de Continue
- Abre Developer Console en VS Code (Help → Toggle Developer Tools)
- Busca errores relacionados con modelos
- Revisa network requests

### Verificar API Usage
- **OpenRouter**: https://openrouter.ai/usage
- **Mistral**: https://console.mistral.ai/usage
- **Anthropic**: https://console.anthropic.com/usage

## 🎨 Características Avanzadas

### Agent Mode
Continue puede ejecutar tareas complejas automáticamente usando modelos con tool_use.

### Multi-file Edits
Edición simultánea de múltiples archivos.

### Custom Prompts
Crear comandos personalizados con `/mi-comando`.

### Workflows
Automatizar secuencias de tareas.

## 📞 Soporte

### Comunidad
- **GitHub Continue**: https://github.com/continuedev/continue
- **Discord**: https://discord.gg/vapESyrFmJ
- **GitHub Issues**: https://github.com/continuedev/continue/issues

### Proveedores
- **Mistral Support**: https://help.mistral.ai/
- **OpenRouter Support**: https://openrouter.ai/support

## 🔄 Actualizaciones

### Mantener Actualizado
- Revisa https://openrouter.ai/models para nuevos modelos
- Actualiza config.yaml cuando salgan nuevas versiones
- Monitorea cambios en precios de APIs

### Backup de Configuración
```bash
# Backup antes de cambios
cp ~/.continue/config.yaml ~/.continue/config.yaml.backup

# Restaurar si algo falla
cp ~/.continue/config.yaml.backup ~/.continue/config.yaml
```

---

## 🎯 Recomendaciones Finales

### Para Principiantes
1. **Empieza con LiquidAI** (gratis, fácil)
2. **Agrega Mistral** si necesitas más calidad
3. **Mantén Ollama** como opción local

### Para Desarrolladores Avanzados
1. **Codestral API** como principal
2. **LiquidAI** como backup gratis
3. **Claude** para tareas complejas

### Para Equipos
1. **Mistral API** (consistente, profesional)
2. **OpenRouter** para miembros sin presupuesto
3. **Ollama local** para desarrollo offline

---

**Versión**: 2.0.0
**Fecha**: Enero 2026
**Estado**: ✅ Completo y actualizado
