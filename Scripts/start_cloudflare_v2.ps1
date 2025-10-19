# Script ALTERNATIVO para iniciar Django con túnel de Cloudflare
# Este script abre dos ventanas separadas para mejor estabilidad
# Ejecutar con: .\Scripts\start_cloudflare_v2.ps1

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Iniciando TodoLaptop con Cloudflare" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Ruta base del proyecto
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$DjangoPort = 8000

Write-Host "[1/3] Preparando entorno..." -ForegroundColor Yellow
Set-Location $ProjectRoot

# Verificar cloudflared
$cloudflaredExists = Get-Command cloudflared -ErrorAction SilentlyContinue
if (-not $cloudflaredExists) {
    Write-Host "[!] ERROR: cloudflared no está instalado." -ForegroundColor Red
    Write-Host "Instálalo con: winget install --id Cloudflare.cloudflared" -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] Cloudflared encontrado" -ForegroundColor Green
Write-Host ""

Write-Host "[2/3] Iniciando servidor Django en ventana separada..." -ForegroundColor Yellow

# Preparar comando de Django
$ActivateVenv = ""
if (Test-Path "venv\Scripts\Activate.ps1") {
    $ActivateVenv = "& venv\Scripts\Activate.ps1; "
}

$DjangoCommand = "${ActivateVenv}python manage.py runserver 0.0.0.0:${DjangoPort}"

# Iniciar Django en nueva ventana
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ProjectRoot'; Write-Host 'Servidor Django iniciado en puerto $DjangoPort' -ForegroundColor Green; $DjangoCommand"

Write-Host "[OK] Django iniciándose en nueva ventana..." -ForegroundColor Green
Write-Host ""

# Esperar a que Django inicie
Write-Host "Esperando 6 segundos para que Django inicie completamente..." -ForegroundColor Cyan
Start-Sleep -Seconds 6

Write-Host "[3/3] Iniciando túnel de Cloudflare..." -ForegroundColor Yellow
Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "INSTRUCCIONES:" -ForegroundColor Yellow
Write-Host "1. Copia la URL HTTPS que aparecerá abajo" -ForegroundColor Cyan
Write-Host "2. Ábrela en tu navegador" -ForegroundColor Cyan
Write-Host "3. Ambas ventanas deben permanecer abiertas" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para detener:" -ForegroundColor Yellow
Write-Host "- Presiona Ctrl+C aquí para detener Cloudflare" -ForegroundColor Cyan
Write-Host "- Cierra la otra ventana para detener Django" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

# Iniciar cloudflared
cloudflared tunnel --url http://localhost:$DjangoPort --no-autoupdate

Write-Host ""
Write-Host "Túnel de Cloudflare detenido." -ForegroundColor Yellow
Write-Host "Recuerda cerrar la ventana de Django también." -ForegroundColor Yellow
