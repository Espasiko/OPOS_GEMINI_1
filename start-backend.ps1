# OpositaIA Backend Startup Script for Windows PowerShell
# This script starts the FastAPI backend running in WSL

param(
    [switch]$Compose = $false,
    [switch]$Clean = $false,
    [switch]$Help = $false
)

$ErrorActionPreference = "Stop"

# Colors for output
$InfoColor = "Cyan"
$SuccessColor = "Green"
$WarningColor = "Yellow"
$ErrorColor = "Red"

function Write-Info { Write-Host $args -ForegroundColor $InfoColor }
function Write-Success { Write-Host $args -ForegroundColor $SuccessColor }
function Write-Warning { Write-Host $args -ForegroundColor $WarningColor }
function Write-Error-Custom { Write-Host $args -ForegroundColor $ErrorColor }

function Show-Help {
    Write-Info @"
OpositaIA Backend Startup Script

USAGE:
    .\start-backend.ps1 [options]

OPTIONS:
    -Compose   : Use docker-compose to start services (Qdrant + PostgreSQL + Backend)
    -Clean     : Remove all containers and volumes before starting (dangerous!)
    -Help      : Show this help message

EXAMPLES:
    # Start backend only (uses existing PostgreSQL + Qdrant)
    .\start-backend.ps1

    # Start with docker-compose (recommended first time)
    .\start-backend.ps1 -Compose

    # Clean and start fresh
    .\start-backend.ps1 -Compose -Clean

NOTES:
    - Ollama must be running in WSL on localhost:11434
    - PostgreSQL needs to be running on localhost:5432
    - Qdrant needs to be running on localhost:6333
    - All paths assume you're running from project root

REQUIREMENTS:
    - WSL with Docker installed
    - Python 3.12.3+ in WSL
    - Ollama running in WSL
"@
}

function Test-Prerequisites {
    Write-Info "🔍 Verificando requisitos previos..."
    
    # Check WSL
    wsl echo "OK" 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Custom "❌ WSL no está disponible"
        exit 1
    }
    Write-Success "✅ WSL disponible"
    
    # Check Docker in WSL
    wsl which docker 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Custom "❌ Docker no está instalado en WSL"
        exit 1
    }
    Write-Success "✅ Docker instalado en WSL"
    
    # Check Python in WSL
    $pythonCheck = wsl python3 --version 2>&1
    Write-Success "✅ Python en WSL: $pythonCheck"
    
    # Check Ollama
    Write-Info "Verificando Ollama en localhost:11434..."
    $ollamaCheck = wsl curl -s http://localhost:11434/api/tags 2>&1
    if ($ollamaCheck -like "*model*") {
        Write-Success "✅ Ollama está corriendo"
    } else {
        Write-Warning "⚠️  Ollama podría no estar disponible"
    }
}

function Start-WithDockerCompose {
    Write-Info "🚀 Iniciando servicios con docker-compose..."
    
    if ($Clean) {
        Write-Warning "⚠️  Limpiando containers y volúmenes..."
        wsl docker-compose down -v
        Write-Info "Esperando 3 segundos antes de iniciar..."
        Start-Sleep -Seconds 3
    }
    
    Write-Info "Iniciando docker-compose..."
    wsl docker-compose up -d
    
    Write-Info "Esperando a que los servicios se inicien..."
    Start-Sleep -Seconds 5
    
    Write-Info "Verificando estado de servicios..."
    wsl docker ps --format "table {{.Names}}\t{{.Status}}"
    
    Write-Success "✅ Servicios iniciados con docker-compose"
    
    # Now start backend in WSL
    Start-BackendInWSL
}

function Start-BackendInWSL {
    Write-Info ""
    Write-Info "🎯 Iniciando FastAPI Backend en WSL..."
    Write-Info ""
    
    $command = @"
cd /mnt/e/1/OPOS_GEMINI_1/backend
source venv/bin/activate
echo "🔍 Verificando dependencias..."
pip install -q -r requirements.txt 2>&1 | grep -v "already satisfied"
echo "✅ Dependencias OK"
echo ""
echo "🚀 Iniciando uvicorn..."
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
"@

    Write-Info "Ejecutando backend..."
    Write-Info "Backend accesible en: http://localhost:8000"
    Write-Info "Docs en: http://localhost:8000/docs"
    Write-Info ""
    Write-Info "Presiona Ctrl+C para detener"
    Write-Info ""
    
    wsl bash -c $command
}

function Test-Services {
    Write-Info ""
    Write-Info "🔍 Verificando servicios..."
    Write-Info ""
    
    # Check Qdrant
    Write-Info "Verificando Qdrant en localhost:6333..."
    $qdrantStatus = wsl curl -s http://localhost:6333/health 2>&1
    if ($qdrantStatus -like "*version*") {
        Write-Success "✅ Qdrant OK"
    } else {
        Write-Warning "⚠️  Qdrant podría no estar listo"
    }
    
    # Check PostgreSQL
    Write-Info "Verificando PostgreSQL en localhost:5432..."
    $psqlCheck = wsl docker ps --filter "name=opositaia-postgres" --format "{{.Status}}" 2>&1
    if ($psqlCheck -like "*Up*") {
        Write-Success "✅ PostgreSQL corriendo"
    } else {
        Write-Warning "⚠️  PostgreSQL no está listo"
    }
    
    # Check Ollama
    Write-Info "Verificando Ollama en localhost:11434..."
    $ollamaCheck = wsl curl -s http://localhost:11434/api/tags 2>&1
    if ($ollamaCheck -like "*model*") {
        Write-Success "✅ Ollama OK"
    } else {
        Write-Warning "⚠️  Ollama no está disponible"
    }
    
    Write-Info ""
}

# Main execution
if ($Help) {
    Show-Help
    exit 0
}

try {
    Write-Info ""
    Write-Info "╔════════════════════════════════════════╗"
    Write-Info "║   OpositaIA Backend Startup Script     ║"
    Write-Info "║   Windows PowerShell + WSL Edition     ║"
    Write-Info "╔════════════════════════════════════════╗"
    Write-Info ""
    
    Test-Prerequisites
    
    if ($Compose) {
        Start-WithDockerCompose
    } else {
        Write-Info ""
        Write-Info "📌 Modo local (sin docker-compose)"
        Write-Info "Asegúrate de que PostgreSQL y Qdrant estén corriendo:"
        Write-Info "  - PostgreSQL: localhost:5432"
        Write-Info "  - Qdrant: localhost:6333"
        Write-Info "  - Ollama: localhost:11434"
        Write-Info ""
        
        Test-Services
        Start-BackendInWSL
    }
}
catch {
    Write-Error-Custom "❌ Error: $_"
    exit 1
}
