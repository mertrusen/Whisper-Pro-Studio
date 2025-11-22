# Whisper Pro Studio 🎙️

Advanced GUI for OpenAI Whisper | Optimized for Apple Silicon M4 & Windows

Whisper Pro Studio is a modern, dark-themed, high-performance desktop application developed for OpenAI's Whisper model. It provides a professional interface for the command-line Whisper tool, designed to make transcription and translation effortless.

## ⚠️ Critical Prerequisites

This application is a GUI wrapper. You MUST have the following installed on your system for it to work properly.

### 1. FFmpeg (Required)

Essential for audio and video processing.

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org) and add it to your system PATH.

### 2. Python & Whisper (Required)

The core AI engine runs on Python.

- **Python:** Version 3.10 or 3.11 is highly recommended. (Avoid 3.13+ for now due to compatibility issues).
- **Whisper:** Open Terminal/CMD and run:
```bash
pip install openai-whisper
```

## 💾 Model Download Warning

On the first run or when selecting a new model size (e.g., large-v3), an AI model of approx. 2-3 GB will be automatically downloaded to your computer. This may take some time depending on your internet speed. Please be patient and do not close the app while it's processing.

## ⚙️ Hardware Selection Guide

To get the best performance, please select the correct device setting for your hardware:

### For macOS Users 
| Hardware            | Setting | Performance | Notes |
|--------------------|--------|------------|-------|
| Apple Silicon (M1-M4) | mps    | 🚀 Ultra Fast | Recommended |
| Intel Macs          | cpu    | 🐢 Slow but Stable | Switch to this if mps crashes |

### For Windows Users 🪟
| Hardware            | Setting | Performance | Notes |
|--------------------|--------|------------|-------|
| NVIDIA GPU (RTX/GTX) | cuda   | 🚀 Ultra Fast | Requires CUDA drivers |
| AMD / No GPU        | cpu    | 🐢 Slow but Stable | Fallback mode |

## 🚀 Features

- **Cross-Platform:** Fully compatible with macOS and Windows.
- **Video Preview:** Built-in video player with real-time subtitle preview.
- **Auto-Logic:** Intelligent locking system for line count and width settings.
- **Professional Tools:** Word-level timing, gap filling (prevents flickering), smart prompting.
- **Multi-Format:** Supports .srt, .vtt, and .txt outputs.

## 🛠️ Installation (For Developers)

If you want to run the source code directly:

1. Clone the repository:
```bash
git clone https://github.com/mertrusen/Whisper-Pro-Studio.git
```

2. Install requirements:
*(Python 3.10 or 3.11 is recommended)*
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## 📦 Download (For Users)

You can download the ready-to-use application (macOS .app or Windows .exe) directly from the Releases section on the right side of this GitHub page.

**Note:** Don't forget to install the "Prerequisites" listed above before running the app!

**Developer:** mertrusen
