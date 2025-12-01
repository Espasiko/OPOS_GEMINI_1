# Script para arrancar el backend en Windows
Write-Host "Arrancando backend en puerto 8000..." -ForegroundColor Green

# Matar procesos previos
wsl bash -c "pkill -9 -f 'uvicorn main:app'" 2>$null

# Esperar un momento
Start-Sleep -Seconds 2

# Arrancar el backend en background
$job = Start-Job -ScriptBlock {
    wsl bash -c "cd /mnt/e/1/OPOS_GEMINI_1 && bash start-backend.sh"
}

Write-Host "Backend iniciado (Job ID: $($job.Id))" -ForegroundColor Green
Write-Host "Esperando que el servidor este listo..." -ForegroundColor Yellow

# Esperar a que el servidor este listo
$maxAttempts = 15
$attempt = 0
$ready = $false

while ($attempt -lt $maxAttempts -and -not $ready) {
    Start-Sleep -Seconds 2
    $attempt++
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 2 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $ready = $true
            Write-Host "Backend listo en http://localhost:8000" -ForegroundColor Green
        }
    } catch {
        Write-Host "." -NoNewline
    }
}

if (-not $ready) {
    Write-Host ""
    Write-Host "El backend no respondio despues de $maxAttempts intentos" -ForegroundColor Red
    Write-Host "Verifica los logs con: wsl bash -c 'ps aux | grep uvicorn'" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "Puedes verificar el estado en: http://localhost:8000/docs" -ForegroundColor Cyan
}
