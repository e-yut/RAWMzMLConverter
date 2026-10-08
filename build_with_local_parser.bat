@echo off
setlocal
cd /d "%~dp0"

set "PARSER_DIR=C:\Users\eylan\OneDrive - Swansea University\Desktop\Python\MSPeakIntegrator\PyInstaller\Raw_mzML_converter\ThermoRawFileParser"

if not exist "%PARSER_DIR%\ThermoRawFileParser.exe" (
    echo ERROR: ThermoRawFileParser.exe not found in "%PARSER_DIR%"
    pause
    exit /b 1
)

python -m pip install --quiet -r requirements-dev.txt
if errorlevel 1 goto :fail

python -m PyInstaller --noconfirm --clean --noconsole --onefile ^
    --name ThermoRAW-to-MzML-Converter ^
    --add-data "%PARSER_DIR%;ThermoRawFileParser" ^
    src\thermo_raw_to_mzml_gui.py
if errorlevel 1 goto :fail

echo.
echo Build complete: %~dp0dist\ThermoRAW-to-MzML-Converter.exe
pause
exit /b 0

:fail
echo.
echo Build FAILED.
pause
exit /b 1
