# Script para iniciar Django con túnel de Cloudflare
# Ejecutar con: .\Scripts\start_cloudflare.ps1

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Iniciando TodoLaptop con Cloudflare" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Ruta base del proyecto
$ProjectRoot = Split-Path -Parent $PSScriptRoot

# Cambiar al directorio del proyecto
Set-Location $ProjectRoot

# Verificar si existe el entorno virtual
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "[1/4] Activando entorno virtual..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
} else {
    Write-Host "[!] Advertencia: No se encontró el entorno virtual." -ForegroundColor Red
    Write-Host "    Continuando con el Python del sistema..." -ForegroundColor Red
}

Write-Host ""
Write-Host "[2/4] Verificando cloudflared..." -ForegroundColor Yellow

# Verificar si cloudflared está instalado
$cloudflaredExists = Get-Command cloudflared -ErrorAction SilentlyContinue

if (-not $cloudflaredExists) {
    Write-Host "[!] ERROR: cloudflared no está instalado." -ForegroundColor Red
    Write-Host ""
    Write-Host "Para instalarlo, ejecuta:" -ForegroundColor Yellow
    Write-Host "  winget install --id Cloudflare.cloudflared" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "O descárgalo desde:" -ForegroundColor Yellow
    Write-Host "  https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/" -ForegroundColor Cyan
    exit 1
}

Write-Host "[OK] cloudflared encontrado" -ForegroundColor Green
Write-Host ""

# Puerto para Django
$DjangoPort = 8000

Write-Host "[3/4] Iniciando servidor Django en puerto $DjangoPort..." -ForegroundColor Yellow
Write-Host ""

# Iniciar Django en segundo plano
$DjangoJob = Start-Job -ScriptBlock {
    param($ProjectPath, $Port)
    Set-Location $ProjectPath
    if (Test-Path "venv\Scripts\Activate.ps1") {
        & "venv\Scripts\Activate.ps1"
    }
    # Usar 0.0.0.0 para que Django escuche en todas las interfaces
    python manage.py runserver 0.0.0.0:$Port
} -ArgumentList $ProjectRoot, $DjangoPort

# Esperar a que Django inicie completamente
Write-Host "Esperando a que Django inicie..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

# Verificar que Django esté corriendo
try {
    $response = Invoke-WebRequest -Uri "http://localhost:$DjangoPort" -UseBasicParsing -TimeoutSec 5 -ErrorAction SilentlyContinue
    Write-Host "[OK] Django está corriendo correctamente" -ForegroundColor Green
} catch {
    Write-Host "[!] Advertencia: No se pudo verificar Django, pero continuaremos..." -ForegroundColor Yellow
}

Write-Host ""

Write-Host "[4/4] Iniciando túnel de Cloudflare..." -ForegroundColor Yellow
Write-Host ""
Write-Host ""
Write-Host "Presiona Ctrl+C para detener ambos servicios" -ForegroundColor Yellow
Write-Host ""

# Iniciar cloudflared (esto bloqueará hasta que se presione Ctrl+C)
try {
    # Añadir más opciones para estabilidad
    cloudflared tunnel --url http://localhost:$DjangoPort --no-autoupdate
} catch {
    Write-Host ""
    Write-Host "[!] Error al iniciar cloudflared: $_" -ForegroundColor Red
} finally {
    # Limpiar al salir
    Write-Host ""
    Write-Host "Deteniendo servicios..." -ForegroundColor Yellow
    Stop-Job -Job $DjangoJob -ErrorAction SilentlyContinue
    Remove-Job -Job $DjangoJob -ErrorAction SilentlyContinue
    Write-Host "[OK] Servicios detenidos" -ForegroundColor Green
}ry {
    cloudflared tunnel --url http://localhost:$DjangoPort
} finally {
    # Limpiar al salir
    Write-Host ""
    Write-Host "Deteniendo servicios..." -ForegroundColor Yellow
    Stop-Job -Job $DjangoJob -ErrorAction SilentlyContinue
    Remove-Job -Job $DjangoJob -ErrorAction SilentlyContinue
    Write-Host "[OK] Servicios detenidos" -ForegroundColor Green
}
