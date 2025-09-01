@echo off
setlocal enabledelayedexpansion

:: Portable HTML to PDF Converter
:: Works from any location - automatically finds this script's directory

echo.
echo ==========================================
echo   PORTABLE HTML TO PDF CONVERTER
echo ==========================================
echo.

:: Get the directory where this batch file is located
cd /d "%~dp0"
set CONVERTER_DIR=%CD%

:: Check if Node.js is available
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found. Please install Node.js 14+ and add to PATH.
    pause
    exit /b 1
)

:: Check if dependencies are installed
if not exist "node_modules" (
    echo [INFO] Installing dependencies...
    npm install
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies. Please run: npm install
        pause
        exit /b 1
    )
)

:: Show options
echo Choose conversion option:
echo.
echo 1. Convert single HTML file
echo 2. Convert all HTML files in current directory  
echo 3. Convert all HTML files in specific folder
echo 4. Convert specific application folder (e.g., CompanyName_JobTitle)
echo 5. Help
echo.
set /p choice="Enter choice (1-5): "

if "%choice%"=="1" (
    set /p htmlfile="Enter HTML file path: "
    echo [INFO] Converting single file...
    node "%CONVERTER_DIR%\batch_html_to_pdf.js" "!htmlfile!"
) else if "%choice%"=="2" (
    echo [INFO] Converting all HTML files in current directory...
    node "%CONVERTER_DIR%\batch_html_to_pdf.js" .
) else if "%choice%"=="3" (
    set /p folder="Enter folder path: "
    echo [INFO] Converting all HTML files in folder...
    node "%CONVERTER_DIR%\batch_html_to_pdf.js" "!folder!"
) else if "%choice%"=="4" (
    echo.
    echo Available application folders:
    dir ".." /b /ad 2>nul | findstr /v "PDF_Converter _PENDING_ANALYSIS" 
    echo.
    set /p appfolder="Enter application folder name: "
    if exist "..\!appfolder!" (
        echo [INFO] Converting HTML files in application folder: !appfolder!
        node "%CONVERTER_DIR%\batch_html_to_pdf.js" "..\!appfolder!"
    ) else (
        echo [ERROR] Application folder not found: !appfolder!
    )
) else if "%choice%"=="5" (
    node "%CONVERTER_DIR%\batch_html_to_pdf.js" --help
) else (
    echo [ERROR] Invalid choice. Please select 1-5.
)

echo.
echo Conversion complete!
echo.
pause