#!/bin/bash

### Shell script to install EcoAssist on macOS arm64
### Desinged to be executed by a GitHub action
### Peter van Lunteren, 18 Dec 2024 (latest edit)

### refresh root
root="$HOME/EcoAssist"
if [ -d "EcoAssist" ]; then
    rm -rf EcoAssist
    echo "EcoAssist folder removed"
else
    echo "EcoAssist folder does not exist"
fi

### create folder structure
mkdir -p EcoAssist
mkdir -p EcoAssist/envs
mkdir -p EcoAssist/models
mkdir -p EcoAssist/models/det
mkdir -p EcoAssist/models/cls
mkdir -p "EcoAssist/models/det/MegaDetector 5a"
mkdir -p EcoAssist/yolov5_versions/yolov5_old
mkdir -p EcoAssist/yolov5_versions/yolov5_new
echo "Hello world!" >> "EcoAssist/first-startup.txt"

## clone repositories
git clone --depth 1 https://github.com/PetervanLunteren/EcoAssist-experiments.git "EcoAssist/EcoAssist-experiments"
rm -rf "EcoAssist/EcoAssist-experiments/.git"
mv "EcoAssist/EcoAssist-experiments" "EcoAssist/EcoAssist" # DEBUG
mv "EcoAssist/EcoAssist/main.py" "EcoAssist/main.py"
echo "EcoAssist cloned"

git clone https://github.com/agentmorris/MegaDetector.git "EcoAssist/MegaDetector"
git -C "EcoAssist/MegaDetector" checkout e8a4fc19a2b9ad1892dd9ce65d437252df271576
rm -rf "EcoAssist/MegaDetector/.git"
mv "EcoAssist/MegaDetector" "EcoAssist/cameratraps"
echo "MegaDetector cloned"

git clone https://github.com/ultralytics/yolov5.git "EcoAssist/yolov5_versions/yolov5_old/yolov5"
git -C "EcoAssist/yolov5_versions/yolov5_old/yolov5" checkout 868c0e9bbb45b031e7bfd73c6d3983bcce07b9c1
rm -rf "EcoAssist/yolov5_versions/yolov5_old/yolov5/.git"
echo "yolov5 old version cloned"

git clone https://github.com/ultralytics/yolov5.git "EcoAssist/yolov5_versions/yolov5_new/yolov5"
git -C "EcoAssist/yolov5_versions/yolov5_new/yolov5" checkout 3e55763d45f9c5f8217e4dad5ba1e6c1f42e3bf8
rm -rf "EcoAssist/yolov5_versions/yolov5_new/yolov5/.git"
echo "yolov5 new version cloned"

git clone --depth 1 https://github.com/PetervanLunteren/Human-in-the-loop.git "EcoAssist/Human-in-the-loop"
rm -rf "EcoAssist/Human-in-the-loop/.git"
echo "Human-in-the-loop cloned"

git clone --depth 1 https://github.com/PetervanLunteren/visualise_detection.git "EcoAssist/visualise_detection"
rm -rf "EcoAssist/visualise_detection/.git"
echo "visualise_detection cloned"

### download megadetector 
curl -L https://github.com/agentmorris/MegaDetector/releases/download/v5.0/md_v5a.0.0.pt -o "EcoAssist/models/det/MegaDetector 5a/md_v5a.0.0.pt"

# print current working directory
echo "Current working directory: $(pwd)"

# print all files in current working directory
echo "Files in current working directory:"
ls -la

# print all files in EcoAssist folder
echo "Files in EcoAssist folder:"
ls -la EcoAssist

exit 1

### source conda 
if [ -f /Applications/.EcoAssist_files/miniforge/etc/profile.d/conda.sh ]; then
    source /Applications/.EcoAssist_files/miniforge/etc/profile.d/conda.sh
    conda_exe="/Applications/.EcoAssist_files/miniforge/bin/conda"
    echo "Conda found in /Applications/.EcoAssist_files/miniforge"
fi
if [ -f "$HOME/miniforge/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniforge/etc/profile.d/conda.sh"
    conda_exe="$HOME/miniforge/bin/conda"
    echo "Conda found in $HOME/miniforge"
fi

### install env-base
$conda_exe env create --file="EcoAssist/cameratraps/envs/environment-detector-m1.yml" -p "EcoAssist/envs/env-base"
$conda_exe activate "EcoAssist/envs/env-base"
$conda_exe install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 -c pytorch -y
$conda_exe uninstall opencv -y
pip install opencv-python
pip install RangeSlider
pip install gpsphoto
pip install exifread
pip install piexif
pip install openpyxl
pip install customtkinter
pip install CTkTable
pip install folium
pip install plotly
pip install "gitpython>=3.1.30"
pip install "tensorboard>=2.4.1"
pip install "thop>=0.1.1"
pip install "protobuf<=3.20.1"
pip install "setuptools>=65.5.1"
pip install PySide6
$conda_exe install lxml -y
make Human-in-the-loop/pyside6
$conda_exe deactivate

### install env-tensorflow
$conda_exe env create --file="EcoAssist/EcoAssist/classification_utils/envs/tensorflow-macos-silicon.yml" -p "EcoAssist/envs/env-tensorflow"

### install env-pytorch
$conda_exe create -p "EcoAssist/envs/env-pytorch" python=3.8 -y
$conda_exe activate "EcoAssist/envs/env-pytorch"
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2
pip install "ultralytics==8.0.191"
pip install "numpy==1.24.1"
pip install "humanfriendly==10.0"
pip install "jsonpickle==3.0.2"
pip install timm
pip install dill
$conda_exe deactivate

### install env-pywildlife
$conda_exe create -p "EcoAssist/envs/env-pywildlife" python=3.8 -y
$conda_exe activate "EcoAssist/envs/env-pywildlife"
pip install pytorchwildlife
pip install "setuptools<70"
pip install jsonpickle
$conda_exe deactivate

# create fresh pyinstaller environment
$conda_exe create -n fresh python=3.8 pyinstaller -y
$conda_exe activate fresh
pyinstaller --onefile --windowed --icon="EcoAssist/EcoAssist/imgs/logo_small_bg.icns" "EcoAssist/main.py"
$conda_exe deactivate

# clean
$conda_exe clean --all --yes --force-pkgs-dirs
$conda_exe clean --all --yes

# move and rename executables to EcoAssist
mv "dist/main" "EcoAssist/debug_mode"
mv "dist/main.app" "EcoAssist/EcoAssist ${RELEASE_VERSION}.app"
