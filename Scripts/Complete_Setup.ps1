# =========================================
# Script de Configuración Completa - TodoLap
# =========================================
# Autor: TodoLap Team
# Descripción: Instalación y configuración completa del proyecto TodoLap
# Uso: .\Scripts\Complete_Setup.ps1

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   Configuración Completa de TodoLap" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Este script realizará:" -ForegroundColor Yellow
Write-Host "  1. Instalación de dependencias" -ForegroundColor White
Write-Host "  2. Configuración de la base de datos" -ForegroundColor White
Write-Host "  3. Carga de datos iniciales (opcional)" -ForegroundColor White
Write-Host ""

$Continue = Read-Host "¿Deseas continuar? (S/N)"
if ($Continue -ne "S" -and $Continue -ne "s") {
    Write-Host "Configuración cancelada." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   PASO 1: Instalación de Dependencias" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Ejecutar instalación de dependencias
& "$PSScriptRoot\Install_Dependencies.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Falló la instalación de dependencias" -ForegroundColor Red
    Write-Host "Por favor, revisa los errores anteriores." -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Presiona Enter para continuar con la configuración de la base de datos..."
Read-Host

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   PASO 2: Configuración de Base de Datos" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Obtener ruta del proyecto
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

# Activar entorno virtual
if (Test-Path "venv\Scripts\Activate.ps1") {
    & venv\Scripts\Activate.ps1
}

# Aplicar migraciones
python manage.py migrate

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Falló la configuración de la base de datos" -ForegroundColor Red
    Write-Host ""
    Write-Host "Verifica:" -ForegroundColor Yellow
    Write-Host "  1. PostgreSQL está corriendo" -ForegroundColor White
    Write-Host "  2. La base de datos 'TodoLaptop' existe" -ForegroundColor White
    Write-Host "  3. Las credenciales en settings.py son correctas" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "[OK] Base de datos configurada correctamente" -ForegroundColor Green
Write-Host ""

# Preguntar por datos iniciales
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   PASO 3: Datos Iniciales (Opcional)" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$FixturesDir = Join-Path $ProjectRoot "fixtures"
if (Test-Path $FixturesDir) {
    $LoadData = Read-Host "¿Deseas cargar datos iniciales desde 'fixtures'? (S/N)"
    if ($LoadData -eq "S" -or $LoadData -eq "s") {
        Write-Host ""
        & "$PSScriptRoot\Load_Initial_Data.ps1"
    }
} else {
    Write-Host "[INFO] No se encontró carpeta 'fixtures' con datos iniciales" -ForegroundColor Yellow
    Write-Host "       Puedes agregar datos manualmente o exportarlos después" -ForegroundColor Yellow
}

Write-Host ""

# Crear superusuario
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   Usuario Administrador" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$CreateAdmin = Read-Host "¿Deseas crear un usuario administrador? (S/N)"
if ($CreateAdmin -eq "S" -or $CreateAdmin -eq "s") {
    Write-Host ""
    Write-Host "Sigue las instrucciones para crear el administrador:" -ForegroundColor Cyan
    Write-Host ""
    python manage.py createsuperuser
}

# Resumen final
Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "   ✓ Configuración Completa Finalizada" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "TodoLap está listo para usar!" -ForegroundColor Green
Write-Host ""
Write-Host "Comandos útiles:" -ForegroundColor Cyan
Write-Host "  Iniciar servidor:  .\Scripts\Start_TodoLap.ps1" -ForegroundColor White
Write-Host "  Detener servidor:  .\Scripts\Stop_TodoLap.ps1" -ForegroundColor White
Write-Host "  Exportar datos:    .\Scripts\Export_Data.ps1" -ForegroundColor White
Write-Host "  Cargar datos:      .\Scripts\Load_Initial_Data.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Accede a tu aplicación en: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "Panel de administración:   http://127.0.0.1:8000/admin" -ForegroundColor Cyan
Write-Host ""
