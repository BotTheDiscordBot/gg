# Recap Generator

This repository contains a simple Python script `recap_generator.py` that can
create short recap videos for manhwa, anime or book titles. The script uses the
OpenAI API for text summarization, the Unsplash API for images, and gTTS for
text-to-speech.

## Requirements
- Python 3.10+
- `openai`, `requests`, `gtts`, `moviepy`

Environment variables:
- `OPENAI_API_KEY`: your OpenAI API key
- `UNSPLASH_ACCESS_KEY`: your Unsplash API key

## Usage
1. Install dependencies (requires internet access):
   ```bash
   pip install openai requests gtts moviepy
   ```
2. Run the script:
   ```bash
   python recap_generator.py
   ```
3. To build a Windows executable, use [PyInstaller](https://www.pyinstaller.org/):
   ```bash
   pyinstaller --onefile recap_generator.py
   ```

The generated video will be saved as `recap.mp4` in the current directory.
