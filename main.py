# This is a placeholder script for PyInstaller to create the main executable 
# https://addaxdatascience.com/ecoassist/
# Created by Peter van Lunteren
# Latest edit by Peter van Lunteren on 17 Dec 2024

import os
import subprocess
import sys

if getattr(sys, 'frozen', False):
    EcoAssist_files = os.path.dirname(sys.executable)
else:
    EcoAssist_files = os.path.dirname(os.path.abspath(__file__))
    
if EcoAssist_files.endswith("main.app/Contents/MacOS"):
    EcoAssist_files = EcoAssist_files.replace("main.app/Contents/MacOS", "")
    
if EcoAssist_files.endswith(".app/Contents/MacOS"):
    EcoAssist_files = os.path.dirname(os.path.dirname(os.path.dirname(EcoAssist_files)))
    
GUI_script = os.path.join(EcoAssist_files, "EcoAssist", "EcoAssist_GUI.py")

print(f"  EcoAssist_files: {EcoAssist_files}")
print(f"   sys.executable: {sys.executable}")
print(f"       GUI_script: {GUI_script}")

def get_python_interprator(env_name):
    return os.path.join(EcoAssist_files, "envs", f"env-{env_name}", "bin", "python")

# check base env
subprocess.run([get_python_interprator("base"), GUI_script])
