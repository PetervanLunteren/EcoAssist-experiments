# This is a placeholder script for PyInstaller to create the main executable 
# https://addaxdatascience.com/ecoassist/
# Created by Peter van Lunteren
# Latest edit by Peter van Lunteren on 17 Dec 2024

import os
import subprocess
import sys
import platform

# show info message
def show_info_message(message):
    system = platform.system()
    if system == 'Windows':
        subprocess.Popen(['python', '-c', f'import ctypes; ctypes.windll.user32.MessageBoxW(0, "{message}", "Information", 0x40)'])
    elif system == 'Darwin':
        subprocess.Popen(['osascript', '-e', f'display dialog "{message}"'])
    elif system == 'Linux':
        subprocess.Popen(['zenity', '--info', '--text', message])
    else:
        print("Unsupported OS")
        return
show_info_message("Starting EcoAssist...\n\n"
                  "This may take a few minutes initially as dependencies, environments, and models are loaded.\n\n"
                  "Don't worry – subsequent starts will be faster!")

# clean path
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

# os dependent python executables
def get_python_interprator(env_name):
    return os.path.join(EcoAssist_files, "envs", f"env-{env_name}", "bin", "python")

# run the GUI script
subprocess.run([get_python_interprator("base"), GUI_script])
