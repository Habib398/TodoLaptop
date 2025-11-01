# =========================================
# Script de Configuración de Variables de Entorno
# =========================================
# Autor: TodoLap Team
# Descripción: Ayuda a crear y configurar el archivo .env
# Uso: .\Scripts\Setup_Env.ps1

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   Configuración de Variables de Entorno" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Obtener ruta del proyecto
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

# Verificar si existe .env.example
if (-not (Test-Path ".env.example")) {
    Write-Host "[ERROR] No se encontró el archivo .env.example" -ForegroundColor Red
    Write-Host "Este archivo es necesario como plantilla." -ForegroundColor Yellow
    exit 1
}

# Verificar si ya existe .env
if (Test-Path ".env") {
    Write-Host "[!] Ya existe un archivo .env" -ForegroundColor Yellow
    $Overwrite = Read-Host "¿Deseas sobrescribirlo? (S/N)"
    if ($Overwrite -ne "S" -and $Overwrite -ne "s") {
        Write-Host "Operación cancelada." -ForegroundColor Yellow
        exit 0
    }
}

Write-Host ""
Write-Host "Vamos a configurar las variables de entorno para TodoLap." -ForegroundColor Cyan
Write-Host "Presiona Enter para usar los valores predeterminados." -ForegroundColor Gray
Write-Host ""

# Configuración de Base de Datos
Write-Host "=== Configuración de Base de Datos ===" -ForegroundColor Yellow
Write-Host ""

$DbName = Read-Host "Nombre de la base de datos [TodoLaptop]"
if ([string]::IsNullOrWhiteSpace($DbName)) { $DbName = "TodoLaptop" }

$DbUser = Read-Host "Usuario de PostgreSQL [postgres]"
if ([string]::IsNullOrWhiteSpace($DbUser)) { $DbUser = "postgres" }

$DbPassword = Read-Host "Contraseña de PostgreSQL [12345678]"
if ([string]::IsNullOrWhiteSpace($DbPassword)) { $DbPassword = "12345678" }

$DbHost = Read-Host "Host de PostgreSQL [localhost]"
if ([string]::IsNullOrWhiteSpace($DbHost)) { $DbHost = "localhost" }

$DbPort = Read-Host "Puerto de PostgreSQL [5432]"
if ([string]::IsNullOrWhiteSpace($DbPort)) { $DbPort = "5432" }

Write-Host ""
Write-Host "=== Configuración de Django ===" -ForegroundColor Yellow
Write-Host ""

$SecretKey = Read-Host "Secret Key (dejar vacío para generar una aleatoria)"
if ([string]::IsNullOrWhiteSpace($SecretKey)) {
    # Generar secret key aleatoria
    $SecretKey = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 50 | ForEach-Object {[char]$_})
    Write-Host "Secret Key generada automáticamente" -ForegroundColor Green
}

$Debug = Read-Host "Modo Debug (True/False) [True]"
if ([string]::IsNullOrWhiteSpace($Debug)) { $Debug = "True" }

# Crear archivo .env
Write-Host ""
Write-Host "Creando archivo .env..." -ForegroundColor Cyan

$EnvContent = @"
# =========================================
# Configuración de Variables de Entorno
# =========================================
# IMPORTANTE: Este archivo contiene información sensible
# NO subir a Git / NO compartir públicamente

# Django Settings
SECRET_KEY=$SecretKey
DEBUG=$Debug

# Base de Datos PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=$DbName
DB_USER=$DbUser
DB_PASSWORD=$DbPassword
DB_HOST=$DbHost
DB_PORT=$DbPort

# Configuración de Seguridad (Producción)
# Cambiar a True en producción con HTTPS
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
"@

Set-Content -Path ".env" -Value $EnvContent

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "   ✓ Archivo .env Creado Exitosamente" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Configuración guardada en: .env" -ForegroundColor Green
Write-Host ""
Write-Host "Resumen de configuración:" -ForegroundColor Cyan
Write-Host "  Base de datos: $DbName" -ForegroundColor White
Write-Host "  Usuario: $DbUser" -ForegroundColor White
Write-Host "  Host: $DbHost" -ForegroundColor White
Write-Host "  Puerto: $DbPort" -ForegroundColor White
Write-Host "  Debug: $Debug" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  IMPORTANTE: El archivo .env NO debe subirse a Git" -ForegroundColor Yellow
Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Cyan
Write-Host "  1. Ejecutar: .\Scripts\Complete_Setup.ps1" -ForegroundColor White
Write-Host "  2. O ejecutar: .\Scripts\Install_Dependencies.ps1" -ForegroundColor White
Write-Host ""
