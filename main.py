# This is a placeholder script for PyInstaller to create the main executable 
# https://addaxdatascience.com/ecoassist/
# Created by Peter van Lunteren
# Latest edit by Peter van Lunteren on 17 Dec 2024

import os
import subprocess
import sys
import PySimpleGUI as sg

# clean ecoassist fpath
if getattr(sys, 'frozen', False):
    EcoAssist_files = os.path.dirname(sys.executable)
else:
    EcoAssist_files = os.path.dirname(os.path.abspath(__file__))
    
if EcoAssist_files.endswith("main.app/Contents/MacOS"):
    EcoAssist_files = EcoAssist_files.replace("main.app/Contents/MacOS", "")
    
if EcoAssist_files.endswith(".app/Contents/MacOS"):
    EcoAssist_files = os.path.dirname(os.path.dirname(os.path.dirname(EcoAssist_files)))
    
# script path
GUI_script = os.path.join(EcoAssist_files, "EcoAssist", "EcoAssist_GUI.py")

# open simple window
first_startup_file = os.path.join(EcoAssist_files, "first-startup.txt")
if os.path.isfile(first_startup_file):
    layout = [[sg.Text("Starting up EcoAssist...\n"
                       "This may take a few minutes the first time due to the initial loading of all the dependencies, conda environments, and models.\n"
                       "All subsequent times will be faster.")]]
    window = sg.Window("Progress", layout)

# fetch python interprator
def get_python_interprator(env_name):
    return os.path.join(EcoAssist_files, "envs", f"env-{env_name}", "bin", "python")

# check base env
subprocess.run([get_python_interprator("base"), GUI_script])

# close window
if 'window' in locals():
    window.close()
