#!/bin/bash

# Find a modern python3.12 or python3 from homebrew
BREW_PYTHON="/opt/homebrew/bin/python3.12"
if [ ! -f "$BREW_PYTHON" ]; then
    BREW_PYTHON=$(which python3.12 || which python3)
fi

echo "[*] Using Python: $BREW_PYTHON"

# Remove old venv if it exists
if [ -d "venv" ]; then
    echo "[*] Removing old virtual environment..."
    rm -rf venv
fi

# Create virtual environment
echo "[*] Creating new virtual environment with modern Tcl/Tk support..."
$BREW_PYTHON -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "[*] Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "[*] Installing dependencies for Apple Silicon..."
# Note: torch, torchvision, torchaudio should work from standard pip for MPS
# but we can also specify it just in case
pip install -r requirements_macos.txt

# Post-installation check
echo "[*] Checking for MPS support..."
python -c "import torch; print(f'MPS is available: {torch.backends.mps.is_available()}')"

echo "[+] Done! To run the app, use: ./run_macos.sh"
