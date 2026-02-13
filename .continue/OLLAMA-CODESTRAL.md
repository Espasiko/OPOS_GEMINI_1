🔧 GUÍA: Codestral + Ollama Local
═══════════════════════════════════════════════════════════════

Configuración de Continue IDE con Codestral (Mistral) en Ollama Local

## ✅ ESTADO ACTUAL (WSL + Ollama)

Modelos Disponibles:
├─ ✓ salamandra-base:latest   (7.8B, Q4_K_M)
├─ ✓ mistral:latest            (7.2B, Q4_K_M)
└─ ⏳ codestral                 (necesita instalación)

API Ollama: http://localhost:11434/api
Estado: ✓ CORRIENDO (PID: 509)

## 🚀 INSTALAR CODESTRAL EN OLLAMA

### Opción 1: Descarga Automática (Recomendado)

```bash
# Descargar Codestral (2.3B - rápido)
ollama pull codestral

# Verificar descarga
ollama list | grep codestral
```

Tiempo estimado: 5-10 minutos (depende velocidad internet)

### Opción 2: Codestral Completo (7B - mejor calidad)

```bash
# Instalar versión 7B (mejor rendimiento)
ollama pull codestral:7b

# o latest (que es la misma)
ollama pull codestral
```

### Opción 3: Ver todas las versiones disponibles

```bash
# En: https://ollama.ai/library/codestral
# O buscar en Ollama Hub
```

## 🧪 PROBAR CODESTRAL

Después de instalar:

```bash
# Probar interactivamente
ollama run codestral

# Escribir prompt y presionar Enter
# Para salir: /exit o Ctrl+D
```

## 📋 MODELOS CONFIGURADOS EN CONTINUE

```yaml
PRINCIPAL (más rápido):
└─ Codestral Local     → Chat, Edit, Agent, Autocomplete
   (Modelo recomendado para desarrollo)

ALTERNATIVAS LOCALES:
├─ Mistral Local       → Chat, Edit, Autocomplete
└─ Salamandra Local    → Chat, Edit (tu modelo personalizado)

OPCIONALES (Cloud - si tienes API key):
├─ Claude Sonnet 4.5   → Para tareas complejas
└─ Claude Haiku        → Autocomplete en la nube
```

## 💡 USO EN CONTINUE IDE

```
En VS Code:
1. Ctrl+L          → Abre Continue Chat
2. Verifica modelo → Debe mostrar "Codestral Local" como predeterminado
3. Empieza a escribir → ¡Sin latencia de API!
```

## ⚙️ CONFIGURACIÓN ACTUAL

Archivo: `/home/spas/OPOS_GEMINI_1/.continue/config.yaml`

```yaml
models:
  - name: Codestral Local      ← PRINCIPAL
    provider: ollama
    model: codestral
    apiBase: http://localhost:11434/api
    roles: [chat, edit, apply, autocomplete]
```

## 📊 COMPARATIVA DE MODELOS

| Modelo | Ubicación | Velocidad | Calidad | Sin Costo |
|--------|-----------|-----------|---------|-----------|
| **Codestral** | Local | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | ✓ |
| **Mistral** | Local | ⚡⚡⚡⚡ | ⭐⭐⭐ | ✓ |
| Salamandra | Local | ⚡⚡⚡ | ⭐⭐⭐⭐ | ✓ |
| Claude | Cloud | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | ✗ |

## 🔄 CAMBIAR MODELO PREDETERMINADO

Si quieres otro modelo como principal, edita `config.yaml`:

```yaml
# Mueve este modelo al inicio de la lista:
  - name: Mistral Local
    provider: ollama
    ...
```

El primero en la lista es el modelo predeterminado.

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "Connection refused"
```bash
# Verificar que Ollama está corriendo
ps aux | grep ollama

# Si no está, iniciar:
ollama serve
```

### Error: "Model not found"
```bash
# Verificar modelos disponibles
ollama list

# Descargar Codestral
ollama pull codestral
```

### Error: "Context length exceeded"
Reduce `maxTokens` en config.yaml para modelos locales pequeños:

```yaml
defaultCompletionOptions:
  maxTokens: 2048  # Reduce de 4096
```

### Modelo muy lento
```bash
# 1. Verificar recursos del WSL
wsl -d [nombre] -e free -h

# 2. Verificar si Ollama está usando GPU
ollama ps

# 3. Usar Haiku o modelo más pequeño
```

## 📈 OPTIMIZACIONES RECOMENDADAS

1. **Usar Codestral local** (sin costo, sin latencia)
2. **GPU en WSL2** (si disponible) para velocidad 10x
3. **Prompt Caching** (si necesitas)
4. **Temperature baja** para código (0.3-0.5)

## 🔗 RECURSOS

- Ollama: https://ollama.ai
- Codestral: https://ollama.ai/library/codestral
- Mistral Docs: https://docs.mistral.ai/
- Continue: https://docs.continue.dev/

## ✅ CHECKLIST

- [ ] Ollama corriendo en WSL
- [ ] `ollama list` muestra modelos
- [ ] `ollama pull codestral` descargado
- [ ] `config.yaml` actualizado con Ollama
- [ ] `~/.continue/config.yaml` copiado
- [ ] VS Code reiniciado
- [ ] Ctrl+L abre Continue con Codestral
- [ ] Primera prueba exitosa

═══════════════════════════════════════════════════════════════
✓ Configuración Ollama + Codestral LISTA
═══════════════════════════════════════════════════════════════
