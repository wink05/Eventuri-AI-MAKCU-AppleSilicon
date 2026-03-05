#!/bin/bash

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "[!] Virtual environment not found. Please run ./setup_macos.sh first."
    exit 1
fi

# Run the app
echo "[*] Starting Eventuri-AI..."
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
python src/Eventuri-AI.py
