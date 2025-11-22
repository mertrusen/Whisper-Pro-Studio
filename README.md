Whisper Pro Studio 🎙️

Advanced GUI for OpenAI Whisper | Optimized for Apple Silicon M4 & Windows

Whisper Pro Studio is a modern, dark-themed, high-performance desktop application developed for OpenAI's Whisper model. It provides a professional interface for the command-line Whisper tool, designed to make transcription and translation effortless.

⚠️ Critical Prerequisites

This application is a GUI wrapper. You MUST have the following installed on your system for it to work properly.

1. FFmpeg (Required)

Essential for audio and video processing.

Mac: Run brew install ffmpeg in Terminal.

Windows: Download from ffmpeg.org and add it to your system PATH.

2. Python & Whisper (Required)

The core AI engine runs on Python.

Install Python: Version 3.10 or 3.11 is highly recommended. (Avoid 3.13+ for now due to compatibility issues).

Install Whisper: Open Terminal/CMD and run:

pip install openai-whisper


💾 Model Download Warning

IMPORTANT: On the first run or when selecting a new model size (e.g., large-v3), an AI model of approx. 2-3 GB will be automatically downloaded to your computer. This may take some time depending on your internet speed. Please be patient and do not close the app while it's processing.

⚙️ Hardware Selection Guide

To get the best performance, please select the correct device setting for your hardware:

for macOS Users:

Apple Silicon (M1 / M2 / M3 / M4): Select mps. (🚀 Performance: Ultra Fast - Recommended)

Intel Macs: Select cpu. (🐢 Performance: Slow but Stable)

Note: If you encounter errors or crashes in mps mode, please switch to cpu.

for Windows Users:

NVIDIA Graphics Card (RTX/GTX): Select cuda. (🚀 Performance: Ultra Fast - Requires CUDA drivers)

AMD Cards / No Dedicated GPU: Select cpu. (🐢 Performance: Slow but Stable)

🚀 Features

Cross-Platform: Fully compatible with macOS and Windows.

Video Preview: Built-in video player with real-time subtitle preview.

Auto-Logic: Intelligent locking system for line count and width settings.

Professional Tools: Word-level timing, gap filling (prevents flickering), smart prompting.

Multi-Format: Supports SRT, VTT, and TXT outputs.

🛠️ Installation (For Developers)

Clone the repository:

git clone [https://github.com/mertrusen/Whisper-Pro-Studio.git](https://github.com/mertrusen/Whisper-Pro-Studio.git)


Install requirements:
(Python 3.10 or 3.11 is recommended)

pip install -r requirements.txt


Run the application:

python main.py


📦 Download (For Users)

You can download the ready-to-use application (macOS .app or Windows .exe) directly from the [şüpheli bağlantı kaldırıldı] section on the right.

(Note: Don't forget to install the "Prerequisites" listed above before running the app!)

Developer: mertrusen
