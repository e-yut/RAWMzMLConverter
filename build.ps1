$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path "src\ThermoRawFileParser\ThermoRawFileParser.exe")) {
    throw "Missing src\ThermoRawFileParser\ThermoRawFileParser.exe - see docs\BUILD.md"
}

pyinstaller --noconsole --onefile --name ThermoRAW-to-MzML-Converter `
    --add-data "src\ThermoRawFileParser;ThermoRawFileParser" `
    src\thermo_raw_to_mzml_gui.py
