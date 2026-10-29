#!/bin/zsh
set -e
cd "${0:A:h}"
python3.12 -m venv .venv
.venv/bin/pip install --no-deps -r requirements-lock.txt
.venv/bin/python download_model.py
