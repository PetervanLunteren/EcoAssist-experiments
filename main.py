# This is a placeholder script for PyInstaller to create the main executable 
# https://addaxdatascience.com/ecoassist/
# Created by Peter van Lunteren
# Latest edit by Peter van Lunteren on 17 Dec 2024

import os
import subprocess
import sys
import platform

# os dependent preparation
def run_os_dependent_preparation_tasks():
    system = platform.system()
    msg = "Starting EcoAssist...\n\n"
          "This may take a few minutes initially as dependencies, environments, and models are loaded.\n\n"
          "Don't worry – subsequent starts will be faster!"
    if system == 'Windows':
        subprocess.Popen(['python', '-c', f'import ctypes; ctypes.windll.user32.MessageBoxW(0, "{msg}", "Information", 0x40)'])
    elif system == 'Darwin':
        subprocess.Popen(['osascript', '-e', f'display dialog "{msg}"'])            # show message
        subprocess.run(['xattr', '-dr', 'com.apple.quarantine', EcoAssist_files])   # remove attributes
    elif system == 'Linux':
        subprocess.Popen(['zenity', '--info', '--text', msg])
    else:
        print("Unsupported OS")
        return

# os dependent python executables
def get_python_interprator(env_name):
    return os.path.join(EcoAssist_files, "envs", f"env-{env_name}", "bin", "python")

# clean path
if getattr(sys, 'frozen', False):
    EcoAssist_files = os.path.dirname(sys.executable)
else:
    EcoAssist_files = os.path.dirname(os.path.abspath(__file__))
    
if EcoAssist_files.endswith("main.app/Contents/MacOS"):
    EcoAssist_files = EcoAssist_files.replace("main.app/Contents/MacOS", "")
    
if EcoAssist_files.endswith(".app/Contents/MacOS"):
    EcoAssist_files = os.path.dirname(os.path.dirname(os.path.dirname(EcoAssist_files)))

# init paths    
GUI_script = os.path.join(EcoAssist_files, "EcoAssist", "EcoAssist_GUI.py")
first_startup_file = os.path.join(EcoAssist_files, "first-startup.txt")

# prepare
if os.path.exists(first_startup_file):
    run_os_dependent_preparation_tasks()

# log
print(f"first_startup_file: {first_startup_file}")
print(f"   EcoAssist_files: {EcoAssist_files}")
print(f"    sys.executable: {sys.executable}")
print(f"        GUI_script: {GUI_script}")

# run the GUI script
print("Opening...")
subprocess.run([get_python_interprator("base"), GUI_script])
