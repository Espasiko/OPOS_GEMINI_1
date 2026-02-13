🔄 GUÍA: Copiar Configuración a VS Code
═══════════════════════════════════════════════════════════════

Esta guía explica cómo mover la configuración de Continue del proyecto 
a la ubicación correcta de VS Code.

## 📍 Ubicaciones Importantes

```
PROYECTO (actual):
/home/spas/OPOS_GEMINI_1/.continue/config.yaml

VS CODE (destino):
~/.continue/config.yaml

Expandido:
/home/spas/.continue/config.yaml
```

## 🔧 OPCIÓN 1: Comando Manual (Recomendado)

```bash
# Crear directorio si no existe
mkdir -p ~/.continue

# Copiar archivo de configuración
cp /home/spas/OPOS_GEMINI_1/.continue/config.yaml ~/.continue/config.yaml

# Verificar que se copió correctamente
ls -la ~/.continue/config.yaml

# Debería mostrar algo como:
# -rw-r--r--  1 spas spas 2.1K Jan 24 23:10 config.yaml
```

## 🔄 OPCIÓN 2: Script Automatizado

```bash
# Ejecutar script de setup
bash /home/spas/OPOS_GEMINI_1/.continue/setup-continue.sh
```

## 🎯 OPCIÓN 3: Hacerlo desde VS Code

### Método 1: Copiar y Pegar Manual
1. Abre VS Code
2. En la terminal integrada (Ctrl+`):
   ```bash
   cp /home/spas/OPOS_GEMINI_1/.continue/config.yaml ~/.continue/config.yaml
   ```
3. Recarga VS Code (Ctrl+R)

### Método 2: Abrir el archivo en VS Code
1. Abre VS Code
2. Presiona Ctrl+O (Cmd+O en Mac)
3. Ve a: `/home/spas/OPOS_GEMINI_1/.continue/config.yaml`
4. Abre el archivo
5. Presiona Ctrl+Shift+P y escribe "Save As"
6. Guarda como: `~/.continue/config.yaml`

## ✅ VERIFICACIÓN

Después de copiar, verifica:

```bash
# 1. El archivo existe
test -f ~/.continue/config.yaml && echo "✓ Archivo existe" || echo "✗ No existe"

# 2. El archivo tiene contenido
wc -l ~/.continue/config.yaml

# 3. El archivo es legible
head -20 ~/.continue/config.yaml
```

## 🔄 SINCRONIZAR CAMBIOS

Si modificas la configuración en el proyecto, sincronízala:

```bash
# Ver cambios en ambas ubicaciones
diff /home/spas/OPOS_GEMINI_1/.continue/config.yaml ~/.continue/config.yaml

# Copiar cambios (sobrescribe la versión local)
cp /home/spas/OPOS_GEMINI_1/.continue/config.yaml ~/.continue/config.yaml

# O actualizar el proyecto desde la versión local
cp ~/.continue/config.yaml /home/spas/OPOS_GEMINI_1/.continue/config.yaml
```

## 🚀 ACTIVAR EN VS CODE

Una vez copiado:

1. **Cierra VS Code completamente**
   ```bash
   killall code
   ```

2. **Reabre VS Code**
   ```bash
   code /home/spas/OPOS_GEMINI_1
   ```

3. **Abre Continue Chat** (Ctrl+L)
   - Debería reconocer los modelos Claude automáticamente

4. **Verifica en Settings**
   - Abre Continue Settings (engranaje en Continue Chat)
   - Debe mostrar los modelos disponibles

## 🐛 Si No Funciona

### Problema: "Config not found"
```bash
# Verificar ubicación exacta
ls -la ~/.continue/

# Debería mostrar config.yaml
# Si no existe, copiar nuevamente
cp /home/spas/OPOS_GEMINI_1/.continue/config.yaml ~/.continue/config.yaml
```

### Problema: "Invalid YAML"
```bash
# Validar formato YAML
yamllint ~/.continue/config.yaml

# Si hay errores, comparar
diff -u config.yaml ~/.continue/config.yaml
```

### Problema: API Key no reconocida
```bash
# Verificar variable de entorno
echo $ANTHROPIC_API_KEY

# Si está vacía, configurar
export ANTHROPIC_API_KEY='sk-ant-xxxxxxxxxxxxx'

# Agregar a ~/.bashrc permanentemente
echo "export ANTHROPIC_API_KEY='sk-ant-xxxxxxxxxxxxx'" >> ~/.bashrc
source ~/.bashrc
```

## 📊 CHECKLIST DE CONFIGURACIÓN

- [ ] API Key obtenida (https://console.anthropic.com/account/keys)
- [ ] Variable ANTHROPIC_API_KEY configurada
- [ ] Archivo copiado a ~/.continue/config.yaml
- [ ] Formato YAML válido (sin errores)
- [ ] VS Code reiniciado
- [ ] Continue Chat abierto (Ctrl+L)
- [ ] Modelos Claude visibles
- [ ] Primera prueba funcionando

## 💾 BACKUP

Hacer backup antes de cambios:

```bash
# Backup de configuración actual
cp ~/.continue/config.yaml ~/.continue/config.yaml.backup

# Backup de la versión del proyecto
cp /home/spas/OPOS_GEMINI_1/.continue/config.yaml \
   /home/spas/OPOS_GEMINI_1/.continue/config.yaml.backup

# Ver backups
ls -la ~/.continue/*.backup
```

## 🔄 VERSIONAMIENTO GIT

Para versionamiento en Git (sin exponer API key):

```bash
# 1. Crear .gitignore en ~/.continue
echo "# Ignorar archivos sensibles" > ~/.continue/.gitignore
echo ".env" >> ~/.continue/.gitignore
echo "*.key" >> ~/.continue/.gitignore

# 2. No track personal data
git config --global core.excludesfile ~/.continue/.gitignore

# 3. Commit solo la estructura (sin secrets)
git add -p config.yaml  # Revisión selectiva
```

## 📝 ARCHIVOS RELACIONADOS

- [README-CONFIGURACION.md](README-CONFIGURACION.md) - Guía completa
- [QUICK-START.md](QUICK-START.md) - 5 pasos rápidos
- [config.yaml](config.yaml) - Archivo de configuración
- [diagnose.sh](diagnose.sh) - Script de diagnóstico

═══════════════════════════════════════════════════════════════
✓ Después de seguir esta guía, Continue IDE funciona con Claude
═══════════════════════════════════════════════════════════════
