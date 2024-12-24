# This is a placeholder script for PyInstaller to create the main executable 
# https://addaxdatascience.com/ecoassist/
# Created by Peter van Lunteren
# Latest edit by Peter van Lunteren on 17 Dec 2024

import os
import subprocess
import sys
import platform

# check os
system = platform.system()

# os dependent preparation
def run_os_dependent_preparation_tasks():
    msg = "Starting EcoAssist...\n\nThis may take a few minutes initially as dependencies, "\
          "environments, and models are loaded.\n\nDon't worry – subsequent starts will be faster!"
    if system == 'Windows':
        subprocess.Popen([get_python_interprator("base"), '-c',
            'import ctypes; ctypes.windll.user32.MessageBoxW(0, "Starting EcoAssist... This may take a few minutes initially as dependencies, environments, and models are loaded. Subsequent starts will be faster!", "Information", 0x40)'],
            creationflags=subprocess.CREATE_NO_WINDOW)
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
    if system == 'Windows':
        return os.path.join(EcoAssist_files, "envs", f"env-{env_name}", "python.exe")
    else:
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

# check windows debug exe
windows_debug_mode = True if sys.executable.endswith("debug.exe") else False
print(f"\n  windows_debug_mode: {windows_debug_mode}")

# log
print(f"     EcoAssist_files: {EcoAssist_files}")
print(f"      sys.executable: {sys.executable}")
print(f"          GUI_script: {GUI_script}")

# python executable
python_executable = get_python_interprator("base")
print(f"   python_executable: {python_executable}")

# cuda toolkit
cuda_toolkit_path = os.environ.get("CUDA_HOME") or os.environ.get("CUDA_PATH")
# if cuda_toolkit_path:
#     cuda_toolkit_path = os.path.join(cuda_toolkit_path, "bin")
#     current_path = os.environ.get("PATH", "")
#     if cuda_toolkit_path not in current_path:
#         os.environ["PATH"] = current_path + os.pathsep + cuda_toolkit_path
print(f"   cuda_toolkit_path: {cuda_toolkit_path}")

# run the GUI script
print("\nOpening application...")
if system == 'Windows':
    if windows_debug_mode:
        subprocess.run([get_python_interprator("base"), GUI_script])
        input("Press [Enter] to close console window...") # keep console open after closing app
    else:
        subprocess.run([get_python_interprator("base"), GUI_script],
                       creationflags=subprocess.CREATE_NO_WINDOW)
else:
    subprocess.run([get_python_interprator("base"), GUI_script])
