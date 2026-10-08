# ThermoRAW-to-MzML Converter

A simple desktop GUI (Python/Tkinter) for batch-converting Thermo `.raw` mass spectrometry files to open-standard
`.mzML`, powered by [ThermoRawFileParser](https://github.com/compomics/ThermoRawFileParser).

Packaged by Eylan Yutuc.

## Download

Ready-to-run Windows executable (no Python needed): **[Download page](https://e-yut.github.io/RAWMzMLConverter/)**
or the [latest release](https://github.com/e-yut/RAWMzMLConverter/releases/latest).

## Features

- Add individual `.raw` files or a whole folder
- Batch conversion with a progress bar and live log
- Options: indexed mzML, GZip output, disable peak picking, MS-level filter, metadata output (JSON / TXT / none)
- Conversion runs in a background thread; the converter console window stays hidden on Windows
- Can be bundled into a single standalone `.exe` with PyInstaller

## Requirements

- Windows (ThermoRawFileParser.exe is a Windows build; see [docs/BUILD.md](docs/BUILD.md) for other platforms)
- Python 3.9+ with Tkinter (included in the standard python.org installer)
- `ThermoRawFileParser.exe` (not included in this repo, see below)

The GUI itself has no third-party Python dependencies.

## Setup

1. Download a ThermoRawFileParser release from
   <https://github.com/compomics/ThermoRawFileParser/releases> (Windows `.zip`).
2. Extract it so the layout is:

   ```
   src/
   ├── thermo_raw_to_mzml_gui.py
   └── ThermoRawFileParser/
       └── ThermoRawFileParser.exe   (plus its DLLs)
   ```

3. Run:

   ```powershell
   python src/thermo_raw_to_mzml_gui.py
   ```

Optional: place an `app.ico` next to the script to use a custom window icon.

## Usage

See [docs/USAGE.md](docs/USAGE.md). In short: add RAW files, choose an output folder (default `mzMLfiles/` next to
the app), set options, and click **Convert**.

## Building a standalone executable

See [docs/BUILD.md](docs/BUILD.md), or run `build.ps1` from the repository root.

## License and attribution

This project is released under the [MIT License](LICENSE). ThermoRawFileParser is a separate project
(Apache-2.0) by the CompOmics group; it is not distributed here. If you use it in published work, please cite:

> Hulstaert N. et al., *ThermoRawFileParser: Modular, Scalable, and Cross-Platform RAW File Conversion*,
> J. Proteome Res. 2020, 19(1), 537-542. doi:10.1021/acs.jproteome.9b00328
