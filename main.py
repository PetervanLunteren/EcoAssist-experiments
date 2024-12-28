# This is a placeholder script for PyInstaller to create the main executable 
# https://addaxdatascience.com/ecoassist/
# Created by Peter van Lunteren
# Latest edit by Peter van Lunteren on 17 Dec 2024

import os
import subprocess
import sys
import platform

print("\n")

# check os
system = platform.system()

# os dependent preparation
def run_os_dependent_preparation_tasks(os_name):
    msg = "Starting EcoAssist...\n\nThis may take a few minutes initially as dependencies, "\
          "environments, and models are loaded.\n\nDon't worry – subsequent starts will be faster!"
    if os_name == 'Windows':
        subprocess.Popen([get_python_interprator("base"), '-c',
            'import ctypes; ctypes.windll.user32.MessageBoxW(0, "Starting EcoAssist... This may take a few minutes initially as dependencies, environments, and models are loaded. Subsequent starts will be faster!", "Information", 0x40)'],
            creationflags=subprocess.CREATE_NO_WINDOW)
    elif os_name == 'Darwin':
        print("\n")
        print("Checking files... (this can take a minute...)")
        subprocess.run(['xattr', '-dr', 'com.apple.quarantine', EcoAssist_files])   # remove attributes
    elif os_name == 'Linux':
        subprocess.Popen(['zenity', '--info', '--text', msg])

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

# prepare files for windows (will be run via the normal executable)
if os.path.exists(first_startup_file) and system == 'Windows':
    run_os_dependent_preparation_tasks('Windows')

# check windows debug exe
windows_debug_mode = True if sys.executable.endswith("debug.exe") else False
print(f"   windows_debug_mode: {windows_debug_mode}")

# check macos installer mode
macos_installer_mode = True if sys.executable.endswith(" installer") else False
print(f" macos_installer_mode: {macos_installer_mode}")

# log
print(f"      EcoAssist_files: {EcoAssist_files}")
print(f"       sys.executable: {sys.executable.replace(EcoAssist_files, '.')}")
print(f"           GUI_script: {GUI_script.replace(EcoAssist_files, '.')}")

# python executable
python_executable = get_python_interprator("base")
print(f"    python_executable: {python_executable.replace(EcoAssist_files, '.')}")

# cuda toolkit
cuda_toolkit_path = os.environ.get("CUDA_HOME") or os.environ.get("CUDA_PATH")
print(f"    cuda_toolkit_path: {cuda_toolkit_path}")

# prepare files for macos (will be run via installer executable)
if macos_installer_mode:
    run_os_dependent_preparation_tasks("Darwin")
    print("Loading dependencies and environments... (this can take a minute...)")
    subprocess.run([get_python_interprator("base"), GUI_script, "installer"])
    print("\n\nInstallation is done! You can close this window now and open EcoAssist by double clicking the APP file.\n\n")
    sys.exit()

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
