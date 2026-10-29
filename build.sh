#!/bin/zsh
set -e
cd "${0:A:h}"
export PYINSTALLER_CONFIG_DIR="$PWD/.build-cache"
python -m PyInstaller --noconfirm --windowed --name MacBookAccordion --osx-bundle-identifier local.bellows.accordion --collect-all basic_pitch --collect-all librosa --collect-all resampy --collect-all demucs --collect-all imageio_ffmpeg --collect-all onnxruntime --copy-metadata basic-pitch --add-data models:models --add-data THIRD_PARTY.md:. --add-data licenses:licenses main.py
