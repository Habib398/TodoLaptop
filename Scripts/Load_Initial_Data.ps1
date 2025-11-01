# =========================================# =========================================

# Script para Cargar Datos Iniciales - TodoLap# Script para Cargar Datos Iniciales - TodoLap

# =========================================# =========================================

# Autor: TodoLap Team# Autor: TodoLap Team

# Descripción: Carga datos iniciales desde archivos JSON (fixtures)# Descripción: Carga datos iniciales desde archivos JSON (fixtures)

# Uso: .\Scripts\Load_Initial_Data.ps1# Uso: .\Scripts\Load_Initial_Data.ps1



Write-Host ""Write-Host ""

Write-Host "============================================" -ForegroundColor CyanWrite-Host "============================================" -ForegroundColor Cyan

Write-Host "   Cargar Datos Iniciales de TodoLap" -ForegroundColor CyanWrite-Host "   Cargar Datos Iniciales de TodoLap" -ForegroundColor Cyan

Write-Host "============================================" -ForegroundColor CyanWrite-Host "============================================" -ForegroundColor Cyan

Write-Host ""Write-Host ""



# Obtener ruta del proyecto# Obtener ruta del proyecto

$ProjectRoot = Split-Path -Parent $PSScriptRoot$ProjectRoot = Split-Path -Parent $PSScriptRoot

Set-Location $ProjectRootSet-Location $ProjectRoot



# Verificar carpeta de fixtures# Verificar carpeta de fixtures

$FixturesDir = Join-Path $ProjectRoot "fixtures"$FixturesDir = Join-Path $ProjectRoot "fixtures"

if (-not (Test-Path $FixturesDir)) {if (-not (Test-Path $FixturesDir)) {

    Write-Host "[ERROR] No se encontró la carpeta 'fixtures'" -ForegroundColor Red    Write-Host "[ERROR] No se encontró la carpeta 'fixtures'" -ForegroundColor Red

    Write-Host ""    Write-Host ""

    Write-Host "Para exportar datos actuales primero ejecuta:" -ForegroundColor Yellow    Write-Host "Para exportar datos actuales primero ejecuta:" -ForegroundColor Yellow

    Write-Host "  .\Scripts\Export_Data.ps1" -ForegroundColor White    Write-Host "  .\Scripts\Export_Data.ps1" -ForegroundColor White

    Write-Host ""    Write-Host ""

    exit 1    exit 1

}}



Write-Host "[INFO] Buscando archivos de datos en: $FixturesDir" -ForegroundColor YellowWrite-Host "[INFO] Buscando archivos de datos en: $FixturesDir" -ForegroundColor Yellow

Write-Host ""Write-Host ""



# Activar entorno virtual si existe# Activar entorno virtual si existe

if (Test-Path "venv\Scripts\Activate.ps1") {if (Test-Path "venv\Scripts\Activate.ps1") {

    & venv\Scripts\Activate.ps1    & venv\Scripts\Activate.ps1

}}



# Archivos a cargar (en orden de dependencias)# Archivos a cargar (en orden de dependencias)

$DataFiles = @($DataFiles = @(

    @{Name="usuarios"; File="usuarios_data.json"},    @{Name="usuarios"; File="usuarios_data.json"},

    @{Name="inventario"; File="inventario_data.json"},    @{Name="inventario"; File="inventario_data.json"},

    @{Name="servicios"; File="servicios_data.json"},    @{Name="servicios"; File="servicios_data.json"},

    @{Name="ventas"; File="ventas_data.json"}    @{Name="ventas"; File="ventas_data.json"}

))



$LoadedCount = 0$LoadedCount = 0

$SkippedCount = 0$SkippedCount = 0



foreach ($Data in $DataFiles) {foreach ($Data in $DataFiles) {

    $FilePath = Join-Path $FixturesDir $Data.File    $FilePath = Join-Path $FixturesDir $Data.File

        

    Write-Host "[$($LoadedCount + $SkippedCount + 1)/$($DataFiles.Count)] Cargando datos de $($Data.Name)..." -ForegroundColor Yellow    Write-Host "[$($LoadedCount + $SkippedCount + 1)/$($DataFiles.Count)] Cargando datos de $($Data.Name)..." -ForegroundColor Yellow

        

    if (Test-Path $FilePath) {    if (Test-Path $FilePath) {

        python manage.py loaddata $FilePath        python manage.py loaddata $FilePath

                

        if ($LASTEXITCODE -eq 0) {        if ($LASTEXITCODE -eq 0) {

            Write-Host "      [OK] Datos de $($Data.Name) cargados exitosamente" -ForegroundColor Green            Write-Host "      [OK] Datos de $($Data.Name) cargados exitosamente" -ForegroundColor Green

            $LoadedCount++            $LoadedCount++

        } else {        } else {

            Write-Host "      [!] Error al cargar datos de $($Data.Name)" -ForegroundColor Red            Write-Host "      [!] Error al cargar datos de $($Data.Name)" -ForegroundColor Red

        }        }

    } else {    } else {

        Write-Host "      [!] Archivo no encontrado: $($Data.File)" -ForegroundColor Yellow        Write-Host "      [!] Archivo no encontrado: $($Data.File)" -ForegroundColor Yellow

        $SkippedCount++        $SkippedCount++

    }    }

    Write-Host ""    Write-Host ""

}}



# Resumen# Resumen

Write-Host "============================================" -ForegroundColor GreenWrite-Host "============================================" -ForegroundColor Green

Write-Host "   Proceso Completado" -ForegroundColor GreenWrite-Host "   Proceso Completado" -ForegroundColor Green

Write-Host "============================================" -ForegroundColor GreenWrite-Host "============================================" -ForegroundColor Green

Write-Host ""Write-Host ""

Write-Host "Archivos cargados: $LoadedCount de $($DataFiles.Count)" -ForegroundColor CyanWrite-Host "Archivos cargados: $LoadedCount de $($DataFiles.Count)" -ForegroundColor Cyan

if ($SkippedCount -gt 0) {if ($SkippedCount -gt 0) {

    Write-Host "Archivos omitidos: $SkippedCount" -ForegroundColor Yellow    Write-Host "Archivos omitidos: $SkippedCount" -ForegroundColor Yellow

}}

Write-Host ""Write-Host ""



if ($LoadedCount -gt 0) {if ($LoadedCount -gt 0) {

    Write-Host "Los datos han sido importados a la base de datos." -ForegroundColor Green    Write-Host "Los datos han sido importados a la base de datos." -ForegroundColor Green

    Write-Host ""    Write-Host ""

    Write-Host "Ya puedes iniciar el servidor:" -ForegroundColor Cyan    Write-Host "Ya puedes iniciar el servidor:" -ForegroundColor Cyan

    Write-Host "  .\Scripts\Start_TodoLap.ps1" -ForegroundColor White    Write-Host "  .\Scripts\Start_TodoLap.ps1" -ForegroundColor White

} else {} else {

    Write-Host "No se cargaron datos. Verifica que existan archivos en 'fixtures/'" -ForegroundColor Yellow    Write-Host "No se cargaron datos. Verifica que existan archivos en 'fixtures/'" -ForegroundColor Yellow

}}

Write-Host ""Write-Host ""

