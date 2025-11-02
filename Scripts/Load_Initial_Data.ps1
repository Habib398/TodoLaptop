# =========================================
# Script para Cargar Datos Iniciales - TodoLap
# =========================================
# Autor: TodoLap Team
# Descripción: Carga datos iniciales desde archivos JSON (fixtures)
# Uso: .\Scripts\Load_Initial_Data.ps1

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   Cargar Datos Iniciales de TodoLap" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Obtener ruta del proyecto
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

# Verificar carpeta de fixtures
$FixturesDir = Join-Path $ProjectRoot "fixtures"
if (-not (Test-Path $FixturesDir)) {
    Write-Host "[ERROR] No se encontró la carpeta 'fixtures'" -ForegroundColor Red
    Write-Host ""
    Write-Host "Para exportar datos actuales primero ejecuta:" -ForegroundColor Yellow
    Write-Host "  .\Scripts\Export_Data.ps1" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host "[INFO] Buscando archivos de datos en: $FixturesDir" -ForegroundColor Yellow
Write-Host ""

# Activar entorno virtual si existe
if (Test-Path "venv\Scripts\Activate.ps1") {
    & venv\Scripts\Activate.ps1
}

# Archivos a cargar (en orden de dependencias)
$DataFiles = @(
    @{Name="usuarios"; File="usuarios_data.json"},
    @{Name="inventario"; File="inventario_data.json"},
    @{Name="servicios"; File="servicios_data.json"},
    @{Name="ventas"; File="ventas_data.json"}
)

$LoadedCount = 0
$SkippedCount = 0

foreach ($Data in $DataFiles) {
    $FilePath = Join-Path $FixturesDir $Data.File
    
    Write-Host "[$($LoadedCount + $SkippedCount + 1)/$($DataFiles.Count)] Cargando datos de $($Data.Name)..." -ForegroundColor Yellow
    
    if (Test-Path $FilePath) {
        python manage.py loaddata $FilePath
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "      [OK] Datos de $($Data.Name) cargados exitosamente" -ForegroundColor Green
            $LoadedCount++
        } else {
            Write-Host "      [!] Error al cargar datos de $($Data.Name)" -ForegroundColor Red
        }
    } else {
        Write-Host "      [!] Archivo no encontrado: $($Data.File)" -ForegroundColor Yellow
        $SkippedCount++
    }
    Write-Host ""
}

# Resumen
Write-Host "============================================" -ForegroundColor Green
Write-Host "   Proceso Completado" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Archivos cargados: $LoadedCount de $($DataFiles.Count)" -ForegroundColor Cyan
if ($SkippedCount -gt 0) {
    Write-Host "Archivos omitidos: $SkippedCount" -ForegroundColor Yellow
}
Write-Host ""

if ($LoadedCount -gt 0) {
    Write-Host "Los datos han sido importados a la base de datos." -ForegroundColor Green
    Write-Host ""
    Write-Host "Ya puedes iniciar el servidor:" -ForegroundColor Cyan
    Write-Host "  .\Scripts\Start_TodoLap.ps1" -ForegroundColor White
} else {
    Write-Host "No se cargaron datos. Verifica que existan archivos en 'fixtures/'" -ForegroundColor Yellow
}
Write-Host ""