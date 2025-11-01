# =========================================
# Script de Configuración Inicial - TodoLap
# =========================================
# Autor: TodoLap Team
# Descripción: Configura la base de datos y aplica todas las migraciones
# Uso: .\Scripts\Setup_Database.ps1

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   Configuración de Base de Datos TodoLap" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Obtener ruta del proyecto
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "[INFO] Ubicación del proyecto: $ProjectRoot" -ForegroundColor Yellow
Write-Host ""

# Verificar entorno virtual
Write-Host "[1/5] Verificando entorno virtual..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "      [OK] Activando entorno virtual" -ForegroundColor Green
    & venv\Scripts\Activate.ps1
} else {
    Write-Host "      [!] No se encontró entorno virtual" -ForegroundColor Yellow
    Write-Host "      Usando Python del sistema..." -ForegroundColor Yellow
}
Write-Host ""

# Verificar dependencias instaladas
Write-Host "[2/5] Verificando dependencias..." -ForegroundColor Yellow
$DjangoInstalled = python -c "import django; print(django.VERSION)" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "      [ERROR] Django no está instalado" -ForegroundColor Red
    Write-Host "      Por favor ejecuta: .\Scripts\Install_Dependencies.ps1" -ForegroundColor Yellow
    exit 1
}
Write-Host "      [OK] Django instalado correctamente" -ForegroundColor Green
Write-Host ""

# Verificar archivos de migraciones
Write-Host "[3/5] Verificando archivos de migraciones..." -ForegroundColor Yellow
$MigrationsExist = $true
$Apps = @("usuarios", "inventario", "ventas", "servicios")

foreach ($App in $Apps) {
    $MigrationPath = Join-Path $ProjectRoot "$App\migrations\0001_initial.py"
    if (Test-Path $MigrationPath) {
        Write-Host "      [OK] Migraciones encontradas para: $App" -ForegroundColor Green
    } else {
        Write-Host "      [!] No se encontraron migraciones para: $App" -ForegroundColor Yellow
        $MigrationsExist = $false
    }
}
Write-Host ""

# Aplicar migraciones
Write-Host "[4/5] Aplicando migraciones a la base de datos..." -ForegroundColor Yellow
Write-Host "      Esto creará todas las tablas necesarias..." -ForegroundColor Cyan
Write-Host ""

python manage.py migrate

Write-Host ""
if ($LASTEXITCODE -eq 0) {
    Write-Host "      [OK] Migraciones aplicadas exitosamente" -ForegroundColor Green
} else {
    Write-Host "      [ERROR] Hubo un problema al aplicar las migraciones" -ForegroundColor Red
    Write-Host ""
    Write-Host "Posibles causas:" -ForegroundColor Yellow
    Write-Host "  - La base de datos no está corriendo (PostgreSQL)" -ForegroundColor White
    Write-Host "  - Las credenciales en settings.py son incorrectas" -ForegroundColor White
    Write-Host "  - La base de datos 'TodoLaptop' no existe" -ForegroundColor White
    Write-Host ""
    exit 1
}
Write-Host ""

# Crear superusuario (opcional)
Write-Host "[5/5] Configuración de usuario administrador..." -ForegroundColor Yellow
Write-Host ""
$CreateSuperuser = Read-Host "¿Deseas crear un usuario administrador ahora? (S/N)"

if ($CreateSuperuser -eq "S" -or $CreateSuperuser -eq "s") {
    Write-Host ""
    Write-Host "      Creando usuario administrador..." -ForegroundColor Cyan
    Write-Host "      Sigue las instrucciones a continuación:" -ForegroundColor Cyan
    Write-Host ""
    python manage.py createsuperuser
    Write-Host ""
} else {
    Write-Host "      [OK] Puedes crear un administrador más tarde con:" -ForegroundColor Yellow
    Write-Host "      python manage.py createsuperuser" -ForegroundColor White
    Write-Host ""
}

# Resumen final
Write-Host "============================================" -ForegroundColor Green
Write-Host "   ✓ Configuración Completada" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "La base de datos ha sido configurada correctamente." -ForegroundColor Green
Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Cyan
Write-Host "  1. Para cargar datos iniciales: .\Scripts\Load_Initial_Data.ps1" -ForegroundColor White
Write-Host "  2. Para iniciar el servidor: .\Scripts\Start_TodoLap.ps1" -ForegroundColor White
Write-Host "  3. Accede al admin en: http://127.0.0.1:8000/admin" -ForegroundColor White
Write-Host ""
