# Script de DIAGNÓSTICO para verificar configuración
# Ejecutar con: .\Scripts\check_config.ps1

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Verificando configuración TodoLaptop" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "[1/5] Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "[OK] $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[!] ERROR: Python no encontrado" -ForegroundColor Red
}
Write-Host ""

Write-Host "[2/5] Verificando entorno virtual..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "[OK] Entorno virtual encontrado" -ForegroundColor Green
} else {
    Write-Host "[!] Advertencia: No se encontró entorno virtual" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "[3/5] Verificando Django..." -ForegroundColor Yellow
try {
    if (Test-Path "venv\Scripts\Activate.ps1") {
        & venv\Scripts\Activate.ps1
    }
    $djangoVersion = python -c "import django; print(django.get_version())"
    Write-Host "[OK] Django version: $djangoVersion" -ForegroundColor Green
} catch {
    Write-Host "[!] ERROR: Django no está instalado" -ForegroundColor Red
    Write-Host "    Instala con: pip install -r requirements.txt" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "[4/5] Verificando cloudflared..." -ForegroundColor Yellow
$cloudflaredExists = Get-Command cloudflared -ErrorAction SilentlyContinue
if ($cloudflaredExists) {
    $cloudflaredVersion = cloudflared --version
    Write-Host "[OK] Cloudflared instalado" -ForegroundColor Green
} else {
    Write-Host "[!] ERROR: cloudflared no está instalado" -ForegroundColor Red
    Write-Host "    Instala con: winget install --id Cloudflare.cloudflared" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "[5/5] Verificando base de datos..." -ForegroundColor Yellow
if (Test-Path "db.sqlite3") {
    Write-Host "[OK] Base de datos encontrada" -ForegroundColor Green
} else {
    Write-Host "[!] Advertencia: No se encontró db.sqlite3" -ForegroundColor Yellow
    Write-Host "    Ejecuta: python manage.py migrate" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Verificación completada" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
