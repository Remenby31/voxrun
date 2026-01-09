<p align="center">
  <img src="voxtral.svg" alt="Voxtral Logo" width="120">
</p>

<h1 align="center">Voxtral</h1>

<p align="center">
  <strong>Voice-controlled local AI assistant</strong>
</p>

<p align="center">
  Execute quick actions on your computer with your voice. Fully local, fully private.
</p>

---

## What is Voxtral?

Voxtral is a **voice entry point** for controlling your computer and launching AI agents locally. No cloud, no API keys, everything runs on your machine.

**Examples:**
- *"Launch Claude Code on the voxtral project and fix the login bug"*
- *"Start a Mistral agent to review my pull request"*
- *"Open Firefox and search for PyTorch documentation"*
- *"Run the tests in the backend folder"*

## Features

- **Voice-to-action** - Speak commands, execute actions
- **Agent launcher** - Start Claude Code, Mistral, or custom AI agents
- **Fully local** - Powered by Voxtral Mini 3B, runs on your GPU
- **Low VRAM** - ~3.3 GB with 4-bit quantization
- **Wayland native** - Modern overlay UI with layer-shell

## Requirements

- **GPU**: NVIDIA with ~4 GB VRAM minimum
- **RAM**: ~8 GB
- **OS**: Linux with Wayland (KDE Plasma recommended)
- **Dependencies**: PipeWire/PulseAudio, wl-clipboard, gtk4-layer-shell

## Installation

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/voxtral.git
cd voxtral

# System dependencies (Arch Linux)
sudo pacman -S python gtk4-layer-shell wl-clipboard

# Python environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install desktop entry
mkdir -p ~/.local/share/icons/hicolor/scalable/apps
cp voxtral.svg ~/.local/share/icons/hicolor/scalable/apps/
cp voxtral.desktop ~/.local/share/applications/
```

### Configure hotkey (KDE Plasma)

1. **System Settings** → **Shortcuts** → **Custom Shortcuts**
2. New → Global Shortcut → Command/URL
3. Set trigger (e.g., `Meta+V`) and action: `/path/to/voxtral/voxtral_toggle.sh`

## Usage

1. Press hotkey → Overlay appears
2. Speak your command
3. Press hotkey again → Action executed

## Memory Usage

| Component | Usage |
|-----------|-------|
| **VRAM** | ~3.3 GB |
| **RAM** | ~2-3 GB |
| **Model** | ~6 GB (one-time download) |

## Roadmap

- [ ] **Tool system** - Execute actions via voice (open apps, run commands, control agents)
- [ ] **Agent integration** - Launch Claude Code, Mistral, custom agents with voice
- [ ] **Lighter runtime** - Model caching for instant responses
- [ ] **Custom commands** - Define your own voice → action mappings

## Tech Stack

- [Voxtral Mini 3B](https://huggingface.co/mistralai/Voxtral-Mini-3B-2507) - Mistral AI
- [GTK4 + layer-shell](https://github.com/wmww/gtk4-layer-shell) - Wayland overlay
- [bitsandbytes](https://github.com/TimDettmers/bitsandbytes) - 4-bit quantization

## License

MIT
