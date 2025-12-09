# Script de Restauración VS Code - Portátil
# restore_from_backup.ps1

Write-Host "🔄 Iniciando restauración de configuración VS Code..." -ForegroundColor Green

$BackupPath = "vscode_mcp_backup"

if (-not (Test-Path $BackupPath)) {
    Write-Host "❌ No se encontró carpeta de backup. Ejecuta git pull primero." -ForegroundColor Red
    Write-Host "📝 Comandos necesarios:" -ForegroundColor Yellow
    Write-Host "  git pull origin main" -ForegroundColor White
    Write-Host "  .\restore_from_backup.ps1" -ForegroundColor White
    exit 1
}

# 1. Verificar VS Code instalado
try {
    $VsCodeVersion = code --version -ErrorAction Stop
    Write-Host "✅ VS Code detectado: Versión $($VsCodeVersion[0])" -ForegroundColor Green
} catch {
    Write-Host "❌ VS Code no instalado o no en PATH" -ForegroundColor Red
    Write-Host "📥 Instala VS Code desde: https://code.visualstudio.com/" -ForegroundColor Yellow
    exit 1
}

# 2. Restaurar configuración MCP
Write-Host "🔧 Restaurando configuración MCP..." -ForegroundColor Cyan
$McpDir = "$env:APPDATA\Code\User"
New-Item -ItemType Directory -Path $McpDir -Force

if (Test-Path "$BackupPath\mcp.json") {
    Copy-Item "$BackupPath\mcp.json" "$env:APPDATA\Code\User\" -Force
    Write-Host "  ✅ mcp.json restaurado" -ForegroundColor Green
} else {
    Write-Host "  ⚠️ mcp.json no encontrado en backup" -ForegroundColor Yellow
}

# 3. Restaurar configuraciones de extensiones
$ExtSettingsSource = "$BackupPath\extension_settings"
if (Test-Path $ExtSettingsSource) {
    Write-Host "  🔧 Restaurando configuraciones de extensiones MCP..." -ForegroundColor Cyan
    $RestoredCount = 0
    Get-ChildItem -Path $ExtSettingsSource -Recurse -ErrorAction SilentlyContinue | 
        ForEach-Object {
            $RelativePath = $_.FullName.Replace([regex]::Escape($ExtSettingsSource), "")
            $DestPath = "$env:APPDATA\Code\User\globalStorage$RelativePath"
            $DestDir = Split-Path $DestPath -Parent
            New-Item -ItemType Directory -Path $DestDir -Force -ErrorAction SilentlyContinue | Out-Null
            Copy-Item $_.FullName $DestPath -Force -ErrorAction SilentlyContinue
            $RestoredCount++
        }
    Write-Host "  ✅ $RestoredCount configuraciones de extensiones restauradas" -ForegroundColor Green
}

# 4. Mostrar información de migración
if (Test-Path "$BackupPath\migration_info.json") {
    Write-Host "📋 Información de migración:" -ForegroundColor Yellow
    try {
        $MigrationInfo = Get-Content "$BackupPath\migration_info.json" | ConvertFrom-Json
        Write-Host "  📅 Fecha backup: $($MigrationInfo.timestamp)" -ForegroundColor White
        Write-Host "  🔢 VS Code version: $($MigrationInfo.vsCodeVersion)" -ForegroundColor White
        Write-Host "  📦 Extensiones disponibles: $($MigrationInfo.extensionCount)" -ForegroundColor White
        Write-Host "  🔧 MCP configurado: $($MigrationInfo.mcpConfigured)" -ForegroundColor White
        
        if ($MigrationInfo.gitAliases) {
            Write-Host "  🔗 Git aliases:" -ForegroundColor White
            $MigrationInfo.gitAliases | ForEach-Object {
                Write-Host "    $($_)" -ForegroundColor Gray
            }
        }
    } catch {
        Write-Host "  ⚠️ Error leyendo migration_info.json" -ForegroundColor Yellow
    }
}

# 5. Verificaciones finales
Write-Host "🔍 Verificando instalación..." -ForegroundColor Cyan

# Verificar MCP
if (Test-Path "$env:APPDATA\Code\User\mcp.json") {
    try {
        $McpConfig = Get-Content "$env:APPDATA\Code\User\mcp.json" | ConvertFrom-Json
        $ServerCount = ($McpConfig.servers | Get-Member -MemberType NoteProperty).Count
        Write-Host "  ✅ MCP: $ServerCount servers configurados" -ForegroundColor Green
        
        # Listar servers configurados
        $McpConfig.servers | Get-Member -MemberType NoteProperty | 
            ForEach-Object { Write-Host "    📡 $($_.Name)" -ForegroundColor Cyan }
    } catch {
        Write-Host "  ⚠️ Error en configuración MCP" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ❌ MCP no configurado" -ForegroundColor Red
}

# 6. Verificar extensiones disponibles
if (Test-Path "$BackupPath\extensions_list.txt") {
    $ExtensionsList = Get-Content "$BackupPath\extensions_list.txt"
    Write-Host "  📦 Lista de extensiones disponible: $($ExtensionsList.Count) extensiones" -ForegroundColor Green
} else {
    Write-Host "  ⚠️ Lista de extensiones no encontrada" -ForegroundColor Yellow
}

# 7. Verificar dependencias del sistema
Write-Host "🔍 Verificando dependencias del sistema..." -ForegroundColor Cyan

# Node.js (necesario para MCP servers)
try {
    $NodeVersion = node --version -ErrorAction Stop
    Write-Host "  ✅ Node.js: $NodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Node.js no instalado" -ForegroundColor Red
    Write-Host "    💡 Instalar: winget install OpenJS.NodeJS" -ForegroundColor Yellow
}

# Python (necesario para algunas extensiones AI)
try {
    $PythonVersion = python --version -ErrorAction Stop
    Write-Host "  ✅ Python: $PythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Python no instalado" -ForegroundColor Red
    Write-Host "    💡 Instalar: winget install Python.Python.3.12" -ForegroundColor Yellow
}

# Git
try {
    $GitVersion = git --version -ErrorAction Stop
    Write-Host "  ✅ Git: $GitVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Git no instalado" -ForegroundColor Red
    Write-Host "    💡 Instalar: winget install Git.Git" -ForegroundColor Yellow
}

Write-Host "🎉 Restauración completada!" -ForegroundColor Green
Write-Host "" -ForegroundColor White
Write-Host "📝 Próximos pasos:" -ForegroundColor Yellow
Write-Host "  1. Abrir VS Code: code ." -ForegroundColor White
Write-Host "  2. Activar Settings Sync:" -ForegroundColor White
Write-Host "     • Ctrl+Shift+P" -ForegroundColor Gray
Write-Host "     • Buscar: 'Settings Sync: Turn On'" -ForegroundColor Gray
Write-Host "     • Iniciar sesión con la MISMA cuenta que usaste en el PC" -ForegroundColor Gray
Write-Host "  3. Esperar sincronización automática (2-5 minutos)" -ForegroundColor White
Write-Host "  4. Verificar extensiones instaladas: Ctrl+Shift+X" -ForegroundColor White
Write-Host "  5. Reconfigurar credenciales:" -ForegroundColor White
Write-Host "     • Git: git config --global user.name 'Tu Nombre'" -ForegroundColor Gray
Write-Host "     • GitHub: gh auth login" -ForegroundColor Gray
Write-Host "     • Docker: docker login (si lo usas)" -ForegroundColor Gray

Write-Host "" -ForegroundColor White
Write-Host "🔧 Verificación rápida:" -ForegroundColor Cyan
Write-Host "  • MCP servers: Ctrl+Shift+P → 'Developer: Reload Window'" -ForegroundColor White
Write-Host "  • Extensiones: code --list-extensions | Measure-Object -Line" -ForegroundColor White
Write-Host "  • Git sync: git config --local alias.sync" -ForegroundColor White

Write-Host "" -ForegroundColor White
Write-Host "📚 Documentación completa disponible en:" -ForegroundColor Cyan
Write-Host "  📄 SINCRONIZACION_VSCODE_PORTATIL.md" -ForegroundColor White