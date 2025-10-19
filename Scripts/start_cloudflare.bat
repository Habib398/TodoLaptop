@echo off
REM Script alternativo para iniciar Django con Cloudflare (usando CMD)
REM Ejecutar con: Scripts\start_cloudflare.bat

echo ==================================
echo Iniciando TodoLaptop con Cloudflare
echo ==================================
echo.

cd /d "%~dp0.."

REM Activar entorno virtual si existe
if exist "venv\Scripts\activate.bat" (
    echo [1/3] Activando entorno virtual...
    call venv\Scripts\activate.bat
) else (
    echo [!] Advertencia: No se encontro el entorno virtual
)

echo.
echo [2/3] Iniciando servidor Django en puerto 8000...
start "Django Server" cmd /k "python manage.py runserver 8000"

timeout /t 3 /nobreak >nul

echo [OK] Django iniciado
echo.
echo [3/3] Iniciando tunel de Cloudflare...
echo.
echo ================================================
echo El tunel se iniciara y te dara una URL publica
echo Copia la URL que aparece
echo ================================================
echo.
echo Presiona Ctrl+C para detener el tunel
echo (Cierra la otra ventana para detener Django)
echo.

cloudflared tunnel --url http://localhost:8000

pause
