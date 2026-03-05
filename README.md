# EVENTURI-AI for MAKCU (Apple Silicon & macOS Edition)

The ultimate AI aimbot and detection GUI, now fully optimized for **Apple Silicon (M1, M2, M3)** and Windows. This version features native **MPS (Metal Performance Shaders)** acceleration for high-speed AI detection on Mac, while maintaining full support for YOLOv8–v12 models.

Made for the MAKCU community, with custom class selection for multiple games and a super-smooth, modern UI.

---
## ⚠️ Disclaimer
This program is intended to be used as a 2pc setup.
I am not responsible for any account bans, penalties, or any other consequences that may result from using this program.
Use it at your own risk and be aware of the potential implications.

## 💬 Discord
- [Join Discord for general support](https://discord.gg/BZnZeTjN38)
- [Join Makcu Discord for Makcu Hardware Support](https://discord.gg/wHqqw5eWV5)

---

## ✨ Features (macOS & Apple Silicon)

- **Native Apple Silicon Support:** Optimized for M1/M2/M3 chips using **MPS (Metal Performance Shaders)** for GPU-accelerated inference.
- **Modern Tcl/Tk 9.0:** Built-in compatibility fixes for macOS windowing to prevent startup crashes.
- **Model Support:** Supports YOLOv8–v12 (PyTorch `.pt` and `.onnx` recommended for Mac; `.engine` for Windows/NVIDIA).
- **Device Support:** Works with standard USB serial devices:
  - MAKCU (1A86:55D3)
  - CH343 (1A86:5523)
  - CH340 (1A86:7523)
  - CH347 (1A86:5740)
  - CP2102 (10C4:EA60)
- **Fast Aim Modes:** Normal, Bezier, Silent, and the advanced **WindMouse Smooth Aim**.
- **Polished GUI:** Built with CustomTkinter for a responsive, high-tech aesthetic.

---

## 🚀 Installation & Setup

### 🍎 For macOS (Apple Silicon M1/M2/M3)

1. **Install Homebrew** (if you haven't already):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Clone the repo**:
   ```bash
   git clone https://github.com/wink05/Eventuri-AI-MAKCU-AppleSilicon.git
   cd Eventuri-AI-MAKCU-AppleSilicon
   ```

3. **Run the macOS Setup Script**:
   This will install Python 3.12, Tcl/Tk 9.0, and all necessary dependencies.
   ```bash
   chmod +x setup_macos.sh run_macos.sh
   ./setup_macos.sh
   ```

4. **Start the App**:
   ```bash
   ./run_macos.sh
   ```

---

### 🪟 For Windows (Legacy)

1. **Setup for NVIDIA (CUDA 12.6)**:
   - Install [CUDA 12.6](https://developer.nvidia.com/cuda-12-6-0-download-archive).
   - Run `install_setup_cuda.bat`.
   - Start with `run_eventuri_ai.bat`.

2. **Setup for DirectML (AMD/Intel)**:
   - Run `install_setup_directml.bat`.
   - Start with `run_eventuri_ai.bat`.

---

## 📖 Usage

1. **Connect your device:** Plug in your MAKCU or compatible serial device.
2. **Launch the app:** Use `./run_macos.sh` (Mac) or the appropriate `.bat` (Windows).
3. **Select your Model:** Choose a `.pt` or `.onnx` file from the `models/` directory in the GUI.
4. **Configure Settings:** Set your confidence, FOV, and target classes.
5. **Start Aimbot:** Click **START AIMBOT**, set your in-game sensitivity, and hold your activation key (default: Middle Mouse).

---

## ❓ FAQ (macOS Specific)

**Q: Can I use `.engine` files on Mac?**  
A: No, `.engine` files are for NVIDIA TensorRT only. Use `.pt` or `.onnx` for Apple Silicon.

**Q: Is the Debug Window supported on Mac?**  
A: macOS restricts GUI updates on background threads. If the debug window crashes, it will be automatically disabled to keep the aimbot running. For visual feedback, we recommend using NDI to a second PC.

**Q: My Mac Mini says "macOS 26 required".**  
A: This is fixed in the Apple Silicon Edition. Ensure you ran `./setup_macos.sh` to install the correct Tcl/Tk 9.0 headers.

---

## 🤝 Credits

- **Original Project:** Made with ♥ by Ahmo934 and Jealousyhaha for the MAKCU Community.
- **macOS/Apple Silicon Port:** Specialized updates for M-series compatibility.

---

Enjoy!  
If you need more help or want to suggest a feature, open an issue or pull request.
