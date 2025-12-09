# 🔄 GUÍA COMPLETA: Git Sync Multi-Máquina

**Fecha:** 9 Diciembre 2025  
**Proyecto:** OPOS_GEMINI_1  
**Objetivo:** Sincronización perfecta entre múltiples máquinas y entornos

---

## 🎯 **RESUMEN EJECUTIVO**

Esta guía te permite trabajar en el proyecto desde **cualquier máquina** (portátil, PC, WSL, Linux, Mac) manteniendo perfecta sincronización del código y configuración Git.

### ✅ **LO QUE CONSEGUIRÁS:**
- Sincronización automática entre Windows ↔ WSL ↔ Cualquier máquina
- Alias `git sync` funcionando en todos lados
- Flujo de trabajo consistente en VS Code/cualquier IDE
- Respaldo automático de cambios locales

---

## 🔧 **CONFIGURACIÓN INICIAL**

### **PASO 1: Clonar el Repositorio**

```bash
# En cualquier máquina nueva
git clone https://github.com/Espasiko/OPOS_GEMINI_1.git
cd OPOS_GEMINI_1

# Verificar que todo está sincronizado
git status
git log --oneline -5
```

### **PASO 2: Verificar Alias Automático**

El alias `git sync` **YA ESTÁ CONFIGURADO** en el repositorio:

```bash
# Verificar que el alias existe
git config --local --list | grep sync

# Debería mostrar:
# alias.sync=!git stash -u && git checkout main && git pull origin main
```

### **PASO 3: Configurar Git Personal (Solo primera vez)**

```bash
# Configurar tu identidad (solo una vez por máquina)
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# Verificar configuración
git config --global --list
```

---

## 🚀 **COMANDOS ESENCIALES**

### **📥 SINCRONIZAR CON GITHUB (Bajar cambios)**

```bash
# Comando principal - úsalo siempre antes de trabajar
git sync

# ¿Qué hace internamente?
# 1. git stash -u     → Guarda tus cambios locales
# 2. git checkout main → Cambia a rama principal  
# 3. git pull origin main → Descarga últimos cambios
```

### **📤 SUBIR CAMBIOS A GITHUB**

```bash
# Flujo completo para subir cambios
git add archivo1.py archivo2.md          # Añadir archivos específicos
git add .                               # O añadir todos los cambios

git commit -m "📊 Descripción del cambio"  # Crear commit con mensaje

git push origin main                    # Subir a GitHub
```

### **🔍 COMANDOS DE VERIFICACIÓN**

```bash
# Ver estado actual
git status

# Ver últimos commits
git log --oneline -10

# Ver diferencias no guardadas
git diff

# Ver ramas disponibles
git branch -v
```

---

## 📱 **FLUJO DE TRABAJO MULTI-MÁQUINA**

### **💻 ESCENARIO: Trabajas en PC Principal**

1. **Antes de empezar:**
   ```bash
   git sync  # Sincronizar con GitHub
   ```

2. **Trabajar normalmente:**
   - Editar archivos en VS Code
   - Crear/modificar scripts
   - Probar funcionalidad

3. **Al terminar:**
   ```bash
   git add .
   git commit -m "✨ Nueva funcionalidad terminada"
   git push origin main
   ```

### **🔄 ESCENARIO: Cambias a Portátil/Otra Máquina**

1. **Primer setup (solo una vez):**
   ```bash
   git clone https://github.com/Espasiko/OPOS_GEMINI_1.git
   cd OPOS_GEMINI_1
   ```

2. **Cada vez que trabajas:**
   ```bash
   git sync  # ¡Automáticamente tienes los últimos cambios!
   ```

3. **Continuar trabajando:**
   - Abrir VS Code: `code .`
   - Todos tus cambios del PC principal están ahí
   - Continuar desde donde lo dejaste

4. **Al terminar:**
   ```bash
   git add .
   git commit -m "🔧 Mejoras desde portátil"
   git push origin main
   ```

### **🌊 ESCENARIO: Vuelta al PC Principal**

```bash
git sync  # ¡Automáticamente tienes los cambios del portátil!
```

---

## 🛠 **CONFIGURACIÓN ESPECÍFICA POR ENTORNO**

### **🪟 WINDOWS (PowerShell)**

```powershell
# Navegar al proyecto
cd E:\1\OPOS_GEMINI_1

# Verificar alias funciona
git sync

# Abrir VS Code
code .
```

### **🐧 WSL (Linux Ubuntu)**

```bash
# Navegar al proyecto
cd ~/OPOS_GEMINI_1

# Verificar alias funciona  
git sync

# Abrir VS Code desde WSL
code .
```

### **💻 PORTÁTIL/NUEVA MÁQUINA**

```bash
# Primera vez
git clone https://github.com/Espasiko/OPOS_GEMINI_1.git
cd OPOS_GEMINI_1

# Configurar identidad
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# Sincronizar
git sync

# Abrir en tu IDE favorito
code .        # VS Code
idea .        # IntelliJ
subl .        # Sublime
```

---

## 🔧 **CONFIGURACIÓN AVANZADA**

### **📋 ALIAS ADICIONALES ÚTILES**

```bash
# Añadir más aliases útiles (ejecutar una vez por máquina)
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.ps push
git config --global alias.pl pull

# Ahora puedes usar:
git st    # en lugar de git status
git br    # en lugar de git branch
git cm -m "mensaje"  # en lugar de git commit -m "mensaje"
```

### **🎨 CONFIGURACIÓN VISUAL**

```bash
# Mejor visualización de logs
git config --global alias.lg "log --oneline --graph --decorate --all"

# Colores en terminal
git config --global color.ui auto

# Editor preferido
git config --global core.editor "code --wait"  # VS Code
# git config --global core.editor "nano"       # Nano (Linux)
```

---

## 🆘 **RESOLUCIÓN DE PROBLEMAS**

### **❌ "El alias sync no existe"**

**Problema:** En máquina nueva no funciona `git sync`

**Solución:**
```bash
cd OPOS_GEMINI_1
git config --local alias.sync '!git stash -u && git checkout main && git pull origin main'
git sync  # Ahora debería funcionar
```

### **⚠️ "Conflictos de merge"**

**Problema:** Cambios conflictivos entre máquinas

**Solución:**
```bash
git sync           # Intenta sincronizar
git stash list     # Ver cambios guardados
git stash show -p  # Ver qué cambios tienes

# Si hay conflictos, resolverlos manualmente
git stash pop      # Aplicar tus cambios
# Resolver conflictos en VS Code
git add .
git commit -m "🔀 Resolver conflictos"
git push origin main
```

### **🚫 "Cambios no guardados se perderán"**

**Problema:** Tienes cambios sin commit y quieres sincronizar

**Solución:**
```bash
# Opción 1: Guardar cambios temporalmente
git stash -u       # Guardar todo
git pull origin main
git stash pop      # Recuperar tus cambios

# Opción 2: Commitear directamente
git add .
git commit -m "🚧 WIP: Trabajo en progreso"
git push origin main
```

---

## 📊 **COMANDOS DE MONITOREO**

### **📈 ESTADO DEL REPOSITORIO**

```bash
# Estado completo
git status --porcelain

# Ver cambios pendientes
git diff --stat

# Ver último commit
git log -1 --stat

# Ver archivos ignorados (.gitignore)
git status --ignored
```

### **🔍 VERIFICAR SINCRONIZACIÓN**

```bash
# Comparar con GitHub
git fetch origin
git log HEAD..origin/main --oneline  # Commits que faltan bajar
git log origin/main..HEAD --oneline  # Commits que faltan subir

# Si ambos están vacíos = perfectamente sincronizado
```

---

## 📝 **MEJORES PRÁCTICAS**

### **✅ HACER SIEMPRE:**

1. **Antes de trabajar:** `git sync`
2. **Commits frecuentes:** No acumules muchos cambios
3. **Mensajes descriptivos:** `git commit -m "🐛 Fix: Corregir error en dataset"`
4. **Push al terminar:** `git push origin main`

### **❌ EVITAR:**

1. **No sincronizar** antes de empezar a trabajar
2. **Commits enormes** con muchos archivos diferentes
3. **Mensajes vagos:** "cambios", "fix", "update"
4. **Dejar cambios sin subir** al cambiar de máquina

### **📋 WORKFLOW RECOMENDADO:**

```bash
# 🌅 Al empezar el día
git sync

# 🔨 Mientras trabajas (cada 1-2 horas)
git add .
git commit -m "🚧 WIP: Avance en funcionalidad X"
git push origin main

# 🌙 Al terminar el día
git add .
git commit -m "✅ Completado: Funcionalidad X terminada"  
git push origin main
```

---

## 🎯 **ESCENARIOS ESPECÍFICOS DEL PROYECTO**

### **📊 TRABAJANDO CON DATASETS**

```bash
# Los datasets grandes están en .gitignore
# Solo se suben los scripts de generación

git add dataset_generator/nuevo_script.py
git commit -m "📊 Nuevo generador de QA para DeepSeek"
git push origin main
```

### **🚀 TRABAJANDO CON DOCKER**

```bash
# Docker configs se sincronizan
# Pero no se suben los volúmenes/storage

git add backend/Dockerfile backend/docker-compose.yml
git commit -m "🐳 Docker: Configuración mejorada"
git push origin main
```

### **📖 DOCUMENTACIÓN**

```bash
# Documentación siempre se sube
git add *.md docs/**/*.md
git commit -m "📖 Docs: Actualizar guías y manuales"  
git push origin main
```

---

## 📱 **INTEGRACIÓN CON VS CODE**

### **⚙️ EXTENSIONES RECOMENDADAS:**

1. **Git Extension Pack** - Gestión visual de Git
2. **GitLens** - Información detallada de commits
3. **Git Graph** - Visualización de ramas
4. **Remote - WSL** - Para trabajar con WSL

### **🎮 ATAJOS VS CODE:**

- `Ctrl+Shift+G` - Abrir panel Git
- `Ctrl+Shift+P` → "Git: Sync" - Sincronizar
- `Ctrl+K Ctrl+C` - Commit cambios
- `F1` → "Git: Push" - Subir cambios

---

## 🎉 **RESULTADO FINAL**

Con esta configuración tendrás:

✅ **Sincronización perfecta** entre todas tus máquinas  
✅ **Comando único** `git sync` que funciona en todos lados  
✅ **Flujo de trabajo consistente** sin importar el entorno  
✅ **Respaldo automático** de todos tus cambios  
✅ **Colaboración fácil** con otros desarrolladores

### **🚀 PRUEBA FINAL:**

1. **En máquina A:** Crear un archivo `test_sync.txt`
2. **Commit y push:** `git add . && git commit -m "test" && git push origin main`
3. **En máquina B:** `git sync`
4. **Verificar:** El archivo `test_sync.txt` debe aparecer

¡Si funciona, ya tienes sincronización perfecta multi-máquina! 🎯

---

*Guía creada: 9 Diciembre 2025*  
*Proyecto: OPOS_GEMINI_1*  
*Autor: GitHub Copilot + Espasiko*