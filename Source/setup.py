from distutils.core import setup
import py2exe
import os
import sys

sys.path.append("C:\\Users\\Trevor\\Documents\\ComputerScience\\Python\\GroceryDatabaseProject\\cRuntimeDLL")

from glob import glob
data_files = [("Microsoft.VC90.CRT", glob(r'C:\Users\Trevor\Documents\ComputerScience\Python\GroceryDatabaseProject\cRuntimeDLL\*.*'))]
setup(
    data_files=data_files,
)

origIsSystemDLL = py2exe.build_exe.isSystemDLL # save the orginal before we edit it
def isSystemDLL(pathname):
    # checks if the freetype and ogg dll files are being included
    if os.path.basename(pathname).lower() in ("freesansbold.ttf", "libfreetype-6.dll", "libogg-0.dll", "zlib1.dll", "SDL.dll", "sdl_ttf.dll"):
            return 0
    return origIsSystemDLL(pathname) # return the orginal function
py2exe.build_exe.isSystemDLL = isSystemDLL # override the default function with this one

setup(console=['GrocerySpy.py'])