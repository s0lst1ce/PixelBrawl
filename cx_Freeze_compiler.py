from cx_Freeze import setup, Executable
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))


""" Production: """
setup(name="Pixelbrawl", version="0.3-a3-DEV", description="Small yet (hopefully !) fun game", author='NotaSmartDev', executables=[Executable("main.py", base=None, targetName='PixelBrawl-ALPHA')])