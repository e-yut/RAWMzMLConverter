#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

APP_TITLE = "Thermo RAW to mzML Converter v1 (packaged by Eylan Yutuc)"
PARSER_NAME = "ThermoRawFileParser.exe"


def app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def bundled_parser_path() -> Path:
    base = Path(getattr(sys, "_MEIPASS", str(app_dir())))
    return base / "ThermoRawFileParser" / "ThermoRawFileParser.exe"


def hidden_subprocess_kwargs() -> dict:
    kwargs: dict = {}
    if sys.platform.startswith("win"):
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = getattr(subprocess, "SW_HIDE", 0)
        kwargs["startupinfo"] = si
    return kwargs


class ConverterGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("760x520")

        self.selected_files: list[str] = []
        self.output_dir = tk.StringVar(value=str(app_dir() / "mzMLfiles"))
        self.indexed_var = tk.BooleanVar(value=False)
        self.gzip_var = tk.BooleanVar(value=False)
        self.no_peak_pick_var = tk.BooleanVar(value=False)
        self.ms_level_var = tk.StringVar(value="")
        self.status_var = tk.StringVar(value="Ready")
        self.metadata_var = tk.StringVar(value="2")

        self._build_ui()
        self._update_parser_status()

    def _build_ui(self) -> None:
        outer = ttk.Frame(self.root, padding=12)
        outer.pack(fill="both", expand=True)

        ttk.Label(outer, text=APP_TITLE, font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 10))

        parser_frame = ttk.LabelFrame(outer, text="Bundled converter", padding=10)
        parser_frame.pack(fill="x", pady=(0, 10))
        self.parser_label = ttk.Label(parser_frame, text="Checking for bundled ThermoRawFileParser...")
        self.parser_label.pack(anchor="w")

        files_frame = ttk.LabelFrame(outer, text="RAW files", padding=10)
        files_frame.pack(fill="both", expand=True, pady=(0, 10))

        btn_row = ttk.Frame(files_frame)
        btn_row.pack(fill="x", pady=(0, 8))
        ttk.Button(btn_row, text="Add RAW Files", command=self.add_files).pack(side="left", padx=(0, 8))
        ttk.Button(btn_row, text="Add Folder", command=self.add_folder).pack(side="left", padx=(0, 8))
        ttk.Button(btn_row, text="Clear List", command=self.clear_files).pack(side="left")

        self.file_list = tk.Listbox(files_frame, height=12, selectmode=tk.EXTENDED)
        self.file_list.pack(fill="both", expand=True)

        options = ttk.LabelFrame(outer, text="Options", padding=10)
        options.pack(fill="x", pady=(0, 10))

        out_row = ttk.Frame(options)
        out_row.pack(fill="x", pady=(0, 8))
        ttk.Label(out_row, text="Output folder:", width=14).pack(side="left")
        ttk.Entry(out_row, textvariable=self.output_dir).pack(side="left", fill="x", expand=True, padx=(0, 8))
        ttk.Button(out_row, text="Browse", command=self.choose_output_dir).pack(side="left")

        opt_row1 = ttk.Frame(options)
        opt_row1.pack(fill="x", pady=(0, 6))
        ttk.Checkbutton(opt_row1, text="Indexed mzML", variable=self.indexed_var).pack(side="left", padx=(0, 12))
        ttk.Checkbutton(opt_row1, text="GZip output", variable=self.gzip_var).pack(side="left", padx=(0, 12))
        ttk.Checkbutton(opt_row1, text="Disable peak picking", variable=self.no_peak_pick_var).pack(side="left")

        opt_row2 = ttk.Frame(options)
        opt_row2.pack(fill="x")
        ttk.Label(opt_row2, text="MS level:", width=14).pack(side="left")
        ttk.Entry(opt_row2, textvariable=self.ms_level_var, width=12).pack(side="left", padx=(0, 12))
        ttk.Label(opt_row2, text="Metadata:").pack(side="left")
        ttk.Combobox(opt_row2, textvariable=self.metadata_var, values=["0", "1", "2"], width=5, state="readonly").pack(side="left")
        ttk.Label(opt_row2, text="0=json, 1=txt, 2=none").pack(side="left", padx=(8, 0))

        action_row = ttk.Frame(outer)
        action_row.pack(fill="x", pady=(0, 10))
        self.convert_btn = ttk.Button(action_row, text="Convert", command=self.start_conversion)
        self.convert_btn.pack(side="left")
        ttk.Button(action_row, text="Open Output Folder", command=self.open_output_folder).pack(side="left", padx=(8, 0))

        self.progress = ttk.Progressbar(outer, mode="determinate")
        self.progress.pack(fill="x", pady=(0, 6))
        ttk.Label(outer, textvariable=self.status_var).pack(anchor="w")

        log_frame = ttk.LabelFrame(outer, text="Log", padding=8)
        log_frame.pack(fill="both", expand=True)
        self.log = tk.Text(log_frame, height=10, wrap="word", state="disabled")
        self.log.pack(fill="both", expand=True)

    def log_message(self, msg: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _update_parser_status(self) -> None:
        parser = bundled_parser_path()
        if parser.exists():
            self.parser_label.config(text=f"Bundled parser found: {parser}")
        else:
            self.parser_label.config(text=f"Bundled parser not found: {parser}")

    def add_files(self) -> None:
        files = filedialog.askopenfilenames(
            title="Select Thermo RAW files",
            filetypes=[("Thermo RAW", "*.raw"), ("All files", "*.*")],
        )
        self._append_files(files)

    def add_folder(self) -> None:
        folder = filedialog.askdirectory(title="Select folder containing RAW files")
        if not folder:
            return
        files = sorted(str(p) for p in Path(folder).glob("*.raw"))
        self._append_files(files)

    def _append_files(self, files) -> None:
        for file in files:
            if file not in self.selected_files:
                self.selected_files.append(file)
                self.file_list.insert("end", file)
        self.status_var.set(f"{len(self.selected_files)} file(s) selected")

    def clear_files(self) -> None:
        self.selected_files.clear()
        self.file_list.delete(0, "end")
        self.status_var.set("Ready")

    def choose_output_dir(self) -> None:
        folder = filedialog.askdirectory(title="Choose output folder", initialdir=self.output_dir.get())
        if folder:
            self.output_dir.set(folder)

    def open_output_folder(self) -> None:
        out = Path(self.output_dir.get())
        out.mkdir(parents=True, exist_ok=True)
        if sys.platform.startswith("win"):
            os.startfile(out)  # type: ignore[attr-defined]
        else:
            subprocess.run(["xdg-open", str(out)], check=False)

    def build_command(self, raw_file: Path, output_dir: Path) -> list[str]:
        fmt = "2" if self.indexed_var.get() else "1"
        cmd = [
            str(bundled_parser_path()),
            f"-i={raw_file}",
            f"-o={output_dir}",
            f"-f={fmt}",
            f"-m={self.metadata_var.get()}",
            "-l=2",
        ]
        if self.gzip_var.get():
            cmd.append("-g")
        if self.no_peak_pick_var.get():
            cmd.append("-p")
        ms_level = self.ms_level_var.get().strip()
        if ms_level:
            cmd.append(f"-L={ms_level}")
        return cmd

    def start_conversion(self) -> None:
        if not bundled_parser_path().exists():
            messagebox.showerror("Missing converter", "ThermoRawFileParser.exe is not bundled with this app.")
            return
        if not self.selected_files:
            messagebox.showwarning("No files", "Please add one or more .raw files first.")
            return

        output_dir = Path(self.output_dir.get()).expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

        self.convert_btn.config(state="disabled")
        self.progress["maximum"] = len(self.selected_files)
        self.progress["value"] = 0
        self.status_var.set("Converting...")
        self.log_message("Starting conversion...")

        thread = threading.Thread(target=self._convert_worker, args=(output_dir,), daemon=True)
        thread.start()

    def _convert_worker(self, output_dir: Path) -> None:
        failures = 0
        hidden_kwargs = hidden_subprocess_kwargs()

        for idx, file_str in enumerate(self.selected_files, start=1):
            raw_file = Path(file_str)
            cmd = self.build_command(raw_file, output_dir)
            self.root.after(0, self.log_message, f"Converting {raw_file.name}")
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=True,
                    **hidden_kwargs,
                )
                if result.stdout.strip():
                    self.root.after(0, self.log_message, result.stdout.strip())
                self.root.after(0, self.log_message, f"Finished {raw_file.name}\n")
            except subprocess.CalledProcessError as e:
                failures += 1
                detail = e.stderr.strip() or e.stdout.strip() or "Unknown conversion error"
                self.root.after(0, self.log_message, f"FAILED {raw_file.name}: {detail}\n")
            self.root.after(0, self.progress.configure, {"value": idx})

        def done() -> None:
            self.convert_btn.config(state="normal")
            if failures:
                self.status_var.set(f"Completed with {failures} failure(s)")
                messagebox.showwarning("Conversion finished", f"Finished with {failures} failure(s). See log for details.")
            else:
                self.status_var.set("All conversions finished successfully")
                messagebox.showinfo("Conversion finished", f"Converted {len(self.selected_files)} file(s) to {output_dir}")

        self.root.after(0, done)


def main() -> None:
    root = tk.Tk()
    try:
        icon = app_dir() / "app.ico"
        if icon.exists():
            root.iconbitmap(default=str(icon))
    except Exception:
        pass
    ConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
