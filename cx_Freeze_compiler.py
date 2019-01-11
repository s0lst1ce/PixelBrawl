'''Generic script to compile a .py file using cx_Freeze'''

from cx_Freeze import setup, Executable

setup(
    name = "PixelBrawl",
    version = "v0.1-a1",
    description = "Small and simple yet (hopefully ! ) fun game.",
    executables = [Executable("main.py")],
)