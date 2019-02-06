import sys
from cx_Freeze import setup, Executable
#NOT yet ready
# Dependencies are automatically detected, but it might need fine tuning.
assets_to_include = ["ROADMAP.md"]
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"], "include_files": assets_to_include}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "PixelBrawl",
        version = "0.3-a3-DEV",
        description = "A simple yet (hopefully !) fun game",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])

