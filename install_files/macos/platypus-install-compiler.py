# MacOS Application installer script for EcoAssist
# To be used with Platipus packaging tool (https://github.com/sveinbjornt/Platypus)
# Github actions will add the version number as a first line to the script like 'VERSION="v5.109"'
# Peter van Lunteren, 9 jan 2025

import os
import subprocess
import shutil
import requests
import sys
import tarfile

# Define variables
URL = f"https://storage.googleapis.com/github-release-files-storage/{VERSION}/osx-arm-{VERSION}.tar.xz"
APP_NAME = "EcoAssist"
APPLICATIONS_DIR = "/Applications"
SHORTCUT = os.path.expanduser(f"~/Desktop/{APP_NAME}.app")
TAR_FILE = f"/tmp/{APP_NAME}.tar.xz"
INSTALL_DIR = f"/Applications/{APP_NAME}"
PBAR_POS = 0

print(f"PROGRESS:{PBAR_POS}");sys.stdout.flush();PBAR_POS += 2

# Read previous version
previous_version_path = os.path.join(INSTALL_DIR, "EcoAssist", "version.txt")
if os.path.exists(previous_version_path):
    with open(previous_version_path, "r") as file:
        PREVIOUS_VERSION = f"v{file.read().strip()}"
else:
    PREVIOUS_VERSION = "previous installation"

print(f"PROGRESS:{PBAR_POS}");sys.stdout.flush();PBAR_POS += 3

# Step 0: Remove previous installation
print(f"{str(PBAR_POS).ljust(3)}% - Step 1 of 5 - Uninstalling {PREVIOUS_VERSION}...");sys.stdout.flush()
if os.path.exists(INSTALL_DIR):
    try:
        shutil.rmtree(INSTALL_DIR)
    except Exception as e:
        print(f"ALERT:Error|Failed to remove {PREVIOUS_VERSION} {INSTALL_DIR}");sys.stdout.flush()
        print(f"Error: {e}");sys.stdout.flush()
        exit(1)

print(f"PROGRESS:{PBAR_POS}");sys.stdout.flush();PBAR_POS += 16

# Remove existing shortcut
if os.path.islink(SHORTCUT):
    os.unlink(SHORTCUT)

print(f"PROGRESS:{PBAR_POS}");sys.stdout.flush();PBAR_POS += 1

# Step 1: Download the tar.xz file
if os.path.exists(TAR_FILE):
    os.remove(TAR_FILE)

print(f"PROGRESS:{PBAR_POS}");sys.stdout.flush();PBAR_POS += 1
print(f"{str(PBAR_POS).ljust(3)}% - Step 2 of 5 - Downloading {VERSION}...");sys.stdout.flush()

# this downloads the tar file in chunks and updates the pbar every 5% with 1% increments
try:
    response = requests.get(URL, stream=True)
    response.raise_for_status()
    
    # Get the total file size from the headers
    total_size = int(response.headers.get('Content-Length', 0))
    chunk_size = 8192  # Size of each chunk

    # Track progress
    downloaded = 0
    last_reported_progress = 0  # Keeps track of the last reported percentage
    
    with open(TAR_FILE, "wb") as file:
        for chunk in response.iter_content(chunk_size=chunk_size):
            file.write(chunk)
            downloaded += len(chunk)
            
            # Calculate the progress percentage
            progress = (downloaded / total_size) * 100
            
            # Check if progress increased by at least 5%
            if progress - last_reported_progress >= 5:
                PBAR_POS_INCREMENT = int((progress - last_reported_progress) // 5)
                last_reported_progress += PBAR_POS_INCREMENT * 5  # Update to the latest 5% threshold
                print(f"PROGRESS:{PBAR_POS}");sys.stdout.flush();PBAR_POS += PBAR_POS_INCREMENT
                print(f"{str(PBAR_POS).ljust(3)}% - Step 2 of 5 - Downloading {VERSION}...");sys.stdout.flush()

except Exception as e:
    print(f"ALERT:Error|Failed to download {APP_NAME} from {URL}");sys.stdout.flush()
    print(f"Error: {e}");sys.stdout.flush()
    exit(1)

# Step 2: Extract the tar.xz file to the Applications folder
if not os.path.exists(INSTALL_DIR):
    os.makedirs(INSTALL_DIR)

print(f"PROGRESS:{PBAR_POS}");sys.stdout.flush();PBAR_POS += 2

print(f"{str(PBAR_POS).ljust(3)}% - Step 3 of 5 - Extracting files...");sys.stdout.flush()
try:
    shutil.unpack_archive(TAR_FILE, APPLICATIONS_DIR)
except Exception as e:
    print(f"ALERT:Error|Failed to extract {APP_NAME} to {APPLICATIONS_DIR}");sys.stdout.flush()
    print(f"Error: {e}");sys.stdout.flush()
    exit(1)

print(f"PROGRESS:{PBAR_POS}");sys.stdout.flush();PBAR_POS += 19

# Cleanup: Remove the downloaded tar.xz file
os.remove(TAR_FILE)

print(f"PROGRESS:{PBAR_POS}");sys.stdout.flush();PBAR_POS += 2

# Step 3: Remove attributes recursively
print(f"{str(PBAR_POS).ljust(3)}% - Step 4 of 5 - Removing attributes...");sys.stdout.flush()
try:
    subprocess.run(["xattr", "-dr", "com.apple.quarantine", INSTALL_DIR], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error: Failed to remove attributes: {e}");sys.stdout.flush()
    exit(1)

print(f"PROGRESS:{PBAR_POS}");sys.stdout.flush();PBAR_POS += 21

# Dummy open the app to trigger the first run experience
print(f"{str(PBAR_POS).ljust(3)}% - Step 5 of 5 - Compiling scripts...");sys.stdout.flush()
try:
    subprocess.run([f"{INSTALL_DIR}/envs/env-base/bin/python", 
                    f"{INSTALL_DIR}/EcoAssist/EcoAssist_GUI.py", 
                    "installer"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error: Failed to trigger the first run experience: {e}");sys.stdout.flush()
    exit(1)

print(f"PROGRESS:{PBAR_POS}");sys.stdout.flush();PBAR_POS += 12

# Step 4: Create a shortcut on the Desktop
if os.path.exists(SHORTCUT):
    os.remove(SHORTCUT)

print(f"PROGRESS:{PBAR_POS}");sys.stdout.flush();PBAR_POS += 2

try:
    os.symlink(f"{INSTALL_DIR}/{APP_NAME} {VERSION}.app", SHORTCUT)
    print(f"Installation completed successfully!");sys.stdout.flush()
    print(f"ALERT:Installation successfull!|You can now open EcoAssist via the Desktop shortcut:{' ' * 70}'{SHORTCUT}'");sys.stdout.flush()
except Exception as e:
    print(f"ALERT:Error|Failed to create shortcut {SHORTCUT}");sys.stdout.flush()
    print(f"Error: {e}");sys.stdout.flush()
    exit(1)
