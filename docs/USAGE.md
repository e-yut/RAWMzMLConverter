# Usage

1. **Add RAW Files** – select one or more `.raw` files, or **Add Folder** to add every `.raw` file in a folder
   (non-recursive). Duplicates are ignored. **Clear List** empties the queue.
2. **Output folder** – defaults to `mzMLfiles` next to the app. Use **Browse** to change it.
3. **Options**

   | Option | ThermoRawFileParser flag | Notes |
   |---|---|---|
   | Indexed mzML | `-f=2` (otherwise `-f=1`) | Plain mzML vs. indexedmzML |
   | GZip output | `-g` | Compress output |
   | Disable peak picking | `-p` | Keep profile data |
   | MS level | `-L=<levels>` | Optional, e.g. `1`, `2`, `1-3`, `1,2` |
   | Metadata | `-m=0/1/2` | 0 = JSON, 1 = TXT, 2 = none (default) |

4. Click **Convert**. Progress and parser output appear in the log. A summary dialog is shown when finished.
5. **Open Output Folder** opens the destination in the file manager.

## Troubleshooting

- **"Bundled parser not found"** – place `ThermoRawFileParser/ThermoRawFileParser.exe` next to the script
  (or bundle it with PyInstaller, see [BUILD.md](BUILD.md)).
- **A file fails** – the log shows ThermoRawFileParser's error output; corrupted or still-acquiring RAW files are
  the usual cause.
