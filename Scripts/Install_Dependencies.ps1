# =========================================# =========================================

# Script para instalar dependencias de TodoLap# Script para instalar dependencias de TodoLap

# =========================================# =========================================

# Autor: TodoLap Team# Autor: TodoLap Team

# Descripción: Instala todas las dependencias necesarias para el proyecto TodoLap# Descripción: Instala todas las dependencias necesarias para el proyecto TodoLap

# Uso: .\Scripts\Install_Dependencies.ps1# Uso: .\Scripts\Install_Dependencies.ps1



Write-Host ""Write-Host ""

Write-Host "============================================" -ForegroundColor CyanWrite-Host "============================================" -ForegroundColor Cyan

Write-Host "   Instalador de Dependencias TodoLap" -ForegroundColor CyanWrite-Host "   Instalador de Dependencias TodoLap" -ForegroundColor Cyan

Write-Host "============================================" -ForegroundColor CyanWrite-Host "============================================" -ForegroundColor Cyan

Write-Host ""Write-Host ""



# Obtener ruta del proyecto# Obtener ruta del proyecto

$ProjectRoot = Split-Path -Parent $PSScriptRoot$ProjectRoot = Split-Path -Parent $PSScriptRoot

Set-Location $ProjectRootSet-Location $ProjectRoot



Write-Host "[1/6] Ubicación del proyecto: $ProjectRoot" -ForegroundColor YellowWrite-Host "[1/6] Ubicación del proyecto: $ProjectRoot" -ForegroundColor Yellow

Write-Host ""Write-Host ""



# Verificar que existe requirements.txt# Verificar que existe requirements.txt

Write-Host "[2/6] Verificando archivo requirements.txt..." -ForegroundColor YellowWrite-Host "[2/6] Verificando archivo requirements.txt..." -ForegroundColor Yellow

if (-not (Test-Path "requirements.txt")) {if (-not (Test-Path "requirements.txt")) {

    Write-Host "      [ERROR] No se encontró el archivo requirements.txt" -ForegroundColor Red    Write-Host "      [ERROR] No se encontró el archivo requirements.txt" -ForegroundColor Red

    Write-Host "      Por favor, asegúrate de que existe en la raíz del proyecto" -ForegroundColor Red    Write-Host "      Por favor, asegúrate de que existe en la raíz del proyecto" -ForegroundColor Red

    exit 1    exit 1

}}

Write-Host "      [OK] Archivo requirements.txt encontrado" -ForegroundColor GreenWrite-Host "      [OK] Archivo requirements.txt encontrado" -ForegroundColor Green

Write-Host ""Write-Host ""



# Verificar Python# Verificar Python

Write-Host "[3/6] Verificando instalación de Python..." -ForegroundColor YellowWrite-Host "[3/6] Verificando instalación de Python..." -ForegroundColor Yellow

$PythonVersion = python --version 2>&1$PythonVersion = python --version 2>&1

if ($LASTEXITCODE -ne 0) {if ($LASTEXITCODE -ne 0) {

    Write-Host "      [ERROR] Python no está instalado o no está en el PATH" -ForegroundColor Red    Write-Host "      [ERROR] Python no está instalado o no está en el PATH" -ForegroundColor Red

    Write-Host "      Instala Python desde: https://www.python.org/downloads/" -ForegroundColor Yellow    Write-Host "      Instala Python desde: https://www.python.org/downloads/" -ForegroundColor Yellow

    exit 1    exit 1

}}

Write-Host "      [OK] Python encontrado: $PythonVersion" -ForegroundColor GreenWrite-Host "      [OK] Python encontrado: $PythonVersion" -ForegroundColor Green

Write-Host ""Write-Host ""



# Verificar/Crear entorno virtual# Verificar/Crear entorno virtual

Write-Host "[4/6] Configurando entorno virtual..." -ForegroundColor YellowWrite-Host "[4/6] Configurando entorno virtual..." -ForegroundColor Yellow

if (Test-Path "venv") {if (Test-Path "venv") {

    Write-Host "      [OK] Entorno virtual existente encontrado" -ForegroundColor Green    Write-Host "      [OK] Entorno virtual existente encontrado" -ForegroundColor Green

    Write-Host "      Activando entorno virtual..." -ForegroundColor Cyan    Write-Host "      Activando entorno virtual..." -ForegroundColor Cyan

    & venv\Scripts\Activate.ps1    & venv\Scripts\Activate.ps1

} else {} else {

    Write-Host "      [!] No se encontró entorno virtual" -ForegroundColor Yellow    Write-Host "      [!] No se encontró entorno virtual" -ForegroundColor Yellow

    Write-Host "      Creando nuevo entorno virtual..." -ForegroundColor Cyan    Write-Host "      Creando nuevo entorno virtual..." -ForegroundColor Cyan

    python -m venv venv    python -m venv venv

        

    if (-not (Test-Path "venv")) {    if (-not (Test-Path "venv")) {

        Write-Host "      [ERROR] No se pudo crear el entorno virtual" -ForegroundColor Red        Write-Host "      [ERROR] No se pudo crear el entorno virtual" -ForegroundColor Red

        exit 1        exit 1

    }    }

        

    Write-Host "      [OK] Entorno virtual creado exitosamente" -ForegroundColor Green    Write-Host "      [OK] Entorno virtual creado exitosamente" -ForegroundColor Green

    Write-Host "      Activando entorno virtual..." -ForegroundColor Cyan    Write-Host "      Activando entorno virtual..." -ForegroundColor Cyan

    & venv\Scripts\Activate.ps1    & venv\Scripts\Activate.ps1

}}

Write-Host ""Write-Host ""



# Actualizar pip# Actualizar pip

Write-Host "[5/6] Actualizando pip..." -ForegroundColor YellowWrite-Host "[5/6] Actualizando pip..." -ForegroundColor Yellow

python -m pip install --upgrade pip --quietpython -m pip install --upgrade pip --quiet

if ($LASTEXITCODE -eq 0) {if ($LASTEXITCODE -eq 0) {

    Write-Host "      [OK] pip actualizado correctamente" -ForegroundColor Green    Write-Host "      [OK] pip actualizado correctamente" -ForegroundColor Green

} else {} else {

    Write-Host "      [!] Advertencia: No se pudo actualizar pip" -ForegroundColor Yellow    Write-Host "      [!] Advertencia: No se pudo actualizar pip" -ForegroundColor Yellow

}}

Write-Host ""Write-Host ""



# Instalar dependencias# Instalar dependencias

Write-Host "[6/6] Instalando dependencias desde requirements.txt..." -ForegroundColor YellowWrite-Host "[6/6] Instalando dependencias desde requirements.txt..." -ForegroundColor Yellow

Write-Host ""Write-Host ""

Write-Host "      Esto puede tomar algunos minutos..." -ForegroundColor CyanWrite-Host "      Esto puede tomar algunos minutos..." -ForegroundColor Cyan

Write-Host "      ----------------------------------------" -ForegroundColor GrayWrite-Host "      ----------------------------------------" -ForegroundColor Gray



pip install -r requirements.txtpip install -r requirements.txt



Write-Host ""Write-Host ""

if ($LASTEXITCODE -eq 0) {if ($LASTEXITCODE -eq 0) {

    Write-Host "============================================" -ForegroundColor Green    Write-Host "============================================" -ForegroundColor Green

    Write-Host "   ✓ Instalación Completada con Éxito" -ForegroundColor Green    Write-Host "   ✓ Instalación Completada con Éxito" -ForegroundColor Green

    Write-Host "============================================" -ForegroundColor Green    Write-Host "============================================" -ForegroundColor Green

    Write-Host ""    Write-Host ""

    Write-Host "Todas las dependencias han sido instaladas correctamente." -ForegroundColor Green    Write-Host "Todas las dependencias han sido instaladas correctamente." -ForegroundColor Green

    Write-Host ""    Write-Host ""

    Write-Host "Próximos pasos:" -ForegroundColor Cyan    Write-Host "Próximos pasos:" -ForegroundColor Cyan

    Write-Host "  1. Configura tu base de datos en TodoLap\settings.py" -ForegroundColor White    Write-Host "  1. Configura tu base de datos en TodoLap\settings.py" -ForegroundColor White

    Write-Host "  2. Ejecuta las migraciones: python manage.py migrate" -ForegroundColor White    Write-Host "  2. Ejecuta las migraciones: python manage.py migrate" -ForegroundColor White

    Write-Host "  3. Inicia el servidor: .\Scripts\Start_TodoLap.ps1" -ForegroundColor White    Write-Host "  3. Inicia el servidor: .\Scripts\Start_TodoLap.ps1" -ForegroundColor White

    Write-Host ""    Write-Host ""

} else {} else {

    Write-Host "============================================" -ForegroundColor Red    Write-Host "============================================" -ForegroundColor Red

    Write-Host "   ✗ Error en la Instalación" -ForegroundColor Red    Write-Host "   ✗ Error en la Instalación" -ForegroundColor Red

    Write-Host "============================================" -ForegroundColor Red    Write-Host "============================================" -ForegroundColor Red

    Write-Host ""    Write-Host ""

    Write-Host "Ocurrió un error durante la instalación de dependencias." -ForegroundColor Red    Write-Host "Ocurrió un error durante la instalación de dependencias." -ForegroundColor Red

    Write-Host "Por favor, revisa los mensajes de error anteriores." -ForegroundColor Yellow    Write-Host "Por favor, revisa los mensajes de error anteriores." -ForegroundColor Yellow

    Write-Host ""    Write-Host ""

    Write-Host "Soluciones comunes:" -ForegroundColor Cyan    Write-Host "Soluciones comunes:" -ForegroundColor Cyan

    Write-Host "  1. Verifica tu conexión a internet" -ForegroundColor White    Write-Host "  1. Verifica tu conexión a internet" -ForegroundColor White

    Write-Host "  2. Asegúrate de tener permisos de administrador" -ForegroundColor White    Write-Host "  2. Asegúrate de tener permisos de administrador" -ForegroundColor White

    Write-Host "  3. Actualiza pip: python -m pip install --upgrade pip" -ForegroundColor White    Write-Host "  3. Actualiza pip: python -m pip install --upgrade pip" -ForegroundColor White

    Write-Host ""    Write-Host ""

    exit 1    exit 1

}}

