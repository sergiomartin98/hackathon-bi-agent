@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul
title Agente de BI - Retail Intelligence
color 0B

cd /d "%~dp0"

echo ======================================================================
echo           SISTEMA AGENTE DE BI - RETAIL INTELLIGENCE
echo ======================================================================
echo.
echo [1/3] Verificando entorno de Python...

where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] No se encontro Python en el PATH del sistema.
    echo Por favor asegurese de tener instalado Python 3.10+ y marcado "Add to PATH".
    echo.
    pause
    exit /b 1
)

echo [OK] Python detectado correctamente.
echo.

echo [2/3] Verificando dependencias necesarias...
python -c "import pandas, sqlalchemy, psycopg2, dotenv" >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [INFO] Instalando librerias requeridas desde requirements.txt...
    python -m pip install -r requirements.txt
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Error al instalar dependencias con pip.
        pause
        exit /b 1
    )
)
echo [OK] Dependencias listas y verificadas.
echo.

if not exist ".env" (
    echo [AVISO] No se encontro el archivo .env con las credenciales de Supabase.
    if exist ".env.example" (
        echo [INFO] Creando archivo .env a partir de .env.example...
        copy ".env.example" ".env" >nul
        echo [IMPORTANTE] Se ha generado el archivo .env.
        echo Por favor abre .env en tu editor y coloca la contraseña de tu base de datos Supabase.
        echo.
        pause
    )
)

echo [3/3] Ejecutando el Agente de BI (Skill 1 y Skill 2)...
echo ----------------------------------------------------------------------
python 04_agente\main.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] La ejecucion del agente finalizo con errores.
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo                 EJECUCION COMPLETADA CON EXITO
echo ======================================================================
echo   1. Dashboard HTML:  04_agente\outputs\dashboard_clientes_vip.html
echo   2. Reporte PDF:     04_agente\outputs\reporte_clientes_vip.pdf
echo ======================================================================
echo.

set /p ABRIR="Deseas abrir el Dashboard HTML interactivo en tu navegador? (S/N): "
if /i "%ABRIR%"=="S" (
    start "" "04_agente\outputs\dashboard_clientes_vip.html"
)

set /p ABRIR_PDF="Deseas abrir el Documento PDF generado? (S/N): "
if /i "%ABRIR_PDF%"=="S" (
    start "" "04_agente\outputs\reporte_clientes_vip.pdf"
)

echo.
echo Presiona cualquier tecla para salir...
pause >nul
