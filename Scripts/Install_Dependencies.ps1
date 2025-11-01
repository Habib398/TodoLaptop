# =========================================
# Script para instalar dependencias de TodoLap
# =========================================
# Autor: TodoLap Team
# Descripcion: Instala todas las dependencias necesarias para el proyecto TodoLap
# Uso: .\Scripts\Install_Dependencies.ps1

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   Instalador de Dependencias TodoLap" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Obtener ruta del proyecto
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "[1/6] Ubicacion del proyecto: $ProjectRoot" -ForegroundColor Yellow
Write-Host ""

# Verificar que existe requirements.txt
Write-Host "[2/6] Verificando archivo requirements.txt..." -ForegroundColor Yellow
if (-not (Test-Path "requirements.txt")) {
    Write-Host "      [ERROR] No se encontro el archivo requirements.txt" -ForegroundColor Red
    Write-Host "      Por favor, asegurate de que existe en la raiz del proyecto" -ForegroundColor Red
    exit 1
}
Write-Host "      [OK] Archivo requirements.txt encontrado" -ForegroundColor Green
Write-Host ""

# Verificar Python
Write-Host "[3/6] Verificando instalacion de Python..." -ForegroundColor Yellow
$PythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "      [ERROR] Python no esta instalado o no esta en el PATH" -ForegroundColor Red
    Write-Host "      Instala Python desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}
Write-Host "      [OK] Python encontrado: $PythonVersion" -ForegroundColor Green
Write-Host ""

# Verificar/Crear entorno virtual
Write-Host "[4/6] Configurando entorno virtual..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "      [OK] Entorno virtual existente encontrado" -ForegroundColor Green
    Write-Host "      Activando entorno virtual..." -ForegroundColor Cyan
    & venv\Scripts\Activate.ps1
} else {
    Write-Host "      [!] No se encontro entorno virtual" -ForegroundColor Yellow
    Write-Host "      Creando nuevo entorno virtual..." -ForegroundColor Cyan
    python -m venv venv
    
    if (-not (Test-Path "venv")) {
        Write-Host "      [ERROR] No se pudo crear el entorno virtual" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "      [OK] Entorno virtual creado exitosamente" -ForegroundColor Green
    Write-Host "      Activando entorno virtual..." -ForegroundColor Cyan
    & venv\Scripts\Activate.ps1
}
Write-Host ""

# Actualizar pip
Write-Host "[5/6] Actualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "      [OK] pip actualizado correctamente" -ForegroundColor Green
} else {
    Write-Host "      [!] Advertencia: No se pudo actualizar pip" -ForegroundColor Yellow
}
Write-Host ""

# Instalar dependencias
Write-Host "[6/6] Instalando dependencias desde requirements.txt..." -ForegroundColor Yellow
Write-Host ""
Write-Host "      Esto puede tomar algunos minutos..." -ForegroundColor Cyan
Write-Host "      ----------------------------------------" -ForegroundColor Gray

pip install -r requirements.txt

Write-Host ""
if ($LASTEXITCODE -eq 0) {
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "   Instalacion Completada con Exito" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Todas las dependencias han sido instaladas correctamente." -ForegroundColor Green
    Write-Host ""
    Write-Host "Proximos pasos:" -ForegroundColor Cyan
    Write-Host "  1. Configura tu base de datos en TodoLap\settings.py" -ForegroundColor White
    Write-Host "  2. Ejecuta las migraciones: python manage.py migrate" -ForegroundColor White
    Write-Host "  3. Inicia el servidor: .\Scripts\Start_TodoLap.ps1" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "============================================" -ForegroundColor Red
    Write-Host "   Error en la Instalacion" -ForegroundColor Red
    Write-Host "============================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Ocurrio un error durante la instalacion de dependencias." -ForegroundColor Red
    Write-Host "Por favor, revisa los mensajes de error anteriores." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Soluciones comunes:" -ForegroundColor Cyan
    Write-Host "  1. Verifica tu conexion a internet" -ForegroundColor White
    Write-Host "  2. Asegurate de tener permisos de administrador" -ForegroundColor White
    Write-Host "  3. Actualiza pip: python -m pip install --upgrade pip" -ForegroundColor White
    Write-Host ""
    exit 1
}
