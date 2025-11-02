# =========================================
# Script para Exportar Datos - TodoLap
# =========================================
# Autor: TodoLap Team
# Descripción: Exporta todos los datos actuales de la base de datos a archivos JSON
# Uso: .\Scripts\Export_Data.ps1

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   Exportar Datos de TodoLap" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Obtener ruta del proyecto
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

# Crear carpeta de fixtures si no existe
$FixturesDir = Join-Path $ProjectRoot "fixtures"
if (-not (Test-Path $FixturesDir)) {
    New-Item -ItemType Directory -Path $FixturesDir | Out-Null
    Write-Host "[INFO] Carpeta 'fixtures' creada" -ForegroundColor Cyan
}

Write-Host "[INFO] Los datos se exportarán a: $FixturesDir" -ForegroundColor Yellow
Write-Host ""

# Activar entorno virtual si existe
if (Test-Path "venv\Scripts\Activate.ps1") {
    & venv\Scripts\Activate.ps1
}

# Exportar datos por app
Write-Host "[1/4] Exportando datos de usuarios..." -ForegroundColor Yellow
python manage.py dumpdata usuarios --indent 2 --output "fixtures/usuarios_data.json"
if ($LASTEXITCODE -eq 0) {
    # Convertir a UTF-8 sin BOM
    $content = [System.IO.File]::ReadAllText("fixtures/usuarios_data.json", [System.Text.Encoding]::UTF8)
    $utf8NoBom = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText("fixtures/usuarios_data.json", $content, $utf8NoBom)
    Write-Host "      [OK] Datos de usuarios exportados" -ForegroundColor Green
}

Write-Host ""
Write-Host "[2/4] Exportando datos de inventario..." -ForegroundColor Yellow
python manage.py dumpdata inventario --indent 2 --output "fixtures/inventario_data.json"
if ($LASTEXITCODE -eq 0) {
    # Convertir a UTF-8 sin BOM
    $content = [System.IO.File]::ReadAllText("fixtures/inventario_data.json", [System.Text.Encoding]::UTF8)
    $utf8NoBom = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText("fixtures/inventario_data.json", $content, $utf8NoBom)
    Write-Host "      [OK] Datos de inventario exportados" -ForegroundColor Green
}

Write-Host ""
Write-Host "[3/4] Exportando datos de ventas..." -ForegroundColor Yellow
python manage.py dumpdata ventas --indent 2 --output "fixtures/ventas_data.json"
if ($LASTEXITCODE -eq 0) {
    # Convertir a UTF-8 sin BOM
    $content = [System.IO.File]::ReadAllText("fixtures/ventas_data.json", [System.Text.Encoding]::UTF8)
    $utf8NoBom = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText("fixtures/ventas_data.json", $content, $utf8NoBom)
    Write-Host "      [OK] Datos de ventas exportados" -ForegroundColor Green
}

Write-Host ""
Write-Host "[4/4] Exportando datos de servicios..." -ForegroundColor Yellow
python manage.py dumpdata servicios --indent 2 --output "fixtures/servicios_data.json"
if ($LASTEXITCODE -eq 0) {
    # Convertir a UTF-8 sin BOM
    $content = [System.IO.File]::ReadAllText("fixtures/servicios_data.json", [System.Text.Encoding]::UTF8)
    $utf8NoBom = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText("fixtures/servicios_data.json", $content, $utf8NoBom)
    Write-Host "      [OK] Datos de servicios exportados" -ForegroundColor Green
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "   ✓ Exportación Completada" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Los datos han sido exportados a la carpeta 'fixtures'" -ForegroundColor Green
Write-Host ""
Write-Host "Archivos creados:" -ForegroundColor Cyan
Write-Host "  - fixtures/usuarios_data.json" -ForegroundColor White
Write-Host "  - fixtures/inventario_data.json" -ForegroundColor White
Write-Host "  - fixtures/ventas_data.json" -ForegroundColor White
Write-Host "  - fixtures/servicios_data.json" -ForegroundColor White
Write-Host ""
Write-Host "Estos archivos se pueden cargar con: .\Scripts\Load_Initial_Data.ps1" -ForegroundColor Yellow
Write-Host ""
