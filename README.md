# YTGermanizer 🎥 🇩🇪

YTGermanizer is a powerful tool that automatically translates YouTube videos into German, complete with natural-sounding German voice synthesis using state-of-the-art AI technology.

## 🌟 Features

- 🎥 YouTube video downloading with yt-dlp
- 🔊 High-quality audio extraction using FFmpeg
- 📝 Speech-to-text transcription
- 🔄 Neural machine translation to German using Google Translate
- 🗣️ Advanced German text-to-speech using either:
  - Bark AI for highly natural speech
  - Tacotron2 for faster processing
- 🎬 Intelligent video-audio synchronization with pitch preservation
- ⚡ Smart media speed adjustment
- 🧹 Automatic temporary file management
- 🤖 Interactive command-line interface

## 🎮 Quick Start

1. Clone the repository
2. Set up Python environment: `python -m venv .venv && source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the app: `python src/main.py`
5. Follow the interactive prompts!

See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed setup instructions and examples.

## 🛠️ Architecture

The project is organized into modular components:

```
src/
├── main.py                    # Main application entry point
└── modules/
    ├── video_downloader.py    # YouTube video downloading (yt-dlp)
    ├── audio_extractor.py     # Audio extraction (FFmpeg)
    ├── transcriber.py         # Speech-to-text conversion
    ├── translator.py          # Neural translation (Google Translate)
    ├── tts_generator.py       # Text-to-speech (Bark/Tacotron2)
    ├── synchronizer.py        # Audio-video sync (moviepy)
    ├── media_speed_adjuster.py# Speed/pitch adjustment
    ├── file_manager.py        # File operations management
    └── cleanup.py            # Temporary file cleanup
```

## 💫 Key Features in Detail

### Advanced TTS Generation
- Dual TTS engine support (Bark and Tacotron2)
- Automatic text chunking for optimal processing
- Parallel processing for batch generation
- Smart timing adjustments for video sync

### Intelligent Media Processing
- Pitch-preserving speed adjustment
- Automatic duration harmonization
- High-quality audio extraction
- Smart file management with automatic cleanup

### Interactive Experience
- User-friendly command-line interface
- Step-by-step guidance
- Progress indicators
- Helpful error messages

### Robust File Management
- Organized directory structure:
  - `/downloads`: Main media files
  - `/downloads/temp`: Temporary processing files
  - `/downloads/output`: Final output files
- Automatic cleanup of temporary files
- Timestamp-based file naming

## 📋 Requirements

- Python 3.8+
- FFmpeg for media processing
- For Bark TTS: CUDA-capable GPU required
- For Tacotron2: CPU or GPU (GPU recommended for faster processing)
- Internet connection for:
  - YouTube video downloading
  - Google Translate API
  - Model downloads (first run)

## 💻 Hardware Requirements

### Minimum (Tacotron2 only)
- CPU: Any modern multi-core processor
- RAM: 8GB
- Storage: 2GB for models and temporary files
- GPU: Optional, but recommended for faster processing

### Recommended (For Bark)
- CPU: Modern multi-core processor
- RAM: 16GB
- Storage: 5GB for models and temporary files
- GPU: NVIDIA GPU with at least 6GB VRAM (required)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Bark](https://github.com/suno-ai/bark) for state-of-the-art TTS
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube integration
- [MoviePy](https://zulko.github.io/moviepy/) for video processing
- [FFmpeg](https://ffmpeg.org/) for media manipulation
- [Google Translate](https://translate.google.com/) for neural translation
