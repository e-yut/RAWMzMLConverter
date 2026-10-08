# Building a standalone executable

The app locates the parser at `ThermoRawFileParser/ThermoRawFileParser.exe` relative to the script, or inside
PyInstaller's bundle directory (`sys._MEIPASS`) when frozen.

## Steps (Windows)

1. Put the extracted ThermoRawFileParser folder at `src\ThermoRawFileParser\`.
2. Install PyInstaller: `pip install -r requirements-dev.txt`
3. From the repository root run:

   ```powershell
   .\build.ps1
   ```

   The executable is written to `dist\ThermoRAW-to-MzML-Converter.exe`.

Equivalent manual command:

```powershell
pyinstaller --noconsole --onefile --name ThermoRAW-to-MzML-Converter `
  --add-data "src\ThermoRawFileParser;ThermoRawFileParser" src\thermo_raw_to_mzml_gui.py
```

Add `--icon app.ico` for a custom icon.

## Other platforms

ThermoRawFileParser also ships Linux/macOS builds that need .NET/Mono. The GUI currently hard-codes
`ThermoRawFileParser.exe`, so non-Windows use requires adjusting `bundled_parser_path()` and `build_command()`.
