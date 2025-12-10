# Script de Migración VS Code - PC Principal
# migrate_to_laptop.ps1
param(
    [Parameter(Mandatory=$false)]
    [string]$BackupBranch = "main"
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
$ExtensionsList = code --list-extensions
@{
    extensions = $ExtensionsList
    extensionCount = $ExtensionsList.Count
    mcpConfigured = Test-Path "$env:APPDATA\Code\User\mcp.json"
    gitAliases = (git config --local --list | Where-Object { $_ -like "alias.*" })
    vsCodeVersion = (code --version)[0]
    timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    backupPath = $BackupPath
} | ConvertTo-Json -Depth 3 | Out-File "$BackupPath\migration_info.json"

# 4. Verificar backup
Write-Host "🔍 Verificando backup..." -ForegroundColor Cyan
$BackupFiles = Get-ChildItem -Path $BackupPath -Recurse
$BackupSize = ($BackupFiles | Measure-Object -Property Length -Sum).Sum / 1KB

Write-Host "📊 Resumen del backup:" -ForegroundColor Yellow
Write-Host "  📁 Archivos: $($BackupFiles.Count)" -ForegroundColor White
Write-Host "  💾 Tamaño: $([math]::Round($BackupSize, 2)) KB" -ForegroundColor White
Write-Host "  🔧 MCP configurado: $(Test-Path "$BackupPath\mcp.json")" -ForegroundColor White
Write-Host "  📦 Extensiones: $($ExtensionsList.Count)" -ForegroundColor White

# 5. Commit y push
Write-Host "📤 Guardando en repositorio..." -ForegroundColor Cyan
git add $BackupPath/

$CommitMessage = @"
migrate: Configuración VS Code completa para portátil

- Backup configuración MCP servers
- Lista de $($ExtensionsList.Count) extensiones
- Configuraciones de desarrollo
- Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

Archivos incluidos:
- mcp.json (configuración principal MCP)
- extensions_list.txt (lista de extensiones)
- migration_info.json (metadata de migración)
- extension_settings/ (configuraciones específicas MCP)

Para restaurar en portátil:
1. git clone https://github.com/Espasiko/OPOS_GEMINI_1.git
2. cd OPOS_GEMINI_1
3. .\restore_from_backup.ps1
"@

git commit -m $CommitMessage

Write-Host "🔗 Enviando al repositorio..." -ForegroundColor Cyan
git push origin $BackupBranch

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Migración completada exitosamente!" -ForegroundColor Green
    Write-Host "🔗 Repositorio actualizado en GitHub" -ForegroundColor Green
} else {
    Write-Host "⚠️ Error en git push. Verifica conexión." -ForegroundColor Yellow
}

Write-Host "📱 En el portátil ejecuta:" -ForegroundColor Yellow
Write-Host "  git clone https://github.com/Espasiko/OPOS_GEMINI_1.git" -ForegroundColor White
Write-Host "  cd OPOS_GEMINI_1" -ForegroundColor White
Write-Host "  .\restore_from_backup.ps1" -ForegroundColor White

Write-Host "📋 Archivos listos en: $BackupPath" -ForegroundColor Cyan