# =========================================
# Script para iniciar el servidor TodoLap
# =========================================
# Autor: TodoLap Team
# Descripción: Inicia el servidor Django de TodoLap en el puerto 8000
# Uso: .\Scripts\Start_TodoLap.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Iniciando TodoLap Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Obtener ruta del proyecto
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "[1/4] Ubicación del proyecto: $ProjectRoot" -ForegroundColor Yellow
Write-Host ""

# Verificar si existe un entorno virtual
Write-Host "[2/4] Verificando entorno virtual..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "      [OK] Entorno virtual encontrado" -ForegroundColor Green
    & venv\Scripts\Activate.ps1
} else {
    Write-Host "      [!] No se encontró entorno virtual (venv)" -ForegroundColor Yellow
    Write-Host "      Usando Python del sistema..." -ForegroundColor Yellow
}
Write-Host ""

# Verificar si manage.py existe
Write-Host "[3/4] Verificando archivos del proyecto..." -ForegroundColor Yellow
if (-not (Test-Path "manage.py")) {
    Write-Host "      [ERROR] No se encontró manage.py" -ForegroundColor Red
    Write-Host "      Asegúrate de ejecutar el script desde la raíz del proyecto" -ForegroundColor Red
    exit 1
}
Write-Host "      [OK] Archivos del proyecto encontrados" -ForegroundColor Green
Write-Host ""

# Iniciar el servidor Django
Write-Host "[4/4] Iniciando servidor Django..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   Servidor TodoLap en ejecución" -ForegroundColor Green
Write-Host "   URL Local: http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "   URL Red: http://0.0.0.0:8000" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

# Ejecutar servidor Django
python manage.py runserver 0.0.0.0:8000
