#!/bin/bash

### Shell script to install EcoAssist on macOS arm64
### Desinged to be executed by a GitHub action
### Peter van Lunteren, 18 Dec 2024 (latest edit)

### refresh root
root="$HOME/EcoAssist"
if [ -d "${root}" ]; then
    rm -rf "${root}"
    echo "$root folder removed"
else
    echo "$root folder does not exist"
fi

### create folder structure
mkdir -p "${root}"
mkdir -p "${root}/envs"
mkdir -p "${root}/models"
mkdir -p "${root}/models/det"
mkdir -p "${root}/models/cls"
mkdir -p "${root}/models/det/MegaDetector 5a"
mkdir -p "${root}/yolov5_versions/yolov5_old"
mkdir -p "${root}/yolov5_versions/yolov5_new"
echo "Hello world!" >> "${root}/first-startup.txt"

## clone repositories
git clone --depth 1 https://github.com/PetervanLunteren/EcoAssist-experiments.git "${root}/EcoAssist-experiments"
rm -rf "${root}/EcoAssist-experiments/.git"
mv "${root}/EcoAssist-experiments" "${root}/EcoAssist" # DEBUG
mv "${root}/EcoAssist/main.py" "${root}/main.py"
echo "EcoAssist cloned"

git clone https://github.com/agentmorris/MegaDetector.git "${root}/MegaDetector"
git -C "${root}/MegaDetector" checkout e8a4fc19a2b9ad1892dd9ce65d437252df271576
rm -rf "${root}/MegaDetector/.git"
mv "${root}/MegaDetector" "${root}/cameratraps"
echo "MegaDetector cloned"

git clone https://github.com/ultralytics/yolov5.git "${root}/yolov5_versions/yolov5_old/yolov5"
git -C "${root}/yolov5_versions/yolov5_old/yolov5" checkout 868c0e9bbb45b031e7bfd73c6d3983bcce07b9c1
rm -rf "${root}/yolov5_versions/yolov5_old/yolov5/.git"
echo "yolov5 old version cloned"

git clone https://github.com/ultralytics/yolov5.git "${root}/yolov5_versions/yolov5_new/yolov5"
git -C "${root}/yolov5_versions/yolov5_new/yolov5" checkout 3e55763d45f9c5f8217e4dad5ba1e6c1f42e3bf8
rm -rf "${root}/yolov5_versions/yolov5_new/yolov5/.git"
echo "yolov5 new version cloned"

git clone --depth 1 https://github.com/PetervanLunteren/Human-in-the-loop.git "${root}/Human-in-the-loop"
rm -rf "${root}/Human-in-the-loop/.git"
echo "Human-in-the-loop cloned"

git clone --depth 1 https://github.com/PetervanLunteren/visualise_detection.git "${root}/visualise_detection"
rm -rf "${root}/visualise_detection/.git"
echo "visualise_detection cloned"

### download megadetector 
curl -L https://github.com/agentmorris/MegaDetector/releases/download/v5.0/md_v5a.0.0.pt -o "${root}/models/det/MegaDetector 5a/md_v5a.0.0.pt"

### source conda 
if [ -f "/Applications/.EcoAssist_files/miniforge/etc/profile.d/conda.sh" ]; then
    source "/Applications/.EcoAssist_files/miniforge/etc/profile.d/conda.sh"
    source "/Applications/.EcoAssist_files/miniforge/bin/activate"
    conda_exe="/Applications/.EcoAssist_files/miniforge/bin/conda"
    echo "Conda found in /Applications/.EcoAssist_files/miniforge"
fi
if [ -f "$HOME/miniforge/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniforge/etc/profile.d/conda.sh"
    source "$HOME/miniforge/bin/activate"
    conda_exe="$HOME/miniforge/bin/conda"
    echo "Conda found in $HOME/miniforge"
fi

### install env-base
$conda_exe env create --file="${root}/cameratraps/envs/environment-detector-m1.yml" -p "${root}/envs/env-base"
$conda_exe activate "${root}/envs/env-base"
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
$conda_exe env create --file="${root}/EcoAssist/classification_utils/envs/tensorflow-macos-silicon.yml" -p "${root}/envs/env-tensorflow"

### install env-pytorch
$conda_exe create -p "${root}/envs/env-pytorch" python=3.8 -y
$conda_exe activate "${root}/envs/env-pytorch"
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2
pip install "ultralytics==8.0.191"
pip install "numpy==1.24.1"
pip install "humanfriendly==10.0"
pip install "jsonpickle==3.0.2"
pip install timm
pip install dill
$conda_exe deactivate

### install env-pywildlife
$conda_exe create -p "${root}/envs/env-pywildlife" python=3.8 -y
$conda_exe activate "${root}/envs/env-pywildlife"
pip install pytorchwildlife
pip install "setuptools<70"
pip install jsonpickle
$conda_exe deactivate

# create fresh pyinstaller environment
$conda_exe create -n fresh python=3.8 pyinstaller -y
$conda_exe activate fresh
pyinstaller --onefile --windowed --icon="${root}/EcoAssist/imgs/logo_small_bg.icns" --distpath="${HOME}/dist" --workpath="${HOME}/build" "${root}/main.py"
$conda_exe deactivate

# clean
$conda_exe clean --all --yes --force-pkgs-dirs
$conda_exe clean --all --yes

# move and rename executables to EcoAssist
mv "${HOME}/dist/main" "${root}/debug_mode"
mv "${HOME}/dist/main.app" "${root}/EcoAssist ${RELEASE_VERSION}.app"
