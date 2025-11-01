# =========================================
# Script para detener el servidor TodoLap
# =========================================
# Autor: TodoLap Team
# Descripción: Detiene todos los procesos del servidor Django de TodoLap
# Uso: .\Scripts\Stop_TodoLap.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Deteniendo TodoLap Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Obtener ruta del proyecto
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host "[1/3] Buscando procesos de Django..." -ForegroundColor Yellow

# Buscar procesos de Python que ejecutan manage.py
$DjangoProcesses = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*manage.py*runserver*"
}

if ($null -eq $DjangoProcesses) {
    Write-Host "      [!] No se encontraron procesos de Django ejecutándose" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "      [OK] Se encontraron $($DjangoProcesses.Count) proceso(s) de Django" -ForegroundColor Green
    Write-Host ""
    
    # Mostrar procesos encontrados
    Write-Host "[2/3] Procesos encontrados:" -ForegroundColor Yellow
    foreach ($Process in $DjangoProcesses) {
        Write-Host "      - PID: $($Process.Id) | Nombre: $($Process.ProcessName)" -ForegroundColor Cyan
    }
    Write-Host ""
    
    # Detener procesos
    Write-Host "[3/3] Deteniendo procesos..." -ForegroundColor Yellow
    foreach ($Process in $DjangoProcesses) {
        try {
            Stop-Process -Id $Process.Id -Force
            Write-Host "      [OK] Proceso $($Process.Id) detenido correctamente" -ForegroundColor Green
        } catch {
            Write-Host "      [ERROR] No se pudo detener el proceso $($Process.Id): $_" -ForegroundColor Red
        }
    }
    Write-Host ""
}

# Verificar si hay procesos en el puerto 8000
Write-Host "[INFO] Verificando puerto 8000..." -ForegroundColor Yellow
$PortProcess = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -First 1

if ($null -ne $PortProcess) {
    $PID = $PortProcess.OwningProcess
    Write-Host "      [!] Proceso $PID usando el puerto 8000" -ForegroundColor Yellow
    Write-Host "      Intentando detener..." -ForegroundColor Yellow
    try {
        Stop-Process -Id $PID -Force
        Write-Host "      [OK] Proceso en puerto 8000 detenido" -ForegroundColor Green
    } catch {
        Write-Host "      [ERROR] No se pudo detener el proceso: $_" -ForegroundColor Red
    }
} else {
    Write-Host "      [OK] Puerto 8000 está libre" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   TodoLap Server detenido" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
