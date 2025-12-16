# 🔄 GUÍA COMPLETA: Sincronización VS Code Windows ↔ Portátil

## 📋 **RESUMEN EJECUTIVO**

| Componente | Sincronización Automática | Acción Requerida |
|------------|---------------------------|------------------|
| **Extensiones** | ✅ Settings Sync | Automático |
| **Configuraciones** | ✅ Settings Sync | Automático |
| **Temas/UI** | ✅ Settings Sync | Automático |
| **Snippets** | ✅ Settings Sync | Automático |
| **MCP Servers** | ❌ Manual | Copiar archivos |
| **Proyectos Git** | ✅ Git Sync | `git clone` |
| **Credenciales** | ❌ Manual | Reconfigurar |

---

## 🚀 **PARTE 1: SINCRONIZACIÓN AUTOMÁTICA (SETTINGS SYNC)**

### **1.1 Activar Settings Sync en PC Actual**

```bash
# En VS Code:
# 1. Ctrl+Shift+P
# 2. Buscar: "Settings Sync: Turn On"
# 3. Seleccionar cuenta GitHub/Microsoft
# 4. Confirmar elementos a sincronizar:
```

**Elementos que se sincronizan automáticamente:**
- ✅ **Settings**: Todas las configuraciones de VS Code
- ✅ **Extensions**: Lista y configuración de extensiones
- ✅ **Keybindings**: Atajos de teclado personalizados
- ✅ **Snippets**: Fragmentos de código personalizados
- ✅ **UI State**: Estado de paneles, tema, fuentes
- ✅ **Global State**: Configuraciones globales

### **1.2 Configurar Settings Sync en Portátil**

```bash
# 1. Descargar e instalar VS Code en portátil
# 2. Abrir VS Code
# 3. Ctrl+Shift+P → "Settings Sync: Turn On"
# 4. Iniciar sesión con LA MISMA cuenta
# 5. Seleccionar "Merge" o "Replace Local"
# 6. ¡Listo! Todo se descarga automáticamente
```

---

## 🔧 **PARTE 2: CONFIGURACIÓN MANUAL MCP SERVERS**

### **2.1 Archivos MCP Detectados en tu Sistema**

```
Configuración Principal:
📁 C:\Users\USER\AppData\Roaming\Code\User\mcp.json

Configuraciones por Extensión:
📁 globalStorage\rooveterinaryinc.roo-cline\settings\mcp_settings.json
📁 globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json
📁 globalStorage\streamax.claude-dev-streamax\settings\cline_mcp_settings.json
📁 globalStorage\zhucan.debug-cline\settings\cline_mcp_settings.json

Cache MCP:
📁 C:\Users\USER\AppData\Roaming\Code\User\mcp\
📁 C:\Users\USER\AppData\Roaming\Code\User\sync\mcp\
```

### **2.2 MCP Servers Configurados Actualmente**

| Servidor | Tipo | Comando | Estado |
|----------|------|---------|---------|
| **huggingface** | HTTP | https://hf.co/mcp | ✅ Activo |
| **markitdown** | stdio | uvx markitdown-mcp | ✅ Activo |
| **imagesorcery** | stdio | uvx imagesorcery-mcp | ✅ Activo |
| **deepwiki** | HTTP | https://mcp.deepwiki.com/sse | ✅ Activo |
| **github** | HTTP | https://api.githubcopilot.com/mcp/ | ✅ Activo |
| **playwright** | stdio | npx @playwright/mcp | ✅ Activo |
| **convex** | stdio | npx convex mcp start | ✅ Activo |
| **Vercel** | HTTP | https://mcp.vercel.com | ✅ Activo |
| **serena** | stdio | uvx serena start-mcp-server | ✅ Activo |
| **chrome-devtools** | stdio | npx chrome-devtools-mcp | ✅ Activo |

### **2.3 Script de Backup MCP (Ejecutar en PC Actual)**

```powershell
# Crear carpeta de backup MCP
$BackupPath = "E:\1\OPOS_GEMINI_1\vscode_mcp_backup"
New-Item -ItemType Directory -Path $BackupPath -Force

# Copiar configuración principal MCP
Copy-Item "$env:APPDATA\Code\User\mcp.json" "$BackupPath\" -Force

# Copiar configuraciones de extensiones MCP
$McpSettingsPath = "$BackupPath\extension_settings"
New-Item -ItemType Directory -Path $McpSettingsPath -Force

# Buscar y copiar todos los archivos MCP
Get-ChildItem -Path "$env:APPDATA\Code\User\globalStorage" -Recurse -Filter "*mcp*" | 
    Copy-Item -Destination $McpSettingsPath -Force -Recurse

Write-Host "✅ Backup MCP completado en: $BackupPath" -ForegroundColor Green
Write-Host "📂 Archivos guardados:" -ForegroundColor Cyan
Get-ChildItem -Path $BackupPath -Recurse | Format-Table Name, Length, LastWriteTime
```

### **2.4 Script de Restauración MCP (Ejecutar en Portátil)**

```powershell
# En el portátil, después de clonar el repositorio:
$BackupPath = "E:\1\OPOS_GEMINI_1\vscode_mcp_backup"  # Ajustar ruta según portátil

# Crear directorio MCP si no existe
$McpDir = "$env:APPDATA\Code\User"
New-Item -ItemType Directory -Path $McpDir -Force

# Restaurar configuración principal
Copy-Item "$BackupPath\mcp.json" "$env:APPDATA\Code\User\" -Force

# Restaurar configuraciones de extensiones
$ExtSettingsSource = "$BackupPath\extension_settings"
if (Test-Path $ExtSettingsSource) {
    Get-ChildItem -Path $ExtSettingsSource -Recurse | 
        ForEach-Object {
            $RelativePath = $_.FullName.Replace($ExtSettingsSource, "")
            $DestPath = "$env:APPDATA\Code\User\globalStorage$RelativePath"
            $DestDir = Split-Path $DestPath -Parent
            New-Item -ItemType Directory -Path $DestDir -Force -ErrorAction SilentlyContinue
            Copy-Item $_.FullName $DestPath -Force
        }
}

Write-Host "✅ Restauración MCP completada" -ForegroundColor Green
```

---

## 📦 **PARTE 3: EXTENSIONES DETECTADAS**

### **3.1 Lista Completa de Extensiones (Auto-sincronizadas)**

```
🏷️ DESARROLLO AI:
├── continue.continue (Continue AI)
├── danielsanmedium.dscodegpt (DS Code GPT)
├── emdashcodes.prompt-link (Prompt Link)
├── github.copilot (GitHub Copilot)
├── github.copilot-chat (GitHub Copilot Chat)
├── kingleo.deepseek-web (DeepSeek Web)
├── rooveterinaryinc.roo-cline (Roo Cline)
├── saoudrizwan.claude-dev (Claude Dev)
├── streamax.claude-dev-streamax (Claude Dev Streamax)
├── your-name.mistralvs (Mistral VS)
└── zhucan.debug-cline (Debug Cline)

🔧 DESARROLLO WEB:
├── christian-kohler.path-intellisense (Path IntelliSense)
├── connor4312.esbuild-problem-matchers (ESBuild Problems)
├── dbaeumer.vscode-eslint (ESLint)
├── editorconfig.editorconfig (EditorConfig)
├── mikestead.dotenv (DotEnv)
├── orta.vscode-jest (Jest)
├── tgreen7.vs-code-node-require (Node Require)
├── visualstudioexptteam.intellicode-api-usage-examples (IntelliCode API)
├── visualstudioexptteam.vscodeintellicode (IntelliCode)
├── wallabyjs.quokka-vscode (Quokka.js)
└── wix.vscode-import-cost (Import Cost)

🐳 DOCKER/CONTAINERS:
├── docker.docker (Docker)
├── formulahendry.docker-explorer (Docker Explorer)
├── formulahendry.docker-extension-pack (Docker Extension Pack)
├── george3447.docker-run (Docker Run)
├── ms-azuretools.vscode-containers (Dev Containers)
├── ms-azuretools.vscode-docker (Docker)
├── ms-kubernetes-tools.vscode-kubernetes-tools (Kubernetes)
└── p1c2u.docker-compose (Docker Compose)

🔗 GIT/REMOTE:
├── donjayamanne.githistory (Git History)
├── eamodio.gitlens (GitLens)
├── github.vscode-pull-request-github (GitHub Pull Requests)
├── ms-vscode-remote.remote-containers (Remote Containers)
├── ms-vscode-remote.remote-ssh (Remote SSH)
├── ms-vscode-remote.remote-ssh-edit (Remote SSH Edit)
├── ms-vscode-remote.remote-wsl (Remote WSL)
├── ms-vscode.remote-explorer (Remote Explorer)
└── ms-vsliveshare.vsliveshare (Live Share)

🎨 UI/UTILIDADES:
├── afractal.node-essentials (Node Essentials)
├── be5invis.vscode-icontheme-nomo-dark (Nomo Dark Icons)
├── mechatroner.rainbow-csv (Rainbow CSV)
├── ms-vscode.powershell (PowerShell)
├── redhat.vscode-yaml (YAML)
├── sarthikbhat.json-server (JSON Server)
├── timheuer.jsondbg (JSON Debug)
└── tomoki1207.pdf (PDF Viewer)
```

---

## 🚀 **PARTE 4: PROCESO COMPLETO DE MIGRACIÓN**

### **4.1 Preparación en PC Actual**

```powershell
# 1. Activar Settings Sync
# Ctrl+Shift+P → "Settings Sync: Turn On"

# 2. Crear backup MCP
$BackupPath = "E:\1\OPOS_GEMINI_1\vscode_mcp_backup"
New-Item -ItemType Directory -Path $BackupPath -Force
Copy-Item "$env:APPDATA\Code\User\mcp.json" "$BackupPath\" -Force
Get-ChildItem -Path "$env:APPDATA\Code\User\globalStorage" -Recurse -Filter "*mcp*" | 
    Copy-Item -Destination "$BackupPath\extension_settings" -Force -Recurse

# 3. Commit y push del backup
git add vscode_mcp_backup/
git commit -m "backup: Configuración MCP para sincronización portátil"
git push origin main
```

### **4.2 Configuración en Portátil Nuevo**

```bash
# 1. Instalar VS Code
# Descargar desde: https://code.visualstudio.com/

# 2. Clonar repositorio
git clone https://github.com/Espasiko/OPOS_GEMINI_1.git
cd OPOS_GEMINI_1

# 3. Activar Settings Sync en VS Code
# Ctrl+Shift+P → "Settings Sync: Turn On"
# Usar LA MISMA cuenta GitHub/Microsoft

# 4. Esperar sincronización automática (2-5 minutos)

# 5. Restaurar configuración MCP
# Ejecutar script de restauración PowerShell
```

### **4.3 Verificación Post-Migración**

```powershell
# Verificar extensiones instaladas
code --list-extensions | Measure-Object -Line

# Verificar configuración MCP
if (Test-Path "$env:APPDATA\Code\User\mcp.json") {
    Write-Host "✅ MCP configurado correctamente" -ForegroundColor Green
    Get-Content "$env:APPDATA\Code\User\mcp.json" | ConvertFrom-Json | 
        Select-Object -ExpandProperty servers | 
        Get-Member -MemberType NoteProperty | 
        ForEach-Object { Write-Host "  📡 $($_.Name)" -ForegroundColor Cyan }
} else {
    Write-Host "❌ MCP no configurado" -ForegroundColor Red
}

# Verificar Git sync alias
git config --local alias.sync
```

---

## 📝 **PARTE 5: CONFIGURACIONES ESPECÍFICAS QUE NECESITAN ATENCIÓN**

### **5.1 Rutas que Cambiarán en Portátil**

```json
// Configuraciones que pueden necesitar ajuste:
{
    "terminal.integrated.defaultProfile.windows": "PowerShell",
    "python.defaultInterpreterPath": "C:\\Python\\python.exe",
    "docker.dockerPath": "docker",
    "git.path": "git",
    // Rutas de proyectos locales
    "workbench.startupEditor": "none",
    // Configuraciones de proxy si usas VPN corporativa
    "http.proxy": "",
    "https.proxy": ""
}
```

### **5.2 Credenciales a Reconfigurar**

```bash
# En el portátil, será necesario reconfigurar:
# 1. Git credentials
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"

# 2. GitHub token (si usas HTTPS)
gh auth login

# 3. Docker Hub credentials
docker login

# 4. Extensiones que requieren API keys:
#    - Hugging Face token
#    - OpenAI API key (si usas extensiones AI)
#    - Otras APIs específicas
```

### **5.3 Dependencias del Sistema**

```powershell
# Herramientas que se deben instalar en portátil:
# 1. Node.js (para extensiones MCP)
winget install OpenJS.NodeJS

# 2. Python (para extensiones AI)
winget install Python.Python.3.12

# 3. Git
winget install Git.Git

# 4. Docker Desktop
winget install Docker.DockerDesktop

# 5. WSL (si usas desarrollo híbrido)
wsl --install
```

---

## 🎯 **PARTE 6: SCRIPTS DE AUTOMATIZACIÓN**

### **6.1 Script Completo de Migración (PC Actual)**

```powershell
# migrate_to_laptop.ps1
param(
    [Parameter(Mandatory=$true)]
    [string]$BackupBranch = "laptop-sync"
)

Write-Host "🚀 Iniciando migración de configuración VS Code..." -ForegroundColor Green

# 1. Crear backup MCP
$BackupPath = "vscode_mcp_backup"
New-Item -ItemType Directory -Path $BackupPath -Force

Write-Host "📦 Creando backup MCP..." -ForegroundColor Cyan
Copy-Item "$env:APPDATA\Code\User\mcp.json" "$BackupPath\" -Force -ErrorAction SilentlyContinue

$McpSettingsPath = "$BackupPath\extension_settings"
New-Item -ItemType Directory -Path $McpSettingsPath -Force
Get-ChildItem -Path "$env:APPDATA\Code\User\globalStorage" -Recurse -Filter "*mcp*" -ErrorAction SilentlyContinue | 
    Copy-Item -Destination $McpSettingsPath -Force -Recurse

# 2. Exportar lista de extensiones
Write-Host "📋 Exportando lista de extensiones..." -ForegroundColor Cyan
code --list-extensions > "$BackupPath\extensions_list.txt"

# 3. Exportar configuraciones adicionales
Write-Host "⚙️ Exportando configuraciones..." -ForegroundColor Cyan
@{
    extensions = (code --list-extensions)
    mcpConfigured = Test-Path "$env:APPDATA\Code\User\mcp.json"
    gitAliases = (git config --local --list | Where-Object { $_ -like "alias.*" })
    vsCodeVersion = (code --version)[0]
    timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
} | ConvertTo-Json -Depth 3 | Out-File "$BackupPath\migration_info.json"

# 4. Commit y push
Write-Host "📤 Guardando en repositorio..." -ForegroundColor Cyan
git add $BackupPath/
git commit -m "migrate: Configuración VS Code completa para portátil

- Backup configuración MCP servers
- Lista de extensiones ($(code --list-extensions | Measure-Object -Line | Select-Object -ExpandProperty Lines))
- Configuraciones de desarrollo
- Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
"

git push origin main

Write-Host "✅ Migración completada. Archivos listos en: $BackupPath" -ForegroundColor Green
Write-Host "📱 En el portátil ejecuta: .\restore_from_backup.ps1" -ForegroundColor Yellow
```

### **6.2 Script Completo de Restauración (Portátil)**

```powershell
# restore_from_backup.ps1
Write-Host "🔄 Iniciando restauración de configuración VS Code..." -ForegroundColor Green

$BackupPath = "vscode_mcp_backup"

if (-not (Test-Path $BackupPath)) {
    Write-Host "❌ No se encontró carpeta de backup. Ejecuta git pull primero." -ForegroundColor Red
    exit 1
}

# 1. Restaurar configuración MCP
Write-Host "🔧 Restaurando configuración MCP..." -ForegroundColor Cyan
$McpDir = "$env:APPDATA\Code\User"
New-Item -ItemType Directory -Path $McpDir -Force

if (Test-Path "$BackupPath\mcp.json") {
    Copy-Item "$BackupPath\mcp.json" "$env:APPDATA\Code\User\" -Force
    Write-Host "  ✅ mcp.json restaurado" -ForegroundColor Green
}

# 2. Restaurar configuraciones de extensiones
$ExtSettingsSource = "$BackupPath\extension_settings"
if (Test-Path $ExtSettingsSource) {
    Write-Host "  🔧 Restaurando configuraciones de extensiones MCP..." -ForegroundColor Cyan
    Get-ChildItem -Path $ExtSettingsSource -Recurse -ErrorAction SilentlyContinue | 
        ForEach-Object {
            $RelativePath = $_.FullName.Replace($ExtSettingsSource, "")
            $DestPath = "$env:APPDATA\Code\User\globalStorage$RelativePath"
            $DestDir = Split-Path $DestPath -Parent
            New-Item -ItemType Directory -Path $DestDir -Force -ErrorAction SilentlyContinue
            Copy-Item $_.FullName $DestPath -Force -ErrorAction SilentlyContinue
        }
    Write-Host "  ✅ Configuraciones de extensiones restauradas" -ForegroundColor Green
}

# 3. Mostrar información de migración
if (Test-Path "$BackupPath\migration_info.json") {
    $MigrationInfo = Get-Content "$BackupPath\migration_info.json" | ConvertFrom-Json
    Write-Host "📋 Información de migración:" -ForegroundColor Yellow
    Write-Host "  📅 Fecha backup: $($MigrationInfo.timestamp)" -ForegroundColor White
    Write-Host "  🔢 VS Code version: $($MigrationInfo.vsCodeVersion)" -ForegroundColor White
    Write-Host "  📦 Extensiones: $($MigrationInfo.extensions.Count)" -ForegroundColor White
    Write-Host "  🔧 MCP configurado: $($MigrationInfo.mcpConfigured)" -ForegroundColor White
}

# 4. Verificaciones finales
Write-Host "🔍 Verificando instalación..." -ForegroundColor Cyan

# Verificar MCP
if (Test-Path "$env:APPDATA\Code\User\mcp.json") {
    $McpConfig = Get-Content "$env:APPDATA\Code\User\mcp.json" | ConvertFrom-Json
    $ServerCount = ($McpConfig.servers | Get-Member -MemberType NoteProperty).Count
    Write-Host "  ✅ MCP: $ServerCount servers configurados" -ForegroundColor Green
} else {
    Write-Host "  ❌ MCP no configurado" -ForegroundColor Red
}

# Verificar VS Code
try {
    $VsCodeInstalled = code --version -ErrorAction SilentlyContinue
    if ($VsCodeInstalled) {
        Write-Host "  ✅ VS Code: Versión $($VsCodeInstalled[0])" -ForegroundColor Green
    }
} catch {
    Write-Host "  ❌ VS Code no instalado o no en PATH" -ForegroundColor Red
}

Write-Host "🎉 Restauración completada!" -ForegroundColor Green
Write-Host "📝 Próximos pasos:" -ForegroundColor Yellow
Write-Host "  1. Abrir VS Code: code ." -ForegroundColor White
Write-Host "  2. Activar Settings Sync: Ctrl+Shift+P → 'Settings Sync: Turn On'" -ForegroundColor White
Write-Host "  3. Verificar extensiones en unos minutos" -ForegroundColor White
Write-Host "  4. Reconfigurar credenciales si es necesario" -ForegroundColor White
```

---

## 🎯 **RESUMEN EJECUTIVO FINAL**

### **✅ Lo que se sincroniza AUTOMÁTICAMENTE:**
- ✅ Todas las 44+ extensiones
- ✅ Configuraciones de VS Code
- ✅ Temas y UI personalizada  
- ✅ Atajos de teclado
- ✅ Snippets de código

### **🔧 Lo que requiere CONFIGURACIÓN MANUAL:**
- 🔧 MCP Servers (10+ configurados)
- 🔧 Credenciales (Git, GitHub, Docker)
- 🔧 Rutas específicas del sistema
- 🔧 Dependencias (Node.js, Python, Docker)

### **⏱️ Tiempo estimado de migración:**
- **Settings Sync**: 2-5 minutos (automático)
- **MCP Servers**: 5 minutos (con scripts)
- **Credenciales**: 10 minutos (manual)
- **Verificación**: 5 minutos

**🎉 TOTAL: ~20-25 minutos para migración completa**

---

*💡 **Consejo Pro**: Ejecuta el script de migración antes de configurar el portátil. El backup se guarda en Git, así que estará disponible inmediatamente después del `git clone`.*

*🔄 **Mantenimiento**: Después de la configuración inicial, Settings Sync mantendrá automáticamente la sincronización de extensiones y configuraciones. Solo los MCP servers necesitan backup/restore manual cuando cambies de máquina.*