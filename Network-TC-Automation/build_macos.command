#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
if [ "$(uname -s)" != "Darwin" ]; then
  echo "Run this script on macOS."
  exit 1
fi
if ! command -v python3.12 >/dev/null 2>&1; then
  echo "Python 3.12 is required on this build Mac. Install it from python.org, then retry."
  exit 1
fi
python3.12 -m venv .venv-macos
.venv-macos/bin/python -m pip install -r requirements-macos.txt
.venv-macos/bin/python -m PyInstaller --noconfirm --onedir --windowed \
  --name Network-TC-Automation --osx-bundle-identifier com.networktc.automation \
  --paths "$PWD" --hidden-import keyring.backends.macOS \
  --add-data "gui/translations.json:gui" gui/main.py
/usr/bin/ditto -c -k --sequesterRsrc --keepParent \
  dist/Network-TC-Automation.app Network-TC-Automation-macOS.zip
echo "Built: $PWD/Network-TC-Automation-macOS.zip"
echo "Open dist/Network-TC-Automation.app and test before sharing."
